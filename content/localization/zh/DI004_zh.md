---
uid: DI004
category: Code actions
sub-category: Improvements
title: Add table name
author: Daniel Otykier
updated: 2024-12-19
---

Code action `DI004` (Improvement) **Add table name to column references**

## Description

Column references should always include the table name to avoid ambiguities, even when the table name is optional.

## Example

Change:

```dax
SUMX('Internet Sales', [Line Amount] * [Quantity])
```

To:

```dax
SUMX('Internet Sales', 'Internet Sales'[Line Amount] * 'Internet Sales'[Quantity])
```

## Why is Tabular Editor suggesting this?

Since _measure_ names are always unique within a model, it is always possible to reference a measure without specifying the table name. However, column names are not unique within a model, and it is therefore necessary to specify the table name when referencing a column, such as when using one of the aggregation functions, i.e.: `SUM('Sales'[Amount])`.

However, there are situations in which the table qualifier is optional for column references. For example, this is the case when the column exists within an active row context (such as inside a [Calculated Column](https://learn.microsoft.com/en-us/analysis-services/tabular-models/ssas-calculated-columns-create-a-calculated-column?view=asallproducts-allversions)). Even so, providing the table name in this case is still valid, and helps avoid ambiguities and errors in case a measure with the same name is eventually added to the model.

By applying this practice consistently, you make your code more concise and easier to read, and you make it easier to distinguish between measure references and column references.

## Remarks

This code action has an **(All occurrences)** variant, which will appear when multiple sections of code can be improved. This variant will apply the code action to all relevant sections of the document at once.

## Related to:

- [DI003 - Remove table name from measure references](xref:DI003)