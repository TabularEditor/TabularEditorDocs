---
uid: pivot-grid
title: Pivot Grids
author: Daniel Otykier
updated: 2024-05-28
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---

# Pivot Grids

> [!NOTE]
> Information in this article relates to Tabular Editor 3.16.0 or newer. Please make sure you are using the latest version of Tabular Editor 3 to take advantage of the new features and improvements.

While developing semantic models, you may often want to test that your DAX expressions return the expected values. Traditionally, this was done using client tools such as Excel or Power BI. With Tabular Editor 3, you can use **Pivot Grids** which behave much like the widely known PivotTables in Excel. The Pivot Grid lets you quickly create summarized views of the data in your model, allowing you to test the behavior of your DAX measures when filtering and slicing by various columns and hierarchies.

![Pivot Grid Example](images/pivot-grid-example.png)

The screenshot above shows a Pivot Grid containing two measures, `[Total Net Order Value]` and `[Net Orders]`, which is sliced horizontally by Year, filtered to 2021 and 2022, and vertically by the Product Hierarchy. Tabular Editor 3 users can use this feature to ensure that DAX expressions behind the measures are working as expected and to quickly validate the data in the model.

By default, the Pivot Grid auto-updates every time you save changes to the semantic model (Ctrl+S). Thus, you can quickly iterate on your DAX expressions and see the results in the Pivot Grid without having to wait for the model to refresh by changing your measures, saving the model, and directly seeing the new measure definition reflected in the Pivot Grid. A good workflow is to open the Pivot Grid in a separate window while working on DAX expressions in the **Expression Editor** or using a **DAX Script**.

> [!TIP]
> Some clarifications on terminology:
>
> - **Fields** refers to model measures, KPIs, columns and hierarchies. In other words, anything that can be dragged into the Pivot Grid.
> - **KPIs** are a special type of measure that can be created in Tabular Editor. They are displayed in the Pivot Grid just like measures, but with a special icon to indicate that they are KPIs. Each KPI can have up to 3 different values (target, trend, and status), which are displayed separately in the Pivot Grid.
> - **Columns** in the Pivot Grid (such as in the term "Column Area") should not be confused with columns in the model. In the Pivot Grid, columns are used to slice the data horizontally, while rows are used to slice the data vertically.
> - **Cells** in the Pivot Grid are the individual data points where a row and a column intersect. Each cell contains a single value, which is the result of the DAX expression of the specific measure, evaluated under the filter context produced by values in the _Row Area_ and _Column Area_, in combination with any filters applied to fields in the _Filter Area_.

> [!NOTE]
> Developers with a multidimensional background may be more familiar with the terms _Dimensions_ and _Attributes_. In semantic models, _Dimensions_ are represented by model _tables_, and _Attributes_ are represented by model _columns_. _Hierarchies_ in a semantic model, is just a way to group columns together, such as in a calendar hierarchy: Year > Quarter > Month > Day. Such hierarchies used to be called _Attribute Hierarchies_ or _User-Defined Hierarchies_ in multidimensional models.

## Creating a Pivot Grid

You can create a new, empty Pivot Grid through the **File > New > New Pivot Grid** menu option. Alternatively, select one or more measures in the **TOM Explorer**, right-click or go to the **Measure** menu and select **Add to Pivot Grid**, to create a new Pivot Grid with the selected measures.

![Create Pivot Grid From TOM Explorer](images/create-pivot-grid-from-TOM-Explorer.png)

You can create as many Pivot Grids as you like.

> [!IMPORTANT]
> The option to create a Pivot Grid is only available while Tabular Editor 3 is connected to an instance of Analysis Services or the Power BI / Fabric XMLA endpoint.

## Pivot Grid layout

The Pivot Grid is divided into 4 areas: **Filter Area**, **Column Area**, **Row Area**, and **Data Area**. You can drag fields from the **Field List** or the **TOM Explorer** into these areas to create a Pivot Grid layout. The **Data Area** area is where you place measures or KPIs, while the **Row Area** and **Column Area** are used to slice the data by hierarchies and columns. The **Filter Area** is used to filter the data based on values in columns or hierarchies.

![Empty Pivot Grid Highlighted](images/empty-pivot-grid-highlighted.png)

The screenshot above shows an empty Pivot Grid layout. The 4 empty boxes at the bottom of the Field List represent the 4 areas of the Pivot Grid. You can drag fields from the Field List into these listboxes to create a Pivot Grid layout. Alternatively, you can drag fields directly into the Pivot Grid.

