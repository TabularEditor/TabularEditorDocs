---
uid: te-cli-config
title: 自定义配置
author: Peer Grønnerup
updated: 2026-10-12
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

Tabular Editor CLI 可从 JSON 文件读取可选配置。 The file sets:

- **File paths**: where the CLI reads macros and BPA rules, and where it writes the query log.
- **Behavioral defaults**: BPA gates, auto-format and validation.
- **Saved connection profiles**: the named profiles you switch between.

The CLI doesn't read from or write to Tabular Editor 3 desktop install paths. Set the BPA rules and macros files in this config, or create them with `te bpa rules init` and `te macro init`.

`te config list`, `te config set <key> <value>` and `te profile set` cover the common operations without editing the file.

## 配置文件位置

The CLI checks these locations in order:

1. `$TE_CONFIG` 环境变量（如果已设置且文件存在）。
2. `~/.config/te/config.json`（在 Windows 上为 `%USERPROFILE%\.config\te\config.json`）。
3. 如果没有配置文件，CLI 将使用内置默认值。

`te config list`, `te config set`, `te config init` and `te config paths` all read and write the file at the resolved path, including a path set by `TE_CONFIG`. Use `TE_CONFIG` for testing, scripted installs and per-environment configuration.

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

`te config paths` shows which files the CLI uses for macros and BPA rules. The output has two rows: `macros`, the resolved macros file path, and `bpa.rules`, the first existing BPA rules file. Either row shows `[not set]` if nothing resolves.

> [!NOTE]
> With `--output-format json`, `te config paths` writes unresolved paths as explicit `null` fields, for example `{"macros": null, "bpa": {"rules": null}}`. `te config list --output-format json` omits null fields by default, so parsers must handle missing keys.

## 设置值

```bash
te config set autoFormat true
te config set bpa.onDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
te config set -p spinner=false         # -p key=value works too
```

键可以按位置传入（`te config set <key> <value>`），也可以使用 `-p key=value`。如果键未知，命令将以退出码 `1` 失败，并返回一条列出有效键的错误信息。

如果配置文件不存在，`te config set` 会先在解析后的路径自动创建一个配置文件 (若设置了则为 `$TE_CONFIG`，否则为 `~/.config/te/config.json`)，然后再应用更改。

> [!NOTE]
> `te config set` sets every key in the schema except `formatVersion`, which the CLI manages. Use dotted paths for nested keys, such as `bpa.onDeploy` or `formatOptions.useSqlBiDaxFormatter`. To edit the JSON directly, run `te config paths` to find the file.

## 完整 Schema

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

### 文件路径

