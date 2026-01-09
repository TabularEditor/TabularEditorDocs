---
uid: kb.bpa-calculation-groups-no-items
title: Calculation Groups Should Contain Items
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule identifying calculation groups without calculation items that should be populated or removed.
---

# Calculation Groups Should Contain Items

## Overview

This best practice rule identifies calculation groups that contain no calculation items. Empty calculation groups serve no purpose and should be populated or removed.

<<<<<<< HEAD
- Category: Maintenance
=======
- Category: **Maintenance**
>>>>>>> Added Knowledge base for built in BPA rules
- Severity: Medium (2)

## Applies To

- Calculation Groups

## Why This Matters

- **Deployment errors**: Empty groups may fail validation in Power BI Service
- **Model errors**: Can cause unexpected behavior in DAX calculations
- **Developer confusion**: Team members waste time investigating incomplete structures
- **Performance overhead**: Engine processes unnecessary metadata

## When This Rule Triggers

The rule triggers when a calculation group has zero calculation items:

```csharp
CalculationItems.Count == 0
```

## How to Fix

### Option 1: Add Calculation Items

If the calculation group has a valid business purpose:

1. In **TOM Explorer**, expand the calculation group table
2. Expand the **Calculation Group** column
3. Right-click and select **Add Calculation Item**
4. Define the calculation item expression

### Option 2: Delete the Calculation Group

If no longer needed:

1. In **TOM Explorer**, locate the calculation group table
2. Right-click the table
3. Select **Delete**

## Common Causes

### Cause 1: Incomplete Development

Calculation group created during planning but not yet implemented.

### Cause 2: Migration from Other Models

Calculation group structure copied without items.

### Cause 3: Refactoring

All calculation items moved to a different calculation group.

## Example

### Before Fix

```
Calculation Group: Time Intelligence
  Items: (none)  ← Problem
```

### After Fix

```
Calculation Group: Time Intelligence
  Items:
    - Current Period: SELECTEDMEASURE()
    - Year-to-Date: CALCULATE(SELECTEDMEASURE(), DATESYTD('Date'[Date]))
    - Prior Year: CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
```

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Perspectives Should Contain Objects](xref:kb.bpa-perspectives-no-objects) - Similar rule for empty perspectives
- [Expression Required](xref:kb.bpa-expression-required) - Ensuring calculation items have expressions

## Learn More

- [Calculation Groups in Tabular Models](https://learn.microsoft.com/analysis-services/tabular-models/calculation-groups)
- [Creating Calculation Groups](https://www.sqlbi.com/articles/introducing-calculation-groups/)
- [Calculation Group Patterns](https://www.sqlbi.com/calculation-groups/)
