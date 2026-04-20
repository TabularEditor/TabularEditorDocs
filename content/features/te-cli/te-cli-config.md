---
uid: te-cli-config
title: Configuration
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
# Configuration

> [!IMPORTANT]
> The Tabular Editor CLI is in **Limited Public Preview**. It is offered for evaluation with a Tabular Editor account; no license is required during preview. Commands, flags, and outputs may change before general availability. **The preview build stops functioning after 2026-09-30.** We recommend against using the CLI in production CI/CD pipelines during preview.

The Tabular Editor CLI reads optional configuration from a JSON file. Configuration controls three things: where the CLI looks for Tabular Editor 3's shared data files (Preferences, macros, BPA rules), behavioral defaults (BPA gates, auto-format, validation), and the list of saved connection profiles.

Most users don't need to edit the file directly — `te config show`, `te config set <key> <value>`, and `te profile set` cover the common operations.

## Config file location

Resolution order:

1. `$TE_CONFIG` environment variable (if set and the file exists).
2. `~/.config/te/config.json` (on Windows, `%USERPROFILE%\.config\te\config.json`).
3. No config file — the CLI uses built-in defaults.

To create a default config:

```bash
te config init             # Create ~/.config/te/config.json with defaults
te config init --force     # Overwrite existing config
```

## Viewing configuration

```bash
te config show                         # Display all settings
te config show --output json           # Machine-readable
te config paths                        # Show resolved TE3 file paths
```

`te config paths` resolves where the CLI will actually look for TE3 data files — useful when debugging missing macros or BPA rules.

## Setting values

```bash
te config set autoFormat true
te config set bpaOnDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
```

Unknown keys fail with an error that lists the valid keys.

## Full schema

```json
{
  "te3DataDir": null,
  "preferences": null,
  "macros": null,
  "bpaRules": null,
  "bpaMachineRules": null,

  "autoFormat": false,
  "validateOnMutation": true,
  "bpaOnMutation": false,
  "bpaOnDeploy": true,
  "bpaOnSave": true,
  "vertipaqOnRefresh": false,

  "formatOptions": {
    "useSemicolons": false,
    "shortFormat": false,
    "skipSpaceAfterFunction": false
  },

  "hidePreviewNotice": false,
  "spinner": true,
  "debug": false,

  "profiles": {}
}
```

### Path overrides

| Key | Meaning |
| -- | -- |
| `te3DataDir` | Base directory used for TE3 file discovery when individual paths below are not set. Defaults to `%LOCALAPPDATA%\TabularEditor3` (Windows) or the equivalent auto-detected location on macOS/Linux. |
| `preferences` | Explicit path to `Preferences.json`. |
| `macros` | Explicit path to `MacroActions.json`. |
| `bpaRules` | Explicit path to user-level `BPARules.json`. |
| `bpaMachineRules` | Explicit path to machine-level `BPARules.json`. |

### Path resolution priority

For each TE3 file (Preferences, macros, BPA rules), the CLI resolves the path in this order:

1. **CLI config override** — the explicit entry above (`preferences`, `macros`, …).
2. **Environment variable** — e.g., `TE_MACROS_PATH`, `TE_BPA_RULES_PATH`.
3. **`te3DataDir`** — joined with the default filename.
4. **Auto-detect** — Windows `%LOCALAPPDATA%\TabularEditor3\...`, or the equivalent on macOS/Linux; on macOS we also probe a Parallels-style mapping if present.

Run `te config paths` to see which file the CLI actually resolved for each TE3 asset.

### Behavioral defaults

| Key | Default | Description |
| -- | -- | -- |
| `autoFormat` | `false` | Run DAX Formatter on modified expressions after `te add` / `te set` / `te mv` / `te macro run`. |
| `validateOnMutation` | `true` | Validate `Table[Column]` references after any mutating command. |
| `bpaOnMutation` | `false` | Run BPA after mutating commands. |
| `bpaOnDeploy` | `true` | Run BPA as a gate before `te deploy`. Bypass with `--skip-bpa`. |
| `bpaOnSave` | `true` | Run BPA as a gate before `te save`. Bypass with `--skip-bpa`. |
| `vertipaqOnRefresh` | `false` | Capture VertiPaq stats after a successful refresh. |

