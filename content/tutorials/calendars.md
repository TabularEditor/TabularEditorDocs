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

Before you can use a calendar in your DAX calculations, you need to configure it by specifying which columns in the table represent the different calendar attributes.

## The Calendar Editor (Multi-Calendar Manager)

The January 2026 release of Tabular Editor 3 introduced a dedicated **Calendar Editor** – a multi-calendar manager view that lets you create and maintain all calendars in one place.

### Opening the Calendar Editor

You can open the Calendar Editor in any of the following ways:

- Double click an existing calendar under a table in the TOM Explorer
- Right-click an existing calendar under a table in the TOM Explorer and choose **Edit Calendar...**.
- Open the **View** menu and choose **Calendar Editor**.

The Calendar Editor opens as a new window and focuses on the currently selected calendar.

### Layout of the Calendar Editor

The Calendar Editor is split into two main areas:

1. **Calendars grid (top section)**  
   A grid that lists all calendars defined in the model. In this grid it is possible to:

   - Create new calendars.
   - Rename existing calendars.
   - Delete calendars.
   - Edit the column mappings for the time units in the calendars.
   - See the real-time validations performed on the calendars.

2. **Time-Related columns section (right-side section)**  
   A detail panel that lets you configure which columns are associated with each time unit for the selected calendar.

3. **Time-Related columns section (right-side section)**  
   A detail panel that lets you configure which columns are time-related to the selected calendar.

### Managing Calendars

In the **Calendars** grid you can:

- **Add a calendar**  
  Use the *Add Calendar* action in the grid to create a new calendar. You will be prompted for a name, which must be unique within the semantic model (see validations below).

- **Rename a calendar**  
  Edit the name directly in the grid.

- **Delete a calendar**  
  Righ-click on a calendar calendar name in the grid to delete it from the model. This also removes all its column associations.

The changes done in the Calendar Editor are only applied to the semantic model when you click the **Accept** button in the toolbar. The changes can also be canceled by clicking on the **Cancel** button, similarly to the expression editor.

All operations in this grid operate against the semantic model, so external tools (such as Power BI Desktop or SSMS) will see the updated set of calendars after a save.

### Configuring Associated Columns

The **Associated Columns** section lets you define how table columns map to calendar time units for the currently selected calendar.

For each row (time unit/category) you can:

- Select the **primary column** that represents that time unit (e.g. `Date`, `Year`, `Month`, `Week`, etc.).
- Optionally select **additional associated columns** that represent the same time unit in a different format (for example, numeric month vs. month name, or alternative labels).

This replaces the older *Edit Column Mappings...* dialog and provides a unified, multi-calendar experience directly within the editor.

![Calendar column associations](~/content/assets/images/tutorials/calendar-example.png)

## Real-Time Validation in the Calendar Editor

The Calendar Editor performs real-time validation while you edit calendars and column associations. Validation feedback is surfaced directly in the view (for example, via icons, tooltips, or messages), so you can resolve issues before committing changes.

The following rules are enforced:

1. **Unique calendar name**  
   Each calendar must have a unique name in the semantic model. Duplicate names are not allowed across calendars on the same table or across the model (depending on your engine rules). The editor highlights any duplicate names and prevents saving invalid configurations.

2. **Single association per calendar**  
   A column cannot belong to more than one **category** (time unit) in the same calendar. If you attempt to associate the same column to multiple categories within one calendar, the editor flags this as an error.

3. **Period uniqueness**  
   The assigned categories for a calendar must uniquely identify each period. Practically, this means that the combination of columns chosen for a given time grain (for example, Year + Week or Year + Month + Day) must uniquely identify each period and avoid ambiguities. The editor validates that your configuration satisfies this rule.

4. **Consistent categorization across calendars**  
   Columns must be associated with the same category across calendars. This prevents inconsistent use of the same column (for example, mapping a `FiscalYear` column as `Year` in one calendar and as `WeekYear` in another). When a column is categorized differently in different calendars, the editor reports a consistency violation.

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