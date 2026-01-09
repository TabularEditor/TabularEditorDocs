---
uid: kb.bpa-format-string-measures
title: Provide Format String for Measures
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring visible measures have appropriate format strings for consistent display.
---

# Provide Format String for Measures

## Overview

This best practice rule identifies visible measures with numeric or date data types that lack format strings. All measures should have explicit format strings for professional, consistent display.

- Category: Formatting

- Severity: Medium (2)

## Applies To

- Measures

## Why This Matters

Measures without format strings display raw values, causing user confusion and inconsistent reporting. Format strings ensure:

- **Professional appearance**: Values display with appropriate currency, percentage, or number formatting
- **Consistency**: All reports show values in the same format
- **User confidence**: Properly formatted numbers are easier to read and interpret
- **Business alignment**: Formatting matches corporate standards

## When This Rule Triggers

```csharp
IsVisible
and string.IsNullOrWhitespace(FormatString)
and (DataType = "Int64" or DataType = "DateTime" or DataType = "Double" or DataType = "Decimal")
```

## How to Fix

### Manual Fix

1. In **TOM Explorer**, select the measure
2. In **Properties** pane, locate the **Format String** field
3. Enter an appropriate format string based on what the measure calculates
4. Save changes

### Common Format Patterns

```dax
Total Revenue = 
SUM('Sales'[Amount])
// Format String: "$#,0"

Average Price = 
AVERAGE('Sales'[UnitPrice])
// Format String: "$#,0.00"

YoY Growth = 
DIVIDE([This Year] - [Last Year], [Last Year], 0)
// Format String: "0.0%"

Order Count = 
COUNTROWS('Orders')
// Format String: "#,0"
```

## Common Causes

### Cause 1: Missing Format Definition

When creating a new measure the defualt state is to not have any format string set.

### Cause 2: Copy/Paste from Calculated Columns

Copying measures from columns that don't require format strings.

## Example

### Before Fix

```dax
Total Revenue = SUM('Sales'[Amount])
// No Format String
```

**Display**: 1234567.89 (hard to read, no currency symbol)

### After Fix

```dax
Total Revenue = SUM('Sales'[Amount])
// Format String: "$#,0"
```

**Display**: $1,234,568 (clear, professional formatting)

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Format String for Columns](xref:kb.bpa-format-string-columns) - Similar validation for columns
