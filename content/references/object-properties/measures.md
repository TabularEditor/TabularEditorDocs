---
uid: object-properties-measures
title: Measure and KPI properties
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
# Measure and KPI properties

<!--
SUMMARY: Reference for the properties of measures and KPIs.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

This page covers the properties of measures and of the KPIs attached to them. Each entry gives the property's name in the Tabular Object Model (TOM), its type and its category. For properties that most objects share, see @object-properties-common.

## Measure

A measure is a named DAX expression that's evaluated in the filter context of the query, for example `SUM ( Sales[Amount] )`. The table that a measure belongs to sets where the measure appears in the field list and doesn't affect the calculation. To add measures and edit their expressions in Tabular Editor 3, see @creating-and-testing-dax.

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

### Format String
`FormatString` · string · Basic

The format that client tools apply when they display the measure's value, for example `#,0.00`, `0.0%` or `yyyy-mm-dd`. The syntax is the same as for the DAX [FORMAT](https://dax.guide/format) function. DAX queries return the unformatted value. To pick the format based on the filter context, set `FormatStringExpression`.

The Best Practice Analyzer (BPA) rule @kb.bpa-format-string-measures flags visible numeric and date measures without a format string. In Tabular Editor 3, the @script-format-numeric-measures script sets format strings on the selected measures.

### Data Type
`DataType` · DataType · Metadata · read-only

The data type that the measure's expression returns, for example `Int64`, `Double`, `Decimal`, `String` or `DateTime`. The engine derives it from the expression. It's `Variant` when the expression returns different types in different contexts, for example a number in one context and text in another, and `Unknown` when the expression has an error.

In a model that you open from a file, the engine hasn't set the data type. In Tabular Editor 3, when semantic analysis is enabled, the Properties view then shows the data type that Tabular Editor infers from the expression.

### Expression
`Expression` · string · Options

The DAX expression that calculates the measure. Edit it in the **Expression Editor**. In Tabular Editor 3, the Expression Editor is part of the @dax-editor, with code assist and underlining of syntax and semantic errors as you type. @code-actions suggest improvements to the expression that you apply with a single click. The @dax-debugger steps through the expression and shows the values of its parts. It needs a connection to the model.

The @script-find-replace script replaces text in the expressions of many measures at once. The BPA rule @kb.bpa-expression-required flags measures with an empty expression.

### Format String Expression
`FormatStringExpression` · string · Options · compatibility level 1601+

A DAX expression that returns the format string to use, for example to show a different currency symbol per country or to show large values in thousands or millions. This is known as a *dynamic format string*. Inside the expression, refer to the measure's own value with `SELECTEDMEASURE()` or by the measure's name.

A measure can't have both a `FormatString` and a `FormatStringExpression`. In Tabular Editor 3, setting `FormatStringExpression` clears `FormatString` in the same undo step. When both are set, for example by a C# script, Tabular Editor 3 shows the error "A measure is not allowed to have both its FormatString and FormatStringExpression property assigned" on the measure. To go back to a static format, clear `FormatStringExpression` first and then set `FormatString`.

For the error "A measure is not allowed to have both FormatString and Format Expression" in a composite model on Analysis Services, see @composite-model-measure-formatting.

### Detail Rows Expression
`DetailRowsExpression` · string · Options · compatibility level 1400+

A DAX table expression that defines the rows a user sees when they drill through on a value of this measure, for example with **Show Details** in an Excel PivotTable. The expression is evaluated in the filter context of the cell that was drilled into. For example, `SELECTCOLUMNS ( Sales, "Order", Sales[OrderNumber], "Amount", Sales[Amount] )` returns the order number and amount of each sale. When the property is empty, drill-through returns the rows of the underlying table with the table's default columns.

Power BI doesn't use this property. To set a default for all measures in a table, use `DefaultDetailRowsExpression` on the table (see @object-properties-tables). For a step-by-step example, see @detail-rows-expression.

### Data Category
`DataCategory` · string · Options · compatibility level 1455+

The kind of value the measure returns, which client tools use to display the value. For example, Power BI shows the returned URL as an image when the category is `ImageUrl`, and as a link when it's `WebUrl`. Measures use the same categories as columns. See `DataCategory` on @object-properties-columns.

### KPI
`KPI` · KPI · Options