Paths set in the config apply to every command. Per-command flags and environment variables override them, as described in [Path resolution priority](#path-resolution-priority).

| 键           | 含义                                                                                                                                                                                                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `macros`    | 宏 JSON 文件的显式路径 (通常为 `MacroActions.json`)。每个 `te macro` 命令都会解析它。 To use the same macros on several machines or in both the CLI and Tabular Editor 3, point it at a shared file, such as a file on a network share, in the repository or the Tabular Editor 3 desktop file. |
| `bpa.rules` | 指向 BPA 规则文件的路径或 URL 的有序列表。 `te bpa run` 和 deploy/save gate 会加载**所有**现有条目；`te bpa rules list` 和 `te config paths` 使用第一个现有条目。在 `te config set bpa.rules ...` 中使用逗号分隔的值时，会将其拆分为数组。                                                                                                                              |
| `queryLog`  | 日志文件路径，每次调用 `te query` 时都会将其查询文本和执行元数据追加到该文件中。 Supports `~` for the home directory, for example `~/.config/te/queries.log`.                                                                                                                                                                  |

### 路径解析优先级

对于每个用户提供的文件 (宏、BPA 规则)，CLI 会按以下顺序解析路径：

1. **命令行标志** - 宏命令使用 `--macros <path>`；部署/保存 gate 使用 `--bpa-rules <path>`；`te bpa rules` 子命令使用 `--rules-file <path>`。
2. **环境变量**：宏使用 `TE_MACROS_PATH`，BPA 规则使用 `TE_BPA_RULES`。
3. **CLI 配置**：宏使用 `macros`，BPA 规则使用 `bpa.rules[]` 中第一个现有条目。

The CLI doesn't detect Tabular Editor 3 install locations. To create a default file in the current directory, run `te macro init` (creates `./MacroActions.json`) or `te bpa rules init` (creates `./BPARules.json`).

运行 `te config paths` 可查看 CLI 实际解析到的是哪个文件。

### 行为默认值

BPA settings are under the `bpa` object, and you address them with dotted keys in `te config set`.

| 键名                           | 默认值     | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `autoFormat`                 | `false` | 自动格式化由会产生变更的命令改动过的 DAX 表达式。格式化范围仅限于命令触及的对象，但会覆盖这些对象包含的所有 DAX 表达式属性（表达式、格式字符串表达式、明细行、KPI 目标/状态/趋势、计算组和表格权限表达式等）。 Power Query (M) 和 SQL 分区查询永远不会被重新格式化。始终使用内置的离线格式化程序并采用逗号方言；`formatOptions` 布局键会生效。                                                                                                                                                                                                                                                                                                                                                                                        |
| `validateOnMutation`         | `true`  | 在执行更改命令（`add`、`set`、`mv`、`macro run`）后，检查模型中的每个 `Table[Column]` 引用是否仍可解析。 This catches references broken by renames or removals before deployment.                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `mutationOutput`             | `diff`  | How mutating commands (`add`, `set`, `move`, `remove`, `script`, `bpa run --fix`) render the resulting change set in text output: `diff` (full before/after diff), `stat` (per-object change counts), `name-only` (changed object paths), or `none` (no change set; config only, with no `--none` flag). The `--diff`, `--stat` and `--name-only` flags override it for one invocation. JSON output always contains the full `changes` array. |
| `bpa.onMutation`             | `false` | 在每次更改命令（`set`、`add`、`mv`、`rm`、`macro run`）后，运行一次限定范围的 BPA 分析。 Only the objects of the affected table are checked.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `bpa.onDeploy`               | `true`  | 在执行 `te deploy` 之前运行 BPA 关卡检查。如果有任何规则以严重级别 >= error 触发，部署将中止。可通过 `--skip-bpa` 在单次调用中跳过，或通过 `--fix-bpa` 自动修复。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `bpa.onSave`                 | `true`  | 在 `te save-as` 写入磁盘之前运行 BPA 闸门检查。可通过 `--skip-bpa` 或 `--force` 在单次调用中跳过。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `bpa.builtInRules`           | `true`  | 每次运行关卡检查时，都包含精选的内置 BPA 规则集。 If `false`, the gate runs only the rules in `bpa.rules` and rules embedded in the model.                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `bpa.disabledBuiltInRuleIds` | `null`  | 要从门禁中排除的各个内置规则的 ID。 Change it with `te bpa rules disable <id>` and `te bpa rules enable <id>`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `vertipaqOnRefresh`          | `false` | After a successful refresh (`full`, `dataonly`, `automatic`, or `add`), run VertiPaq analysis and show storage statistics for the refreshed tables.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `interactiveEditMode`        | `stage` | 在 `te interactive` 中对内存中变更的默认处理方式。 `stage` keeps mutations in memory until you run `save`. `save` writes to the source after every mutating command; on a remote source, every `set` is an XMLA write. `revert` discards mutations after each command unless you pass `--save` or `--stage`. The per-command `--save`, `--revert` and `--stage` flags override the setting.                                                                                                                                                                  |
| `launchInteractiveMode`      | `auto`  | 控制在终端中不带任何参数运行 `te` 时，是否启动交互式 REPL。 `auto` (default) launches the REPL only if stdin, stdout and stderr are all attached to a TTY, so scripts and CI pipelines get normal parsing. `always` launches the REPL even with redirection. `never` shows help instead. The global `--non-interactive` flag forces `never` for one invocation, and the `TE_INTERACTIVE` environment variable sets the mode for one invocation.                                                                                                   |
| `disableTelemetry`           | `false` | 选择不参与匿名使用遥测数据收集。 Telemetry contains the command name, exit code and duration. It doesn't contain model content, paths or query text.                                                                                                                                                                                                                                                                                                                                                                                                                                         |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### 格式选项

The CLI's built-in DAX formatter works offline.

- The layout keys `shortFormat` and `skipSpaceAfterFunction` apply when `autoFormat` reformats mutated expressions and when `te query` renders query text.
- `te set <path> --format <Property>` and `te util format-dax` ignore the layout keys and take the flags `--long` and `--no-space-after-function`.
- Config-driven formatting always uses commas as list separators. For DAX written with semicolons, use the `--semicolons` flag of `te util format-dax`.
- `formatOptions.useSqlBiDaxFormatter` sends explicit formatting and `te query` rendering to the SQL BI [daxformatter.com](https://www.daxformatter.com) web service, which requires internet access. `autoFormat` always uses the built-in formatter.

| 键                                      | 默认值     | 说明                                                                                                                                                                                                          |
| -------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `formatOptions.shortFormat`            | `false` | Use short, single-line formatting where possible.                                                                                                                                           |
| `formatOptions.skipSpaceAfterFunction` | `false` | Omit the space between a function name and its opening parenthesis, for example `SUM(x)`.                                                                                                   |
| `formatOptions.useSqlBiDaxFormatter`   | `false` | Format DAX with the [SQL BI daxformatter.com](https://www.daxformatter.com) web service. 需要联网。 The built-in formatter matches the Tabular Editor 3 default. |

### 显示

These settings control terminal output and diagnostic logging.

| 键                   | 默认值     | 说明                                |
| ------------------- | ------- | --------------------------------- |
| `hidePreviewNotice` | `false` | 隐藏黄色预览横幅。**距离到期不足 14 天时，将忽略此设置。** |
| `spinner`           | `true`  | 在终端中显示动画进度指示器。在 CI 环境中禁用。         |
| `debug`             | `false` | 始终启用调试日志（等同于传入 `--debug`）。        |

### 配置文件

Saved connection profiles are stored under the `profiles` key. Manage them with `te profile set`, `te profile remove` and `te profile list`, not by editing the file. 见 @te-cli-auth。

A profile can override these behavioral defaults while it's active: `autoFormat`, `validateOnMutation`, `mutationOutput`, `bpa.onMutation`, `bpa.onDeploy`, `bpa.onSave`, `vertipaqOnRefresh`, `spinner` and `interactiveEditMode`. For example, a dev profile can turn off validation and the deploy gate while a prod profile formats DAX:

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

`te profile set` has flags for `--auto-format`, `--validate-on-mutation`, `--bpa-on-mutation`, `--bpa-on-deploy`, `--vertipaq-on-refresh` and `--spinner`. Each accepts `true`, `false` or `null`, which clears the override.

## BPA 闸门

The BPA gate stops a save or deployment if the model has rule violations at error severity. It runs on these commands:

- `te deploy` 会触发闸门检查，除非传入 `--skip-bpa` 或 `bpa.onDeploy` 为 `false`。
- `te save-as` 会运行闸门检查，除非传入 `--skip-bpa`（或 `--force`），或 `bpa.onSave` 为 `false`。
- `te add`、`te set`、`te move`、`te remove`、`te macro run` 仅在 `bpa.onMutation` 为 `true` 时才会执行 gate 检查。

闸门检查会从 `bpa.rules` 加载 BPA 规则，并且默认还会加载内置规则集（由 `bpa.builtInRules` 控制）。 `te bpa rules disable <id>` excludes an individual built-in rule by adding it to `bpa.disabledBuiltInRuleIds`, and `te bpa rules enable <id>` removes it from the list.

If the gate finds violations at severity `error` or higher, the command fails with exit code `1` and a summary of the violations. To proceed, use one of these options:

- `--fix-bpa` - 在内存中将规则的 `fixExpression` 应用于部署/保存产物；不会修改源文件。
- `--skip-bpa` - 仅对本次命令禁用闸门检查。
- `--bpa-rules <path>` - 可重复指定；仅在本次调用 `te deploy` 或 `te save-as` 时覆盖 `bpa.rules`。除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。

To check the model against the rules without deploying, run `te bpa run`:

```bash
te bpa run --model ./model --fail-on error
te bpa run --model ./model --fix --save     # Apply fixes to the source
```

### 内置 BPA 规则

The CLI includes a set of built-in BPA rules. Built-in rules are read-only: `te bpa rules set` and `te bpa rules remove` fail on built-in IDs and suggest `te bpa rules disable`. To change a built-in rule, copy it into your rules file with a new ID and disable the built-in rule.

`bpa.builtInRules` and `bpa.disabledBuiltInRuleIds` apply to the gate and to `te bpa run`, so a rule disabled with `te bpa rules disable` is excluded everywhere.

## 变更后行为

After a mutating command (`te add`, `te set`, `te move` or `te macro run`), the CLI runs these checks:

1. **TOM errors** always appear. Invalid DAX or M in measures, columns, partitions or calculation items fails the command.
2. **Schema validation** (`validateOnMutation`, default `true`) verifies that `Table[Column]` references in DAX still resolve.
3. **DAX auto-format** (`autoFormat`, default `false`) formats the expressions touched by the mutation with the built-in formatter.
4. **BPA on mutation** (`bpa.onMutation`, default `false`) runs BPA after the mutation and warns or fails according to `--fail-on`.

`te config set <key> false` turns a check off. A profile can override the key for one environment.

## 管理员策略

On Windows, `te` honors the same administrator policies as Tabular Editor 3 and reads them from these registry keys:

- `Software\Policies\Tabular Editor ApS`, for values shared by the CLI and the desktop application
- its `TECLI` subkey, for values that apply to the CLI only
- its `TE3` subkey, for values that apply to the desktop application only
- the earlier `Software\Policies\Kapacity\Tabular Editor` key, which is still honored

A machine-wide value (`HKEY_LOCAL_MACHINE`) takes precedence over a per-user one (`HKEY_CURRENT_USER`). Within a hive, a product-specific value takes precedence over a shared one. When a policy turns a feature off, the command names the policy, does nothing and exits with a failure, which fails any pipeline step that depends on the feature.

| 策略                     | 对 CLI 的影响                                                                                                                                                                                                                                                                                                                                                      |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DisableCSharpScripts` | Blocks `te script` and the automatic fixes of `te bpa run --fix`.                                                                                                                                                                                                                                                                              |
| `DisableMacros`        | Blocks every `te macro` command.                                                                                                                                                                                                                                                                                                               |
| `DisableBpaDownload`   | Blocks Best Practice Analyzer rules given as a URL. 磁盘上的规则文件和内置规则不受影响。                                                                                                                                                                                                                                                                         |
| `DisableTelemetry`     | 无论配置中的 `disableTelemetry` 如何设置，都会关闭匿名使用情况统计。                                                                                                                                                                                                                                                                                                                   |
| `BlockUnsafeScripts`   | Blocks `te script`, `te macro run` and `te bpa run --fix` when the code accesses files, the network, processes or external assemblies. See [What counts as staying within the model](xref:csharp-scripts#what-counts-as-staying-within-the-model) for the blocked APIs. JSON output reports `blockedByPolicy`. |

Policies for update checks, error reports, DAX Optimizer, the DAX Package Manager, the AI Assistant and the MCP server don't affect the CLI. 完整的策略列表及部署方式见 @policies。

In the desktop application, `BlockUnsafeScripts` requires Tabular Editor 3 Enterprise Edition. The CLI has no editions and applies the policy wherever it's set.

## 环境变量

The CLI reads these environment variables for paths, behavior and diagnostics. 有关 Azure 身份验证变量（`AZURE_CLIENT_ID`、`AZURE_TENANT_ID`、`AZURE_CLIENT_CERTIFICATE_PATH` 等），见 @te-cli-auth。

| 变量               | 用途                                                                                                                                                                                              |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TE_CONFIG`      | 替代配置文件的路径。 Used by `te config list`, `set`, `init` and `paths`.                                                                                                                 |
| `TE_MACROS_PATH` | Override the macros file path, second in the [resolution order](#path-resolution-priority). 由 `te macro` 命令读取。                                                                  |
| `TE_BPA_RULES`   | 覆盖 `te bpa run` 和 `te bpa rules` 子命令使用的 BPA 规则文件/URL 列表。                                                                                                                                        |
| `TE_BPA_CONFIG`  | 覆盖 deploy/save 门禁读取的 BPA 门禁配置 (`.te-bpa.json`) 的路径。                                                                                                                          |
| `TE_DEBUG`       | 设为 `1` 可全局启用调试日志（等同于 `--debug` 或配置中的 `debug: true`）。                                                                                                                                            |
| `NO_SPINNER`     | 设为 `1` 或 `true` 可禁用动画进度指示器（可替代配置中的 `spinner: false`）。                                                                                                                                           |
| `CI`             | 自动检测。当设为 `1` 或 `true` 时，CLI 会禁用动画进度指示器，并切换为纯文本输出。 Most CI runners set it.                                                                                                       |
| `TE_SESSION`     | 覆盖用于活动连接状态的按终端划分的会话 ID。 Set it to run isolated CLI sessions in the same shell, for example in parallel CI matrix jobs. 使用 [`te session`](xref:te-cli-commands#session) 查看并管理会话。 |
| `TE_INTERACTIVE` | 为单次调用临时覆盖 `launchInteractiveMode` 设置。 Accepts `auto`, `always` or `never`. `TE_INTERACTIVE=always` launches the REPL, and `TE_INTERACTIVE=never` shows help.    |
| `TE_COMPAT`      | 设为 `te2` 可强制启用 TE2 兼容模式；参见 @te-cli-migrate。                                                                                                                                        |

## 后续步骤

- @te-cli-auth - 配置文件、身份验证和凭据存储。
- @te-cli-commands - `te config` 子命令。
- @te-cli-cicd - 为管道配置 BPA 门禁。
