---
uid: kb.bpa-do-not-summarize-numeric
title: Set SummarizeBy to None for Numeric Columns
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule preventing incorrect default aggregations on numeric columns that should not be summed.
---

# Set SummarizeBy to None for Numeric Columns

## Overview

This best practice rule identifies visible numeric columns (Int64, Decimal, Double) that have a default aggregation behavior (`SummarizeBy`) other than `None`. Most numeric columns should not be automatically aggregated, as summing values like IDs, quantities in non-additive contexts, or codes produces meaningless results.

<<<<<<< HEAD
- Category: Formatting
=======
- Category: **Formatting**
>>>>>>> Added Knowledge base for built in BPA rules

- Severity: High (3)

## Applies To

- Data Columns
- Calculated Columns
- Calculated Table Columns

## Why This Matters

Default aggregation on inappropriate columns causes serious issues:

- **Incorrect analysis**: Users get meaningless totals (sum of CustomerIDs, etc.)
- **Misleading dashboards**: Visualizations show wrong numbers by default
- **User confusion**: Users must manually change aggregation for every visual
- **Wrong decisions**: Business decisions based on incorrect automatic aggregations
- **Data credibility**: Users lose trust in the model and data

Common columns that should NOT be aggregated include IDs, keys, codes, ratios, percentages, and non-additive quantities.

## When This Rule Triggers

The rule triggers when a column meets ALL these conditions:

```csharp
(DataType = "Int64" or DataType="Decimal" or DataType="Double")
and
SummarizeBy <> "None"
and not (IsHidden or Table.IsHidden)
```

In other words: visible numeric columns that have a summarization behavior other than "None".

## How to Fix

### Automatic Fix

This rule includes an automatic fix:

```csharp
SummarizeBy = AggregateFunction.None
```

To apply:
1. In the **Best Practice Analyzer** select flagged objects
3. Click **Apply Fix**

### Manual Fix

1. In **TOM Explorer**, locate the column
2. In **Properties** pane, find **Summarize By**
3. Change from **Sum**, **Average**, **Min**, **Max**, **Count**, or **DistinctCount** to **None**
4. Save changes

## Common Causes

### Cause 1: Default Import Behavior

Numeric columns default to Sum aggregation during import.

### Cause 2: Lack of Column Review

Models deployed without reviewing column aggregation settings.

### Cause 3: ID Columns Not Hidden

Numeric ID columns remain visible with default Sum aggregation.

## Example

### Before Fix

```
Column: CustomerID
  DataType: Int64
  SummarizeBy: Sum
```

**Result**: Visual shows "Sum of CustomerID: 12,456,789" (meaningless number)

### After Fix

```
Column: CustomerID
  DataType: Int64
  SummarizeBy: None
```

**Result**: Visual requires explicit aggregation or shows individual Customer IDs

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Hide Foreign Keys](xref:kb.bpa-hide-foreign-keys) - Related column hygiene rule
- [Format String for Columns](xref:kb.bpa-format-string-columns) - Column formatting

## Learn More

- [Column Properties](https://learn.microsoft.com/analysis-services/tabular-models/column-properties-ssas-tabular)
- [When to Use Measures vs. Calculated Columns](https://learn.microsoft.com/power-bi/transform-model/desktop-tutorial-create-measures)
