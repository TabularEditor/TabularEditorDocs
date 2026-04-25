---
uid: index
title: Tabular Editor
author: Daniel Otykier
updated: 2021-09-09
---

# Tabular Editor

Tabular Editor 是一款工具，可让你在 Analysis Services 表格和 Power BI 语义模型中轻松操作和管理度量值、计算列、显示文件夹、透视和翻译。

该工具提供两种不同的版本：

- Tabular Editor 2.x（免费，[MIT 许可证](https://github.com/TabularEditor/TabularEditor/blob/master/LICENSE)）- [GitHub 项目主页](https://github.com/TabularEditor/TabularEditor)
- Tabular Editor 3.x（商业版）- [主页](https://tabulareditor.com)

## 文档

本网站包含两个版本的文档。 请在屏幕顶部的导航栏中选择你的版本，以查看对应产品的专属文档。

## 如何在 TE3 和 TE2 之间做选择

Tabular Editor 3 是 Tabular Editor 2 的演进版本。 它专为那些在 Tabular 数据建模与开发中寻求“一款工具搞定一切”解决方案的用户而设计。

### [Tabular Editor 3](#tab/TE3)

Tabular Editor 3 是一款更高级的应用，提供高端体验和众多便捷功能，可将你的数据建模与开发需求整合到一款工具中。

![Tabular Editor 3](assets/images/te3.png)

**Tabular Editor 3 主要功能：**

- 高度可自定义、直观的 UI
- 支持高 DPI、多显示器和主题（是的，支持深色模式！）
- 一流的 [DAX 编辑器](xref:dax-editor)，提供语法高亮、语义检查、自动补全、上下文感知等功能，远不止这些
- 表浏览器、Pivot Grid 浏览器和 DAX 查询编辑器
- [导入表向导](xref:importing-tables)，支持 Power Query 数据源
- [数据刷新视图](xref:data-refresh-view) 和 [高级刷新对话框](xref:advanced-refresh)，用于在后台将刷新操作排队并执行
- 关系图编辑器，轻松可视化并编辑表关系
- [DAX脚本](xref:dax-scripts) 功能，可在一个文档中编辑多个对象的 DAX 表达式
- 提供辅助功能、代码操作和命名空间支持的 [DAX 用户自定义函数 (UDFs)](xref:udfs)
- 用于创建和管理日期表，并增强时间智能能力的 [日历编辑器](xref:calendars)
- 用于安装和管理 DAX 组件的 [DAX 组件管理器](xref:dax-package-manager)
- [内置的 Best Practice Analyzer 规则](xref:built-in-bpa-rules)
- VertiPaq分析器与 [DAX优化器](xref:dax-optimizer-integration) 的集成
- [DAX调试器](xref:dax-debugger)
- 用于快速修复和重构的 [代码操作](xref:code-actions)
- [元数据翻译编辑器](xref:metadata-translation-editor) 和 [透视编辑器](xref:perspective-editor)
- 用于 Fabric Git 集成的 [连同支持文件一起保存](xref:save-with-supporting-files)
- [本地化支持](xref:references-application-language)（中文、西班牙语、日语、德语、法语）

### [Tabular Editor 2.x](#tab/TE2)

Tabular Editor 2.x 是一款轻量级应用程序，可快速修改 Analysis Services 或 Power BI 数据模型的 TOM（Tabular Object Model）。 该工具最初于 2016 年发布，并会定期更新和修复缺陷。

![Tabular Editor 2.x](assets/images/te2.png)

**Tabular Editor 2.x 主要功能：**

- 一款非常轻量的应用，界面简单直观，可用于浏览 TOM
- DAX 依赖关系视图，以及用于在 DAX 对象之间导航的键盘快捷键
- 支持编辑模型透视和元数据翻译
- 批量重命名
- 通过搜索框快速定位大型且复杂的模型
- Deployment Wizard
- 最佳实践分析器
- 使用类 C# 脚本进行高级脚本编写，用于自动化重复任务
- 命令行界面（可用于将 Tabular Editor 集成到 DevOps 流水线中）

***

### 功能概览

下表列出了两款工具的所有主要功能。

|                                                                                | TE2（免费）                                                 | TE3（商业版）                                                  |
| ------------------------------------------------------------------------------ | ------------------------------------------------------- | --------------------------------------------------------- |
| 编辑所有 TOM 对象和属性                                                                 | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 批量编辑和重命名                                                                       | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 支持复制粘贴和拖放                                                                      | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 撤销/重做数据建模操作                                                                    | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 从磁盘加载/保存模型元数据                                                                  | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| 保存到文件夹                                                                         | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| [daxformatter.com](https://daxformatter.com) 集成                | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 高级数据建模（OLS、透视、计算组、元数据翻译等）                                                      | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| 语法高亮和公式自动修正                                                                    | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 查看对象之间的 DAX 依赖关系                                                               | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 导入表向导                                                                          | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Deployment Wizard                                                              | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| 最佳实践分析器 (BPA)                                               | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| C# 脚本和自动化                                                                      | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 用作 Power BI Desktop 的外部工具                                                      | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 连接到 SSAS/Azure AS/Power BI Premium                                             | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| 命令行界面                                                                          | <span class="emoji">&#10004;</span> |                                                           |
| 高级且可自定义的用户界面，支持高 DPI、多显示器及主题                                                   |                                                         | <span class="emoji">&#10004;</span>   |
| 一流的 DAX 编辑器，具备类似 IntelliSense<sup>TM</sup> 的功能，支持离线格式化等                        |                                                         | <span class="emoji">&#10004;</span>   |
| 离线 DAX 语法检查与列/数据类型推断                                                           |                                                         | <span class="emoji">&#10004;</span>   |
| 改进的表导入向导与表架构更新检查，并支持 Power Query                                               |                                                         | <span class="emoji">&#10004;</span>   |
| DAX 查询、表格预览和 Pivot Grid                                                        |                                                         | <span class="emoji">&#10004;</span>   |
| 创建图表，用于可视化和编辑表关系                                                               |                                                         | <span class="emoji">&#10004;</span>   |
| 在后台执行数据刷新操作                                                                    |                                                         | <span class="emoji">&#10004;</span>\* |
| C# 宏录制器                                                                        |                                                         | <span class="emoji">&#10004;</span>   |
| 使用 [DAX脚本](xref:dax-scripts) 在同一文档中编辑多个 DAX 表达式                                |                                                         | <span class="emoji">&#10004;</span>   |
| [VertiPaq分析器](https://www.sqlbi.com/tools/vertipaq-analyzer/) 集成               |                                                         | <span class="emoji">&#10004;</span>   |
| [DAX调试器](xref:dax-debugger)                                                    |                                                         | <span class="emoji">&#10004;</span>   |
| [元数据翻译编辑器](xref:metadata-translation-editor)                                   |                                                         | <span class="emoji">&#10004;</span>   |
| [透视编辑器](xref:perspective-editor)                                               |                                                         | <span class="emoji">&#10004;</span>   |
| [表格组](xref:table-groups)                                                       |                                                         | <span class="emoji">&#10004;</span>   |
| [DAX优化器集成](xref:dax-optimizer-integration)                                     |                                                         | <span class="emoji">&#10004;</span>   |
| [代码操作](xref:code-actions)                                                      |                                                         | <span class="emoji">&#10004;</span>   |
| [DAX 用户自定义函数 (UDFs)](xref:udfs) 辅助功能、代码操作和命名空间              |                                                         | <span class="emoji">&#10004;</span>   |
| 用于增强时间智能的[日历编辑器](xref:calendars)                                               |                                                         | <span class="emoji">&#10004;</span>   |
| [DAX 组件管理器](xref:dax-package-manager)                                          |                                                         | <span class="emoji">&#10004;</span>   |
| [内置的 Best Practice Analyzer 规则](xref:built-in-bpa-rules)                       |                                                         | <span class="emoji">&#10004;</span>   |
| 支持[刷新覆盖配置文件](xref:refresh-overrides)的[高级刷新对话框](xref:advanced-refresh)（商业版/企业版） |                                                         | <span class="emoji">&#10004;</span>\* |
| [为 Fabric 保存并包含支持文件](xref:save-with-supporting-files)                          |                                                         | <span class="emoji">&#10004;</span>   |
| Databricks Metric Views 的语义桥接（企业版）                                             |                                                         | <span class="emoji">&#10004;</span>\* |
| [本地化支持](xref:references-application-language)（中文、西班牙语、日语、德语、法语）                |                                                         | <span class="emoji">&#10004;</span>   |

\***注意：** 具体限制取决于你使用的 Tabular Editor 3 [版本](xref:editions)。

### 常见功能

在可用的数据建模选项方面，两款工具提供的功能相同：它们通过直观且响应迅速的用户界面，基本上公开了 [Tabular Object Model](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 的所有对象和属性。 你可以编辑标准工具中无法设置的高级对象属性。 这些工具可以从文件或任何 Analysis Services 实例中加载模型元数据。 更改只会在你按下 Ctrl+S（保存）时才会同步，从而带来一种“离线”编辑体验；大多数人认为这比标准工具的“始终同步”模式更好。 在处理大型且复杂的数据模型时，这一点尤为明显。

此外，两款工具都支持批量修改模型元数据、批量重命名对象、复制/粘贴对象，以及在表和显示文件夹之间拖放对象等。 这些工具甚至支持撤消/重做。

两款工具都提供 Best Practice Analyzer，它会持续扫描模型元数据，并按你自行定义的规则进行检查，例如强制特定的命名规范、确保非维度属性列始终隐藏等。

你还可以在两款工具中编写并执行 C# 风格的脚本，用于自动化重复性任务，例如生成时间智能度量值，以及根据列名自动检测关系。

最后，得益于“Save-to-folder”功能——一种会将模型中的每个对象保存为独立文件的新文件格式——你可以实现并行开发并集成版本控制；这仅靠标准工具很难做到。

## 结论

如果你刚开始接触表格建模，我们建议你先使用标准工具，等你熟悉计算表格、度量值、关系、DAX 等概念后再进一步尝试。 到那时，不妨试用一下 Tabular Editor 2.x，看看它能让你完成某些任务快上多少。 如果你喜欢，并且还想要更多功能，可以考虑 Tabular Editor 3.x！

## 后续步骤

- [开始使用 Tabular Editor 2](xref:getting-started-te2)
- [开始使用 Tabular Editor 3](xref:getting-started)
- [Tabular Editor 3 路线图](xref:roadmap)

