---
uid: calendars
title: Calendars (Enhanced Time Intelligence)
author: Daniel Otykier
updated: 2026-01-20
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

The September 2025 release of Power BI Desktop introduced a new Public Preview feature called **Enhanced Time Intelligence**. This feature lets you define custom calendars in your semantic model, and it also introduces 8 new DAX functions that work with these calendars, enabling week-based time intelligence calculations that were difficult to perform previously.

## Defining a Calendar

![Creating a calendar](~/content/assets/images/tutorials/calendar-create.png)

1. Right-click on a table in your model (typically a Date table) and select **Create > Calendar...**.
2. Give your calendar a name, e.g. `Fiscal`.

Once calendars are added to a table, they will be shown in the TOM Explorer under the **Calendars** node:

![Calendar in TOM Explorer](~/content/assets/images/tutorials/calendar-tom-explorer.png)

Before you can use a calendar in your DAX calculations, you need to configure it by specifying which columns in the table represent the different calendar attributes. You can do this using the **Calendar Editor** (recommended) or the **Edit Column Mappings...** dialog.

## Configuring Calendars with the Column Mappings Dialog

You can configure a calendar by right-clicking on it in the TOM Explorer and choosing the **Edit Column Mappings...** option:

![Editing calendar column mappings](~/content/assets/images/edit-calendar-mappings.png)

For each calendar, you can add one or more **Column Associations**. Each association maps a column from the table to a specific **Time Unit** (e.g. Year, Month, Week, etc.). You can also add additional associated columns for each mapping, which are typically used for columns that represent the same time unit but in a different format. For example, you might have a "Month" column that contains the month number (1-12), and a "Month Name" column that contains the month name ("January", "February", etc.). Both of these columns can be associated with the "MonthOfYear" time unit.

## The Calendar Editor (Multi-Calendar Manager)

The January 2026 release of Tabular Editor 3 introduced a dedicated **Calendar Editor** — a multi-calendar manager view that lets you create and maintain all calendars in one place.

### Opening the Calendar Editor

You can open the Calendar Editor in any of the following ways:

- Double-click an existing calendar under a table in the TOM Explorer.
- Right-click an existing calendar under a table in the TOM Explorer and choose **Edit Calendar...**.
- Select a calendar in the TOM Explorer, then open the **Calendar** menu and choose **Edit Calendar...**.
- Open the **View** menu and choose **Calendar Editor**.

The Calendar Editor opens as a new window displaying all calendars in the model. The first calendar in the list is selected by default.

![Calendar Editor](~/content/assets/images/tutorials/calendar-editor.png)

### Layout of the Calendar Editor

The Calendar Editor is split into two main areas:

1. **Calendars grid (left panel)**
   A vertical grid where each calendar is displayed as a column and time units are displayed as rows. In this grid you can:

   - Create new calendars using the **+ Add Calendar** column.
   - Rename existing calendars by editing the calendar name directly.
   - Delete calendars by right-clicking on a calendar column.
   - Map columns to time units by selecting from the dropdown in each cell.
   - See real-time validation feedback via icons and tooltips.

2. **Context panel (right panel)**
   A detail panel that changes based on your selection in the calendars grid:

   - **Associated Columns**: When you select a time unit row, this panel shows the primary column for that time unit and lets you select additional associated columns (columns that represent the same time unit in a different format).
   - **Time-related Columns**: When you select the "Time-related columns" row at the bottom of the grid, this panel lets you mark columns as time-related to the calendar without assigning them to a specific time unit.

![Calendar Editor layout showing the calendars grid and Associated Columns panel](~/content/assets/images/tutorials/calendar-editor-parts.png)

### Managing Calendars

In the **Calendars** grid you can:

- **Add a calendar**  
  Use the *Add Calendar* action in the grid to create a new calendar. You will be prompted for a name, which must be unique within the semantic model (see validations below).

- **Rename a calendar**  
  Edit the name directly in the grid.

- **Delete a calendar**  
  Right-click on a calendar in the grid to delete it from the model. This also removes all its column associations.

The changes done in the Calendar Editor are only applied to the semantic model when you click the **Accept** button in the toolbar. The changes can also be canceled by clicking on the **Cancel** button, similarly to the expression editor.

All operations in this grid operate against the semantic model, so external tools (such as Power BI Desktop or SSMS) will see the updated set of calendars after a save.

### Configuring Associated Columns

