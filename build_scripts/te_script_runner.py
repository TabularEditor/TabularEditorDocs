#!/usr/bin/env python3
"""Run C# script snippets against a throwaway, empty semantic model via the TE CLI.

Two uses:

1. Standalone CLI (a subcommand is required):
       te_script_runner.py run -e '<C# expr>'                # execute
       te_script_runner.py run -f a.cs -e '<expr>' -f b.cs   # many, in order
       te_script_runner.py check -f a.cs                     # compile-check only, no execution
       cat snippet.cs | te_script_runner.py run              # one snippet on stdin
   run and check take the same script arguments.

2. Importable by an orchestrator (e.g. a semantic-bridge doc runner):
       from te_script_runner import Snippet, run_snippets
       result = run_snippets([Snippet("expr", preamble), Snippet("file", "block.cs")])

The functional core (summarize and its helpers) is pure and independently
testable; the imperative shell (init_model, run_snippets, the cmd_* wrappers)
does subprocess, filesystem, and printing. Every layer is exposed as a COMMANDS
subcommand so it can be exercised on its own.

Snippets always run against a fresh empty model with no --save: nothing is
persisted and nothing outside the throwaway directory is touched. Callers that
need setup (e.g. a loaded Metric View) pass it as the first snippet.

Usage:
    te_script_runner.py <command> [args]
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import Any, NamedTuple

# RUN_TE is the ./run tooling's override convention (see
# build_scripts/run_scripts/README.md); honoring it here means a pinned te
# applies to everything built on this module.
DEFAULT_TE_BIN = os.environ.get("RUN_TE", "te")
_WORKDIR_PREFIX = "te-script-run."
# Emitted between the next-to-last and last script when last_only is set, so the runner
# can report only the final script's output. Chosen to be absent from any real output.
_OUTPUT_BOUNDARY = "<<<te-script-runner-output-boundary>>>"


class Result(NamedTuple):
    """Outcome of a script run, distilled from te's --output-format json stdout.

    output is the snippets' Output() text (newline-joined) -- what a caller
    compares against expected. diagnostics are tagged non-output lines (compile
    errors, runtime error, other messages) derived from the json. te's own stderr
    is never captured -- it inherits the parent's stderr and always prints in full
    -- so it does not appear here.
    """

    exit_code: int
    success: bool
    output: str
    diagnostics: list[str]


class Snippet(NamedTuple):
    """One C# snippet: an inline expression (kind='expr') or a path to a file (kind='file')."""

    kind: str
    value: str


def _parse_json(stdout: str) -> dict[str, Any] | None:
    """te's json object, or None if stdout is empty or not a json object. Pure."""
    if not stdout.strip():
        return None
    try:
        parsed = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _output_lines(data: dict[str, Any]) -> list[str]:
    """The text of every output-level message, in order. Pure."""
    messages = data.get("messages") or []
    return [str(m.get("text", "")) for m in messages if isinstance(m, dict) and m.get("level") == "output"]


def _diagnostic_lines(data: dict[str, Any]) -> list[str]:
    """Tagged non-output diagnostics: compile errors, runtime error, other messages. Pure.

    te reports failures in three shapes -- compileErrors[], a runtimeError string,
    and non-output messages[] -- and any of them can be present, so all three are
    surfaced rather than only the first.
    """
    lines = [f"[compile-error] {e}" for e in data.get("compileErrors") or []]
    runtime_error = data.get("runtimeError")
    if runtime_error:
        lines.append(f"[runtime-error] {runtime_error}")
    lines += [
        f"[{m.get('level')}] {m.get('text')}"
        for m in data.get("messages") or []
        if isinstance(m, dict) and m.get("level") != "output"
    ]
    return lines


def _summarize_dry_run(data: dict[str, Any], exit_code: int) -> Result:
    """Compile-only (--dry-run) results into a Result. Pure.

    --dry-run reports a different shape than an executed run: a per-script
    success/errors list under "scripts" and no messages, because nothing runs.
    There is therefore no output; a compile failure in any script fails the whole.
    """
    scripts = data.get("scripts") or []
    diagnostics: list[str] = []
    all_ok = True
    for script in scripts:
        if not isinstance(script, dict):
            continue
        all_ok = all_ok and bool(script.get("success", False))
        source = str(script.get("source", "<script>"))
        diagnostics += [f"[compile-error] {source}: {e}" for e in script.get("errors") or []]
    return Result(exit_code=exit_code, success=all_ok, output="", diagnostics=diagnostics)


