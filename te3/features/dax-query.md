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

The window can be opened while connected to a sematic model by using either the **File > New > DAX Query** menu or the toolbar shortcut.

![Dax Query New](~/images/features/dax_query_window/create_new_dax_query.png)

The built in context aware intellisense ensures that only the two valid DAX keywords are available when starting a new query: DEFINE or EVALUATE (Press Ctrl+Space to verify for yourself)

## DAX Query Options

The DAX query window has four different query options.

![Dax Query New](~/images/features/dax_query_window/dax_query_toolbar.png)


1. Execute (F5)
2. Execute Selection (Shift+F5)
3. Stop 
4. Auto Execute Query

The Auto Execute Query allows for keeping track of the connected semantic model and update the query results whenever something changes in the model. This can be useful for understanding e.g. how the result of a measure changes if modified. 

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

