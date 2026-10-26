---
uid: refresh-preview-query
title: 刷新、预览和查询数据
author: Daniel Otykier
updated: 2026-10-12
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
# 刷新、预览和查询数据

当 Tabular Editor 3 连接到 Analysis Services 实例时，将提供多项额外的**连接功能**，使你可以将 Tabular Editor 3 用作 Analysis Services 的客户端工具。

> [!NOTE]
> “连接到 Analysis Services 实例”一词是指以下任一情况：
> 
> - 在[**工作区模式**](xref:workspace-mode)下加载模型
> - 直接从 SQL Server Analysis Services、Azure Analysis Services 或 Power BI XMLA endpoint 加载模型
> - 将 Tabular Editor 3 用作 Power BI Desktop 的外部工具

总之，这些连接功能包括：

- 数据刷新操作
- 表格数据预览
- PivotGrid
- DAX 查询
- VertiPaq分析器

# 刷新数据

对数据模型进行更改时，Tabular Editor 不会在 Analysis Services 中自动触发刷新操作。这是设计使然，旨在确保将元数据更改保存到 Analysis Services 不会花费太长时间。刷新操作可能需要很长时间才能完成，在此期间，服务器上可能不会更新任何其他元数据。当然，这样做的缺点是，您可以使用 Tabular Editor 进行更改，这会导致模型进入只能部分查询或完全无法查询的状态。根据所进行的<em>数据模型更改</em>的类型，可能需要不同级别的刷新。

通常，在可以查询所述对象之前，以下更改需要进行完全刷新（即，先进行数据刷新，然后进行计算刷新）：

- 向模型添加新表
- 向表添加新列

通常，以下更改需要进行计算刷新：

- 更改计算表格或计算列的 DAX 表达式
- 添加或修改关系
- 向计算组添加、重命名或从中移除计算项

值得注意的是，在模型中添加、修改或删除度量值不需要进行任何类型的刷新（除非计算列引用了该度量值，在这种情况下，必须重新计算该列所在的表）。

要使用 Tabular Editor 启动刷新，只需右键单击您希望刷新的表格或分区，导航至**刷新表格**或**刷新分区**，然后选择您希望执行的刷新类型。

![刷新表格](~/content/assets/images/refresh-table.png)

您还可以通过“**模型 > 刷新模型**”菜单在模型层面发起刷新。刷新操作开始后，您将看到“数据刷新已开始… <ins>查看刷新队列</ins>”字样。点击该链接，或通过“视图”>“数据刷新”菜单选项找到“数据刷新”视图。这将显示所有刷新操作（包括过去和当前）的列表，显示 Analysis Services 返回的状态消息（包括进度计数器和持续时间），并允许您取消意外的刷新。

![数据刷新视图 2](~/content/assets/images/data-refresh-view2.png)

> [!TIP]
> “数据刷新”视图包含一个**开始时间**列，显示每个刷新操作的开始时间。点击列标题，按时间顺序对操作进行排序，以便轻松地首先查看最近的刷新操作。您可以按任何列进行排序，以根据您的需求来组织刷新操作。有关详细信息，请参阅[数据刷新视图](xref:data-refresh-view)。

在刷新进行期间，您可以根据本文所述继续处理数据模型、查询和预览数据，或将新的数据刷新操作排入队列。但是，在所有数据刷新操作完成之前，您将无法将模型更改保存到 Analysis Services。


## 支持的刷新操作

Tabular Editor 3 支持对不同对象类型执行刷新操作。支持的刷新类型如下所示：

- **模型**（自动、计算、完整）
- **（已导入）表**（自动、计算、仅数据、完整）
- **分区**（完全）
- **计算表格**（计算）
- **计算组**（计算）

