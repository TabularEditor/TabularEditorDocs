---
uid: refresh-preview-query
title: 刷新、预览与查询数据
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

# 刷新数据

当对 Data model 进行更改时，Tabular Editor 不会在 Analysis Services 中自动触发刷新操作。 This is by design, to ensure that saving metadata changes to Analysis Services does not take too long. Potentially, a refresh operation can take a long time to complete, during which no additional metadata may be updated on the server. Of course, the drawback of this, is that you can make changes using Tabular Editor, which causes the model to enter a state where it is only partly queryable or not queryable at all. Depending on what type of data model change was made, different levels of refresh may be needed.

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

你也可以通过 **模型 > 刷新模型** 菜单在模型级别启动刷新。 Once the refresh operation starts, you will see the text "Data refresh started... <ins>View refresh queue</ins>". Click on the link or locate the **Data refresh** view through the **View > Data refresh** menu option. 这将显示所有刷新操作(历史和当前)的列表，显示 Analysis Services 返回的状态消息(包括进度计数器和持续时间)，并允许你取消非预期的刷新。

![数据刷新视图](~/content/assets/images/data-refresh-view2.png)

> [!TIP]
> 数据刷新视图包含一个 **开始时间** 列，用来显示每次刷新操作是什么时候开始的。 Click the column header to sort operations chronologically, making it easy to see your most recent refreshes first. You can sort by any column to organize refresh operations according to your needs. See [Data Refresh view](xref:data-refresh-view) for more details.

While a refresh is in progress you can continue work on your data model, querying and previewing data or queueing new data refresh operations according to this article. 不过，在所有数据刷新操作完成之前，你无法将模型更改保存到 Analysis Services。

## 支持的刷新操作

Tabular Editor 3 支持对不同对象类型执行刷新操作。 The supported refresh types are shown below:

- **模型**（自动、计算、完全）
- **（导入）表**（自动、计算、仅数据、完全）
- **分区**（完全）
- **计算表格**（计算）
- **计算组**（计算）

想了解 Analysis Services / Power BI 支持的刷新操作类型，你可以查看 [刷新类型](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request)。

# 预览表格数据

At certain points during DAX authoring and data model development, you may need to inspect the contents of your tables on a row-by-row basis. 当然，你也可以编写 DAX 查询来实现这一点；但 Tabular Editor 3 让这件事更简单，你可以直接预览表格数据。 To do this, right-click on a table and choose the **Preview data** option.

![预览数据](~/content/assets/images/preview-data-big.png)

You can open multiple such table previews and arrange them anyway you like in the user interface. Tabular Editor executes a DAX query against the model to return just a small number of records suitable to fill the current view, then pages in more rows as you scroll.

Each column header carries a sort and a filter, the grid's right-click menu can open a calculated column's expression or recalculate the table, and **Show actual DAX query...** hands you the query behind the preview as a new DAX query document. Selecting a column in the TOM Explorer scrolls the preview to it.

See @table-preview for the toolbar, the right-click menu, how far you can scroll in each storage mode and the preferences that govern column order and the filter dropdown.

# Pivot Grid

After adding or editing DAX measures in a model, it is common for model developers to test these measures. Traditionally, this was typically done using client tools such as Excel or Power BI. With Tabular Editor 3, you can now use **Pivot Grids** which behave much like the famous PivotTables of Excel. The Pivot Grid lets you quickly create summarized views of the data in your model, allowing you test the behavior of your DAX measures when filtering and slicing by various columns and hierarchies.

To create a new Pivot Grid, use the **File > New > Pivot Grid** option. 接下来，你可以将度量值、列和层级从 TOM Explorer 拖入网格；也可以使用 **Pivot Grid > 显示字段** 菜单选项，显示一个弹出列表，其中列出了所有可拖入 Pivot Grid 的字段（见下图）。

![显示字段 Pivot](~/content/assets/images/show-fields-pivot.png)

当字段被拖入 Pivot Grid 时，Tabular Editor 会生成 MDX 查询并发送到 Analysis Services，以显示结果数据。 In this regard, the behavior is very similar to Pivot Tables in Excel. You can rearrange fields in the Pivot Grid by dragging and dropping, and there are various right-click menu options available for customizing how the data is displayed.

![自定义 Pivot Grid](~/content/assets/images/customizing-pivot-grids.png)

当模型发生更改或刷新操作完成时，Pivot Grid 会自动刷新。 You can toggle this auto-refresh capability within the **Pivot Grid** menu.

# DAX 查询

查询模型数据更直接的方式是编写 DAX 查询。 Use the **File > New > DAX Query** menu option to create a new DAX query document. You can have multiple DAX query documents open at the same time.

DAX 查询可以使用 `.dax` 或 `.msdax` 文件扩展名保存到独立文件中，也可以从这些文件中加载。 See @supported-files for more information.

Type your DAX `EVALUATE` query into the editor and hit **Query > Execute** (F5) to send the query to Analysis Services and see the result. 默认情况下，Tabular Editor 3 会将 Analysis Services 返回的行数限制为 1000；但你可以在 **工具 > 偏好 > 数据浏览 > DAX 查询** 中更改此设置。 If a query exceeds this limit, Tabular Editor 3 displays a shortcut that lets you retrieve all records (see screenshot below).

![查询行集限制](~/content/assets/images/query-rowset-limit.png)

> [!WARNING]
> 在查询结果窗口中显示大量记录可能需要一些时间，并会显著增加 Tabular Editor 3 的内存占用。

