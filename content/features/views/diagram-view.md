---
uid: diagram-view
title: Diagram View
author: Morten Lønskov
updated: 2025-04-24
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
# Diagram View

The **Diagram View** in Tabular Editor 3 is a visual representation of the semantic model. It provides an intuitive layout for viewing tables, their columns, and the relationships between them. It is particularly helpful for understanding the schema at a glance, creating relationships, and presenting models to stakeholders. A diagram can be saved as a stand alone file. See <xref:supported-files#diagram-file-te3diag> for more information.

> [!NOTE]
> We recommend creating multiple smaller diagrams over few large diagrams. When a diagram contains more than 20 or so tables, it quickly becomes overwhelming and difficult to understand.

After loading a model in Tabular Editor 3, choose the **File > New > Diagram** menu option to create a new diagram or open a new diagram in the main toolbar and drag and drop a table from the TOM Explorer to the diagram window.

## Using the diagram view

## Adding tables

Add initial tables to the diagram in any of the following ways:

- (Multi-)select tables in the TOM Explorer, then right-click and choose **Add to diagram**.
- (Multi-)select tables in the TOM Explorer, then drag the tables over to the diagram
- Use the **Diagram > Add tables...** menu option, and (multi-)select the tables you want to add through the dialog box.
  ![Diagram Add Tables](~/content/assets/images/diagram-add-tables.png)

  To add additional tables to the diagram, use the technique above again, or right-click on an existing table in the diagram and choose one of the following options:
  - **Add tables that filter this table**: Adds all tables to the diagram which may, directly or indirectly through other tables, filter the currently selected table. Useful when starting from a fact table.
  - **Add all related tables**: Adds all tables to the diagram which are directly related to the currently selected table. Useful when starting from a dimension table.
    ![Add Related Tables](~/content/assets/images/add-related-tables.png)
  
  Before proceeding, rearrange and resize the tables in the diagram to suit your preferences, or use the **Diagram > Auto-arrange** feature to have Tabular Editor 3 lay out the tables automatically.

## Modifying relationships using the diagram

To add a new relationship between two tables, locate the column on the fact table (many-side) of the relationship, and drag that column over to the corresponding column on the dimension table (one-side). Confirm the settings for the relationship and hit **OK**.

![Create Relationship](~/content/assets/images/create-relationship.png)

To edit an existing relationship, right-click on it and choose **Edit relationship**. The right-click menu also contains shortcuts for reversing or deleting a relationship, as shown on the screenshot below.

![Edit Relationship Diagram](~/content/assets/images/edit-relationship-diagram.png)

> [!NOTE]
> You can also create relationships without using a diagram, through the TOM Explorer. Locate the column from which the relationship should start (many-side / fact-table side), right-click and choose **Create > Relationship from**. Specify the destination column in the Create Relationship dialog that appears on the screen.

## Saving a diagram

To save a diagram, simply use the **File > Save** (CTRL+S) option. Tabular Editor 3 will prompt you to save the diagram if you close the document or the application while the diagram has unsaved changes.

> [!TIP]
> The same diagram file can be loaded for different data models. Diagrams reference tables by their names. Any tables not present in the model upon diagram load are simply removed from the diagram.

> [!NOTE]
> Every time you add or modify a relationship, you will have to run a "calculate" refresh on the data model, before the relationships can be used when querying the model.

## Diagram Features

### Context Menu for Table Actions

Right-clicking anywhere in the Diagram View opens a context menu that provides quick access to several options:

![Diagram Context Menu](~/content/assets/images/diagram-context-menu.png)

- **Add tables...**: Opens a dialog to manually add additional tables to the diagram.
- **Add tables that filter this table**: Automatically brings in related tables that filter the current one.
- **Add all related tables**: Loads all tables that share relationships with the selected table.
- **Fit to page**: Adjusts the diagram zoom to fit all visible tables.
- **Auto-Arrange**: Automatically arrange tables into a star schema
- **Remove from diagram**: Hides the selected table from the current view.

### Relationship Indicators

Relationships between tables are illustrated using directional arrows:

- `1 - *`: Indicates a one-to-many relationship.
- `* - *`: Indicates a many-to-many relationship.
- `➝`: Indicates a single direction relationship, with the arrow defining the filter direction of the relationship.
- `⟷`: Indicates a bi-directional cross-filtering relationship.

These visual markers allow for quick assessment of filter directionality and cardinality.

### Column Display Toggle

A **chevron toggle** is available in the top-right corner of each table, by clicking it you will toggle between the following options:

![Diagram Chevron Toggle](~/content/assets/images/diagram-chevron-toggle.png)


- **All Columns**: Displays all columns.
- **Key Columns Only**: Displays only primary and foreign keys.
- **No Columns**: Hides all columns, showing only the table header.

The toggle helps reduce clutter, especially in complex models with many columns, making it easier to focus on relationships.

### Column Data Type Icons

Each column in the diagram is accompanied by an icon representing its data type:

- <img src="~/content/assets/images/icons/String.svg" alt="Text Icon" width="16" height="16"> for string/text values
- <img src="~/content/assets/images/icons/Integer.svg" alt="Integer Icon" width="16" height="16"> for integer numbers
- <img src="~/content/assets/images/icons/Double.svg" alt="Double Icon" width="16" height="16"> for double / floating-point decimal numbers
- <img src="~/content/assets/images/icons/Currency.svg" alt="Currency Icon" width="16" height="16"> for currency / fixed-point decimal numbers
- <img src="~/content/assets/images/icons/Binary.svg" alt="Binary Icon" width="16" height="16"> for binary values
- <img src="~/content/assets/images/icons/TrueFalse.svg" alt="Boolean Icon" width="16" height="16"> for boolean (true/false) values
- <img src="~/content/assets/images/icons/Calendar.svg" alt="Date Icon" width="16" height="16"> for date/time values


This quick visual reference supports quick data validation and helps understand the data structures. 