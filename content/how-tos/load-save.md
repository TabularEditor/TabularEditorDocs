---
uid: load-save-model
title: Load and save model metadata
author: Morten Lønskov
updated: 2026-09-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
          note: "Desktop Edition cannot open or save model metadata files."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Load and save model metadata

Tabular Editor reads model metadata into memory from a file, a folder or a server, and writes it back to the same place or to a new one.

> [!NOTE]
> Metadata is the definition of your tables, measures, relationships and so on, not your data. Loading a model doesn't load the rows in its tables. See [Table Preview](xref:pivot-grid) and [Advanced refresh](xref:advanced-refresh) for working with data.

## Loading a model

![The File menu with the Open submenu expanded, listing Model from File, Model from DB, Model from Folder, File and Import from Metric View YAML alongside the Save, Save As and Save to Folder commands](~/content/assets/images/file-menu-open.png)

| Source | Command |
|---|---|
| A `Model.bim` or `.bim` file | **File > Open > Model from file...** |
| A folder structure, in either the JSON or the [Tabular Model Definition Language (TMDL)](xref:tmdl) format | **File > Open > Model from folder...** |
| An Analysis Services or Power BI XMLA database | **File > Open > Model from DB...** (**Ctrl+Shift+O**) |
| A running instance of Power BI Desktop | **File > Open > Model from DB...**, or start Tabular Editor from Power BI Desktop's **External Tools** ribbon |

A `.bim` file must be Compatibility Level 1200 or newer. Earlier levels use the older XML-based format, which Tabular Editor doesn't open.

For everything Tabular Editor recognises, including the supporting file types that aren't model metadata, see [Supported file types](xref:supported-files).

> [!TIP]
> **File > Recent tabular models** reopens a model you had open before, whether it came from a file, a folder or a database.

## Saving a model

**File > Save** (**Ctrl+S**) writes the model back where you loaded it from. A model loaded from a file goes back to that file. A model loaded from a folder goes back into that folder, in the format it already uses. A model loaded from a database is deployed back to that database.

To write a model somewhere else, or in a different format:

- **File > Save As...** saves the model metadata as a single `.bim` file.
- **File > Save to folder...** saves the model metadata as a [folder structure](xref:save-to-folder), in either the JSON or the TMDL format, depending on the serialization mode under **Tools > Preferences > File Formats > Save-to-folder**.

> [!IMPORTANT]
> A model loaded from a legacy JSON folder structure is saved in that same format when you use **File > Save**, even if your preferences say TMDL. The format changes only when you explicitly use **File > Save to folder...**. See [TMDL](xref:tmdl).

## Reverting

**File > Revert** discards everything you've changed since your last save and reloads the metadata from the source.

If an agent, a script or a `git pull` rewrites the metadata files while you have the model open, Tabular Editor notices and reloads the model for you, so the two copies stay in step without a manual revert. See [Auto-reload from disk](xref:auto-reload).

> [!WARNING]
> Back up your model metadata before you let any tool write to it, Tabular Editor included. A save overwrites the source, and **File > Revert** can't bring back changes you've already saved.

## Next steps

- [Save to folder](xref:save-to-folder) for the folder formats and the serialization settings that control how a model is split across files.
- [Enabling parallel development using Git and Save to Folder](xref:parallel-development) if more than one person works on the model.
- [Deployment](xref:deployment) to write the model to an Analysis Services server rather than to disk.
