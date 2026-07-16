#!/usr/bin/env bash

################################################################################
# Remove generated build artifacts
#
# Deletes the DocFX build outputs and generated configs: _site, obj, the
# generated docfx.json files, generated API reference yml, language metadata,
# and the localized-content staging outputs. Everything removed is gitignored;
# tracked source is never touched.
#
# Usage:
#   ./run clean
#   ./run clean help
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build_scripts/run_scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"
cd "$SCRIPT_DIR/../.."

clean() {
	# remove all generated build artifacts (gitignored); tracked source is
	# left intact
	log_and_run rm -rf _site obj docfx.json
	log_and_run rm -f content/api/*.yml content/api/.manifest
	log_and_run rm -f metadata/languages.json
	log_and_run rm -rf localizedContent/en
	log_and_run find localizedContent -maxdepth 2 -name docfx.json -delete || true
	# Generated files only: each localized content/api keeps a tracked
	# index.md, so the whole directory must not be removed.
	log_and_run rm -f localizedContent/*/content/api/*.yml localizedContent/*/content/api/.manifest
	log_and_run rm -rf localizedContent/*/content/assets
	info "Clean complete."
}

help() {
	# show this help
	banner_help "$0"
	command_help "$0"
}

dispatch clean "$@"
