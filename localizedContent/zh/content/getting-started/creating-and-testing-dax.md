---
uid: creating-and-testing-dax
title: 添加度量值和其他计算对象
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

# 添加度量值和其他计算对象

自 2017 年初 Tabular Editor 2.x 发布以来，跨度量快速修改 DAX 表达式的功能一直是该工具最受欢迎的功能。该工具结合了后退和前进导航、复制/粘贴操作、DAX 依赖关系可视化以及撤销/重做支持，始终是处理大型复杂数据模型的首选工具，因为在这些模型中，能够快速进行多项小规模更改至关重要。

在这方面，Tabular Editor 2.x 用户唯一的抱怨是缺乏 DAX 代码辅助功能（有时称为“IntelliSense”）。尤其是在您对 DAX 的掌握并不完全精通（很少有人能完全精通！）的情况下，让 DAX 代码编辑器帮助您记忆语法、函数参数等，将大有裨益。

Tabular Editor 3 使用的新 DAX 代码编辑器解决了所有这些问题。

![编辑复杂的 DAX 表达式](~/content/assets/images/dax-editor-screenshot.png)

本文的其余部分将介绍如何创建度量值和其他计算对象，以及如何修改这些对象上的 DAX 表达式。要了解有关 DAX 代码编辑器众多功能的更多信息，请参阅<xref:dax-editor>。

# 添加度量值

