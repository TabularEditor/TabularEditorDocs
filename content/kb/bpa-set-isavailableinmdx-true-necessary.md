---
uid: kb.bpa-set-isavailableinmdx-true-necessary
title: Set IsAvailableInMDX to True When Necessary
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule preventing query errors by ensuring columns used in hierarchies and relationships have MDX availability enabled.
---

# Set IsAvailableInMDX to True When Necessary

## Overview

This best practice rule identifies columns that have `IsAvailableInMDX` set to `false` but are actually used in scenarios requiring MDX access. These columns must have MDX availability enabled to function correctly in hierarchies, relationships, and sort operations.

<<<<<<< HEAD
- Category: Error Prevention
=======
- Category: **Error Prevention**
>>>>>>> Added Knowledge base for built in BPA rules
- Severity: High (3)

## Applies To

- Data Columns
- Calculated Columns
- Calculated Table Columns

## Why This Matters

When a column is used in certain model structures, the Analysis Services engine requires MDX access to that column. Disabling MDX access for columns that need it causes:

- **Query failures**: Hierarchies and sort operations fail with errors
- **Broken visualizations**: Charts and tables using affected hierarchies display errors
- **Relationship problems**: MDX queries against relationships may fail
- **Calendar/variation errors**: Time intelligence features break
- **Unpredictable behavior**: Some queries work while others fail depending on client tool

Columns need `IsAvailableInMDX = true` when they are:
- Used in hierarchies as levels
- Referenced as sort-by columns
- Used in variations (alternate hierarchies)
- Part of calendar definitions
- Serving as sort-by targets for other columns

## When This Rule Triggers

The rule triggers when a column has `IsAvailableInMDX = false` AND any of these conditions are true:

```csharp
IsAvailableInMDX = false
and
(
    UsedInSortBy.Any()
    or
    UsedInHierarchies.Any()
    or
    UsedInVariations.Any()
    or
    UsedInCalendars.Any()
    or
    SortByColumn != null
)
```

The rule checks these dependency collections:

| Property | Description | Example Usage |
|----------|-------------|---------------|
| `UsedInHierarchies` | Hierarchies where column is a level | Product hierarchy levels |
| `UsedInSortBy` | Columns using this as sort key | Month names sorted by month number |
| `UsedInVariations` | Alternate hierarchies using column | Product variations |
| `UsedInCalendars` | Calendar metadata references | Date table calendar definitions |
| `SortByColumn` | Column sorts by another column | This column has a sort-by reference |

## How to Fix

### Automatic Fix

This rule includes an automatic fix:

```csharp
IsAvailableInMDX = true
```

To apply:
1. In the **Best Practice Analyzer** select flagged objects
3. Click **Apply Fix**

### Manual Fix

1. In **TOM Explorer**, locate the flagged column
2. In **Properties** pane, find `IsAvailableInMDX`
3. Set the value to `true`
4. Save and test affected hierarchies/sorts

## Common Scenarios

### Scenario 1: Hierarchy Level Column

**Problem**: A column used as a hierarchy level has MDX disabled

```dax
Hierarchy: Geography
  Levels:
    - Country
    - State (IsAvailableInMDX = false)  ← Problem
    - City
```

**Error**: "The hierarchy 'Geography' cannot be used because one of its levels is not available in MDX."

**Solution**: Set `State[IsAvailableInMDX] = true`

### Scenario 2: Sort-By Column

**Problem**: A column serving as a sort-by target has MDX disabled

```
Month Name column:
  - SortByColumn = MonthNumber
  - MonthNumber.IsAvailableInMDX = false  ← Problem
```

**Error**: Months display in alphabetical order instead of calendar order

**Solution**: Set `MonthNumber[IsAvailableInMDX] = true`

### Scenario 3: Calendar Definition

**Problem**: A date column used in calendar metadata has MDX disabled

```
DateTable:
  - Calendar uses DateKey column
  - DateKey.IsAvailableInMDX = false  ← Problem
```

**Error**: Time intelligence functions fail

**Solution**: Set `DateKey[IsAvailableInMDX] = true`

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Set IsAvailableInMDX to False](xref:kb.bpa-set-isavailableinmdx-false) - The complementary optimization rule
