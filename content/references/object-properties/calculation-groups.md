---
uid: object-properties-calculation-groups
title: Calculation group properties
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
# Calculation group properties

<!--
SUMMARY: Reference for the properties of calculation groups and calculation items.
-->

This page covers the properties of calculation groups and calculation items. A calculation group always lives in a calculation group table. The properties of that table, including shortcuts to the calculation group's own properties, are on @object-properties-tables. For properties that most objects share, see @object-properties-common.

## Calculation group

A calculation group is a set of calculation items that change how measures are calculated. For example, a time intelligence calculation group can have the items `Current`, `YTD` and `Prior year`. When a report author puts the calculation group's column in a slicer and selects `YTD`, every measure in the visual shows its year-to-date value, without the need for a separate YTD measure per measure.

A calculation group has no name of its own: it's identified by the calculation group table it belongs to. You can't select the calculation group itself in the TOM Explorer. You work with the calculation group table, and the Properties view shows the calculation group's properties on that table as **Calculation Group Description**, **Calculation Group Annotations** and **Calculation Group Precedence** (see @object-properties-tables). In C# scripts, you reach the calculation group object through `CalculationGroupTable.CalculationGroup`.

In Tabular Editor 3, you create a calculation group by right-clicking the model or the **Tables** folder and choosing **Create > Calculation Group**. Microsoft documents calculation groups for compatibility level 1500 or higher, which includes all Power BI semantic models. Tabular Editor 3 offers the menu option from compatibility level 1470, the level at which TOM added calculation groups. See @creating-and-testing-dax.

### Common properties

- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Object Type](xref:object-properties-common#object-type)

### Options

#### Precedence
`Precedence` · int

The order in which calculation groups are applied when a query uses items from more than one calculation group, for example a time intelligence group and a currency conversion group. The calculation group with the highest precedence is applied first. In practice this means its calculation item is the outermost one: where it calls `SELECTEDMEASURE()`, the engine uses the result of the calculation item from the group with the next lower precedence, and so on down to the measure.

The order matters whenever the calculation items don't commute. For example, with a time intelligence group that has a `YTD` item and a group that has an `Average per day` item, you get a different result for "year-to-date of the daily average" than for "daily average of the year-to-date value".

For example, with a calculation group at precedence `200` whose item is `SELECTEDMEASURE () * 2`, and one at precedence `100` whose item is `SELECTEDMEASURE () + 2`, selecting both items on a measure that returns `10` gives `( 10 + 2 ) * 2 = 24`, not `10 * 2 + 2 = 22`.

Give each calculation group in the model a different precedence. The TOM default is `0`. When you add a calculation group in Tabular Editor, or paste one, and its precedence is already used by another calculation group in the model, Tabular Editor sets it to one more than the highest precedence in the model. In Tabular Editor, you can also set it on the calculation group table as **Calculation Group Precedence**.

The engine rejects a model in which two calculation groups have the same precedence, with an error like *Calculation Group precedence must be greater or equal zero and unique within Model*. The precedence can't be negative either.

In a Tabular Editor 3 @dax-scripts document, you set it with the `Precedence` property of the calculation group.

## Calculation item

A calculation item is one entry of a calculation group, for example `YTD`. Its name is the value report authors see in the calculation group's column, and its expression says how to change the measure when the item is selected. Inside the expression, `SELECTEDMEASURE()` stands for whichever measure is being evaluated.

If a calculation group has no calculation items, it does nothing. The Best Practice Analyzer rule @kb.bpa-calculation-groups-no-items flags calculation groups that contain no items.

The **Description** of a calculation item is for developers only: Power BI Desktop doesn't show it, for example when a report author hovers over the item in a slicer.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)

### Basic

#### Ordinal
`Ordinal` · int · compatibility level 1500+

The position of the calculation item within its calculation group, starting at `0`. Client tools use it to sort the items, for example in a slicer, so that `Current`, `MTD`, `QTD` and `YTD` appear in that order instead of alphabetically. The engine exposes it through the ordinal column of the calculation group table. The value `-1` means the item has no position. According to Microsoft, items with `-1` aren't included in the ordering and appear before the ordered items in a report. If no item has an ordinal, client tools sort the items alphabetically.

You don't normally set the value by hand. Tabular Editor 3 keeps the ordinals of a calculation group numbered `0`, `1`, `2` and so on, without gaps or duplicates:

- When you drag calculation items into a different order in the TOM Explorer, Tabular Editor renumbers all items in the group.
- When you type a new **Ordinal** in the Properties view, Tabular Editor moves the item to that position and renumbers the other items. If you type `-1`, Tabular Editor sets the ordinal of every item in the group to `-1`, which removes the custom order.
- When you add a calculation item, it gets the next number after the highest ordinal in the group. If no item in the group has an ordinal yet, the new item doesn't get one either.

You can only set **Ordinal** for one calculation item at a time.

Tabular Editor 2 renumbers the ordinals in the same way: when you drag calculation items into a different order in the TOM Explorer, or type a new **Ordinal**, it numbers all items in the group `0`, `1`, `2` and so on.

You can also drag calculation items onto another calculation group to move them there. See @drag-drop.

### Options

#### Expression
`Expression` · string

The DAX expression that's evaluated instead of the measure when this calculation item is selected. Use `SELECTEDMEASURE()` to refer to the measure. For example, a year-to-date item:

```dax
CALCULATE ( SELECTEDMEASURE (), DATESYTD ( 'Date'[Date] ) )
```

And an item that leaves the measure unchanged, which is useful as a default:

```dax
SELECTEDMEASURE ()
```

The expression applies to every measure in the query, including measures that return text or that shouldn't be affected. To limit it to some measures, test the measure with `ISSELECTEDMEASURE` or `SELECTEDMEASURENAME`, for example:

```dax
IF (
    ISSELECTEDMEASURE ( [Total Sales], [Total Cost] ),
    CALCULATE ( SELECTEDMEASURE (), DATESYTD ( 'Date'[Date] ) ),
    SELECTEDMEASURE ()
)
```

Calculation items apply to measures only, not to columns that are aggregated implicitly. That's why Power BI turns on **Discourage Implicit Measures** on the model when you add a calculation group (see @object-properties-model).

In Tabular Editor 3, you write the expression in the Expression Editor of the @dax-editor, with auto-complete and parameter info.

#### Format String Expression
`FormatStringExpression` · string

A DAX expression that returns the format string to use for the measure when this calculation item is selected. Leave it empty to keep the measure's own format. Use it when the item changes what kind of value the measure returns, for example a year-over-year percentage:

```dax
"0.0%"
```

Or when the format depends on the context, for example a currency symbol. Inside the expression, `SELECTEDMEASUREFORMATSTRING()` returns the format string the measure would otherwise use, so you can fall back to it. For example, with a `Currency` table that has a `Format` column:

```dax
SELECTEDVALUE ( 'Currency'[Format], SELECTEDMEASUREFORMATSTRING () )
```

The expression must return a single text value. There's no separate compatibility level requirement: format string expressions on calculation items are available wherever calculation groups are. When several calculation groups apply to a measure, only the format string expression of the calculation group with the highest precedence is used. To remove the expression, clear the value.
