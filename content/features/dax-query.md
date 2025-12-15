---
uid: dax-query
title: DAX Queries
author: Morten Lønskov
updated: 2025-08-27
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# DAX Queries

Tabular Editor has a built-in DAX query window to write and execute DAX queries against the semantic model.

A widespread use case for DAX queries is the DAX query produced by the [Power BI Performance Analyzer](https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/), where it is possible to copy the query of each visual for troubleshooting, debugging, or detailed performance analysis.

The window can be opened while connected to a semantic model using either the **File > New > DAX Query** menu or the toolbar shortcut.

![Dax Query New](~/content/assets/images/features/dax_query_window/create_new_dax_query.png)

The built-in context-aware DAX Editor ensures that only the two valid DAX keywords are available when starting a new query: DEFINE or EVALUATE (Press Ctrl+Space to verify for yourself)

## DAX Query Options

The DAX query window has five different query options.

![Dax Query Toolbar](~/content/assets/images/features/dax_query_window/dax_query_toolbar.png)


1. **Execute (F5)**: If there is a selection, it executes the selected DAX; otherwise, it executes the full query in the DAX Query editor.
2. **Execute full query**: It executes the full query in the DAX Query editor
3. **Execute Selection (Shift+F5)**: If there is a selection, it executes it. Otherwise, it executes the EVALUATE statement where the cursor is currently located.
4. **Stop**: This button cancels the current query execution.
5. **Auto Execute Query**: It allows for keeping track of the connected semantic model and updating the query results whenever something changes in the model. This can be useful for understanding e.g. how the result of a measure changes if modified.
6. **Keep sorting and filtering**: It allows users to control how sorting and filtering are preserved in the result grid(s) when executing queries. There are three preferences available:
   - **Never**: Sorting and filtering reset each time the query runs.
   - **When query is modified**: Sorting and filtering reset only when the query structure changes.
   - **Always**: Sorting and filtering persist as long as columns remain in the new query.

The default values of "Auto Execute Query" and "Keep Sorting and Filtering" preferences can be set up in the Preferences dialog: **Tools > Preferences... > Data browsing > DAX Query** > Basic. 

### Adding or Updating Measures, Columns and Tables with DAX Queries

Tabular Editor (3.12.0 and higher) has the ability to add or change measures directly through the DAX Query window.

From Tabular Editor 3.23.0, Apply and Apply selection also process DEFINE COLUMN and DEFINE TABLE statements. Tabular Editor will create the corresponding calculated columns/tables in your model, or update their expressions if they already exist.

There are four options for applying DAX Query defined measures, columns and tables to the model: 

![Dax Query Apply Measure](~/content/assets/images/features/dax_query_window/dax_query_apply_measure.png)

The "Apply" option syncs the DAX expression for all measures, columns or tables explicitly defined in the query to the definition of the object. Any measures, columns or tables that do not already exist are created.

"Apply Measures & Sync" applies the DAX expression to the definition of the measures, columns or tables and saves the model.

The "Apply Selection" and "Apply Selection & Sync" will only apply the measures, columns or tables within the current selection of the query editor.

Unlike the [DAX Script feature](xrefid:dax-scripts), only the expression property of a measure can be updated this way, as the DAX query syntax does not support specifying other properties, such as Description, Display Folder, etc.

The "Apply" option has also been added to the right-click context menu.

![Dax Query Apple Right Click](~/content/assets/images/features/dax_query_window/dax_query_apply_measure_right_click.png)

The shortcuts for these commands are:

- Apply (F7)
- Apply Measures & Sync (Shift+F7)
- Apply Selection (F8)
- Apply Selection and Synch (Shift F7)

## DAX Query Example

A DAX query always returns a table of results, and the simplest form of DAX query to create is one that evaluates a table within the model.

```DAX
EVALUATE
Products
```

![Dax Query Evaluate Table](~/content/assets/images/features/dax_query_window/evaluate_table.png)

It is also possible to return the value of a measure, but a table constructor {} is required around the measure name to turn the scalar value into a 1x1 table.

```DAX
EVALUATE
{ [Invoice Lines] }
```

![Dax Query Evaluate Measure](~/content/assets/images/features/dax_query_window/evaluate_measure.png)

### Multiple EVALUATE statements

It is perfectly possible to have multiple EVALUATE statements inside the same DAX query. This query type is most often encountered with Power BI Performance Analyzer queries.

Both tables are returned in the below statement but as separate row tabs in the result pane.

```DAX
EVALUATE
Products

EVALUATE
Customers
```

![Dax Query Evaluate Multiple Tables](~/content/assets/images/features/dax_query_window/multiple_evaluate_table.png)

## Debugging DAX Query

DAX queries are one of the two places where it is possible to run the [DAX Debugger](xrefid:dax-debugger), the other being the Pivot Grid.

The DAX debugger unlocks the ability to understand how the DAX works inside a single cell. To start the debugger simply right click on the desired cell and choose 'Debug cell', which will start the debugger in the context of the chosen cell.

![Dax Query Debugger](~/content/assets/images/features/dax_query_window/dax_query_open_dax_debugger.gif)

## Export DAX Query results

Tabular Editor 3, beginning from version 3.16.0, introduces the new capability of exporting the results of a DAX Query to either CSV or Excel. After running the DAX Query, a button activates in the toolbar, enabling users to save the results locally in CSV or Excel format.

> [!TIP]
> To Export more than 1001 rows choose "click to get all rows" after running the DAX Query

![Dax Query Export Data](~/content/assets/images/features/dax_query_window/dax_query_export_data.png)
