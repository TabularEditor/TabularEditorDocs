---
uid: kb.bpa-set-isavailableinmdx-false
title: Set IsAvailableInMDX to False
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule to optimize performance by disabling MDX access for hidden columns that are not used in relationships or hierarchies.
---

# Set IsAvailableInMDX to False

## Overview

This best practice rule identifies hidden columns that have the `IsAvailableInMDX` property set to `true` but don't need to be accessible through MDX queries. Setting this property to `false` for unused hidden columns can improve query performance and reduce memory overhead.

<<<<<<< HEAD
- Category: Performance
=======
- Category: **Performance**
>>>>>>> Added Knowledge base for built in BPA rules
- Severity: Medium (2)

## Applies To

- Data Columns
- Calculated Columns
- Calculated Table Columns

## Why This Matters

When a column has `IsAvailableInMDX` set to `true`, the Analysis Services engine maintains additional metadata and structures to support MDX queries against that column. For hidden columns that aren't used in relationships, hierarchies, variations, calendars, or as sort-by columns, this overhead is unnecessary and can:

- Increase memory consumption
- Slow down query processing
- Add complexity to the model metadata

By explicitly setting `IsAvailableInMDX` to `false` for these columns, you optimize the model for DAX-only scenarios, which is the primary query language for Power BI and modern Analysis Services models.

## When This Rule Triggers

The rule triggers when all of the following conditions are met:

1. The column has `IsAvailableInMDX = true`
2. The column is hidden (or its table is hidden)
3. The column is NOT used in any `SortBy` relationships
4. The column is NOT used in any hierarchies
5. The column is NOT used in any variations
6. The column is NOT used in any calendars
7. The column is NOT serving as a `SortByColumn` for another column

## How to Fix

### Automatic Fix

This rule includes an automatic fix expression. When you apply the fix in the Best Practice Analyzer:

```csharp
IsAvailableInMDX = false
```
To apply:
1. In the **Best Practice Analyzer** select flagged objects
3. Click **Apply Fix**

### Manual Fix

1. In the **TOM Explorer**, locate the flagged column
2. In the **Properties** pane, find the `IsAvailableInMDX` property
3. Set the value to `false`
4. Save your changes

## Example

Consider a hidden calculated column used only for intermediate calculations:

```dax
_TempCalculation = 
CALCULATE(
    SUM('Sales'[Amount]),
    ALLEXCEPT('Sales', 'Sales'[ProductKey])
)
```

If this column is:
- Hidden from client tools
- Not used in any hierarchies or relationships
- Not referenced by sort operations

Then setting `IsAvailableInMDX = false` is recommended for optimal performance.

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Set IsAvailableInMDX to True When Necessary](xref:kb.bpa-set-isavailableinmdx-true-necessary) - The complementary rule ensuring columns that need MDX access have it enabled
