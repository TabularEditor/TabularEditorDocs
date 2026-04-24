---
uid: refresh-preview-query
title: 刷新、预览与查询数据
author: Daniel Otykier
updated: 2026-01-08
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

# 刷新、预览与查询数据

当 Tabular Editor 3 连接到某个 Analysis Services 实例时，会提供一系列额外的**连接功能**，使你能够将 Tabular Editor 3 作为 Analysis Services 的客户端工具来使用。

> [!NOTE]
> “连接到某个 Analysis Services 实例”是指以下任意一种情况：
>
> - 在[**工作区模式**](xref:workspace-mode)中加载模型
> - 直接从 SQL Server Analysis Services、Azure Analysis Services 或 Power BI XMLA endpoint 加载模型
> - 将 Tabular Editor 3 用作 Power BI Desktop 的外部工具

总结一下，这些连接功能包括：

- 数据刷新操作
- 表数据预览
- PivotGrids
- DAX 查询
- VertiPaq分析器

<a name="refreshing-data"></a>

# 刷新数据

当对 Data model 进行更改时，Tabular Editor 不会在 Analysis Services 中自动触发刷新操作。 这是有意为之，以确保将元数据更改保存到 Analysis Services 时不会耗时过长。 刷新操作可能需要很长时间才能完成，在此期间，服务器上将无法更新任何其他元数据。 当然，这样做的缺点是：你可以使用 Tabular Editor 进行更改，从而让模型进入只能部分可查询、甚至完全无法查询的状态。 根据对 Data model 进行的更改类型，可能需要不同级别的刷新。 这是有意为之，以确保将元数据更改保存到 Analysis Services 时不会耗时过长。 刷新操作可能需要很长时间才能完成，在此期间，服务器上将无法更新任何其他元数据。 当然，这样做的缺点是：你可以使用 Tabular Editor 进行更改，从而让模型进入只能部分可查询、甚至完全无法查询的状态。 根据对 Data model 进行的更改类型，可能需要不同级别的刷新。

通常，在可以查询所述对象之前，以下更改需要执行一次完全刷新（即先进行数据刷新，再进行计算刷新）：

- 向模型添加新表
- 向表添加新列

通常，以下更改需要计算刷新：

- 更改计算表格或计算列的 DAX 表达式
- 添加或修改关系
- 在计算组中添加、重命名或删除计算项

需要指出的是，在模型中添加、修改或删除度量值不需要任何类型的刷新（除非该度量值被计算列引用；此时，包含该计算列的表必须重新计算）。

要在 Tabular Editor 中启动刷新，只需在要刷新的表或分区上右键单击，选择 **刷新表** 或 **刷新分区**，然后选择要执行的刷新类型。

![刷新表](~/content/assets/images/refresh-table.png)

你也可以通过 **模型 > 刷新模型** 菜单在模型级别启动刷新。 刷新操作开始后，你会看到文本“数据刷新已开始…… 刷新操作开始后，你会看到文本“数据刷新已开始…… <ins>查看刷新队列</ins>”。 单击该链接，或通过 **视图 > 数据刷新** 菜单选项打开 **数据刷新** 视图。 <ins>查看刷新队列</ins>”。 单击该链接，或通过 **视图 > 数据刷新** 菜单选项打开 **数据刷新** 视图。 这将显示所有刷新操作(历史和当前)的列表，显示 Analysis Services 返回的状态消息(包括进度计数器和持续时间)，并允许你取消非预期的刷新。

![数据刷新视图](~/content/assets/images/data-refresh-view2.png)

> [!TIP]
> 数据刷新视图包含一个 **开始时间** 列，用来显示每次刷新操作是什么时候开始的。 单击列标题即可按时间顺序对操作排序，方便你优先查看最新的刷新记录。 你也可以按任意列排序，以便根据需要整理刷新操作。 详情请参阅 [数据刷新视图](xref:data-refresh-view)。

在刷新进行期间，你可以继续处理你的 Data model，按本文所述继续查询和预览数据，或将新的数据刷新操作加入队列。 在刷新进行期间，你可以继续处理你的 Data model，按本文所述继续查询和预览数据，或将新的数据刷新操作加入队列。 不过，在所有数据刷新操作完成之前，你无法将模型更改保存到 Analysis Services。

