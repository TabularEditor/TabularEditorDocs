---
uid: migrate-from-te2
title: 从 Tabular Editor 2.x 迁移
author: Daniel Otykier
updated: 2026-06-10
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 从 Tabular Editor 2.x 迁移

本文面向已具备一定经验、使用 Tabular Editor 2.x 进行 Power BI Dataset 或 Analysis Services Tabular 开发的开发者。 本文重点介绍 Tabular Editor 3 的相似之处与关键新增功能，帮助你快速上手。

## 并行安装

Tabular Editor 3 的产品代码与 Tabular Editor 2.x 不同。 这意味着你可以将两个工具并排安装，而不会有问题。 实际上，这两个工具会安装到不同的程序文件夹中，它们的设置也分别存放在不同的文件夹里。 换句话说，Tabular Editor 2.x 与 Tabular Editor 3 之间并不适用“升级”或“降级”的说法。 你可以把 Tabular Editor 3 当作一款完全不同的产品。

## 功能对比

从功能角度来看，除少数例外，Tabular Editor 3 基本上是 Tabular Editor 2.x 的超集。 下表对比了两款工具的所有主要功能：

[!include[feature-comparison](../includes/feature-comparison.partial.md)]

## 功能差异

以下总结了主要的功能差异。

### 用户界面

启动 Tabular Editor 3 时，你首先会注意到全新的、类似 Visual Studio Shell 的界面。 这个界面完全可自定义，支持高 DPI、多显示器，还能更换主题。 所有界面元素都可以拖动到不同位置。因此，如果你更喜欢 Tabular Editor 2.x 的界面布局，可以直接在 **Window** 菜单中选择 **Classic layout**。

不过总体而言，Tabular Editor 2.x 中已有的界面元素在 Tabular Editor 3 里名称保持一致，因此你应该能比较轻松地上手新界面。 下面列出了一些重要差异：

