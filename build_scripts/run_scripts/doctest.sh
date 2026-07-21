#!/usr/bin/env bash

################################################################################
# Test the annotated C# code blocks in the docs against the te CLI
#
# Wraps build_scripts/csharp_doctest.py. Code blocks in content markdown opt
# in with a fenced-code annotation (```csharp {compile} or
# ```csharp {run ...}); see the header of csharp_doctest.py for the
# annotation reference. With no file arguments, every annotated markdown
# file under content/ is processed; having none is fine (reported, exit 0).
#
# Files are processed in parallel, at most DOCTEST_JOBS at a time (default
# 4; each invocation runs against its own throwaway model, and update only
# writes its own markdown file). Results print in the order files finish:
# every file's command line, plus the full report (including te's own
# stderr) only when that file failed. The run exits nonzero if any file
# failed.
#
# Needs the Tabular Editor CLI for everything except validate: `te` on PATH,
# or RUN_TE=/path/to/te. update REWRITES the documented outputs inside the
# markdown files.
#
# NOTE: The correctness of the results of doctest` depend entirely on the
#       alignment of your te CLI version with the scripting surface area
#       being documented. If your te version is out of date, you may see false
#       error reports from this command.
#
# Usage:
#   ./run doctest [file.md ...]            # compare (the default)
#   ./run doctest validate [file.md ...]   # annotation coverage; no te needed
#   ./run doctest compile [file.md ...]    # compile-only (te --dry-run)
#   ./run doctest update [file.md ...]     # execute and rewrite doc outputs
#   DOCTEST_JOBS=N ./run doctest           # run at most N jobs at once
#   ./run doctest help
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."

_annotated_files() {
	# print the content markdown files containing annotated csharp fences
	grep --recursive --files-with-matches --include='*.md' -- '```csharp {' content || true
}

_run_one() {
	# xargs worker: run one file, echo its command line on completion, and
	# print its captured report (stdout and stderr, so parallel te chatter
	# never interleaves) only on failure, as a single write so concurrent
	# reports stay intact.
	local -a cmd=("$RUN_PYTHON" build_scripts/csharp_doctest.py "$1" "$2")
	local out
	if out="$("${cmd[@]}" 2>&1)"; then
		log_cmd "${cmd[@]}"
	else
		log_cmd "${cmd[@]}"
		printf '%s\n' "$out"
		return 1
	fi
}

_run_mode() {
	# run csharp_doctest.py <mode> once per file (it takes exactly one file
	# per invocation), at most DOCTEST_JOBS files at a time. Each file's
	# own blocks already run in parallel inside csharp_doctest.py (one te
	# per block), so an unbounded file-level fan-out would oversubscribe
	# the machine. Explicit file arguments always win; discovery of
	# annotated content files fills in only when no files are given.
	local mode="$1"
	shift
	local files=("$@") f
	if [ "${#files[@]}" -eq 0 ]; then
		while IFS= read -r f; do
			files+=("$f")
		done < <(_annotated_files)
	fi
	if [ "${#files[@]}" -eq 0 ]; then
		info 'doctest: no annotated C# blocks found under content/; nothing to do'
		return 0
	fi

	# The xargs-spawned worker shells receive these through the environment.
	export -f _run_one log_cmd

	# xargs runs the workers and refills free slots as files finish, so
	# results print in finish order. Embedding $mode is safe: dispatch
	# already resolved it to one of this script's function names. xargs
	# exits 123 when any invocation failed (BSD and GNU alike).
	local status=0
	printf '%s\0' "${files[@]}" |
		xargs -0 -n 1 -P "${DOCTEST_JOBS:-4}" bash -c "_run_one $mode \"\$1\"" _ || status=1
	return "$status"
}

validate() {
	# check annotation correctness: report on malformed annotations.
	# no te requirement
	require python
	_run_mode validate "$@"
}

compile() {
	# compile every annotated block via te --dry-run; catches API drift
	# without executing anything
	require python te
	_run_mode compile "$@"
}

compare() {
	# execute annotated blocks and compare their documented outputs
	require python te
	_run_mode compare "$@"
}

update() {
	# execute annotated blocks and REWRITE the documented outputs in the
	# markdown files in place
	require python te
	_run_mode update "$@"
}

help() {
	# show this help
	banner_help "$0"
	command_help "$0"
}

# First arg selects a command when it names one; anything else passes through
# to `compare` as file paths, so `./run doctest some-doc.md` just works.
if declare -F "${1:-compare}" >/dev/null; then
	dispatch compare "$@"
else
	compare "$@"
fi
