---
uid: calendar-blank-value
title: Calendar function blank date error
author: Morten Lønskov
updated: 2025-10-20
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---

# Calendar function blank date error


## Overview
This error may occur when refreshing a model in **Tabular Editor 3 (TE3)**, even if the affected table does not directly reference a `CALENDAR()` function. It typically indicates that a dependent Date or Calendar table relies on values from other tables that are temporarily empty, resulting in blank start or end date values.

## Symptoms

- Model refresh in Tabular Editor 3 fails with:

  ```
  The start date or end date in Calendar function cannot be Blank value.
  ```

- The same model or table refreshes successfully in Power BI Desktop or Power BI Service.
- Reimporting the table under a new name (for example, *TableName 1*) succeeds temporarily.
- The M expression for the affected table appears simple and valid:

  ```m
  let
    Source = <DataSource>,
    Data = Source{[Schema=SchemaVar,Item="TableX"]}[Data]
  in
    Data
  ```

## Cause
Although the error may appear unrelated to the table being refreshed, it usually originates from a downstream dependency in the model.

For example, a Date or Calendar table may define its range dynamically based on the minimum and maximum dates across multiple transactional tables:

```dax
CALENDAR(
  MINX(UNION(TableA, TableB, TableC), [Date]),
  MAXX(UNION(TableA, TableB, TableC), [Date])
)
```

If one or more of those source tables is empty, the `MINX` or `MAXX` expressions return blank, which causes the `CALENDAR()` function to fail.

## Steps to resolve
1. **Identify dependent tables**
   - Use the **Dependencies** view in Tabular Editor 3 to locate Date or Calendar tables that reference other tables’ date fields.
2. **Check for empty tables**
   - Verify that all referenced tables contain data. If a source table is empty, refresh the data source or adjust your schema variable configuration.
3. **Add default fallback values**
   - To prevent blank boundaries, wrap expressions with `COALESCE()` or specify default date values:

     ```dax
     CALENDAR(
       COALESCE(MINX(...), DATE(2000,1,1)),
       COALESCE(MAXX(...), TODAY())
     )
     ```
4. **Reprocess the model**
   - After applying fixes or data updates, reprocess the affected tables in Tabular Editor 3.

## Additional notes
> [!NOTE]
> This issue can occur when introducing schema variables in M scripts, such as using a variable to define the schema name (for example, `SchemaVar`).