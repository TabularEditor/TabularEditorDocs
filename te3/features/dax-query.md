---
uid: dax-query
title: DAX Queries
author: Morten Lønskov
updated: 2023-11-09
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# DAX Queries

Tabular Editor has a built in DAX query window to write and execute DAX queries against the semantic model.  

A very common use case for DAX queries is the DAX query produced by the [Power BI Performance Analyzer](https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/), where it is possible to copy the query of each visual for troubleshooting, debugging or detailed performance analysis. 

The window can be opened while connected to a sematic model by using either the **File > New > DAX Query** folder or the toolbar shortcut.

![Dax Query New](~/images/features/dax_query_window/create_new_dax_query.png)

The built in context aware intellisense ensures that only the two valid DAX keywords are available when starting a new query: DEFINE or EVALUATE (Press Ctrl+Space to verify for yourself)

## DAX Query Options

The DAX query window has four standard different query options.

![Dax Query New](~/images/features/dax_query_window/dax_query_toolbar.png)


1. Execute (F5)
2. Execute Selection (Shift+F5)
3. Stop 
4. Auto Execute Query

The Auto Execute Query allows for keeping track of the connected semantic model and update the query results whenever something changes in the model. This can be useful for understanding e.g. how the result of a measure changes if modified. 

### Adding or Updating Measures with DAX Queries

Tabular Editor (3.12.0 and higher) has the ability to add or change measures directly through the DAX Query window.

In addition to the above mentioned options four other have been introduced.

![Dax Query New](~/images/features/dax_query_window/dax_query_apply_measure.png)

The "Apply" option sync the DAX expression for all measures explicitly defined in the query, to the definition of the measures. Any measures that do not already exist, are created.

"Apply Measures & Sync" applies the DAX expression to the definition of the measures and saves the model.

The "Apply Selection" and "Apply Selection & Sync" will only apply the measures within the current selection of the query editor.

Unlike the [DAX Script feature](xrefid:dax-scripts), only the expression property of a measure can be updated this way, as the DAX query syntax does not support specifying other properties, such as Description, Display Folder, etc.

The "Apply" option has also been added to the right-click context menu.

![Dax Query New](~/images/features/dax_query_window/dax_query_apply_measure_right_click.png.png)

The shortcuts for these commands are:

- Apply (F7)
- Apply Measures & Sync (Shift+F7)
- Apply Selection (F8)
- Apply Selection and Synch (Shift F7)

## DAX Query Example

A DAX query always return a table of results, and the simplest form of DAX query to create is one that evaluates a table within the model.

```DAX
EVALUATE
Products
```
![Dax Query New](~/images/features/dax_query_window/evaluate_table.png)

It is also possible to return the value of a measure but a table constructor {} is required around the measure name, to turn the scalar value into a 1x1 table.


```DAX
EVALUATE
{ [Invoice Lines] }
```
![Dax Query New](~/images/features/dax_query_window/evaluate_measusre.png)

### Multiple EVALUATE statements
It is perfectly possible to have multiple EVALUATE statements inside the same DAX query. This type of query is most often encountered with Power BI Performance Analyzer queries.

Both tables are returned in the below statement, but as separate row tabs in the result pane.

```DAX
EVALUATE
Products

EVALUATE
Customers
```

![Dax Query New](~/images/features/dax_query_window/multiple_evaluate_table.png)

## Debugging DAX Query
DAX queries is one of the two places where it is possible to run the [DAX Debugger](xrefid:dax-debugger), the other being the Pivot Grid.

The DAX debugger unlocks the ability to understand how the DAX works inside a single cell. To start the debugger simply right click on the desired cell and choose 'Debug cell', which will start the debugger in the context of the chosen cell. 

![Dax Query New](~/images/features/dax_query_window/dax_query_open_dax_debugger.gif)

