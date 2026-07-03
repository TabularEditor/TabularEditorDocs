#!/usr/bin/env python3
"""Validate the C# code blocks in the semantic-bridge how-to docs against the live TE CLI.

Code blocks opt in via a fenced-code annotation (invisible in rendered docfx output):

    ```csharp {compile}
    ```csharp {run id=<slug> setup=<mv-sample|none> after=<id,...|none> output=<true|false>}

Semantics:
  - no annotation        -> skip (the only implicit behavior)
  - {compile}            -> compile-only (te --dry-run); catches API drift, never executes
  - {run ...}            -> execute; all four options are always required (no defaults)
        id      unique slug, names the block for after= and for reporting
        setup   a key in SETUP_SCRIPTS whose C# is prepended, or 'none'
        after   comma-separated run ids replayed (flat, in order) before this block, or 'none'
        output  'true' means the immediately-following plain fence is this block's
                documented output -- compared in compare mode, rewritten in update mode

Design: fences are parsed once into typed Block objects (the base Block is a skipped
block; CompileBlock and RunBlock add behavior). Only the parser (_classify_fence) and
the ref validator know the concrete kinds. Every command runs the same validate-first
gate (_validate); validate then reports coverage, while compile/compare/update call
block.check(mode) on every block -- each does its own work for that mode (skip: nothing;
compile: compile-check; run: compile / execute-and-compare / execute-and-update) and
reports an Outcome, which may carry an in-place fence edit (update mode). The functional
core (parsing, plan, normalize, RunBlock._diff) is pure and independently testable; the
imperative shell (Block.check, _run_mode, _write_with_edits, _report, main) does
subprocess and file IO.

Usage:
    csharp_doctest.py <validate|compile|compare|update> <file>
"""

import difflib
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, NamedTuple

from te_script_runner import Result, Snippet, run_snippets

# Setup scripts prepended before a {run setup=<key>} block. Hard-coded here for now;
# a future revision may derive them differently. The mv-sample script deserializes the
# sample Metric View from the how-to include, read at import so there is a single source
# of truth (the doc's own sample) rather than a drift-prone embedded copy.
_INCLUDE_DIR = Path(__file__).resolve().parent.parent / "content" / "how-tos" / "includes"


def _deserialize_from(yaml_path: Path) -> str:
    """A C# snippet that deserializes a Metric View from the given yaml file's contents."""
    yaml = yaml_path.read_text(encoding="utf-8")
    return f'SemanticBridge.MetricView.Deserialize("""\n{yaml}""");'


SETUP_SCRIPTS = {
    "mv-sample": _deserialize_from(_INCLUDE_DIR / "sample-metricview.yaml"),
}

# A {run} block must set exactly these options, in this order (no defaults).
RUN_OPTIONS = ("id", "setup", "after", "output")
_ALLOWED_SETUPS = {*SETUP_SCRIPTS, "none"}

# Subcommands. compile/compare/update execute against te and double as the modes passed
# to Block.check; validate only parses and reports coverage.
_EXECUTE_MODES = ("compile", "compare", "update")
_COMMANDS = ("validate", *_EXECUTE_MODES)


class Fence(NamedTuple):
    """One fenced code block: language, {...} annotation, body, 1-based opening line, and body line span."""

    lang: str
    annotation: str
    code: str
    line: int
    body_start: int  # 1-based first body line (exceeds body_end when the body is empty)
    body_end: int  # 1-based last body line


class Edit(NamedTuple):
    """An in-place rewrite of a fence body: replace 1-based lines [start, end] with text."""

    start: int
    end: int
    text: str


class Outcome(NamedTuple):
    """Result of a block's check() for a subcommand: what to print, whether it passed, and any file edit."""

    block: "Block"
    action: str  # verb shown in the report: "compile" | "compare" | "update"
    passed: bool
    detail: list[str]  # failure detail (diffs, compile/runtime errors) printed under the report line on stdout
    note: str = ""  # short status shown inline on the report line (e.g. "updated")
    edit: "Edit | None" = None  # a fence rewrite, applied in update mode