def summarize(stdout: str, exit_code: int) -> Result:
    """Turn te's json stdout and exit code into a Result. Pure functional core.

    Handles both te json shapes: an executed run (messages/compileErrors/
    runtimeError) and a compile-only --dry-run (dryRun/scripts). When te emits no
    json but failed, that fact is itself surfaced as a diagnostic so a failure is
    never silently swallowed.
    """
    data = _parse_json(stdout)
    if data is None:
        diagnostics = [f"[te] failed with exit {exit_code} and no json output"] if exit_code != 0 else []
        return Result(exit_code, exit_code == 0, "", diagnostics)
    if data.get("dryRun"):
        return _summarize_dry_run(data, exit_code)
    return Result(
        exit_code=exit_code,
        success=bool(data.get("success", exit_code == 0)),
        output="\n".join(_output_lines(data)),
        diagnostics=_diagnostic_lines(data),
    )


def parse_snippet_args(args: Sequence[str]) -> list[Snippet]:
    """Parse repeated -e/-f arguments into ordered Snippets. Pure.

    Order across -e and -f is preserved because the run relies on handing te one
    ordered --script list (te otherwise runs all --script before all -e).
    """
    snippets: list[Snippet] = []
    index = 0
    while index < len(args):
        flag = args[index]
        if flag in ("-e", "--expression"):
            kind = "expr"
        elif flag in ("-f", "--file"):
            kind = "file"
        else:
            raise ValueError(f"unexpected argument: {flag}")
        if index + 1 >= len(args):
            raise ValueError(f"{flag} requires a value")
        snippets.append(Snippet(kind, args[index + 1]))
        index += 2
    return snippets


def _emit(result: Result) -> int:
    """Write a Result to the real streams the way the standalone CLI should. Imperative shell.

    te's own stderr has already streamed through (it is never captured), so this
    only adds the snippets' Output() to stdout and the derived diagnostics to stderr.
    """
    if result.output:
        print(result.output)
    if result.diagnostics:
        print("\n".join(result.diagnostics), file=sys.stderr)
    return result.exit_code


def init_model(model_path: Path, *, te_bin: str = DEFAULT_TE_BIN) -> Path:
    """Create an empty single-file .bim model at model_path and return its path. Imperative shell.

    Adds no output of its own: te init's stdout summary is discarded (the throwaway
    model is an implementation detail). Its stderr inherits the parent's and prints
    in full. Raises on failure; the detail has already printed on stderr.
    """
    proc = subprocess.run(
        [te_bin, "init", str(model_path), "--serialization", "bim"],
        stdout=subprocess.DEVNULL,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"te init failed (exit {proc.returncode}); see stderr above")
    return model_path


def materialize(snippets: Sequence[Snippet], snippet_dir: Path) -> list[Path]:
    """Write every snippet to a .cs file under snippet_dir, preserving order. Imperative shell.

    Inline expressions become numbered files; file snippets are used in place after
    an existence check. All are handed to te as --script (see parse_snippet_args).
    """
    snippet_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for index, snippet in enumerate(snippets, start=1):
        if snippet.kind == "expr":
            path = snippet_dir / f"{index:02d}-inline.cs"
            path.write_text(snippet.value + "\n", encoding="utf-8")
        else:
            path = Path(snippet.value)
            if not path.is_file():
                raise FileNotFoundError(f"script file not found: {snippet.value}")
        files.append(path)
    return files


def run_te_script(
    model_path: Path,
    script_files: Sequence[Path],
    *,
    te_bin: str = DEFAULT_TE_BIN,
    dry_run: bool = False,
) -> tuple[int, str]:
    """Run script files in order against model_path in one te session. Imperative shell.

    Returns (exit_code, json_stdout). One session means mutations carry across the
    files. With dry_run, te compiles the scripts and reports errors without executing
    them (a different json shape; summarize handles both). stdout is captured for
    summarize; stderr inherits the parent's and prints in full. No --save, so nothing
    is persisted.
    """
    cmd = [te_bin, "--output-format", "json", "script", str(model_path)]
    for path in script_files:
        cmd += ["--script", str(path)]
    if dry_run:
        cmd.append("--dry-run")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return proc.returncode, proc.stdout


def _keep_after_boundary(result: Result) -> Result:
    """Drop everything up to and including the last-only boundary marker. Pure.

    The scripts run in one te session (the only way shared state, e.g. a loaded Metric
    View, survives), so te reports every script's output in one flat list. To report
    only the final script's output, a boundary marker is emitted just before it and
    everything up to it is dropped here.

    A failed run (any script errors -> te stops) is returned unchanged, with the full
    output and diagnostics -- the whole invocation failed. If the run succeeded but the
    marker is missing, that is also treated as a failure rather than silently trusted.
    """
    if not result.success:
        return result
    lines = result.output.split("\n") if result.output else []
    if _OUTPUT_BOUNDARY not in lines:
        return result._replace(
            exit_code=result.exit_code or 1,
            success=False,
            diagnostics=[*result.diagnostics, "[harness] output boundary marker missing"],
        )
    cut = len(lines) - 1 - lines[::-1].index(_OUTPUT_BOUNDARY)  # last occurrence is ours
    return result._replace(output="\n".join(lines[cut + 1 :]))


