#!/usr/bin/env bash

################################################################################
# Check that all required tooling is installed
#
# Verifies every dependency the run commands need: Python >= 3.11, uvx,
# and shellcheck, the te CLI, plus docfx (either the repo-local dotnet tool
# or a global install). Reports everything that is missing in one pass;
# installs nothing.
#
# Usage:
#   ./run setup
#   ./run setup help
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."

_docfx_ok () {
	# True if docfx is invocable in either form build-docs.py resolves:
	# the repo-local dotnet tool, or a docfx on PATH.
	if docfx --version >/dev/null 2>&1
	then return 0
	fi

	# This function runs inside a conditional (check's `if ! _docfx_ok`),
	# which suspends set -e; a failing require does not stop execution
	# here, so its failure must be propagated explicitly.
	require dotnet || return 1
	"$RUN_DOTNET" docfx --version >/dev/null 2>&1
}

check () {
	# verify all tooling the run commands need; report problems at once
	local failed=0
	# dotnet is not in this list: _docfx_ok requires it only when no global
	# docfx exists, so it is reported exactly once and only when relevant.
	require python shellcheck te uvx || failed=1
	if ! _docfx_ok; then
		error "docfx not found: neither 'dotnet docfx --version' nor 'docfx --version' succeeded."
		info 'See build_scripts/run_scripts/README.md for installation instructions.'
		failed=1
	fi
	if [ "$failed" -eq 0 ]; then
		info 'All dependencies found.'
	fi
	return "$failed"
}

help () {
	# show this help
	banner_help "$0"
	command_help "$0"
}

dispatch check "$@"
