---
uid: pivot-grid
title: Pivot Grid
author: Daniel Otykier
updated: 2026-05-27
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

# Pivot Grid

> [!NOTE]
> 本文信息适用于 Tabular Editor 3.16.0 或更高版本。 Please make sure you are using the latest version of Tabular Editor 3 to take advantage of the new features and improvements.

在开发语义模型时，你经常需要测试 DAX 表达式是否返回了预期值。 Traditionally, this was done using client tools such as Excel or Power BI. With Tabular Editor 3, you can use **Pivot Grids** which behave much like the widely known PivotTables in Excel. The Pivot Grid lets you quickly create summarized views of the data in your model, allowing you to test the behavior of your DAX measures when filtering and slicing by various columns and hierarchies.

![Pivot Grid 示例](~/content/assets/images/pivot-grid-example.png)

The screenshot above shows a Pivot Grid containing two measures, `[Total Net Order Value]` and `[Net Orders]`, which is sliced horizontally by Year, filtered to 2021 and 2022, and vertically by the Product Hierarchy. Tabular Editor 3 users can use this feature to ensure that DAX expressions behind the measures are working as expected and to quickly validate the data in the model.

By default, the Pivot Grid auto-updates every time you save changes to the semantic model (Ctrl+S). Thus, you can quickly iterate on your DAX expressions and see the results in the Pivot Grid without having to wait for the model to refresh by changing your measures, saving the model, and directly seeing the new measure definition reflected in the Pivot Grid. A good workflow is to open the Pivot Grid in a separate window while working on DAX expressions in the **Expression Editor** or using a **DAX Script**.

> [!TIP]
> 关于术语的一些说明：
>
> - **Fields** 指模型度量值、KPI、列和层级。 In other words, anything that can be dragged into the Pivot Grid.
> - **KPIs** 是一种特殊的度量值类型，可在 Tabular Editor 中创建。 They are displayed in the Pivot Grid just like measures, but with a special icon to indicate that they are KPIs. Each KPI can have up to 3 different values (target, trend, and status), which are displayed separately in the Pivot Grid.
> - Pivot Grid 中的**列**（例如术语“Column Area”中的列）不要与模型中的列混为一谈。 In the Pivot Grid, columns are used to slice the data horizontally, while rows are used to slice the data vertically.
> - **Cells** in the Pivot Grid are the individual data points where a row and a column intersect. 每个单元格仅包含一个值。该值是在由 _Row Area_ 和 _Column Area_ 中的值所产生的筛选语境下，并结合对 _Filter Area_ 中各字段应用的任何筛选条件，对特定度量值的 DAX 表达式求值得到的结果。

> [!NOTE]
> Developers with a multidimensional background may be more familiar with the terms _Dimensions_ and _Attributes_. 在语义模型中，_Dimensions_ 由模型表表示，而 _Attributes_ 由模型列表示。 _Hierarchies_ in a semantic model, is just a way to group columns together, such as in a calendar hierarchy: Year > Quarter > Month > Day. Such hierarchies used to be called _Attribute Hierarchies_ or _User-Defined Hierarchies_ in multidimensional models.

## 创建 Pivot Grid

你可以通过菜单选项 **File > New > New Pivot Grid** 创建一个新的空 Pivot Grid。 Alternatively, select one or more measures in the **TOM Explorer**, right-click or go to the **Measure** menu and select **Add to Pivot Grid**, to create a new Pivot Grid with the selected measures.

![从 TOM Explorer 创建 Pivot Grid](~/content/assets/images/create-pivot-grid-from-TOM-Explorer.png)

你可以按需创建任意数量的 Pivot Grid。

> [!IMPORTANT]
> 仅当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI / Fabric XMLA endpoint 时，才能创建 Pivot Grid。

## Pivot Grid 布局

Pivot Grid 分为 4 个区域：**Filter Area**、**Column Area**、**Row Area** 和 **Data Area**。 You can drag fields from the **Field List** or the **TOM Explorer** into these areas to create a Pivot Grid layout. The **Data Area** area is where you place measures or KPIs, while the **Row Area** and **Column Area** are used to slice the data by hierarchies and columns. The **Filter Area** is used to filter the data based on values in columns or hierarchies.

![突出显示的空 Pivot Grid](~/content/assets/images/empty-pivot-grid-highlighted.png)

The screenshot above shows an empty Pivot Grid layout. The 4 empty boxes at the bottom of the Field List represent the 4 areas of the Pivot Grid. 你可以将字段从字段列表拖到这些列表框中，以创建 Pivot Grid 的布局。 Alternatively, you can drag fields directly into the Pivot Grid.

## Pivot Grid 菜单和工具栏

默认情况下，在 Tabular Editor 3 中，只要 Pivot Grid 是活动窗口，就会显示 **Pivot Grid** 菜单和工具栏。 The menu contains the same actions as the toolbar.

![Pivot Grid 工具栏](~/content/assets/images/pivot-grid-toolbar.png)

