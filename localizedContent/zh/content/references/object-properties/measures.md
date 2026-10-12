---
uid: object-properties-measures
title: 度量值和 KPI 属性
author: Jeroen ter Heerdt
updated: 2026-10-05
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 度量值和 KPI 属性

<!--
SUMMARY: Reference for the properties of measures and KPIs.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍度量值及其关联 KPI 的属性。每个条目都会列出该属性在 Tabular Object Model (TOM) 中的名称，以及其类型和类别。有关大多数对象的通用属性，见 @object-properties-common。

## 度量值

度量值是一个命名的 DAX 表达式，会在查询的筛选语境中进行求值，例如 `SUM ( Sales[Amount] )`。度量值所属的表决定了它在字段列表中的显示位置，不会影响计算结果。要在 Tabular Editor 3 中添加度量值并编辑其表达式，见 @creating-and-testing-dax。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [显示文件夹](xref:object-properties-common#display-folder)
- [隐藏](xref:object-properties-common#hidden)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [已更改的属性](xref:object-properties-common#changed-properties)
- [DAX 标识符](xref:object-properties-common#dax-identifier)
- [错误信息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [状态](xref:object-properties-common#state)
- [Lineage tag](xref:object-properties-common#lineage-tag)
- [源 Lineage tag](xref:object-properties-common#source-lineage-tag)
- [翻译后的名称](xref:object-properties-common#translated-names)
- [翻译后的描述](xref:object-properties-common#translated-descriptions)
- [翻译后的显示文件夹](xref:object-properties-common#translated-display-folders)
- [同义词](xref:object-properties-common#synonyms)
- [在透视中显示](xref:object-properties-common#shown-in-perspective)

### 格式字符串

`FormatString` · string · 基本

客户端工具显示度量值时使用的格式，例如 `#,0.00`、`0.0%` 或 `yyyy-mm-dd`。其语法与 DAX [FORMAT](https://dax.guide/format) 函数相同。 DAX 查询返回未经格式化的值。要根据筛选语境选择格式，可设置 `FormatStringExpression`。

Best Practice Analyzer（BPA）规则 @kb.bpa-format-string-measures 会标记未设置格式字符串的可见数值和日期度量值。在 Tabular Editor 3 中，@script-format-numeric-measures 脚本会为所选度量值设置格式字符串。

### 数据类型

`DataType` · DataType · 元数据 · 只读

度量值表达式返回的数据类型，例如 `Int64`、`Double`、`Decimal`、`String` 或 `DateTime`。引擎会根据该表达式推导出此类型。当表达式在不同上下文中返回不同类型时，它为 `Variant`，例如在一种上下文中返回数字、在另一种上下文中返回文本；当表达式有错误时，它为 `Unknown`。

对于从文件打开的模型，引擎尚未设置数据类型。在 Tabular Editor 3 中，启用语义分析后，属性视图会显示 Tabular Editor 根据该表达式推断的数据类型。

### 表达式

`Expression` · string · 选项

用于计算度量值的 DAX 表达式。在 **表达式编辑器** 中编辑。在 Tabular Editor 3 中，表达式编辑器是 @dax-editor 的一部分，提供 Code Assist，并在你输入时用下划线标出语法和语义错误。 @code-actions 会为表达式提出改进建议，你只需点击一次即可应用。 @dax-debugger 可逐步执行表达式，并显示其各部分的值。它需要与模型建立连接。

@script-find-replace 脚本可一次性替换多个度量值表达式中的文本。 BPA 规则 @kb.bpa-expression-required 会标记表达式为空的度量值。

### 格式字符串表达式

`FormatStringExpression` · 字符串 · 选项 · 兼容级别 1601+

一个返回要使用的格式字符串的 DAX 表达式，例如按国家/地区显示不同的货币符号，或将较大的值以千或百万为单位显示。这称为 _动态格式字符串_。在表达式中，可使用 `SELECTEDMEASURE()` 或度量值名称来引用该度量值自身的值。

一个度量值不能同时具有 `FormatString` 和 `FormatStringExpression`。在 Tabular Editor 3 中，设置 `FormatStringExpression` 时，会在同一个撤销步骤中清除 `FormatString`。当两者同时被设置时(例如通过 C# Script)，Tabular Editor 3 会在该度量值上显示错误：“A measure is not allowed to have both its FormatString and FormatStringExpression property assigned”。若要恢复为静态格式，请先清除 `FormatStringExpression`，然后再设置 `FormatString`。

有关 Analysis Services 上复合模型中度量值出现的错误“A measure is not allowed to have both FormatString and Format Expression”，请参阅 @composite-model-measure-formatting。

### 明细行表达式

`DetailRowsExpression` · 字符串 · 选项 · 兼容级别 1400+

一个 DAX 表表达式，用于定义用户在对该度量值的某个值进行向下钻取时所看到的行，例如在 Excel 数据透视表中使用 **显示详细信息** 功能。该表达式会在被钻取的单元格的筛选语境中求值。例如，`SELECTCOLUMNS ( Sales, "Order", Sales[OrderNumber], "Amount", Sales[Amount] )` 会返回每笔销售的订单号和金额。当该属性为空时，向下钻取会返回基础表中的行，并使用该表的默认列。

Power BI 不使用此属性。若要为表中的所有度量值设置默认值，请在该表上使用 `DefaultDetailRowsExpression`（请参阅 @object-properties-tables）。有关分步示例，请参阅 @detail-rows-expression。

### 数据类别

`DataCategory` · 字符串 · 选项 · 兼容级别 1455+

度量值返回的值类型，客户端工具会据此显示该值。例如，当类别为 `ImageUrl` 时，Power BI 会将返回的 URL 显示为图像；当类别为 `WebUrl` 时，则显示为链接。度量值使用与列相同的类别。参见 @object-properties-columns 中的 `DataCategory`。

### KPI

`KPI` · KPI · 选项

与此度量值关联的 KPI（如有）。 KPI 会为该度量值添加目标、状态和趋势。参见下文的 [KPI](#kpi-1)。

在 Tabular Editor 3 中，要在属性视图中添加 KPI，请在空的 `KPI` 属性上点击 **...**，或右键单击该属性并选择 **添加 KPI**。要删除它，右键单击该属性并选择 **删除 KPI**。

Tabular Editor 2 的操作方式相同。在 Tabular Editor 2 中，还可以在 **TOM Explorer** 中右键单击该度量值，然后选择 **新建 > KPI**。随后，KPI 会显示在该度量值下方，你可以在此将其删除。

## KPI

关键绩效指标（KPI）通过为度量值添加目标值、用于将度量值与目标值进行比较的状态，以及趋势来扩展度量值。 Excel 和 SQL Server Management Studio 会使用状态和趋势图标显示 KPI。 Power BI 不会显示在模型中定义的 KPI，并且它有自己的 KPI Visual。

KPI 始终属于单个度量值，而该度量值本身的值就是 KPI 的 _值_。 KPI 本身没有单独的名称。

要在 Tabular Editor 3 中添加 KPI，右键单击一个度量值并选择 **创建 > KPI**。 DAX 脚本也可以同时定义度量值及其 KPI。参见 @dax-scripts。

### 常用属性

- [说明](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

### 父度量值

`MeasureName` · string · 元数据 · 只读 · _作为度量值名称的快捷方式_

此 KPI 所属度量值的名称。

### 度量值

`Measure` · 度量值 · 选项 · 只读

此 KPI 所属的度量值。 C# Script 使用它从 KPI 获取其对应的度量值。 Tabular Editor 3 会在属性视图中隐藏此属性，并改为在那里显示 `MeasureName`。

### 目标表达式

`TargetExpression` · string · 选项

一个返回度量值目标的 DAX 表达式，例如固定数字 `1000000`、另一个度量值（如 `[Sales Budget]`）或某个计算。

### 目标格式字符串

`TargetFormatString` · string · 选项

目标值的格式字符串，语法与度量值上的 `FormatString` 相同。

### 目标说明

`TargetDescription` · string · 选项

目标的说明，将在支持该属性的客户端工具中向用户显示。

### 状态表达式

`StatusExpression` · string · 选项

一个 DAX 表达式，用于将度量值与目标进行比较，并返回 `-1` 到 `1` 之间的数值，其中 `-1` 表示较差，`0` 表示中性，`1` 表示良好。客户端工具使用此数值从 `StatusGraphic` 中选择图标。比如：

```dax
VAR Ratio = DIVIDE ( [Total Sales], [Sales Budget] )
RETURN
    SWITCH ( TRUE (), Ratio >= 1, 1, Ratio >= 0.9, 0, -1 )
```

### 状态图标

`StatusGraphic` · string · 选项

客户端工具用于显示状态的图标集，例如 `Traffic Light` 或 `Shapes`，应填写为客户端工具可识别的名称。

在 Tabular Editor 3 中，可从列表中选择一个名称，或输入其他任意值。 Tabular Editor 3 接受任何值。列表包含 `Cylinder`、`Faces`、`Five Bars Colored`、`Five Boxes Colored`、`Gauge`、`Gauge - Ascending`、`Gauge - Descending`、`Reversed Gauge`、`Reversed status arrow`、`Road Signs`、`Shapes`、`Smiley`、`Smiley Face`、`Standard Arrow`、`Status Arrow`、`Status Arrow - Ascending`、`Status Arrow - Descending`、`Thermometer`、`Three Circles Colored`、`Three Flags Colored`、`Three Stars Colored`、`Three Symbols Uncircled Colored`、`Three Triangles`、`Traffic Light`、`Traffic Light - Single` 和 `Variance Arrow`。

Excel 只识别其中少数几个名称。在 Excel 数据透视表中，这些名称会显示各自对应的状态图标：

| 状态图标                                         | Excel 显示的内容    |
| -------------------------------------------- | -------------- |
| `Road Signs`                                 | 状态良好时显示对勾      |
| `Traffic Light`                              | 交通灯图标          |
| `Standard Arrow`                             | 灰色箭头           |
| `Status Arrow - Ascending`, `Variance Arrow` | 状态良好时显示向上的彩色箭头 |
| `Status Arrow - Descending`                  | 状态良好时显示向下的彩色箭头 |
| `Gauge - Ascending`, `Gauge - Descending`    | 一个深色圆圈或空心圆圈    |

所有其他名称，包括 `Shapes`、`Thermometer`、`Smiley`、`Cylinder` 以及 Excel 不识别的名称，都会显示为一个纯色圆圈。

### 状态描述

`StatusDescription` · string · 选项

状态的说明，会在支持该功能的客户端工具中向用户显示。

### 趋势表达式

`TrendExpression` · 字符串 · 选项

一个 DAX 表达式，返回介于 `-1` 到 `1` 之间的数值，用于指示度量值是否随时间变差 (`-1`)、保持不变 (`0`) 或变好 (`1`)，例如与上一期间相比。

### 趋势图标

`TrendGraphic` · 字符串 · 选项

客户端工具用于显示趋势的图标集名称，例如 `Standard Arrow`；应使用客户端工具能够识别的名称。在 Tabular Editor 3 中，你可以从与 `StatusGraphic` 相同的名称列表中选择，或输入其他任意值。

在 Excel 中，大多数名称会显示彩色箭头；`Standard Arrow` 显示灰色箭头，而 `Status Arrow - Descending` 会在趋势良好时显示向下箭头。少数名称，例如 `Cylinder`、`Smiley Face` 和 `Traffic Light - Single`，会显示圆圈。

### 趋势说明

`TrendDescription` · 字符串 · 选项

趋势的说明，会在支持该功能的客户端工具中向用户显示。