有关 Analysis Services / Power BI 支持的刷新操作类型的更多信息，请参阅[刷新类型](https://docs.microsoft.com/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request)。

# 预览表格数据

在 DAX 编写和数据模型开发的某些阶段，您可能需要逐行检查表格的内容。当然，您可以编写 DAX 查询来实现此目的，但 Tabular Editor 3 通过允许您直接预览表数据，使此操作变得更加轻松。要执行此操作，请右键单击表，然后选择**预览数据**选项。

![预览数据](~/content/assets/images/preview-data-big.png)

您可以打开多个此类表预览，并在用户界面中以您喜欢的方式排列它们。Tabular Editor 对模型执行 DAX 查询，仅返回适合填充当前视图的少量记录，然后在你滚动时分页显示更多行。

每个列标题都包含一个排序和一个筛选器，网格的右键菜单可以打开计算列的表达式或重新计算表，而**显示实际 DAX 查询…**则会将预览背后的查询作为新的 DAX 查询文档提供给您。在 TOM Explorer 中选择一列，预览将滚动到该列。

请参阅 @table-preview，了解工具栏、右键菜单、在每种存储模式下可以滚动多远，以及控制列顺序和筛选器下拉列表的偏好设置。

# Pivot Grid

在模型中添加或编辑 DAX 度量值后，模型开发人员通常会测试这些度量值。传统上，这通常使用 Excel 或 Power BI 等客户端工具来完成。使用 Tabular Editor 3，您现在可以使用**数据透视网格**，其行为与 Excel 中著名的数据透视表非常相似。数据透视表让您可以快速创建模型中数据的汇总视图，从而让您能够在按各种列和层次结构进行筛选和切片时测试 DAX 度量的行为。

要创建新的 Pivot Grid，请使用**文件 > 新建 > Pivot Grid**选项。在此，您可以将度量值、列和层次结构从 TOM 资源管理器拖入网格，也可以使用**Pivot Grid > Show fields**菜单选项，显示一个弹出列表，其中包含所有可以拖入 Pivot Grid 的字段（请参阅下图）。

![显示字段数据透视](~/content/assets/images/show-fields-pivot.png)

将字段拖入 Pivot Grid 时，Tabular Editor 会生成 MDX 查询并将其发送到 Analysis Services，以显示结果数据。在这方面，其行为与 Excel 中的数据透视表非常相似。您可以通过拖放来重新排列Pivot Grid中的字段，并且有各种右键菜单选项可用于自定义数据的显示方式。

![自定义 Pivot Grid](~/content/assets/images/customizing-pivot-grids.png)

对模型进行更改或刷新操作完成后，Pivot Grid会自动刷新。您可以在**Pivot Grid**菜单中切换此自动刷新功能。

# DAX 查询

查询模型中数据的更直接方法是编写 DAX 查询。使用**文件 > 新建 > DAX 查询**菜单选项，创建新的 DAX 查询文档。您可以同时打开多个 DAX 查询文档。

可以使用 `.dax` 或 `.msdax` 文件扩展名将 DAX 查询保存到独立文件并从独立文件加载。有关详细信息，请参阅 @supported-files。

在编辑器中输入您的 DAX `EVALUATE` 查询，然后点击**查询 > 执行** (F5)，将查询发送到 Analysis Services 并查看结果。默认情况下，Tabular Editor 3 将从 Analysis Services 返回的行数限制为 1000 行，但您可以在**工具 > 首选项 > 数据浏览 > DAX 查询**下更改此设置。如果查询超过此限制，Tabular Editor 3 将显示一个快捷方式，让您检索所有记录（请参阅下图）。

![查询行集限制](~/content/assets/images/query-rowset-limit.png)

> [!WARNING]
> 在查询结果窗口中显示大量记录可能需要一段时间，并会大幅增加 Tabular Editor 3 占用的内存。

Tabular Editor 3 使用的查询编辑 DAX 代码编辑器与用于在对象上定义 DAX 表达式的编辑器相同。因此，所有与代码补全、自动格式化等相关的功能均可使用。有关详细信息，请参阅@dax-editor。此外，由于 DAX 查询的语法与对象表达式略有不同，因此 DAX 查询编辑器为常见任务提供了更多选项。

例如，如果您右键单击 Measure 引用，则有一个**定义 Measure**选项，如下图所示。此选项将在 DAX 查询的顶部添加一个 `DEFINE MEASURE` 语句，使您能够轻松地在查询范围内修改该度量的 DAX 表达式。

![DAX查询功能](~/content/assets/images/dax-query-features.png)

此外，DAX 查询可以包含多个 `EVALUATE` 语句。在这种情况下，Tabular Editor 3 会在单独的带编号选项卡上显示每个此类语句的结果。如果您只想执行单个 `EVALUATE` 语句（即使您的文档包含多个此类语句），您可以将光标放置在要执行的语句中的某个位置，然后使用**查询 > 执行选定内容**（SHIFT+F5）选项。

当对模型进行更改或刷新操作完成后，Tabular Editor 3 中的 DAX 查询会自动刷新。您可以在**查询**菜单中切换此自动刷新功能。

# 模拟

在查询模型中的数据时，有时能够模拟特定用户或角色组合非常有用，以便从最终用户的角度查看模型的行为。通过点击**模拟……**按钮，Tabular Editor 3 允许您模拟特定用户或一个或多个角色。这适用于[表预览](#previewing-table-data)、[数据透视表](#pivot-grids)和[DAX 查询](#dax-queries)。 

> [!NOTE]
> 为了模拟用户，Tabular Editor 在连接到 Analysis Services 时，会将 [`EffectiveUserName` 属性](https://docs.microsoft.com/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#effectiveusername)添加到连接字符串中。要模拟角色，Tabular Editor 会将[`Roles`属性](https://docs.microsoft.com/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#roles)添加到连接字符串中。这仅适用于指定了模拟的数据视图（即 DAX 查询、Pivot Grid 或表预览）。

单击**模拟身份..**按钮（也可以通过**查询**、**数据透视表**或**表预览**菜单找到，具体取决于哪种类型的数据视图处于活动状态）时，将弹出一个窗口，允许您指定一个用户，或选择一个或多个角色。

![选择模拟](~/content/assets/images/select-impersonation.png)

启用模拟后，**模拟..**按钮将被选中，模拟将应用于当前数据视图。通过点击“**模拟身份..**”按钮旁的小箭头，您可以查看并快速切换最近使用的 10 个模拟身份。

![模拟身份下拉菜单](~/content/assets/images/impersonation-dropdown.png)

在数据视图中启用自动刷新时，更改模拟将立即刷新视图。 

## CustomData

CustomData 功能允许您传递一个可用于 DAX 表达式的自定义字符串值，通常用于实现动态行级安全场景。此功能可与上述任何模拟选项（包括**无模拟**）结合使用。

![选择模拟](~/content/assets/images/impersonation-customdata.png)

当您在**CustomData**输入字段中输入值时，Tabular Editor 3 会将[`CustomData`属性](https://docs.microsoft.com/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#customdata)添加到连接字符串中。然后，您可以使用 [`CUSTOMDATA()` 函数](https://dax.guide/customdata/)在 DAX 表达式中检索此值。

当应用程序使用自定义身份验证时，CustomData 通常用于实现动态行级安全性。您提供的值可以在角色筛选器表达式中加以利用，以根据通过连接字符串传递的自定义数据控制用户可以查看哪些行。

此功能在**Power BI Embedded**场景中尤为有用，您可以在其中原生使用 CustomData 添加行筛选器，该筛选器传递自由文本（字符串），以便在嵌入式报表、仪表板和磁贴中利用动态行级安全性。

**示例用例：**您可以将用户的部门或区域作为 CustomData 传递，然后在角色的筛选器表达式中使用该值，例如：
```dax
'Department'[DepartmentCode] = CUSTOMDATA()
```   

# VertiPaq分析器

Tabular Editor 3 包含一个由 [SQLBI](https://www.sqlbi.com/tools/vertipaq-analyzer/) 创建的开源 [VertiPaq 分析器](https://sqlbi.com)工具版本。VertiPaq分析器对于分析您的 Power BI 或表格数据模型的 VertiPaq 存储结构非常有用。

使用 Tabular Editor 3，您可以在连接到任何 Analysis Services 实例时收集 VertiPaq 分析器统计信息。您还可以将统计信息导出为 [.vpax 文件](https://www.youtube.com/watch?v=zRa9y01Ub30)，或从 .vpax 文件导入统计信息。

要收集统计信息，只需点击**VertiPaq Analyzer**视图中的**收集统计信息**按钮即可。

如果无法从模型的数据中读取统计信息，例如当高基数列超过 Power BI 容量的每个查询内存限制时，则仅从模型元数据中收集统计信息。此时会显示“未读取数据即收集统计信息”警告以及服务器错误，且基数可能缺失或不准确。要跳过从数据读取统计信息，请在**工具 > 首选项 > 文件格式 > VertiPaq Analyzer**下取消选中**从数据读取统计信息**。

![Vertipaq Analyzer 收集统计信息](~/content/assets/images/vertipaq-analyzer-collect-stats.png)

收集统计信息后，VertiPaq Analyzer 将显示模型大小、表数等汇总信息。您可以在**表**、**列**、**关系**和**分区**选项卡中查看更详细的统计信息。

此外，每当加载统计信息时，将鼠标光标悬停在 TOM Explorer 中的对象上时，Tabular Editor 3 将以工具提示的形式显示基数和大小信息：

![TOM Explorer 中的 VertiPaq Analyzer 统计信息](~/content/assets/images/vertipaq-analyzer-stats.png)

……或者将鼠标光标悬停在 DAX 表达式中的对象引用上时：

![DAX 表达式中的 Vertipaq Analyzer 统计信息](~/content/assets/images/vertipaq-analyzer-stats-dax.png)

# 后续步骤

- @creating-and-testing-dax