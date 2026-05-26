---
uid: te-cli-config
title: Custom Configuration
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
# Custom Configuration

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

The Tabular Editor CLI reads optional configuration from a JSON file. Configuration controls three things: where the CLI looks for its own data files (macros, BPA rules), behavioral defaults (BPA gates, auto-format, validation), and the list of saved connection profiles.

The CLI is self-contained - it does not read from or write to any Tabular Editor 3 desktop install path. BPA rules and macros files must be set explicitly via this config (or initialized on demand with `te bpa rules init` / `te macro init`); there is no auto-detection of `%LocalAppData%\TabularEditor3\` or `%ProgramData%\TabularEditor3\`.

Most users don't need to edit the file directly - `te config show`, `te config set <key> <value>`, and `te profile set` cover the common operations.

## Config file location

Resolution order:

1. `$TE_CONFIG` environment variable (if set and the file exists).
2. `~/.config/te/config.json` (on Windows, `%USERPROFILE%\.config\te\config.json`).
3. No config file - the CLI uses built-in defaults.

`TE_CONFIG` is honored consistently by every config-file operation - `te config show`, `te config set`, `te config init`, and `te config paths` all read and write at the resolved path. This is primarily intended for testing, scripted installs, and per-environment configuration.

To create a default config:

```bash
te config init             # Create config at TE_CONFIG (or ~/.config/te/config.json)
te config init --force     # Overwrite existing config
```

## Viewing configuration

```bash
te config show                         # Display all settings
te config show --output-format json           # Machine-readable
te config paths                        # Show resolved macros and BPA rule paths
```

`te config paths` resolves the files the CLI will actually use for macros and BPA rules - useful when debugging missing data files. The output shows two rows: `macros` (the resolved macros file path or `[not set]`) and `bpa.rules` (the first existing BPA rules file resolved by the path resolver, or `[not set]`).

> [!NOTE]
> `te config paths` emits `null` fields explicitly in `--output-format json` mode (e.g., `{"macros": null, "bpa": {"rules": null}}`). Reporting resolution outcomes is the command's whole purpose, so `null` is a meaningful "tried but resolved to nothing" answer. `te config show --output-format json` strips null fields by default, so consumers should parse it tolerantly.

## Setting values

```bash
te config set autoFormat true
te config set bpa.onDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
```

Unknown keys fail with exit code `1` and an error that lists the valid keys.

If no config file exists, `te config set` auto-creates one at the resolved path (`$TE_CONFIG` if set, otherwise `~/.config/te/config.json`) before applying the change.

## Full schema

```json
{
  "formatVersion": 1,
  "macros": null,
  "autoFormat": false,
  "validateOnMutation": true,
  "vertipaqOnRefresh": false,

  "bpa": {
    "rules": null,
    "onDeploy": true,
    "onSave": true,
    "onMutation": false,
    "builtInRules": true,
    "disabledBuiltInRuleIds": null
  },

  "interactiveEditMode": "stage",

  "formatOptions": {
    "useSemicolons": false,
    "shortFormat": false,
    "skipSpaceAfterFunction": false
  },

  "hidePreviewNotice": false,
  "spinner": true,
  "debug": false,

  "queryLog": null,
  "te3ExePath": null,

  "profiles": {}
}
```

### Path overrides

| Key | Meaning |
| -- | -- |
| `macros` | Explicit path to a macros JSON file (typically `MacroActions.json`). Resolved by `te macro` commands. |
| `bpa.rules` | Ordered list of BPA rule files / URLs the gate loads. The gate uses every existing entry. Comma-separated values on `te config set bpa.rules ...` are split into the array. |
| `te3ExePath` | Explicit path to the TE3 desktop executable (`TabularEditor.exe`). Used **only** by `te open`; safe to leave unset on Linux/macOS or when you don't use `te open`. |

### Path resolution priority

For each user-provided file (macros, BPA rules), the CLI resolves the path in this order:

1. **Command-line flag** - `--macros <path>` for macro commands; `--bpa-rules <path>` for the deploy/save gate; `--rules-file <path>` for `te bpa rules` subcommands.
2. **Environment variable** - `TE_MACROS_PATH` for macros, `TE_BPA_PATH` for BPA rules.
3. **CLI config** - `macros` for macros, the first existing entry of `bpa.rules[]` for BPA rules.
4. **Working-directory fallback** - `./MacroActions.json` for `te macro init`, `./BPARules.json` for `te bpa rules init`.

The CLI does not auto-detect any TE3 install location - configure these explicitly or use the `init` commands.

Run `te config paths` to see which file the CLI actually resolved.

### Behavioral defaults

All BPA-related settings live under the `bpa` object and are addressed via dotted keys on `te config set`.

| Key | Default | Description |
| -- | -- | -- |
| `autoFormat` | `false` | Run DAX Formatter on modified expressions after `te add` / `te set` / `te mv` / `te macro run`. |
| `validateOnMutation` | `true` | Validate `Table[Column]` references after any mutating command. |
| `bpa.onMutation` | `false` | Run BPA after mutating commands (`set`, `add`, `mv`, `rm`, `macro run`). |
| `bpa.onDeploy` | `true` | Run BPA as a gate before `te deploy`. Bypass with `--skip-bpa`. |
| `bpa.onSave` | `true` | Run BPA as a gate before `te save`. Bypass with `--skip-bpa` or `--force`. |
| `bpa.builtInRules` | `true` | Include the built-in BPA rule set whenever the gate runs. |
| `bpa.disabledBuiltInRuleIds` | `null` | IDs of individual built-in rules to exclude from the gate. Mutated by `te bpa rules disable` / `te bpa rules enable`. |
| `vertipaqOnRefresh` | `false` | Capture VertiPaq stats after a successful refresh. |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### Other schema keys

`formatVersion` is set by the CLI when writing the file and is **not** user-settable via `te config set`. The CLI refuses to load a file whose `formatVersion` is higher than the build understands, so an older CLI cannot silently clobber a newer config.

`interactiveEditMode` comes from the interactive-staging feature (`stage` / `save` / `revert`); it can be set via `te config set interactiveEditMode <mode>` and is documented in that feature's release notes.

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

Saved connection profiles live under the `profiles` key. Don't edit them by hand - use `te profile set / remove / list`. See @te-cli-auth for profile management.

Profiles can carry **overrides** that override the behavioral defaults above whenever the profile is active. This is how a dev profile can relax validation and BPA while a prod profile keeps them strict:

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

## BPA gate

The BPA gate is the safety net that prevents a model with rule violations from being saved or deployed. It runs automatically when:

- `te deploy` executes - unless `--skip-bpa` is passed or `bpa.onDeploy` is `false`.
- `te save` executes - unless `--skip-bpa` (or `--force`) is passed or `bpa.onSave` is `false`.
- `te add` / `te set` / `te mv` / `te macro run` executes - only when `bpa.onMutation` is `true`.

The gate loads BPA rules from `bpa.rules` plus, by default, the built-in rule set (controlled by `bpa.builtInRules`). Built-in rules can be individually excluded via `bpa.disabledBuiltInRuleIds` - managed with `te bpa rules disable <id>` / `te bpa rules enable <id>`.

When the gate fires and finds violations at severity ≥ `error`, the command fails with exit code `1` and a summary of the violations. Options to resolve:

- `--fix-bpa` - apply the rule's `fixExpression` in memory for the deploy/save artifact; source files are not modified.
- `--skip-bpa` - disable the gate for this one command.
- `--bpa-rules <path>` - repeatable; override `bpa.rules` for this single `te deploy` or `te save` invocation. Built-in rules still apply unless `bpa.builtInRules` is `false`.

Run `te bpa run` independently to preview the gate's behavior without deploying:

```bash
te bpa run ./model --fail-on error
te bpa run ./model --fix --save     # Apply fixes to the source
```

### Built-in BPA rules

The CLI ships a single canonical set of built-in BPA rules embedded as a JSON resource. Built-in rules are read-only - `te bpa rules set` and `te bpa rules rm` refuse to mutate built-in IDs and point users at `te bpa rules disable` instead. To customize a built-in rule's behavior, copy it into your local rules file as a new rule with a different ID and disable the built-in.

Both `bpa.builtInRules` and `bpa.disabledBuiltInRuleIds` apply consistently to the deploy/save/mutation gate **and** the manual `te bpa run` command - disabling a rule once via `te bpa rules disable` excludes it everywhere.

## Post-mutation behavior

When you run a mutating command (`te add`, `te set`, `te mv`, `te replace --save`, `te macro run`), the CLI performs these checks automatically:

1. **TOM errors** are always surfaced - invalid DAX or M in measures, columns, partitions, calculation items. These always fail the command.
2. **Schema validation** (`validateOnMutation`, default `true`) - verifies that `Table[Column]` references in DAX still resolve. Cross-check of metadata consistency.
3. **DAX auto-format** (`autoFormat`, default `false`) - when enabled, formats any expressions touched by the mutation via the built-in DAX Formatter.
4. **BPA on mutation** (`bpa.onMutation`, default `false`) - when enabled, runs BPA after the mutation and warns/fails based on `--fail-on`.

Disable a check with `te config set <key> false`, or scope the relaxation to a specific environment via a profile.

## Environment variables

| Variable | Purpose |
| -- | -- |
| `TE_CONFIG` | Path to an alternative config file. Honored by every `te config` operation (`show`, `set`, `init`, `paths`). |
| `TE_DEBUG` | Set to `1` to enable debug logging globally (same as `--debug` or `debug: true` in config). |
| `TE_COMPAT` | Set to `te2` to force TE2-compatibility mode - see @te-cli-migrate. |
| `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID` | Service principal credentials, used by `--auth env`. |
| `TE_MACROS_PATH` | Per-invocation override for the macros file path (second in resolution order - see above). |
| `TE_BPA_PATH` | Per-invocation override for the BPA rules file path used by `te bpa rules` subcommands. |

## Related pages

- @te-cli-auth - profiles, authentication, and credential storage.
- @te-cli-commands - `te config` subcommands.
- @te-cli-cicd - configuring the BPA gate for pipelines.