def run_snippets(
    snippets: Sequence[Snippet],
    *,
    te_bin: str = DEFAULT_TE_BIN,
    keep_workdir: bool = False,
    dry_run: bool = False,
    last_only: bool = False,
) -> Result:
    """Run snippets in order against one fresh, empty .bim model; return a Result. Imperative shell.

    This is the importable entry point. With dry_run the snippets are compiled but not
    executed (Result.output is empty; compile errors land in Result.diagnostics). With
    last_only, only the final snippet's Output() is reported (earlier snippets are setup
    whose output is noise); this is done by emitting a boundary marker before the last
    script and dropping everything up to it -- necessary because the snippets share one
    te session and te reports all their output in one flat list. It adds no output of its
    own (only te's inherited stderr streams through), so an orchestrator can consume the
    Result as data. The throwaway directory is always removed unless keep_workdir. Raises
    if te is missing or the model cannot be created.
    """
    if not snippets:
        raise ValueError("run_snippets requires at least one snippet")
    if shutil.which(te_bin) is None:
        raise FileNotFoundError(f"{te_bin!r} (Tabular Editor CLI) not found on PATH")
    workdir = Path(tempfile.mkdtemp(prefix=_WORKDIR_PREFIX))
    try:
        model_path = init_model(workdir / "model.bim", te_bin=te_bin)
        snippet_dir = workdir / "snippets"
        script_files = materialize(snippets, snippet_dir)
        bounded = last_only and not dry_run and len(script_files) > 1
        if bounded:
            boundary = snippet_dir / "00-boundary.cs"
            boundary.write_text(f'Output("{_OUTPUT_BOUNDARY}");\n', encoding="utf-8")
            script_files = [*script_files[:-1], boundary, script_files[-1]]
        exit_code, stdout = run_te_script(model_path, script_files, te_bin=te_bin, dry_run=dry_run)
        result = summarize(stdout, exit_code)
        return _keep_after_boundary(result) if bounded else result
    finally:
        if keep_workdir:
            print(f"[keep] throwaway dir retained: {workdir}", file=sys.stderr)
        else:
            shutil.rmtree(workdir, ignore_errors=True)


def _gather_snippets(args: list[str]) -> tuple[list[Snippet], bool]:
    """Parse the shared -e/-f/--keep args (or read one snippet from stdin). Returns (snippets, keep).

    run and check take identical script arguments; this is where that shared parse lives.
    """
    keep = "--keep" in args
    snippets = parse_snippet_args([a for a in args if a != "--keep"])
    if not snippets:
        if sys.stdin.isatty():
            raise ValueError("no snippet provided; use -e, -f, or pipe C# on stdin")
        snippets = [Snippet("expr", sys.stdin.read())]
    return snippets, keep


def cmd_run(args: list[str]) -> int:
    """Execute snippets from -e/-f (in order) or stdin against a throwaway model. --keep retains the dir."""
    snippets, keep = _gather_snippets(args)
    return _emit(run_snippets(snippets, keep_workdir=keep))


def cmd_check(args: list[str]) -> int:
    """Compile-check snippets from -e/-f (in order) or stdin without executing them. --keep retains the dir."""
    snippets, keep = _gather_snippets(args)
    return _emit(run_snippets(snippets, keep_workdir=keep, dry_run=True))


def cmd_init(args: list[str]) -> int:
    """Create an empty .bim model at <path> and print the path (for testing the init step)."""
    if not args:
        raise ValueError("init requires a model path")
    print(init_model(Path(args[0])))
    return 0


def cmd_summarize(args: list[str]) -> int:
    """Summarize te json from <file> (or stdin if '-'), at optional [exit_code] (default 0)."""
    stdout = sys.stdin.read() if not args or args[0] == "-" else Path(args[0]).read_text(encoding="utf-8")
    exit_code = int(args[1]) if len(args) > 1 else 0
    return _emit(summarize(stdout, exit_code))


COMMANDS = {
    "run": cmd_run,
    "check": cmd_check,
    "init": cmd_init,
    "summarize": cmd_summarize,
}


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in COMMANDS:
        print(f"usage: {Path(sys.argv[0]).name} <{'|'.join(COMMANDS)}> [args]", file=sys.stderr)
        return 2
    try:
        return COMMANDS[argv[0]](argv[1:])
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"te_script_runner: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
