---
uid: pivot-grid
title: Pivot Grids
author: Morten Lønskov
updated: 2024-01-22
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Pivot Grids

After adding or editing DAX measures in a model, it is common for model developers to test these measures. Traditionally, this was typically done using client tools such as Excel or Power BI. With Tabular Editor 3, you can now use **Pivot Grids** which behave much like the famous PivotTables of Excel. The Pivot Grid lets you quickly create summarized views of the data in your model, allowing you test the behavior of your DAX measures when filtering and slicing by various columns and hierarchies.

To create a new Pivot Grid, use the **File > New > Pivot Grid** option. From here, you can either drag measures, columns and hierarchies from the TOM Explorer into the grid, or you can use the **Pivot Grid > Show fields** menu option to display a popup list of all fields that can be dragged into the Pivot Grid (see screenshot below).

![Show Fields Pivot](~/images/show-fields-pivot.png)

As fields are dragged into the Pivot Grid, Tabular Editor generates MDX queries that are sent to Analysis Services, to display the resulting data. In this regard, the behavior is very similar to Pivot Tables in Excel. You can rearrange fields in the Pivot Grid by dragging and dropping, and there are various right-click menu options available for customizing how the data is displayed.

![Customizing Pivot Grids](../images/customizing-pivot-grids.png)

The Pivot Grid is automatically refreshed when a change is made to the model or a refresh operation finishes. You can toggle this auto-refresh capability within the **Pivot Grid** menu.

> [!Note]
> The Pivot Grid is an third-party tool and has certain inbuilt limitations. Two specific limitations are that it does not work with [hidden fields](https://github.com/TabularEditor/TabularEditor3/issues/345) and it only show column and row values when there are [measure present](https://github.com/TabularEditor/TabularEditor3/issues/776)