### Format options

Applied whenever the CLI invokes the DAX Formatter (for `te format` and, when enabled, `autoFormat` on mutations).

| Key | Default | Description |
| -- | -- | -- |
| `formatOptions.useSemicolons` | `false` | Use `;` as the list separator (European locale). |
| `formatOptions.shortFormat` | `false` | Use the compact layout variant. |
| `formatOptions.skipSpaceAfterFunction` | `false` | Omit the space between a function name and its opening parenthesis. |

### Display

| Key | Default | Description |
| -- | -- | -- |
| `hidePreviewNotice` | `false` | Suppress the yellow preview banner. **Ignored within 14 days of expiry.** |
| `spinner` | `true` | Show animated progress indicators in the terminal. Disable for CI. |
| `debug` | `false` | Always enable debug logging (same as passing `--debug`). |

### Profiles

Saved connection profiles live under the `profiles` key. Don't edit them by hand — use `te profile set / remove / list`. See @te-cli-auth for profile management.

Profiles can carry **overrides** that override the behavioral defaults above whenever the profile is active. This is how a dev profile can relax validation and BPA while a prod profile keeps them strict:

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

## BPA gate

The BPA gate is the safety net that prevents a model with rule violations from being saved or deployed. It runs automatically when:

- `te deploy` executes — unless `--skip-bpa` is passed or `bpaOnDeploy` is `false`.
- `te save` executes — unless `--skip-bpa` is passed or `bpaOnSave` is `false`.
- `te add` / `te set` / `te mv` / `te macro run` executes — only when `bpaOnMutation` is `true`.

When the gate fires and finds violations at severity ≥ `error`, the command fails with exit code `1` and a summary of the violations. Options to resolve:

- `--fix-bpa` — apply the rule's `fixExpression` in memory for the deploy/save artifact; source files are not modified.
- `--skip-bpa` — disable the gate for this one command.
- `.te-bpa.json` in the model directory — project-local BPA gate configuration (replacement for editing Preferences). <!-- TBD: confirm shape/scope of .te-bpa.json with Peer before publishing. -->

Run `te bpa run` independently to preview the gate's behavior without deploying:

```bash
te bpa run ./model --fail-on error
te bpa run ./model --fix --save     # Apply fixes to the source
```

## Post-mutation behavior

When you run a mutating command (`te add`, `te set`, `te mv`, `te replace --save`, `te macro run`), the CLI performs these checks automatically:

1. **TOM errors** are always surfaced — invalid DAX or M in measures, columns, partitions, calculation items. These always fail the command.
2. **Schema validation** (`validateOnMutation`, default `true`) — verifies that `Table[Column]` references in DAX still resolve. Cross-check of metadata consistency.
3. **DAX auto-format** (`autoFormat`, default `false`) — when enabled, formats any expressions touched by the mutation via the built-in DAX Formatter.
4. **BPA on mutation** (`bpaOnMutation`, default `false`) — when enabled, runs BPA after the mutation and warns/fails based on `--fail-on`.

Disable a check with `te config set <key> false`, or scope the relaxation to a specific environment via a profile.

## Environment variables

| Variable | Purpose |
| -- | -- |
| `TE_CONFIG` | Path to an alternative config file. Overrides `~/.config/te/config.json`. |
| `TE_DEBUG` | Set to `1` to enable debug logging globally (same as `--debug` or `debug: true` in config). |
| `TE_COMPAT` | Set to `te2` to force TE2-compatibility mode — see @te-cli-migrate. |
| `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID` | Service principal credentials, used by `--auth env`. |
| `TE_MACROS_PATH`, `TE_BPA_RULES_PATH`, ... | Per-file overrides for TE3 asset paths (second in resolution order — see above). |

## Related pages

- @te-cli-auth — profiles, authentication, and credential storage.
- @te-cli-commands — `te config` subcommands.
- @te-cli-cicd — configuring the BPA gate for pipelines.
