---
uid: kb.bpa-data-column-source
title: Data Column Must Have Source
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring data columns have a valid source column mapping to prevent refresh errors.
---

# Data Column Must Have Source

## Overview

This best practice rule identifies data columns that lack a valid `SourceColumn` property. Every data column must reference a source column from the underlying data source to function correctly during refresh.

- Category: **Error Prevention**
- Severity: High (3)

## Applies To

- Data Columns

## Why This Matters

- **Refresh failures**: Data refresh operations fail with column not found errors
- **Deployment issues**: Model validation fails in Power BI Service or Analysis Services
- **Data integrity**: Column remains empty or contains stale data
- **Broken dependencies**: Measures and relationships produce incorrect results

## When This Rule Triggers

The rule triggers when a data column has:

```csharp
string.IsNullOrWhitespace(SourceColumn)
```

## How to Fix

### Manual Fix

1. In **TOM Explorer**, locate the flagged data column
2. In **Properties** pane, find the `Source Column` property
3. Enter the correct source column name from your data source query
4. Verify the mapping matches the partition query

The source column name must exactly match:
- For Power Query: Column name in M expression output
- For SQL: Column name or alias in SELECT statement
- For Direct Lake: Column name in Delta Lake table

## Common Causes

### Cause 1: Renamed Source Column

Source query was modified and column renamed.

### Cause 2: Manual Column Creation

Column created manually without specifying source.

### Cause 3: Copy/Paste Corruption

Columns copied from another table without preserving metadata.

## Example

### Before Fix

```
Table: Sales
Column: ProductName (DataColumn)
  SourceColumn: [empty]
```

Result: Refresh fails with "Column 'ProductName' not found in source query"

### After Fix

```
Table: Sales
Column: ProductName (DataColumn)
  SourceColumn: ProductName
```

Result: Column populates correctly during refresh

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Expression Required for Calculated Objects](xref:kb.bpa-expression-required) - Ensuring calculated columns have expressions
