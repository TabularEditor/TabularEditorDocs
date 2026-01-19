---
uid: kb.bpa-remove-auto-date-table
title: Remove Auto Date Tables
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule to identify and remove automatically generated date tables that increase model size and reduce performance.
---

# Remove Auto Date Tables

## Overview

This best practice rule identifies automatically generated date tables created by Power BI Desktop. These auto-generated tables (`DateTableTemplate_` and `LocalDateTable_`) should be removed in favor of a single, explicit date table to optimize model size and performance.

- Category: Performance

- Severity: Medium (2)

## Applies To

- Tables
- Calculated Tables

## Why This Matters

Power BI automatically creates hidden date tables for every date/datetime column when "Auto Date/Time" is enabled. This causes issues:

- **Increased model size**: Each auto-generated table adds unnecessary data
- **Memory overhead**: Multiple date tables consume more memory than one shared table
- **Slower refresh**: Additional tables increase refresh duration

A single, well-designed date table is far more efficient and maintainable.

## When This Rule Triggers

The rule triggers when it finds calculated tables with names that:

- Start with `"DateTableTemplate_"`, or
- Start with `"LocalDateTable_"`

These prefixes indicate Power BI's automatically generated date tables.

## How to Fix

### Manual Fix

1. Disable **Auto Date/Time** in Power BI Desktop (**File** > **Options** > **Data Load**)
2. Create a dedicated date table.
3. Mark it as a date table and create relationships to fact tables
4. In **TOM Explorer**, delete tables starting with `DateTableTemplate_` or `LocalDateTable_`
5. Verify custom date table relationships work correctly

## Common Causes

### Cause 1: Auto Date/Time Feature Enabled

Power BI Desktop's "Auto Date/Time" feature automatically creates these tables.

### Cause 2: Migrated Models

Models created with auto tables enabled and never cleaned up.

### Cause 3: Default Settings

New models use default settings which enable auto date tables.

## Example

### Before Fix

```
Tables:
  - Sales
  - LocalDateTable_OrderDate (hidden, auto-generated)
  - LocalDateTable_ShipDate (hidden, auto-generated)
  - Products
  - LocalDateTable_ReleaseDate (hidden, auto-generated)
```

**Result**: Multiple hidden tables inflate model size

### After Fix

```
Tables:
  - Sales
  - Products
  - DateTable (explicit, marked as date table)
    -> Relationships to Sales[OrderDate], Sales[ShipDate], Products[ReleaseDate]
```

**Result**: Single efficient date table serves all date relationships

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Date Table Should Exist](xref:kb.bpa-date-table-exists) - Ensuring a proper date table is present

## Learn More

- [Disable Auto Date/Time in Power BI](https://learn.microsoft.com/power-bi/guidance/auto-date-time)
- [Create Date Tables](https://learn.microsoft.com/power-bi/guidance/model-date-tables)
- [Date Table Best Practices](https://www.sqlbi.com/articles/creating-a-simple-date-table-in-dax/)
