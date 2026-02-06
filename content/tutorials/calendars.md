---
uid: calendars
title: Calendars (Enhanced Time Intelligence)
author: Daniel Otykier and Maria José Ferreira
updated: 2026-01-22
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

# Calendars (Enhanced Time Intelligence)

The September 2025 release of Power BI Desktop introduced a new Public Preview feature called **Enhanced Time Intelligence** (also known as **Calendar-based Time Intelligence**). This feature lets you define custom calendars in your semantic model, enabling time intelligence calculations across diverse calendar systems such as fiscal, retail (4-4-5, 4-5-4, 5-4-4), ISO, and other non-Gregorian calendars.

Unlike classic time intelligence functions that assume a standard Gregorian calendar, the new calendar-based functions derive their behavior from explicit column mappings you define in your Date table. This approach also introduces week-level time intelligence calculations that were difficult to perform previously.

For more information about how calendar-based time intelligence works, see:
- [Introducing Calendar-based Time Intelligence in DAX](https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/) (SQLBI)
- [Calendar-based Time Intelligence Preview](https://powerbi.microsoft.com/en-us/blog/calendar-based-time-intelligence-time-intelligence-tailored-preview/) (Microsoft)

## Defining a Calendar

![Creating a calendar](~/content/assets/images/tutorials/calendar-create.png)

1. Right-click on a table in your model (typically a Date table) and select **Create > Calendar...**.
2. Give your calendar a name, e.g. `Fiscal`.

Once calendars are added to a table, they will be shown in the TOM Explorer under the **Calendars** node:

![Calendar in TOM Explorer](~/content/assets/images/tutorials/calendar-tom-explorer.png)

Before you can use a calendar in your DAX calculations, you need to configure it by mapping columns in the table to the appropriate time unit categories.

## The Calendar Editor

The January 2026 release of Tabular Editor 3 introduced a dedicated **Calendar Editor** that provides a comprehensive interface for configuring calendars. The editor displays all time unit categories in a structured grid with helpful tooltips, and performs real-time validation to help you avoid configuration errors.

### Opening the Calendar Editor

You can open the Calendar Editor in any of the following ways:

- Double-click an existing calendar under a table in the TOM Explorer.
- Right-click an existing calendar under a table in the TOM Explorer and choose **Edit Calendar...**.
- Select a calendar in the TOM Explorer, then open the **Calendar** menu and choose **Edit Calendar...**.
- Open the **View** menu and choose **Calendar Editor**.

![Calendar Editor](~/content/assets/images/tutorials/calendar-editor.png)

### Layout of the Calendar Editor

The Calendar Editor is split into two main areas:

1. **Calendars grid (left panel)**
   A vertical grid where each calendar is displayed as a column and time unit categories are displayed as rows. The rows are organized hierarchically by Year, Quarter, Month, Week, and Day. In this grid you can:

   - Select the table that the calendar should get its columns from (typically a Date table) in the **Table** row.
   - Map columns to time unit categories by selecting from the dropdown in each cell.
   - See real-time validation feedback via icons and tooltips.
   - Create additional calendars using the **+ Add Calendar** column (if your model requires multiple calendar definitions).
   - Rename calendars by editing the name directly in the grid.
   - Delete calendars by right-clicking on a calendar column.

2. **Context panel (right panel)**
   A detail panel that changes based on your selection in the calendars grid:

   - **Associated Columns**: When you select a time unit row that has a column mapped, this panel lets you select additional associated columns.
   - **Time-Related Columns**: When you select the "Time-related columns" row at the bottom of the grid, this panel lets you mark columns as time-related.

![Calendar Editor layout showing the calendars grid and context panel](~/content/assets/images/tutorials/calendar-editor-parts.png)

### Mapping Columns to Time Units

The calendars grid displays all available time unit categories. To map a column to a time unit, click on a time-unit cell under a calendar column in the grid. This opens a dropdown where you can select the **primary column** for that time unit.

![Selecting a column from the dropdown](~/content/assets/images/tutorials/calendar-dropdown-column-selection.png)

You don't need to map every time unit—only the ones that apply to your calendar structure and for which your table has appropriate columns.

Time units are divided into **complete** categories (which uniquely identify a period on their own) and **partial** categories (which require a parent time unit to be mapped first). Hover over any time unit row to see a tooltip describing the expected data format and examples.

![Tooltip for a complete time unit showing description and examples](~/content/assets/images/tutorials/calendar-complete-time-unit-tooltip.png)

For partial time units, the tooltip also shows which parent time units must be mapped:

![Tooltip for a partial time unit showing dependencies](~/content/assets/images/tutorials/calendar-partial-time-unit-tooltip.png)

#### Example: Using Partial Time Units

In some cases, your Date table may not have columns that uniquely identify complete time units like Quarter or Month (e.g., "Q1 2024" or "January 2024"). Instead, you might have columns like `QuarterOfYear` (1-4) and `MonthOfYear` (1-12) that only make sense when combined with a Year column.

In this scenario, you can map the partial time units (`Quarter of Year`, `Month of Year`) along with the `Year` complete time unit. This is a valid configuration because the partial time units can derive their full context from the Year mapping.

![A calendar configuration using partial time units](~/content/assets/images/tutorials/calendar-simple-example.png)

> [!TIP]
> To see the available columns and their values while configuring your calendar, right-click on your Date table in the TOM Explorer and choose **Preview Data**.
>
> ![Preview Data option in context menu](~/content/assets/images/tutorials/calendar-preview-data-button.png)
>
> You can then dock the Data Preview window next to the Calendar Editor for easy reference.
>
> ![Docking the Data Preview window](~/content/assets/images/tutorials/calendar-dock-example.png)
>
> Alternatively, you can use the **DAX Query** window to query your Date table and keep it visible alongside the Calendar Editor.

With the Date table preview docked, you can see the column values as you configure your calendar:

![Calendar Editor with Date table preview](~/content/assets/images/tutorials/calendar-configured-example.png)

**Complete Time Units:**

| Time Unit | Description | Examples |
|-----------|-------------|----------|
| Year | The year | 2024, 2025 |
| Quarter | The quarter including the year | Q1 2024, Q2 2025 |
| Month | The month including the year | January 2023, 2024 Feb |
| Week | The week including the year | Week 50 2023, W50-2023 |
| Date | The date | 12/31/2025, 4/3/2023 |

**Partial Time Units** (require a parent time unit to be mapped):

| Time Unit | Description | Examples | Requires | Or requires one of |
|-----------|-------------|----------|----------|-------------------|
| Quarter of Year | The quarter of the year | Q1, Quarter 2, YQ1 | Year | |
| Month of Year | The month of the year | January, M11, 11 | Year | |
| Month of Quarter | The month within a quarter | 1, QM2 | Quarter | <ul><li>Quarter of Year + Year</li></ul> |
| Week of Year | The week of the year | Week 50, W50, 50 | Year | |
| Week of Quarter | The week within a quarter | QW10, 10 | Quarter | <ul><li>Quarter of Year + Year</li></ul> |
| Week of Month | The week within a month | MW2, 2 | Month | <ul><li>Month of Year + Year</li><li>Month of Quarter + Quarter</li><li>Month of Quarter + Quarter of Year + Year</li></ul> |
| Day of Year | The day of the year | 365, D1 | Year | |
| Day of Quarter | The day within a quarter | QD2, 50 | Quarter | <ul><li>Quarter of Year + Year</li></ul> |
| Day of Month | The day of the month | MD10, 30 | Month | <ul><li>Month of Year + Year</li><li>Month of Quarter + Quarter</li><li>Month of Quarter + Quarter of Year + Year</li></ul> |
| Day of Week | The day of the week | WD5, 5 | Week | <ul><li>Week of Year + Year</li><li>Week of Quarter + Quarter</li><li>Week of Quarter + Quarter of Year + Year</li><li>Week of Month + Month</li><li>Week of Month + Month of Year + Year</li><li>Week of Month + Month of Quarter + Quarter</li><li>Week of Month + Month of Quarter + Quarter of Year + Year</li></ul> |

### Associated Columns

When you map a column to a time unit, that column becomes the **primary column** for that time unit. You can optionally add **associated columns** that represent the same time unit in a different format.

For example, if you map a numeric `MonthNumber` column (containing values 1-12) to "Month of Year", you might also want to associate a `MonthName` column (containing "January", "February", etc.) with the same time unit. Both columns represent the same concept, but in different formats.

To add associated columns:

1. Select a time unit row in the grid that has a column mapped.
2. In the **Associated Columns** panel on the right, check the columns you want to associate with that time unit.

Associated columns receive the same filter behavior as the primary column during time intelligence calculations.

![Associated Columns panel in the Calendar Editor](~/content/assets/images/tutorials/calendar-associated-columns.png)

## Known limitations of the Calendar Editor
- **Sort By columns and Associated columns**

When a column is used as a **Sort By** column for a Primary time unit column, Analysis Services implicitly treats it as an Associated column. You should **not** explicitly add that Sort By column as an Associated column in the Calendar Editor, as this will cause an error from Analysis Services (duplicate mapping).

For example, if you set `MonthName` as the Primary column for "Month of Year" and `MonthName` has `MonthNumber` configured as its Sort By column, then `MonthNumber` is implicitly associated. In this case, you do not need to (and should not) add `MonthNumber` as an explicit Associated column. The Sort By column will still provide the expected enhanced calendar behavior (including proper `REMOVEFILTERS()` handling) since the association is inferred.
Note that this behavior is asymmetric: if you instead set the Sort By column (e.g., `MonthNumber`) as the Primary time unit column, then the display column (e.g., `MonthName`) is **not** automatically treated as Associated. In that scenario, you can explicitly add the display column as an Associated column if desired.

- **Hidden columns are not displayed**

Columns with their **Hidden** property set to `True` do not appear in the Calendar Editor's column dropdowns or in the Associated Columns and Time-Related Columns panels. This is unintended behavior, as hidden columns may still need to be used for calendar configuration (for example, numeric key columns used for sorting are often hidden from end users).

A future version of Tabular Editor will address these limitations.

### Time-Related Columns

In addition to mapping columns to specific time unit categories, you can mark columns as **time-related**. Time-related columns are columns in your Date table that don't fit into a specific time unit category but should still receive special treatment during time intelligence calculations.

Examples of time-related columns include:
- `IsHoliday` - A flag indicating whether the date is a holiday
- `IsWeekday` - A flag indicating whether the date is a weekday
- `FiscalPeriodName` - A descriptive label for the fiscal period

**How time-related columns behave:**

- During **lateral shifts** (such as `DATEADD` or `SAMEPERIODLASTYEAR`), filters on time-related columns are preserved, maintaining the same granularity.
- During **hierarchical shifts** (such as `DATESYTD` or `NEXTMONTH`), filters on time-related columns are cleared.

For more details on lateral and hierarchical shifts, see [Understanding lateral shift and hierarchical shift](https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/#:~:text=Understanding%20lateral%20shift%20and%20hierarchical%20shift) (SQLBI).

To configure time-related columns:

1. Select the **Time-related columns** row at the bottom of the calendars grid.
2. In the **Time-Related Columns** panel on the right, check the columns you want to mark as time-related.

![Time-Related Columns panel](~/content/assets/images/tutorials/calendar-time-related-columns.png)

### Applying Changes

Changes made in the Calendar Editor are applied to the local model (but not saved to disk) in two ways:

- Click the **Accept** button in the toolbar to apply changes to the local model.
- Changes are also automatically applied when you navigate away from the Calendar Editor (losing focus from the view).

You can discard pending changes by clicking the **Cancel** button before navigating away.

To persist the changes, save the model.

## Real-Time Validation

The Calendar Editor performs real-time validation as you configure your calendars. Validation feedback is displayed via icons and tooltips directly in the grid, helping you identify and resolve issues before saving.

The following rules are enforced:

1. **Unique calendar name**
   Each calendar must have a unique name in the semantic model. If you create a calendar with a duplicate name, the editor automatically appends a suffix (e.g., "(1)") to ensure uniqueness.

2. **Time unit dependency validation**
   Partial time units require their parent time units to be mapped. For example, if you map a column to "Day of Month", you must also map a column to "Month" (or to "Month of Year" + "Year", etc.). The editor highlights cells with missing dependencies and displays a tooltip explaining which parent time units are required.

   ![Dependency error showing missing parent time unit](~/content/assets/images/tutorials/calendar-dependency-error.png)

3. **Cross-calendar category consistency**
   If your model contains multiple calendars, a column must be associated with the same time unit category across all calendars. For example, if you map a `FiscalYear` column as "Year" in one calendar, you cannot map the same column as "Week of Year" in another calendar.

   ![Cross-calendar category conflict showing Time Unit Conflict error](~/content/assets/images/tutorials/calendar-cross-category-validation.png)

## Configuring Calendars with the Column Mappings Dialog

As an alternative to the Calendar Editor, you can configure a calendar by right-clicking on it in the TOM Explorer and choosing the **Edit Column Mappings...** option:

![Editing calendar column mappings](~/content/assets/images/edit-calendar-mappings.png)

This dialog allows you to add column associations one at a time. Click **Add Column Association** and choose **Column Association** to add a new mapping. For each association, you select a column and assign it to a time unit category. You can also add additional associated columns for each mapping by expanding the **Columns** property.

![Column associations in the Collection Editor](~/content/assets/images/tutorials/calendar-example.png)

#### Adding Time-Related Columns in the Column Mappings Dialog

To add time-related columns through this dialog, click **Add Column Association** and choose **Column Group**. This creates a Time Related Column Group where you can add columns that should be treated as time-related (see [Time-Related Columns](#time-related-columns) for more information about how these columns behave).

![Adding a Column Group for time-related columns](~/content/assets/images/tutorials/calendar-collection-editor-column-group.png)

The Calendar Editor is recommended for most scenarios as it provides a more comprehensive view of all time units, helpful tooltips, and real-time validation feedback.

## Using Calendars in DAX

Once you've defined a calendar and mapped its columns, you can use it in your DAX calculations. Calendars work with existing DAX time intelligence functions that accept a date column as input (such as [`TOTALYTD`](https://dax.guide/totalytd), [`CLOSINGBALANCEMONTH`](https://dax.guide/closingbalancemonth) and [`DATEADD`](https://dax.guide/dateadd)).

Additionally, 8 new DAX functions for week-based time intelligence have been introduced. These functions exclusively work with calendars:

- [`CLOSINGBALANCEWEEK`](https://dax.guide/closingbalanceweek)
- [`OPENINGBALANCEWEEK`](https://dax.guide/openingbalanceweek)
- [`STARTOFWEEK`](https://dax.guide/startofweek)
- [`ENDOFWEEK`](https://dax.guide/endofweek)
- [`NEXTWEEK`](https://dax.guide/nextweek)
- [`PREVIOUSWEEK`](https://dax.guide/previousweek)
- [`DATESWTD`](https://dax.guide/dateswtd)
- [`TOTALWTD`](https://dax.guide/totalwtd)

Click the links above to learn more about each function.
