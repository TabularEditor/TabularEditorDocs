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
# Success is silent beyond the echoed commands; a failing file's full report
# is printed, and the run exits nonzero after all files have been processed.
#
# Needs the Tabular Editor CLI for everything except validate: `te` on PATH,
# or RUN_TE=/path/to/te. update REWRITES the documented outputs inside the
# markdown files.
#
# Usage:
#   ./run doctest [file.md ...]            # compare (the default)
#   ./run doctest validate [file.md ...]   # annotation coverage; no te needed
#   ./run doctest compile [file.md ...]    # compile-only (te --dry-run)
#   ./run doctest update [file.md ...]     # execute and rewrite doc outputs
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

_run_mode() {
	# run csharp_doctest.py <mode> once per file (it takes exactly one file
	# per invocation), continuing past failures so every file is reported.
	# Explicit file arguments always win; discovery of annotated content
	# files fills in only when no files are given.
	# Success is silent: each file's report is captured and printed only
	# when that file fails.
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
	local out status=0
	for f in "${files[@]}"; do
		if ! out="$(log_and_run "$RUN_PYTHON" build_scripts/csharp_doctest.py "$mode" "$f")"; then
			printf '%s\n' "$out"
			status=1
		fi
	done
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
