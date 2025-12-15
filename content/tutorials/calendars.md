---
uid: calendars
title: Calendars (Enhanced Time Intelligence)
author: Daniel Otykier
updated: 2025-09-15
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

The September 2025 release of Power BI Desktop introduced a new Public Preview feature called "Enhanced Time Intelligence". This feature lets you define custom calendars in your semantic model, and it also introduces 8 new DAX functions that work with these calendars, enabling week-based time intelligence calculations that were difficult to perform previously.

## Defining a Calendar

![Creating a calendar](~/content/assets/images/tutorials/calendar-create.png)

1. Right-click on a table in your model (typically a Date table) and select **Create > Calendar...**.
2. Give your calendar a name, e.g. "Fiscal"

Once calendars are added to a table, they will be shown in the TOM Explorer under the **Calendars** node:

![Calendar in TOM Explorer](~/content/assets/images/tutorials/calendar-tom-explorer.png)

Before you can use a calendar in your DAX calculations, you need to configure it by specifying which columns in the table represent the different calendar attributes. You can do this by right-clicking on the calendar in the TOM Explorer, then choosing the **Edit Column Mappings...** option:

![Editing calendar column mappings](~/content/assets/images/edit-calendar-mappings.png)

For each calendar, you can add one or more so-called **Column Associations**. Each such association maps a column from the table, to a specific **Time Unit** (e.g. Year, Month, Week, etc.). You can also add additional associated columns for each mapping, which are typically used for columns that represent the same time unit, but in a different format. For example, you might have a "Month" column that contains the month number (1-12), and a "Month Name" column that contains the month name ("January", "February", etc.). Both of these columns can be associated with the "MonthOfYear" time unit.

![Calendar column associations](~/content/assets/images/tutorials/calendar-example.png)

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