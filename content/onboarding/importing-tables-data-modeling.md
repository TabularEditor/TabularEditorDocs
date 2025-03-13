---
uid: importing-tables-data-modeling
title: Importing tables and data modeling
author: Daniel Otykier
updated: 2021-10-08
applies_to:
  editions:
    - edition: Desktop
      partial: TE3 Desktop Edition includes this feature. External tools adding/editing tables, columns and relationships against a Power BI Desktop model is not supported by Microsoft, however.
    - edition: Business
    - edition: Enterprise
---
# Importing tables and data modeling

This article describes how to use the [Table Import Wizard](#table-import-wizard) of Tabular Editor 3, to add new tables to the model. There is also a section on how to [update the table schema](#updating-table-schema) of an existing table. Lastly, we cover how to use the [diagram tool](#working-with-diagrams) to define and edit relationships between tables.

## Table Import Wizard

[!include[importing-tables1](~/content/te3/import-tables.partial.md)]

# Working with diagrams

In Tabular Editor 3, **diagrams** are documents that can be used to visualize and edit the relationships between tables in the model. You can create as many diagrams as you want to visualize certain areas of your model. A diagram can be saved as a stand alone file. See <xref:supported-files#diagram-file-te3diag> for more information.

> [!NOTE]
> We recommend creating multiple smaller diagrams over few large diagrams. When a diagram contains more than 20 or so tables, it quickly becomes overwhelming and difficult to understand.

After loading a model in Tabular Editor 3, choose the **File > New > Diagram** menu option to create a new diagram.

## Adding tables

Add initial tables to the diagram in any of the following ways:

- (Multi-)select tables in the TOM Explorer, then right-click and choose **Add to diagram**.
- (Multi-)select tables in the TOM Explorer, then drag the tables over to the diagram
- Use the **Diagram > Add tables...** menu option, and (multi-)select the tables you want to add through the dialog box.
  ![Diagram Add Tables](~/assets/images/diagram-add-tables.png)

To add additional tables to the diagram, use the technique above again, or right-click on an existing table in the diagram and choose one of the following options:
- **Add tables that filter this table**: Adds all tables to the diagram which may, directly or indirectly through other tables, filter the currently selected table. Useful when starting from a fact table.
- **Add all related tables**: Adds all tables to the diagram which are directly related to the currently selected table. Useful when starting from a dimension table.
  ![Add Related Tables](~/assets/images/add-related-tables.png)

Before proceeding, rearrange and resize the tables in the diagram to suit your preferences, or use the **Diagram > Auto-arrange** feature to have Tabular Editor 3 lay out the tables automatically.

## Modifying relationships using the diagram

To add a new relationship between two tables, locate the column on the fact table (many-side) of the relationship, and drag that column over to the corresponding column on the dimension table (one-side). Confirm the settings for the relationship and hit **OK**.

![Create Relationship](~/assets/images/create-relationship.png)

To edit an existing relationship, right-click on it and choose **Edit relationship**. The right-click menu also contains shortcuts for reversing or deleting a relationship, as shown on the screenshot below.

![Edit Relationship Diagram](~/assets/images/edit-relationship-diagram.png)

> [!NOTE]
> You can also create relationships without using a diagram, through the TOM Explorer. Locate the column from which the relationship should start (many-side / fact-table side), right-click and choose **Create > Relationship from**. Specify the destination column in the Create Relationship dialog that appears on the screen.

## Saving a diagram

To save a diagram, simply use the **File > Save** (CTRL+S) option. Tabular Editor 3 will prompt you to save the diagram if you close the document or the application while the diagram has unsaved changes.

> [!TIP]
> The same diagram file can be loaded for different data models. Diagrams reference tables by their names. Any tables not present in the model upon diagram load are simply removed from the diagram.

> [!NOTE]
> Every time you add or modify a relationship, you will have to run a "calculate" refresh on the data model, before the relationships can be used when querying the model.

# Next steps

- @refresh-preview-query
- @creating-and-testing-dax