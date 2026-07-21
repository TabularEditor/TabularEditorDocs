#!/usr/bin/env bash

################################################################################
# Check the built site for broken links
#
# Wraps build_scripts/check_links.py: walks the built HTML in _site, resolves
# every href/src to a local file or external URL, and reports references to
# broken targets. Local failures (missing files or anchors) are errors and
# fail the run; external failures are warnings, listed for verification by
# hand. Needs a built site: run `./run build` first.
#
# The full check fetches every unique external URL once, so it needs network
# access and can take a while; `local` stays entirely on disk.
#
# Arguments pass through to check_links.py validate:
#   local           skip external fetching (on-disk checks only; offline)
#   all             include generated API and localized pages
#                   (default: authored content only)
#   stats           print per-host fetch diagnostics
#   under=<path>    only check links from pages under _site/<path>
#
# Tool overrides (env vars): RUN_PYTHON.
#
# Usage:
#   ./run check-links               # full check (fetches external URLs)
#   ./run check-links local         # offline: on-disk checks only
#   ./run check-links local all     # offline, including generated pages
#   ./run check-links help
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."

check() {
	# validate the built site; args pass through to check_links.py validate
	require python
	log_and_run "$RUN_PYTHON" build_scripts/check_links.py validate "$@"
}

help() {
	# show this help
	banner_help "$0"
	command_help "$0"
}

# First arg selects a command when it names one; anything else passes through
# to `check` as validate arguments, so `./run check-links local` just works.
if declare -F "${1:-check}" >/dev/null; then
	dispatch check "$@"
else
	check "$@"
fi
