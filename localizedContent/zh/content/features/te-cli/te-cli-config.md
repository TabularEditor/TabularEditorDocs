---
uid: te-cli-config
title: 自定义配置
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

# 自定义配置

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI 可从 JSON 文件读取可选配置。 配置控制三类内容：

- **File paths** - where the CLI reads macros, BPA rules, and (optionally) the TE3 Desktop executable, and where to write the query log.
- **Behavioral defaults** - BPA gates, auto-format, validation.
- **Saved connection profiles** - the list of named profiles you can switch between.

CLI 是自包含的 - 它不会从任何 Tabular Editor 3 桌面版安装路径读取或写入任何内容。 BPA 规则和宏文件必须通过此配置显式设置（或按需使用 `te bpa rules init` / `te macro init` 进行初始化）。

Most users don't need to edit the config file directly - `te config list`, `te config set <key> <value>`, and `te profile set` cover the common operations.

## 配置文件位置

将按以下顺序检查这些位置：

1. `$TE_CONFIG` 环境变量（如果已设置且文件存在）。
2. `~/.config/te/config.json`（在 Windows 上为 `%USERPROFILE%\.config\te\config.json`）。
3. 如果没有配置文件，CLI 将使用内置默认值。

`TE_CONFIG` is honored consistently by every config-file operation - `te config list`, `te config set`, `te config init`, and `te config paths` all read and write at the resolved path. 这主要用于测试、脚本化安装以及按环境进行配置。

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

使用 `te config paths` 查看 CLI 实际会为宏和 BPA 规则使用哪些文件。 这在调试缺失的数据文件时很有用。 输出会显示两行：`macros` (解析后的宏文件路径或 `[not set]`) 和 `bpa.rules` (由路径解析器解析出的第一个存在的 BPA 规则文件，或 `[not set]`)。

> [!NOTE]
> 在 `--output-format json` 模式下，`te config paths` 会显式输出值为 `null` 的字段 (例如 `{"macros": null, "bpa": {"rules": null}}`)。 报告解析结果本来就是此命令的全部用途，因此 `null` 表示“尝试过，但未解析到任何内容”，这是一个有意义的结果。 `te config list --output-format json` strips null fields by default, so consumers should parse it tolerantly.

## 设置值

```bash
te config set autoFormat true
te config set bpa.onDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
```

如果键未知，命令将以退出码 `1` 失败，并返回一条列出有效键的错误信息。

如果配置文件不存在，`te config set` 会先在解析后的路径自动创建一个配置文件 (若设置了则为 `$TE_CONFIG`，否则为 `~/.config/te/config.json`)，然后再应用更改。

> [!NOTE]
> 架构中的每个键都可以通过 `te config set` 设置，包括通过点分路径设置嵌套键 (`bpa.onDeploy`、`formatOptions.useSqlBiDaxFormatter` 等)。 唯一的例外是 `formatVersion`，它由 CLI 自动管理。 如果你更愿意直接编辑 JSON，可运行 `te config paths` 来找到配置文件。

## 完整 Schema

完整的 JSON 配置 Schema，包含所有键及其默认值。 直接编辑配置文件时可将其作为参考，或在为 `te config set` 调用查找点分路径时使用。

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

### 文件路径

