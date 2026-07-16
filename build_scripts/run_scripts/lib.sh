#!/usr/bin/env bash
# Shared helpers for the ./run command scripts.
#
# Sourced as a library by the command scripts in this directory, or executed
# directly to exercise a single helper:
#   bash build_scripts/run_scripts/lib.sh require git python3

# Status/progress chatter, on stderr so stdout stays clean for command output.
info() { printf '%s\n' "$*" >&2; }

# Error message with a uniform prefix, on stderr.
error() { printf 'ERROR: %s\n' "$*" >&2; }

# Print a command line without running it, bold (like just's recipe echo)
# with a "$ " prefix. Goes to stderr so a command's stdout stays clean for
# its own output; escape codes only when stderr is a terminal and NO_COLOR
# is unset, so redirected output stays plain. Use directly when the command
# itself runs indirected (e.g. backgrounded with captured output).
log_cmd() {
	if [ -t 2 ] && [ -z "${NO_COLOR:-}" ]; then
		printf '\033[1m$ %s\033[0m\n' "$*" >&2
	else
		printf '$ %s\n' "$*" >&2
	fi
}

# Print a command then execute it.
log_and_run() {
	log_cmd "$@"
	"$@"
}

run_var_name() {
	# Print the RUN_<NAME> variable name for a tool (uppercased, dashes to
	# underscores: uvx -> RUN_UVX). The single source of the require naming
	# convention. LC_ALL=C pins ASCII range semantics regardless of locale.
	printf 'RUN_%s' "$(printf '%s' "$1" | LC_ALL=C tr 'a-z-' 'A-Z_')"
}

require() {
	# Check the given tools and resolve which executable to use for each.
	# Takes bare tool names, not paths. A pre-set RUN_<NAME> env var (name
	# uppercased, dashes to underscores: RUN_UVX for uvx, RUN_SHELLCHECK
	# for shellcheck) is a user override and is the only candidate checked
	# otherwise the tool must be on PATH. The winner is exported as
	# RUN_<NAME> for callers to invoke and for delegated scripts to
	# inherit. Failures are reported all at once.
	# The name `python` is special: it delegates to _require_python, which
	# version-gates the interpreter and reports its own detail.
	local missing=() cmd var val failed=0
	for cmd in "$@"; do
		if [ "$cmd" = "python" ]; then
			_require_python || failed=1
			continue
		fi
		var="$(run_var_name "$cmd")"
		val="${!var:-$cmd}"
		if command -v "$val" >/dev/null 2>&1; then
			export "$var=$val"
		elif [ "$val" = "$cmd" ]; then
			missing+=("$cmd")
		else
			missing+=("$cmd ($var=$val not found)")
		fi
	done
	if [ "${#missing[@]}" -gt 0 ]; then
		error 'missing required command(s):'
		for cmd in "${missing[@]}"; do
			info "  $cmd"
		done
		info 'See build_scripts/run_scripts/README.md for installation instructions.'
		return 1
	fi
	return "$failed"
}

_python_ok() {
	# True if the given interpreter exists and is Python >= 3.11 (the
	# version floor for the repo's build tooling, matching CI).
	command -v "$1" >/dev/null 2>&1 &&
		"$1" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1
}

_require_python() {
	# Locate a Python >= 3.11 and export it as RUN_PYTHON for commands to
	# invoke. When RUN_PYTHON is already set (contributor override) it is
	# the ONLY candidate checked, so a broken override fails loudly instead
	# of silently falling back. Otherwise probe python3, python, then the
	# Windows launcher (py -3, resolved to its underlying executable so
	# RUN_PYTHON stays a single quotable word). On failure, reports the
	# version of every candidate that was present.
	local cand tried=""
	if [ -n "${RUN_PYTHON:-}" ]; then
		if _python_ok "$RUN_PYTHON"; then
			export RUN_PYTHON
			return 0
		fi
		error "RUN_PYTHON=$RUN_PYTHON is not a Python >= 3.11."
		if command -v "$RUN_PYTHON" >/dev/null 2>&1; then
			info "  found: $("$RUN_PYTHON" --version 2>&1 || true)"
		fi
		info 'See build_scripts/run_scripts/README.md for installation instructions.'
		return 1
	fi

	for cand in python3 python; do
		if _python_ok "$cand"; then
			RUN_PYTHON="$cand"
			export RUN_PYTHON
			return 0
		fi
		if command -v "$cand" >/dev/null 2>&1; then
			tried="$tried
  $cand: $("$cand" --version 2>&1 || true)"
		fi
	done

	if command -v py >/dev/null 2>&1; then
		cand="$(py -3 -c 'import sys; print(sys.executable)' 2>/dev/null || true)"
		if [ -n "$cand" ] && _python_ok "$cand"; then
			RUN_PYTHON="$cand"
			export RUN_PYTHON
			return 0
		fi
		tried="$tried
  py -3: $(py -3 --version 2>&1 || true)"
	fi

	error "Python >= 3.11 is required and was not found."
	if [ -n "$tried" ]; then
		info "Candidates checked:$tried"
	fi
	info 'Set RUN_PYTHON to a suitable interpreter, or see build_scripts/run_scripts/README.md for installation instructions.'
	return 1
}

print_resolved() {
	# Print each tool name with the executable path its RUN_<TOOL> variable
	# resolved to. Call require on the tools first.
	local tool var
	for tool in "$@"; do
		var="$(run_var_name "$tool")"
		printf '  %-11s %s\n' "$tool" "$(command -v "${!var}")"
	done
}

dispatch() {
	# dispatch <default_fn> [args...]: call the function named by the first
	# remaining arg, or default_fn when none is given. Unknown names print
	# the calling script's help and fail with a usage error.
	local fn="${2:-$1}"
	shift
	if [ "$#" -gt 0 ]; then
		shift
	fi
	if declare -F "$fn" >/dev/null; then
		"$fn" "$@"
	else
		error "unknown command: $fn"
		if declare -F help >/dev/null; then
			help
		fi
		return 2
	fi
}

banner_title() {
	# Print only the first line of the #### banner block of the given script
	# (used by ./run for its one-line-per-command index).
	awk '
		/^#{10,}/ { if (inIntro) exit; inIntro=1; next }
		inIntro && /^#/ { gsub(/^# ?/, ""); print; exit }
	' "$1"
}

banner_help() {
	# Print the #### banner block at the top of the given script, unprefixed.
	awk '
		BEGIN { inIntro=0; introDone=0 }
		/^#{10,}/ && introDone==0 && inIntro==0 { inIntro=1; next }
		/^#{10,}/ && inIntro==1 { inIntro=0; introDone=1; print ""; next }
		inIntro==1 { gsub(/^# ?/, ""); print }
	' "$1"
}

command_help() {
	# Print each function in the given script with its leading comment lines.
	# Underscore-prefixed functions are internal and excluded.
	printf 'Commands:\n'
	awk '
		/^[a-z][a-z_]* *\(\) *\{/ { fn=$1; sub(/\(\)$/, "", fn); inCmd=1; next }
		inCmd==1 && /^[ \t]+#/ {
			if (fn != "") { print "  " fn; fn="" }
			gsub(/^[ \t]+# ?/, "    ")
			print
			next
		}
		inCmd==1 { inCmd=0 }
	' "$1"
}

# Dispatch only when executed directly; stay silent when sourced.
if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
	set -euo pipefail
	"$@"
fi
