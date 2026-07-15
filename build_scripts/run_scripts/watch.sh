#!/usr/bin/env bash

################################################################################
# Rebuild the English docs on every save
#
# Polling loop: watches content/ and templates/ and runs the fast build
# (build.sh fast) whenever a file changes. Zero dependencies beyond the build
# itself; the ~1s poll latency is nothing next to the build time, and rapid
# saves coalesce into one rebuild. Ctrl-C to stop.
#
# Run alongside `./run serve` in another terminal, then refresh the browser
# after each rebuild.
#
# Usage:
#   ./run watch
#   ./run watch help
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."

watch () {
	# poll content/ and templates/; run the fast build on each change
	require python
	info "Watching content/ and templates/ for changes (Ctrl-C to stop)..."
	# stamp is intentionally a script global (not local) so the EXIT trap
	# can still reference it when the loop is interrupted.
	stamp="$(mktemp)"
	trap 'rm -f "$stamp"' EXIT
	while true; do
		if find content templates -type f -newer "$stamp" -print -quit | grep -q .; then
			touch "$stamp"
			bash "$SCRIPT_DIR/build.sh" fast || true
			info ''
			info "--- rebuilt $(date +%T) - refresh your browser ---"
		fi
		sleep 1
	done
}

help () {
	# show this help
	banner_help "$0"
	command_help "$0"
}

dispatch watch "$@"
