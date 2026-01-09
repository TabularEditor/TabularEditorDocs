---
uid: kb.bpa-date-table-exists
title: Date Table Should Exist
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring your model includes a dedicated date table for proper time intelligence functionality.
---

# Date Table Should Exist

## Overview

This best practice rule verifies that your tabular model contains at least one properly configured date table. Date tables are essential for time intelligence calculations and ensuring consistent date-based filtering across your model.

- Category: **Performance**

- Severity: Medium (2)

## Applies To

- Model

## Why This Matters

A dedicated date table is essential because it:

- **Enables time intelligence**: Functions like `DATESYTD`, `SAMEPERIODLASTYEAR`, and `TOTALYTD` require a date table
- **Ensures consistent filtering**: Provides single source of truth for date attributes
- **Improves performance**: Establishes proper calendar relationships
- **Supports custom calendars**: Enables fiscal year calculations and custom hierarchies

Without a properly marked date table, many DAX time intelligence functions will fail or produce incorrect results.

## When This Rule Triggers

The rule triggers when **all** tables in your model meet the following conditions:

1. No table has any calendars defined (`Calendars.Count = 0`)
2. No table contains a column marked as a key with `DataType = DateTime`
3. No table has `DataCategory = "Time"`

This indicates that the model lacks a proper date dimension.

## How to Fix

### Option 1: Create a Date Table Using DAX

Add a calculated table with a complete date range:

```dax
DateTable = 
ADDCOLUMNS (
    CALENDAR (DATE(2020, 1, 1), DATE(2030, 12, 31)),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "Month", FORMAT([Date], "MMMM"),
    "MonthNumber", MONTH([Date]),
    "Day", DAY([Date]),
    "WeekDay", FORMAT([Date], "dddd")
)
```

### Option 2: Import from Data Source

Create a date dimension table in your data warehouse or data source and import it into the model.

### Mark as Date Table

After creating the table:

1. Select the date table in the **TOM Explorer**
2. Right-click and choose **Mark as Date Table**
3. Select the date column as the key column
4. Create relationships between the date table and your fact tables

### Set Calendar Metadata

Alternatively, configure the calendar metadata:

1. Select the date table
2. In the **Properties** pane, expand **Calendars**
3. Add a new calendar and configure the date column reference

## Example

A typical date table structure:

| Date | Year | Quarter | Month | MonthNumber | Day |
|------|------|---------|-------|-------------|-----|
| 2025-01-01 | 2025 | Q1 | January | 1 | 1 |
| 2025-01-02 | 2025 | Q1 | January | 1 | 2 |
| ... | ... | ... | ... | ... | ... |

Once created, establish relationships:

```
'DateTable'[Date] (1) -> (*) 'Sales'[OrderDate]
'DateTable'[Date] (1) -> (*) 'Orders'[ShipDate]
```

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Remove Auto Date Table](xref:kb.bpa-remove-auto-date-table) - Removing automatic date tables that duplicate functionality

## Learn More

- [Create Date Tables in Power BI](https://learn.microsoft.com/power-bi/guidance/model-date-tables)
- [Time Intelligence Functions in DAX](https://learn.microsoft.com/dax/time-intelligence-functions-dax)
- [Mark as Date Table](https://learn.microsoft.com/power-bi/transform-model/desktop-date-tables)
