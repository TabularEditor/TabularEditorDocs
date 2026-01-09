---
uid: kb.bpa-relationship-same-datatype
title: Relationship Columns Must Have Same Data Type
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring relationships connect columns with matching data types to prevent errors and performance issues.
---

# Relationship Columns Must Have Same Data Type

## Overview

This best practice rule identifies relationships where the connected columns have mismatched data types. Both columns in a relationship must share the same data type to ensure proper filtering, prevent errors, and maintain optimal query performance.

- Category: Error Prevention

- Severity: High (3)

## Applies To

- Relationships

## Why This Matters

Relationships with mismatched data types cause serious problems:

- **Model validation errors**: The model may fail to save or deploy
- **Relationship creation failures**: Power BI and Analysis Services may reject the relationship
- **Implicit conversions**: Expensive data type conversions on every query
- **Incorrect results**: Type coercion leads to unexpected filtering behavior
- **Performance degradation**: Converting data types during queries slows execution
- **Memory overhead**: Additional memory required for conversion buffers

## When This Rule Triggers

The rule triggers when:

```csharp
FromColumn.DataType != ToColumn.DataType
```

This detects relationships connecting columns with different data types.

## How to Fix

### Manual Fix

1. Identify which column should change data type
2. Change the data type in **Power Query**, in the underlying data source or in the model
3. Delete the existing relationship
4. Create a new relationship between the corrected columns
5. Verify filtering works correctly

## Common Causes

### Cause 1: Inconsistent Data Type Choices

Different data types chosen for the same logical key during import or table creation.

### Cause 2: Source System Differences

Foreign keys imported from different source systems with different type conventions.

### Cause 3: DateTime vs Date Mismatch

Fact tables using DateTime columns while date dimensions use Date type.

## Example

### Before Fix

```
Relationship: Sales[CustomerID] (Int64) → Customers[CustomerID] (String)
```

**Error**: Relationship fails validation or creates performance issues with implicit conversion

### After Fix

```
Relationship: Sales[CustomerID] (Int64) → Customers[CustomerID] (Int64)
```

**Result**: Relationship works efficiently with no type conversion overhead

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Many-to-Many Relationships Should Use Single Direction](xref:kb.bpa-many-to-many-single-direction) - Relationship performance optimization
