---
uid: te-cli-config
title: 自定义配置
author: Peer Grønnerup
updated: 2026-09-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# 自定义配置

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI 可从 JSON 文件读取可选配置。 Configuration controls three things:

- **File paths** - where the CLI reads macros and BPA rules, and where to write the query log.
- **Behavioral defaults** - BPA gates, auto-format, validation.
- **Saved connection profiles** - the list of named profiles you can switch between.

CLI 是自包含的 - 它不会从任何 Tabular Editor 3 桌面版安装路径读取或写入任何内容。 BPA rules and macros files must be set explicitly via this config (or initialized on demand with `te bpa rules init` / `te macro init`).

Most users don't need to edit the config file directly - `te config list`, `te config set <key> <value>`, and `te profile set` cover the common operations.

## 配置文件位置

将按以下顺序检查这些位置：

1. `$TE_CONFIG` 环境变量（如果已设置且文件存在）。
2. `~/.config/te/config.json`（在 Windows 上为 `%USERPROFILE%\.config\te\config.json`）。
3. 如果没有配置文件，CLI 将使用内置默认值。

`TE_CONFIG` is honored consistently by every config-file operation - `te config list`, `te config set`, `te config init`, and `te config paths` all read and write at the resolved path. This is primarily intended for testing, scripted installs, and per-environment configuration.

要创建默认配置：

```bash
te config init             # Create config at TE_CONFIG (or ~/.config/te/config.json)
te config init --force     # Overwrite existing config
```

## 查看配置

```bash
te config list                         # Display all settings
te config list --output-format json    # Machine-readable
te config paths                        # Show resolved macros and BPA rule paths
```

使用 `te config paths` 查看 CLI 实际会为宏和 BPA 规则使用哪些文件。 It's handy when debugging missing data files. The output shows two rows: `macros` (the resolved macros file path or `[not set]`) and `bpa.rules` (the first existing BPA rules file resolved by the path resolver, or `[not set]`).

> [!NOTE]
> 在 `--output-format json` 模式下，`te config paths` 会显式输出值为 `null` 的字段 (例如 `{"macros": null, "bpa": {"rules": null}}`)。 Reporting resolution outcomes is the command's whole purpose, so `null` is a meaningful "tried but resolved to nothing" answer. `te config list --output-format json` strips null fields by default, so consumers should parse it tolerantly.

## 设置值

```bash
te config set autoFormat true
te config set bpa.onDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
te config set -p spinner=false         # -p key=value works too
```

Keys can be passed positionally (`te config set <key> <value>`) or as `-p key=value`. 如果键未知，命令将以退出码 `1` 失败，并返回一条列出有效键的错误信息。

如果配置文件不存在，`te config set` 会先在解析后的路径自动创建一个配置文件 (若设置了则为 `$TE_CONFIG`，否则为 `~/.config/te/config.json`)，然后再应用更改。

> [!NOTE]
> 架构中的每个键都可以通过 `te config set` 设置，包括通过点分路径设置嵌套键 (`bpa.onDeploy`、`formatOptions.useSqlBiDaxFormatter` 等)。 The only exception is `formatVersion`, which the CLI manages automatically. Run `te config paths` to find the config file if you'd rather edit the JSON directly.

## 完整 Schema

完整的 JSON 配置 Schema，包含所有键及其默认值。 Use this as a reference when editing the config file directly, or when looking up the dotted path for a `te config set` call.

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

### 文件路径