在将[一些表导入](xref:importing-tables-data-modeling#importing-new-tables)到你的模型并[在它们之间创建关系](xref:importing-tables-data-modeling#modifying-relationships-using-the-diagram)后，是时候添加一些包含你的业务逻辑的显式度量值了。

> [!TIP]
> 从技术上讲，在 Power BI 报表中可视化数据之前，您无需向模型添加显式度量值。但是，最佳做法是始终这样做，因为基于 MDX 的客户端工具（例如 Excel 和 Tabular Editor 3 的 Pivot Grid）需要显式度量值。此外，[计算组](https://docs.microsoft.com/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions)仅适用于显式度量值。

要使用 Tabular Editor 添加新度量值，请右键单击要添加度量值的表，然后选择**创建 > 度量值** (ALT+1)。

![添加新度量值](~/content/assets/images/adding-new-measure.png)

添加新度量值时，该度量值的名称将可编辑。为该度量值提供名称后，请按 ENTER 键。您始终可以在 **Properties** 视图中或在 **TOM Explorer** 中选中度量值时按 F2 键，稍后编辑名称。

**表达式编辑器**视图用于提供该度量的 DAX 表达式。在您输入代码时，请注意 DAX 编辑器如何提供代码建议，甚至还会将语法或语义错误加下划线。

![添加度量值 编辑 DAX](~/content/assets/images/add-measure-edit-dax.png)

**表达式编辑器**左上角的下拉框用于在当前选定对象的不同 DAX 属性之间切换。例如，在较新版本的 Analysis Services 中，度量值具有 `Expression` 属性以及 [`Detail Rows Expression`](https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/)。其他类型的对象可能具有包含 DAX 代码的不同属性。例如，[KPI](https://docs.microsoft.com/analysis-services/tabular-models/kpis-ssas-tabular?view=asallproducts-allversions) 有三种不同的 DAX 属性。要在 Tabular Editor 中添加 KPI，请右键单击度量值，然后选择**创建 > KPI**。

![编辑 KPI](~/content/assets/images/editing-kpis.png)

如果您希望隐藏度量值，只需右键单击并选择**隐藏**（CTRL+I）选项即可。同样，您可以通过选择**显示**（CTRL+U）选项来取消隐藏度量值。

## 其他度量值属性

除了`Name`、`Expression`和`Hidden`属性外，您还可以使用**Properties**视图查看和编辑**TOM资源管理器**中当前选定对象的所有属性的值。对于度量，您可以在此处设置“格式字符串”等。有关更多信息，请参阅[属性视图](xref:properties-view)。

# 添加计算列

要添加计算列，请右键单击要添加列的表格，然后选择**创建 > 计算列** (ALT+2)。为列命名，并使用**表达式编辑器**编辑其 DAX 表达式，类似于我们上面对度量值所做的操作。

> [!IMPORTANT]
> 连接到 Power BI Desktop 模型时，此选项默认不可用。这是因为[Power BI Desktop 对外部工具的支持存在局限性](xref:desktop-limitations)。点击链接了解更多。

> [!NOTE]
> 当计算列的 DAX 表达式发生更改时，必须先刷新该列所在的表，然后才能在报表中使用该列。有关详细信息，请参阅<xref:refresh-preview-query#refreshing-data>。

# 添加计算表格

要添加计算表格，请右键单击模型或“表格”文件夹，然后选择**创建 > 计算表格** (ALT+6)。为表命名，并使用**表达式编辑器**编辑其 DAX 表达式，类似于我们对上述度量值的操作。请注意，当您对 DAX 表达式进行更改时，表上的列会自动发生变化。如果其他 DAX 表达式引用该表，或者如果在层次结构中使用了列，则可能会产生级联效应。

> [!IMPORTANT]
> 连接到 Power BI Desktop 模型时，此选项默认不可用。这是因为[Power BI Desktop 对外部工具的支持存在局限性](xref:desktop-limitations)。点击链接了解更多。

> [!NOTE]
> 当计算表格的 DAX 表达式发生更改时，必须先刷新该表格，然后才能在报表中使用。有关详细信息，请参阅<xref:refresh-preview-query#refreshing-data>。

# 添加计算组

要添加[计算组](https://docs.microsoft.com/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions)，请右键单击模型或“表格”文件夹，然后选择**创建 > 计算组** (ALT+7)。为计算组命名。还可以考虑为默认的**名称**列使用其他名称。

> [!IMPORTANT]
> 此选项仅适用于兼容级别为 1470 或更高的模型。Analysis Services 支持兼容级别 1500 或更高的计算组。

要添加计算项，请右键单击新创建的计算组，然后选择**创建 > 计算项**。为计算项命名，并使用**表达式编辑器**编辑其 DAX 表达式，类似于我们上面对度量值所做的操作。

您可以通过在 TOM Explorer 中拖动计算项来排列其显示顺序，也可以在**属性**视图中设置`Ordinal`属性。设置 `Ordinal` 会将该项移动到该位置，而超出最后一个位置的值会将该项移动到末尾。

> [!NOTE]
> 当计算项被添加到计算组、在计算组中重命名或从计算组中移除时，必须先刷新计算组，然后才能在报表中使用该计算组。有关详细信息，请参阅<xref:refresh-preview-query#refreshing-data>。

# 常用建模操作

## 复制/粘贴

可以使用 Tabular Editor 复制和粘贴 TOM Explorer 中的所有对象。您甚至可以在不同 Tabular Editor 实例之间进行复制和粘贴，甚至在 Tabular Editor 2.x 和 Tabular Editor 3 之间进行复制和粘贴。您可以使用熟悉的键盘快捷键：

- **编辑 > 复制** (CTRL+C)
- **编辑 > 剪切** (CTRL+X)
- **编辑 > 粘贴** (CTRL+V)

> [!TIP]
> 如果你想用一个表替换另一个表，同时保留该表的所有现有关系，请将一个表复制到剪贴板，然后在 TOM Explorer 中选择要替换的表并粘贴。系统将提示您是否要用剪贴板中的表格替换所选表格。

## 撤销/重做

每当对 Tabular Editor 中的对象或属性进行更改时，系统都会跟踪完整的更改历史记录，使您可以撤消所做的每项更改。您可以使用熟悉的键盘快捷键：

- **编辑 > 撤消** (CTRL+Z)
- **编辑 > 重做** (CTRL+Y)

> [!NOTE]
> Tabular Editor 3 中的文本编辑器有自己的撤销历史记录。当光标位于文本编辑器中时， **Ctrl+Z** 和 **Ctrl+Y** 分别用于撤消和重做该编辑器中的键入操作。要撤消模型更改，请先单击“TOM Explorer”，或在“编辑”菜单中选择“模型撤消”项。请参阅[在文本编辑器中撤消](xref:undo-redo#undo-in-text-editors)。

# 导航

当光标位于 DAX 编辑器中的对象引用上时，右键单击并选择**转到定义** (F12)，即可快速跳转到该对象。当然，您也可以使用 TOM Explorer 在对象之间导航。

您可以使用**表达式编辑器**右上角的箭头按钮，在已访问的对象之间快速来回跳转。

## DAX 依赖关系

要查看对象之间的 DAX 依赖项，请在**TOM Explorer**中选择一个对象，然后右键单击并选择**显示依赖项**（**Shift+F12**）。这将打开**DAX 依赖关系**视图，该视图显示所选对象的依赖关系。双击树中的对象以导航至该对象，或右键单击以选择**转到项**、**复制为文本**和**复制为 JSON**。

![DAX 依赖项和 TOM Explorer](~/content/assets/images/dax-dependencies-and-tom-explorer.png)

该视图一次显示一个方向。使用单选按钮选择方向：

| 选项 | 显示内容 |
|---|---|
| **依赖于此的对象** | 如果您更改或删除了所选对象，哪些内容会出错 |
| **此对象依赖的对象** | 所选对象读取的对象 |
| **从此表格开始的关系** | 从所选表格开始的关系。选择一列后，此项显示为**从此列开始的关系** |

勾选**显示非活跃项**以包含非活跃关系。

### 跟踪 TOM Explorer

与其逐个为每个对象调用**显示依赖项**，不如勾选**跟踪 TOM Explorer**，视图将跟随树中选定的任何内容。选中此项将立即显示*已*选定对象的依赖项，而不是等待下一次选择更改。

跟踪适用于单个选定对象。选择多个对象或不选择任何对象将清除视图，而不是显示部分答案。

# 显示文件夹

当您的模型开始拥有大量度量值时，一个好的做法是使用显示文件夹来组织它们。在 Tabular Editor 中，要创建显示文件夹，可以通过“属性”视图编辑“显示文件夹”属性，或者右键单击度量值，然后选择“创建 > 显示文件夹”选项。

您还可以在显示文件夹之间剪切/复制/粘贴或拖放对象。

# 后续步骤

- @dax-脚本-简介
- @bpa
- @cs-scripts-and-macros