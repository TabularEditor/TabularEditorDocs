---
uid: te-cli-migrate
title: Migrating from the TE2 Command Line
author: Peer Grønnerup
updated: 2026-04-20
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---
# Migrating from the TE2 Command Line

> [!IMPORTANT]
> The Tabular Editor CLI is in **Limited Public Preview**. It is offered for evaluation with a Tabular Editor account; no license is required during preview. Commands, flags, and outputs may change before general availability. **The preview build stops functioning after 2026-09-30.** We recommend against using the CLI in production CI/CD pipelines during preview.

Teams with existing build pipelines that invoke `TabularEditor.exe` with TE2-style flags (`-S`, `-A`, `-D`, `-O`, `-C`, etc.) can adopt the new CLI incrementally. The Tabular Editor CLI accepts both command shapes: the new subcommand-based form (`te deploy`, `te bpa run`, …) and the legacy TE2 flag syntax, via a built-in compatibility layer.

For the legacy TE2 Windows command-line reference, see @command-line-options.

## How TE2 compatibility works

TE2 compatibility mode is activated in any of three ways:

1. **Binary name.** Rename `te` to `te2` (or symlink it) and the CLI runs in TE2-exact mode. This is the drop-in replacement path: swap `TabularEditor.exe` for `te2` in your existing pipeline and the same arguments work.
2. **Environment variable.** Set `TE_COMPAT=te2` before invoking `te` to force TE2 mode.
3. **Auto-detection.** If the first argument isn't a `te` subcommand (`load`, `deploy`, …) and at least one recognized TE2 flag appears somewhere in the argument list, the CLI auto-routes to TE2 mode. This means most existing TE2 invocations work without any changes.

```bash
# All three are equivalent — each runs in TE2 mode
./te2 Model.bim -S fix.csx -D localhost\tabular MyDB -O
TE_COMPAT=te2 te Model.bim -S fix.csx -D localhost\tabular MyDB -O
te Model.bim -S fix.csx -D localhost\tabular MyDB -O
```

> [!NOTE]
> TE2 mode runs the same `Load → Scripts → Schema Check → Save → BPA → Deploy → TRX` pipeline as `TabularEditor.exe`, including context-sensitive flag behavior (e.g., `-S` after `-D` means `-SHARED`, not `-SCRIPT`).

## The migrate command

Use `te migrate` as a live reference for how TE2 flags map to the new CLI. It prints a colorized table of every known TE2 flag, its status (supported, renamed, planned), and the equivalent `te` command.

```bash
te migrate                   # Full flag mapping table
te migrate -A                # Look up a single flag
te migrate --output json     # Machine-readable mapping
```

Prefer `te migrate` over this page when you need the current mapping — it reflects the CLI version you have installed.

## Flag mapping (curated subset)

A non-exhaustive summary of the most commonly used flags. Run `te migrate` for the full list.