在配置中设置这些路径，以避免每次执行命令都传入相同的路径。 每个命令的标志和环境变量都会覆盖配置值；请参阅下方的[路径解析优先级](#path-resolution-priority)。

| 键            | 含义                                                                                                                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `macros`     | 宏 JSON 文件的显式路径 (通常为 `MacroActions.json`)。 每个 `te macro` 命令都会解析它。 可将其指向共享文件（网络共享、仓库内文件，甚至 TE3 Desktop 的文件），以便在不同计算机之间以及在 CLI 与 TE3 Desktop 之间复用同一组宏。                |
| `bpa.rules`  | 指向 BPA 规则文件的路径或 URL 的有序列表。 `te bpa run` 和 deploy/save gate 会加载**所有**现有条目；`te bpa rules list` 和 `te config paths` 使用第一个现有条目。 在 `te config set bpa.rules ...` 中使用逗号分隔的值时，会将其拆分为数组。      |
| `te3ExePath` | Tabular Editor 3 Desktop 可执行文件 (`TabularEditor.exe`) 的显式路径。 **仅** `te open` 在启动桌面应用时才会用到；在 Linux/macOS 上，或不使用 `te open` 时，可安全留空。 如果未设置，`te open` 会回退到在 `PATH` 中查找。 |
| `queryLog`   | 日志文件路径，每次调用 `te query` 时都会将其查询文本和执行元数据追加到该文件中。 可用于审计追踪，或分析随时间变化的查询模式。 支持使用 `~` 表示主目录（例如 `~/.config/te/queries.log`）。                                                                  |

### 路径解析优先级

对于每个用户提供的文件 (宏、BPA 规则)，CLI 会按以下顺序解析路径：

1. **命令行标志** - 宏命令使用 `--macros <path>`；部署/保存 gate 使用 `--bpa-rules <path>`；`te bpa rules` 子命令使用 `--rules-file <path>`。
2. **环境变量**：宏使用 `TE_MACROS_PATH`，BPA 规则使用 `TE_BPA_RULES`。
3. **CLI 配置**：宏使用 `macros`，BPA 规则使用 `bpa.rules[]` 中第一个现有条目。

CLI 不会自动检测 TE3 的任何安装位置——请显式配置这些项。 若要从当前工作目录中的默认文件开始，可运行 `te macro init`（创建 `./MacroActions.json`）或 `te bpa rules init`（创建 `./BPARules.json`）。

运行 `te config paths` 可查看 CLI 实际解析到的是哪个文件。

### 行为默认值

所有与 BPA 相关的设置都位于 `bpa` 对象下，并可在 `te config set` 中使用点号分隔的键进行设置。

| 键名                           | 默认值     | 说明                                                                                                                                                                                                                                      |
| ---------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `autoFormat`                 | `false` | Run the DAX Formatter on modified expressions after `te add` / `te set` / `te move` / `te macro run`. 默认使用内置格式化程序；可通过 `formatOptions.useSqlBiDaxFormatter` 改用 SQL BI Web 服务。                                            |
| `validateOnMutation`         | `true`  | 在执行更改命令（`add`、`set`、`mv`、`replace --save`、`macro run`）后，检查模型中的每个 `Table[Column]` 引用是否仍可解析。 可在部署前捕获因重命名或删除而引入的悬空引用。                                                                                                                      |
| `bpa.onMutation`             | `false` | 在每次更改命令（`set`、`add`、`mv`、`rm`、`macro run`）后，运行一次限定范围的 BPA 分析。 只检查受影响表中的对象，而不是整个模型——这对于迭代编辑时获得快速反馈很有用。                                                                                                                                   |
| `bpa.onDeploy`               | `true`  | 在执行 `te deploy` 之前运行 BPA 关卡检查。 The deploy is aborted if any rule fires at severity >= error. 可通过 `--skip-bpa` 在单次调用中跳过，或通过 `--fix-bpa` 自动修复。                                                                            |
| `bpa.onSave`                 | `true`  | 在 `te save -o` 写入磁盘之前运行 BPA 关卡检查。 可通过 `--skip-bpa` 或 `--force` 在单次调用中跳过。                                                                                                                                                                |
| `bpa.builtInRules`           | `true`  | 每次运行关卡检查时，都包含精选的内置 BPA 规则集。 设为 `false` 可完全忽略内置规则；此时关卡检查只运行通过 `bpa.rules` 配置的规则以及嵌入模型中的规则。                                                                                                                                               |
| `bpa.disabledBuiltInRuleIds` | `null`  | 要从门禁中排除的各个内置规则的 ID。 可通过 `te bpa rules disable <id>` / `te bpa rules enable <id>` 修改——优先使用这些命令，而不是直接编辑该数组。                                                                                                                               |
| `vertipaqOnRefresh`          | `false` | 成功刷新后（`full`、`dataonly`、`automatic` 或 `add`），自动运行 VertiPaq 分析，以显示已刷新表的存储统计信息。 有助于立即发现意外的基数变化或内存回归。                                                                                                                                      |
| `interactiveEditMode`        | `stage` | 在 `te interactive` 中对内存中变更的默认处理方式。 `stage` 会将变更保留在内存中，直到调用 `save`（最安全）；`save` 会在每次产生变更的命令后写回源（对远程源请谨慎使用——每次 `set` 都会触发一次 XMLA 写入）；`revert` 会在每条命令后丢弃变更，除非传入了 `--save` 或 `--stage`。 每个命令上的 `--save` / `--revert` / `--stage` 标志始终会覆盖此设置。 |
| `disableTelemetry`           | `false` | 选择不参与匿名使用遥测数据收集。 CLI 会收集粗粒度的命令使用数据（命令名称、退出代码、持续时间），用于确定功能优先级。 CLI 绝不会收集模型内容、PATH 或查询文本。                                                                                                                                                 |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### 格式选项

每当 CLI 调用 DAX 格式化程序时都会应用（用于 `te format`，以及在启用 `autoFormat` 时对变更进行格式化）。 CLI 附带一个可完全离线工作的自研格式化器；如果你需要那种风格，或希望在启用 "Use daxformatter.com..." 时与 TE2 或 TE3 的行为一致，可通过 `formatOptions.useSqlBiDaxFormatter` 选择使用 SQL BI 的 [daxformatter.com](https://www.daxformatter.com) Web 服务。

| 键                                      | 默认值     | 说明                                                                                                                                                                   |
| -------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `formatOptions.useSemicolons`          | `false` | 使用 `;` 作为列表分隔符（欧洲/欧盟区域设置惯例）。 默认的 `,` 与 en-US 区域设置一致。                                                                                                                 |
| `formatOptions.shortFormat`            | `false` | 尽可能优先使用简短的单行格式，而不是默认的多行布局。                                                                                                                                           |
| `formatOptions.skipSpaceAfterFunction` | `false` | 省略函数名称与左括号之间的空格（例如使用 `SUM(x)`，而不是 `SUM (x)`）。                                                                                                                        |
| `formatOptions.useSqlBiDaxFormatter`   | `false` | 通过 [SQL BI daxformatter.com](https://www.daxformatter.com) Web 服务格式化 DAX，而不是使用内部格式化程序。 需要联网。 内置格式化器（默认）可离线使用，其效果与 Tabular Editor 3 Desktop 的默认格式化一致。 |

### 显示

控制 CLI 终端输出和诊断详细程度的设置。

| 键                   | 默认值     | 说明                                 |
| ------------------- | ------- | ---------------------------------- |
| `hidePreviewNotice` | `false` | 隐藏黄色预览横幅。 **距离到期不足 14 天时，将忽略此设置。** |
| `spinner`           | `true`  | 在终端中显示动画进度指示器。 在 CI 环境中禁用。         |
| `debug`             | `false` | 始终启用调试日志（等同于传入 `--debug`）。         |

### 配置文件

已保存的连接配置文件存放在 `profiles` 键下。 不要手动编辑——请使用 `te profile set / remove / list`。 配置文件管理见 @te-cli-auth。

配置文件可以包含 **覆盖项**，在配置文件处于启用状态时，用来覆盖上述默认行为。 这样一来，开发配置文件可以放宽验证和 BPA，而生产配置文件则保持严格：

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

## BPA 闸门

BPA 闸门是一道安全防线，用于防止存在规则违规的模型被保存或部署。 执行以下命令时，它会自动运行：

- `te deploy` 会触发闸门检查，除非传入 `--skip-bpa` 或 `bpa.onDeploy` 为 `false`。
- `te save` 会触发闸门检查，除非传入 `--skip-bpa`（或 `--force`）或 `bpa.onSave` 为 `false`。
- `te add`, `te set`, `te move`, `te macro run` run the gate only when `bpa.onMutation` is `true`.

闸门检查会从 `bpa.rules` 加载 BPA 规则，并且默认还会加载内置规则集（由 `bpa.builtInRules` 控制）。 可通过 `bpa.disabledBuiltInRuleIds` 单独排除内置规则——可使用 `te bpa rules disable <id>` / `te bpa rules enable <id>` 管理。

When the gate fires and finds violations at severity >= `error`, the command fails with exit code `1` and a summary of the violations. 处理选项：

- `--fix-bpa` - 在内存中将规则的 `fixExpression` 应用于部署/保存产物；不会修改源文件。
- `--skip-bpa` - 仅对本次命令禁用闸门检查。
- `--bpa-rules <path>` - 可重复指定；仅在本次调用 `te deploy` 或 `te save` 时覆盖 `bpa.rules`。 除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。

可单独运行 `te bpa run`，在不部署的情况下预览闸门检查的行为：

```bash
te bpa run ./model --fail-on error
te bpa run ./model --fix --save     # Apply fixes to the source
```

### 内置 BPA 规则

CLI 随附一套权威的内置 BPA 规则集，并以 JSON 资源的形式嵌入其中。 Built-in rules are read-only - `te bpa rules set` and `te bpa rules remove` refuse to mutate built-in IDs and point users at `te bpa rules disable` instead. 如果想自定义内置规则的行为，可以把它复制到本地规则文件中，作为一个使用不同 ID 的新规则，然后再禁用内置规则。

`bpa.builtInRules` 和 `bpa.disabledBuiltInRuleIds` 会一致地应用于部署/保存/变更的门控检查 **以及** 手动执行的 `te bpa run` 命令——通过 `te bpa rules disable` 禁用一次后，该规则将在所有场景中被排除。

## 变更后行为

When you run a mutating command (`te add`, `te set`, `te move`, `te replace --save`, `te macro run`), the CLI performs these checks automatically:

1. **TOM 错误**始终会被提示。 度量值、列、分区或计算项中的无效 DAX 或 M 始终会导致命令失败。
2. **架构验证** (`validateOnMutation`，默认值为 `true`) 会验证 DAX 中的 `Table[Column]` 引用是否仍可解析，并交叉检查元数据一致性。
3. **DAX 自动格式化** (`autoFormat`，默认值为 `false`) 在启用时会通过内置的 DAX Formatter 格式化此次变更涉及的所有表达式。
4. **变更时运行 BPA** (`bpa.onMutation`，默认值为 `false`) 在启用时会在变更后运行 BPA，并根据 `--fail-on` 发出警告或使命令失败。

可使用 `te config set <key> false` 禁用某项检查，或通过配置文件将放宽范围限定到特定环境。

## 环境变量

使用以下 CLI 专用环境变量来设置路径、行为和诊断。 有关 Azure 身份验证变量（`AZURE_CLIENT_ID`、`AZURE_TENANT_ID`、`AZURE_CLIENT_CERTIFICATE_PATH` 等），见 @te-cli-auth。

| 变量               | 用途                                                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `TE_CONFIG`      | 替代配置文件的路径。 所有 `te config` 操作（`show`、`set`、`init`、`paths`）都会遵循该变量的设置。                                                            |
| `TE_MACROS_PATH` | 覆盖宏文件路径（在解析顺序中排第二，见上文）。 由 `te macro` 命令读取。                                                                                      |
| `TE_BPA_RULES`   | 覆盖 `te bpa run` 和 `te bpa rules` 子命令使用的 BPA 规则文件/URL 列表。                                                                        |
| `TE_BPA_CONFIG`  | 覆盖 deploy/save 门禁读取的 BPA 门禁配置 (`.te-bpa.json`) 的路径。                                                          |
| `TE3_EXE_PATH`   | Tabular Editor 3 桌面版二进制文件的路径。 此项 **仅** 用于 `te open`；在 Linux/macOS 上或不使用 `te open` 时，可安全留空。 会回退到 `PATH` 查找。                      |
| `TE_DEBUG`       | 设为 `1` 可全局启用调试日志（等同于 `--debug` 或配置中的 `debug: true`）。                                                                            |
| `NO_SPINNER`     | 设为 `1` 或 `true` 可禁用动画进度指示器（可替代配置中的 `spinner: false`）。                                                                           |
| `CI`             | 自动检测。 当设为 `1` 或 `true` 时，CLI 会禁用动画进度指示器，并切换为纯文本输出。 大多数 CI 运行器都会自动设置此项。                                                          |
| `TE_SESSION`     | 覆盖用于活动连接状态的按终端划分的会话 ID。 适用于在同一个 shell 中运行多个相互隔离的 CLI 会话，例如并行的 CI 矩阵作业。 使用 [`te session`](xref:te-cli-commands#session) 查看并管理会话。 |
| `TE_COMPAT`      | 设为 `te2` 可强制启用 TE2 兼容模式；参见 @te-cli-migrate。                                                                        |

## 相关页面

- @te-cli-auth - 配置文件、身份验证和凭据存储。
- @te-cli-commands - `te config` 子命令。
- @te-cli-cicd - 为管道配置 BPA 门禁。