## Pivot Grid menu and toolbar

By default, when a Pivot Grid is the active window in Tabular Editor 3, a **Pivot Grid** menu and toolbar are available. The menu contains the same actions as the toolbar.

![Pivot Grid Toolbar](images/pivot-grid-toolbar.png)

![Pivot Grid Menu](images/pivot-grid-menu.png)

These actions are:

- **Impersonation...**: Displays a dialog that allows you to specify a role or user to impersonate through the Pivot Grid. This is useful when you want to test the behavior of your model for different users or roles, such as when [RLS or OLS](xref:data-security-about) has been applied to the model.
- **Refresh**: Re-execute the query generated by the Pivot Grid. This is useful when auto-refresh is disabled, or if changes have been made to the model outside of Tabular Editor 3.
- **Auto Refresh**: Toggles auto-refresh on or off. When auto-refresh is enabled, the Pivot Grid will automatically refresh every time you save changes to the model, or when a [Data Refresh operation](xref:data-refresh-view) completes.
- **Clear filters**: Clears all filters from the Pivot Grid.
- **Clear**: Removes all fields from the Pivot Grid.
- **Show empty values on columns**: Toggles whether empty values should be shown in the Pivot Grid, for fields that are added to the Pivot Grids Column Area.
- **Show empty values on rows**: Toggles whether empty values should be shown in the Pivot Grid, for fields that are added to the Pivot Grids Row Area.
- **Show fields**: Display and move focus to the Field List.

## Field List

By default, the Field List is displayed on the right side of the Pivot Grid. The Field List contains all the fields (measures, KPIs, columns, and hierarchies) that are available in the model. You can drag fields from the Field List into the Pivot Grid to create a layout. You can also drag fields between the different areas of the Pivot Grid to rearrange the layout.

The Field List itself can be docked to the left or right side of the Pivot Grid, above or below, it can be hidden, or it can be undocked so that it "floats" as a separate window. If you have multiple Pivot Grids open, each Pivot Grid has its own Field List.

If you would like the Field List to not be shown by default, uncheck the **Always show field list** option under **Tools > Preferences > Data Browsing > Pivot Grid > Field List**.

You can change the default layout of the Field List under **Tools > Preferences > Data Browsing > Pivot Grid > Field List > Layout**. You can also change the layout of any field lists, by right-clicking in an empty area of the Field List and choosing the desired layout from the context menu.

![Field List Settings](images/field-list-settings.png)

By default, any field you add to the Pivot Grid remains visible in the Field List. If you would like to hide fields that are added to the Pivot Grid, you can uncheck the **Keep fields visible** option under **Tools > Preferences > Data Browsing > Pivot Grid > Field List** (this behavior is similar to how Pivot Grid worked prior to Tabular Editor v. 3.16.0).

If you are working on a large, complex model, and you are expecting measures used in the Pivot Grid to be relatively slow, you can check the **Defer Layout Update** option at the bottom of the Field List. This will prevent the Pivot Grid from updating the layout every time you add or remove a field, which can be useful, if you intend to make multiple changes to the Pivot Grid layout before updating it. Hit the **Update** button to apply the changes to the Pivot Grid.

> [!IMPORTANT]
> Columns without an attribute hierarchy (IsAvailableIn MDX = false) cannot be used in the Pivot Grid and are not shown in the Field list.

## Customizing Pivot Grids

### Adding fields

There are several ways to add a field to a Pivot Grid:

**From the TOM Explorer:**

- Right-click on one or more _measures_ and choose **Add to Pivot Grid**.
- Right-click on a _column_ or _hierarchy_ and choose any of the **Add to pivot**-options (choose between rows, columns, or filters).
- If a measure, column or hierarchy is already shown in the Pivot Grid, the right-click options will allow you to **Remove from Pivot Grid**. in addition, you will see options to move columns or hierarchies between the different areas of the Pivot Grid.
- All of the options above are also available through the **Measure**, **Column**, and **Hierarchy** menus (respectively), when one or more such objects are selected in the TOM Explorer.
- In addition to the above, you can also drag one or more measures, columns, or hierarchies from the TOM Explorer into the Pivot Grid areas.

![Add hierarchy to Pivot Grid through TOM Explorer](images/add-through-tom-explorer.png)

