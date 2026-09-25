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

本文面向已具备一定经验、使用 Tabular Editor 2.x 进行 Power BI Dataset 或 Analysis Services Tabular 开发的开发者。 The article highlights similarities and important feature additions of Tabular Editor 3, to get you quickly up to speed.

## 并行安装

Tabular Editor 3 的产品代码与 Tabular Editor 2.x 不同。 This means that you can install both tools side-by-side without issues. In fact, the tools are installed into separate program folders and their settings are also kept in separate folders. In other words, the term "upgrade" or "downgrade" between Tabular Editor 2.x and Tabular Editor 3 does not apply. It is better to think of Tabular Editor 3 as an entirely different product.

## 功能对比

从功能角度来看，除少数例外，Tabular Editor 3 基本上是 Tabular Editor 2.x 的超集。 The table below compares all major features of the two tools:

[!include[feature-comparison](../includes/feature-comparison.partial.md)]

## 功能差异

以下总结了主要的功能差异。

### 用户界面

启动 Tabular Editor 3 时，你首先会注意到全新的、类似 Visual Studio Shell 的界面。 This interface is fully customizable, supports high-DPI, multiple monitors and even allows you to change the theming. All interface elements can be moved to different locations, so if you prefer the interface layout of Tabular Editor 2.x, immediately choose **Classic layout** from the **Window** menu.

不过总体而言，Tabular Editor 2.x 中已有的界面元素在 Tabular Editor 3 里名称保持一致，因此你应该能比较轻松地上手新界面。 A few important differences are listed below:

