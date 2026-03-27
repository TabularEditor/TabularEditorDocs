---
uid: kb.bpa-udf-use-compound-names
title: Use Compound Names for User-Defined Functions
author: Morten Lønskov
updated: 2026-03-19
description: Best practice rule ensuring User-Defined Functions use separator characters to prevent naming conflicts with future built-in DAX functions.
---

# Use Compound Names for User-Defined Functions

## Overview

This best practice rule identifies User-Defined Functions (UDFs) whose names do not contain a separator character (`.` or `_`). Compound names prevent naming conflicts if Microsoft introduces a built-in DAX function with the same name.

- Category: Error Prevention

- Severity: Low (1)

## Applies To

- User-Defined Functions

## Why This Matters

UDFs without separator characters in their names risk breaking in the future:

- **Naming conflicts**: If Microsoft adds a new built-in DAX function with the same name as your UDF, the built-in function takes precedence and your UDF will stop working
- **Ambiguity**: Without a namespace or prefix, it is unclear whether a function call refers to a built-in DAX function or a custom UDF
- **Maintenance burden**: Renaming UDFs after a conflict occurs requires updating all references throughout the model

Using compound names (e.g., `Finance.CalcProfit` or `My_CalcProfit`) makes your UDFs distinguishable from built-in DAX functions.

## When This Rule Triggers

The rule triggers when a UDF name contains neither a period nor an underscore:

```csharp
not Name.Contains(".") and not Name.Contains("_")
```

## How to Fix

### Manual Fix

1. In the **TOM Explorer**, locate the User-Defined Function
2. Rename it to include a namespace separator (`.`) or underscore (`_`)
3. Tabular Editor automatically updates all references throughout the model

## Common Causes

### Cause 1: Simple Naming

The function was given a plain name without considering future conflicts.

### Cause 2: Imported from Query

A UDF was applied from a DAX query DEFINE section where namespace conventions were not followed.

## Example

### Before Fix

```dax
// Function named without separator
FUNCTION CalcProfit =
    (
        revenue: DOUBLE,
        cost: DOUBLE
    )
    => revenue - cost
```

### After Fix

```dax
// Function named with namespace separator
FUNCTION Finance.CalcProfit =
    (
        revenue: DOUBLE,
        cost: DOUBLE
    )
    => revenue - cost
```

## Compatibility Level

This rule applies to models with compatibility level **1702** and higher.

## Related Rules

- [DAX User-Defined Functions](xref:udfs)
- [Built-in BPA Rules](xref:built-in-bpa-rules)
