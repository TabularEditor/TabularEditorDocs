---
uid: object-properties-calendars
title: Calendar properties
author: Jeroen ter Heerdt
updated: 2026-10-05
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.23.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Calendar properties

<!--
SUMMARY: Reference for the properties of calendars, time unit column associations and time-related column groups, used by calendar-based time intelligence.
-->

This page lists the properties of calendars and of the two kinds of column groups that make up a calendar. For properties that most objects share, see @object-properties-common.

Calendars are the objects behind *calendar-based time intelligence*, also called *enhanced time intelligence*. A calendar tells DAX time intelligence functions which columns of a date table hold the year, the quarter, the month, the week and so on. With a calendar, functions such as `TOTALYTD` and `DATEADD` work with fiscal, retail (4-4-5) and other non-Gregorian calendars, and week-based functions such as `TOTALWTD` become available.

A calendar is made up of column groups:

- a **time unit column association** maps one column, and optionally some associated columns, to a time unit such as **Year** or **Month of Year**
- a **time-related column group** lists columns that relate to time without belonging to one time unit, such as an `IsHoliday` flag

All three objects need compatibility level 1701 or higher. In Tabular Editor 3, the **Calendar Editor** shows the whole calendar in one grid and shows errors in it while you work. See @calendars.

## Calendar

A calendar belongs to a table, usually the date table, and defines one way of dividing time, for example `Gregorian` or `Fiscal`. A table can have more than one calendar. In DAX, you refer to a calendar by name in place of a date column, for example:

```dax
TOTALYTD ( [Sales Amount], 'Fiscal' )
```

Calendar names must be unique in the whole model.