@dataclass(frozen=True)
class Block:
    """A classified code block. The base behavior is a skipped block; subclasses add
    compile/run behavior. Callers other than the parser and ref validator use this
    interface (label, summary, register_refs, check) rather than inspecting the kind."""

    code: str
    line: int
    kind: ClassVar[str] = "skip"

    @property
    def label(self) -> str:
        """Identifier shown in reports; blank when the line already identifies the block."""
        return ""

    def summary(self) -> str:
        """One-line description for the validate report."""
        return f"L{self.line}\t{self.kind}"

    def register_refs(self, seen: set[str]) -> None:
        """Validate this block's cross-references against ids seen so far, and record its own."""
        return None

    def check(self, mode: str, runs: "dict[str, RunBlock]") -> "Outcome | None":
        """Do this block's work for the subcommand mode; return an Outcome, or None if nothing to do. Imperative shell."""
        return None


@dataclass(frozen=True)
class CompileBlock(Block):
    """A {compile} block: compile-checked in every mode (compare/update imply compile), never executed."""

    kind: ClassVar[str] = "compile"

    def check(self, mode: str, runs: "dict[str, RunBlock]") -> "Outcome | None":
        # Compiled in every mode that implies compilation; strict otherwise, so an
        # unrecognized mode fails loudly rather than silently skipping the block.
        if mode in _EXECUTE_MODES:
            return _compile_check(self)
        raise ValueError(f"unknown mode: {mode}")


@dataclass(frozen=True)
class RunBlock(Block):
    """A fully-specified {run} block. documented is the following plain fence's text when output is true."""

    id: str
    setup: str
    after: tuple[str, ...]
    output: bool
    documented: str | None
    documented_span: tuple[int, int] | None  # (start, end) 1-based body lines of the documented fence
    kind: ClassVar[str] = "run"

    @property
    def label(self) -> str:
        return self.id

    def summary(self) -> str:
        after = ",".join(self.after) or "none"
        has_documented = "yes" if self.documented is not None else "no"
        return (
            f"L{self.line}\trun\tid={self.id} setup={self.setup} "
            f"after={after} output={str(self.output).lower()} documented={has_documented}"
        )

    def register_refs(self, seen: set[str]) -> None:
        if self.id in seen:
            raise ValueError(f"duplicate run id: {self.id}")
        for ref in self.after:
            if ref not in seen:
                raise ValueError(f"run {self.id!r} after={ref!r} is not a run id defined earlier")
        seen.add(self.id)

    def plan(self, runs: "dict[str, RunBlock]") -> list[str]:
        """The ordered C# scripts to execute for this block: setup + replayed after-blocks + own code. Pure.

        after is flat: only the listed blocks' own code is replayed, in order. This
        block's setup (not the referenced blocks') governs the preamble.
        """
        scripts: list[str] = []
        if self.setup != "none":
            scripts.append(SETUP_SCRIPTS[self.setup])
        scripts.extend(runs[ref].code for ref in self.after)
        scripts.append(self.code)
        return scripts

    def check(self, mode: str, runs: "dict[str, RunBlock]") -> "Outcome | None":
        if mode == "compile":
            return _compile_check(self)
        # last_only: report only this block's Output(), not the setup/after replay that
        # shares its te session (otherwise a dependency's output leaks into the diff).
        result = run_snippets([Snippet("expr", script) for script in self.plan(runs)], last_only=True)
        if mode == "compare":
            return self._compare(result)
        if mode == "update":
            return self._update(result)
        raise ValueError(f"unknown mode: {mode}")

    def _diff(self, result: Result) -> tuple[bool, str, list[str]]:
        """Compare produced output against documented output. Pure given result.

        Returns (matches, produced, diff_lines). The only place that pairs the documented
        (in-doc) and produced (fresh) outputs; both compare and update consume it.
        """
        documented = normalize(self.documented or "")
        produced = normalize(result.output)
        if produced == documented:
            return True, produced, []
        diff = difflib.unified_diff(
            documented.splitlines(),
            produced.splitlines(),
            fromfile="documented",
            tofile="produced",
            lineterm="",
        )
        return False, produced, list(diff)

    def _compare(self, result: Result) -> Outcome:
        """compare-mode verdict: produced output must match the documented fence. Pure given result."""
        if not result.success:
            return Outcome(self, "compare", False, result.diagnostics)
        if not self.output:
            return Outcome(self, "compare", True, [])
        matches, _, diff = self._diff(result)
        return Outcome(self, "compare", matches, diff)

    def _update(self, result: Result) -> Outcome:
        """update-mode verdict plus a fence edit; the command applies the edit. Pure given result.

        A failed run is reported without touching the doc. A matching or output=false
        block needs no edit; otherwise the documented fence is rewritten with produced output.
        """
        if not result.success:
            return Outcome(self, "update", False, result.diagnostics)
        if not self.output or self.documented_span is None:
            return Outcome(self, "update", True, [], note="no output")
        matches, produced, _ = self._diff(result)
        if matches:
            return Outcome(self, "update", True, [], note="unchanged")
        start, end = self.documented_span
        return Outcome(self, "update", True, [], note="updated", edit=Edit(start, end, produced))


