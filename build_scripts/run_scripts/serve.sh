#!/usr/bin/env bash

################################################################################
# Serve a local English preview at http://localhost:8080
#
# Does a full English build first (including the API reference), so it works
# from a clean tree with no prior build, then serves the result. Permissive:
# transient DocFX warnings do not block the preview. Ctrl-C stops the server.
#
# Run `./run watch` in another terminal for live rebuilds as you edit, then
# refresh the browser after each rebuild.
#
# Tool overrides (env vars): RUN_PYTHON.
#
# Usage:
#   ./run serve
#   ./run serve help
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."

serve() {
	# full English build, then serve at http://localhost:8080 (Ctrl-C stops)
	require python
	log_and_run "$RUN_PYTHON" build-docs.py --serve --permissive
}

help() {
	# show this help
	banner_help "$0"
	command_help "$0"
}

dispatch serve "$@"