Set these in your config to avoid passing the same paths on every command. 每个命令的标志和环境变量都会覆盖配置值；请参阅下方的[路径解析优先级](#path-resolution-priority)。

| 键           | 含义                                                                                                                                                                                                                                                                                                                                            |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `macros`    | 宏 JSON 文件的显式路径 (通常为 `MacroActions.json`)。 Resolved by every `te macro` command. Point at a shared file (network share, repo-local, or even the TE3 desktop file) to reuse the same set of macros across machines and between the CLI and TE3 Desktop.                   |
| `bpa.rules` | Ordered list of paths or URLs to BPA rule files. `te bpa run` 和 deploy/save gate 会加载**所有**现有条目；`te bpa rules list` 和 `te config paths` 使用第一个现有条目。 Comma-separated values on `te config set bpa.rules ...` are split into the array.                                                                           |
| `queryLog`  | Path to a log file where every `te query` invocation appends its query text and execution metadata. Useful for audit trails or analyzing query patterns over time. Supports `~` for the home directory (e.g., `~/.config/te/queries.log`). |

### 路径解析优先级

对于每个用户提供的文件 (宏、BPA 规则)，CLI 会按以下顺序解析路径：

1. **命令行标志** - 宏命令使用 `--macros <path>`；部署/保存 gate 使用 `--bpa-rules <path>`；`te bpa rules` 子命令使用 `--rules-file <path>`。
2. **环境变量**：宏使用 `TE_MACROS_PATH`，BPA 规则使用 `TE_BPA_RULES`。
3. **CLI 配置**：宏使用 `macros`，BPA 规则使用 `bpa.rules[]` 中第一个现有条目。

CLI 不会自动检测 TE3 的任何安装位置——请显式配置这些项。 To start from a default file in the current working directory, run `te macro init` (creates `./MacroActions.json`) or `te bpa rules init` (creates `./BPARules.json`).

运行 `te config paths` 可查看 CLI 实际解析到的是哪个文件。

### 行为默认值

所有与 BPA 相关的设置都位于 `bpa` 对象下，并可在 `te config set` 中使用点号分隔的键进行设置。

| 键名                           | 默认值     | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `autoFormat`                 | `false` | Automatically format the DAX expressions changed by a mutating command. Formatting is scoped to the objects the command touched but covers every DAX expression property they hold (expressions, format string expressions, detail rows, KPI target/status/trend, calculation group and table permission expressions, etc.). Power Query (M) and SQL partition queries are never reformatted. Always uses the built-in offline formatter in the comma dialect; the `formatOptions` layout keys apply.                                                                                        |
| `validateOnMutation`         | `true`  | After a mutating command (`add`, `set`, `mv`, `macro run`), check that every `Table[Column]` reference in the model still resolves. Catches dangling references introduced by renames or removals before they reach deploy.                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `mutationOutput`             | `diff`  | How mutating commands (`add`, `set`, `move`, `remove`, `script`, `bpa run --fix`) render the resulting change set in text output: `diff` (full before/after diff), `stat` (per-object change counts), `name-only` (changed object paths), or `none` (suppress the change set; config-only - there is no `--none` flag). The per-command `--diff` / `--stat` / `--name-only` flags override for one invocation. JSON output always carries the full `changes` array regardless.                                                                      |
| `bpa.onMutation`             | `false` | 在每次更改命令（`set`、`add`、`mv`、`rm`、`macro run`）后，运行一次限定范围的 BPA 分析。 Only the affected table's objects are checked, not the whole model - useful for fast feedback during iterative edits.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `bpa.onDeploy`               | `true`  | Run the BPA gate before `te deploy` executes. The deploy is aborted if any rule fires at severity >= error. Bypass per-invocation with `--skip-bpa`, or auto-fix with `--fix-bpa`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `bpa.onSave`                 | `true`  | Run the BPA gate before `te save-as` writes to disk. Bypass per-invocation with `--skip-bpa` or `--force`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `bpa.builtInRules`           | `true`  | Include the curated built-in BPA rule set whenever the gate runs. 设为 `false` 可完全忽略内置规则；此时关卡检查只运行通过 `bpa.rules` 配置的规则以及嵌入模型中的规则。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `bpa.disabledBuiltInRuleIds` | `null`  | IDs of individual built-in rules to exclude from the gate. 可通过 `te bpa rules disable <id>` / `te bpa rules enable <id>` 修改——优先使用这些命令，而不是直接编辑该数组。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `vertipaqOnRefresh`          | `false` | 成功刷新后（`full`、`dataonly`、`automatic` 或 `add`），自动运行 VertiPaq 分析，以显示已刷新表的存储统计信息。 Useful for catching unexpected cardinality or memory regressions immediately.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `interactiveEditMode`        | `stage` | Default behavior for in-memory mutations inside `te interactive`. `stage` 会将变更保留在内存中，直到调用 `save`（最安全）；`save` 会在每次产生变更的命令后写回源（对远程源请谨慎使用——每次 `set` 都会触发一次 XMLA 写入）；`revert` 会在每条命令后丢弃变更，除非传入了 `--save` 或 `--stage`。 Per-command `--save` / `--revert` / `--stage` flags always override.                                                                                                                                                                                                                                                                                                                                                                                             |
| `launchInteractiveMode`      | `auto`  | Whether running `te` in a terminal with no arguments launches the interactive REPL. `auto` (default) launches the REPL only when all three streams (stdin, stdout, stderr) are attached to a TTY, so scripts and CI pipelines fall through to normal parse. `always` launches the REPL regardless of redirection. `never` disables the auto-launch entirely, restoring the traditional help-on-empty behavior. The global `--non-interactive` flag forces `never` for a single invocation. Can also be set for one invocation via the `TE_INTERACTIVE` environment variable. |
| `disableTelemetry`           | `false` | Opt out of anonymous usage telemetry. The CLI collects coarse-grained command usage data (command name, exit code, duration) to inform feature priority. The CLI never collects model content, paths, or query text.                                                                                                                                                                                                                                                                                                                                                                                                                            |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### 格式选项

Applied whenever the CLI formats DAX. The CLI ships a formatter that works fully offline. The layout keys (`shortFormat`, `skipSpaceAfterFunction`) apply when `autoFormat` reformats mutated expressions and when `te query` renders query text; explicit formatting via `te set <path> --format <Property>` and `te util format-dax` takes the equivalent per-invocation flags (`--long`, `--no-space-after-function`) instead. There is deliberately no list-separator key: DAX stored in a model or sent to Analysis Services is always comma-separated, so every config-driven formatting pass uses commas. The one place the semicolon dialect applies is the `--semicolons` flag on `te util format-dax`, for DAX you have typed with semicolons yourself. `formatOptions.useSqlBiDaxFormatter` routes explicit formatting and `te query`'s rendering through the SQL BI [daxformatter.com](https://www.daxformatter.com) web service (requires internet access) if you need that style; `autoFormat` always uses the built-in formatter regardless.

| 键                                      | 默认值     | 说明                                                                                                                                                                                                                                                                                                                                      |
| -------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `formatOptions.shortFormat`            | `false` | 尽可能优先使用简短的单行格式，而不是默认的多行布局。                                                                                                                                                                                                                                                                                                              |
| `formatOptions.skipSpaceAfterFunction` | `false` | 省略函数名称与左括号之间的空格（例如使用 `SUM(x)`，而不是 `SUM (x)`）。                                                                                                                                                                                                                                                                                           |
| `formatOptions.useSqlBiDaxFormatter`   | `false` | Format DAX via the [SQL BI daxformatter.com](https://www.daxformatter.com) web service instead of the built-in formatter. Requires internet access. The built-in formatter (default) works offline and matches the Tabular Editor 3 Desktop default. |

### 显示

控制 CLI 终端输出和诊断详细程度的设置。

| 键                   | 默认值     | 说明                                                                                                        |
| ------------------- | ------- | --------------------------------------------------------------------------------------------------------- |
| `hidePreviewNotice` | `false` | Suppress the yellow preview banner. **Ignored within 14 days of expiry.** |
| `spinner`           | `true`  | Show animated progress indicators in the terminal. Disable for CI.        |
| `debug`             | `false` | 始终启用调试日志（等同于传入 `--debug`）。                                                                                |

### 配置文件

Saved connection profiles live under the `profiles` key. Don't edit them by hand - use `te profile set / remove / list`. See @te-cli-auth for profile management.

Profiles can carry **overrides** that override the behavioral defaults above whenever the profile is active. The keys a profile can override are `autoFormat`, `validateOnMutation`, `mutationOutput`, `bpa.onMutation`, `bpa.onDeploy`, `bpa.onSave`, `vertipaqOnRefresh`, `spinner`, and `interactiveEditMode`. This is how a dev profile can relax validation and BPA while a prod profile keeps them strict:

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

`te profile set` exposes flags for the common ones (`--auto-format`, `--validate-on-mutation`, `--bpa-on-mutation`, `--bpa-on-deploy`, `--vertipaq-on-refresh`, `--spinner`); each accepts `true`, `false`, or `null` to clear the override.

## BPA 闸门

BPA 闸门是一道安全防线，用于防止存在规则违规的模型被保存或部署。 It runs automatically when the following commands are executed:

- `te deploy` 会触发闸门检查，除非传入 `--skip-bpa` 或 `bpa.onDeploy` 为 `false`。
- `te save-as` runs the gate unless `--skip-bpa` (or `--force`) is passed or `bpa.onSave` is `false`.
- `te add`, `te set`, `te move`, `te remove`, `te macro run` run the gate only when `bpa.onMutation` is `true`.

闸门检查会从 `bpa.rules` 加载 BPA 规则，并且默认还会加载内置规则集（由 `bpa.builtInRules` 控制）。 Built-in rules can be individually excluded via `bpa.disabledBuiltInRuleIds` - managed with `te bpa rules disable <id>` / `te bpa rules enable <id>`.

When the gate fires and finds violations at severity >= `error`, the command fails with exit code `1` and a summary of the violations. 可用的解决办法：

- `--fix-bpa` - 在内存中将规则的 `fixExpression` 应用于部署/保存产物；不会修改源文件。
- `--skip-bpa` - 仅对本次命令禁用闸门检查。
- `--bpa-rules <path>` - repeatable; override `bpa.rules` for this single `te deploy` or `te save-as` invocation. 除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。

可单独运行 `te bpa run`，在不部署的情况下预览闸门检查的行为：

```bash
te bpa run --model ./model --fail-on error
te bpa run --model ./model --fix --save     # Apply fixes to the source
```

### 内置 BPA 规则

CLI 随附一套权威的内置 BPA 规则集，并以 JSON 资源的形式嵌入其中。 Built-in rules are read-only - `te bpa rules set` and `te bpa rules remove` refuse to mutate built-in IDs and point users at `te bpa rules disable` instead. To customize a built-in rule's behavior, copy it into your local rules file as a new rule with a different ID and disable the built-in.

`bpa.builtInRules` 和 `bpa.disabledBuiltInRuleIds` 会一致地应用于部署/保存/变更的门控检查 **以及** 手动执行的 `te bpa run` 命令——通过 `te bpa rules disable` 禁用一次后，该规则将在所有场景中被排除。

## 变更后行为

When you run a mutating command (`te add`, `te set`, `te move`, `te macro run`), the CLI performs these checks automatically:

1. **TOM errors** are always surfaced. 度量值、列、分区或计算项中的无效 DAX 或 M 始终会导致命令失败。
2. **架构验证** (`validateOnMutation`，默认值为 `true`) 会验证 DAX 中的 `Table[Column]` 引用是否仍可解析，并交叉检查元数据一致性。
3. **DAX 自动格式化** (`autoFormat`，默认值为 `false`) 在启用时会通过内置的 DAX Formatter 格式化此次变更涉及的所有表达式。
4. **变更时运行 BPA** (`bpa.onMutation`，默认值为 `false`) 在启用时会在变更后运行 BPA，并根据 `--fail-on` 发出警告或使命令失败。

可使用 `te config set <key> false` 禁用某项检查，或通过配置文件将放宽范围限定到特定环境。

## Administrator policies

On Windows, `te` honors the same administrator policies as Tabular Editor 3. Policies are read from the registry under `Software\Policies\Tabular Editor ApS` - with an optional `TECLI` subkey for values that should apply to the CLI only, and a `TE3` subkey for the desktop - and from the earlier `Software\Policies\Kapacity\Tabular Editor` key, which keeps working unchanged. A machine-wide value (`HKEY_LOCAL_MACHINE`) takes precedence over a per-user one (`HKEY_CURRENT_USER`), and within a hive a product-specific value takes precedence over a shared one. Where a policy turns a feature off, the command names the policy responsible, does nothing, and exits with a failure - so a pipeline that depends on something an administrator has since turned off fails visibly rather than reporting success for work it never did.

| Policy                 | Effect on the CLI                                                                                                                                                                                                                                                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `DisableCSharpScripts` | Refuses `te script` and the automatic fixes of `te bpa run --fix`.                                                                                                                                                                                                                                                   |
| `DisableMacros`        | Refuses every `te macro` command.                                                                                                                                                                                                                                                                                    |
| `DisableBpaDownload`   | Refuses Best Practice Analyzer rules given as a URL. Rule files on disk and the built-in rules are unaffected.                                                                                                                                                                                       |
| `DisableTelemetry`     | Turns anonymous usage statistics off, whatever `disableTelemetry` in config says.                                                                                                                                                                                                                                    |
| `BlockUnsafeScripts`   | Allows `te script`, `te macro run` and `te bpa run --fix` only where the code stays within the semantic model. Anything that reads or writes a file, reaches the network, starts another program or references an outside assembly is refused before it runs, with `blockedByPolicy` in JSON output. |

Policies that govern features the CLI does not have - update checks, error reports, DAX Optimizer, the DAX Package Manager, the AI assistant, and the MCP server - have no effect on it. See @policies for the full list of policies and how to deploy them.

`BlockUnsafeScripts` requires Tabular Editor 3 Enterprise Edition in the desktop application. The CLI has no editions, so it simply applies the policy wherever it finds it. See [C# Scripts](xref:csharp-scripts#administrator-policies) for what counts as staying within the model.

## 环境变量

Use the following CLI-specific environment variables for paths, behavior, and diagnostics. 有关 Azure 身份验证变量（`AZURE_CLIENT_ID`、`AZURE_TENANT_ID`、`AZURE_CLIENT_CERTIFICATE_PATH` 等），见 @te-cli-auth。

| 变量               | 用途                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TE_CONFIG`      | Path to an alternative config file. Honored by every `te config` operation (`list`, `set`, `init`, `paths`).                                                                                                                                                                                                                         |
| `TE_MACROS_PATH` | 覆盖宏文件路径（在解析顺序中排第二，见上文）。 Read by `te macro` commands.                                                                                                                                                                                                                                                                                                                    |
| `TE_BPA_RULES`   | 覆盖 `te bpa run` 和 `te bpa rules` 子命令使用的 BPA 规则文件/URL 列表。                                                                                                                                                                                                                                                                                                                                |
| `TE_BPA_CONFIG`  | 覆盖 deploy/save 门禁读取的 BPA 门禁配置 (`.te-bpa.json`) 的路径。                                                                                                                                                                                                                                                                                                                  |
| `TE_DEBUG`       | 设为 `1` 可全局启用调试日志（等同于 `--debug` 或配置中的 `debug: true`）。                                                                                                                                                                                                                                                                                                                                    |
| `NO_SPINNER`     | 设为 `1` 或 `true` 可禁用动画进度指示器（可替代配置中的 `spinner: false`）。                                                                                                                                                                                                                                                                                                                                   |
| `CI`             | Auto-detected. When `1` or `true`, the CLI disables the spinner and switches to plain output. Most CI runners set this automatically.                                                                                                                                                                                                   |
| `TE_SESSION`     | Override the per-terminal session ID used for active-connection state. Useful for running multiple isolated CLI sessions inside the same shell, e.g. in parallel CI matrix jobs. Inspect and manage sessions with [`te session`](xref:te-cli-commands#session).                                         |
| `TE_INTERACTIVE` | Override `launchInteractiveMode` for a single invocation. Accepts `auto`, `always`, or `never`. Handy for one-off scripts that want the interactive REPL (`TE_INTERACTIVE=always`) or want to force the classic help-on-empty behavior (`TE_INTERACTIVE=never`) without touching the config file. |
| `TE_COMPAT`      | 设为 `te2` 可强制启用 TE2 兼容模式；参见 @te-cli-migrate。                                                                                                                                                                                                                                                                                                                                |

## 相关页面

- @te-cli-auth - 配置文件、身份验证和凭据存储。
- @te-cli-commands - `te config` 子命令。
- @te-cli-cicd - 为管道配置 BPA 门禁。
