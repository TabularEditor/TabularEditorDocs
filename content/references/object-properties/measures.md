---
uid: object-properties-measures
title: Measure and KPI properties
author: Jeroen ter Heerdt
updated: 2026-09-23
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
# Measure and KPI properties

<!--
SUMMARY: Reference for the properties of measures and KPIs.
-->

This page covers the properties of measures and of the KPIs that can be attached to them. For properties that most objects share, see @object-properties-common.

## Measure

A measure is a named DAX expression that's evaluated in the filter context of the query, for example `SUM ( Sales[Amount] )`. Measures belong to a table, but the table only decides where the measure appears in the field list. It doesn't affect how the measure is calculated. To learn how to add measures and edit their expressions in Tabular Editor 3, see @creating-and-testing-dax.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Display Folder](xref:object-properties-common#display-folder)
- [Hidden](xref:object-properties-common#hidden)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Changed Properties](xref:object-properties-common#changed-properties)
- [DAX identifier](xref:object-properties-common#dax-identifier)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)
- [Lineage Tag](xref:object-properties-common#lineage-tag)
- [Source Lineage Tag](xref:object-properties-common#source-lineage-tag)
- [Translated Names](xref:object-properties-common#translated-names)
- [Translated Descriptions](xref:object-properties-common#translated-descriptions)
- [Translated Display Folders](xref:object-properties-common#translated-display-folders)
- [Synonyms](xref:object-properties-common#synonyms)
- [Shown in Perspective](xref:object-properties-common#shown-in-perspective)

### Basic

#### Format String
`FormatString` · string

How client tools display the measure's value, for example `#,0.00` for a number with two decimals, `0.0%` for a percentage or `yyyy-mm-dd` for a date. The format only affects display: the measure still returns the unformatted value to DAX, and to tools that request unformatted values.

The format string uses the same syntax as the DAX `FORMAT` function. To choose a format that depends on the context, such as a currency symbol that follows the selected currency, use **Format String Expression** instead.

The Best Practice Analyzer rule @kb.bpa-format-string-measures flags visible numeric and date measures without a format string. In Tabular Editor 3, to set default format strings on the selected measures at once, use the @script-format-numeric-measures script.

### Metadata

#### Data Type
`DataType` · DataType · read-only

The data type the measure's expression returns, for example `Int64`, `Double`, `Decimal`, `String` or `DateTime`. The engine works it out from the expression, so you can't set it. It's `Variant` when the expression can return different types, for example a number in one context and text in another, and `Unknown` when the expression has an error.

A model that you open from a file isn't connected to an engine, so the engine hasn't set the data type there. In Tabular Editor 3, when semantic analysis is enabled, the Properties view shows the data type that Tabular Editor infers from the expression instead.

### Options

#### Expression
`Expression` · string

The DAX expression that calculates the measure. Edit it in the Expression Editor. In Tabular Editor 3, the Expression Editor is part of the @dax-editor: it offers code assist, and it underlines syntax and semantic errors as you type. @code-actions suggest improvements to the expression that you can apply with a single click. To step through the expression and see the values of its parts, use the @dax-debugger, which needs a connection to the model.

To replace text in the expressions of many measures at once, use the @script-find-replace script. The Best Practice Analyzer rule @kb.bpa-expression-required flags measures with an empty expression.

#### Format String Expression
`FormatStringExpression` · string · compatibility level 1601+

A DAX expression that returns the format string to use, for example to show a different currency symbol per country, or to show large values in thousands or millions. This is known as a *dynamic format string*. Inside the expression, you can refer to the measure's own value with `SELECTEDMEASURE()` or by its name.

A measure can't have both a **Format String** and a **Format String Expression**. When you set a **Format String Expression** in Tabular Editor 3, it clears **Format String** for you, in the same undoable step. When both are set, for example by a C# script, Tabular Editor 3 shows the error *A measure is not allowed to have both its FormatString and FormatStringExpression property assigned* on the measure. To go back to a static format, clear **Format String Expression** first, and then set **Format String**.

In a composite model on Analysis Services, you can get the error *A measure is not allowed to have both FormatString and Format Expression*. See @composite-model-measure-formatting.

#### Detail Rows Expression
`DetailRowsExpression` · string · compatibility level 1400+

A DAX table expression that defines the rows a user sees when they drill through on a value of this measure, for example in **Show Details** in an Excel PivotTable. Without it, drill-through returns the rows of the underlying table with the table's default columns.

For example, `SELECTCOLUMNS ( Sales, "Order", Sales[OrderNumber], "Amount", Sales[Amount] )`. The expression is evaluated in the filter context of the cell that was drilled into.

Power BI doesn't use this property. To set a default for all measures in a table, use **Default Detail Rows Expression** on the table (see @object-properties-tables). For a step-by-step example, see @detail-rows-expression.

#### Data Category
`DataCategory` · string · compatibility level 1455+

Tells client tools what kind of value the measure returns, so they can display it in a special way. For example, `ImageUrl` makes Power BI show the returned URL as an image, and `WebUrl` shows it as a link.

The same categories are available as for columns. See **Data Category** on @object-properties-columns.

#### KPI
`KPI` · KPI

The KPI attached to this measure, if there is one. A KPI adds a target, a status and a trend to the measure. See [KPI](#kpi) below.

In Tabular Editor 3, to add a KPI from the Properties view, select **...** on the empty **KPI** property, or right-click the property and choose **Add KPI**. To remove it, right-click the property and choose **Remove KPI**.

Tabular Editor 2 works the same way: select **...** on the empty **KPI** property, or right-click the property and choose **Add KPI** or **Remove KPI**. You can also right-click the measure in the TOM Explorer and choose **Create New > KPI**. The KPI then appears under the measure, and you can delete it there.

## KPI

A key performance indicator (KPI) extends a measure with a target value, a status that compares the measure to the target, and a trend. Excel and SQL Server Management Studio show KPIs with status and trend icons. Power BI doesn't show KPIs defined in the model. It uses its own KPI visual instead.

A KPI always belongs to a single measure: the measure's own value is the KPI's *value*. The KPI has no name of its own.

To add a KPI in Tabular Editor 3, right-click a measure and choose **Create > KPI**. You can also define a measure together with its KPI in a DAX script. See @dax-scripts.

### Common properties

- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Metadata

#### Parent Measure
`MeasureName` · string · read-only · *shortcut to* the name of the measure

The name of the measure this KPI belongs to.

### Options

#### Measure
`Measure` · Measure · read-only

The measure this KPI belongs to. Useful in C# scripts to get from the KPI back to its measure. Tabular Editor 3 doesn't show this property in the Properties view. Use **Parent Measure** instead.

#### Target Expression
`TargetExpression` · string

A DAX expression that returns the goal for the measure, for example a fixed number such as `1000000`, another measure such as `[Sales Budget]`, or a calculation.

#### Target Format String
`TargetFormatString` · string

The format string used to display the target value. Same syntax as **Format String** on a measure.

#### Target Description
`TargetDescription` · string

A description of the target, shown to users in client tools that support it.

#### Status Expression
`StatusExpression` · string

A DAX expression that compares the measure to the target and returns a number between `-1` and `1`: `-1` is bad, `0` is neutral and `1` is good. Client tools use this number to choose the icon from **Status Graphic**. For example:

```dax
VAR Ratio = DIVIDE ( [Total Sales], [Sales Budget] )
RETURN
    SWITCH ( TRUE (), Ratio >= 1, 1, Ratio >= 0.9, 0, -1 )
```

#### Status Graphic
`StatusGraphic` · string

The icon set that client tools use to show the status, for example `Traffic Light` or `Shapes`. The value is a name that the client tool recognizes.

In Tabular Editor 3, you can pick a name from a list, or type any other value. Tabular Editor doesn't check it. The list contains: `Cylinder`, `Faces`, `Five Bars Colored`, `Five Boxes Colored`, `Gauge`, `Gauge - Ascending`, `Gauge - Descending`, `Reversed Gauge`, `Reversed status arrow`, `Road Signs`, `Shapes`, `Smiley`, `Smiley Face`, `Standard Arrow`, `Status Arrow`, `Status Arrow - Ascending`, `Status Arrow - Descending`, `Thermometer`, `Three Circles Colored`, `Three Flags Colored`, `Three Stars Colored`, `Three Symbols Uncircled Colored`, `Three Triangles`, `Traffic Light`, `Traffic Light - Single` and `Variance Arrow`.

Excel only recognizes a few of these names. In an Excel PivotTable, these show their own icon for the status:

| Status Graphic | What Excel shows |
|---|---|
| `Road Signs` | A check mark when the status is good |
| `Traffic Light` | A traffic light |
| `Standard Arrow` | A grey arrow |
| `Status Arrow - Ascending`, `Variance Arrow` | A colored arrow that points up when the status is good |
| `Status Arrow - Descending` | A colored arrow that points down when the status is good |
| `Gauge - Ascending`, `Gauge - Descending` | A dark or an empty circle, not a gauge |

All other names, including `Shapes`, `Thermometer`, `Smiley`, `Cylinder` and a name Excel doesn't know, show a plain colored circle. So check the result in the client tool your users have.

#### Status Description
`StatusDescription` · string

A description of the status, shown to users in client tools that support it.

#### Trend Expression
`TrendExpression` · string

A DAX expression that returns a number between `-1` and `1` that shows whether the measure is getting worse (`-1`), staying the same (`0`) or getting better (`1`) over time, for example compared to the previous period.

#### Trend Graphic
`TrendGraphic` · string

The icon set that client tools use to show the trend, for example `Standard Arrow`. The value is a name that the client tool recognizes, just like **Status Graphic**. In Tabular Editor 3, you pick it from the same list of names as **Status Graphic**, or type any other value.

Excel shows a colored arrow for most names, a grey arrow for `Standard Arrow`, and an arrow that points down when the trend is good for `Status Arrow - Descending`. A few names, such as `Cylinder`, `Smiley Face` and `Traffic Light - Single`, show a circle instead.

#### Trend Description
`TrendDescription` · string

A description of the trend, shown to users in client tools that support it.
