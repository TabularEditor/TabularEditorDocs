#!/usr/bin/env bash

################################################################################
# Develop the repo tooling: check, format, and scaffold the scripts themselves
#
# Commands for working on the repo's own tooling: the run scripts and the
# qualified Python build scripts. Contributing docs does not need any of
# this; see `./run setup` for the doc-contributor checks.
#
# Python rules, line length, strict mode, and the qualified-file lists live
# in pyproject.toml at the repo root; the shell file list is defined at the
# top of this script. File arguments are routed by kind (.py to the Python
# tools; .sh and the `run` dispatcher to the shell tools) and always trump
# the configured lists.
#
# Tool overrides (env vars): RUN_UVX, RUN_SHELLCHECK, RUN_SHFMT.
#
# Usage:
#   ./run scripts                     # check: linters + formatter diffs
#   ./run scripts check [file ...]    # same, explicitly
#   ./run scripts format [file ...]   # apply the formatters (writes files)
#   ./run scripts new <name>          # scaffold a new run script
#   ./run scripts setup               # check the script-development tools
#   ./run scripts help
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."

# Default shell source list: the tooling that meets the check bar. The Python
# equivalent lives in pyproject.toml (ruff include / mypy files).
SHELL_SOURCES=(run build_scripts/run_scripts/*.sh)

_check_python() {
	# non-mutating: ruff lint, ruff format diff, mypy (slowest last)
	require uvx
	log_and_run "$RUN_UVX" ruff check --quiet "$@"
	log_and_run "$RUN_UVX" ruff format --check --quiet "$@"
	# --no-error-summary drops only the trailing tally line ("Found N errors
	# ..."/"Success: ..."); per-error diagnostics and the exit code are
	# unaffected, so success is silent like shellcheck.
	log_and_run "$RUN_UVX" mypy --no-error-summary "$@"
}

_check_shell() {
	# non-mutating: shellcheck, then shfmt as a diff
	require shellcheck shfmt
	local files=("$@")
	if [ "${#files[@]}" -eq 0 ]; then
		files=("${SHELL_SOURCES[@]}")
	fi
	log_and_run "$RUN_SHELLCHECK" --external-sources "${files[@]}"
	# -s simplifies the code where possible; -d prints a diff and fails
	# when formatting is off (shfmt has no long-form flags)
	log_and_run "$RUN_SHFMT" -s -d "${files[@]}"
}

_format_python() {
	require uvx
	log_and_run "$RUN_UVX" ruff format "$@"
}

_format_shell() {
	require shfmt
	local files=("$@")
	if [ "${#files[@]}" -eq 0 ]; then
		files=("${SHELL_SOURCES[@]}")
	fi
	log_and_run "$RUN_SHFMT" -s -w "${files[@]}"
}

_route() {
	# Split file args by kind and hand them to the given python/shell
	# functions. With no files, call both with none, so each falls back to
	# its configured or default list.
	local python_fn="$1" shell_fn="$2"
	shift 2
	if [ "$#" -eq 0 ]; then
		"$python_fn"
		"$shell_fn"
		return
	fi
	local py=() sh=() path
	for path in "$@"; do
		case "$path" in
		*.py) py+=("$path") ;;
		*.sh | run | */run) sh+=("$path") ;;
		*) info "scripts: ignoring path of unrecognized kind: $path" ;;
		esac
	done
	if [ "${#py[@]}" -eq 0 ] && [ "${#sh[@]}" -eq 0 ]; then
		error "no recognized files among: $*"
		return 2
	fi
	if [ "${#py[@]}" -gt 0 ]; then
		"$python_fn" "${py[@]}"
	fi
	if [ "${#sh[@]}" -gt 0 ]; then
		"$shell_fn" "${sh[@]}"
	fi
}

check() {
	# lint and verify formatting without modifying anything: shellcheck +
	# shfmt diff on the shell tooling, ruff + format diff + mypy on the
	# Python tooling
	_route _check_python _check_shell "$@"
}

format() {
	# apply the formatters (WRITES files): shfmt on the shell tooling,
	# ruff format on the Python tooling
	_route _format_python _format_shell "$@"
}

new() {
	# scaffold a new run script with the standard anatomy and mark it
	# executable; the name becomes the subcommand (./run <name>)
	local name="${1:-}"
	case "$name" in
	"" | *[!a-z0-9-]* | -* | *-)
		error 'usage: ./run scripts new <name>  (lowercase letters, digits, and inner dashes)'
		return 2
		;;
	help | commands)
		# the run dispatcher answers these itself, so a script by either
		# name would be unreachable
		error "$name is reserved by the run dispatcher"
		return 2
		;;
	esac
	local target="$SCRIPT_DIR/$name.sh"
	if [ -e "$target" ]; then
		error "$target already exists"
		return 1
	fi
	local fn
	fn="$(printf '%s' "$name" | LC_ALL=C tr '-' '_')"
	cat "$SCRIPT_DIR"/RUN_SCRIPT_TEMPLATE >"$target"
	chmod +x "$target"
	info "Created $target."
	info "Replace every TODO (suggested function name: $fn); ./run picks the command up automatically."
}

setup() {
	# check that the script-development tools are installed and print what
	# each tool resolved to
	require shellcheck shfmt uvx || return 1
	print_resolved shellcheck shfmt uvx
	info 'All script-development tools found.'
}

help() {
	# show this help
	banner_help "$0"
	command_help "$0"
}

# First arg selects a command when it names one; anything else is treated as
# a file list for `check`, so `./run scripts file1.sh file2.py` just works.
if declare -F "${1:-check}" >/dev/null; then
	dispatch check "$@"
else
	check "$@"
fi
