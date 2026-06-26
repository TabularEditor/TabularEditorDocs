---
uid: te-cli-config
title: Custom Configuration
author: Peer Grønnerup
updated: 2026-06-11
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

The Tabular Editor CLI reads optional configuration from a JSON file. Configuration controls three things:
 
- **File paths** - where the CLI reads macros, BPA rules, and (optionally) the TE3 Desktop executable, and where to write the query log.
- **Behavioral defaults** - BPA gates, auto-format, validation.
- **Saved connection profiles** - the list of named profiles you can switch between.

The CLI is self-contained - it does not read from or write to any Tabular Editor 3 desktop install path. BPA rules and macros files must be set explicitly via this config (or initialized on demand with `te bpa rules init` / `te macro init`).

Most users don't need to edit the config file directly - `te config show`, `te config set <key> <value>`, and `te profile set` cover the common operations.

## Config file location

The following locations are checked in this order:

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
te config show --output-format json    # Machine-readable
te config paths                        # Show resolved macros and BPA rule paths
```

Use `te config paths` to see which files the CLI will actually use for macros and BPA rules. It's handy when debugging missing data files. The output shows two rows: `macros` (the resolved macros file path or `[not set]`) and `bpa.rules` (the first existing BPA rules file resolved by the path resolver, or `[not set]`).

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

> [!NOTE]
> Every key in the schema is settable via `te config set`, including nested keys via dotted paths (`bpa.onDeploy`, `formatOptions.useSqlBiDaxFormatter`, etc.). The only exception is `formatVersion`, which the CLI manages automatically. Run `te config paths` to find the config file if you'd rather edit the JSON directly.

## Full schema

The complete JSON config schema with all keys at their default values. Use this as a reference when editing the config file directly, or when looking up the dotted path for a `te config set` call.

```json
{
  "formatVersion": 2,
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
    "skipSpaceAfterFunction": false,
    "useSqlBiDaxFormatter": false
  },

  "hidePreviewNotice": false,
  "spinner": true,
  "debug": false,
  "disableTelemetry": false,

  "queryLog": null,
  "te3ExePath": null,

  "profiles": {}
}
```

### File paths

Set these in your config to avoid passing the same paths on every command. Per-command flags and environment variables override config values; see [Path resolution priority](#path-resolution-priority) below.

| Key | Meaning |
| -- | -- |
| `macros` | Explicit path to a macros JSON file (typically `MacroActions.json`). Resolved by every `te macro` command. Point at a shared file (network share, repo-local, or even the TE3 desktop file) to reuse the same set of macros across machines and between the CLI and TE3 Desktop. |
| `bpa.rules` | Ordered list of paths or URLs to BPA rule files. `te bpa run` and the deploy/save gate load **every** existing entry; `te bpa rules list` and `te config paths` use the first existing entry. Comma-separated values on `te config set bpa.rules ...` are split into the array. |
| `te3ExePath` | Explicit path to the Tabular Editor 3 Desktop executable (`TabularEditor.exe`). Used **only** by `te open` to launch the desktop app; safe to leave unset on Linux/macOS or when you don't use `te open`. If unset, `te open` falls back to a `PATH` lookup. |
| `queryLog` | Path to a log file where every `te query` invocation appends its query text and execution metadata. Useful for audit trails or analyzing query patterns over time. Supports `~` for the home directory (e.g., `~/.config/te/queries.log`). |

### Path resolution priority

For each user-provided file (macros, BPA rules), the CLI resolves the path in this order:

1. **Command-line flag** - `--macros <path>` for macro commands; `--bpa-rules <path>` for the deploy/save gate; `--rules-file <path>` for `te bpa rules` subcommands.
2. **Environment variable** - `TE_MACROS_PATH` for macros, `TE_BPA_RULES` for BPA rules.
3. **CLI config** - `macros` for macros, the first existing entry of `bpa.rules[]` for BPA rules.

The CLI does not auto-detect any TE3 install location - configure these explicitly. To start from a default file in the current working directory, run `te macro init` (creates `./MacroActions.json`) or `te bpa rules init` (creates `./BPARules.json`).

Run `te config paths` to see which file the CLI actually resolved.

### Behavioral defaults

All BPA-related settings live under the `bpa` object and are addressed via dotted keys on `te config set`.

| Key | Default | Description |
| -- | -- | -- |
| `autoFormat` | `false` | Run the DAX Formatter on modified expressions after `te add` / `te set` / `te mv` / `te macro run`. Uses the in-house formatter by default; opt into the SQL BI web service via `formatOptions.useSqlBiDaxFormatter`. |
| `validateOnMutation` | `true` | After a mutating command (`add`, `set`, `mv`, `replace --save`, `macro run`), check that every `Table[Column]` reference in the model still resolves. Catches dangling references introduced by renames or removals before they reach deploy. |
| `bpa.onMutation` | `false` | Run a scoped BPA analysis after each mutating command (`set`, `add`, `mv`, `rm`, `macro run`). Only the affected table's objects are checked, not the whole model - useful for fast feedback during iterative edits. |
| `bpa.onDeploy` | `true` | Run the BPA gate before `te deploy` executes. The deploy is aborted if any rule fires at severity >= error. Bypass per-invocation with `--skip-bpa`, or auto-fix with `--fix-bpa`. |
| `bpa.onSave` | `true` | Run the BPA gate before `te save -o` writes to disk. Bypass per-invocation with `--skip-bpa` or `--force`. |
| `bpa.builtInRules` | `true` | Include the curated built-in BPA rule set whenever the gate runs. Set to `false` to ignore built-ins entirely; the gate then runs only the rules configured via `bpa.rules` and any model-embedded rules. |
| `bpa.disabledBuiltInRuleIds` | `null` | IDs of individual built-in rules to exclude from the gate. Mutated by `te bpa rules disable <id>` / `te bpa rules enable <id>` - prefer those over editing the array directly. |
| `vertipaqOnRefresh` | `false` | After a successful refresh (`full`, `dataonly`, `automatic`, or `add`), automatically run VertiPaq analysis to show storage stats for the refreshed tables. Useful for catching unexpected cardinality or memory regressions immediately. |
| `interactiveEditMode` | `stage` | Default behavior for in-memory mutations inside `te interactive`. `stage` keeps mutations in memory until `save` is invoked (safest); `save` writes to source after every mutating command (use with care on remote sources - every `set` triggers an XMLA write); `revert` discards mutations after each command unless `--save` or `--stage` was passed. Per-command `--save` / `--revert` / `--stage` flags always override. |
| `disableTelemetry` | `false` | Opt out of anonymous usage telemetry. The CLI collects coarse-grained command usage data (command name, exit code, duration) to inform feature priority. The CLI never collects model content, paths, or query text. |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### Format options

Applied whenever the CLI invokes a DAX formatter (for `te format` and, when enabled, `autoFormat` on mutations). The CLI ships with an in-house formatter that works fully offline; opt into the SQL BI [daxformatter.com](https://www.daxformatter.com) web service via `formatOptions.useSqlBiDaxFormatter` if you need that style or want to match the behavior of TE2 or TE3 with "Use daxformatter.com..." enabled.

| Key | Default | Description |
| -- | -- | -- |
| `formatOptions.useSemicolons` | `false` | Use `;` as the list separator (European/EU locale convention). The default `,` matches the en-US locale. |
| `formatOptions.shortFormat` | `false` | Prefer short, single-line formatting where possible instead of the default multi-line layout. |
| `formatOptions.skipSpaceAfterFunction` | `false` | Omit the space between a function name and its opening parenthesis (e.g. `SUM(x)` instead of `SUM (x)`). |
| `formatOptions.useSqlBiDaxFormatter` | `false` | Format DAX via the [SQL BI daxformatter.com](https://www.daxformatter.com) web service instead of the in-house formatter. Requires internet access. The in-house formatter (default) works offline and matches the Tabular Editor 3 Desktop default. |

### Display

Settings that control the CLI's terminal output and diagnostic verbosity.

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

The BPA gate is the safety net that prevents a model with rule violations from being saved or deployed. It runs automatically when the following commands are executed:

- `te deploy` runs the gate unless `--skip-bpa` is passed or `bpa.onDeploy` is `false`.
- `te save` runs the gate unless `--skip-bpa` (or `--force`) is passed or `bpa.onSave` is `false`.
- `te add`, `te set`, `te mv`, `te macro run` run the gate only when `bpa.onMutation` is `true`.

The gate loads BPA rules from `bpa.rules` and, by default, the built-in rule set (controlled by `bpa.builtInRules`). Built-in rules can be individually excluded via `bpa.disabledBuiltInRuleIds` - managed with `te bpa rules disable <id>` / `te bpa rules enable <id>`.

When the gate fires and finds violations at severity >= `error`, the command fails with exit code `1` and a summary of the violations. Options to resolve:

- `--fix-bpa` - apply the rule's `fixExpression` in memory for the deploy/save artifact; source files are not modified.
- `--skip-bpa` - disable the gate for this one command.
- `--bpa-rules <path>` - repeatable; override `bpa.rules` for this single `te deploy` or `te save` invocation. Built-in rules still apply unless `bpa.builtInRules` is `false`.

Run `te bpa run` independently to preview the gate's behavior without deploying:

```bash
te bpa run ./model --fail-on error
te bpa run ./model --fix --save     # Apply fixes to the source
```

### Built-in BPA rules

The CLI ships a single canonical set of built-in BPA rules embedded as a JSON resource. Built-in rules are read-only - `te bpa rules set` and `te bpa rules remove` refuse to mutate built-in IDs and point users at `te bpa rules disable` instead. To customize a built-in rule's behavior, copy it into your local rules file as a new rule with a different ID and disable the built-in.

Both `bpa.builtInRules` and `bpa.disabledBuiltInRuleIds` apply consistently to the deploy/save/mutation gate **and** the manual `te bpa run` command - disabling a rule once via `te bpa rules disable` excludes it everywhere.

## Post-mutation behavior

When you run a mutating command (`te add`, `te set`, `te mv`, `te replace --save`, `te macro run`), the CLI performs these checks automatically:

1. **TOM errors** are always surfaced. Invalid DAX or M in measures, columns, partitions, or calculation items always fails the command.
2. **Schema validation** (`validateOnMutation`, default `true`) verifies that `Table[Column]` references in DAX still resolve, cross-checking metadata consistency.
3. **DAX auto-format** (`autoFormat`, default `false`) formats any expressions touched by the mutation via the built-in DAX Formatter when enabled.
4. **BPA on mutation** (`bpa.onMutation`, default `false`) runs BPA after the mutation when enabled, warning or failing based on `--fail-on`.

Disable a check with `te config set <key> false`, or scope the relaxation to a specific environment via a profile.

## Environment variables

Use the following CLI-specific environment variables for paths, behavior, and diagnostics. For Azure authentication variables (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_CERTIFICATE_PATH`, etc.), see @te-cli-auth.

