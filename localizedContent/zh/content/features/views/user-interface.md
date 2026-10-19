---
uid: user-interface
title: 基本用户界面
author: Daniel Otykier
updated: 2026-10-13
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

本文介绍了 Tabular Editor 3 的用户界面。

## 基本用户界面元素

加载语义模型后，Tabular Editor 3 显示以下默认布局。

![基本用户界面](~/content/assets/images/basic-ui.png)

1. **标题栏**：已加载文件的名称，或者您所连接的 Analysis Services 数据库或 Power BI 语义模型的名称。
2. **菜单栏**： Tabular Editor 3 的所有功能。请参阅[菜单](#menus)了解每个菜单。
3. **工具栏**：最常用的功能。每个工具栏命令也都在菜单中。在**工具 > 自定义……**下自定义工具栏及其按钮。
4. **TOM 资源管理器视图**：模型对象的树状视图，由 [Tabular Object Model (TOM)](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 元数据构建。顶部的切换按钮用于筛选要显示的对象类型，搜索框用于按名称筛选对象。
5. **表达式编辑器**：编辑在 TOM Explorer 中选定对象的 DAX、SQL 或 M 表达式。如果您将其关闭，请双击 TOM Explorer 中的对象以再次打开。如果对象具有多个表达式属性，则顶部的下拉菜单可在它们之间切换。例如，KPI 有一个目标、一个状态和一个趋势表达式。
6. **属性视图**：在 TOM Explorer 中选定对象的所有 TOM 属性。您可以在网格中编辑大多数属性，也可以在选择多个对象时进行编辑。对于某些属性（例如**格式字符串**、**连接字符串**和**角色成员**），可以通过值单元格中的省略号按钮打开对话框或集合编辑器。
7. **消息视图**：通过对模型的 DAX 表达式进行持续分析发现的语义错误，以及来自 C# 脚本的消息和 Analysis Services 报告的错误。
8. **状态栏**：有关当前所选内容、最佳实践分析器发现结果等的信息。连接项将您连接到的数据库和服务器显示为“<database>@<server>”，或对于 Power BI Desktop 显示为“<host>:<port>”，对于在无连接的情况下加载的模型显示为 **(无连接)**。当[MCP 服务器](xref:mcp-server)可用时，右端的指示器显示为**MCP 已启动**或**MCP 已停止**，其工具提示显示服务器侦听的地址。单击指示器以打开**MCP 服务器**对话框，或右键单击指示器以启动或停止服务器、复制代理的注册配置或打开首选项页面。

[“视图”菜单](#view)可打开其他视图。

## 自定义用户界面

您可以调整所有 UI 元素的大小并重新排列，还可以将视图拖出主窗口，例如拖到另一台显示器上。当你关闭应用程序时，Tabular Editor 3 会保存布局，并在下次启动时恢复该布局。

### 选择不同的布局

选择**“窗口”>“默认布局”**，将应用程序重置为默认布局；或选择**“窗口”>“经典布局”**，将 TOM 资源管理器置于左侧，并将“属性”视图置于“表达式编辑器”下方，与 Tabular Editor 2.x 一样。

要切换您自己的布局，请使用**“窗口”>“捕获布局”**保存当前布局，它将成为**“窗口”**菜单中的一个选项。**“窗口”>“布局...”**列出了所有布局，您可以在其中应用、加载、删除和保存布局。保存到磁盘的布局是一个 .xml 文件，您可以与其他 Tabular Editor 3 用户共享该文件。

![管理布局](~/content/assets/images/manage-layouts.png)

### 窗口停靠选项

当您拖动视图或文档时，停靠指示器会显示您可以将其停靠的位置。

![窗口停靠选项](~/content/assets/images/window-docking-options.png)

您将窗口拖放到哪里决定了它的行为方式：

**文档选项卡停靠（中心指示器）**：拖放到中心指示器上的窗口将成为主文档区域中的文档选项卡，位于 DAX 查询、脚本和图表等文档旁边。文档选项卡：
- 在您使用 **Ctrl+Tab** 循环切换时包含在内
- 不具备自动隐藏功能

**工具窗口停靠（边缘指示器）**：拖放到左侧、右侧、顶部或底部指示器上的窗口将作为工具窗口停靠，例如 TOM Explorer 和“消息”视图。工具窗口：
- 不包括在 **Ctrl+Tab** 中
- 具有可开启自动隐藏功能的图钉图标，该功能会在窗口不使用时将其折叠
- 可停靠在主文档区域的任意一侧

> [!TIP]
> 固定窗口的大小取决于您将其固定的位置的可用空间，您可以通过拖动窗口之间的分隔线来调整其大小。

### 更改主题和调色板

在**窗口 > 主题**下选择一个主题：

- Basic 和 Bezier 基于矢量，可在高 DPI 显示器上缩放。
- 蓝色、深色和浅色是基于光栅的，在高 DPI 显示器上缩放效果不佳。

对于“基本”和“贝塞尔”，**“窗口”>“默认调色板”**可更改主题的颜色。

![调色板](~/content/assets/images/palettes.png)

## 菜单

本节介绍每个菜单。

*活动文档*是指带有光标的文档，例如表达式编辑器或下图中的“DAX 脚本 1”选项卡。某些快捷键和菜单项取决于文档是否处于活动状态及其类型。

> [!NOTE]
> 菜单和工具栏默认锁定在原位。要解锁它们，请在**工具 > 自定义... > 选项**下取消选中**锁定菜单和工具栏**。

<!-- 重新截取屏幕截图 (3.27.1)：active-document.png。标题栏使用旧格式。可选。-->
![活动文档](~/content/assets/images/active-document.png)

### 文件

“**文件**”菜单用于加载和保存模型元数据、支持文件和文档。

![“文件”菜单](~/content/assets/images/file-menu.png)

- **新建**：创建新的空白模型 (**Ctrl+N**) 或[支持文件](xref:supported-files#supported-file-types)，例如 DAX 查询、DAX 脚本（文本文件）或图表（JSON 文件）。C# 脚本以外的支持文件需要已加载的模型。
  
  ![“文件”菜单“新建”](~/content/assets/images/file-menu-new.png)

> [!IMPORTANT]
> **新建 > 模型…** 在 Tabular Editor 3 Desktop 版本中不可用，该版本仅作为 Power BI Desktop 的外部工具使用。请参阅@editions。

- **打开**：从以下来源之一加载模型，或打开任何其他受支持的文件：

  ![“文件”菜单“打开”](~/content/assets/images/file-menu-open.png)

  - **从文件打开模型…** 从 .bim 或 .pbit 文件等文件中打开模型元数据。
  - **从数据库打开模型...**加载已部署模型的元数据。输入 Analysis Services 或 Power BI XMLA 连接详细信息，或连接到本地实例，例如 Visual Studio 的集成工作区服务器或 Power BI Desktop。右键单击**服务器**列表中的服务器，将其固定到列表顶部或将其删除。请参阅 @xmla-as-connectivity。
  - **从文件夹打开模型…** 从由任何版本的 Tabular Editor 保存的文件夹结构打开模型元数据。
  - **文件…** 按文件扩展名打开 Tabular Editor 3 支持的任何文件类型。请参阅[支持的文件类型](xref:supported-files)。
  - **从指标视图 YAML 导入...** 从 Databricks 指标视图 YAML 文件导入模型元数据。

    ![支持的文件类型](~/content/assets/images/supported-file-types.png)

> [!IMPORTANT]
> 在 Tabular Editor 3 Desktop 版本中，**打开 > 从文件打开模型…** 和 **打开 > 从文件夹打开模型…** 不可用，而 **打开 > 文件…** 仅可打开[支持的文件](xref:supported-files#supported-file-types)。

- **从磁盘重新加载**/**从服务器重新加载**：从源重新加载模型元数据并放弃所有未保存的更改。对于从文件或文件夹加载的模型，该命令显示为**从磁盘重新加载**；对于从 Analysis Services 或 Power BI 打开的模型，该命令显示为**从服务器重新加载**。如果 Tabular Editor 3 作为 Power BI Desktop 的外部工具运行，并且模型在 Power BI Desktop 中发生变化，请使用此命令在不重新连接的情况下重新加载模型元数据。从文件或文件夹加载的模型会在文件发生变化时自动重新加载。请参阅[从磁盘自动重新加载](xref:auto-reload)。在重新加载过程中，打开的 DAX 查询和 Pivot Grid 文档将保持打开状态，并连接到重新加载的模型。
- **关闭文档** (**Ctrl+W**)：关闭主区域中的活动文档或面板，例如 DAX 查询、C# 脚本或图表。如果文档有未保存的更改，则会显示保存更改的提示。
- **关闭模型**：卸载模型元数据。如果您更改了元数据，则会显示保存更改的提示。打开的 DAX 查询和 Pivot Grid 文档将随模型一起关闭，对于每个有未保存更改的文档，都会显示保存提示。
- **保存**：将活动文档保存到其源文件。如果没有处于活动状态的文档，则将模型元数据保存到其源：Model.bim 文件、Database.json 文件夹结构、Analysis Services 实例（包括 Power BI Desktop）或 Power BI XMLA endpoint。
- **另存为…**将活动文档另存为新文件。如果没有处于活动状态的文档，则将模型元数据另存为新的 .bim (JSON) 文件。
- **保存到文件夹…**将模型元数据保存为[文件夹结构](xref:save-to-folder)。
- **全部保存**：保存所有未保存的文档和模型元数据。
- **最近使用的文件**：列出最近使用的支持文件。
- **最近的表格模型**：列出最近使用的模型元数据文件和文件夹。

将**模型源详细信息**设置为**仅名称**或**隐藏**时，最近文件和模型菜单的悬停文本将显示不带目录的文件名。

> [!IMPORTANT]
> 在 Tabular Editor 3 Desktop 版本中，**保存到文件夹**和**最近使用的表格模型**被禁用，**另存为**仅对[支持文件](xref:supported-files#supported-file-types)启用。

- **退出**：关闭 Tabular Editor 3。首先会显示保存未保存文件或模型元数据的提示。

### 编辑

**“编辑”**菜单用于编辑活动文档或已加载的模型元数据。

![“编辑”菜单](~/content/assets/images/edit-menu.png)

- **撤消**：撤消窗口中具有焦点的部分中的最后一次更改。在文本控件（例如文档或**表达式编辑器**）中，它会撤消键入操作，并显示为**撤消键入**。在其他地方，它会撤消对模型元数据的上一次更改。**Ctrl+Z** 可运行此命令。
- **重做**：重做上一次撤销的更改，遵循与**撤销**相同的规则。**Ctrl+Y** 运行此命令。
- **撤消**/**重做**后跟模型更改的名称，例如**撤消 C# 脚本 (MCP)**：仅在文本控件获得焦点时显示，并撤消或重做对模型元数据的上一次更改。请参阅[在文本编辑器中撤消](xref:undo-redo#undo-in-text-editors)。
- **查找**：在“查找”选项卡上打开“查找和替换”对话框。请参阅[查找](xref:find-replace#find)。
- **替换**：在“替换”选项卡上打开“查找和替换”对话框。请参阅[替换](xref:find-replace#replace)。
- **剪切/复制/粘贴**：当文本控件获得焦点时，这些操作将应用于选定的文本。当 TOM Explorer 获得焦点时，它们将应用于所选对象。例如，要复制多个度量值，请在 TOM Explorer 中使用 **Shift** 或 **Ctrl** 选择它们，然后按 **Ctrl+C**，再按 **Ctrl+V**。
- **删除**：当文本控件获得焦点时，删除所选文本；当 TOM Explorer 获得焦点时，删除所选对象。

> [!NOTE]
> 仅当选择了多个对象，或者当其他对象依赖于您要删除的对象时，才会显示删除提示。**撤消** (**Ctrl+Z**) 可恢复已删除的对象。

- **全选**：选择活动文档中的所有文本，或 TOM Explorer 中具有相同父级的所有对象。
- **代码助手**：DAX 代码助手功能的快捷方式。在您编辑 DAX 时可用。请参阅[DAX 编辑器](xref:dax-editor#code-assist-features)。
- **自动换行**：切换活动文本文档中的自动换行。

### 查看

**“视图”**菜单打开并聚焦 Tabular Editor 3 的视图，包括隐藏的视图。未列出文档；使用[“窗口”菜单](#window)在它们之间切换。

![“视图”菜单](~/content/assets/images/view-menu.png)

- **TOM 资源管理器**：已加载模型的[Tabular Object Model (TOM)](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 的树。请参阅 @tom-explorer-view。
- **AI 助手**：与 AI 助手进行聊天，以完成建模任务。
- **DAX 组件管理器**：浏览 DAX 用户定义函数组件，并将其安装到模型中。
- **Best Practice Analyzer**：根据您定义的最佳实践规则验证模型。请参阅 @bpa-view。
- **消息**：来自 Tabular Editor 3 语义分析器等来源的错误、警告和信息性消息。请参阅 @messages-view。
- **数据刷新**：跟踪在后台运行的刷新操作。请参阅 @data-refresh-view。
- **表达式编辑器**：编辑在 TOM Explorer 中选定对象的 DAX、M 或 SQL 表达式。请参阅@dax-editor。
- **宏**：管理您从 @csharp-scripts 创建的宏。请参阅 @creating-macros。
- **VertiPaq 分析器**：收集、导入和导出有关模型中数据的统计信息，用于 DAX 性能调优。VertiPaq Analyzer 由 [SQLBI](https://twitter.com/marcorus) 的 [Marco Russo](https://sqlbi.com) 根据 MIT 许可证创建和维护。请参阅[GitHub 项目页面](https://github.com/sql-bi/VertiPaq-Analyzer)。
- **依赖项**：[**DAX依赖项**视图](xref:creating-and-testing-dax#dax-dependencies)显示选定对象与模型中其他对象之间的依赖关系。选择**跟踪 TOM Explorer**，使其跟随 TOM Explorer 的选择。
- **DAX 优化器**：使用 [DAX 优化器](https://www.daxoptimizer.com)分析模型的 DAX 性能问题。
- **日历编辑器**：为现代时间智能功能定义和管理日历。
- **透视编辑器**：一个矩阵，显示模型每个透视包含的对象。
- **元数据翻译编辑器**：用于编辑模型对象的元数据翻译（文化）的网格。
- **工具栏/属性**：切换工具栏的可见性并打开“属性”视图（**F4**）。

### 模型

**“模型”**菜单包含对模型对象（TOM Explorer 的根）的操作。

![视图菜单](~/content/assets/images/model-menu.png)

- **部署…**：打开 Tabular Editor 部署向导。请参阅[模型部署](xref:deployment)。

> [!IMPORTANT]
> **部署**在 Tabular Editor 3 Desktop 版本中不可用。请参阅@editions。

- **序列化选项...** 设置模型元数据在保存到文件或文件夹结构时如何进行序列化。
- **导入表格...** 打开 Tabular Editor 3 导入表格向导。请参阅@importing-tables。
- **更新架构(所有表格)…**将所有表格的列与其数据源进行比较，并检测架构更改。请参阅[更新表格架构](xref:importing-tables#updating-table-schema)。
- **脚本 DAX**：为选定对象生成 DAX 脚本，如果未选择任何内容，则为模型中的所有 DAX 对象生成 DAX 脚本。请参阅 @dax-scripts。
- **刷新模型**：当 Tabular Editor 连接到 Analysis Services 时，启动模型的后台刷新。请参阅[刷新命令 (TMSL)](https://docs.microsoft.com/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request )。子菜单具有以下选项：
  - **自动(模型)**：Analysis Services 仅刷新不处于“就绪”状态的对象。
  - **完全刷新(模型)**：Analysis Services 对模型执行完全刷新。
  - **计算(模型)**：Analysis Services 重新计算所有计算表、计算列、计算组和关系。不会从数据源读取任何数据。
- **添加 [对象类型]**：其余项目创建模型子对象，例如表、数据源和透视。

### 工具

**“工具”**菜单包含 Tabular Editor 3 的首选项和自定义项。

![“视图”菜单](~/content/assets/images/tools-menu.png)

- **自定义……**将打开“用户界面布局”自定义对话框，您可以在其中创建工具栏，并重新排列和编辑菜单及工具栏按钮。
- **偏好设置…** 打开“偏好设置”对话框，其中包含更新检查、代理设置、查询行数限制和请求超时等设置。请参阅 @preferences。
- **管理 BPA 规则…** 打开 Best Practice Analyzer 规则管理器，您可以在其中查看和编辑规则及规则集合。请参阅 @bpa-view。
- **MCP 服务器...** 打开“**MCP 服务器**”对话框，您可以在其中启动和停止允许外部 AI 代理在打开的模型上工作的服务器，查看代理获得的权限，并复制代理的注册配置。请参阅@mcp-server。当未安装 AI 功能组件、取消选中**启用 MCP 服务器**或管理员通过策略禁用该功能时，此项将被隐藏。

### 窗口

**“窗口”**菜单用于管理和切换应用程序的视图和文档（统称为*窗口*），还包含[主题和调色板](#changing-themes-and-palettes)设置。

![“窗口”菜单](~/content/assets/images/window-menu.png)

- **新建…**用于创建[支持文件](xref:supported-files#supported-file-types)。选项与**文件 > 新建**下的选项相同。
- **浮动**将当前视图或文档分离为浮动窗口。
- **固定选项卡**将选项卡固定到文档选项卡的左端。选项卡右键单击菜单包含仅关闭未固定的选项卡的命令。
  
  ![视图菜单](~/content/assets/images/tab-context-menu.png)

- **新建水平/垂直选项卡组**：将主文档区域划分为选项卡组，以便并排或上下显示多个文档。
- **全部关闭**：关闭所有文档选项卡。首先会显示保存未保存更改的提示。
- **重置窗口布局**：重置主文档区域的所有自定义设置。
- **1..N [document]**：前 10 个打开的文档。**Ctrl+Tab** 还可以切换已打开的文档和视图：

  ![视图菜单](~/content/assets/images/ctrl-tab.png)

- **窗口...**：打开一个对话框，其中列出所有已打开的文档，您可以在其中切换到或关闭每个文档。

  ![视图菜单](~/content/assets/images/windows-manager.png)

- **捕获布局**/**布局...**/**默认布局**/**经典布局**：请参阅[选择不同的布局](#choosing-a-different-layout)。
- **主题**/**默认调色板**：请参阅[更改主题和调色板](#changing-themes-and-palettes)。
- **语言**：更改 Tabular Editor 3 用户界面的显示语言。

### 帮助

“**帮助**”菜单链接到在线资源。

![“帮助”菜单](~/content/assets/images/help-menu.png)

- **在线文档**：在默认Web浏览器中打开 [docs.tabulareditor.com](https://docs.tabulareditor.com)。
- **入门指南**：打开面向新用户的 Tabular Editor 3 入门指南。
- **社区支持**：打开[公共社区支持网站](https://github.com/TabularEditor/TabularEditor3 )。
- **专门支持**：向专门支持热线发送电子邮件。
- **入门**：打开**入门**页面，该页面收集了 Tabular Editor 的课程、演示和文档。在 Tabular Editor 3.27.0 之前，此项称为**新增功能**。有关发布说明，请参阅 @release-history。

> [!NOTE]
> 专用支持面向 Tabular Editor 3 企业版客户。其他客户使用[公共社区支持网站](https://github.com/TabularEditor/TabularEditor3)来咨询技术和产品问题。

- **关于 Tabular Editor**：显示版本、安装和许可详细信息，并允许您更改许可证密钥。
 
### 动态菜单（取决于上下文）

根据哪个 UI 元素具有焦点以及在 TOM Explorer 中选定了哪个对象，将显示额外的菜单。例如，如果您选择一个表格，则会显示一个**表格**菜单，其中的项目与 TOM Explorer 中表格的右键单击菜单中的项目相同。

每种文档类型（例如 DAX 查询、Pivot Grid 和图表）也会在相应类型的文档获得焦点时添加一个菜单。例如，处于焦点的图表会添加一个**图表**菜单，其中包含一个用于将表格添加到图表的项。

在**工具 > 偏好 > Tabular Editor > 用户界面**下设置这些动态菜单的行为。

## 后续步骤

- @tom-explorer-view
- @supported-files
- @preferences