Tabular Editor 3 在编辑查询时使用与在对象上定义 DAX 表达式相同的 DAX 代码编辑器。 As such, all the features regarding code-completion, auto-formatting, etc. are available. See @dax-editor for more information. In addition, since a DAX query has a slightly different syntax than object expressions, the DAX query editor provides a few more options for common tasks.

For example, if you right-click on a measure reference, there is an option to **Define measure** as seen on the screenshot below. 此选项会在 DAX 查询顶部添加一条 `DEFINE MEASURE` 语句，使你可以在查询作用域内轻松修改该度量值的 DAX 表达式。

![Dax 查询功能](~/content/assets/images/dax-query-features.png)

In addition, a DAX query can contain multiple `EVALUATE` statements. When that is the case, Tabular Editor 3 displays the result from each such statement on a separate, numbered tab. 如果文档中包含多个 `EVALUATE` 语句，但你只想执行其中一条，可以将光标放在要执行的语句中的任意位置，然后使用 **查询 > 执行所选内容**（SHIFT+F5）。

Tabular Editor 3 中的 DAX 查询会在模型发生更改或刷新操作完成时自动刷新。 You can toggle this auto-refresh capability within the **Query** menu.

# Impersonation

When querying the data in the model, it is sometimes useful to be able to impersonate a specific user or a combination of roles, to see what the behavior of the model from an end user perspective would be. Tabular Editor 3 allows you to impersonate a specific user or one or more roles, by clicking on the **Impersonate...** button. This applies to [Table previews](#previewing-table-data), [Pivot Grids](#pivot-grids) and [DAX queries](#dax-queries).

> [!NOTE]
> 要模拟用户，Tabular Editor 在连接到 Analysis Services 时会将 [`EffectiveUserName` 属性](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#effectiveusername) 添加到连接字符串中。 To impersonate a role, Tabular Editor adds the [`Roles` property](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#roles) to the connection string. This only applies to the data view (i.e. the DAX query, the Pivot Grid or the Table Preview) where the impersonation is specified.

点击 **模拟身份..** 按钮后（根据当前激活的数据视图类型，也可以在 **查询**、**Pivot Grid** 或 **表格预览** 菜单中找到），会弹出一个窗口，让你指定用户或选择一个或多个角色。

![选择模拟身份](~/content/assets/images/select-impersonation.png)

Once the impersonation is enabled, the **Impersonation..** button is checked, and the impersonation will be applied to the current data view. By clicking on the small arrow next to the **Impersonation..** button, you can view and quickly switch between the 10 most recent impersonations used.

![模拟身份下拉列表](~/content/assets/images/impersonation-dropdown.png)

当某个数据视图启用了自动刷新时，更改模拟身份会立即刷新该视图。

## CustomData

CustomData 功能允许你传入一个自定义字符串值，可在 DAX 表达式中使用，通常用于实现动态行级安全性方案。 This feature can be combined with any of the impersonation options described above, including **No Impersonation**.

![选择模拟](~/content/assets/images/impersonation-customdata.png)

当你在 **CustomData** 输入框中输入值时，Tabular Editor 3 会将 [`CustomData` 属性](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#customdata) 添加到连接字符串中。 This value can then be retrieved within your DAX expressions using the [`CUSTOMDATA()` function](https://dax.guide/customdata/).

当应用使用自定义身份验证时，CustomData 常用于实现动态行级安全性。 The value you provide can be leveraged in role filter expressions to control which rows users can see based on the custom data passed through the connection string.

此功能在 **Power BI Embedded** 场景中特别有用，你可以直接利用 CustomData 添加行筛选器，传入自由文本(字符串)，从而在嵌入式 Report、Dashboard 和 Tile 中实现动态行级安全性。

**示例用例：** 你可以将用户的部门或区域作为 CustomData 传入，然后在某个角色的筛选表达式中使用该值，例如：

```dax
'Department'[DepartmentCode] = CUSTOMDATA()
```

# VertiPaq分析器

Tabular Editor 3 内置了由 [SQLBI](https://sqlbi.com) 创建的开源工具 [VertiPaq分析器](https://www.sqlbi.com/tools/vertipaq-analyzer/) 的一个版本。 VertiPaq Analyzer is useful to analyze VertiPaq storage structures for your Power BI or Tabular data model.

使用 Tabular Editor 3，只要你连接到任意 Analysis Services 实例，就可以收集 VertiPaq分析器统计信息。 You can also export the statistics as a [.vpax file](https://www.youtube.com/watch?v=zRa9y01Ub30), or import statistics from a .vpax file.

要收集统计信息，只需在 **VertiPaq分析器** 视图中点击 **收集统计信息** 按钮。

![VertiPaq分析器收集统计信息](~/content/assets/images/vertipaq-analyzer-collect-stats.png)

收集完成后，VertiPaq分析器会显示模型大小、表数量等摘要信息。 You can find more detailed statistics on the **Tables**, **Columns**, **Relationships** and **Partitions** tabs.

此外，只要已加载统计信息，当鼠标悬停在 TOM Explorer 中的对象上时，Tabular Editor 3 就会以工具提示的形式显示基数和大小信息：

![TOM Explorer 中的 VertiPaq分析器统计信息](~/content/assets/images/vertipaq-analyzer-stats.png)

……或将鼠标指针悬停在 DAX 表达式中的对象引用上时：

![DAX 表达式中的 VertiPaq分析器统计信息](~/content/assets/images/vertipaq-analyzer-stats-dax.png)

# 后续步骤

- @creating-and-testing-dax