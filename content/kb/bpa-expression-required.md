---
uid: kb.bpa-expression-required
title: Expression Required for Calculated Objects
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring measures, calculated columns, and calculation items have valid DAX expressions.
---

# Expression Required for Calculated Objects

## Overview

This best practice rule identifies measures, calculated columns, and calculation items that lack a DAX expression. All calculated objects must have a valid, non-empty expression to function correctly and prevent errors during model deployment and query execution.

- Category: **Error Prevention**

- Severity: High (3)

## Applies To

- Measures
- Calculated Columns
- Calculation Items

## Why This Matters

Calculated objects without expressions will cause critical failures:

- **Model validation errors**: The model will fail validation when saved or deployed
- **Query failures**: Attempts to use the object in queries will generate errors
- **Broken dependencies**: Other measures or calculations referencing the object will fail
- **Deployment blockers**: Power BI Service and Analysis Services will reject models with empty expressions
- **Unexpected behavior**: The object may appear in field lists but produce no results

Empty expressions typically result from incomplete object creation, copy/paste operations, or programmatic model generation errors.

## When This Rule Triggers

The rule triggers when any of the following objects have an empty or whitespace-only expression:

```csharp
string.IsNullOrWhiteSpace(Expression)
```

This applies to:
- **Measures**: Should contain a DAX aggregation or calculation
- **Calculated Columns**: Should contain a row-context DAX expression
- **Calculation Items**: Should contain a DAX expression modifying the base measure

## How to Fix

### Manual Fix

1. In **TOM Explorer**, locate the measure, calculated column, or calculation item
2. Double-click to open the **DAX Editor**
3. Enter a valid DAX expression
4. Validate the syntax and save

## Common Causes

### Cause 1: Incomplete Creation

Object was created intending to define it later but was forgotten.

### Cause 2: Template-Based Creation

Scripts or templates created objects without expressions.

### Cause 3: Failed Copy Operation

Copied an object but the expression didn't transfer.

## Example

### Before Fix

```
Measure: [Total Revenue]
  Expression: [empty]
  FormatString: $#,0.00
```

**Error when queried**: "The expression for measure '[Total Revenue]' is not valid."

### After Fix

```
Measure: [Total Revenue]
  Expression: SUM('Sales'[Revenue])
  FormatString: $#,0.00
```

**Result**: Measure functions correctly and returns aggregated revenue.

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

