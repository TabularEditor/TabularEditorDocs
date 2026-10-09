---
uid: te-cli-config
title: Custom Configuration
author: Peer Grønnerup
updated: 2026-09-23
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

The Tabular Editor CLI reads optional configuration from a JSON file. The file sets the paths of the macros file, BPA rule files and query log, behavioral defaults such as BPA gates, auto-format and validation, and saved connection profiles.

The CLI doesn't read from or write to Tabular Editor 3 desktop install paths. Set the BPA rules and macros files in this config, or create them with `te bpa rules init` and `te macro init`.

`te config list`, `te config set <key> <value>` and `te profile set` cover the common operations without editing the file.

## Config file location

The CLI checks these locations in order:

1. `$TE_CONFIG` environment variable (if set and the file exists).
2. `~/.config/te/config.json` (on Windows, `%USERPROFILE%\.config\te\config.json`).
3. No config file - the CLI uses built-in defaults.

`te config list`, `te config set`, `te config init` and `te config paths` all read and write the file at the resolved path, including a path set by `TE_CONFIG`. Use `TE_CONFIG` for testing, scripted installs and per-environment configuration.

To create a default config:

```bash
te config init             # Create config at TE_CONFIG (or ~/.config/te/config.json)
te config init --force     # Overwrite existing config
```

## Viewing configuration

```bash
te config list                         # Display all settings
te config list --output-format json    # Machine-readable
te config paths                        # Show resolved macros and BPA rule paths
```

`te config paths` shows which files the CLI uses for macros and BPA rules. The output has two rows: `macros`, the resolved macros file path, and `bpa.rules`, the first existing BPA rules file. Either row shows `[not set]` if nothing resolves.

> [!NOTE]
> With `--output-format json`, `te config paths` writes unresolved paths as explicit `null` fields, for example `{"macros": null, "bpa": {"rules": null}}`. `te config list --output-format json` omits null fields by default, so parsers must handle missing keys.

## Setting values

```bash
te config set autoFormat true
te config set bpa.onDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
te config set -p spinner=false         # -p key=value works too
```

Keys can be passed positionally (`te config set <key> <value>`) or as `-p key=value`. Unknown keys fail with exit code `1` and an error that lists the valid keys.

If no config file exists, `te config set` auto-creates one at the resolved path (`$TE_CONFIG` if set, otherwise `~/.config/te/config.json`) before applying the change.

> [!NOTE]
> `te config set` sets every key in the schema except `formatVersion`, which the CLI manages. Use dotted paths for nested keys, such as `bpa.onDeploy` or `formatOptions.useSqlBiDaxFormatter`. To edit the JSON directly, run `te config paths` to find the file.

## Full schema

The complete config schema, with every key at its default value:

```json
{
  "formatVersion": 2,
  "macros": null,
  "autoFormat": false,
  "validateOnMutation": true,
  "vertipaqOnRefresh": false,
  "mutationOutput": "diff",

  "bpa": {
    "rules": null,
    "onDeploy": true,
    "onSave": true,
    "onMutation": false,
    "builtInRules": true,
    "disabledBuiltInRuleIds": null
  },

  "interactiveEditMode": "stage",
  "launchInteractiveMode": "auto",

  "formatOptions": {
    "shortFormat": false,
    "skipSpaceAfterFunction": false,
    "useSqlBiDaxFormatter": false
  },

  "hidePreviewNotice": false,
  "spinner": true,
  "debug": false,
  "disableTelemetry": false,

  "queryLog": null,

  "profiles": {}
}
```

### File paths

