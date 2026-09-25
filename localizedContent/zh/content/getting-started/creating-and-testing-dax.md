---
uid: creating-and-testing-dax
title: 添加度量值和其他计算对象
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

# 添加度量值和其他计算对象

自 2017 年初发布 Tabular Editor 2.x 以来，能够在多个度量值上快速修改 DAX 表达式一直是该工具最受欢迎的功能。 Combined with back and forward navigation, copy/paste operations, DAX dependency visualisation and undo/redo support, the tool has always been the preferred option for anyone working with large and complex data models, where the ability to quickly make multiple smaller changes is crucial.

Tabular Editor 2.x 用户在这方面唯一的抱怨，是缺少 DAX Code Assist 功能（有时也称为“IntelliSense”）。 Especially when you are not a 100% proficient with DAX (and very few people are!), having the DAX code editor assist you in remembering syntax, function parameters, etc. is incredibly helpful.

Tabular Editor 3 使用的新 DAX 代码编辑器已将这些问题全部解决。

![编辑复杂的 DAX 表达式](~/content/assets/images/dax-editor-screenshot.png)

本文其余部分将介绍如何创建度量值和其他计算对象，以及如何修改这些对象上的 DAX 表达式。 To learn more about the many features of the DAX code editor, see <xref:dax-editor>.

# 添加度量值

