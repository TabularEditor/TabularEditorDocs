---
uid: user-interface
title: 基本用户界面
author: Daniel Otykier
updated: 2026-09-14
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

# 了解 Tabular Editor 3 的用户界面

本文介绍 Tabular Editor 3 的用户界面。

## 基本用户界面元素

首次启动 Tabular Editor 3 并加载语义模型时，你将看到如下截图所示的界面。

![基本用户界面](~/content/assets/images/basic-ui.png)

1. **标题栏**：显示当前加载的文件名；如果已连接，还会显示 Analysis Services 数据库或 Power BI 数据集的名称。
2. **菜单栏**：菜单栏用于访问 Tabular Editor 3 的各项功能。 See [Menus](#menus) for a detailed walkthrough of all menu items.
3. **工具栏**：工具栏提供对最常用功能的快速访问。 All features accessible through the toolbar can also be accessed through the menus. You may customize the toolbars and their buttons under **Tools > Customize...**
4. **TOM Explorer 视图**：以层级结构展示您的数据模型，所有对象均可用 .  这些对象来自表示您的数据模型的 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 元数据。 The toggle buttons at the top allow you to filter which objects are displayed. The search box allows you to filter objects by names.
5. **Expression Editor**: The expression editor provides a quick way to edit any DAX, SQL or M expressions of the currently selected object in the TOM Explorer. If you close the expression editor, you can bring it back up by double-clicking on an object in the TOM Explorer. The dropdown at the top allows you to switch between different expression properties, in case the currently selected object has more than one such property (for example, KPIs have Target Expressions, Status Expressions and Trend Expressions, which are 3 different DAX expressions belonging to the same KPI object).
6. **属性视图**：显示 TOM Explorer 中当前选定对象（一个或多个）的所有可用 TOM 属性的详细信息。 Most properties can be edited through the grid, even when multiple objects are selected. Some properties (such as "Format String", "Connection String", "Role Members") have popup dialogs or collection editors that can be brought up by clicking on the ellipsis button within the property value cell.
7. **信息视图**：Tabular Editor 3 会持续分析你模型中的 DAX 表达式，查找语义错误。 Any such errors are outputted here. In addition, messages shown in this view, can originate from C# scripts or from error messages reported by Analysis Services.
8. **状态栏**：状态栏会提供与当前选择相关的各种上下文信息、Best Practice Analyzer 的检测结果等。 When the [MCP server](xref:mcp-server) is available, an indicator at the right-hand end reads **MCP Started** or **MCP Stopped**, with the address the server is listening on in its tooltip. Click it to open the MCP Server dialog, or right-click it to start and stop the server, copy a registration configuration for your agent or jump to the preferences page.

There are a number of additional views available, serving various purposes. More information in the [View menu](#view) section.

# 自定义用户界面

All UI elements may be resized and/or rearranged to fit your needs. You can even drag individual views out of the main view, thus splitting up an instance of Tabular Editor 3 across multiple monitors. Tabular Editor 3 will save the customization when the application is closed, and reload it automatically upon next launch.

### 选择不同的布局

To reset the application to the default layout, choose the **Window > Default layout** option. Tabular Editor 2.x 用户可能更喜欢 **窗口 > 经典布局** 选项：TOM Explorer 位于屏幕左侧，属性视图位于表达式编辑器下方。

Use the **Window > Capture Layout** option to save a customized layout such that it will become available as a new layout option within the Window menu, allowing you to quickly switch back and forth between different layouts. Use the **Window > Layouts...** option to bring up a list of all available layouts, allowing you to apply, load, remove and save layouts. When saving a layout to disk, the result is an .xml file which you can share with other users of Tabular Editor 3.

![管理布局](~/content/assets/images/manage-layouts.png)

### 窗口停靠选项

When rearranging views and documents in Tabular Editor 3, you can choose to dock windows in different areas of the interface. When dragging a window to a new position, docking indicators will appear showing you the available docking locations.

![窗口停靠选项](~/content/assets/images/window-docking-options.png)

停靠窗口主要有两种方式，各有不同用途：

**文档选项卡停靠（中心指示器）**：将窗口拖到中心停靠指示器时，它会被放置在主文档区域。 Windows docked this way become document tabs that:

- 可使用 **Ctrl+Tab** 在选项卡之间切换
- 会在主工作区与 DAX 查询、脚本和图表等其他文档并排显示
- 不支持自动隐藏

**工具窗口停靠（边缘指示器）**：将窗口拖到左侧、右侧、顶部或底部的停靠指示器时，它会作为工具窗口停靠。 Tool windows:

- 无法通过 **Ctrl+Tab** 访问
- 带有图钉图标，可用于启用自动隐藏（不使用时窗口会折叠）
- 其行为与 TOM Explorer 和信息视图等其他工具窗口类似
- 可停靠在主文档区域周围的不同位置

> [!TIP]
> 停靠窗口的大小取决于你选择停靠区域中的可用空间，而不是停靠选项本身。 You can resize windows by dragging the dividers between them.

### 更改主题和调色板

你可以通过选择不同的主题和/或调色板来更改 Tabular Editor 3 的外观。 Tabular Editor 3 ships with five different themes (sometimes called "skins"), available through the **Window > Theme** menu:

- Basic 与 Bezier（矢量主题，适用于高 DPI 显示器）
- Blue, Dark and Light (raster based, not recommended for high-DPI displays)

For the vector based themes (Basic and Bezier), use the **Window > Default palette** menu item to change the colors used by the theme.

![Palettes](~/content/assets/images/palettes.png)

# 菜单

以下部分将更详细地介绍 Tabular Editor 3 中的各个菜单。

在下文中，我们使用 **活动文档** 一词，指光标位于某个文档中，例如表达式编辑器或下方截图中的“DAX 脚本 1”选项卡。 Some keyboard shortcuts and menu items behave differently depending on whether there is an active document or not, and what type of document is active.

> [!NOTE]
> 默认情况下，菜单和工具栏会被锁定在原位，防止误操作导致重新定位。 To unlock them, go to **Tools > Customize... > 选项**，并取消选中 **锁定菜单和工具栏** 选项

![Active Document](~/content/assets/images/active-document.png)

## 文件

**文件** 菜单主要包含用于加载和保存模型元数据，以及相关支持文件和文档的菜单项。

![File Menu](~/content/assets/images/file-menu.png)

- **新建**：打开一个子菜单，可创建新的空白数据模型 (Ctrl+N)，或创建各种 [支持文件](xref:supported-files#supported-file-types)，例如新的 DAX 查询或 DAX 脚本（文本文件），或数据模型图表（JSON 文件）。 Supporting files (with the exception of C# scripts), can be created only when a model is already loaded in Tabular Editor.

  ![File Menu New](~/content/assets/images/file-menu-new.png)

> [!IMPORTANT]
> **新建 > 模型...** 选项在 Tabular Editor 3 桌面版中不可用，因为该版本只能作为 Power BI Desktop 的外部工具使用。[更多信息](xref:editions)。

- **打开**：打开一个子菜单，提供从多种来源加载数据模型的选项，以及一个用于加载任何其他类型文件的选项。 The submenu items are:

  ![File Menu Open](~/content/assets/images/file-menu-open.png)

  - **从文件加载模型...** 从 .bim 或 .pbit 等文件打开模型元数据。
  - **从 DB 加载模型...** 指定 Analysis Services 或 Power BI XMLA 连接详细信息，或连接到本地 Analysis Services 实例（例如 Visual Studio 的集成 Workspace 服务器或 Power BI Desktop），以便从已部署的表格模型加载模型元数据。
  - **从文件夹加载模型...** 从文件夹结构中打开模型元数据，该结构此前使用任意版本的 Tabular Editor 保存。
  - **文件...** 会显示一个对话框，可根据文件扩展名打开 Tabular Editor 3 支持的任意类型文件。 See [Supported file types](xref:supported-files) for more information.
  - **Import from Metric View YAML...** Imports model metadata from a Databricks Metric View YAML file.

    ![支持的文件类型](~/content/assets/images/supported-file-types.png)

> [!IMPORTANT]
> 在 Tabular Editor 3 桌面版中，**打开 > 从文件打开模型...** 和 **打开 > 从文件夹打开模型...** 选项不可用，并且 **打开 > 文件...** 对话框只允许打开[支持的文件](xref:supported-files#supported-file-types)，不允许打开包含元数据的文件。

- **Revert**: This option lets you reload the model metadata from the source, discarding any changes that are made in Tabular Editor, which have not yet been saved. This option is useful when Tabular Editor 3 is used as an External Tool for Power BI Desktop, and a change is made in Power BI Desktop while Tabular Editor 3 is connected. 选择 **还原** 后，Tabular Editor 3 无需重新连接即可从 Power BI Desktop 重新加载模型元数据。 If you loaded the model from a file or a folder you rarely need this command, because Tabular Editor reloads the model by itself when those files change on disk. See [Auto-reload from disk](xref:auto-reload).
- **Close Document** (Ctrl+W): Closes the currently active document or panel in the main area, such as a DAX Query, a C# script, a data model diagram, or any other view with focus. If the document has unsaved changes, Tabular Editor will prompt you to save the changes before closing. This command is context-aware and will close whichever item is currently active in the main workspace area.
- **关闭模型**：会从 Tabular Editor 中卸载当前加载的模型元数据。 If you made changes to the metadata, Tabular Editor will prompt you to save the changes before closing.
- **Save**: This saves the active document back to the source file. 如果当前没有活动文档，此操作会将模型元数据保存回源；源可以是 Model.bim 文件、Database.json（文件夹结构），也可以是已连接的 Analysis Services 实例（包括 Power BI Desktop）或 Power BI XMLA endpoint。
- **Save as...** This allows you to save the active document as a new file. 如果当前没有活动文档，此操作允许你将模型元数据另存为新文件，使用 .bim (基于 JSON) 文件。
- **保存到文件夹...**：允许你将模型元数据保存为[文件夹结构](xref:save-to-folder)。
- **全部保存**：一次性保存所有未保存的文档和模型元数据。
- **最近使用的文件**：显示最近使用的支持文件列表，便于你快速重新打开它们。
- **最近使用的表格模型**：显示最近使用的模型元数据文件或文件夹列表，便于你从其中之一快速重新加载模型元数据。

> [!IMPORTANT]
> 在 Tabular Editor 3 桌面版中，**保存到文件夹** 和 **最近使用的表格模型** 选项已禁用。 In addition, the **Save as** option is only enabled for [supporting files](xref:supported-files#supported-file-types).

- **退出**：关闭 Tabular Editor 3 应用程序。 You are prompted to save any unsaved files or model metadata before the application is shut down.

## 编辑

**编辑** 菜单包含标准的 Windows 应用程序菜单项，用于编辑文档或对当前加载的模型元数据进行更改。

![编辑菜单](~/content/assets/images/edit-menu.png)

- **Undo**: This option undoes the last change made to the model metadata. When there is no active document, the familiar CTRL+Z shortcut maps to this option.
- **Redo**: This option undoes the last undo against the model metadata. When there is no active document, the familiar CTRL+Y shortcut maps to this option.
- **Find**: Displays the "Find and replace" dialog with the "Find" tab selected. [更多信息](xref:find-replace#find)。
- **Replace**: Displays the "Find and replace" dialog with the "Replace" tab selected. [更多信息](xref:find-replace#replace)。
- **Cut / Copy / Paste**: These are the familiar Windows editing operations. If there is an active document, then these apply to the text selection within that document. Otherwise, these options may be used to manipulate objects in the TOM Explorer. For example, you can duplicate multiple measures by holding down the SHIFT or CTRL key while selecting the measures in the TOM Explorer, then hitting CTRL+C followed by CTRL+V.
- **删除**：删除活动文档中选定的文本；如果没有活动文档，则删除 TOM Explorer 中当前选定的一个或多个对象。

> [!NOTE]
> Tabular Editor 通常仅在选择了多个对象，或要删除的对象存在依赖关系时，才会弹出删除确认对话框。 Object deletion can be undone by using the **Undo** option (CTRL+Z).

- **全选**：选中当前活动文档中的所有文本，或选中 TOM Explorer 中属于同一父级的所有对象。
- **Code Assist**：此选项仅在编辑 DAX 代码时可用。 It provides a shortcut to various code assist features relevant for editing DAX code. See [DAX editor](xref:dax-editor#code-assist-features) for more information.
- **Word Wrap**: Toggles word wrapping in the currently active text document.

## 视图

The **View** menu lets you navigate between the different views of the Tabular Editor 3 UI. If a view has been hidden, click on the view title in this menu will unhide the view and bring it into focus. Note that documents are not shown in the View menu. To navigate between documents, use the [Window menu](#window).

![视图菜单](~/content/assets/images/view-menu.png)

- **TOM Explorer**: 以层次结构视图呈现当前加载的模型元数据的整个 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)。更多信息见 @tom-explorer-view。
- **AI Assistant**: The AI Assistant view lets you interact with an AI assistant that can help you with modeling tasks.
- **DAX Package Manager**: The DAX Package Manager view lets you browse and install DAX user-defined function packages into your model.
- **Best Practice Analyzer**: 通过让你指定用于最佳实践验证的规则，帮助提升模型质量。 See @bpa-view for more information.
- **信息**: 信息视图显示来自各种来源的错误、警告和信息性消息，例如 Tabular Editor 3 语义分析器。 See @messages-view for more information.
- **数据刷新**：数据刷新视图用于跟踪后台运行的数据刷新操作。 See @data-refresh-view for more information.
- **表达式编辑器**：这是一个“快速编辑器”，可让你编辑 TOM Explorer 中当前选定对象的 DAX、M 或 SQL 表达式。 See @dax-editor for more information.
- **宏**: 宏视图允许你管理你创建的任何宏。 Macros can be created from @csharp-scripts. See @creating-macros for more information.
- **VertiPaq分析器**：VertiPaq分析器视图允许你收集、导入和导出有关模型数据的详细统计信息，用于优化和调试 DAX 性能。 VertiPaq Analyzer is created and maintained by [Marco Russo](https://twitter.com/marcorus) of [SQLBI](https://sqlbi.com) under MIT license. More information on the [GitHub project page](https://github.com/sql-bi/VertiPaq-Analyzer).
- **Dependencies**: The [**DAX Dependencies** view](xref:creating-and-testing-dax#dax-dependencies) visualizes dependencies between the currently selected object and other objects in the model. Tick **Track TOM Explorer** to have it follow the tree selection.
- **DAX Optimizer**: The DAX Optimizer view integrates with [DAX Optimizer](https://www.daxoptimizer.com) to analyze your model for DAX performance issues.
- **Calendar Editor**: The Calendar Editor view lets you define and manage calendars in models using the modern time intelligence feature.
- **Perspective Editor**: The Perspective Editor view provides a matrix overview of which objects are included in each perspective of the model.
- **Metadata Translation Editor**: The Metadata Translation Editor view provides a grid for editing metadata translations (cultures) of model objects.
- **Toolbars / Properties**: The remaining items let you toggle the visibility of toolbars and bring up the Properties view (F4).

## 模型

**模型**菜单显示可在“模型”对象级别执行的操作（即 TOM Explorer 的根对象）。

![模型菜单](~/content/assets/images/model-menu.png)

- **Deploy...**: 启动 Tabular Editor 部署向导。 For more information, see [Model deployment](../deployment.md).

> [!IMPORTANT]
> **Deploy** 选项在 Tabular Editor 3 桌面版中不可用。 For more information see @editions.

- **Serialization options...** Lets you configure how model metadata is serialized when saving to disk (file or folder structure).
- **导入表...** 启动 Tabular Editor 3 导入表向导。 For more information, see @importing-tables.
- **Update schema (all tables)...** Detects schema changes in the data source(s) for all tables of the model compared to the currently imported columns. See [Updating table schema](xref:importing-tables#updating-table-schema) for more information.
- **Script DAX**: 为当前选定的对象生成 DAX 脚本(如果未选择任何对象，则为模型中的所有 DAX 对象生成 DAX 脚本)。 See @dax-scripts for more information.
- **刷新模型**: 当 Tabular Editor 连接到 Analysis Services 实例时，此子菜单包含用于在模型级别启动后台刷新操作的选项。 The submenu has the options below. For more information, see [Refresh command (TMSL)](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request).
  - **自动（模型）**：Analysis Services 将决定要刷新的对象（仅刷新不处于“Ready”状态的对象）。
  - **完全刷新（模型）**：Analysis Services 对模型执行完全刷新。
  - **计算（模型）**：Analysis Services 将对所有计算表格、计算列、计算组以及关系执行重新计算。 No data is read from the data sources.
- **Add [object type]**: The remaining shortcuts in the **Model** menu lets you create new types of model child objects (tables, data sources, perspectives, etc.).

## 工具

**工具** 菜单包含用于设置 Tabular Editor 3 偏好和自定义项的选项。

![视图菜单](~/content/assets/images/tools-menu.png)

- **自定义...** 启动 Tabular Editor 3 用户界面布局自定义对话框，可在其中创建新工具栏、重新排列并编辑菜单和工具栏按钮等。
- **偏好...** 启动 Tabular Editor 3 偏好对话框。它是管理 Tabular Editor 及其各项功能的中心入口，例如更新检查、代理设置、查询行数限制、请求超时等。 See @preferences for more information.
- **Manage BPA rules...** Launches the Best Practice Analyzer rule manager, which lets you view and edit the Best Practice Analyzer rules and rule collections. See @bpa-view for more information.
- **MCP Server...** Launches the MCP Server dialog, from which you start and stop the server that lets an external AI agent work on the model you have open, review the permissions it will be given and copy a registration configuration for your agent. See @mcp-server for more information. The item is hidden when the AI features component is not installed, when **Enable MCP Server** is unchecked, or where an administrator has disabled it by policy.

## 窗口

**窗口** 菜单提供用于管理和在应用程序的各种视图与文档之间导航的快捷方式（统称为 _窗口_）。 It also has menu items for controlling the theming and color palettes as described [above](#changing-themes-and-palettes).

![查看菜单](~/content/assets/images/window-menu.png)

- **新建...**：此子菜单提供用于创建新[支持文件](xref:supported-files#supported-file-types)的快捷方式。 The options here are identical to those under **File > New**.

- **浮动**：将当前视图或文档从停靠状态解除，并在浮动窗口中显示。

- **Pin tab** pins a tab. When a tab is pinned, it is shown at the left-most side of the document tabs, and when right-clicking on the tabs, shortcuts are available for closing only unpinned tabs.

  ![标签页上下文菜单](~/content/assets/images/tab-context-menu.png)

- **新建水平/垂直选项卡组**：此选项可将主文档区域划分为多个区域（即“选项卡组”），以便同时并排或上下显示多个文档。

- **Close All**: Closes all document tabs. You are prompted to save unsaved changes, if any.

- **重置窗口布局**：重置对主文档区域应用的所有自定义设置。

- **1..N [document]**: The first 10 open documents are listed here, allowing you to navigate between them. You can also use the CTLR+Tab shortcut to quickly switch between open documents and views, such as shown in the screenshot below:

  ![Ctrl+Tab 快捷键](~/content/assets/images/ctrl-tab.png)

- **窗口...**：打开一个对话框，列出所有已打开的文档，使你可以在它们之间切换或逐个关闭。

  ![窗口管理器](~/content/assets/images/windows-manager.png)

- **Capture Layout** / **Layouts...** / **Default layout** / **Classic layout**: These menu items were discussed [earlier in this article](#choosing-a-different-layout).

- **主题** / **默认调色板**：这些菜单项已在[本文前面](#changing-themes-and-palettes)讨论过。

- **Language**: Lets you change the display language of the Tabular Editor 3 user interface.

## 帮助

**帮助**菜单提供在线资源等内容的快捷入口。

![帮助菜单](~/content/assets/images/help-menu.png)

- **Online Documentation**: This menu item opens [docs.tabulareditor.com](https://docs.tabulareditor.com), this documentation site, in your default web browser.
- **Onboarding Guide**: This menu item opens the Tabular Editor 3 onboarding guide, which helps new users get started with the application.
- **社区支持**：此菜单项链接到我们的[公开社区支持站点](https://github.com/TabularEditor/TabularEditor3)。
- **专属支持**：此菜单项可让你直接向我们的专属支持热线发送电子邮件。
- **Get Started**: This menu item opens the **Get Started** page, which collects courses, demos and documentation for Tabular Editor. Prior to Tabular Editor 3.27.0 this item was called **What's New** and showed the release notes of the installed version; release notes now live in the @release-history.

> [!NOTE]
> 专属支持仅提供给 Tabular Editor 3 企业版客户。 All other customers should reach out on the [public community support site](https://github.com/TabularEditor/TabularEditor3) for any technical issues, questions or other product-specific questions.

- **关于 Tabular Editor**：打开一个对话框，显示当前使用的 Tabular Editor 版本的详细信息，以及安装与许可详情。 The dialog also lets you change your license key.

## 动态菜单（取决于上下文）

除了上面提到的菜单外，还可能在特定情况下出现其他菜单，具体取决于当前获得焦点的 UI 元素，以及在 TOM Explorer 中当前选中的对象。 For example, if you select a Table-object, a **Table** menu will appear, holding the same context-specific shortcut items as when you right-click on that object in the TOM Explorer.

If you switch the input focus between different types of documents (i.e. DAX 查询、Pivot Grid、图表等），你也会看到一个表示当前处于焦点的文档类型的菜单。 That menu will hold items relevant for the current document. For example, when a diagram currently has focus, there will be a **Diagram** menu which has an item for adding tables to the diagram, among others.

你可以在 **工具 > 偏好 > 用户界面** 中更改这些动态菜单的行为。

# 后续步骤

- @tom-explorer-view
- @supported-files
- @偏好