- The **Advanced Scripting** tab in Tabular Editor 2.x is gone. In Tabular Editor 3, you instead create **C# Scripts** using the **File > New** menu. You are not limited to working on a single script at a time. In addition, **Custom actions** have been renamed to **Macros**.
- TOM Explorer 目前不支持 **Dynamic LINQ filtering**。 Instead, if you want to find objects using [Dynamic LINQ](https://dynamic-linq.net/expression-language) you have to bring up the **Find and replace** dialog by pressing CTRL+F.
- 如果你关闭了 **表达式编辑器**，可以在 **TOM Explorer** 中双击某个对象的图标将其重新打开，或选择 **View > Expression Editor** 菜单项。
- When using the default layout in Tabular Editor 3, the **Best Practice Analyzer** will be located as a tab next to the **TOM Explorer**. Here, you will also find the new **Data Refresh** view (which lets you view the queue of background refresh operations) and the **Macros** view (which lets you manage any macros that were previously saved from C# scripts).
- Tabular Editor 3 会在全新的 **信息视图** 中显示所有 DAX 语法和语义错误。 In the default layout, this is located at the bottom left of the interface.
- 此外，Tabular Editor 3 还包含 **VertiPaq分析器**（你可能在 [DAX Studio](https://daxstudio.org/) 里见过它）。
- 最后补充一点：Tabular Editor 3 引入了 **文档** 的概念，这是一个统称，用来指代 C# Script、DAX脚本、DAX 查询、图示、数据预览和 Pivot Grid。

想了解更多信息，可以看看 <xref:user-interface>。

### 新的 DAX 编辑器与语义功能

Tabular Editor 3 拥有自己的 DAX 解析引擎（又称“语义分析器”），这意味着该工具现在能够理解模型中任何 DAX 代码的语义。 This engine is also used to power our DAX editor (codename "Daxscilla"), to enable features such as syntax highlighting, automatic formatting, code completion, calltips, refactoring and much more. Of course the editor is highly configurable, allowing you to tweak it to match your preferred DAX coding style.

想了解更多关于新 DAX 编辑器的内容，可以看看 <xref:dax-editor>。

此外，语义分析器会持续 Report 模型中所有对象的任何 DAX 语法或语义错误。 This works even if not connected to Analysis Services and is lightning fast. The semantic analyzer also enabled Tabular Editor 3 to automatically infer data types from DAX expressions. In other words, Tabular Editor 3 automatically detects which columns would result from a calculated table expression. This is a big improvement over Tabular Editor 2.x, where you would have to manually map columns on a calculated table, or rely on Analysis Services to return the column metadata.

### 支持 Power Query 的表导入和架构更新

与 Tabular Editor 2.x 相比，Tabular Editor 3 的另一大优势是支持 Structured数据源以及 Power Query (M) 分区。 Specifically, the "Schema Update" feature now works for these types of data sources and partitions, and the Table Import Wizard can generate the necessary M code when importing new tables.

架构比较对话框本身也有多项改进，例如允许你轻松将“列删除 + 列插入”操作映射为一次“列重命名”操作（反之亦然）。 There are also options for controlling how floating and decimal data types should be treated (for example, sometimes your data source may be using a floating point data type, but you may still want to import it always as a decimal type).

要了解更多信息，请参阅 <xref:importing-tables>。

### 工作区模式

Tabular Editor 3 引入了 **工作区模式** 的概念：模型元数据从磁盘（Model.bim 或 Database.json）加载后，会立即部署到你选择的 Analysis Services 实例中。 Whenever you hit Save (CTRL+S), the workspace database is synchronized and updated model metadata is saved back to the disk. The advantage of this approach, is that Tabular Editor is connected to Analysis Services, thus enabling the [connected features](#connected-features) listed below, while also making it easy to update the source files on disk. With Tabular Editor 2.x, you had to open a model from a database, and then remember to manually save to disk once in a while.

这种方式非常适合实现[并行开发](xref:parallel-development)，并将模型元数据集成到版本控制系统中。

要了解更多信息，请参阅 <xref:workspace-mode>。

### 已连接功能

Tabular Editor 3 包含多项新的已连接功能，让你可以将其用作 Analysis Services 的客户端工具。 These features are enabled whenever Tabular Editor 3 is connected to Analysis Services, either directly or when using the [workspace mode](#workspace-mode) feature.

新的已连接功能包括：

- 表数据预览
- PivotGrids
- DAX 查询
- 数据刷新操作
- VertiPaq分析器

### Diagrams

One highly requested feature of Tabular Editor 2.x, was the ability to better visualize relationships between tables. 使用 Tabular Editor 3，你现在可以创建模型关系图。 Each diagram is a simple JSON file that holds the names and coordinates of tables to be included in the diagram. Tabular Editor 3 then renders the tables and relationships and provides features for easily editing relationships, adding additional tables to the diagram based on existing relationships, etc.

![轻松添加相关表](~/content/assets/images/diagram-menu.png)

更多信息请参阅[使用图表](xref:importing-tables-data-modeling#working-with-diagrams)。

### C# Script 与宏录制器

Tabular Editor 2.x 的 **Advanced Scripting** 功能在 Tabular Editor 3 中延续为 **C# Script**。 One important difference in Tabular Editor 3 is that you are no longer limited to working with a single script. Instead, using the **File > New > C# Script** option, you can create and work with as many C# scripts as you need. Similar to Tabular Editor 2.x, these scripts can be saved as reusable actions that are integrated directly into the right-click context menu of the TOM Explorer. In Tabular Editor 3, we call these actions **Macros**, and you can even create your own menus and toolbars to which you can add macros.

更重要的是，Tabular Editor 3 提供了 **宏录制器**，可根据用户操作自动生成 C# 代码。

要了解更多信息，请参阅 @cs-scripts-and-macros。

### DAX脚本

The last important feature you need to know about, when coming from Tabular Editor 2.x, is **DAX Scripting**. With this feature, you can create documents that allow you to edit the DAX expression and basic properties of several calculated objects at once. Calculated objects are measures, calculated columns, calculated tables, etc.

This is very convenient when authoring complex business logic across several objects. By (multi)selecting objects in the TOM Explorer, right-clicking and choosing the **Script DAX** option, you get a new DAX script containing the definitions of all selected objects. The DAX script editor of course has all of the same DAX capabilities of the Expression Editor and the DAX query editor.

在 **连接** 或 **Workspace** 模式下，DAX脚本是一项非常强大的工具，可用于快速修改并测试更新后的业务逻辑。例如，如下图所示，你可以将其与 Pivot Grid 配合使用。 Simply hitting SHIFT+F5 causes the database to be updated based on the DAX expressions in the script, after which the Pivot Grid will immediately update.

![Dax 脚本与 Pivot](~/content/assets/images/dax-scripting-and-pivot.png)

要了解更多信息，请参阅 @dax-script-introduction。

## Major additions since 2021

Tabular Editor 3 has gained many features since this article was first written. The feature comparison table above is the canonical catalog. The highlights most relevant to developers coming from Tabular Editor 2.x are:

- [DAX User-Defined Functions (UDFs)](xref:udfs) with authoring assistance, code actions and namespaces
- [Calendar Editor](xref:calendars) for building date tables with enhanced time intelligence
- [DAX Package Manager](xref:dax-package-manager) for installing and sharing reusable DAX
- [Code Actions](xref:code-actions) for quick fixes and refactoring in the DAX editor
- [DAX debugger](xref:dax-debugger) for stepping through expression evaluation
- [DAX Optimizer integration](xref:dax-optimizer-integration) alongside VertiPaq Analyzer
- [Table Groups](xref:table-groups) for organizing large models
- [AI Assistant](xref:ai-assistant) for DAX and modeling help
- [TMDL](xref:tmdl) serialization, [Save to folder](xref:save-to-folder) and [Save with supporting files](xref:save-with-supporting-files) for Fabric Git integration
- Cross-platform [Tabular Editor CLI](xref:te-cli) (`te`, in Limited Public Preview) for automation and CI/CD
- [Semantic Bridge](xref:semantic-bridge) for Databricks Metric Views (Enterprise Edition)
- [Localization](xref:references-application-language) of the application interface

## 后续步骤

- @migrate-from-vs
- @te-cli-migrate
- @并行开发
- @boosting-productivity-te3