当你已将[一些表导入](xref:importing-tables-data-modeling#importing-new-tables)模型，并[在它们之间创建了关系](xref:importing-tables-data-modeling#modifying-relationships-using-the-diagram)之后，就该添加一些包含业务逻辑的显式度量值了。

> [!TIP]
> Technically, you are not required to add explicit measures to your model before visualizing data in a Power BI report. However, it is a best practice to always do so, as MDX-based client tools (such as Excel and Tabular Editor 3's Pivot Grid) require explicit measures. In addition, [Calculation Groups](https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions) only apply to explicit measures.

要使用 Tabular Editor 添加新的度量值，请在要添加度量值的表上单击右键，然后选择 **创建 > 度量值**（ALT+1）。

![添加新度量值](~/content/assets/images/adding-new-measure.png)

When a new measure is added, the name of that measure will be editable. Hit ENTER when you have provided a name for the measure. You can always edit the name later in the **Properties** view or by pressing F2 while the measure is selected in the **TOM Explorer**.

**表达式编辑器** 视图用于为度量值提供 DAX 表达式。 As you enter the code, notice how the DAX editor provides code suggestions and even underlines syntax or semantic errors.

![添加度量值并编辑 Dax](~/content/assets/images/add-measure-edit-dax.png)

The dropdown box at the top left corner of the **Expression Editor** is used to switch between different DAX properties of the currently selected object. For example, in newer versions of Analysis Services, measures have an `Expression` property as well as a [`Detail Rows Expression`](https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/). Other types of objects can have different properties that contain DAX code. For example, [KPIs](https://docs.microsoft.com/en-us/analysis-services/tabular-models/kpis-ssas-tabular?view=asallproducts-allversions) have three different DAX properties. To add a KPI in Tabular Editor, right-click on a measure and choose **Create > KPI**.

![编辑 Kpis](~/content/assets/images/editing-kpis.png)

如果你希望隐藏度量值，只需右键单击并选择 **设为不可见**（CTRL+I）。 Likewise, you can unhide a measure by choosing the **Make visible** (CTRL+U) option.

## 其他度量值属性

除了 `Name`、`Expression` 和 `Hidden` 属性之外，你还可以使用 **属性** 视图来查看并编辑 **TOM Explorer** 中当前所选对象(一个或多个)的所有属性值。 For measures, this is where you can set the `Format String`, for example. For more information, see [Properties view](xref:properties-view).

# 添加计算列

要添加计算列，请右键单击要添加该列的表，然后选择 **创建 > 计算列**（ALT+2）。 Give the column a name and edit its DAX expression using the **Expression Editor**, similar to how we did for measures above.

> [!IMPORTANT]
> 连接到 Power BI Desktop 模型时，此选项默认不可用。这是因为 [Power BI Desktop 对外部工具支持的限制](xref:desktop-limitations)。 Click the link to learn more.

> [!NOTE]
> 当计算列的 DAX 表达式发生更改后，必须先刷新该列所在的表，才能在 Report 中使用该列。 See <xref:refresh-preview-query#refreshing-data> for more information.

# 添加计算表格

To add a calculated table, right-click on the model or on the "Tables" folder, and choose **Create > Calculated Table** (ALT+6). Give the table a name and edit its DAX expression using the **Expression Editor**, similar to how we did for measures above. Notice that the columns on the table changes automatically, when you make a change to the DAX expression. This can cause cascading effects, if other DAX expressions reference the table, or if columns are used in a hierarchy.

> [!IMPORTANT]
> 连接到 Power BI Desktop 模型时，此选项默认不可用。这是因为 [Power BI Desktop 对外部工具支持的限制](xref:desktop-limitations)。 Click the link to learn more.

> [!NOTE]
> 当计算表格的 DAX 表达式发生更改后，必须先刷新该表格，才能在 Report 中使用。 See <xref:refresh-preview-query#refreshing-data> for more information.

# 添加计算组

要添加[计算组](https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions)，在模型或“表”文件夹上右键点击，然后选择 **创建 > 计算组** (ALT+7)。 Give the Calculation Group a name. Also consider a different name for the default **Name** column.

> [!IMPORTANT]
> 此选项仅适用于兼容级别为 1500 或更高的模型。

To add calculation items, right-click on the newly created calculation group and choose **Create > Calculation Item**. 为计算项命名，并使用 **表达式编辑器** 编辑其 DAX 表达式，方式与我们在上面创建度量值时类似。

你可以在 TOM Explorer 中拖动计算项来调整显示顺序，或在 **属性** 视图中设置 `Ordinal` 属性。

> [!NOTE]
> 在计算组中添加、重命名或删除计算项后，必须先刷新计算组，才能在 Report 中使用。 See <xref:refresh-preview-query#refreshing-data> for more information.

# 常见建模操作

## 复制/粘贴

TOM Explorer 中的所有对象都可以使用 Tabular Editor 进行复制和粘贴。 You can even copy and paste between different instances of Tabular Editor, and even between Tabular Editor 2.x and Tabular Editor 3. You can use the familiar keyboard shortcuts:

- **编辑 > 复制** (CTRL+C)
- **编辑 > 剪切** (CTRL+X)
- **编辑 > 粘贴** (CTRL+V)

> [!TIP]
> 如果你想用另一张表替换某张表，同时保留与该表之间现有的所有关系，请先把一张表复制到剪贴板，然后在 TOM Explorer 中选择要替换的表并粘贴。 You will be prompted whether you want to replace the selected table with the one in the clipboard.

## 撤销/重做

在 Tabular Editor 中，只要对对象或属性进行了更改，就会记录完整的更改历史，让你可以撤销所做的每一次更改。 You can use the familiar keyboard shortcuts:

- **编辑 > 撤销** (CTRL+Z)
- **编辑 > 重做** (CTRL+Y)

> [!NOTE]
> Tabular Editor 3 中的所有文本编辑器都有各自的撤销/重做历史记录，因此如果光标当前位于某个文本编辑器中，键盘快捷键将撤销/重做该编辑器中的输入操作。 You can use the options in the **Edit** menu to perform an undo/redo at the model level, or deactivate the current text editor by clicking on another element in the user interface (such as the TOM Explorer).

# 导航

当光标停留在 DAX 编辑器中的对象引用上时，右键单击并选择 **转到定义** (F12)，即可快速跳转到该对象。 Of course, you can also navigate between objects using the TOM Explorer.

你可以使用 **表达式编辑器** 右上角的箭头按钮，在已访问的对象之间快速前后跳转。

## DAX 依赖项

To view DAX dependencies between objects, select an object in the **TOM Explorer**, then right-click and choose **Show dependencies** (**Shift+F12**). This opens the **DAX Dependencies** view, which displays the dependencies of the selected object. Double-click an object in the tree to navigate to it, or right-click for **Go to item**, **Copy as text** and **Copy as JSON**.

![Dax 依赖项与 Tom Explorer](~/content/assets/images/dax-dependencies-and-tom-explorer.png)

The view shows one direction at a time. Choose which with the radio buttons:

| 选项                                         | Shows                                                                                                                                        |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objects that depend on this**            | What would break if you changed or deleted the selected object                                                                               |
| **Objects on which this depends**          | What the selected object reads from                                                                                                          |
| **Relationships starting from this table** | The relationships leaving the selected table. With a column selected, this reads **Relationships starting from this column** |

Tick **Show inactive** to include inactive relationships.

### Following the TOM Explorer

Rather than invoking **Show dependencies** for each object in turn, tick **Track TOM Explorer** and the view follows whatever is selected in the tree. Ticking it shows the dependencies of the object that is _already_ selected straight away, rather than waiting for the next selection change.

Tracking applies to a single selected object. Selecting several objects, or none, clears the view rather than showing a partial answer.

# 显示文件夹

Once your model starts to gain a considerable number of measures, a good practice is to organize them using Display Folders. In Tabular Editor, to create a Display Folder, either edit the `Display Folder` property through the **Properties** view, or alternatively, right-click on the measure(s), and select the **Create > Display Folder** option.

你还可以在显示文件夹之间剪切/复制/粘贴对象，或通过拖放移动对象。

# 后续步骤

- @dax-script-introduction
- @bpa
- @C# 脚本和宏