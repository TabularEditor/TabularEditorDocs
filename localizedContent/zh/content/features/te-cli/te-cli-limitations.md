---
uid: te-cli-limitations
title: 已知限制
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

# 已知限制

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

本页列出了 Tabular Editor CLI（`te`）的已知限制，帮助你提前规划并避开常见陷阱。 本页会随每次发布而更新；如果你发现此处未列出的问题，请在公开的 [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repository 中提交 issue。

> [!NOTE]
> 这些限制按领域分类。 每个条目都会说明具体限制，并在适用时提供变通方法或推荐的 CLI 友好替代方案。

## 脚本

CLI 会针对你在 Tabular Editor 2 和 3 中使用的同一个 `Model` 对象运行 C# Script（`te script`），但它是无界面的控制台宿主程序。 任何依赖 Windows Forms UI、TOM Explorer 的选择内容，或实时的 UI 端服务（宏注册表、在线 DAX Formatter、实时 VertiPaq分析器）的功能，其行为都会不同——通常表现为空、无操作，或直接报错。

| 限制                                                                          | 说明 / 变通方法                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **未加载 `System.Windows.Forms`**                                              | CLI 使用的是跨平台 `TOMWrapper` 版本，其中剥离了所有与 WinForms 耦合的代码；WinForms 程序集不会被加载到 AppDomain 中。 引用 `System.Windows.Forms` 类型（`MessageBox`、`Form`、文件选择器、自定义对话框等）的脚本 将无法编译。 将所有 UI 交互重构为通过环境变量或 stdin 提供输入。                               |
| **`Selected.<Plural>` 返回空的可枚举对象**                                           | 在 CLI 中，`Selected.Tables`、`Selected.Measures`、`Selected.Columns`、`Selected.Hierarchies` 等的枚举结果都为空——不会出现编译或运行时错误，只是不会返回任何项。 改用显式查找：`Model.AllMeasures.Where(...)`、`Model.Tables["Sales"].Measures`；或通过环境变量或 stdin 将对象路径传入脚本。 |
| **`Selected.<Singular>` 会在运行时抛出错误**                                         | `Selected.Table`、`Selected.Measure`、`Selected.Column`、`Selected.Hierarchy` 等都会报错，因为它们要求恰好选中一个该类型的对象，而 CLI 中的选择始终为空。 直接引用该对象，例如 `Model.Tables["Sales"]`。                                                                     |
| **`Selected.ActivePerspectives` 和 `Selected.ActiveCulture`**：分别为活动透视和活动区域设置 | 它们分别始终返回空集合和 `null`。 如果需要，就在脚本中显式设置透视或区域设置。                                                                                                                                                                                 |
| **`Select<Object>` 对话框会抛出 `NotSupportedException`**                         | `SelectTable`、`SelectColumn`、`SelectMeasure`、`SelectObject`、`SelectObjects`（以及所有重载）都会返回以下错误：_"对象选择对话框… 在 CLI 脚本中不可用。 在编写脚本前，先按名称或路径预先选定对象。_ 通过环境变量、配置或查询模型，提前解析目标。                                                          |
| **`Info` / `Warning` / `Error` / `Output` 会写入控制台**                          | 这些仍然可用，但会输出到 stdout/stderr，而不是打开对话框。 它们不会阻塞，也不会提供“忽略后续弹窗”的提示。 可安全用于 CI。                                                                                                                                                     |
| **`ShowPrompt(...)` 始终返回 `Cancel`**                                         | 无法进行交互式确认。 通过环境变量或配置预先确定答案。                                                                                                                                                                                                 |
| **`SuspendWaitForm` / `WaitFormVisible` 都是空操作**                             | “请稍候”加载指示器是 TE3 的一个 UI 元素。 `WaitFormVisible` 是一个可设置的标志位，但没有任何 Visual 效果；`SuspendWaitForm` 会被静默忽略——现有脚本仍可继续编译。                                                                                                               |
| **`host.Macro(...)` / `CustomAction(...)` 会抛出错误**                           | CLI 不会加载 `%APPDATA%/TabularEditor3/MacroActions.json`，因此在脚本内部调用宏会报错。 把宏逻辑直接写进脚本里，或直接调用该宏底层的脚本文件。                                                                                                                            |
| **`table.GetCardinality()` / `column.GetTotalSize()` 返回 0**                 | CLI 主机中没有实时 VPA，因此脚本内的 VertiPaq 基数辅助函数无法使用。 如果要查看 VPA 统计信息，显式加载 VPAX 并使用 `host.Vpa.*`，或运行 [`te vertipaq`](xref:te-cli-commands#vertipaq)。                                                                                   |

## Best Practice Analyzer

| 限制                                           | 说明 / 变通方法                                                                                                                                                                                                                                                               |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **BPA 规则源必须是 HTTPS URL 或本地文件路径**             | 只接受 `https://` URL 和不带协议的本地文件路径。 系统能识别 `http://`，但会在加载时故意拒绝，并给出清晰的错误信息——BPA 规则是可执行的规则表达式，通过未经过身份验证的通道获取会有被篡改的风险。 其他 URL 方案（`file://`、`ftp://`、…） 不受支持。 这既适用于 `te bpa run --rules`，也适用于通过 [`te config set`](xref:te-cli-commands#config-list--paths--init--set) 配置的规则列表。 |
| **规则 URL 的验证在运行阶段进行，而不是在 `te config set` 时** | 像 `http://` 这样的拼写错误会被 `te config set` 接受，只有在 BPA 实际运行时才会暴露出来。 编辑已配置的规则源后，运行一次 `te bpa run`（或 `te validate`），以验证每个 URL 都能成功加载。                                                                                                                                           |
| **`--rules` 不会禁用内置规则**                       | 当传入 `te bpa run --rules <path-or-url>` 时，本次运行将使用提供的规则覆盖 [`bpa.rules`](xref:te-cli-commands#config-list--paths--init--set) 和 `TE_BPA_RULES` 中的条目，但仍会同时加载内置默认规则。 若只想运行显式指定的规则文件，还需传入 `--no-defaults`。                                                                     |
| **没有可在单次调用中跳过 `bpa.rules` 配置的标志**            | 配置了 `bpa.rules` 后，每次执行 `te bpa run` 都会在加载内置规则的同时加载这些规则。 目前没有可在单次运行中跳过已配置规则文件的标志。 变通方法：显式传入 `--rules <path-or-url>`——该标志会在本次调用中完全替换 `bpa.rules` 和 `TE_BPA_RULES`。                                                                                                        |

## 验证

| 限制                                       | 说明 / 变通方法                                                                                                                                        |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`te validate` 无法自动修复 Code Action 违规项** | `te validate` 会生成 Report 来指出 Code Action 违规项，但不提供用于应用建议修复的 CLI 参数。 在 Tabular Editor 3 中应用修复；或者对与 BPA 规则重叠的那部分 Code Action，使用 `te bpa run --fix`。 |

## 模型 I/O

| 限制                                          | 说明 / 变通方法                                                                                                                                                                                          |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`--serialization` 不能将序列化格式与 PBIP 容器组合使用** | 在 [`te save`](xref:te-cli-commands#save) 中，`--serialization` 选项会将 `bim`、`tmdl`、`Database.json` 和 `pbip` 视为互斥，因此目前无法将采用 TMSL 序列化（`.bim`）的模型打包生成 PBIP 容器。 将 TMDL 保存到 PBIP 中，或将 `.bim` 保存在 PBIP 容器之外。 |

## 身份验证

| 限制                   | 说明 / 变通方法                                                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **每种身份验证方法只能缓存一个身份** | CLI 同时只会缓存一个 UPN（交互式）身份和一个 SPN（服务主体）身份。 在同一种身份验证方法下切换到其他用户或租户时，需要先执行 `te auth logout`，再重新执行 `te auth login`，这会使之前的缓存失效。 |

## 命令行输入

| 限制                                | 说明 / 变通方法                                                                                                                                                                                                        |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **包含空格的 DAX 对象路径必须用 shell 引号括起来** | 当表名或列名包含空格时，必须在终端中用 shell 引号将整个 DAX 对象引用括起来：`te get "'My Table'[My Column]"`。 如果没有外层引号，shell 会将该路径拆分为多个参数，导致解析失败。 在 [`te interactive`](xref:te-cli-interactive) 中不需要 shell 引号，因为 REPL 会在 shell 将输入拆分为参数之前接收原始输入。 |

## TE2 功能对等性

| 限制                          | 说明 / 变通方法                                                                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **`te schemacheck` 目前尚未实现** | TE2 的 `-SC` / `-SCHEMACHECK` 标志目前在 `te` 中还没有对应项；针对源数据源的架构漂移检测计划在未来版本中推出。 有关完整的 TE2 到 `te` 的标志映射表，请参见 @te-cli-migrate。 |

## Report 缺失的限制

如果某个行为让你感到意外，而且这里没有列出，请到 [TabularEditor/CLI](https://github.com/TabularEditor/CLI/issues) 提交一个 Issue，并附上你运行的命令、实际看到的输出，以及你期望的输出。 经确认的限制会在下一个版本中补充到此页面。

## 相关页面

- @csharp-scripts - 完整的 C# Script 参考（UI 和 CLI）。
- @script-helper-methods - `ScriptHost` 辅助方法列表，以及这些方法在 CLI 中的行为。
- @te-cli-commands - 完整的 CLI 命令参考。
- @te-cli-automation - 在脚本和流水线中使用 CLI 的模式与最佳实践。
