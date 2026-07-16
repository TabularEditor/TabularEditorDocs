#!/usr/bin/env bash

################################################################################
# Lint the repo's tooling
#
# Python (*.py) via uvx: ruff (F,B,SIM,I,UP) + mypy --strict.
# Shell (*.sh, and the extensionless ./run) via shellcheck.
#
# Each command takes an optional list of files; with no files it lints the
# default source lists defined at the top of this script. Runs from the repo
# root, so file arguments are repo-root-relative.
#
# Tool overrides (env vars): RUN_UVX and RUN_SHELLCHECK name the executables
# to use for uvx and shellcheck; when set, only that path is checked.
#
# Usage:
#   ./run lint                        # python + shell on the default lists
#   ./run lint file1.sh file2.py ...  # route a mixed file list by extension
#   ./run lint python [file.py ...]
#   ./run lint shell [file.sh ...]
#   ./run lint help
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."

# Default source lists: the tooling that meets the lint bar. Add files as
# they qualify.
PYTHON_SOURCES=(
	build_scripts/check_links.py
	build_scripts/te_script_runner.py
	build_scripts/csharp_doctest.py
)
SHELL_SOURCES=(run build_scripts/run_scripts/*.sh)

python() {
	# ruff + mypy --strict on the Python tooling (default: PYTHON_SOURCES)
	require uvx
	local files=("$@")
	if [ "${#files[@]}" -eq 0 ]; then
		files=("${PYTHON_SOURCES[@]}")
	fi
	log_and_run "$RUN_UVX" ruff check --quiet --select F,B,SIM,I,UP "${files[@]}"
	# --no-error-summary drops only the trailing tally line ("Found N errors
	# ..."/"Success: ..."); per-error diagnostics and the exit code are
	# unaffected, so success is silent like shellcheck.
	log_and_run "$RUN_UVX" mypy --strict --no-error-summary "${files[@]}"
}

shell() {
	# check the shell tooling with shellcheck (default: SHELL_SOURCES)
	require shellcheck
	local files=("$@")
	if [ "${#files[@]}" -eq 0 ]; then
		files=("${SHELL_SOURCES[@]}")
	fi
	log_and_run "$RUN_SHELLCHECK" --external-sources "${files[@]}"
}

all() {
	# python + shell; with file args, routes each by extension (run -> shell)
	if [ "$#" -eq 0 ]; then
		python
		shell
		return
	fi
	local py=() sh=() path
	for path in "$@"; do
		case "$path" in
		*.py) py+=("$path") ;;
		*.sh | run | */run) sh+=("$path") ;;
		*) info "lint: ignoring path with unrecognized extension: $path" ;;
		esac
	done
	if [ "${#py[@]}" -eq 0 ] && [ "${#sh[@]}" -eq 0 ]; then
		error "no lintable files among: $*"
		return 2
	fi
	if [ "${#py[@]}" -gt 0 ]; then
		python "${py[@]}"
	fi
	if [ "${#sh[@]}" -gt 0 ]; then
		shell "${sh[@]}"
	fi
}

help() {
	# show this help
	banner_help "$0"
	command_help "$0"
}

# First arg selects a command when it names one; anything else is treated as
# a file list for `all`, so `./run lint file1.sh file2.py` just works.
if declare -F "${1:-all}" >/dev/null; then
	dispatch all "$@"
else
	all "$@"
fi