![Pivot Grid 菜单](~/content/assets/images/pivot-grid-menu.png)

这些操作包括：

- **Impersonation...**: Displays a dialog that allows you to specify a role or user to impersonate through the Pivot Grid. This is useful when you want to test the behavior of your model for different users or roles, such as when [RLS or OLS](xref:data-security-about) has been applied to the model.
- **刷新**：重新执行 Pivot Grid 生成的查询。 This is useful when auto-refresh is disabled, or if changes have been made to the model outside of Tabular Editor 3.
- **Auto Refresh**: Toggles auto-refresh on or off. 启用自动刷新后，每次保存对模型的更改，或当某个 [数据刷新操作](xref:data-refresh-view) 完成时，Pivot Grid 都会自动刷新。
- **清除筛选器**：清除 Pivot Grid 中的所有筛选器。
- **清除**：从 Pivot Grid 中移除所有字段。
- **在列中显示空值**：切换是否在 Pivot Grid 中显示空值，适用于添加到 Pivot Grid 列区域的字段。
- **在行中显示空值**：切换是否在 Pivot Grid 中显示空值，适用于添加到 Pivot Grid 行区域的字段。
- **字段列表**：切换字段列表显示/隐藏。

## 字段列表

By default, the Field List is displayed on the right side of the Pivot Grid. The Field List contains all the fields (measures, KPIs, columns, and hierarchies) that are available in the model. You can drag fields from the Field List into the Pivot Grid to create a layout. You can also drag fields between the different areas of the Pivot Grid to rearrange the layout.

The Field List itself can be docked to the left or right side of the Pivot Grid, above or below, it can be hidden, or it can be undocked so that it "floats" as a separate window. 如果你同时打开了多个 Pivot Grid，每个 Pivot Grid 都有自己的字段列表。

如果你希望默认不显示字段列表，请在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 字段列表** 下取消勾选 **始终显示字段列表** 选项。

你可以在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 字段列表 > 布局** 中更改字段列表的默认布局。 You can also change the layout of any field lists, by right-clicking in an empty area of the Field List and choosing the desired layout from the context menu.

![字段列表设置](~/content/assets/images/field-list-settings.png)

By default, any field you add to the Pivot Grid remains visible in the Field List. 如果你希望隐藏已添加到 Pivot Grid 的字段，可以在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 字段列表** 下取消勾选 **保持字段可见** 选项（此行为与 Tabular Editor v. 3.16.0 之前的 Pivot Grid 类似）。

如果你正在处理大型复杂模型，并且预计 Pivot Grid 中用到的度量值计算会比较慢，你可以勾选字段列表底部的 **延迟更新布局** 选项。 This will prevent the Pivot Grid from updating the layout every time you add or remove a field, which can be useful, if you intend to make multiple changes to the Pivot Grid layout before updating it. Hit the **Update** button to apply the changes to the Pivot Grid.

> [!IMPORTANT]
> 没有属性层次结构（IsAvailableIn MDX = false）的列无法在 Pivot Grid 中使用，也不会显示在字段列表中。

## 自定义 Pivot Grid

### 添加字段

将字段添加到 Pivot Grid 有多种方式：

**从 TOM Explorer：**

- 右键单击一个或多个 _度量值_，然后选择 **添加到 Pivot Grid**。
- 右键单击 _列_ 或 _层次结构_，然后选择任一 **Add to pivot** 选项（可选择添加到行、列或筛选器）。
- 如果某个度量值、列或层次结构已经显示在 Pivot Grid 中，右键选项会允许你 **从 Pivot Grid 中移除**。 in addition, you will see options to move columns or hierarchies between the different areas of the Pivot Grid.
- 当你在 TOM Explorer 中选择了一个或多个此类对象时，上述所有选项也可以分别在 **度量值**、**列** 和 **层次结构** 菜单(分别)中找到。
- 除了以上方式，你还可以将一个或多个度量值、列或层次结构从 TOM Explorer 拖放到 Pivot Grid 的各个区域。

![通过 TOM Explorer 将层次结构添加到 Pivot Grid](~/content/assets/images/add-through-tom-explorer.png)

**从字段列表中：**

- 将字段从字段列表拖放到 Pivot Grid。
- 将字段从字段列表拖放到字段列表底部的各个区域列表框中，即可将其添加到 Pivot Grid。
- 在“字段列表”中右键单击某个字段，即可看到将其添加到 Pivot Grid 的选项。
- 如果某个字段已显示在 Pivot Grid 中，右键上下文菜单还会提供移除该字段的选项，或将其移动到其他区域（仅列/层级字段）。
- Double-clicking on a field will immediately add it to the Pivot Grid. 度量值/KPI 会添加到“数据区域”，而列和层级字段会添加到“筛选区域”。

![通过字段列表添加](~/content/assets/images/add-through-field-list.png)

### 调整字段

将字段添加到 Pivot Grid 后，你可以调整列宽，让内容显示得更合适。 Double-clicking on a column header separator will automatically adjust the column width to fit the content of the column. You can also drag the column header separator to manually adjust the column width. Lastly, you can use the **Best Fit** or **Set width...** context menu options by right-clicking on the column header.