| TE2 flag | New CLI equivalent | Notes |
| -- | -- | -- |
| `file` (positional) | `te <command> <path>` or global `--model` | First positional arg on most commands. |
| `server`, `database` | `te connect <server>` or `te deploy <server> <database>` | Server is no longer a global positional. |
| `-L` / `-LOCAL` | `te connect --local` | Windows only. |
| `-S` / `-SCRIPT` | `te script -s <file.csx>` or `-e "code"` | Supports multiple scripts, inline code, and stdin. |
| `-A` / `-ANALYZE` | `te bpa run --rules <file-or-url>` | Supports `--fail-on`, `--fix`, multiple rule files. |
| `-AX` / `-ANALYZEX` | `te bpa run --rules <file>` (without `--model-rules`) | Excluding model-embedded rules is the new default. |
| `-B` / `-BIM` | `te save <model> -o <file.bim> --format bim` | |
| `-F` / `-FOLDER` | `te save <model> -o <dir> --format te-folder` | After `-D`, TE2's `-F` means `-FULL` — see `--deploy-full`. |
| `-TMDL` | `te save <model> -o <dir> --format tmdl` | TMDL is the default save format. |
| `-D` / `-DEPLOY` | `te deploy <server> <database> <model>` | Separate command with named options. |
| `-O` / `-OVERWRITE` | (default) or `--create-only` to opt out | Overwrite is the default in the new CLI. |
| `-C` / `-CONNECTIONS` | `te deploy --deploy-connections` | |
| `-P` / `-PARTITIONS` | `te deploy --deploy-partitions` | |
| `-Y` / `-SKIPPOLICY` | `te deploy --deploy-partitions --skip-refresh-policy` | Requires `--deploy-partitions`. |
| `-SHARED` | `te deploy --deploy-shared-expressions` | After `-D`, TE2's `-S` means `-SHARED`. |
| `-R` / `-ROLES` | `te deploy --deploy-roles` | |
| `-M` / `-MEMBERS` | `te deploy --deploy-role-members` | |
| `-FULL` (after `-D`) | `te deploy --deploy-full` | Equivalent to overwrite + connections + partitions + shared + roles + role-members. |
| `-X` / `-XMLA <file>` | `te deploy ... --xmla <file>` | Use `-` for stdout. |
| `-V` / `-VSTS` | `--ci vsts` on `validate`, `bpa run`, `deploy` | Emits `##vso[...]` annotations to stderr. |
| `-G` / `-GITHUB` | `--ci github` | Emits `::error::` / `::warning::` annotations. |
| `-T` / `-TRX <file>` | `--trx <file>` on `validate`, `bpa run`, `test run` | VSTEST `.trx` file for Azure DevOps test publishing. |
| `-W` / `-WARN` | (default) | Warnings always reported in deploy results. |
| `-E` / `-ERR` | (default) | Deploy returns non-zero exit on DAX errors. |
| `-SC` / `-SCHEMACHECK` | *Not yet implemented.* | TE2 schema check connects to actual data sources. Different from `te validate` (DAX semantic validation, no data source connection). |
| `-L` / `-LOGIN <user> <pass>` (after `-D`) | *Not yet implemented.* | Use `te auth login` with service principal or env-based credentials instead — see @te-cli-auth. |

## Migration playbook

The recommended path from a TE2-based pipeline to the new CLI:

1. **Drop-in replacement.** Replace `TabularEditor.exe` with `te` (or `te2`) in your existing pipeline. Verify the pipeline still runs — TE2 compatibility handles most invocations unchanged.
2. **Replace flags incrementally.** Convert one flag group at a time:
   - Start with `-A` / `-AX` → `te bpa run` to pick up richer BPA output (`--fail-on`, `--fix`, `--trx`).
   - Then `-D` → `te deploy` for fine-grained deploy control.
   - Finally `-V` / `-G` → `--ci vsts` / `--ci github`.
3. **Switch to non-interactive CI flags.** Add `--non-interactive --ci <vsts|github>` to every `te` command and remove any `start /wait` wrappers — the new CLI is a regular console binary and doesn't need them.
4. **Adopt service principal auth.** Replace `-D -L <user> <pass>` with `te auth login -u ... -p ... -t ...` or an environment-credential pipeline step. See @te-cli-auth.

## Differences worth knowing

- **BPA gate on deploy.** `te deploy` now runs BPA as a pre-flight gate by default. Use `--skip-bpa` to preserve the old behavior, or `--fix-bpa` to auto-fix violations before deploy. See @te-cli-config.
- **Interactive confirmation on deploy.** `te deploy` prompts for confirmation by default (with `n` as the safe default answer). CI pipelines must pass `--force`.
- **Structured output.** Every command supports `--output json` for machine-readable output — see @te-cli-automation.
- **No `start /wait` needed.** The new CLI is a regular console binary; invoke it directly in shell scripts, PowerShell, and CI tasks.
- **Cross-platform.** The CLI runs on Windows, macOS, and Linux. Local SSAS and Power BI Desktop connections remain Windows-only.

## Related pages

- @command-line-options — the legacy TE2 command-line reference.
- @te-cli-commands — the new CLI's full command reference.
- @te-cli-cicd — pipeline examples for GitHub Actions and Azure DevOps.
