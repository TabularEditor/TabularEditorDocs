---
uid: user-interface
title: 基本用户界面
author: Daniel Otykier
updated: 2026-11-23
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

加载语义模型后，Tabular Editor 3 会显示如下默认布局。

![基本用户界面](~/content/assets/images/basic-ui.png)

1. **标题栏**：已加载文件的名称，或您所连接的 Analysis Services 数据库或 Power BI 语义模型的名称，以及 Tabular Editor 3 的版本，例如 **v28.0.0**。
2. **菜单栏**：Tabular Editor 3 的所有功能。请参阅[菜单](#menus)了解每个菜单。
3. **工具栏**：最常用的功能。每个工具栏命令也位于菜单中。在**工具 > 自定义……**下自定义工具栏及其按钮。
4. **TOM 资源管理器视图**：模型对象的树状视图，由 [Tabular Object Model (TOM)](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 元数据构建而成。顶部的切换按钮用于筛选要显示的对象类型，搜索框用于按名称筛选对象。
5. **表达式编辑器**：编辑在 TOM Explorer 中选定对象的 DAX、SQL 或 M 表达式。如果您将其关闭，请双击 TOM Explorer 中的对象以再次打开。如果对象具有多个表达式属性，则顶部的下拉菜单可在它们之间切换。例如，KPI 具有目标、状态和趋势表达式。
6. **属性视图**：在包含所有 TOM 属性的网格中显示在 TOM Explorer 中选定对象的属性。启用**基本属性视图**公开预览后，该视图底部有两个选项卡：**基本**显示 Power BI Desktop 以表单形式显示的字段，**高级**显示网格。您可以编辑大多数属性，也可以在选择多个对象时进行编辑。在**“高级”**选项卡上，对于某些属性（例如**“格式字符串”**、**“连接字符串”**和**“角色成员”**），可以通过值单元格中的省略号按钮打开对话框或集合编辑器。
7. **消息视图**：通过对模型的 DAX 表达式进行持续分析发现的语义错误，以及来自 C# 脚本的消息和 Analysis Services 报告的错误。
8. **状态栏**：有关当前选择、Best Practice Analyzer 发现结果等的信息。连接项将您连接到的数据库和服务器显示为 `<database>@<server>`，或对于 Power BI Desktop 显示为 `<host>:<port>`，对于在没有连接的情况下加载的模型显示为 **(无连接)**。当 [MCP 服务器](xref:mcp-server)可用时，右端的指示器显示 **MCP 已启动** 或 **MCP 已停止**，其工具提示显示服务器侦听的地址。单击指示器以打开**MCP 服务器**对话框，或右键单击指示器以启动或停止服务器、复制代理的注册配置或打开首选项页面。

[视图菜单](#view) 可打开其他视图。

## 自定义用户界面

你可以调整并重新排列所有 UI 元素，还可以将视图拖出主窗口，例如拖到另一台显示器上。关闭应用程序时，Tabular Editor 3 会保存布局，并在下次启动时恢复。

### 选择不同的布局

选择 **窗口 > 默认布局** 可将应用程序重置为默认布局；或者选择 **窗口 > 经典布局**，将 TOM Explorer 放在左侧，并将属性视图放在表达式编辑器下方，就像 Tabular Editor 2.x 一样。

要切换您自己的布局，请使用“窗口”>“捕获布局”保存当前布局，它将成为“窗口”菜单中的一个选项。**“窗口”>“布局...”**列出了所有布局，您可以在其中应用、加载、移除和保存布局。保存到磁盘的布局是一个 .xml 文件，您可以与其他 Tabular Editor 3 用户共享该文件。布局会保留作为文档选项卡固定的工具窗口（例如**表达式编辑器**或**消息**）的顺序，以及其中哪些窗口被锁定。

![管理布局](~/content/assets/images/manage-layouts.png)

### 窗口停靠选项

拖动视图或文档时，停靠指示器会显示可停靠的位置。

![窗口停靠选项](~/content/assets/images/window-docking-options.png)

将窗口放到哪里，决定了它的停靠方式：

**文档选项卡停靠（中心指示器）**：将窗口拖放到中心指示器上后，它会成为主文档区域中的一个文档选项卡，与 DAX 查询、脚本和关系图等文档并列。文档选项卡：

- 使用 **Ctrl+Tab** 循环切换时会包含在内
- 不支持自动隐藏

**工具窗口停靠（边缘指示器）**：将窗口拖放到左侧、右侧、顶部或底部指示器上后，它会作为工具窗口停靠，例如 TOM Explorer 和信息视图。工具窗口：

- 使用 **Ctrl+Tab** 切换时不会包含在内
- 带有可启用自动隐藏的图钉图标；窗口未使用时会自动折叠
- 可停靠在主文档区域的任意一侧

> [!TIP]
> 停靠窗口的大小取决于停靠位置的可用空间，你可以拖动窗口之间的分隔条来调整其大小。

### 更改主题和调色板

在 **窗口 > 主题** 中选择主题：

- Basic 和 Bezier 是基于矢量的，可在高 DPI 显示器上缩放。
- Blue、Dark 和 Light 是基于位图的，在高 DPI 显示器上缩放效果不佳。

对于 Basic 和 Bezier，**窗口 > 默认调色板** 可更改主题颜色。

![Palettes](~/content/assets/images/palettes.png)

## 菜单

本节介绍各个菜单。

_活动文档_ 是指当前光标所在的文档，比如表达式编辑器或下方截图中的“DAX脚本 1”选项卡。某些快捷键和菜单项取决于当前是否有活动文档，以及该文档的类型。

> [!NOTE]
> 默认情况下，菜单和工具栏会锁定在原位。要解锁，请取消选中 **锁定菜单和工具栏**，位于 **工具 > 自定义…… > 选项**。

![Tabular Editor 3，其中 DAX 脚本 1 为活动文档](~/content/assets/images/active-document.png)

### 文件

**文件** 菜单用于加载和保存模型元数据、相关支持文件以及文档。

![File Menu](~/content/assets/images/file-menu.png)

- **新建**：创建新的空白模型（**Ctrl+N**），或创建一个[支持文件](xref:supported-files#supported-file-types)，例如 DAX 查询、DAX脚本（文本文件）或关系图（JSON 文件）。除 C# Script 外，其他支持文件在使用前都需要先加载模型。

  ![File Menu New](~/content/assets/images/file-menu-new.png)

> [!IMPORTANT]
> **新建 > 模型...** 选项在 Tabular Editor 3 桌面版中不可用；该版本只能作为 Power BI Desktop 的外部工具使用。参见 @editions。

- **打开**：从以下来源之一加载模型，或打开任何其他支持的文件：

  ![File Menu Open](~/content/assets/images/file-menu-open.png)

  - **从文件加载模型...**：从 .bim 或 .pbit 等文件打开模型元数据。
  - **从数据库打开模型…**加载已部署模型的元数据。输入 Analysis Services 或 Power BI XMLA 连接详细信息，或连接到本地实例，例如 Visual Studio 的集成工作区服务器或 Power BI Desktop。右键单击**服务器**列表中的服务器，将其固定到列表顶部或将其删除。请参阅@xmla-as-connectivity。
  - **从文件夹加载模型...**：从由任意版本的 Tabular Editor 保存的文件夹结构中打开模型元数据。
  - **文件...**：根据文件扩展名打开 Tabular Editor 3 支持的任意文件类型。参见[支持的文件类型](xref:supported-files)。
  - **从 Metric View YAML 导入...**：从 Databricks Metric View YAML 文件导入模型元数据。

    ![支持的文件类型](~/content/assets/images/supported-file-types.png)

> [!IMPORTANT]
> 在 Tabular Editor 3 桌面版中，**打开 > 从文件加载模型...** 和 **打开 > 从文件夹加载模型...** 不可用，且 **打开 > 文件...** 只能打开[支持文件](xref:supported-files#supported-file-types)。

- **从磁盘重新加载**/**从服务器重新加载**：从源重新加载模型元数据并放弃所有未保存的更改。对于从文件或文件夹加载的模型，该命令显示为**从磁盘重新加载**；对于从 Analysis Services 或 Power BI 打开的模型，该命令显示为**从服务器重新加载**。如果 Tabular Editor 3 作为 Power BI Desktop 的外部工具运行，并且模型在 Power BI Desktop 中发生变化，请使用此命令在不重新连接的情况下重新加载模型元数据。从文件或文件夹加载的模型会在文件发生变化时自动重新加载。请参阅[从磁盘自动重新加载](xref:auto-reload)。打开的 DAX 查询和 Pivot Grid 文档在重新加载期间保持打开状态，并连接到重新加载的模型。
- **关闭文档**（**Ctrl+W**）：关闭主区域中当前活动的文档或面板，例如 DAX 查询、C# Script 或关系图。如果文档有未保存的更改，系统会提示你保存这些更改。
- **关闭模型**：卸载模型元数据。如果您更改了元数据，则会显示保存更改的提示。打开的 DAX 查询和 Pivot Grid 文档将随模型一起关闭，对于每个有未保存更改的文档，都会显示保存提示。
- **保存**：将活动文档保存到其源文件。如果当前没有活动文档，则会将模型元数据保存回其源：Model.bim 文件、Database.json 文件夹结构、Analysis Services 实例（包括 Power BI Desktop）或 Power BI XMLA endpoint。
- **另存为...**：将活动文档另存为新文件。如果当前没有活动文档，则将模型元数据另存为新的 .bim（JSON）文件。
- **保存到文件夹...**：将模型元数据以[文件夹结构](xref:save-to-folder)的形式保存。
- **全部保存**：一次性保存所有未保存的文档和模型元数据。
- **最近文件**：列出最近使用的支持文件。
- **最近的表格模型**：列出最近使用的模型元数据文件和文件夹。

如果将**模型源详细信息**设置为**仅名称**或**隐藏**，则最近文件和模型菜单的悬停文本将显示不带目录的文件名。

> [!IMPORTANT]
> 在 Tabular Editor 3 桌面版中，**保存到文件夹**和**最近的表格模型**已禁用，而**另存为**仅可用于[支持文件](xref:supported-files#supported-file-types)。

- **退出**：关闭 Tabular Editor 3。此时会先提示你保存未保存的文件或模型元数据。

### 编辑

**编辑**菜单用于编辑活动文档或已加载的模型元数据。

![“编辑”菜单，底部显示“重置缩放”](~/content/assets/images/edit-menu.png)

- **撤消**：撤消窗口中具有焦点的部分中的上一次更改。在文本控件（例如文档或**表达式编辑器**）中，它会撤消键入操作，并显示为**撤消键入**。在其他地方（包括下拉列表或只读文本框），它会撤消对模型元数据的上一次更改。**Ctrl+Z** 可运行此命令。
- **重做**：重做上一次已撤销的更改，规则与 **撤销** 相同。 **Ctrl+Y** 执行此命令。
- **撤销** / **重做** 后跟模型更改名称，例如 **撤销 C# script (MCP)**：仅当文本控件获得焦点时才会出现，用于撤销或重做对模型元数据所做的最后一次更改。参见 [文本编辑器中的撤销](xref:undo-redo#undo-in-text-editors)。
- **查找**：打开“查找和替换”对话框，并切换到“查找”选项卡。参见[查找](xref:find-replace#find)。
- **替换**：打开“查找和替换”对话框，并切换到“替换”选项卡。参见[替换](xref:find-replace#replace)。
- **剪切 / 复制 / 粘贴**：当文本控件具有焦点时，这些命令作用于所选文本。当 TOM Explorer 获得焦点时，这些命令作用于所选对象。例如，要复制多个度量值，请在 TOM Explorer 中按住 **Shift** 或 **Ctrl** 选择它们，然后按 **Ctrl+C**，再按 **Ctrl+V**。
- **删除**：当文本控件获得焦点时，删除所选文本；当 TOM Explorer 获得焦点时，删除所选对象。

> [!NOTE]
> 只有在选中了多个对象，或其他对象依赖于你要删除的对象时，才会出现删除提示。**撤销**（**Ctrl+Z**）可还原已删除的对象。

- **全选**：选中活动文档中的所有文本，或选中 TOM Explorer 中具有相同父级的所有对象。
- **Code Assist**：用于 DAX 的 Code Assist 功能的快捷方式。在编辑 DAX 时可用。请参阅 [DAX 编辑器](xref:dax-editor#code-assist-features)。
- **自动换行**：在当前活动的文本文档中切换是否启用自动换行。
- **重置缩放**（**Ctrl+0** 或 **Ctrl+NumPad0**）：将使用 Ctrl+鼠标滚轮缩放的代码编辑器恢复为在 **工具 > 首选项 > Tabular Editor > 用户界面**下设置的**代码编辑器字体大小**。仅在活动编辑器或页面缩放时可用。请参阅[字体](xref:preferences#fonts)。

### 视图

**视图**菜单用于打开并聚焦 Tabular Editor 3 的各个视图，包括隐藏的视图。这里不会列出文档；可通过 [窗口菜单](#window) 在它们之间切换。

![视图菜单](~/content/assets/images/view-menu.png)

- **TOM 资源管理器**：加载模型的[Tabular Object Model (TOM)](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 的树状视图。请参阅@tom-explorer-view。
- **AI 助手**：与 AI 助手聊天的窗口，用于处理建模任务。
- **DAX 组件管理器**：浏览 DAX 用户定义函数组件并将其安装到模型中。
- **Best Practice Analyzer**：根据您定义的最佳实践规则验证模型。请参阅 @bpa-view。
- **消息**：来自 Tabular Editor 3 语义分析器等来源的错误、警告和信息消息。请参阅 @messages-view。
- **数据刷新**：跟踪在后台运行的刷新操作。请参阅 @data-refresh-view。
- **表达式编辑器**：编辑在 TOM Explorer 中选定对象的 DAX、M 或 SQL 表达式。请参阅 @dax-editor。
- **宏**：管理您从 @csharp-scripts 创建的宏。请参阅 @creating-macros。
- **VertiPaq 分析器**：收集、导入和导出有关模型中数据的统计信息，用于 DAX 性能优化。VertiPaq Analyzer 由 [SQLBI](https://sqlbi.com) 的 [Marco Russo](https://twitter.com/marcorus) 根据 MIT 许可证创建和维护。请参阅[GitHub 项目页面](https://github.com/sql-bi/VertiPaq-Analyzer)。
- **依赖项**：[**DAX 依赖项**视图](xref:creating-and-testing-dax#dax-dependencies)显示所选对象与模型中其他对象之间的依赖项。选择**跟踪 TOM Explorer**，使其跟随 TOM Explorer 的选择。
- **DAX 优化器**：使用 [DAX 优化器](https://www.daxoptimizer.com)分析模型的 DAX 性能问题。
- **日历编辑器**：为现代时间智能功能定义和管理日历。
- **透视编辑器**：一个矩阵，显示模型的每个透视包含哪些对象。
- **元数据翻译编辑器**：用于编辑模型对象的元数据翻译（文化）的网格。
- **工具栏/属性**：切换工具栏的可见性并打开“属性”视图（**F4**）。

### 模型

**“模型”**菜单包含对模型对象（TOM Explorer 的根）的操作。

![模型菜单](~/content/assets/images/model-menu.png)

- **Deploy...**：打开 Tabular Editor Deployment Wizard。参见 [模型部署](xref:deployment)。

> [!IMPORTANT]
> **部署**在 Tabular Editor 3 Desktop 版本中不可用。请参阅@editions。

- **序列化选项...** 设置模型元数据在保存到文件或文件夹结构时如何进行序列化。
- **导入表格…** 打开 Tabular Editor 3 导入表格向导。请参阅@importing-tables。
- **更新架构(所有表格)…**将所有表格的列与其数据源进行比较，并检测架构更改。请参阅[更新表格架构](xref:importing-tables#updating-table-schema)。
- **脚本 DAX**：为选定对象生成 DAX 脚本，如果未选择任何内容，则为模型中的所有 DAX 对象生成 DAX 脚本。请参阅@dax-scripts。
- **刷新模型**：当 Tabular Editor 连接到 Analysis Services 时，启动模型的后台刷新。请参阅[刷新命令 (TMSL)](https://docs.microsoft.com/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request)。子菜单包含以下选项：
  - **自动(模型)**：Analysis Services 仅刷新不处于“就绪”状态的对象。
  - **完全刷新（模型）**：Analysis Services 对模型执行完全刷新。
  - **计算（模型）**：Analysis Services 将重新计算所有计算表格、计算列、计算组和关系。不会从数据源读取任何数据。
- **添加 [对象类型]**：其余项用于创建模型的子对象，例如表、数据源和透视。

### 工具

**工具**菜单包含用于设置 Tabular Editor 3 偏好设置和自定义项的选项。

![视图菜单](~/content/assets/images/tools-menu.png)

- **自定义...**：打开“用户界面布局”自定义对话框，可在其中创建工具栏、重新排列并编辑菜单和工具栏按钮。
- **偏好...**：打开“偏好”对话框，其中包含更新检查、代理设置、查询行数限制和请求超时等设置。见 @preferences。
- **管理 BPA 规则...**：打开 Best Practice Analyzer 规则管理器，可在其中查看和编辑规则及规则集。请参阅 @bpa-view。
- **MCP Server...**：打开 **MCP Server** 对话框，可在其中启动或停止服务器，使外部 AI 代理能够处理当前打开的模型，查看该代理获得的权限，并复制用于代理的注册配置。请参阅 @mcp-server。如果未安装 AI 功能组件、未勾选 **启用 MCP 服务器**，或者管理员已通过策略将其禁用，则该项会被隐藏。

### 窗口

**窗口**菜单用于管理和切换应用中的视图和文档，这些统称&#x4E3A;_&#x7A97;口_；此外，该菜单还包含[主题和调色板](#changing-themes-and-palettes)设置。

![查看菜单](~/content/assets/images/window-menu.png)

- **新建...**：用于创建[支持文件](xref:supported-files#supported-file-types)。这些选项与 **文件 > 新建** 中的选项相同。

- **浮动**：将当前视图或文档从停靠状态解除，并在浮动窗口中显示。
- **固定选项卡**将选项卡固定到文档选项卡的左端。选项卡右键菜单包含仅关闭未固定的选项卡的命令，以及**复制**命令，该命令可打开 DAX 查询、DAX 脚本、C# 脚本、图表或数据透视表的未保存的新副本，包括其未保存的编辑内容。在您运行 DAX 查询副本之前，该副本不会有任何结果。 
  
  ![包含“复制”以及“固定”和“关闭”命令的选项卡右键菜单](~/content/assets/images/tab-context-menu.png)

- **新建水平/垂直选项卡组**：将主文档区域拆分为多个选项卡组，以并排或上下显示多个文档。

- **全部关闭**：关闭所有文档选项卡。如果存在未保存的更改，会先提示你保存。

- **重置窗口布局**：重置对主文档区域应用的所有自定义设置。

- **1..N [document]**：前 10 个已打开的文档。 **Ctrl+Tab** 也可在打开的文档和视图之间切换：

  ![Ctrl+Tab 快捷键](~/content/assets/images/ctrl-tab.png)

- **窗口...**：打开一个列出所有打开文档的对话框，你可以在其中切换到某个文档或将其关闭。

  ![窗口管理器](~/content/assets/images/windows-manager.png)

- **捕获布局** / **布局...** / **默认布局** / **经典布局**：参见[选择其他布局](#choosing-a-different-layout)。

- **主题** / **默认调色板**：参见[更改主题和调色板](#changing-themes-and-palettes)。

- **语言**：可以更改 Tabular Editor 3 用户界面的显示语言。

### 帮助

**帮助**菜单提供联机资源的入口。

![帮助菜单](~/content/assets/images/help-menu.png)

- **联机文档**：在默认 Web 浏览器中打开文档站点 [docs.tabulareditor.com](https://docs.tabulareditor.com)。
- **入门指南**：打开面向新用户的 Tabular Editor 3 入门指南。
- **社区支持**：打开我们的[公开社区支持站点](https://github.com/TabularEditor/TabularEditor3)。
- **专属支持**：发送电子邮件至专属支持热线。
- **入门**：打开**入门**页面，该页面汇集了 Tabular Editor 的课程、演示和文档。有关发布说明，请参阅 @release-history。

> [!NOTE]
> 专属支持仅面向 Tabular Editor 3 企业版客户。其他客户如果有技术或产品相关问题，可以前往[公开社区支持站点](https://github.com/TabularEditor/TabularEditor3)寻求帮助。

- **关于 Tabular Editor**：显示版本、安装和许可详细信息，并可更改许可证密钥。

### 动态菜单（取决于上下文）

额外的菜单会根据当前获得焦点的 UI 元素以及在 TOM Explorer 中选中的对象而显示。例如，如果你选择一个表，就会出现一个 **表** 菜单，其中的菜单项与在 TOM Explorer 中右键单击该表时显示的菜单相同。

每种文档类型(如 DAX 查询、Pivot Grid 和图表)在该类型文档获得焦点时，也会添加一个菜单。例如，当关系图获得焦点时，会添加一个 **关系图** 菜单，其中包含“向关系图添加表”的命令。

你可以在 **工具 > 偏好 > Tabular Editor > 用户界面** 中设置这些动态菜单的行为。

## 后续步骤

- @tom-explorer-view
- @supported-files
- @偏好
