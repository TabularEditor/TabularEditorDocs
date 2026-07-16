#!/usr/bin/env bash

################################################################################
# Build the English docs for local iteration
#
# Wraps the canonical build-docs.py orchestration; no parallel build logic.
# Never touches the localized es/zh content.
#
#   full  (default) regenerate the API reference; reuse the generated
#         docfx.json configs; fail on DocFX warnings
#   fast  also reuse existing API metadata and tolerate DocFX warnings;
#         the same build that `watch` runs
#
# Tool overrides (env vars): RUN_PYTHON.
#
# Usage:
#   ./run build [full|fast]
#   ./run build help
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."

common_flags() {
	# Set FLAGS to the markdown-iteration base: English only, and reuse the
	# generated docfx.json configs (--skip-gen) when they exist. After a
	# `clean` they do not, so the generation step runs on the next build.
	FLAGS=(--lang en)
	if [ -f localizedContent/en/docfx.json ] && [ -f metadata/languages.json ]; then
		FLAGS+=(--skip-gen)
	fi
}

full() {
	# regenerate the API reference; fail on DocFX warnings
	require python
	common_flags
	log_and_run "$RUN_PYTHON" build-docs.py "${FLAGS[@]}"
}

fast() {
	# reuse existing API metadata (--skip-api); tolerate DocFX warnings
	# (--permissive); the build that watch runs after each save
	require python
	common_flags
	log_and_run "$RUN_PYTHON" build-docs.py "${FLAGS[@]}" --skip-api --permissive
}

help() {
	# show this help
	banner_help "$0"
	command_help "$0"
}

dispatch full "$@"
