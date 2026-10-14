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

Tabular Editor CLI 可从 JSON 文件读取可选配置。该文件用于设置：

- **文件路径**：CLI 用于读取宏和 BPA 规则的位置，以及写入查询日志的位置。
- **行为默认值**：BPA 门槛、自动格式化和验证。
- **已保存的连接配置文件**：可在这些命名配置之间切换。

CLI 不会从 Tabular Editor 3 桌面版安装路径读取内容，也不会向其中写入内容。在此配置中设置 BPA 规则和宏文件，或使用 `te bpa rules init` 和 `te macro init` 创建它们。

无需编辑该文件，`te config list`、`te config set <key> <value>` 和 `te profile set` 即可完成常见操作。

## 配置文件位置

CLI 会按以下顺序检查这些位置：

1. `$TE_CONFIG` 环境变量（如果已设置且文件存在）。
2. `~/.config/te/config.json`（在 Windows 上为 `%USERPROFILE%\.config\te\config.json`）。
3. 如果没有配置文件，CLI 将使用内置默认值。

`te config list`、`te config set`、`te config init` 和 `te config paths` 都会在解析后的路径上读取和写入该文件，包括通过 `TE_CONFIG` 设置的路径。可将 `TE_CONFIG` 用于测试、脚本化安装以及按环境配置。

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

`te config paths` 会显示 CLI 为宏和 BPA 规则使用的是哪些文件。输出有两行：`macros`，表示解析后的宏文件路径；`bpa.rules`，表示第一个存在的 BPA 规则文件。如果未解析到任何内容，对应行会显示 `[not set]`。

> [!NOTE]
> 使用 `--output-format json` 时，`te config paths` 会将未解析的路径写成显式的 `null` 字段，例如 `{"macros": null, "bpa": {"rules": null}}`。 `te config list --output-format json` 默认会省略值为 null 的字段，因此解析器必须处理缺失的键。

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
> `te config set` 可设置 schema 中除 `formatVersion` 之外的所有键，后者由 CLI 管理。对嵌套键使用点号路径，例如 `bpa.onDeploy` 或 `formatOptions.useSqlBiDaxFormatter`。如果要直接编辑 JSON，请运行 `te config paths` 来找到该文件。

## 完整 Schema

完整的配置 schema，其中每个键都为默认值：

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

