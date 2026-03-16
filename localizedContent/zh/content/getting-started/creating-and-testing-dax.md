---
uid: creating-and-testing-dax
title: 添加度量值和其他计算对象
author: Daniel Otykier
updated: 2021-10-08
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# 添加度量值和其他计算对象

自 2017 年初发布 Tabular Editor 2.x 以来，能够在多个度量值上快速修改 DAX 表达式一直是该工具最受欢迎的功能。 结合后退/前进导航、复制/粘贴操作、DAX 依赖关系可视化以及撤销/重做支持，这款工具一直是处理大型且复杂 Data model 的用户的首选，因为能够快速完成多处小幅修改往往至关重要。

Tabular Editor 2.x 用户在这方面唯一的抱怨，是缺少 DAX Code Assist 功能（有时也称为“IntelliSense”）。 尤其是当你对 DAX 还没做到 100% 熟练（说实话，几乎没人能做到！）时，让 DAX 代码编辑器帮你记住语法、函数参数等，会非常有用。

Tabular Editor 3 使用的新 DAX 代码编辑器已将这些问题全部解决。

![编辑复杂的 DAX 表达式](~/content/assets/images/dax-editor-screenshot.png)

本文其余部分将介绍如何创建度量值和其他计算对象，以及如何修改这些对象上的 DAX 表达式。 想详细了解 DAX 代码编辑器的众多功能，可以查看 <xref:dax-editor>。

# 添加度量值

