# Docs tooling runner (`./run`)

`./run` in the repo root dispatches to the command scripts in this directory.
Run `./run` (or `./run help`) for the full command list, and
`./run <command> help` for details on one command.

- macOS / Linux: `./run <command>`
- Windows: use Git Bash (installed with [Git for Windows](https://gitforwindows.org/)):
  `./run <command>`, or `bash run <command>` from any shell (e.g., PowerShell) that can invoke bash.

`./run setup` checks that everything below is installed and reports all
problems in one pass. It installs nothing.

**Most common commands**:
- once: `./run setup`
- when editing (in two terminals):
  - `./run serve`: http://localhost:8080 with rendered docs
  - `./run watch`: regenerate docs whenever a file changes (manually refresh in browser to see new docs rendered)

## Requirements

| Tool   | Needed by                                           | Notes                                                       |
|--------|-----------------------------------------------------|-------------------------------------------------------------|
| bash   | everything                                          | 3.2+; Git Bash on Windows; included on most other platforms |
| Python | `build`, `serve`, `watch`, `check-links`, `doctest` | 3.11 or newer                                               |
| dotnet | docfx install and hosting                           | .NET SDK 8.0 or newer                                       |
| docfx  | `build`, `serve`, `watch`                           | local dotnet tool or global                                 |
| te     | `doctest` (all but validate)                        | Tabular Editor CLI                                          |

Working on these scripts (python and shell scripts) needs a few more tools;
see [Run script development](#run-script-development) under Contributing below.

### Installation

We provide the most common and script-friendly installation methods per platform in each section below.
If you prefer, though, you can follow these links to each tool's official installation docs

- Bash (Git for Windows): https://git-scm.com/install/windows
- Bash (non-windows): https://www.gnu.org/software/bash/
- Python: https://www.python.org/
- docfx: https://dotnet.github.io/docfx/
- te (Tabular Editor CLI): https://tabulareditor.com/download-tabular-editor-cli

#### Linux

```bash
# Python from your distro, e.g. Debian/Ubuntu:
sudo apt-get install python3
# .NET SDK (for docfx): see https://learn.microsoft.com/dotnet/core/install/linux
```

#### macOS

```bash
brew install python3
brew install --cask dotnet-sdk    # .NET SDK (for docfx)
```

#### Windows

Install [Git for Windows](https://gitforwindows.org/) for Git Bash, then:

```powershell
winget install Python.PythonInstallManager
winget install Microsoft.DotNet.SDK.10
```

Note: winget has no unversioned .NET SDK id; docfx needs SDK 8.0 or newer.

#### docfx (all platforms)

With the .NET SDK installed (see your platform above), install docfx as a
repo-local dotnet tool. From the repo root:

```bash
dotnet tool install docfx
dotnet tool restore
```

If you are running a `dotnet` older than 10.0, run `dotnet new tool-manifest` first.

#### te CLI (all platforms)

The te CLI is installed the same way on every platform:
sign in at [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli),
download the archive for your platform and architecture, extract it,
and put `te` on your PATH (or point `RUN_TE` at it).
Full instructions, including verification, live in this repo's own docs:
[te CLI install guide](../../content/features/te-cli/te-cli-install.md).

## Usage

The most common commands are provided below for reference.
All sub-commands provide help text at the command line.

- Check all dependencies are installed:
  - `./run setup`: run only to start and ensure you have the correct tools
  - `RUN_TE=/path/to/te RUN_PYTHON=/path/to/python ./run setup`: (advanced usage) confirm that tools at custom paths are resolved correctly
- Hot reloading iteration on markdown content (run in two separate terminals); likely all you need for most content contribution:
  - `./run serve`: builds docs site and launches a localhost server at http://localhost:8080 where you can browse rendered docs
  - `./run watch`: watches for changes in template files and markdown files, runs a fast rebuild upon detecting changes
- One-off build (pick one):
  - `./run build`: required after a `./run clean` or a fresh clone of the repo
  - `./run build fast`: skip re-generating the API docs; what you probably want most of the time and saves 1/3-1/2 build time
- Check the built site for broken links (needs a built site: run `./run build` first):
  - `./run check-links`: full check; fetches every unique external URL once, so it needs network access and can take a while
  - `./run check-links local`: offline; on-disk files and anchors only
- Test the annotated C# code blocks in the docs (needs the te CLI); without file args, automatically discovers all markdown files with annotated C# code blocks:
  - `./run doctest`: compile and run all annotated code blocks; compare results to `**Output**` blocks, but do not update files
  - `./run doctest file1.md file2.md`: same, for exactly the named files
  - `./run doctest update`: compile, run, and replace `**Output**` blocks in all markdown files with annotated code blocks
  - `./run doctest update file1.md path/to/file2.md`: same, but only for the named files
- Clean build artifacts: `./run clean`
- Get help:
  - `./run help`: print top-level help for the `run` dispatcher and list all subcommands
  - `./run <subcommand> help`: print full help for `<subcommand>`

### Dependency overrides

Every external tool can be pinned to a specific executable with a `RUN_<TOOL>` environment variable:
`RUN_PYTHON`, `RUN_TE` (and, for the tooling developers' tools, `RUN_UVX`, `RUN_SHELLCHECK`, `RUN_SHFMT`).
When set, that path is the only candidate checked; there is no fallback to your `PATH` environment variable.
Example:

```bash
RUN_PYTHON=/opt/python3.12/bin/python3 ./run build
RUN_PYTHON=/opt/python3.12/bin/python3 RUN_SHELLCHECK=/path/to/shellcheck ./run build
```

These environment variables are intended for testing specific versions or for users with these binaries not available in their `PATH`.

docfx is resolved by build-docs.py itself:
a `DOCFX` environment variable, then a repo-local dotnet tool manifest, then a global `docfx` on PATH.

## Contributing

This section is specifically about contributing to the run scripts themselves.
For guidance on contributing documentation content, [see the project README](../../README.md#bookmark-links-and-translations)
and the authoring guidance below that section.

### Run script development

`./run scripts` and its nested commands are the gateway to run scripts about run scripts.

- Check the script-development tools are installed: `./run scripts setup`
- Lint and verify formatting, without modifying anything (the check a PR should pass):
  - `./run scripts check`: everything (all shell tooling, the qualified Python sources)
  - `./run scripts check file1.sh file2.py ...`: specific files, routed by kind
- Apply the formatters (writes files): `./run scripts format [file ...]`
- Scaffold a new run script: `./run scripts new <name>` (creates `build_scripts/run_scripts/<name>.sh` from the anatomy below, ready to edit)

Additional requirements beyond the doc-contributor table above:

| Tool       | Needed by                    | Notes                                    |
|------------|------------------------------|------------------------------------------|
| uvx        | `scripts` (Python sources)   | part of [uv](https://docs.astral.sh/uv/) |
| shellcheck | `scripts` (shell sources)    |                                          |
| shfmt      | `scripts` (shell formatting) | [mvdan/sh](https://github.com/mvdan/sh)  |

The first `./run scripts check` needs network access: uvx downloads ruff and mypy into its cache on first use.

**Installation:**

```bash
# Linux (Debian/Ubuntu):
sudo apt-get install shellcheck shfmt
curl -LsSf https://astral.sh/uv/install.sh | sh    # uv provides uvx

# macOS:
brew install uv shellcheck shfmt
```

```powershell
# Windows:
winget install astral-sh.uv
winget install koalaman.shellcheck
winget install mvdan.shfmt
```

### Conventions for these scripts

- bash 3.2 compatible (macOS default bash), ASCII only, long-form CLI flags where a long form exists
- Shell formatted by `./run scripts format`
  (shfmt -s: tab indentation, `name() {` function style, simplifications applied)
- Python tooling formatted with ruff format (also via `./run scripts format`);
  lint rules, line length, strict mode, and the qualified-file lists live in pyproject.toml at the repo root
  (the ruff `include` and mypy `files` lists sit adjacent there and must stay in sync)
- Each script: banner help block, per-function comment docs, awk-extracted help, `dispatch <default_fn> "$@"` at the bottom
- Shared helpers live in `lib.sh`; command-specific state lives in the command's script
- All of this tooling must pass `./run scripts check`
  (shellcheck + shfmt diff for the shell sources; ruff, ruff format diff, and mypy for the Python sources)
- Any internal function not intended for re-use is prefixed with an underscore

### General architecture

Everything flows through the `run` command,
which is a dispatcher to various special-purpose scripts, exposed as subcommands to `run`.
Every subcommand is a script in this directory (run_scripts/).
The script must be named `name.sh` and `name` becomes the name of the sub-command;
there is no other registration for sub-commands, if the script exists, it's a subcommand.

#### `run` dispatcher

`run` is the script in the repo root, through which we invoke all run scripts.
It is intentionally minimal, and does only these things:

**Happy path**:

1. `cd` to the repo root, so every run script starts from the same working directory no matter where you invoke it from
2. resolve `<subcommand>` to `build_scripts/run_scripts/<subcommand>.sh` and invoke it with `bash`, passing all remaining arguments through verbatim

**`help`**: Print help (`./run`, `./run help`) and the command list (`./run commands`, `./run --list`)

**Error path**: Print an error plus the command list when the first argument does not resolve to a script

The command list is discovered by scanning this directory for `*.sh` files (excluding `lib.sh`);
the one-line description for each command is pulled from its banner comment with `banner_title`.
Anything beyond the above belongs in a run script, not in `run`.

#### `lib.sh`

Shared helpers live in [lib.sh](./lib.sh); these are intended to be used for boilerplate and common operations across sub-commands:
- `info`: print informational messages onto stderr for the user
- `error`: print error messages prefixed with "ERROR: "
- `log_and_run`: prints the command being run in bold on stderr; use for all commands that actually get run for a scripts work
- `log_cmd`: the printing half of `log_and_run` on its own;
   use when the command's execution is indirected (e.g. parallel workers whose output is captured, as in `doctest.sh`)
- `require`: automatically handle the env var for tool overrides and fail with info if the tool can't be found
- `run_var_name`: print the `RUN_<TOOL>` env var name for a tool name (the naming convention, defined in one place)
- `print_resolved`: print each given tool with the executable path its `RUN_<TOOL>` resolved to (for setup-style reports; call `require` first)
- `dispatch`: provide a way to take a default function with args (see usage in commands for examples)
- `banner_title`: print the first one-line summary of a comment banner at the top of a script file (for command lists)
- `banner_help`: print the whole comment banner at the top of a script file (for help and usage)
- `command_help`: print doc comments for each function in a script (for help output)

If you are writing or editing a run script, you should use these helpers.
If there's some new generic requirement, that's a decent candidate to be added to `lib.sh`.

#### Anatomy of a run script

All run scripts must:
- be named `<subcommand>.sh` in this directory; they are automatically discovered based on that naming convention.
- have a `#!/usr/bin/env bash` shebang, and are marked executable with `chmod +x`.
- have a comment banner with a one-line summary, help text, and usage examples
- contain the header below
- use shell functions for all functionality
- contain a standard `help` function
- use the `dispatch` pattern

##### Banner comment

A banner comment is of the form below.
This becomes the help text for this script.

```shell
###################################### (at least 10 octothorpes starting at character 0)
# One line command summary
#
# all banner comment lines must start with an octothorpe.
# provide descriptive help text
# explain what this run script does
# give any relevant details for a user running this command
# not information about the development of the command
#
# Usage:
#   ./run command          # what this invocation does
#   ./run command arg      # what *this* one does
###################################### (at least 10 octothorpes starting at character 0)
```

##### Script header

This:
1. sets up some safety defaults for Bash
2. makes sure that all scripts are executing in the same working directory context
3. sources `lib.sh` so we have the shared helpers

```shell
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."
```

##### Implementation functions

Anything that looks like an argument or a sub-subcommand is implemented as a Bash function.
The very first thing in the function definition must be comments that become the help text for this function.

Example:

```shell
fn() {
	# the help text for this function
	# can span many lines
	require ...
	<implementation>
```

These functions must declare their required tools upfront with `require`, e.g., `require uvx`;
do not use a path here, but only the exact binary name.
The sole exception is Python, which must always be written as "python" verbatim (`require` handles platform specifics for this).

Examples:
- `require uvx`
- `require python`
- `require python shellcheck uvx`

Using `require` means we get automatic environment variable handling for these things, and helpful error messages when the binaries are not available.

##### Using the `RUN_<TOOL>` variables that `require` sets up

`require` does two jobs.
1. It checks that each named tool is available,
   honoring the user's `RUN_<TOOL>` override as described in [Dependency overrides](#dependency-overrides),
2. It exports a `RUN_<TOOL>` environment variable holding the winner.
   The variable name is the tool name uppercased, with dashes turned into underscores:
   `require uvx` exports `RUN_UVX`, `require shellcheck` exports `RUN_SHELLCHECK`, `require python` exports `RUN_PYTHON`.

Always invoke a required tool through its variable, never by its bare name:

```shell
python () {
	# ruff on the Python tooling
	require uvx
	log_and_run "$RUN_UVX" ruff check --quiet "$@"
}
```

Invoking `"$RUN_UVX"` (quotes included; the path may contain spaces) is what makes a user's override actually take effect.
A bare `uvx` on that line would search the user's `PATH`, but if they provided `RUN_UVX=/other/path/to/uvx ./run scripts check`,
then they are explicitly telling us, "Use the `uvx` at the provided path, not from `PATH`,"
so we honor that.
These exports also flow into any script the current one delegates to (e.g., `watch.sh` runs `build.sh fast`, which sees the same `RUN_PYTHON`),
so an override applies consistently across a whole command.

###### How `require` failures behave

On failure, `require` prints what is missing and a pointer to this README.
When there are multiple arguments to `require`, e.g., `require python uvx`, it resolves and sets all variables.
If one or more tools are not found, then the error printed to the terminal includes details about all missing tools.
When it doesn't find all required tools then it **returns** nonzero; it never exits the script itself.
In the normal placement, at the top of a function that the user invoked directly, that is all you need:
the script header's `set -euo pipefail` turns the non-0 `return` into a clean stop.

The exception is a function that gets called inside a conditional (`if`, `!`, `&&`, `||`).
Bash suspends `set -e` for everything running inside a condition, including called functions, so a failing `require` there does not stop anything;
execution falls through to the next line as if nothing happened.
In that placement, you must propagate the failure explicitly:

```shell
require dotnet || return 1
```

`setup.sh` is the resident example: its `check` function probes helpers inside `if !` conditionals, so those helpers use the explicit form.

##### Standard `help` function

This uses `lib.sh` helpers to give a standardized help text.
These pull help text out of the banner comment and all leading comments in functions.
They are automatically formatted as you see when you run `./run help` or `./run subcommand help`.

```shell
help() {
	# show this help
	banner_help "$0"
	command_help "$0"
}
```

##### `dispatch` pattern

The last line of every run script is a call to `dispatch`:

```shell
dispatch <default_fn> "$@"
```

Read it as: "look at what the user typed after `./run <subcommand>`, and call the function with that name".

Take `build.sh`, which ends with `dispatch full "$@"`, as a worked example.
`"$@"` stands for "everything the user typed after `./run build`", so:

- When a user submits `./run build`, there is nothing after the subcommand, so we end up with `dispatch full` and nothing in `"$@"`.
  With no user input to look at, `dispatch` falls back to the default it was given and calls the `full` function.
- When a user submits `./run build fast`, we end up with `dispatch full fast`.
  `dispatch` sees the user's `fast`, finds a function with that name in the script, and calls `fast`; the `full` default is ignored.
- When a user submits `./run build nonsense`, we end up with `dispatch full nonsense`.
  There is no `nonsense` function in the script, so dispatch prints an error, then the script's `help`, and exits with a usage error.
- Anything after the function name is handed to that function as its arguments.
  In `scripts.sh` (default `check`), `./run scripts format a.py b.sh` ends up as `dispatch check format a.py b.sh`;
  dispatch calls the `format` function with `a.py b.sh` as its arguments.

Name the default function after what it does (`full`, `all`, `check`), not a generic `main`;
function names are user interface here, since they are exactly what a user types after `./run <subcommand>`.

There are exactly two correct ways to write the dispatch line:

1. The standard form shown above: `dispatch <default_fn> "$@"`.
   The default function name is required; `dispatch` always needs to know what to run when the user types nothing.
2. A wrapper around form 1, for a script that wants to handle unrecognized arguments itself instead of treating them as an error.
   For example, `scripts.sh` treats an unrecognized first argument as a list of files to check:

```shell
if declare -F "${1:-check}" >/dev/null; then
	dispatch check "$@"
else
	check "$@"
fi
```

Two mistakes to avoid:

- `dispatch "$@"` (leaving out the default) is broken, not just incomplete:
  `dispatch` would mistake the user's second argument for the name of the function to call, or crash the script when there are no arguments at all.
  If a script has no obvious default action, make `help` its default.
- `"$@"` must always be written with the quotes.
  Without them, an argument containing a space (such as a file path) gets split into pieces before `dispatch` ever sees it.


### Shell script or python?

We use shell scripts primarily for orchestration of other tools.
If you just want to provide a friendly wrapper for some more complex command,
or a bunch of reasonable defaults, then a shell script in this directory is the right choice.
If there is significant logic, data processing, or any sort of parsing, then a python script is probably the right choice.
If you build a python script that is a reasonable tool for most contributors to use,
then you should also give it a friendly run script wrapper here.
A good example of a run script wrapper improving contributor convenience is [doctest.sh](./doctest.sh);
this wraps a python tool that can only operate on one file,
and gives a run script interface that lets you pass many files,
calling the python script once for each.

### Style guidelines

Write everything as a series of small functions,
using dispatch patterns as in these run scripts and demonstrated in [`check_links.py`](../check_links.py),
[`te_script_runner.py`](../te_script_runner.py), and [`csharp_doctest.py`](../csharp_doctest.py).
This allows incremental testing and validation:
small pieces are built that do a part of the work and their logic is demonstrated to be sound;
then downstream components compose and orchestrate this functionality.
This style supports incremental validation, as well as ad hoc reuse of components.
We do not follow TDD (there are not test suites for these scripts),
but following this approach still keeps the code test*able*, which is critical.


General conventions and guidelines.

- Output routing: stdout carries only a command's real output;
  all chatter (progress, status, errors) goes to stderr via `info`/`error`,
  so output stays clean for piping and redirection.
- Success is quiet: pick tool flags that silence success output
  (e.g. ruff `--quiet`, mypy `--no-error-summary`),
  or capture a step's report and print it only on failure (as `doctest.sh` does).
  Anything printed should mean something needs attention.
- Ensure failures have non-0 exit stati;
  for anything in a pipeline or other automation, this is the sole reliable indicator of failure.
- `log_and_run` executed commands: every command that performs a script's actual work runs through `log_and_run`,
  or announces itself with `log_cmd` when its execution is indirected (see the parallel workers in `doctest.sh`);
  silent probes and internal plumbing do not.
  When delegating to another script, let the delegate echo its own commands: see `watch.sh` and `build.sh`
- Report everything at once: collect all failures (missing tools, broken files) and report them together,
  one per line, before failing; this allows a user to remediate as much as possible at once,
  rather than chasing one error at a time.
  If there is useful documentation to point to in an error context, do so; this README is a good choice.
- No silent false successes: a checker that found nothing to check must fail or say so loudly,
  never pass quietly (see the missing-root and zero-pages guards in `check_links.py`).
- Explicit user input always overrides defaults: if a user gives us filenames or sets an env var,
  we use exactly what they have provided, rather than automatic discovery or default file lists.
  See `RUN_<TOOL>` handling and all commands that accept file args.
- Run scripts should always accept multiple files, and route these files intelligently;
  see the mixed .py and .sh handling in `scripts.sh`.
- A wrapper is a chance to fix warts in what it wraps, not to reproduce them;
  when porting or wrapping existing behavior surfaces a bug, fix it.
- Use constructs portable across the BSD and GNU userlands:
  plain `tr` ranges under `LC_ALL=C` rather than `[:class:]`-plus-literal sets,
  and streaming filters rather than `sed -i` (whose flags differ between the two).
- Keep docs, comments, and implementation in sync.
- Ensure python scripts remain cleanly importable by using setup functions guarded in `if __name__ == '__main__':`.