The **Associated Columns** panel lets you define how table columns map to calendar time units for the currently selected calendar. For more background on how associated columns work in Enhanced Time Intelligence, see the [SQLBI article on Enhanced Time Intelligence](https://www.sqlbi.com/articles/enhanced-time-intelligence-in-power-bi/).

The calendars grid displays rows for each time unit category, organized hierarchically. Time units are divided into **complete** units (which uniquely identify a period on their own) and **partial** units (which require a parent time unit).

**Complete Time Units:**

| Time Unit | Description | Examples |
|-----------|-------------|----------|
| Year | The year | 2024, 2025 |
| Quarter | The quarter including the year | Q1 2024, Q2 2025 |
| Month | The month including the year | January 2023, 2024 Feb |
| Week | The week including the year | Week 50 2023, W50-2023 |
| Date | The date | 12/31/2025, 4/3/2023 |

**Partial Time Units** (require a parent time unit to be mapped):

| Time Unit | Description | Examples | Requires |
|-----------|-------------|----------|----------|
| Quarter of Year | The quarter of the year | Q1, Quarter 2, YQ1 | Year |
| Month of Year | The month of the year | January, M11, 11 | Year |
| Month of Quarter | The month within a quarter | 1, QM2 | Quarter |
| Week of Year | The week of the year | Week 50, W50, 50 | Year |
| Week of Quarter | The week within a quarter | QW10, 10 | Quarter |
| Week of Month | The week within a month | MW2, 2 | Month |
| Day of Year | The day of the year | 365, D1 | Year |
| Day of Quarter | The day within a quarter | QD2, 50 | Quarter |
| Day of Month | The day of the month | MD10, 30 | Month |
| Day of Week | The day of the week | WD5, 5 | Week |

For each time unit you can:

- Select the **primary column** that represents that time unit (e.g. `Date`, `Year`, `Month`, `Week`, etc.).
- Optionally select **additional associated columns** that represent the same time unit in a different format (for example, numeric month vs. month name, or alternative labels).

Hover over each time unit row to see a tooltip with more details about the expected column format and usage.

The Calendar Editor provides a unified, multi-calendar experience compared to the *Edit Column Mappings...* dialog, which only allows editing one calendar at a time.

![Calendar column associations](~/content/assets/images/tutorials/calendar-example.png)

## Real-Time Validation in the Calendar Editor

The Calendar Editor performs real-time validation while you edit calendars and column associations. Validation feedback is surfaced directly in the view (for example, via icons, tooltips, or messages), so you can resolve issues before committing changes.

The following rules are enforced:

1. **Unique calendar name**
   Each calendar must have a unique name in the semantic model. The editor highlights duplicate names and prevents saving invalid configurations.

2. **Time unit dependency validation**
   Partial time units require their parent time units to be mapped. For example, if you map a column to "Day of Month", you must also map a column to "Month" (or to "Month of Year" + "Year", etc.). The editor shows which parent time units are required and prevents saving until the dependency is satisfied.

3. **Cross-calendar category consistency**
   A column must be associated with the same time unit category across all calendars. For example, if you map a `FiscalYear` column as "Year" in one calendar, you cannot map the same column as "Week of Year" in another calendar. When a column is categorized differently across calendars, the editor reports a consistency violation.

Validation is performed as you type or edit selections, and errors must be resolved before changes can be safely applied.

## Using Calendars in DAX

Once you've defined a calendar and mapped its columns, you can start using it in your DAX calculations. Calendars work with all DAX functions that accept a date column as input (such as [`TOTALYTD`](https://dax.guide/totalytd), [`CLOSINGBALANCEMONTH`](https://dax.guide/closingbalancemonth) and [`DATEADD`](https://dax.guide/dateadd)).

Moreover, 8 new DAX functions for week-based time intelligence have been introduced. These exclusively work with calendars:

- [`CLOSINGBALANCEWEEK`](https://dax.guide/closingbalanceweek)
- [`OPENINGBALANCEWEEK`](https://dax.guide/openingbalanceweek)
- [`STARTOFWEEK`](https://dax.guide/startofweek)
- [`ENDOFWEEK`](https://dax.guide/endofweek)
- [`NEXTWEEK`](https://dax.guide/nextweek)
- [`PREVIOUSWEEK`](https://dax.guide/previousweek)
- [`DATESWTD`](https://dax.guide/dateswtd)
- [`TOTALWTD`](https://dax.guide/totalwtd)

Click the links above to learn more about each function.