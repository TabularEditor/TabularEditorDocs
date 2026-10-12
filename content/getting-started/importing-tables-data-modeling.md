---
uid: importing-tables-data-modeling
title: Importing tables and data modeling
author: Daniel Otykier
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
# Importing tables and data modeling

This article describes how to use the [Table Import Wizard](#table-import-wizard) of Tabular Editor 3, to add new tables to the model. There is also a section on how to [update the table schema](#updating-table-schema) of an existing table. Lastly, we cover how to use the [diagram tool](#working-with-diagrams) to define and edit relationships between tables.

## Table Import Wizard

[!include[importing-tables1](../features/import-tables.partial.md)]

# Working with diagrams

In Tabular Editor 3, **diagrams** are documents that can be used to visualize and edit the relationships between tables in the model. You can create as many diagrams as you want to visualize certain areas of your model. A diagram can be saved as a standalone file. See <xref:supported-files#diagram-file-te3diag> for more information.

> [!NOTE]
> We recommend creating multiple smaller diagrams over few large diagrams. When a diagram contains more than 20 or so tables, it quickly becomes overwhelming and difficult to understand.

After loading a model in Tabular Editor 3, choose the **File > New > Diagram** menu option to create a new diagram.

[!include[diagram-basics](../features/views/diagram-basics.partial.md)]

# Next steps

- @refresh-preview-query
- @creating-and-testing-dax