The Best Practice Analyzer (BPA) rule @kb.bpa-date-table-exists flags a model that has no calendar and no marked date table.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Object Type](xref:object-properties-common#object-type)
- [Lineage Tag](xref:object-properties-common#lineage-tag)
- [Source Lineage Tag](xref:object-properties-common#source-lineage-tag)

### Calendar Column Groups
`CalendarColumnGroups` · CalendarColumnGroupCollection · Basic · read-only

The column groups that make up the calendar, which are its time unit column associations and its time-related column groups. This is the Tabular Object Model (TOM) name of the collection. The **Properties view** shows the same collection as `ColumnMappings`. In a C# script, you can use either name.

### Column Mappings
`ColumnMappings` · CalendarColumnGroupCollection · Basic · read-only · *shortcut to* **Calendar Column Groups**

The same collection as `CalendarColumnGroups`, under the name that the **Properties view** shows. You can add, change and remove the groups in the collection. In Tabular Editor 3, double-click the calendar in the @tom-explorer-view to open the **Calendar Editor**. The **...** button of the property and **Edit Column Mappings...** on the right-click menu of the calendar in the **TOM Explorer** both open a collection editor.

## Time unit column association

A time unit column association maps a column of the table to a time unit of the calendar, for example the `Fiscal Year` column to **Year** or the `Month Name` column to **Month of Year**. The mapped column is the *primary column*. You can add *associated columns* that hold the same time unit in another format, such as a month number next to a month name.

Each time unit can be mapped once per calendar. The **Calendar Editor** has one row per time unit, and the `AddTimeUnit` method in C# scripts fails when the calendar already maps that time unit. A column can belong to only one time unit in a calendar, and it must map to the same time unit in every calendar of the model. The **Calendar Editor** in Tabular Editor 3 shows an error when a column maps to different time units in two calendars, or when the sort column of one primary column is the primary column of another time unit.

### Common properties

- [Object Type](xref:object-properties-common#object-type)

### Primary Column
`PrimaryColumn` · Column · Basic

The column that holds the values of this time unit. Its values must fit the time unit: a column mapped to **Month** identifies a month including its year, such as `January 2025`, and a column mapped to **Month of Year** only identifies the month, such as `January` or `1`.

If the primary column has a `SortByColumn`, the engine also treats the sort column as an associated column, and you don't need to add it.

To see the values of the columns while you map them, open a @table-preview of the date table and dock it next to the **Calendar Editor**.

### Time Unit
`TimeUnit` · TimeUnit · Basic

The time unit that the primary column represents. A *complete* time unit identifies a period on its own. A *partial* time unit only identifies a period together with a larger time unit, which the calendar must also map. For example, **Month of Year** needs **Year**.

| Value | Kind | Meaning | Example values |
|---|---|---|---|
| `Year` | Complete | The year. | `2024`, `FY2025` |
| `Semester` | Complete | The half-year including the year. | `H1 2024` |
| `SemesterOfYear` | Partial, needs `Year` | The half-year within the year. | `H1`, `1` |
| `Quarter` | Complete | The quarter including the year. | `Q1 2024` |
| `QuarterOfYear` | Partial, needs `Year` | The quarter within the year. | `Q1`, `1` |
| `QuarterOfSemester` | Partial, needs `Semester` | The quarter within the half-year. | `1`, `2` |
| `Month` | Complete | The month including the year. | `January 2024`, `2024-01` |
| `MonthOfYear` | Partial, needs `Year` | The month within the year. | `January`, `1` |
| `MonthOfSemester` | Partial, needs `Semester` | The month within the half-year. | `1` to `6` |
| `MonthOfQuarter` | Partial, needs `Quarter` | The month within the quarter. | `1` to `3` |
| `Week` | Complete | The week including the year. | `W50-2023` |
| `WeekOfYear` | Partial, needs `Year` | The week within the year. | `W50`, `50` |
| `WeekOfSemester` | Partial, needs `Semester` | The week within the half-year. | `1` to `27` |
| `WeekOfQuarter` | Partial, needs `Quarter` | The week within the quarter. | `1` to `14` |
| `WeekOfMonth` | Partial, needs `Month` | The week within the month. | `1` to `6` |
| `Date` | Complete | The date. | `2025-12-31` |
| `DayOfYear` | Partial, needs `Year` | The day within the year. | `1` to `366` |
| `DayOfSemester` | Partial, needs `Semester` | The day within the half-year. | `1` to `184` |
| `DayOfQuarter` | Partial, needs `Quarter` | The day within the quarter. | `1` to `92` |
| `DayOfMonth` | Partial, needs `Month` | The day within the month. | `1` to `31` |
| `DayOfWeek` | Partial, needs `Week` | The day within the week. | `1` to `7` |
| `Unknown` | | No time unit is set. Not a valid choice. | |

A partial time unit can also get its larger unit from a combination of other partial units. For example, **Month of Year** together with **Year** is enough for **Day of Month**. See the table of dependencies in @calendars.

TOM defines the semester time units (`Semester`, `SemesterOfYear`, `QuarterOfSemester`, `MonthOfSemester`, `WeekOfSemester` and `DayOfSemester`), and Power BI doesn't list them among its calendar categories. Tabular Editor 3 hides them from the **Time Unit** dropdown of the **Properties view** and from the **Calendar Editor**, and it also hides `Unknown` from the dropdown. You only see these values when a C# script or another tool has set them.

The engine supports the semester units. In Power BI Desktop, calendars built with semester time units, for example **Year**, **Semester**, **Semester of Year**, **Month** and **Date**, are accepted, and time intelligence functions such as `DATESYTD` and `SAMEPERIODLASTYEAR` work with them. The engine rejects a calendar that maps the same time unit twice, and a column that is mapped to different time units in two calendars of the same table.

The dependencies in the table apply to the semester units too. When you save, the engine accepts a calendar that doesn't meet them, for example a calendar with only **Semester of Year** and **Date**. The engine applies them when a query uses the calendar: a partial unit only counts when its larger unit is also mapped, so **Quarter of Semester** works as the calendar's quarter only together with **Semester**. A time intelligence function that needs a unit the calendar doesn't have fails with an error like "'DATESYTD' uses calendar 'Fiscal', which does not define all the categories that are required for this operation. At minimum, ensure the 'Year' category is tagged". Year-based functions such as `DATESYTD` and `SAMEPERIODLASTYEAR` always need a **Year** unit, and **Semester** doesn't count as one.

### Associated Columns
`AssociatedColumns` · AssociatedColumnCollection · Options · read-only

Other columns that hold the same time unit as the primary column, in a different format. For example, when `Month Number` is the primary column for **Month of Year**, you can add `Month Name` and `Month Short Name` as associated columns. Time intelligence functions treat a filter on any of these columns like a filter on the primary column.

You can add and remove columns in the collection, for example in the **Associated Columns** panel of the **Calendar Editor**.

## Time-related column group

A time-related column group lists columns that describe dates without mapping to one time unit, for example `IsHoliday`, `IsWorkingDay` or `Fiscal Period Name`. Time intelligence functions handle filters on these columns by the kind of shift they do:

- a *lateral shift*, which only `DATEADD` and `SAMEPERIODLASTYEAR` do, keeps filters on them, so the working days of this month move to the working days of the same month last year
- a *hierarchical shift*, which all other time intelligence functions do, for example `DATESYTD` or `NEXTMONTH`, removes filters on them

All time intelligence functions keep filters on columns of the table that the calendar doesn't mention at all, as a time unit or in a time-related group. Add a column to a time-related group only when you want hierarchical shifts to remove filters on it.

When a table has more than one calendar, the engine applies these rules for every calendar on the table, including the calendars that the function doesn't use.

### Common properties

- [Object Type](xref:object-properties-common#object-type)

### Columns
`Columns` · AssociatedColumnCollection · Options · read-only

The columns in the group. You can add and remove columns in the collection, for example in the **Time-Related Columns** panel of the **Calendar Editor**.
