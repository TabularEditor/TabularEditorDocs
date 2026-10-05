---
uid: object-properties-calculation-groups
title: Calculation group properties
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
# Calculation group properties

<!--
SUMMARY: Reference for the properties of calculation groups and calculation items.
-->

This page covers the properties of calculation groups and calculation items. A calculation group always belongs to a calculation group table. The properties of that table, including shortcuts to the calculation group's own properties, are on @object-properties-tables. For properties that most objects share, see @object-properties-common.

## Calculation group

A calculation group is a set of calculation items that change how measures are calculated. For example, a time intelligence calculation group can have the items `Current`, `YTD` and `Prior year`. When a report author puts the calculation group's column in a slicer and selects `YTD`, every measure in the visual shows its year-to-date value, without a separate YTD measure for each measure.

A calculation group has no name of its own and is identified by its calculation group table. You can't select the calculation group in the **TOM Explorer**. Select the calculation group table, where the **Properties** view shows the calculation group's properties as `CalculationGroupDescription`, `CalculationGroupAnnotations` and `CalculationGroupPrecedence` (see @object-properties-tables). In C# scripts, you reach the calculation group object through `CalculationGroupTable.CalculationGroup`.

In Tabular Editor 3, you create a calculation group by right-clicking the model or the **Tables** folder and choosing **Create > Calculation Group**. Microsoft documents calculation groups for compatibility level 1500 or higher, which includes all Power BI semantic models. Tabular Editor 3 shows the menu option from compatibility level 1470, the level at which the Tabular Object Model (TOM) added calculation groups. See @creating-and-testing-dax.

### Common properties

- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Object Type](xref:object-properties-common#object-type)

### Precedence
`Precedence` · int · Options

The order in which calculation groups are applied when a query uses items from more than one calculation group, for example a time intelligence group and a currency conversion group. The calculation group with the highest precedence is applied first, which makes its calculation item the outermost one. Where that item calls [SELECTEDMEASURE](https://dax.guide/selectedmeasure), the engine uses the result of the calculation item from the group with the next lower precedence, and so on down to the measure.

The order changes the result when the calculation items don't commute. With a time intelligence group that has a `YTD` item and a group that has an `Average per day` item, the year-to-date of the daily average differs from the daily average of the year-to-date value. In this example, a calculation group at precedence `200` has the item `SELECTEDMEASURE () * 2` and one at precedence `100` has the item `SELECTEDMEASURE () + 2`. Selecting both items on a measure that returns `10` gives `( 10 + 2 ) * 2 = 24`.

The TOM default is `0`. Give each calculation group in the model a different precedence of `0` or higher. The engine rejects a model in which two calculation groups have the same precedence, with an error like "Calculation Group precedence must be greater or equal zero and unique within Model".

When you add or paste a calculation group whose precedence another calculation group in the model already uses, Tabular Editor sets it to one more than the highest precedence in the model. You can also set it on the calculation group table as `CalculationGroupPrecedence`. In a Tabular Editor 3 @dax-scripts document, you set it with the `Precedence` property of the calculation group.

## Calculation item

A calculation item is one entry of a calculation group, for example `YTD`. Report authors see its name as a value in the calculation group's column, and its expression sets how the measure changes when the item is selected. Inside the expression, [SELECTEDMEASURE](https://dax.guide/selectedmeasure) returns the measure that's being evaluated.

A calculation group without calculation items has no effect. The Best Practice Analyzer (BPA) rule @kb.bpa-calculation-groups-no-items flags calculation groups that contain no items.

The `Description` of a calculation item is for developers only. Power BI Desktop doesn't show it, for example when a report author hovers over the item in a slicer.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)

### Ordinal
`Ordinal` · int · Basic · compatibility level 1500+

The position of the calculation item within its calculation group, starting at `0`. Client tools sort the items by it, for example to show `Current`, `MTD`, `QTD` and `YTD` in that order in a slicer. The engine exposes it through the ordinal column of the calculation group table.

The value `-1` means the item has no position. According to Microsoft, items with `-1` aren't included in the ordering and appear before the ordered items in a report. If no item has an ordinal, client tools sort the items alphabetically.

Tabular Editor 3 keeps the ordinals of a calculation group numbered `0`, `1`, `2` and so on, without gaps or duplicates:

- when you drag calculation items into a different order in the **TOM Explorer**, Tabular Editor renumbers all items in the group
- when you type a new `Ordinal` in the **Properties** view, Tabular Editor moves the item to that position and renumbers the other items
- when you type `-1`, Tabular Editor sets the ordinal of every item in the group to `-1`, which removes the custom order
- when you add a calculation item, it gets the next number after the highest ordinal in the group, unless no item in the group has an ordinal yet

You can set `Ordinal` for one calculation item at a time. Tabular Editor 2 renumbers the ordinals in the same way when you drag calculation items into a different order in the **TOM Explorer** or type a new `Ordinal`.

You can also drag calculation items onto another calculation group to move them there. See @drag-drop.

### Expression
`Expression` · string · Options

The DAX expression that the engine evaluates in place of the measure when this calculation item is selected. Use [SELECTEDMEASURE](https://dax.guide/selectedmeasure) to refer to the measure. This is a year-to-date item:

```dax
CALCULATE ( SELECTEDMEASURE (), DATESYTD ( 'Date'[Date] ) )
```

This item leaves the measure unchanged and works as a default:

```dax
SELECTEDMEASURE ()
```

The expression applies to every measure in the query, including measures that return text. To limit it to some measures, test the measure with [ISSELECTEDMEASURE](https://dax.guide/isselectedmeasure) or [SELECTEDMEASURENAME](https://dax.guide/selectedmeasurename), for example:

```dax
IF (
    ISSELECTEDMEASURE ( [Total Sales], [Total Cost] ),
    CALCULATE ( SELECTEDMEASURE (), DATESYTD ( 'Date'[Date] ) ),
    SELECTEDMEASURE ()
)
```

Calculation items apply to measures only, and columns that are aggregated implicitly aren't affected. Power BI turns on `DiscourageImplicitMeasures` on the model when you add a calculation group (see @object-properties-model).

In Tabular Editor 3, you write the expression in the **Expression Editor** of the @dax-editor, with auto-complete and parameter info.

### Format String Expression
`FormatStringExpression` · string · Options

A DAX expression that returns the format string for the measure when this calculation item is selected. Leave it empty to keep the measure's own format. Set it when the item changes the kind of value the measure returns, for example a year-over-year percentage:

```dax
"0.0%"
```

You can also make the format depend on the context, for example a currency symbol. Inside the expression, [SELECTEDMEASUREFORMATSTRING](https://dax.guide/selectedmeasureformatstring) returns the measure's own format string, which you can use as a fallback. This example uses a `Currency` table with a `Format` column:

```dax
SELECTEDVALUE ( 'Currency'[Format], SELECTEDMEASUREFORMATSTRING () )
```

The expression must return a single text value. Format string expressions on calculation items have no separate compatibility level requirement and are available wherever calculation groups are. When several calculation groups apply to a measure, the engine uses only the format string expression of the calculation group with the highest precedence. To remove the expression, clear the value.