## 支持的刷新操作

Tabular Editor 3 支持对不同对象类型执行刷新操作。 支持的刷新类型如下所示： 支持的刷新类型如下所示：

- **模型**（自动、计算、完全）
- **（导入）表**（自动、计算、仅数据、完全）
- **分区**（完全）
- **计算表格**（计算）
- **计算组**（计算）

想了解 Analysis Services / Power BI 支持的刷新操作类型，你可以查看 [刷新类型](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request)。

<a name="previewing-table-data"></a>

# 预览表格数据

在编写 DAX 和开发 Data model 的过程中，有时你可能需要逐行检查表中的内容。 在编写 DAX 和开发 Data model 的过程中，有时你可能需要逐行检查表中的内容。 当然，你也可以编写 DAX 查询来实现这一点；但 Tabular Editor 3 让这件事更简单，你可以直接预览表格数据。 要做到这一点，你可以右键单击某个表格，然后选择 **预览数据**。 要做到这一点，你可以右键单击某个表格，然后选择 **预览数据**。

![预览数据](~/content/assets/images/preview-data-big.png)

你可以打开多个此类表格预览，并在用户界面中按你的习惯随意排列。 此外，你还可以对单个列进行排序或筛选。 可预览的行数实际上没有限制。 Tabular Editor 只是在模型上执行一条 [`TOPNSKIP`](https://dax.guide/topnskip) DAX 查询，返回少量记录，用于填充当前视图。

如果一个或多个计算列处于无效状态，这些列会显示文本 _(需要计算)_。 你可以通过右键单击该列并选择 **重新计算表格...** 选项来重新计算表格。 你可以通过右键单击该列并选择 **重新计算表格...** 选项来重新计算表格。

![重新计算表格](~/content/assets/images/recalculate-table.png)

<a name="pivot-grids"></a>

# Pivot Grid：数据透视网格

在模型中新增或编辑 DAX 度量值后，你通常会想测试一下这些度量值。 传统上，这通常通过 Excel 或 Power BI 等客户端工具来完成。 借助 Tabular Editor 3，你现在可以使用 **Pivot Grid**，其使用方式与 Excel 中著名的数据透视表非常相似。 Pivot Grid 可让你快速创建模型数据的汇总视图，从而在按不同列与层级进行筛选和切片时，测试 DAX 度量值的行为。

要创建新的 Pivot Grid，请选择 **文件 > 新建 > Pivot Grid**。 要创建新的 Pivot Grid，请选择 **文件 > 新建 > Pivot Grid**。 接下来，你可以将度量值、列和层级从 TOM Explorer 拖入网格；也可以使用 **Pivot Grid > 显示字段** 菜单选项，显示一个弹出列表，其中列出了所有可拖入 Pivot Grid 的字段（见下图）。

![显示字段 Pivot](~/content/assets/images/show-fields-pivot.png)

当字段被拖入 Pivot Grid 时，Tabular Editor 会生成 MDX 查询并发送到 Analysis Services，以显示结果数据。 在这一点上，其行为与 Excel 中的数据透视表非常相似。 你可以通过拖拽重新排列 Pivot Grid 中的字段，并可通过右键菜单中的多种选项自定义数据的显示方式。 在这一点上，其行为与 Excel 中的数据透视表非常相似。 你可以通过拖拽重新排列 Pivot Grid 中的字段，并可通过右键菜单中的多种选项自定义数据的显示方式。

![自定义 Pivot Grid](~/content/assets/images/customizing-pivot-grids.png)

当模型发生更改或刷新操作完成时，Pivot Grid 会自动刷新。 你可以在 **Pivot Grid** 菜单中切换此自动刷新功能。 你可以在 **Pivot Grid** 菜单中切换此自动刷新功能。

<a name="dax-queries"></a>

# DAX 查询

查询模型数据更直接的方式是编写 DAX 查询。 你可以使用 **文件 > 新建 > DAX 查询** 菜单选项来创建新的 DAX 查询文档。 你可以同时打开多个 DAX 查询文档。 你可以使用 **文件 > 新建 > DAX 查询** 菜单选项来创建新的 DAX 查询文档。 你可以同时打开多个 DAX 查询文档。

DAX 查询可以使用 `.dax` 或 `.msdax` 文件扩展名保存到独立文件中，也可以从这些文件中加载。 更多信息请参阅 @supported-files。 更多信息请参阅 @supported-files。

在编辑器中输入 DAX `EVALUATE` 查询，然后点击 **查询 > 执行**（F5），即可将查询发送到 Analysis Services 并查看结果。 在编辑器中输入 DAX `EVALUATE` 查询，然后点击 **查询 > 执行**（F5），即可将查询发送到 Analysis Services 并查看结果。 默认情况下，Tabular Editor 3 会将 Analysis Services 返回的行数限制为 1000；但你可以在 **工具 > 偏好 > 数据浏览 > DAX 查询** 中更改此设置。 如果查询超过此限制，Tabular Editor 3 会显示一个快捷链接，方便你检索所有记录（见下方截图）。 如果查询超过此限制，Tabular Editor 3 会显示一个快捷链接，方便你检索所有记录（见下方截图）。

![查询行集限制](~/content/assets/images/query-rowset-limit.png)

> [!WARNING]
> 在查询结果窗口中显示大量记录可能需要一些时间，并会显著增加 Tabular Editor 3 的内存占用。

Tabular Editor 3 在编辑查询时使用与在对象上定义 DAX 表达式相同的 DAX 代码编辑器。 因此，代码补全、自动格式化等所有相关功能都可用。 更多信息请参阅 @dax-editor。 此外，由于 DAX 查询的语法与对象表达式略有不同，DAX 查询编辑器还为常见任务提供了一些额外选项。 因此，代码补全、自动格式化等所有相关功能都可用。 更多信息请参阅 @dax-editor。 此外，由于 DAX 查询的语法与对象表达式略有不同，DAX 查询编辑器还为常见任务提供了一些额外选项。

例如，如果你右键单击某个度量值引用，就会看到 **定义度量值** 选项，如下方截图所示。 例如，如果你右键单击某个度量值引用，就会看到 **定义度量值** 选项，如下方截图所示。 此选项会在 DAX 查询顶部添加一条 `DEFINE MEASURE` 语句，使你可以在查询作用域内轻松修改该度量值的 DAX 表达式。

![Dax 查询功能](~/content/assets/images/dax-query-features.png)

此外，一个 DAX 查询可以包含多个 `EVALUATE` 语句。 在这种情况下，Tabular Editor 3 会将每条语句的结果显示在单独的编号选项卡上。 此外，一个 DAX 查询可以包含多个 `EVALUATE` 语句。 在这种情况下，Tabular Editor 3 会将每条语句的结果显示在单独的编号选项卡上。 如果文档中包含多个 `EVALUATE` 语句，但你只想执行其中一条，可以将光标放在要执行的语句中的任意位置，然后使用 **查询 > 执行所选内容**（SHIFT+F5）。

Tabular Editor 3 中的 DAX 查询会在模型发生更改或刷新操作完成时自动刷新。 你可以在 **查询** 菜单中开启或关闭此自动刷新功能。 你可以在 **查询** 菜单中开启或关闭此自动刷新功能。

# 身份模拟

在查询模型中的数据时，有时需要模拟某个特定用户或一组角色，以便从最终用户的透视角度查看模型的行为表现。 Tabular Editor 3 支持点击 **模拟身份...** 按钮，来模拟特定用户或一个或多个角色。 这适用于 [表格预览](#previewing-table-data)、[Pivot Grid](#pivot-grids) 和 [DAX 查询](#dax-queries)。

> [!NOTE]
> 要模拟用户，Tabular Editor 在连接到 Analysis Services 时会将 [`EffectiveUserName` 属性](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#effectiveusername) 添加到连接字符串中。 为了模拟角色，Tabular Editor 会将 [`Roles` 属性](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#roles) 添加到连接字符串中。 这仅适用于指定了模拟身份的那个数据视图（即 DAX 查询、Pivot Grid 或表格预览）。 为了模拟角色，Tabular Editor 会将 [`Roles` 属性](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#roles) 添加到连接字符串中。 这仅适用于指定了模拟身份的那个数据视图（即 DAX 查询、Pivot Grid 或表格预览）。

点击 **模拟身份..** 按钮后（根据当前激活的数据视图类型，也可以在 **查询**、**Pivot Grid** 或 **表格预览** 菜单中找到），会弹出一个窗口，让你指定用户或选择一个或多个角色。

![选择模拟身份](~/content/assets/images/select-impersonation.png)

启用模拟身份后，**模拟身份..** 按钮将显示为已选中，并且该模拟身份会应用于当前数据视图。 点击 **模拟身份..** 按钮旁的小箭头，你可以查看并快速切换最近使用的 10 个模拟身份。

![模拟身份下拉列表](~/content/assets/images/impersonation-dropdown.png)

当某个数据视图启用了自动刷新时，更改模拟身份会立即刷新该视图。

## CustomData

CustomData 功能允许你传入一个自定义字符串值，可在 DAX 表达式中使用，通常用于实现动态行级安全性方案。 此功能可以与上文介绍的任何模拟选项结合使用，包括 **不进行模拟**。 此功能可以与上文介绍的任何模拟选项结合使用，包括 **不进行模拟**。

![选择模拟](~/content/assets/images/impersonation-customdata.png)

当你在 **CustomData** 输入框中输入值时，Tabular Editor 3 会将 [`CustomData` 属性](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#customdata) 添加到连接字符串中。 然后，你可以在 DAX 表达式中通过 [`CUSTOMDATA()` 函数](https://dax.guide/customdata/) 取回该值。 然后，你可以在 DAX 表达式中通过 [`CUSTOMDATA()` 函数](https://dax.guide/customdata/) 取回该值。

当应用使用自定义身份验证时，CustomData 常用于实现动态行级安全性。 你提供的值可用于角色筛选表达式，通过连接字符串传入的自定义数据来控制用户能够看到哪些行。 你提供的值可用于角色筛选表达式，通过连接字符串传入的自定义数据来控制用户能够看到哪些行。

此功能在 **Power BI Embedded** 场景中特别有用，你可以直接利用 CustomData 添加行筛选器，传入自由文本(字符串)，从而在嵌入式 Report、Dashboard 和 Tile 中实现动态行级安全性。

**示例用例：** 你可以将用户的部门或区域作为 CustomData 传入，然后在某个角色的筛选表达式中使用该值，例如：

```dax
'Department'[DepartmentCode] = CUSTOMDATA()
```

# VertiPaq分析器

Tabular Editor 3 内置了由 [SQLBI](https://sqlbi.com) 创建的开源工具 [VertiPaq分析器](https://www.sqlbi.com/tools/vertipaq-analyzer/) 的一个版本。 VertiPaq分析器可用于分析 Power BI 或 Tabular Data model 的 VertiPaq 存储结构。 VertiPaq分析器可用于分析 Power BI 或 Tabular Data model 的 VertiPaq 存储结构。

使用 Tabular Editor 3，只要你连接到任意 Analysis Services 实例，就可以收集 VertiPaq分析器统计信息。 你还可以将统计信息导出为 [.vpax 文件](https://www.youtube.com/watch?v=zRa9y01Ub30)，或从 .vpax 文件导入统计信息。 你还可以将统计信息导出为 [.vpax 文件](https://www.youtube.com/watch?v=zRa9y01Ub30)，或从 .vpax 文件导入统计信息。

要收集统计信息，只需在 **VertiPaq分析器** 视图中点击 **收集统计信息** 按钮。

![VertiPaq分析器收集统计信息](~/content/assets/images/vertipaq-analyzer-collect-stats.png)

收集完成后，VertiPaq分析器会显示模型大小、表数量等摘要信息。 你可以在 **表**、**列**、**关系** 和 **分区** 选项卡中查看更详细的统计信息。 你可以在 **表**、**列**、**关系** 和 **分区** 选项卡中查看更详细的统计信息。

此外，只要已加载统计信息，当鼠标悬停在 TOM Explorer 中的对象上时，Tabular Editor 3 就会以工具提示的形式显示基数和大小信息：

![TOM Explorer 中的 VertiPaq分析器统计信息](~/content/assets/images/vertipaq-analyzer-stats.png)

……或将鼠标指针悬停在 DAX 表达式中的对象引用上时：

![DAX 表达式中的 VertiPaq分析器统计信息](~/content/assets/images/vertipaq-analyzer-stats-dax.png)

# 后续步骤

- @creating-and-testing-dax