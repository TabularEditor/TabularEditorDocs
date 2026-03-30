---
uid: user-interface
title: 基本用户界面
author: Daniel Otykier
updated: 2021-09-08
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
2. **菜单栏**：菜单栏用于访问 Tabular Editor 3 的各项功能。 有关所有菜单项的详细说明，请参阅[菜单](#menus)。 有关所有菜单项的详细说明，请参阅[菜单](#menus)。
3. **工具栏**：工具栏提供对最常用功能的快速访问。 工具栏中可用的所有功能也都可以通过菜单访问。 你可以在 **工具 > 自定义...** 中自定义工具栏及其按钮 工具栏中可用的所有功能也都可以通过菜单访问。 你可以在 **工具 > 自定义...** 中自定义工具栏及其按钮
4. **TOM Explorer 视图**：以层级结构展示您的数据模型，所有对象均可用 .  这些对象来自表示您的数据模型的 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 元数据。 顶部的切换按钮可让你筛选要显示的对象。 搜索框可按名称筛选对象。 顶部的切换按钮可让你筛选要显示的对象。 搜索框可按名称筛选对象。
5. **表达式编辑器**：表达式编辑器提供一种快捷方式，用于编辑 TOM Explorer 中当前选中对象的任意 DAX、SQL 或 M 表达式。 如果你关闭了表达式编辑器，只需在 TOM Explorer 中双击某个对象，即可将其重新打开。 顶部的下拉列表可让你在不同的表达式属性之间切换，以防当前选定对象包含多个此类属性（例如，KPI 具有目标表达式、状态表达式和趋势表达式，它们是同一个 KPI 对象下的 3 个不同 DAX 表达式）。
6. **属性视图**：显示 TOM Explorer 中当前选定对象（一个或多个）的所有可用 TOM 属性的详细信息。 大多数属性都可以通过网格进行编辑，即使同时选中了多个对象也一样。 某些属性（例如“格式字符串”“连接字符串”“角色成员”）提供弹出对话框或集合编辑器，可通过点击属性值单元格中的省略号按钮打开。 大多数属性都可以通过网格进行编辑，即使同时选中了多个对象也一样。 某些属性（例如“格式字符串”“连接字符串”“角色成员”）提供弹出对话框或集合编辑器，可通过点击属性值单元格中的省略号按钮打开。
7. **信息视图**：Tabular Editor 3 会持续分析你模型中的 DAX 表达式，查找语义错误。 任何此类错误都会在此处显示。 此外，此视图中显示的信息还可能来自 C# 脚本，或来自 Analysis Services 报告的错误消息。 任何此类错误都会在此处显示。 此外，此视图中显示的信息还可能来自 C# 脚本，或来自 Analysis Services 报告的错误消息。
8. **状态栏**：状态栏会提供与当前选择相关的各种上下文信息、Best Practice Analyzer 的检测结果等。

还提供一些其他视图，用于不同用途。 更多信息请查看 [视图菜单](#view) 一节。

# 自定义用户界面

所有 UI 元素都可以调整大小和/或重新排列，以满足你的需求。 你甚至可以将某个视图从主窗口拖出，从而把同一个 Tabular Editor 3 实例分布到多个显示器上。 关闭应用时，Tabular Editor 3 会保存这些自定义设置，并在下次启动时自动恢复。

<a name="choosing-a-different-layout"></a>

### 选择不同的布局

要将应用重置为默认布局，请选择 **窗口 > 默认布局**。 要将应用重置为默认布局，请选择 **窗口 > 默认布局**。 Tabular Editor 2.x 用户可能更喜欢 **窗口 > 经典布局** 选项：TOM Explorer 位于屏幕左侧，属性视图位于表达式编辑器下方。

使用 \*\*窗口 > 捕获当前布局...\" 选项保存自定义布局，使其在“窗口”菜单中作为新的布局选项可用，从而让你能够在不同布局之间快速切换。 使用 \*\*窗口 > 捕获当前布局...\" 选项保存自定义布局，使其在“窗口”菜单中作为新的布局选项可用，从而让你能够在不同布局之间快速切换。 使用 **窗口 > 管理布局...** 选项可打开所有可用布局的列表，你可以重命名、保存、删除布局等。 将布局保存到磁盘时，会生成一个 .xml 文件，你可以与其他 Tabular Editor 3 用户共享。 将布局保存到磁盘时，会生成一个 .xml 文件，你可以与其他 Tabular Editor 3 用户共享。

![管理布局](~/content/assets/images/manage-layouts.png)

<a name="changing-themes-and-palettes"></a>

### 窗口停靠选项

在 Tabular Editor 3 中重新排列视图和文档时，你可以选择将窗口停靠到界面的不同区域。 将窗口拖到新位置时，会出现停靠指示器，显示可用的停靠位置。

![窗口停靠选项](~/content/assets/images/window-docking-options.png)

停靠窗口主要有两种方式，各有不同用途：

**文档选项卡停靠（中心指示器）**：将窗口拖到中心停靠指示器时，它会被放置在主文档区域。 以这种方式停靠的窗口会成为文档选项卡，其特点包括： 以这种方式停靠的窗口会成为文档选项卡，其特点包括：

- 可使用 **Ctrl+Tab** 在选项卡之间切换
- 会在主工作区与 DAX 查询、脚本和图表等其他文档并排显示
- 不支持自动隐藏

**工具窗口停靠（边缘指示器）**：将窗口拖到左侧、右侧、顶部或底部的停靠指示器时，它会作为工具窗口停靠。 工具窗口： 工具窗口：

- 无法通过 **Ctrl+Tab** 访问
- 带有图钉图标，可用于启用自动隐藏（不使用时窗口会折叠）
- 其行为与 TOM Explorer 和信息视图等其他工具窗口类似
- 可停靠在主文档区域周围的不同位置

> [!TIP]
> 停靠窗口的大小取决于你选择停靠区域中的可用空间，而不是停靠选项本身。 你可以拖动窗口之间的分隔线来调整大小。 你可以拖动窗口之间的分隔线来调整大小。

### 更改主题和调色板

你可以通过选择不同的主题和/或调色板来更改 Tabular Editor 3 的外观。 Tabular Editor 3 内置五种不同的主题（有时也称为“皮肤”），可通过 **窗口 > 主题** 菜单选择： Tabular Editor 3 内置五种不同的主题（有时也称为“皮肤”），可通过 **窗口 > 主题** 菜单选择：

- Basic 与 Bezier（矢量主题，适用于高 DPI 显示器）
- Blue、Dark 与 Light（位图主题，不推荐用于高 DPI 显示器）

对于基于矢量的主题（Basic 和 Bezier），可以用 **窗口 > 调色板** 菜单项来更改主题使用的颜色。

![Palettes](~/content/assets/images/palettes.png)

<a name="menus"></a>

# 菜单

以下部分将更详细地介绍 Tabular Editor 3 中的各个菜单。

在下文中，我们使用 **活动文档** 一词，指光标位于某个文档中，例如表达式编辑器或下方截图中的“DAX 脚本 1”选项卡。 某些键盘快捷键和菜单项的行为会因是否存在活动文档，以及当前活动文档的类型而有所不同。 某些键盘快捷键和菜单项的行为会因是否存在活动文档，以及当前活动文档的类型而有所不同。

> [!NOTE]
> 默认情况下，菜单和工具栏会被锁定在原位，防止误操作导致重新定位。 要解锁它们，请转到 \*\*工具 > 自定义... 要解锁它们，请转到 **工具 > 自定义... > 选项**，并取消选中 **锁定菜单和工具栏** 选项

![Active Document](~/content/assets/images/active-document.png)

## 文件

**文件** 菜单主要包含用于加载和保存模型元数据，以及相关支持文件和文档的菜单项。

![File Menu](~/content/assets/images/file-menu.png)

- **新建**：打开一个子菜单，可创建新的空白数据模型 (Ctrl+N)，或创建各种 [支持文件](xref:supported-files#supported-file-types)，例如新的 DAX 查询或 DAX 脚本（文本文件），或数据模型图表（JSON 文件）。 支持文件（C# Script 除外）只能在 Tabular Editor 中已加载模型时创建。 支持文件（C# Script 除外）只能在 Tabular Editor 中已加载模型时创建。

  ![File Menu New](~/content/assets/images/file-menu-new.png)

> [!IMPORTANT]
> **新建 > 模型...** 选项在 Tabular Editor 3 桌面版中不可用，因为该版本只能作为 Power BI Desktop 的外部工具使用。 [更多信息](xref:editions)。 [更多信息](xref:editions)。

- **打开**：打开一个子菜单，提供从多种来源加载数据模型的选项，以及一个用于加载任何其他类型文件的选项。 子菜单项包括： 子菜单项包括：

  ![File Menu Open](~/content/assets/images/file-menu-open.png)

  - **从文件加载模型...** 从 .bim 或 .pbit 等文件打开模型元数据。
  - **从 DB 加载模型...** 指定 Analysis Services 或 Power BI XMLA 连接详细信息，或连接到本地 Analysis Services 实例（例如 Visual Studio 的集成 Workspace 服务器或 Power BI Desktop），以便从已部署的表格模型加载模型元数据。
  - **从文件夹加载模型...** 从文件夹结构中打开模型元数据，该结构此前使用任意版本的 Tabular Editor 保存。
  - **文件...** 会显示一个对话框，可根据文件扩展名打开 Tabular Editor 3 支持的任意类型文件。 更多信息，请参阅 [支持的文件类型](xref:supported-files)。 更多信息，请参阅 [支持的文件类型](xref:supported-files)。

    ![支持的文件类型](~/content/assets/images/supported-file-types.png)

> [!IMPORTANT]
> 在 Tabular Editor 3 桌面版中，**打开 > 从文件打开模型...** 和 **打开 > 从文件夹打开模型...** 选项不可用，并且 **打开 > 文件...** 对话框只允许打开[支持的文件](xref:supported-files#supported-file-types)，不允许打开包含元数据的文件。

- **还原**：此选项可让你从源重新加载模型元数据，并丢弃在 Tabular Editor 中所做但尚未保存的任何更改。 当 Tabular Editor 3 作为 Power BI Desktop 的外部工具使用，并且在 Tabular Editor 3 保持连接期间你在 Power BI Desktop 中进行了更改时，此选项非常有用。 **还原**：此选项可让你从源重新加载模型元数据，并丢弃在 Tabular Editor 中所做但尚未保存的任何更改。 当 Tabular Editor 3 作为 Power BI Desktop 的外部工具使用，并且在 Tabular Editor 3 保持连接期间你在 Power BI Desktop 中进行了更改时，此选项非常有用。 选择 **还原** 后，Tabular Editor 3 无需重新连接即可从 Power BI Desktop 重新加载模型元数据。
- **关闭文档** (Ctrl+W): 关闭主区域中当前处于活动状态的文档或面板，例如 DAX 查询、C# Script、Data model 图，或任何其他具有焦点的视图。 如果文档有未保存的更改，Tabular Editor 会在关闭前提示你保存这些更改。 此命令具有上下文感知能力，会关闭主 Workspace 区域中当前处于活动状态的项目。
- **关闭模型**：会从 Tabular Editor 中卸载当前加载的模型元数据。 如果你更改了元数据，Tabular Editor 会在关闭前提示你保存这些更改。 如果你更改了元数据，Tabular Editor 会在关闭前提示你保存这些更改。
- **保存**：此操作会将当前活动文档保存回源文件。 **保存**：此操作会将当前活动文档保存回源文件。 如果当前没有活动文档，此操作会将模型元数据保存回源；源可以是 Model.bim 文件、Database.json（文件夹结构），也可以是已连接的 Analysis Services 实例（包括 Power BI Desktop）或 Power BI XMLA endpoint。
- **另存为...**：允许你将活动文档另存为新文件。 **另存为...**：允许你将活动文档另存为新文件。 如果当前没有活动文档，此操作允许你将模型元数据另存为新文件，使用 .bim (基于 JSON) 文件。
- **保存到文件夹...**：允许你将模型元数据保存为[文件夹结构](xref:save-to-folder)。
- **全部保存**：一次性保存所有未保存的文档和模型元数据。
- **最近使用的文件**：显示最近使用的支持文件列表，便于你快速重新打开它们。
- **最近使用的表格模型**：显示最近使用的模型元数据文件或文件夹列表，便于你从其中之一快速重新加载模型元数据。

> [!IMPORTANT]
> 在 Tabular Editor 3 桌面版中，**保存到文件夹** 和 **最近使用的表格模型** 选项已禁用。 此外，**另存为** 选项仅对[支持的文件](xref:supported-files#supported-file-types)启用。 此外，**另存为** 选项仅对[支持的文件](xref:supported-files#supported-file-types)启用。

- **退出**：关闭 Tabular Editor 3 应用程序。 在应用程序关闭之前，系统会提示你保存所有未保存的文件或模型元数据。 在应用程序关闭之前，系统会提示你保存所有未保存的文件或模型元数据。

## 编辑

**编辑** 菜单包含标准的 Windows 应用程序菜单项，用于编辑文档或对当前加载的模型元数据进行更改。

![编辑菜单](~/content/assets/images/edit-menu.png)

- **撤销**：此选项将撤销对模型元数据所做的最后一次更改。 当没有活动文档时，常用的 CTRL+Z 快捷键会执行此选项。
- **重做**：这个选项会重新执行上一次对模型元数据的撤销操作。 当没有活动文档时，常用的 CTRL+Y 快捷键会执行此选项。
- **撤销输入**：撤销当前活动文档中的上一次文本更改。 当没有活动文档时，这个选项不可用。
- **撤销输入**：撤销当前活动文档中的上一次文本更改。 当没有活动文档时，这个选项不可用。 当没有活动文档时，这个选项不可用。
- **查找**：显示“查找和替换”对话框，并选中“查找”选项卡。 **查找**：显示“查找和替换”对话框，并选中“查找”选项卡。 [更多信息](xref:find-replace#find)。
- **替换**：显示“查找和替换”对话框，并选中“替换”选项卡。 **替换**：显示“查找和替换”对话框，并选中“替换”选项卡。 [更多信息](xref:find-replace#replace)。
- **剪切 / 复制 / 粘贴**：这些都是熟悉的 Windows 编辑操作。 如果有活动文档，这些操作将作用于该文档中的文本选区。 否则，可以使用这些选项来操作 TOM Explorer 中的对象。 例如，在 TOM Explorer 中选择度量值时按住 SHIFT 或 CTRL 键进行多选，然后按 CTRL+C，再按 CTRL+V，即可复制这些度量值。
- **删除**：删除活动文档中选定的文本；如果没有活动文档，则删除 TOM Explorer 中当前选定的一个或多个对象。

> [!NOTE]
> Tabular Editor 通常仅在选择了多个对象，或要删除的对象存在依赖关系时，才会弹出删除确认对话框。 对象删除可通过使用 **撤销** 选项 (CTRL+Z) 来撤销。 对象删除可通过使用 **撤销** 选项 (CTRL+Z) 来撤销。

- **全选**：选中当前活动文档中的所有文本，或选中 TOM Explorer 中属于同一父级的所有对象。
- **Code Assist**：此选项仅在编辑 DAX 代码时可用。 它提供了一个快捷入口，可访问多种与编辑 DAX 代码相关的 Code Assist 功能。 更多信息，请参阅 [DAX 编辑器](xref:dax-editor#code-assist-features)。 它提供了一个快捷入口，可访问多种与编辑 DAX 代码相关的 Code Assist 功能。 更多信息，请参阅 [DAX 编辑器](xref:dax-editor#code-assist-features)。

<a name="view"></a>

## 视图

**视图** 菜单可让你在 Tabular Editor 3 用户界面的不同视图之间导航。 如果某个视图已被隐藏，在此菜单中点击该视图的标题即可取消隐藏，并将其置于焦点。 注意，“视图”菜单中不会显示文档。 要在文档之间切换，请使用[窗口菜单](#window)。

![视图菜单](~/content/assets/images/view-menu.png)

- **TOM Explorer**: 以层次结构视图呈现当前加载的模型元数据的整个 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)。 更多信息请参见 @tom-explorer-view。 更多信息请参见 @tom-explorer-view。
- **Best Practice Analyzer**: 通过让你指定用于最佳实践验证的规则，帮助提升模型质量。 更多信息请参见 @bpa-view。 更多信息请参见 @bpa-view。
- **信息**: 信息视图显示来自各种来源的错误、警告和信息性消息，例如 Tabular Editor 3 语义分析器。 更多信息请参见 @messages-view。 更多信息请参见 @messages-view。
- **数据刷新**：数据刷新视图用于跟踪后台运行的数据刷新操作。 更多信息请参见 @data-refresh-view。 更多信息请参见 @data-refresh-view。
- **宏**: 宏视图允许你管理你创建的任何宏。 可通过 @csharp-scripts 创建宏。 更多信息请参见 @creating-macros。 可通过 @csharp-scripts 创建宏。 更多信息请参见 @creating-macros。
- **VertiPaq分析器**：VertiPaq分析器视图允许你收集、导入和导出有关模型数据的详细统计信息，用于优化和调试 DAX 性能。 VertiPaq分析器由 [SQLBI](https://sqlbi.com) 的 [Marco Russo](https://twitter.com/marcorus) 在 MIT 许可下创建并维护。 更多信息请参阅 [GitHub 项目页面](https://github.com/sql-bi/VertiPaq-Analyzer)。 VertiPaq分析器由 [SQLBI](https://sqlbi.com) 的 [Marco Russo](https://twitter.com/marcorus) 在 MIT 许可下创建并维护。 更多信息请参阅 [GitHub 项目页面](https://github.com/sql-bi/VertiPaq-Analyzer)。
- **表达式编辑器**：这是一个“快速编辑器”，可让你编辑 TOM Explorer 中当前选定对象的 DAX、M 或 SQL 表达式。 更多信息请参见 @dax-editor。 更多信息请参见 @dax-editor。

## 模型

**模型**菜单显示可在“模型”对象级别执行的操作（即 TOM Explorer 的根对象）。

![模型菜单](~/content/assets/images/model-menu.png)

- **Deploy...**: 启动 Tabular Editor 部署向导。 更多信息请参见 [模型部署](../deployment.md)。 更多信息请参见 [模型部署](../deployment.md)。

> [!IMPORTANT]
> **Deploy** 选项在 Tabular Editor 3 桌面版中不可用。 有关详细信息，请参阅 @editions。 有关详细信息，请参阅 @editions。

- **导入表...** 启动 Tabular Editor 3 导入表向导。 有关详细信息，请参阅 @importing-tables。 有关详细信息，请参阅 @importing-tables。
- **更新表架构...** 检测数据源(s)中当前选定的表(s)或分区(s)的架构更改，并与当前已导入的列进行比较。 有关详细信息，请参阅 @importing-tables#updating-table-schema。 有关详细信息，请参阅 @importing-tables#updating-table-schema。
- **Script DAX**: 为当前选定的对象生成 DAX 脚本(如果未选择任何对象，则为模型中的所有 DAX 对象生成 DAX 脚本)。 有关详细信息，请参阅 @dax-scripts。 有关详细信息，请参阅 @dax-scripts。
- **刷新模型**: 当 Tabular Editor 连接到 Analysis Services 实例时，此子菜单包含用于在模型级别启动后台刷新操作的选项。 此子菜单包含以下选项。 有关详细信息，请参阅 [刷新命令 (TMSL)](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request)。 此子菜单包含以下选项。 有关详细信息，请参阅 [刷新命令 (TMSL)](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request)。
  - **自动（模型）**：Analysis Services 将决定要刷新的对象（仅刷新不处于“Ready”状态的对象）。
  - **完全刷新（模型）**：Analysis Services 对模型执行完全刷新。
  - **计算（模型）**：Analysis Services 将对所有计算表格、计算列、计算组以及关系执行重新计算。 不会从数据源读取任何数据。 不会从数据源读取任何数据。
- **创建 [对象类型]**：**模型** 菜单中其余的快捷方式可用于创建新的模型子对象类型（表、数据源、透视等）。

## 工具

**工具** 菜单包含用于设置 Tabular Editor 3 偏好和自定义项的选项。

![视图菜单](~/content/assets/images/tools-menu.png)

- **自定义...** 启动 Tabular Editor 3 用户界面布局自定义对话框，可在其中创建新工具栏、重新排列并编辑菜单和工具栏按钮等。
- **偏好...** 启动 Tabular Editor 3 偏好对话框。它是管理 Tabular Editor 及其各项功能的中心入口，例如更新检查、代理设置、查询行数限制、请求超时等。 有关详细信息，请参阅 @preferences。 有关详细信息，请参阅 @preferences。

<a name="window"></a>

## 窗口

**窗口** 菜单提供用于管理和在应用程序的各种视图与文档之间导航的快捷方式（统称为 _窗口_）。 它还包含用于控制主题和调色板的菜单项，如[上文](#changing-themes-and-palettes)所述。 它还包含用于控制主题和调色板的菜单项，如[上文](#changing-themes-and-palettes)所述。

![查看菜单](~/content/assets/images/window-menu.png)

- **新建...**：此子菜单提供用于创建新[支持文件](xref:supported-files#supported-file-types)的快捷方式。 这里的选项与 **文件 > 新建** 下的选项完全相同。 这里的选项与 **文件 > 新建** 下的选项完全相同。

- **浮动**：将当前视图或文档从停靠状态解除，并在浮动窗口中显示。

- **固定选项卡**：固定一个选项卡。 选项卡固定后，会显示在文档选项卡的最左侧；在选项卡上右键单击时，还会提供仅关闭未固定选项卡的快捷操作。

  ![标签页上下文菜单](~/content/assets/images/tab-context-menu.png)

- **新建水平/垂直选项卡组**：此选项可将主文档区域划分为多个区域（即“选项卡组”），以便同时并排或上下显示多个文档。

- **关闭所有文档**：关闭所有文档选项卡。 如有未保存的更改，系统会提示你保存。 如有未保存的更改，系统会提示你保存。

- **重置窗口布局**：重置对主文档区域应用的所有自定义设置。

- **1..N [文档]**：此处列出前 10 个已打开的文档，方便你在它们之间导航。 你也可以使用 CTRL+Tab 快捷键在已打开的文档和视图之间快速切换，如下图所示：

  ![Ctrl+Tab 快捷键](~/content/assets/images/ctrl-tab.png)

- **窗口...**：打开一个对话框，列出所有已打开的文档，使你可以在它们之间切换或逐个关闭。

  ![窗口管理器](~/content/assets/images/windows-manager.png)

- **捕获当前布局** / **管理布局...** / **默认布局** / **经典布局**：这些菜单项已在[本文前面](#choosing-a-different-layout)讨论过。

- **主题** / **默认调色板**：这些菜单项已在[本文前面](#changing-themes-and-palettes)讨论过。

## 帮助

**帮助**菜单提供在线资源等内容的快捷入口。

![帮助菜单](~/content/assets/images/help-menu.png)

- **入门**：此菜单项链接到[这篇文章](xref:getting-started)。
- **Tabular Editor 3 文档**：此菜单项链接到 [docs.tabulareditor.com](https://docs.tabulareditor.com/te3)。
- **社区支持**：此菜单项链接到我们的[公开社区支持站点](https://github.com/TabularEditor/TabularEditor3)。
- **专属支持**：此菜单项可让你直接向我们的专属支持热线发送电子邮件。

> [!NOTE]
> 专属支持仅提供给 Tabular Editor 3 企业版客户。 其他客户如有任何技术问题、疑问或其他产品相关问题，请前往[公开社区支持站点](https://github.com/TabularEditor/TabularEditor3)寻求帮助。 其他客户如有任何技术问题、疑问或其他产品相关问题，请前往[公开社区支持站点](https://github.com/TabularEditor/TabularEditor3)寻求帮助。

- **关于 Tabular Editor**：打开一个对话框，显示当前使用的 Tabular Editor 版本的详细信息，以及安装与许可详情。 该对话框还允许你更改许可证密钥。 该对话框还允许你更改许可证密钥。

## 动态菜单（取决于上下文）

除了上面提到的菜单外，还可能在特定情况下出现其他菜单，具体取决于当前获得焦点的 UI 元素，以及在 TOM Explorer 中当前选中的对象。 例如，如果你选择一个 Table 对象，就会出现一个 **Table** 菜单，其中包含与在 TOM Explorer 中右键单击该对象时相同的、与上下文相关的快捷菜单项。 例如，如果你选择一个 Table 对象，就会出现一个 **Table** 菜单，其中包含与在 TOM Explorer 中右键单击该对象时相同的、与上下文相关的快捷菜单项。

如果你在不同类型的文档之间切换输入焦点（即。 如果你在不同类型的文档之间切换输入焦点（即。 DAX 查询、Pivot Grid、图表等），你也会看到一个表示当前处于焦点的文档类型的菜单。 该菜单将包含与当前文档相关的菜单项。 例如，当图表当前获得焦点时，会出现一个 **Diagram** 菜单，其中包含“将表添加到图表”等相关菜单项。 该菜单将包含与当前文档相关的菜单项。 例如，当图表当前获得焦点时，会出现一个 **Diagram** 菜单，其中包含“将表添加到图表”等相关菜单项。

你可以在 **工具 > 偏好 > 用户界面** 中更改这些动态菜单的行为。

# 后续步骤

- @tom-explorer-view
- @supported-files
- @preferences