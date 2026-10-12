---
uid: diagram-view
title: Diagram View
author: Morten Lønskov
updated: 2026-09-14
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

[!include[diagram-basics](diagram-basics.partial.md)]

## Diagram Features

### Context Menu for Table Actions

Right-clicking anywhere in the Diagram View opens a context menu that provides quick access to several options:

![Diagram Context Menu](~/content/assets/images/diagram-context-menu.png)

- **Add tables...**: Opens a dialog to manually add additional tables to the diagram.
- **Add tables that filter this table**: Automatically brings in related tables that filter the current one.
- **Add all related tables**: Loads all tables that share relationships with the selected table.
- **Edit relationship**: Opens the relationship editor for the selected relationship. Only visible when a relationship is selected.
- **Invert relationship**: Swaps the from and to sides of the selected relationship. Only visible when a relationship is selected.
- **Activate relationship**: Activates an inactive relationship. Only visible when an inactive relationship is selected.
- **Deactivate relationship**: Deactivates an active relationship. Only visible when an active relationship is selected.
- **Fit to page**: Adjusts the diagram zoom to fit all visible tables.
- **Auto-Arrange**: Automatically arrange tables into a star schema.
- **Remove from diagram**: Hides the selected table from the current view.
- **Delete relationship**: Deletes the selected relationship from the model. Only visible when a relationship is selected.

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