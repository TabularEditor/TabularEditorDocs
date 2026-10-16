---
uid: object-properties-calculation-groups
title: 计算组属性
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

# 计算组属性

<!--
SUMMARY: Reference for the properties of calculation groups and calculation items.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍计算组和计算项的属性。计算组始终属于某个计算组表。该表的属性(包括可直接访问计算组自身属性的快捷方式)见 @object-properties-tables。有关大多数对象共有的属性，见 @object-properties-common。

## 计算组

计算组是一组用于更改度量值计算方式的计算项。例如，时间智能计算组可以包含 `Current`、`YTD` 和 `Prior year` 等计算项。当 Report 作者将计算组的列放入切片器中并选择 `YTD` 时，Visual 中的所有度量值都会显示其本年迄今值，而无需为每个度量值单独创建一个 YTD 度量值。

计算组本身没有单独的名称，而是通过其计算组表来标识。在 **TOM Explorer** 中无法选择计算组。选择计算组表后，**属性** 视图会将计算组属性显示为 `CalculationGroupDescription`、`CalculationGroupAnnotations` 和 `CalculationGroupPrecedence`（见 @object-properties-tables）。在 C# Script 中，可通过 `CalculationGroupTable.CalculationGroup` 访问计算组对象。

在 Tabular Editor 3 中，可通过右键单击模型或 **表** 文件夹，然后选择 **创建 > 计算组** 来创建计算组。 Microsoft 文档指出，计算组适用于兼容级别 1500 或更高的模型，其中包括所有 Power BI 语义模型。 Tabular Editor 3 从兼容级别 1470 起就会显示该菜单选项，因为 Tabular Object Model（TOM）是在这一兼容级别新增了计算组。见 @creating-and-testing-dax。

### 通用属性

- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [对象类型](xref:object-properties-common#object-type)

### 优先级

`Precedence` · int · 选项

当查询同时使用来自多个计算组的项时，例如时间智能组和货币换算组，这些计算组的应用顺序。优先级最高的计算组会最先应用，因此它的计算项位于最外层。当该项调用 [SELECTEDMEASURE](https://dax.guide/selectedmeasure) 时，引擎会使用下一个优先级更低的计算组中的计算项结果，依此类推，直到度量值本身。

如果这些计算项不满足交换律，顺序就会影响结果。例如，当一个时间智能组包含 `YTD` 项，另一个组包含 `Average per day` 项时，日均值的年初至今值与年初至今值的日均值并不相同。在此示例中，优先级为 `200` 的计算组包含计算项 `SELECTEDMEASURE () * 2`，优先级为 `100` 的计算组包含计算项 `SELECTEDMEASURE () + 2`。如果在一个返回 `10` 的度量值上同时选择这两个计算项，结果为 `( 10 + 2 ) * 2 = 24`。

TOM 默认值为 `0`。为模型中的每个计算组设置不同的优先级，且值为 `0` 或更高。如果模型中有两个计算组使用相同的优先级，引擎会拒绝该模型，并报出类似“Calculation Group precedence must be greater or equal zero and unique within Model”的错误。

当你添加或粘贴一个计算组，而模型中的其他计算组已使用其优先级时，Tabular Editor 会将其设置为比模型中最高优先级高一级。你也可以在计算组表中通过 `CalculationGroupPrecedence` 属性来设置。在 Tabular Editor 3 的 @dax-scripts 文档中，你可以通过计算组的 `Precedence` 属性进行设置。

## 计算项

计算项是计算组中的一个条目，例如 `YTD`。 Report 作者会在计算组的列中将它的名称视为一个值，而它的表达式会定义选中该项时度量值如何变化。在表达式内部，[SELECTEDMEASURE](https://dax.guide/selectedmeasure) 会返回当前正在求值的度量值。

没有计算项的计算组不会产生任何效果。 Best Practice Analyzer (BPA) 规则 @kb.bpa-calculation-groups-no-items 会标记不包含任何计算项的计算组。

计算项的 `Description` 仅供开发人员使用。例如，当 Report 作者将鼠标悬停在切片器中的该项上时，Power BI Desktop 不会显示它。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [错误消息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [状态](xref:object-properties-common#state)

### 序号

`Ordinal` · int · 基本 · 兼容级别 1500+

计算项在其计算组中的位置，从 `0` 开始。客户端工具会按此值对这些项进行排序，例如在切片器中按 `Current`、`MTD`、`QTD` 和 `YTD` 的顺序显示它们。引擎通过计算组表中的 Ordinal 列公开该值。

值 `-1` 表示该项没有位置。根据 Microsoft 的说法，值为 `-1` 的项不参与排序，并会在 Report 中排在已排序项之前。如果没有任何项具有 ordinal 值，客户端工具会按字母顺序对这些项排序。

Tabular Editor 3 会将计算组中的 ordinal 值保持为 `0`、`1`、`2` 等连续编号，不留空缺也不重复：

- 当你在 **TOM Explorer** 中拖动计算项以调整顺序时，Tabular Editor 会为组中的所有项重新编号
- 当你在 **属性** 视图中输入新的 `Ordinal` 时，Tabular Editor 会将该项移动到对应位置，并为其他项重新编号
- 当你输入 `-1` 时，Tabular Editor 会将组中每一项的 ordinal 都设为 `-1`，从而移除自定义顺序
- 添加计算项时，它会分配到组内最高 ordinal 之后的下一个编号，除非组中尚无任何项具有 ordinal 值

你一次只能为一个计算项设置 `Ordinal`。在 **TOM Explorer** 中拖动计算项以调整顺序，或输入新的 `Ordinal` 时，Tabular Editor 2 也会以相同方式重新编号这些项的 ordinal 值。

你也可以将计算项拖到另一个计算组中，把它们移动过去。参见 @drag-drop。

### 表达式

`Expression` · 字符串 · 选项

选中此计算项时，引擎会用该 DAX 表达式替代度量值进行计算。使用 [SELECTEDMEASURE](https://dax.guide/selectedmeasure) 来引用该度量值。这是一个年初至今计算项：

```dax
CALCULATE ( SELECTEDMEASURE (), DATESYTD ( 'Date'[Date] ) )
```

此项不会改变度量值，可用作默认项：

```dax
SELECTEDMEASURE ()
```

该表达式会应用于查询中的每个度量值，包括返回文本的度量值。如果只想让它作用于某些度量值，可以用 [ISSELECTEDMEASURE](https://dax.guide/isselectedmeasure) 或 [SELECTEDMEASURENAME](https://dax.guide/selectedmeasurename) 来判断当前度量值，例如：

```dax
IF (
    ISSELECTEDMEASURE ( [Total Sales], [Total Cost] ),
    CALCULATE ( SELECTEDMEASURE (), DATESYTD ( 'Date'[Date] ) ),
    SELECTEDMEASURE ()
)
```

计算项仅应用于度量值，隐式聚合的列不受影响。添加计算组时，Power BI 会在模型中启用 `DiscourageImplicitMeasures` (请参阅 @object-properties-model)。

在 Tabular Editor 3 中，你可以在 @dax-editor 的 **表达式编辑器** 中编写该表达式，并使用自动补全和参数提示。

### 格式字符串表达式

`FormatStringExpression` · 字符串 · 选项

一个 DAX 表达式，在选中此计算项时返回度量值的格式字符串。将其留空即可保留度量值自身的格式。当该项会改变度量值返回的值类型时，请设置它，例如同比百分比：

```dax
"0.0%"
```

你也可以让格式取决于上下文，例如货币符号。在表达式中，[SELECTEDMEASUREFORMATSTRING](https://dax.guide/selectedmeasureformatstring) 会返回度量值自身的格式字符串，你可以将其用作备用值。此示例使用一个包含 `Format` 列的 `Currency` 表：

```dax
SELECTEDVALUE ( 'Currency'[Format], SELECTEDMEASUREFORMATSTRING () )
```

该表达式必须返回单个文本值。计算项上的格式字符串表达式没有单独的兼容级别要求，在支持计算组的任何地方都可用。当多个计算组应用于同一个度量值时，引擎只会使用优先级最高的计算组的格式字符串表达式。要删除该表达式，清空该值即可。
