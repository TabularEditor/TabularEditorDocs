---
uid: calendars
title: Calendars (Enhanced Time Intelligence)
author: Daniel Otykier
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

The calendars grid displays all available time unit categories. To configure your calendar, select a column from the dropdown for each time unit that applies to your calendar structure.

Time units are divided into **complete** categories (which uniquely identify a period on their own) and **partial** categories (which require a parent time unit to be mapped first). Hover over any time unit row to see a tooltip describing the expected data format.

**Complete Time Units:**

| Time Unit | Description | Examples |
|-----------|-------------|----------|
| Year | The year | 2024, 2025 |
| Quarter | The quarter including the year | Q1 2024, Q2 2025 |
| Month | The month including the year | January 2023, 2024 Feb |
| Week | The week including the year | Week 50 2023, W50-2023 |
| Date | The date | 12/31/2025, 4/3/2023 |

**Partial Time Units** (require a parent time unit to be mapped):

| Time Unit | Description | Examples | Requires | Alternatives |
|-----------|-------------|----------|----------|--------------|
| Quarter of Year | The quarter of the year | Q1, Quarter 2, YQ1 | Year | |
| Month of Year | The month of the year | January, M11, 11 | Year | |
| Month of Quarter | The month within a quarter | 1, QM2 | Quarter | Quarter of Year + Year |
| Week of Year | The week of the year | Week 50, W50, 50 | Year | |
| Week of Quarter | The week within a quarter | QW10, 10 | Quarter | Quarter of Year + Year |
| Week of Month | The week within a month | MW2, 2 | Month | Month of Year + Year<br>Month of Quarter + Quarter<br>Month of Quarter + Quarter of Year + Year |
| Day of Year | The day of the year | 365, D1 | Year | |
| Day of Quarter | The day within a quarter | QD2, 50 | Quarter | Quarter of Year + Year |
| Day of Month | The day of the month | MD10, 30 | Month | Month of Year + Year<br>Month of Quarter + Quarter<br>Month of Quarter + Quarter of Year + Year |
| Day of Week | The day of the week | WD5, 5 | Week | Week of Year + Year<br>Week of Quarter + Quarter<br>Week of Quarter + Quarter of Year + Year<br>Week of Month + Month<br>Week of Month + Month of Year + Year<br>Week of Month + Month of Quarter + Quarter<br>Week of Month + Month of Quarter + Quarter of Year + Year |

### Associated Columns

When you map a column to a time unit, that column becomes the **primary column** for that time unit. You can optionally add **associated columns** that represent the same time unit in a different format.

For example, if you map a numeric `MonthNumber` column (containing values 1-12) to "Month of Year", you might also want to associate a `MonthName` column (containing "January", "February", etc.) with the same time unit. Both columns represent the same concept, but in different formats.

To add associated columns:

1. Select a time unit row in the grid that has a column mapped.
2. In the **Associated Columns** panel on the right, check the columns you want to associate with that time unit.

Associated columns receive the same filter behavior as the primary column during time intelligence calculations.

![Associated Columns panel in the Calendar Editor](~/content/assets/images/tutorials/calendar-associated-columns.png)

### Time-Related Columns

In addition to mapping columns to specific time unit categories, you can mark columns as **time-related**. Time-related columns are columns in your Date table that don't fit into a specific time unit category but should still receive special treatment during time intelligence calculations.

Examples of time-related columns include:
- `IsHoliday` - A flag indicating whether the date is a holiday
- `IsWeekday` - A flag indicating whether the date is a weekday
- `FiscalPeriodName` - A descriptive label for the fiscal period

**How time-related columns behave:**

- During **lateral shifts** (such as `DATEADD` or `SAMEPERIODLASTYEAR`), filters on time-related columns are preserved, maintaining the same granularity.
- During **hierarchical shifts** (such as `DATESYTD` or `NEXTMONTH`), filters on time-related columns are cleared.

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
   Each calendar must have a unique name in the semantic model. The editor highlights duplicate names and prevents saving invalid configurations.

2. **Time unit dependency validation**
   Partial time units require their parent time units to be mapped. For example, if you map a column to "Day of Month", you must also map a column to "Month" (or to "Month of Year" + "Year", etc.). The editor shows which parent time units are required and prevents saving until the dependency is satisfied.

3. **Cross-calendar category consistency**
   If your model contains multiple calendars, a column must be associated with the same time unit category across all calendars. For example, if you map a `FiscalYear` column as "Year" in one calendar, you cannot map the same column as "Week of Year" in another calendar.

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