Paths set in the config apply to every command. Per-command flags and environment variables override them, as described in [Path resolution priority](#path-resolution-priority).

| Key | Meaning |
| -- | -- |
| `macros` | Explicit path to a macros JSON file (typically `MacroActions.json`). Resolved by every `te macro` command. To use the same macros on several machines or in both the CLI and Tabular Editor 3, point it at a shared file, such as a file on a network share, in the repository or the Tabular Editor 3 desktop file. |
| `bpa.rules` | Ordered list of paths or URLs to BPA rule files. `te bpa run` and the deploy/save gate load **every** existing entry; `te bpa rules list` and `te config paths` use the first existing entry. Comma-separated values on `te config set bpa.rules ...` are split into the array. |
| `queryLog` | Path to a log file where every `te query` invocation appends its query text and execution metadata. Supports `~` for the home directory, for example `~/.config/te/queries.log`. |

### Path resolution priority

For each user-provided file (macros, BPA rules), the CLI resolves the path in this order:

1. **Command-line flag** - `--macros <path>` for macro commands; `--bpa-rules <path>` for the deploy/save gate; `--rules-file <path>` for `te bpa rules` subcommands.
2. **Environment variable** - `TE_MACROS_PATH` for macros, `TE_BPA_RULES` for BPA rules.
3. **CLI config** - `macros` for macros, the first existing entry of `bpa.rules[]` for BPA rules.

The CLI doesn't detect Tabular Editor 3 install locations. To create a default file in the current directory, run `te macro init` (creates `./MacroActions.json`) or `te bpa rules init` (creates `./BPARules.json`).

Run `te config paths` to see which file the CLI actually resolved.

### Behavioral defaults

BPA settings are under the `bpa` object, and you address them with dotted keys in `te config set`.

| Key | Default | Description |
| -- | -- | -- |
| `autoFormat` | `false` | Automatically format the DAX expressions changed by a mutating command. Formatting is scoped to the objects the command touched but covers every DAX expression property they hold (expressions, format string expressions, detail rows, KPI target/status/trend, calculation group and table permission expressions, etc.). Power Query (M) and SQL partition queries are never reformatted. Always uses the built-in offline formatter in the comma dialect; the `formatOptions` layout keys apply. |
| `validateOnMutation` | `true` | After a mutating command (`add`, `set`, `mv`, `macro run`), check that every `Table[Column]` reference in the model still resolves. This catches references broken by renames or removals before deployment. |
| `mutationOutput` | `diff` | How mutating commands (`add`, `set`, `move`, `remove`, `script`, `bpa run --fix`) render the resulting change set in text output: `diff` (full before/after diff), `stat` (per-object change counts), `name-only` (changed object paths), or `none` (no change set; config only, with no `--none` flag). The `--diff`, `--stat` and `--name-only` flags override it for one invocation. JSON output always contains the full `changes` array. |
| `bpa.onMutation` | `false` | Run a scoped BPA analysis after each mutating command (`set`, `add`, `mv`, `rm`, `macro run`). Only the objects of the affected table are checked. |
| `bpa.onDeploy` | `true` | Run the BPA gate before `te deploy` executes. The deploy is aborted if any rule fires at severity >= error. Bypass per-invocation with `--skip-bpa`, or auto-fix with `--fix-bpa`. |
| `bpa.onSave` | `true` | Run the BPA gate before `te save-as` writes to disk. Bypass per-invocation with `--skip-bpa` or `--force`. |
| `bpa.builtInRules` | `true` | Include the curated built-in BPA rule set whenever the gate runs. If `false`, the gate runs only the rules in `bpa.rules` and rules embedded in the model. |
| `bpa.disabledBuiltInRuleIds` | `null` | IDs of individual built-in rules to exclude from the gate. Change it with `te bpa rules disable <id>` and `te bpa rules enable <id>`. |
| `vertipaqOnRefresh` | `false` | After a successful refresh (`full`, `dataonly`, `automatic`, or `add`), run VertiPaq analysis and show storage statistics for the refreshed tables. |
| `interactiveEditMode` | `stage` | Default behavior for in-memory mutations inside `te interactive`. `stage` keeps mutations in memory until you run `save`. `save` writes to the source after every mutating command; on a remote source, every `set` is an XMLA write. `revert` discards mutations after each command unless you pass `--save` or `--stage`. The per-command `--save`, `--revert` and `--stage` flags override the setting. |
| `launchInteractiveMode` | `auto` | Whether running `te` in a terminal with no arguments launches the interactive REPL. `auto` (default) launches the REPL only if stdin, stdout and stderr are all attached to a TTY, so scripts and CI pipelines get normal parsing. `always` launches the REPL even with redirection. `never` shows help instead. The global `--non-interactive` flag forces `never` for one invocation, and the `TE_INTERACTIVE` environment variable sets the mode for one invocation. |
| `disableTelemetry` | `false` | Opt out of anonymous usage telemetry. Telemetry contains the command name, exit code and duration. It doesn't contain model content, paths or query text. |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### Format options

The CLI's built-in DAX formatter works offline.

- The layout keys `shortFormat` and `skipSpaceAfterFunction` apply when `autoFormat` reformats mutated expressions and when `te query` renders query text.
- `te set <path> --format <Property>` and `te util format-dax` ignore the layout keys and take the flags `--long` and `--no-space-after-function`.
- Config-driven formatting always uses commas as list separators. For DAX written with semicolons, use the `--semicolons` flag of `te util format-dax`.
- `formatOptions.useSqlBiDaxFormatter` sends explicit formatting and `te query` rendering to the SQL BI [daxformatter.com](https://www.daxformatter.com) web service, which requires internet access. `autoFormat` always uses the built-in formatter.

| Key | Default | Description |
| -- | -- | -- |
| `formatOptions.shortFormat` | `false` | Use short, single-line formatting where possible. |
| `formatOptions.skipSpaceAfterFunction` | `false` | Omit the space between a function name and its opening parenthesis, for example `SUM(x)`. |
| `formatOptions.useSqlBiDaxFormatter` | `false` | Format DAX with the [SQL BI daxformatter.com](https://www.daxformatter.com) web service. Requires internet access. The built-in formatter matches the Tabular Editor 3 default. |

### Display

These settings control terminal output and diagnostic logging.

| Key | Default | Description |
| -- | -- | -- |
| `hidePreviewNotice` | `false` | Suppress the yellow preview banner. **Ignored within 14 days of expiry.** |
| `spinner` | `true` | Show animated progress indicators in the terminal. Disable for CI. |
| `debug` | `false` | Always enable debug logging (same as passing `--debug`). |

### Profiles

Saved connection profiles are stored under the `profiles` key. Manage them with `te profile set`, `te profile remove` and `te profile list`, not by editing the file. See @te-cli-auth.

A profile can override these behavioral defaults while it's active: `autoFormat`, `validateOnMutation`, `mutationOutput`, `bpa.onMutation`, `bpa.onDeploy`, `bpa.onSave`, `vertipaqOnRefresh`, `spinner` and `interactiveEditMode`. For example, a dev profile can turn off validation and the deploy gate while a prod profile formats DAX:

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

`te profile set` has flags for `--auto-format`, `--validate-on-mutation`, `--bpa-on-mutation`, `--bpa-on-deploy`, `--vertipaq-on-refresh` and `--spinner`. Each accepts `true`, `false` or `null`, which clears the override.

## BPA gate

The BPA gate stops a save or deployment if the model has rule violations at error severity. It runs on these commands:

- `te deploy` runs the gate unless `--skip-bpa` is passed or `bpa.onDeploy` is `false`.
- `te save-as` runs the gate unless `--skip-bpa` (or `--force`) is passed or `bpa.onSave` is `false`.
- `te add`, `te set`, `te move`, `te remove`, `te macro run` run the gate only when `bpa.onMutation` is `true`.

The gate loads BPA rules from `bpa.rules` and, by default, the built-in rule set (controlled by `bpa.builtInRules`). `te bpa rules disable <id>` excludes an individual built-in rule by adding it to `bpa.disabledBuiltInRuleIds`, and `te bpa rules enable <id>` removes it from the list.

If the gate finds violations at severity `error` or higher, the command fails with exit code `1` and a summary of the violations. To proceed, use one of these options:

- `--fix-bpa` - apply the rule's `fixExpression` in memory for the deploy/save artifact; source files are not modified.
- `--skip-bpa` - disable the gate for this one command.
- `--bpa-rules <path>` - repeatable; override `bpa.rules` for this single `te deploy` or `te save-as` invocation. Built-in rules still apply unless `bpa.builtInRules` is `false`.

To check the model against the rules without deploying, run `te bpa run`:

```bash
te bpa run --model ./model --fail-on error
te bpa run --model ./model --fix --save     # Apply fixes to the source
```

### Built-in BPA rules

The CLI includes a set of built-in BPA rules. Built-in rules are read-only: `te bpa rules set` and `te bpa rules remove` fail on built-in IDs and suggest `te bpa rules disable`. To change a built-in rule, copy it into your rules file with a new ID and disable the built-in rule.

`bpa.builtInRules` and `bpa.disabledBuiltInRuleIds` apply to the gate and to `te bpa run`, so a rule disabled with `te bpa rules disable` is excluded everywhere.

## Post-mutation behavior

After a mutating command (`te add`, `te set`, `te move` or `te macro run`), the CLI runs these checks:

1. TOM errors always appear. Invalid DAX or M in measures, columns, partitions or calculation items fails the command.
2. Schema validation (`validateOnMutation`, default `true`) verifies that `Table[Column]` references in DAX still resolve.
3. DAX auto-format (`autoFormat`, default `false`) formats the expressions touched by the mutation with the built-in formatter.
4. BPA on mutation (`bpa.onMutation`, default `false`) runs BPA after the mutation and warns or fails according to `--fail-on`.

`te config set <key> false` turns a check off. A profile can override the key for one environment.

## Administrator policies

On Windows, `te` honors the same administrator policies as Tabular Editor 3 and reads them from these registry keys:

- `Software\Policies\Tabular Editor ApS`, for values shared by the CLI and the desktop application
- its `TECLI` subkey, for values that apply to the CLI only
- its `TE3` subkey, for values that apply to the desktop application only
- the earlier `Software\Policies\Kapacity\Tabular Editor` key, which is still honored

A machine-wide value (`HKEY_LOCAL_MACHINE`) takes precedence over a per-user one (`HKEY_CURRENT_USER`). Within a hive, a product-specific value takes precedence over a shared one. When a policy turns a feature off, the command names the policy, does nothing and exits with a failure, which fails any pipeline step that depends on the feature.

| Policy | Effect on the CLI |
| -- | -- |
| `DisableCSharpScripts` | Blocks `te script` and the automatic fixes of `te bpa run --fix`. |
| `DisableMacros` | Blocks every `te macro` command. |
| `DisableBpaDownload` | Blocks Best Practice Analyzer rules given as a URL. Rule files on disk and the built-in rules are unaffected. |
| `DisableTelemetry` | Turns anonymous usage statistics off, whatever `disableTelemetry` in config says. |
| `BlockUnsafeScripts` | Blocks `te script`, `te macro run` and `te bpa run --fix` when the code accesses files, the network, processes or external assemblies. See [What BlockUnsafeScripts blocks](xref:csharp-scripts#what-blockunsafescripts-blocks) for the blocked APIs. JSON output reports `blockedByPolicy`. |

Policies for update checks, error reports, DAX Optimizer, the DAX Package Manager, the AI Assistant and the MCP server don't affect the CLI. See @policies for the full list of policies and how to deploy them.

In the desktop application, `BlockUnsafeScripts` requires Tabular Editor 3 Enterprise Edition. The CLI has no editions and applies the policy wherever it's set.

## Environment variables

The CLI reads these environment variables for paths, behavior and diagnostics. For Azure authentication variables (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_CERTIFICATE_PATH`, etc.), see @te-cli-auth.

| Variable | Purpose |
| -- | -- |
| `TE_CONFIG` | Path to an alternative config file. Used by `te config list`, `set`, `init` and `paths`. |
| `TE_MACROS_PATH` | Override the macros file path, second in the [resolution order](#path-resolution-priority). Read by `te macro` commands. |
| `TE_BPA_RULES` | Override the BPA rules file/URL list used by `te bpa run` and `te bpa rules` subcommands. |
| `TE_BPA_CONFIG` | Override the path to the BPA gate config (`.te-bpa.json`) the deploy/save gate reads. |
| `TE_DEBUG` | Set to `1` to enable debug logging globally (same as `--debug` or `debug: true` in config). |
| `NO_SPINNER` | Set to `1` or `true` to disable animated progress indicators (alternative to `spinner: false` in config). |
| `CI` | Auto-detected. When `1` or `true`, the CLI disables the spinner and switches to plain output. Most CI runners set it. |
| `TE_SESSION` | Override the per-terminal session ID used for active-connection state. Set it to run isolated CLI sessions in the same shell, for example in parallel CI matrix jobs. Inspect and manage sessions with [`te session`](xref:te-cli-commands#session). |
| `TE_INTERACTIVE` | Override `launchInteractiveMode` for a single invocation. Accepts `auto`, `always` or `never`. `TE_INTERACTIVE=always` launches the REPL, and `TE_INTERACTIVE=never` shows help. |
| `TE_COMPAT` | Set to `te2` to force TE2-compatibility mode - see @te-cli-migrate. |

## Next steps

- @te-cli-auth - profiles, authentication, and credential storage.
- @te-cli-commands - `te config` subcommands.
- @te-cli-cicd - configuring the BPA gate for pipelines.