def _annotation(info: str) -> str:
    """The text inside the first {...} of a fence info string, or '' if there is none. Pure."""
    open_brace = info.find("{")
    close_brace = info.rfind("}")
    if open_brace != -1 and close_brace > open_brace:
        return info[open_brace + 1 : close_brace].strip()
    return ""


def parse_fences(markdown: str) -> list[Fence]:
    """Extract every fenced code block from markdown, in order. Pure.

    A line whose first non-space content is ``` toggles a fence. The opening fence's
    remaining text is its info string; its first token is the language ('' for a plain
    fence) and any {...} is the annotation.
    """
    fences: list[Fence] = []
    lines = markdown.splitlines()
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith("```"):
            index += 1
            continue
        info = lines[index].lstrip()[3:].strip()
        open_line = index + 1
        body: list[str] = []
        index += 1
        body_start = index + 1  # 1-based first body line
        while index < len(lines) and not lines[index].lstrip().startswith("```"):
            body.append(lines[index])
            index += 1
        body_end = index  # 1-based last body line (< body_start when the body is empty)
        lang = "" if not info or info.startswith("{") else info.split(None, 1)[0]
        fences.append(Fence(lang, _annotation(info), "\n".join(body), open_line, body_start, body_end))
        index += 1  # step past the closing fence
    return fences


def _parse_run_options(annotation: str) -> dict[str, str]:
    """Parse and validate a {run ...} annotation's four options into a dict. Pure.

    Every option is required with a valid value -- there are no defaults, so an
    incompletely specified block is an error rather than a silent assumption.
    """
    params: dict[str, str] = {}
    for token in annotation.split()[1:]:  # [0] is "run"
        if "=" not in token:
            raise ValueError(f"run option is not key=value: {token!r}")
        key, value = token.split("=", 1)
        if key in params:
            raise ValueError(f"run block has duplicate option: {key}")
        params[key] = value
    missing = [opt for opt in RUN_OPTIONS if opt not in params]
    if missing:
        raise ValueError(f"run block missing required options: {', '.join(missing)}")
    unknown = [key for key in params if key not in RUN_OPTIONS]
    if unknown:
        raise ValueError(f"run block has unknown options: {', '.join(unknown)}")
    if params["id"] == "none":
        raise ValueError("run block id must not be 'none' (reserved sentinel for after=none)")
    # A slug id keeps ids clean and, by excluding commas, avoids colliding with the
    # after= separator (a comma'd id would be unreferenceable). Also rejects empty ids.
    if not re.fullmatch(r"[A-Za-z0-9_-]+", params["id"]):
        raise ValueError(f"run block id must be a slug of letters, digits, - or _, got {params['id']!r}")
    if params["setup"] not in _ALLOWED_SETUPS:
        raise ValueError(f"run block setup={params['setup']} is not a known setup key")
    if params["output"] not in ("true", "false"):
        raise ValueError(f"run block output must be true or false, got {params['output']!r}")
    return params