当你已将[一些表导入](xref:importing-tables-data-modeling#importing-new-tables)模型，并[在它们之间创建了关系](xref:importing-tables-data-modeling#modifying-relationships-using-the-diagram)之后，就该添加一些包含业务逻辑的显式度量值了。

> [!TIP]
> 从技术角度来说，在 Power BI Report 里可视化数据之前，你不必先在模型里添加显式度量值。 不过，最佳实践是始终这样做，因为基于 MDX 的客户端工具（例如 Excel 和 Tabular Editor 3 的 Pivot Grid）要求显式定义度量值。 此外，[计算组](https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions) 仅适用于显式度量值。

要使用 Tabular Editor 添加新的度量值，请在要添加度量值的表上单击右键，然后选择 **创建 > 度量值**（ALT+1）。

![添加新度量值](~/content/assets/images/adding-new-measure.png)

添加新的度量值后，该度量值的名称将处于可编辑状态。 为度量值输入名称后，按 Enter 键。 你随时都可以在 **属性** 视图中编辑名称，也可以在 **TOM Explorer** 中选中该度量值后按 F2 键。

**表达式编辑器** 视图用于为度量值提供 DAX 表达式。 输入代码时，注意 DAX 编辑器会提供代码建议，甚至会为语法或语义错误加下划线提示。

![添加度量值并编辑 Dax](~/content/assets/images/add-measure-edit-dax.png)

**表达式编辑器** 左上角的下拉框用于在当前所选对象的不同 DAX 属性之间切换。 例如，在较新版本的 Analysis Services 中，度量值既有 `Expression` 属性，也有 [`Detail Rows Expression`](https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/)。 其他类型的对象可能有不同的属性用于承载 DAX 代码。 例如，[KPI](https://docs.microsoft.com/en-us/analysis-services/tabular-models/kpis-ssas-tabular?view=asallproducts-allversions) 有三个不同的 DAX 属性。 要在 Tabular Editor 中添加 KPI，右键单击某个度量值，然后选择 **创建 > KPI**。

![编辑 Kpis](~/content/assets/images/editing-kpis.png)

如果你希望隐藏度量值，只需右键单击并选择 **设为不可见**（CTRL+I）。 同样，你也可以通过选择 **设为可见**（CTRL+U）来取消隐藏度量值。

## 其他度量值属性

除了 `Name`、`Expression` 和 `Hidden` 属性之外，你还可以使用 **属性** 视图来查看并编辑 **TOM Explorer** 中当前所选对象(一个或多个)的所有属性值。 例如，对于度量值，你可以在这里设置 `Format String`。 更多信息请参阅 [属性视图](xref:properties-view)。

# 添加计算列

要添加计算列，请右键单击要添加该列的表，然后选择 **创建 > 计算列**（ALT+2）。 为该列命名，并使用 **表达式编辑器** 编辑其 DAX 表达式，方式与上面创建度量值时类似。

> [!IMPORTANT]
> 连接到 Power BI Desktop 模型时，默认情况下此选项不可用。 这是因为 Power BI Desktop 对外部工具的支持存在[限制](xref:desktop-limitations)。 单击链接了解更多信息。

> [!NOTE]
> 当计算列的 DAX 表达式发生更改后，必须先刷新该列所在的表，才能在 Report 中使用该列。 更多信息请参阅<xref:refresh-preview-query#refreshing-data>。

# 添加计算表格

要添加计算表格，请在模型或“Tables”文件夹上右键单击，然后选择 **创建 > 计算表格** (ALT+6)。 为表格命名，并使用 **表达式编辑器** 编辑其 DAX 表达式，方式与我们在上面创建度量值时类似。 注意，当你修改 DAX 表达式时，表中的列会自动更新。 如果其他 DAX 表达式引用了该表格，或某些列被用在层次结构中，这可能会产生连锁影响。

> [!IMPORTANT]
> 连接到 Power BI Desktop 模型时，此选项默认不可用。 这是因为 [Power BI Desktop 对外部工具支持的限制](xref:desktop-limitations)。 点击链接了解更多。

> [!NOTE]
> 当计算表格的 DAX 表达式发生更改后，必须先刷新该表格，才能在 Report 中使用。 更多信息见 <xref:refresh-preview-query#refreshing-data>。

# 添加计算组

要添加[计算组](https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions)，在模型或“表”文件夹上右键点击，然后选择 **创建 > 计算组** (ALT+7)。 为计算组命名。 另外，建议为默认的 **Name** 列另取一个名称。

> [!IMPORTANT]
> 此选项仅适用于兼容级别为 1500 或更高的模型。

要添加计算项，请在新建的计算组上右键单击，然后选择 **创建 > 计算项**。 为计算项命名，并使用 **表达式编辑器** 编辑其 DAX 表达式，方式与我们在上面创建度量值时类似。

你可以在 TOM Explorer 中拖动计算项来调整显示顺序，或在 **属性** 视图中设置 `Ordinal` 属性。

> [!NOTE]
> 在计算组中添加、重命名或删除计算项后，必须先刷新计算组，才能在 Report 中使用。 更多信息见 <xref:refresh-preview-query#refreshing-data>。

# 常见建模操作

## 复制/粘贴

TOM Explorer 中的所有对象都可以使用 Tabular Editor 进行复制和粘贴。 你甚至可以在不同的 Tabular Editor 实例之间复制和粘贴，也可以在 Tabular Editor 2.x 和 Tabular Editor 3 之间复制和粘贴。 你可以使用熟悉的键盘快捷键：

- **编辑 > 复制** (CTRL+C)
- **编辑 > 剪切** (CTRL+X)
- **编辑 > 粘贴** (CTRL+V)

> [!TIP]
> 如果你想用另一张表替换某张表，同时保留与该表之间现有的所有关系，请先把一张表复制到剪贴板，然后在 TOM Explorer 中选择要替换的表并粘贴。 系统会提示你是否要用剪贴板中的表替换所选表。

## 撤销/重做

在 Tabular Editor 中，只要对对象或属性进行了更改，就会记录完整的更改历史，让你可以撤销所做的每一次更改。 你可以使用熟悉的键盘快捷键：

- **编辑 > 撤销** (CTRL+Z)
- **编辑 > 重做** (CTRL+Y)

> [!NOTE]
> Tabular Editor 3 中的所有文本编辑器都有各自的撤销/重做历史记录，因此如果光标当前位于某个文本编辑器中，键盘快捷键将撤销/重做该编辑器中的输入操作。 你可以使用 **编辑** 菜单中的选项在模型级别执行撤销/重做，或者点击用户界面中的其他元素（例如 TOM Explorer）来停用当前文本编辑器。

# 导航

当光标停留在 DAX 编辑器中的对象引用上时，右键单击并选择 **转到定义** (F12)，即可快速跳转到该对象。 当然，你也可以使用 TOM Explorer 在对象之间导航。

你可以使用 **表达式编辑器** 右上角的箭头按钮，在已访问的对象之间快速前后跳转。

## DAX 依赖项

要查看对象之间的 DAX 依赖项，请在 **TOM Explorer** 中选择一个对象，然后右键单击并选择 **显示依赖项** (SHIFT+F12)。 这将打开一个窗口，显示所选对象的依赖项（双向）。 在此窗口中双击某个对象，可快速导航到该对象。

![Dax 依赖项与 Tom Explorer](~/content/assets/images/dax-dependencies-and-tom-explorer.png)

# 显示文件夹

当模型里的度量值数量增长到一定规模后，用显示文件夹来组织它们会更方便。 在 Tabular Editor 中，要创建显示文件夹，可以在 **属性** 视图中编辑 `Display Folder` 属性；或者右键单击度量值(可多选)，然后选择 **创建 > 显示文件夹**。

你还可以在显示文件夹之间剪切/复制/粘贴对象，或通过拖放移动对象。

# 后续步骤

- @dax-script-introduction
- @bpa
- @cs-scripts-and-macros