在配置中设置的路径适用于每个命令。每个命令的标志和环境变量都会覆盖这些设置，如 [路径解析优先级](#path-resolution-priority) 所述。

| 键           | 含义                                                                                                                                                                                                 |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `macros`    | 宏 JSON 文件的显式路径 (通常为 `MacroActions.json`)。每个 `te macro` 命令都会解析它。如果你想在多台机器上，或在 CLI 与 Tabular Editor 3 中共用同一套宏，请将其指向一个共享文件，例如网络共享上的文件、repository 中的文件，或 Tabular Editor 3 桌面版使用的文件。 |
| `bpa.rules` | 指向 BPA 规则文件的路径或 URL 的有序列表。 `te bpa run` 和 deploy/save gate 会加载**所有**现有条目；`te bpa rules list` 和 `te config paths` 使用第一个现有条目。在 `te config set bpa.rules ...` 中使用逗号分隔的值时，会将其拆分为数组。                    |
| `queryLog`  | 日志文件路径，每次调用 `te query` 时都会将其查询文本和执行元数据追加到该文件中。支持使用 `~` 表示主目录，例如 `~/.config/te/queries.log`。                                                                                                        |

### 路径解析优先级

对于每个用户提供的文件 (宏、BPA 规则)，CLI 会按以下顺序解析路径：

1. **命令行标志** - 宏命令使用 `--macros <path>`；部署/保存 gate 使用 `--bpa-rules <path>`；`te bpa rules` 子命令使用 `--rules-file <path>`。
2. **环境变量**：宏使用 `TE_MACROS_PATH`，BPA 规则使用 `TE_BPA_RULES`。
3. **CLI 配置**：宏使用 `macros`，BPA 规则使用 `bpa.rules[]` 中第一个现有条目。

CLI 不会检测 Tabular Editor 3 的安装位置。要在当前目录中创建默认文件，运行 `te macro init`（创建用于宏的 `./MacroActions.json`）或 `te bpa rules init`（创建 `./BPARules.json`）。

运行 `te config paths` 可查看 CLI 实际解析到的是哪个文件。

### 行为默认值

BPA 设置位于 `bpa` 对象下，并在 `te config set` 中通过点号分隔的键来指定这些设置。

| 键名                           | 默认值     | 说明                                                                                                                                                                                                                                                            |
| ---------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `autoFormat`                 | `false` | 自动格式化由会产生变更的命令改动过的 DAX 表达式。格式化范围仅限于命令触及的对象，但会覆盖这些对象包含的所有 DAX 表达式属性（表达式、格式字符串表达式、明细行、KPI 目标/状态/趋势、计算组和表格权限表达式等）。 Power Query (M) 和 SQL 分区查询永远不会被重新格式化。始终使用内置的离线格式化程序并采用逗号方言；`formatOptions` 布局键会生效。                                         |
| `validateOnMutation`         | `true`  | 在执行更改命令（`add`、`set`、`mv`、`macro run`）后，检查模型中的每个 `Table[Column]` 引用是否仍可解析。这可在部署前发现因重命名或删除导致的失效引用。                                                                                                                                                              |
| `mutationOutput`             | `diff`  | 变更命令（`add`、`set`、`move`、`remove`、`script`、`bpa run --fix`）在文本输出中如何呈现最终的变更集：`diff`（完整的前后差异）、`stat`（按对象统计的变更计数）、`name-only`（已变更对象路径），或 `none`（不显示变更集；仅可通过配置项设置——没有 `--none` 标志）。 `--diff`、`--stat` 和 `--name-only` 标志可在单次调用中覆盖该设置。 JSON 输出始终包含完整的 `changes` 数组。 |
| `bpa.onMutation`             | `false` | 在每次更改命令（`set`、`add`、`mv`、`rm`、`macro run`）后，运行一次限定范围的 BPA 分析。仅检查受影响表中的对象。                                                                                                                                                                                     |
| `bpa.onDeploy`               | `true`  | 在执行 `te deploy` 之前运行 BPA 关卡检查。如果有任何规则以严重级别 >= error 触发，部署将中止。可通过 `--skip-bpa` 在单次调用中跳过，或通过 `--fix-bpa` 自动修复。                                                                                                                                                  |
| `bpa.onSave`                 | `true`  | 在 `te save-as` 写入磁盘之前运行 BPA 闸门检查。可通过 `--skip-bpa` 或 `--force` 在单次调用中跳过。                                                                                                                                                                                       |
| `bpa.builtInRules`           | `true`  | 每次运行关卡检查时，都包含精选的内置 BPA 规则集。若为 `false`，该门禁仅运行 `bpa.rules` 中的规则以及嵌入模型中的规则。                                                                                                                                                                                      |
| `bpa.disabledBuiltInRuleIds` | `null`  | 要从门禁中排除的各个内置规则的 ID。可使用 `te bpa rules disable <id>` 和 `te bpa rules enable <id>` 来切换。                                                                                                                                                                          |
| `vertipaqOnRefresh`          | `false` | 成功刷新后（`full`、`dataonly`、`automatic` 或 `add`），会运行 VertiPaq 分析，并显示已刷新表的存储统计信息。                                                                                                                                                                                  |
| `interactiveEditMode`        | `stage` | 在 `te interactive` 中对内存中变更的默认处理方式。 `stage` 会将更改保留在内存中，直到你运行 `save`。 `save` 会在每个变更命令后写回源；对于远程源，每次 `set` 都是一次 XMLA 写入。 `revert` 会在每个命令后丢弃更改，除非你传递 `--save` 或 `--stage`。每个命令上的 `--save` / `--revert` / `--stage` 标志会覆盖此设置。                                       |
| `launchInteractiveMode`      | `auto`  | 控制在终端中不带任何参数运行 `te` 时，是否启动交互式 REPL。 `auto`（默认）仅在 stdin、stdout 和 stderr 都连接到 TTY 时才会启动 REPL，从而让脚本和 CI 流水线按常规方式解析。 `always` 即使有重定向也会启动 REPL。 `never` 则改为显示帮助。全局 `--non-interactive` 标志会在单次调用中强制使用 `never`，而 `TE_INTERACTIVE` 环境变量可为单次调用设置该模式。                   |
| `disableTelemetry`           | `false` | 选择不参与匿名使用遥测数据收集。遥测数据包含命令名称、退出代码和耗时。其中不包含模型内容、路径或查询文本。                                                                                                                                                                                                         |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### 格式选项

CLI 内置的 DAX 格式化程序可离线使用。

- 布局键 `shortFormat` 和 `skipSpaceAfterFunction` 会在 `autoFormat` 重新格式化已修改的表达式时，以及在 `te query` 呈现查询文本时生效。
- `te set <path> --format <Property>` 和 `te util format-dax` 会忽略这些布局键，并接受 `--long` 和 `--no-space-after-function` 标志。
- 由配置驱动的格式化始终使用逗号作为列表分隔符。如果 DAX 使用分号编写，就用 `te util format-dax` 的 `--semicolons` 标志。
- `formatOptions.useSqlBiDaxFormatter` 会将显式格式化和 `te query` 的渲染交由 SQL BI 的 [daxformatter.com](https://www.daxformatter.com) Web 服务处理，该服务需要联网。 `autoFormat` 始终使用内置格式化程序。

| 键                                      | 默认值     | 说明                                                                                                                               |
| -------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `formatOptions.shortFormat`            | `false` | 尽可能使用简短的单行格式。                                                                                                                    |
| `formatOptions.skipSpaceAfterFunction` | `false` | 省略函数名称与左括号之间的空格，例如 `SUM(x)`。                                                                                                     |
| `formatOptions.useSqlBiDaxFormatter`   | `false` | 通过 [SQL BI daxformatter.com](https://www.daxformatter.com) Web 服务格式化 DAX。需要联网。内置格式化程序与 Tabular Editor 3 的默认格式一致。 |

### 显示

这些设置控制终端输出和诊断日志记录。

| 键                   | 默认值     | 说明                                |
| ------------------- | ------- | --------------------------------- |
| `hidePreviewNotice` | `false` | 隐藏黄色预览横幅。**距离到期不足 14 天时，将忽略此设置。** |
| `spinner`           | `true`  | 在终端中显示动画进度指示器。在 CI 环境中禁用。         |
| `debug`             | `false` | 始终启用调试日志（等同于传入 `--debug`）。        |

### 配置文件

已保存的连接配置文件存放在 `profiles` 键下。使用 `te profile set`、`te profile remove` 和 `te profile list` 管理它们，不要直接编辑该文件。见 @te-cli-auth。

配置文件在启用期间可以覆盖以下行为的默认设置：`autoFormat`、`validateOnMutation`、`mutationOutput`、`bpa.onMutation`、`bpa.onDeploy`、`bpa.onSave`、`vertipaqOnRefresh`、`spinner` 和 `interactiveEditMode`。例如，dev 配置文件可以关闭验证和部署闸门检查，而 prod 配置文件可以格式化 DAX：

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

`te profile set` 提供了 `--auto-format`、`--validate-on-mutation`、`--bpa-on-mutation`、`--bpa-on-deploy`、`--vertipaq-on-refresh` 和 `--spinner` 等标志位。每项都接受 `true`、`false` 或 `null`，其中 `null` 会清除覆盖。

## BPA 闸门

如果模型存在严重级别为 `error` 的规则违规项，BPA 闸门会阻止保存或部署。它会在执行以下命令时运行：

- `te deploy` 会触发闸门检查，除非传入 `--skip-bpa` 或 `bpa.onDeploy` 为 `false`。
- `te save-as` 会运行闸门检查，除非传入 `--skip-bpa`（或 `--force`），或 `bpa.onSave` 为 `false`。
- `te add`、`te set`、`te move`、`te remove`、`te macro run` 仅在 `bpa.onMutation` 为 `true` 时才会执行 gate 检查。

闸门检查会从 `bpa.rules` 加载 BPA 规则，并且默认还会加载内置规则集（由 `bpa.builtInRules` 控制）。 `te bpa rules disable <id>` 会将指定内置规则添加到 `bpa.disabledBuiltInRuleIds`，从而将其排除；`te bpa rules enable <id>` 则会将其从列表中移除。

如果闸门检查发现严重性为 `error` 或更高的违规项，命令将以退出代码 `1` 失败，并输出违规摘要。要继续，可以使用以下任一选项：

- `--fix-bpa` - 在内存中将规则的 `fixExpression` 应用于部署/保存产物；不会修改源文件。
- `--skip-bpa` - 仅对本次命令禁用闸门检查。
- `--bpa-rules <path>` - 可重复指定；仅在本次调用 `te deploy` 或 `te save-as` 时覆盖 `bpa.rules`。除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。

要在不部署的情况下根据规则检查模型，运行 `te bpa run`：

```bash
te bpa run --model ./model --fail-on error
te bpa run --model ./model --fix --save     # Apply fixes to the source
```

### 内置 BPA 规则

CLI 包含一组内置 BPA 规则。内置规则是只读的：`te bpa rules set` 和 `te bpa rules remove` 对内置 ID 执行时会失败，并提示改用 `te bpa rules disable`。要更改内置规则，把它以新 ID 复制到你的规则文件中，然后禁用该内置规则。

`bpa.builtInRules` 和 `bpa.disabledBuiltInRuleIds` 同时适用于闸门检查和 `te bpa run`，因此通过 `te bpa rules disable` 禁用的规则会在所有场景中被排除。

## 变更后行为

执行会产生变更的命令（`te add`、`te set`、`te move` 或 `te macro run`）后，CLI 会运行以下检查：

1. **TOM 错误** 始终会显示。如果度量值、列、分区或计算项中包含无效的 DAX 或 M，命令将失败。
2. **架构验证** (`validateOnMutation`，默认值为 `true`) 会验证 DAX 中的 `Table[Column]` 引用是否仍可解析。
3. **DAX 自动格式化** (`autoFormat`，默认值为 `false`) 会使用内置格式化程序对本次变更涉及的表达式进行格式化。
4. **变更时运行 BPA** (`bpa.onMutation`，默认值为 `false`) 会在变更后运行 BPA，并根据 `--fail-on` 发出警告或使命令失败。

`te config set <key> false` 可关闭某项检查。配置文件可以为某个环境覆盖该键。

## 管理员策略

在 Windows 上，`te` 遵循与 Tabular Editor 3 相同的管理员策略，并从以下注册表项读取这些策略：

- `Software\\Policies\\Tabular Editor ApS`，用于 CLI 和桌面应用程序共享的值
- 其 `TECLI` 子键，用于仅适用于 CLI 的值
- 其 `TE3` 子键，用于仅适用于桌面应用程序的值
- 较早的 `Software\\Policies\\Kapacity\\Tabular Editor` 键，仍会生效

计算机范围的值 (`HKEY_LOCAL_MACHINE`) 优先于按用户设置的值 (`HKEY_CURRENT_USER`)。在同一注册表配置单元中，产品特定值优先于共享值。当某项策略禁用某个功能时，命令会指出该策略名称，不执行任何操作，并以失败状态退出，从而导致任何依赖该功能的管道步骤失败。

| 策略                     | 对 CLI 的影响                                                                                                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DisableCSharpScripts` | 阻止 `te script` 和 `te bpa run --fix` 的自动修复。                                                                                                                                                          |
| `DisableMacros`        | 阻止所有 `te macro` 宏命令。                                                                                                                                                                                |
| `DisableBpaDownload`   | 阻止通过 URL 提供的 Best Practice Analyzer 规则。磁盘上的规则文件和内置规则不受影响。                                                                                                                                           |
| `DisableTelemetry`     | 无论配置中的 `disableTelemetry` 如何设置，都会关闭匿名使用情况统计。                                                                                                                                                        |
| `BlockUnsafeScripts`   | 当代码访问文件、网络、进程或外部程序集时，阻止 `te script`、`te macro run` 和 `te bpa run --fix`。有关被阻止的 API，请参阅 [哪些情况算作保持在模型范围内](xref:csharp-scripts#what-counts-as-staying-within-the-model)。 JSON 输出会报告 `blockedByPolicy`。 |

用于更新检查、错误Report、DAX优化器、DAX 组件管理器、AI 助手和 MCP 服务器的策略不会影响 CLI。完整的策略列表及部署方式见 @policies。

在桌面应用程序中，`BlockUnsafeScripts` 需要 Tabular Editor 3 企业版。 CLI 没有版本之分，因此只要设置了该策略就会应用。

## 环境变量

CLI 会读取以下环境变量，用于路径、行为和诊断。有关 Azure 身份验证变量（`AZURE_CLIENT_ID`、`AZURE_TENANT_ID`、`AZURE_CLIENT_CERTIFICATE_PATH` 等），见 @te-cli-auth。

| 变量               | 用途                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `TE_CONFIG`      | 替代配置文件的路径。用于 `te config list`、`set`、`init` 和 `paths`。                                                                                |
| `TE_MACROS_PATH` | 覆盖宏文件路径，在[解析顺序](#path-resolution-priority)中位列第二。由 `te macro` 命令读取。                                                                   |
| `TE_BPA_RULES`   | 覆盖 `te bpa run` 和 `te bpa rules` 子命令使用的 BPA 规则文件/URL 列表。                                                                             |
| `TE_BPA_CONFIG`  | 覆盖 deploy/save 门禁读取的 BPA 门禁配置 (`.te-bpa.json`) 的路径。                                                               |
| `TE_DEBUG`       | 设为 `1` 可全局启用调试日志（等同于 `--debug` 或配置中的 `debug: true`）。                                                                                 |
| `NO_SPINNER`     | 设为 `1` 或 `true` 可禁用动画进度指示器（可替代配置中的 `spinner: false`）。                                                                                |
| `CI`             | 自动检测。当设为 `1` 或 `true` 时，CLI 会禁用动画进度指示器，并切换为纯文本输出。大多数 CI 运行器都会设置这个变量。                                                                 |
| `TE_SESSION`     | 覆盖用于活动连接状态的按终端划分的会话 ID。设置这个变量后，就能在同一个 shell 中运行彼此隔离的 CLI 会话，例如在并行 CI 矩阵作业中。使用 [`te session`](xref:te-cli-commands#session) 查看并管理会话。  |
| `TE_INTERACTIVE` | 为单次调用临时覆盖 `launchInteractiveMode` 设置。可设为 `auto`、`always` 或 `never`。 `TE_INTERACTIVE=always` 会启动 REPL，而 `TE_INTERACTIVE=never` 会显示帮助。 |
| `TE_COMPAT`      | 设为 `te2` 可强制启用 TE2 兼容模式；参见 @te-cli-migrate。                                                                             |

## 后续步骤

- @te-cli-auth - 配置文件、身份验证和凭据存储。
- @te-cli-commands - `te config` 子命令。
- @te-cli-cicd - 为管道配置 BPA 门禁。