![最佳适应列 2](~/content/assets/images/best-fit-columns-2.png)

要同时对 Pivot Grid 中的所有列应用“最佳适应”，或为所有列设置特定的像素宽度，请在“值”标题上右键单击，然后在上下文菜单中选择所需选项。

By default, field headers will expand vertically to fit the content of the field name. 如果你想把字段标题的高度限制为一行，可以在 **工具 > 偏好 > Pivot Grid > 字段标题** 中禁用 **字段标题自动换行** 选项。

要更改 Pivot Grid 中字段的顺序，你可以在 Pivot Grid 的不同区域之间拖动字段。 You can also drag fields within the same area to change their order. To remove a field from the Pivot Grid, drag it back to the Field List or right-click on the field and choose **Remove from Pivot Grid** from the context menu.

如果你想让度量值显示在行上而不是列上，把“值”字段从“列区域”拖到“行区域”即可。

### 可视化规则

你可以为 Pivot Grid 中的单元格添加可视化规则，这有助于根据数值突出显示单元格，例如更容易发现异常值。 To add visualization rules, right-click on any Data Area cell in the Pivot Grid, and choose which rules to apply from the context menu (see screenshot below).

![自定义 Pivot Grid](~/content/assets/images/customizing-pivot-grids.png)

## 保存 Pivot Grid 布局

当你关闭 Pivot Grid 时，Tabular Editor 会提示你保存 Pivot Grid 的布局。 If you choose to save the layout, the next time you open the Pivot Grid, it will be restored to the same layout as when you closed it. You can also save the layout of a Pivot Grid manually by hitting (Ctrl+S) or using the **File > Save** option, while the Pivot Grid is the active window.

The file extension used for saving Pivot Grid layouts is `.te3pivot`. 这是一个简单的 json 文件，用于指定 Pivot Grid 中显示哪些模型对象，以及它们放置在哪些区域。 Objects are referenced by name and lineage tag (if present), so the Pivot Grid layout can generally be restored even if the model has been modified since the layout was saved.

> [!NOTE]
> 你可以打开在其他模型中创建的 Pivot Grid 布局，不过要注意：该布局中的字段可能在你当前连接的模型中并不存在。 In such cases, the Pivot Grid will show a warning message, and any fields that do not exist in the model will be removed from the layout. The warning message may be toggled off under **Tools > Preferences > Data Browsing > Pivot Grid > Show warning if Pivot Grid doesn't match model**.

## 其他功能

Pivot Grid 还有一些值得了解的功能：

- If you right-click on a field, you will have the option to **Go to** that field. This brings the TOM Explorer into focus, with the equivalent model object selected. For measures and calculated columns, the **Expression Editor** will be brought into focus, with the DAX expression of the measure displayed.
- If you right-click on a cell in the Pivot Grid, you can select the option to **Debug this value**. 这将启动 [**DAX Debugger**](xref:dax-debugger)，并以生成该单元格值的特定度量值和筛选语境为起点进行调试。
- 当 Pivot Grid 正在 **刷新** 时，某些工具栏项会被禁用，上下文菜单操作也会暂时不可用。

## 限制与已知问题

下面列出了 Tabular Editor 3.16.0 中 Pivot Grid 的已知限制与问题，我们正在努力在后续版本中解决：

- Format rules (such as icon sets, data bars, etc.) 在将 Pivot Grid 布局保存为 `.te3pivot` 文件时，这些规则无法被正确保留。
- 如果你在与保存布局时不同的模型上打开 `.te3pivot` 文件，当前模型中不存在的字段会从布局中移除。 Hitting Save (Ctrl+S) will save the layout with the removed fields removed. We may change this behavior in a future release so that the .te3pivot file is not overwritten without explicit confirmation.
- Columns that use the **Group By Columns** property (including field parameter columns) cannot be added to the Row Area or Column Area on their own. Doing so produces the error _"Column X is part of a composite key, but not all columns of the composite key are included in the expression or its dependent expression"_. This is a general limitation of MDX clients and also occurs when using such a column in an Excel PivotTable. 为绕过此问题，请在添加依赖列之前，先将相关的 Group By Column 添加到 Pivot Grid，然后再添加依赖列。 For example, if `[ProductKey]` is configured as the Group By Column of `[ProductName]`, add `[ProductKey]` to the Row Area or Column Area first, then add `[ProductName]`.
- Applying an explicit ascending or descending sort to a column in the Row Area or Column Area sorts values alphabetically as strings, regardless of the column data type. Dates formatted as long date (for example "May 4, 2024") and integers are sorted lexicographically rather than chronologically or numerically. This is a limitation of how MDX clients sort and the same behavior occurs in an Excel PivotTable connected to the model. To get chronological or numerical ordering, rely on the column's natural sort (do not apply an explicit sort) or use the **Sort By Column** property on the model column to point at a column with a sortable underlying value.