- Tabular Editor 2.x 中的 **Advanced Scripting** 选项卡已不再提供。 在 Tabular Editor 3 中，你需要通过 **File > New** 菜单创建 **C# Script**。 你不再局限于一次只能处理一个脚本。 此外，**Custom actions** 已更名为 **宏**。
- TOM Explorer 目前不支持 **Dynamic LINQ filtering**。 如果你想使用 [Dynamic LINQ](https://dynamic-linq.net/expression-language) 查找对象，需要按 CTRL+F 打开 **Find and replace** 对话框。
- 如果你关闭了 **表达式编辑器**，可以在 **TOM Explorer** 中双击某个对象的图标将其重新打开，或选择 **View > Expression Editor** 菜单项。
- 在 Tabular Editor 3 的默认布局中，**Best Practice Analyzer** 会作为一个选项卡显示在 **TOM Explorer** 旁边。 在这里，你还会看到全新的 **数据刷新** 视图（用于查看后台刷新操作队列）以及 **宏** 视图（用于管理此前从 C# Script 保存的宏）。
- Tabular Editor 3 会在全新的 **信息视图** 中显示所有 DAX 语法和语义错误。 在默认布局中，它位于界面左下角。
- 此外，Tabular Editor 3 还包含 **VertiPaq分析器**（你可能在 [DAX Studio](https://daxstudio.org/) 里见过它）。
- 最后补充一点：Tabular Editor 3 引入了 **文档** 的概念，这是一个统称，用来指代 C# Script、DAX脚本、DAX 查询、图示、数据预览和 Pivot Grid。

想了解更多信息，可以看看 <xref:user-interface>。

### 新的 DAX 编辑器与语义功能

Tabular Editor 3 拥有自己的 DAX 解析引擎（又称“语义分析器”），这意味着该工具现在能够理解模型中任何 DAX 代码的语义。 这个引擎也用来驱动我们的 DAX 编辑器（代号“Daxscilla”），并支持语法高亮、自动格式化、代码补全、参数提示、重构等更多功能。 当然，编辑器也高度可配置，你可以根据自己偏好的 DAX 编码风格进行调整。

想了解更多关于新 DAX 编辑器的内容，可以看看 <xref:dax-editor>。

此外，语义分析器会持续 Report 模型中所有对象的任何 DAX 语法或语义错误。 即使未连接到 Analysis Services，这也同样有效，而且速度快得惊人。 语义分析器还使 Tabular Editor 3 能够从 DAX 表达式中自动推断数据类型。 换句话说，Tabular Editor 3 会自动检测计算表格表达式将生成哪些列。 与 Tabular Editor 2.x 相比，这是一个很大的改进：在之前的版本中，你必须在计算表格上手动映射列，或依赖 Analysis Services 返回列元数据。

### 支持 Power Query 的表导入和架构更新

与 Tabular Editor 2.x 相比，Tabular Editor 3 的另一大优势是支持 Structured数据源以及 Power Query (M) 分区。 具体来说，“架构更新”功能现在适用于这些类型的数据源和分区，并且表导入向导在导入新表时可以生成所需的 M 代码。

架构比较对话框本身也有多项改进，例如允许你轻松将“列删除 + 列插入”操作映射为一次“列重命名”操作（反之亦然）。 此外还提供了选项，用于控制如何处理浮点和十进制数据类型（例如，有时你的数据源使用的是浮点数据类型，但你可能仍希望始终将其导入为十进制类型）。

要了解更多信息，请参阅 <xref:importing-tables>。

<a name="workspace-mode"></a>

### 工作区模式

Tabular Editor 3 引入了 **工作区模式** 的概念：模型元数据从磁盘（Model.bim 或 Database.json）加载后，会立即部署到你选择的 Analysis Services 实例中。 每当你点击“保存”（CTRL+S）时，Workspace 数据库都会同步，并将更新后的模型元数据保存回磁盘。 这种方式的优势在于，Tabular Editor 会连接到 Analysis Services，从而启用下面列出的[已连接功能](#connected-features)，同时也便于更新磁盘上的源文件。 在 Tabular Editor 2.x 中，你必须从数据库打开模型，然后还得记得隔一段时间手动保存到磁盘。

这种方式非常适合实现[并行开发](xref:parallel-development)，并将模型元数据集成到版本控制系统中。

要了解更多信息，请参阅 <xref:workspace-mode>。

<a name="connected-features"></a>

### 已连接功能

Tabular Editor 3 包含多项新的已连接功能，让你可以将其用作 Analysis Services 的客户端工具。 这些功能会在 Tabular Editor 3 连接到 Analysis Services 时启用——不管是直接连接，还是使用[工作区模式](#workspace-mode)功能。

新的已连接功能包括：

- 表数据预览
- PivotGrids
- DAX 查询
- 数据刷新操作
- VertiPaq分析器

### 模型关系图

Tabular Editor 2.x 中一个呼声很高的需求是：能够更好地可视化表之间的关系。 使用 Tabular Editor 3，你现在可以创建模型关系图。 每个图表都是一个简单的 JSON 文件，用于保存要包含在图表中的表名称及其坐标。 随后，Tabular Editor 3 会呈现这些表和关系，并提供便于编辑关系、基于现有关系向图表添加更多表等功能。

![轻松添加相关表](~/content/assets/images/diagram-menu.png)

更多信息请参阅[使用图表](xref:importing-tables-data-modeling#working-with-diagrams)。

### C# Script 与宏录制器

Tabular Editor 2.x 的 **Advanced Scripting** 功能在 Tabular Editor 3 中延续为 **C# Script**。 Tabular Editor 3 的一个重要差异是，你不再局限于只能使用单个脚本。 相反，使用 **文件 > 新建 > C# Script** 选项，你可以按需创建并使用任意数量的 C# Script。 与 Tabular Editor 2.x 类似，这些脚本可以保存为可复用的操作，并直接集成到 TOM Explorer 的右键上下文菜单中。 在 Tabular Editor 3 中，我们将这些操作称为 **宏**，你甚至可以创建自己的菜单和工具栏，并在其中添加宏。

更重要的是，Tabular Editor 3 提供了 **宏录制器**，可根据用户操作自动生成 C# 代码。

要了解更多信息，请参阅 @cs-scripts-and-macros。

### DAX脚本

如果你是从 Tabular Editor 2.x 迁移过来，需要了解的最后一个重要功能是 **DAX脚本**。 借助此功能，你可以创建文档，一次性编辑多个计算对象的 DAX 表达式和基本属性。 计算对象包括度量值、计算列、计算表格等。

当你需要在多个对象之间编写复杂的业务逻辑时，这会非常方便。 在 TOM Explorer 中（多）选中对象后，右键并选择 **Script DAX** 选项，即可生成一个新的 DAX脚本，其中包含所有已选对象的定义。 当然，DAX脚本编辑器具备与表达式编辑器和 DAX 查询编辑器相同的全部 DAX 能力。

在 **连接** 或 **Workspace** 模式下，DAX脚本是一项非常强大的工具，可用于快速修改并测试更新后的业务逻辑。例如，如下图所示，你可以将其与 Pivot Grid 配合使用。 只需按下 SHIFT+F5，就会根据脚本中的 DAX 表达式更新数据库，随后 Pivot Grid 会立即刷新。

![Dax 脚本与 Pivot](~/content/assets/images/dax-scripting-and-pivot.png)

要了解更多信息，请参阅 @dax-script-introduction。

## 自 2021 年以来的主要新增功能

自本文首次撰写以来，Tabular Editor 3 已新增许多功能。 上方的功能对比表是权威清单。 对于从 Tabular Editor 2.x 迁移过来的开发人员，最值得关注的亮点包括：

- 提供编写辅助、代码操作和命名空间支持的 [DAX 用户自定义函数 (UDFs)](xref:udfs)
- 用于构建具备增强时间智能功能的日期表的 [日历编辑器](xref:calendars)
- 用于安装和共享可重用 DAX 组件的 [DAX 组件管理器](xref:dax-package-manager)
- 用于在 DAX 编辑器中执行快速修复和重构的 [代码操作](xref:code-actions)
- 用于逐步调试表达式求值过程的 [DAX调试器](xref:dax-debugger)
- 可与 VertiPaq分析器配合使用的 [DAX优化器集成](xref:dax-optimizer-integration)
- 用于组织大型模型的 [表格组](xref:table-groups)
- 用于提供 DAX 和建模帮助的 [AI 助手](xref:ai-assistant)
- 支持 Fabric Git 集成的 [TMDL](xref:tmdl) 序列化、[保存到文件夹](xref:save-to-folder) 和 [连同支持文件一起保存](xref:save-with-supporting-files)
- 用于自动化和 CI/CD 的跨平台 [Tabular Editor CLI](xref:te-cli)（`te`，目前为有限公开预览版）
- 用于 Databricks Metric Views 的 [语义桥接](xref:semantic-bridge)（企业版）
- 应用程序界面的 [本地化](xref:references-application-language)

## 后续步骤

- @migrate-from-vs
- @te-cli-migrate
- @parallel-development
- @boosting-productivity-te3