| Variable | Purpose |
| -- | -- |
| `TE_CONFIG` | Path to an alternative config file. Honored by every `te config` operation (`show`, `set`, `init`, `paths`). |
| `TE_MACROS_PATH` | Override the macros file path (second in resolution order - see above). Read by `te macro` commands. |
| `TE_BPA_RULES` | Override the BPA rules file/URL list used by `te bpa run` and `te bpa rules` subcommands. |
| `TE_BPA_CONFIG` | Override the path to the BPA gate config (`.te-bpa.json`) the deploy/save gate reads. |
| `TE3_EXE_PATH` | Path to the Tabular Editor 3 desktop binary. Used **only** by `te open`; safe to leave unset on Linux/macOS or when you don't use `te open`. Falls back to `PATH` lookup. |
| `TE_DEBUG` | Set to `1` to enable debug logging globally (same as `--debug` or `debug: true` in config). |
| `NO_SPINNER` | Set to `1` or `true` to disable animated progress indicators (alternative to `spinner: false` in config). |
| `CI` | Auto-detected. When `1` or `true`, the CLI disables the spinner and switches to plain output. Most CI runners set this automatically. |
| `TE_SESSION` | Override the per-terminal session ID used for active-connection state. Useful for running multiple isolated CLI sessions inside the same shell, e.g. in parallel CI matrix jobs. Inspect and manage sessions with [`te session`](xref:te-cli-commands#session). |
| `TE_COMPAT` | Set to `te2` to force TE2-compatibility mode - see @te-cli-migrate. |

## Related pages

- @te-cli-auth - profiles, authentication, and credential storage.
- @te-cli-commands - `te config` subcommands.
- @te-cli-cicd - configuring the BPA gate for pipelines.