def _make_run_block(annotation: str, code: str, line: int, following: Fence | None) -> RunBlock:
    """Build a validated RunBlock, resolving documented output from the following plain fence. Pure."""
    params = _parse_run_options(annotation)
    output = params["output"] == "true"
    documented: str | None = None
    documented_span: tuple[int, int] | None = None
    if output:
        if following is None or following.lang != "":
            raise ValueError(
                f"run block {params['id']!r} (line {line}) has output=true "
                "but is not immediately followed by a plain output fence"
            )
        documented = following.code
        documented_span = (following.body_start, following.body_end)
    after = () if params["after"] == "none" else tuple(params["after"].split(","))
    return RunBlock(
        code=code,
        line=line,
        id=params["id"],
        setup=params["setup"],
        after=after,
        output=output,
        documented=documented,
        documented_span=documented_span,
    )


def _classify_fence(fence: Fence, following: Fence | None) -> Block | None:
    """Turn one fence into its typed Block, or None if it is not an actionable block. Pure.

    This and _make_run_block are the only places that map annotations to kinds.
    """
    if fence.lang != "csharp":
        # compile/run are only meaningful on csharp; flag them elsewhere rather than
        # silently ignoring a block the author expected to be executed.
        first = fence.annotation.split(None, 1)[0] if fence.annotation else ""
        if first in ("compile", "run"):
            raise ValueError(
                f"{first} annotation is only valid on a csharp block "
                f"(line {fence.line}, lang={fence.lang or 'plain'})"
            )
        return None
    annotation = fence.annotation
    if annotation == "":
        return Block(fence.code, fence.line)  # untagged -> base block (skip)
    if annotation == "compile":
        return CompileBlock(fence.code, fence.line)
    if annotation == "run" or annotation.startswith("run "):
        return _make_run_block(annotation, fence.code, fence.line, following)
    raise ValueError(f"unknown code-block annotation: {{{annotation}}}")


def build_blocks(fences: list[Fence]) -> list[Block]:
    """Classify the csharp fences into typed Blocks and validate cross-references. Pure."""
    blocks: list[Block] = []
    for position, fence in enumerate(fences):
        following = fences[position + 1] if position + 1 < len(fences) else None
        block = _classify_fence(fence, following)
        if block is not None:
            blocks.append(block)
    seen: set[str] = set()
    for block in blocks:
        block.register_refs(seen)
    return blocks


def kind_counts(blocks: list[Block]) -> Counter[str]:
    """Count blocks by kind. Pure."""
    return Counter(block.kind for block in blocks)


def index_runs(blocks: list[Block]) -> dict[str, RunBlock]:
    """Map each run block's id to itself, in document order. Pure.

    This is the one place that selects run blocks by type; callers use the map so an
    after= reference resolves to the block whose code should be replayed.
    """
    return {block.id: block for block in blocks if isinstance(block, RunBlock)}


def normalize(text: str) -> str:
    """Normalize output for comparison. Pure.

    Strict but forgiving of incidental whitespace: strip trailing whitespace from each
    line and drop trailing blank lines. Interior content must match exactly.
    """
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def _compile_check(block: Block) -> Outcome:
    """Compile-check a single block's code via te --dry-run (no execution). Imperative shell."""
    result = run_snippets([Snippet("expr", block.code)], dry_run=True)
    return Outcome(block, "compile", result.success, [] if result.success else result.diagnostics)