The KPI attached to this measure, if there is one. A KPI adds a target, a status and a trend to the measure. See [KPI](#kpi-1) below.

In Tabular Editor 3, to add a KPI from the Properties view, select **...** on the empty `KPI` property, or right-click the property and select **Add KPI**. To remove it, right-click the property and select **Remove KPI**.

Tabular Editor 2 works the same way. In Tabular Editor 2, you can also right-click the measure in the **TOM Explorer** and select **Create New > KPI**. The KPI then appears under the measure, where you can delete it.

## KPI

A key performance indicator (KPI) extends a measure with a target value, a status that compares the measure to the target and a trend. Excel and SQL Server Management Studio show KPIs with status and trend icons. Power BI doesn't show KPIs defined in the model and has its own KPI visual.

A KPI always belongs to a single measure, and the measure's own value is the KPI's *value*. The KPI has no name of its own.

To add a KPI in Tabular Editor 3, right-click a measure and select **Create > KPI**. A DAX script can also define a measure together with its KPI. See @dax-scripts.

### Common properties

- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Parent Measure
`MeasureName` · string · Metadata · read-only · *shortcut to* the name of the measure

The name of the measure this KPI belongs to.

### Measure
`Measure` · Measure · Options · read-only

The measure this KPI belongs to. C# scripts use it to get from the KPI to its measure. Tabular Editor 3 hides this property in the Properties view and shows `MeasureName` there.

### Target Expression
`TargetExpression` · string · Options

A DAX expression that returns the goal for the measure, for example a fixed number such as `1000000`, another measure such as `[Sales Budget]` or a calculation.

### Target Format String
`TargetFormatString` · string · Options

The format string for the target value, with the same syntax as `FormatString` on a measure.

### Target Description
`TargetDescription` · string · Options

A description of the target, shown to users in client tools that support it.

### Status Expression
`StatusExpression` · string · Options

A DAX expression that compares the measure to the target and returns a number between `-1` and `1`, where `-1` is bad, `0` is neutral and `1` is good. Client tools use this number to pick the icon from `StatusGraphic`. For example:

```dax
VAR Ratio = DIVIDE ( [Total Sales], [Sales Budget] )
RETURN
    SWITCH ( TRUE (), Ratio >= 1, 1, Ratio >= 0.9, 0, -1 )
```

### Status Graphic
`StatusGraphic` · string · Options

The icon set that client tools use to show the status, for example `Traffic Light` or `Shapes`, as a name that the client tool recognizes.

In Tabular Editor 3, pick a name from the list or type any other value. Tabular Editor 3 accepts any value. The list contains `Cylinder`, `Faces`, `Five Bars Colored`, `Five Boxes Colored`, `Gauge`, `Gauge - Ascending`, `Gauge - Descending`, `Reversed Gauge`, `Reversed status arrow`, `Road Signs`, `Shapes`, `Smiley`, `Smiley Face`, `Standard Arrow`, `Status Arrow`, `Status Arrow - Ascending`, `Status Arrow - Descending`, `Thermometer`, `Three Circles Colored`, `Three Flags Colored`, `Three Stars Colored`, `Three Symbols Uncircled Colored`, `Three Triangles`, `Traffic Light`, `Traffic Light - Single` and `Variance Arrow`.

Excel recognizes only a few of these names. In an Excel PivotTable, these names show their own status icon:

| Status Graphic | What Excel shows |
|---|---|
| `Road Signs` | A check mark when the status is good |
| `Traffic Light` | A traffic light |
| `Standard Arrow` | A grey arrow |
| `Status Arrow - Ascending`, `Variance Arrow` | A colored arrow that points up when the status is good |
| `Status Arrow - Descending` | A colored arrow that points down when the status is good |
| `Gauge - Ascending`, `Gauge - Descending` | A dark or an empty circle |

All other names, including `Shapes`, `Thermometer`, `Smiley`, `Cylinder` and names that Excel doesn't know, show a plain colored circle.

### Status Description
`StatusDescription` · string · Options

A description of the status, shown to users in client tools that support it.

### Trend Expression
`TrendExpression` · string · Options

A DAX expression that returns a number between `-1` and `1` that shows whether the measure gets worse (`-1`), stays the same (`0`) or gets better (`1`) over time, for example compared to the previous period.

### Trend Graphic
`TrendGraphic` · string · Options

The icon set that client tools use to show the trend, for example `Standard Arrow`, as a name that the client tool recognizes. In Tabular Editor 3, pick it from the same list of names as `StatusGraphic`, or type any other value.

In Excel, most names show a colored arrow, `Standard Arrow` shows a grey arrow and `Status Arrow - Descending` shows an arrow that points down when the trend is good. A few names, such as `Cylinder`, `Smiley Face` and `Traffic Light - Single`, show a circle.

### Trend Description
`TrendDescription` · string · Options

A description of the trend, shown to users in client tools that support it.
