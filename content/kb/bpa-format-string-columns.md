---
uid: kb.bpa-format-string-columns
title: Provide Format String for Numeric and Date Columns
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring visible numeric and date columns have appropriate format strings for consistent display.
---

# Provide Format String for Numeric and Date Columns

## Overview

This best practice rule identifies visible columns with numeric or date data types that lack format strings. Format strings ensure consistent, professional data display across all client tools.

- Category: **Formatting**

- Severity: Medium (2)

## Applies To

- Data Columns
- Calculated Columns
- Calculated Table Columns

## Why This Matters

Columns without format strings display inconsistently:

- **Unprofessional appearance**: Raw numbers like 1234567.89 instead of $1,234,567.89
- **User confusion**: Users can't tell if values are currency, percentages, or plain numbers
- **Inconsistent formatting**: Different visuals may show different formats
- **Manual formatting burden**: Users must format every visual individually
- **Date ambiguity**: Dates show timestamps when only dates are needed

## When This Rule Triggers

```csharp
IsVisible
and string.IsNullOrWhitespace(FormatString)
and (DataType = "Int64" or DataType = "DateTime" or DataType = "Double" or DataType = "Decimal")
```

## How to Fix

### Manual Fix

1. In **TOM Explorer**, select the column
2. In **Properties** pane, locate the **Format String** field
3. Choose from standard formats or enter custom format
4. Save changes

## Common Causes

### Cause 1: Missing Format Definition

Columns do not have a format string when imported. 

## Example

### Before Fix

```
Column: SalesAmount
Format String: (empty)
```

**Display**: 1234567.89 (hard to read, no currency symbol)

### After Fix

```
Column: SalesAmount
Format String: "$#,0.00"
```

**Display**: $1,234,567.89 (clear, professional formatting)

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Provide Format String for Measures](xref:kb.bpa-format-string-measures) - Similar validation for measures