def _report(outcomes: list[Outcome]) -> int:
    """Print each outcome and a summary; return 1 if any failed. Imperative shell.

    Verdicts, failure detail (diffs, compile/runtime errors), and the summary are the
    report -- all on stdout. Only harness-operational problems go to stderr (raised and
    handled in main), matching how test runners like pytest/go test stream results.
    """
    failures = 0
    for outcome in outcomes:
        status = "PASS" if outcome.passed else "FAIL"
        tail = f" {outcome.block.label}" if outcome.block.label else ""
        note = f" ({outcome.note})" if outcome.note else ""
        print(f"L{outcome.block.line}\t{status}\t{outcome.action}{tail}{note}")
        if not outcome.passed:
            failures += 1
            for line in outcome.detail:
                print(f"    {line}")
    print(f"# {len(outcomes)} block(s): {len(outcomes) - failures} pass, {failures} fail")
    return 1 if failures else 0


def _validate(path: str) -> tuple[str, list[Fence], list[Block]]:
    """Parse and validate a doc's code-block annotations. Returns (text, fences, blocks). Imperative shell (reads the file).

    build_blocks raises on any malformed block, so this is the gate every command runs
    first -- compile/compare/update never touch te for a doc whose annotations are invalid.
    """
    text = Path(path).read_text(encoding="utf-8")
    fences = parse_fences(text)
    blocks = build_blocks(fences)
    return text, fences, blocks


def _run_mode(path: str, text: str, blocks: list[Block], mode: str) -> int:
    """Run compile/compare/update over already-validated blocks; apply edits; report. Imperative shell.

    Each block shells out to te against its own isolated model, so blocks are checked
    concurrently (one thread per block -- a doc has few). Results are gathered in
    document order; any fence edits (update mode) are then applied to the file in place,
    single-threaded.
    """
    runs = index_runs(blocks)
    with ThreadPoolExecutor(max_workers=max(1, len(blocks))) as pool:
        results = list(pool.map(lambda block: block.check(mode, runs), blocks))
    outcomes = [outcome for outcome in results if outcome is not None]
    edits = [outcome.edit for outcome in outcomes if outcome.edit is not None]
    if edits:
        _write_with_edits(path, text, edits)
    return _report(outcomes)


def _write_with_edits(path: str, text: str, edits: list[Edit]) -> None:
    """Apply fence-body rewrites to the file in place, bottom-up so line numbers stay valid. Imperative shell."""
    lines = text.splitlines()
    for edit in sorted(edits, key=lambda e: e.start, reverse=True):
        lines[edit.start - 1 : edit.end] = edit.text.split("\n") if edit.text else []
    Path(path).write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")


def _coverage(fences: list[Fence], blocks: list[Block]) -> None:
    """Print the validate report: one line per block plus coverage counts. Imperative shell."""
    for block in blocks:
        print(block.summary())
    counts = kind_counts(blocks)
    csharp = sum(1 for fence in fences if fence.lang == "csharp")
    breakdown = ", ".join(f"{counts[kind]} {kind}" for kind in ("run", "compile", "skip"))
    print(f"# {len(fences)} code blocks found ({csharp} csharp) | valid: {breakdown}")


def main(argv: list[str]) -> int:
    # One dispatcher for every subcommand. They share the single-path contract, the
    # filename header (so batch runs like `xargs -n1` attribute each result to its file),
    # and the validate-first gate. validate stops after the coverage report; the execute
    # commands pass their own name to _run_mode as the block.check() mode.
    if not argv or argv[0] not in _COMMANDS:
        print(f"usage: {Path(sys.argv[0]).name} <{'|'.join(_COMMANDS)}> <file>", file=sys.stderr)
        return 2
    command, rest = argv[0], argv[1:]
    if len(rest) != 1:
        print(f"{command} requires exactly one markdown file path", file=sys.stderr)
        return 2
    path = rest[0]
    print(path)
    try:
        text, fences, blocks = _validate(path)
        if command == "validate":
            _coverage(fences, blocks)
            return 0
        return _run_mode(path, text, blocks, command)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"csharp_doctest: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