**From the Field List:**

- Drag a field from the Field List into the Pivot Grid.
- Drag a field from the Field List into the area listboxes at the bottom of the Field List to add it to the Pivot Grid.
- Right-click on a field in the Field List for options to add it to the Pivot Grid.
- If a field is already showing in the Pivot Grid, the right-click context menu will also have an option to remove the field, or move it to a different area (column/hierarchy fields only).
- Double-clicking on a field will immediately add it to the Pivot Grid. Measures/KPIs are added to the Data Area, while columns and hierarchies are added to the Filter Area.

![Add Through Field List](images/add-through-field-list.png)

### Adjusting fields

After fields have been added to the Pivot Grid, you can adjust the width of columns to better accommodate their content. Double-clicking on a column header separator will automatically adjust the column width to fit the content of the column. You can also drag the column header separator to manually adjust the column width. Lastly, you can use the **Best Fit** or **Set width...** context menu options by right-clicking on the column header.

![Best Fit Columns 2](images/best-fit-columns-2.png)

To apply a "Best Fit" or set a specific pixel width for all columns in the Pivot Grid simultaneously, right-click on the "Values" header and select the desired option from the context menu.

By default, field headers will expand vertically to fit the content of the field name. If you would like to limit the height of field headers to one row, you can disable the **Word wrap field headers**-option under **Tools > Preferences > Pivot Grid > Field Headers**.

To change the order of fields in the Pivot Grid, you can drag fields between the different areas of the Pivot Grid. You can also drag fields within the same area to change their order. To remove a field from the Pivot Grid, drag it back to the Field List or right-click on the field and choose **Remove from Pivot Grid** from the context menu.

If you want measures to be displayed on rows rather than on columns, drag the "Values" field from the Column Area to the Row Area.

### Visualization rules

You can add visualization rules to cells in the Pivot Grids, which is useful for highlighting cells based on their values, for example in order to better spot outliers. To add visualization rules, right-click on any Data Area cell in the Pivot Grid, and choose which rules to apply from the context menu (see screenshot below).

![Customizing Pivot Grids](images/customizing-pivot-grids.png)

## Persisting Pivot Grid layouts

When you close a Pivot Grid, Tabular Editor will prompt you to save the layout of the Pivot Grid. If you choose to save the layout, the next time you open the Pivot Grid, it will be restored to the same layout as when you closed it. You can also save the layout of a Pivot Grid manually by hitting (Ctrl+S) or using the **File > Save** option, while the Pivot Grid is the active window.

The file extension used for saving Pivot Grid layouts is `.te3pivot`. This is a simple json file that specifies which model objects are shown in the Pivot Grid, and in which areas they are placed. Objects are referenced by name and lineage tag (if present), so the Pivot Grid layout can generally be restored even if the model has been modified since the layout was saved.

> [!NOTE]
> It is possible to open a Pivot Grid layout that was created in a different model, but be aware that the fields in the layout may not exist in the model you are currently connected to. In such cases, the Pivot Grid will show a warning message, and any fields that do not exist in the model will be removed from the layout. The warning message may be toggled off under **Tools > Preferences > Data Browsing > Pivot Grid > Show warning if Pivot Grid doesn't match model**.

## Additional features

The Pivot Grid has a few more features that are useful to know about:

- If you right-click on a field, you will have the option to **Go to** that field. This brings the TOM Explorer into focus, with the equivalent model object selected. For measures and calculated columns, the **Expression Editor** will be brought into focus, with the DAX expression of the measure displayed.
- If you right-click on a cell in the Pivot Grid, you can select the option to **Debug this value**. This will launch the [**DAX Debugger**](xref:dax-debugger) starting from the specific measure and filter context that produced the value in the cell.

## Limitations and known issues

Below is a list of known limitations and issues with Pivot Grids in Tabular Editor 3.16.0, which we are working to address in future releases:

- Format rules (such as icon sets, data bars, etc.) are not properly persisted when saving a Pivot Grid layout as a `.te3pivot` file.
- The .te3pivot file does not currently store the state of the "Show empty values on columns" and "Show empty values on rows" options.
- If you open a .te3pivot file on a model different from the one the layout was saved from, fields that do not exist in the current model will be removed from the layout. Hitting Save (Ctrl+S) will save the layout with the removed fields removed. We may change this behavior in a future release so that the .te3pivot file is not overwritten without explicit confirmation.