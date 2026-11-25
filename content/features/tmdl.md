---
uid: tmdl
title: Tabular Model Definition Language (TMDL)
author: Daniel Otykier
updated: 2026-11-12
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Tabular Model Definition Language (TMDL)

**TMDL** is a model metadata file format [announced by Microsoft in April 2023](https://powerbi.microsoft.com/en-us/blog/announcing-public-preview-of-the-tabular-model-definition-language-tmdl/). It aims to provide a human-readable, text-based alternative to the JSON-based model.bim file format. TMDL is inspired by YAML, and as such, is easy to read and write, with minimal use of string quotes and escape characters. It also serializes a model as several smaller files in a folder structure, and is therefore also better suited for version control integration.

## Saving a model as TMDL in Tabular Editor 3

**File > Save to Folder...** saves the model as a TMDL folder when **Save to Folder format** under **Tools > Preferences > File Formats > Save-to-folder** is **TMDL**, the default. The TMDL formatting settings, such as indentation, encoding and casing, are under **Tools > Preferences > File Formats > Save-to-folder > TMDL Serialization**. See [Preferences](xref:preferences#file-formats--save-to-folder--tmdl-serialization).

> [!NOTE]
> A model loaded from a Database.json folder is saved in that format when you use **File > Save** (**Ctrl+S**). Use **File > Save to Folder...** with **Save to Folder format** set to **TMDL** to convert it to TMDL.

In Tabular Editor 3 Enterprise Edition, a TMDL folder can store each column, measure, partition and hierarchy, and each function, shared expression, data source and relationship, in its own file. See @tmdl-per-object-serialization.

## New models

The **Default save format** setting under **Tools > Preferences > File Formats > General** controls how a new model is saved the first time. With **Always ask** (default), Tabular Editor asks you to choose between a Model.bim file and a folder in the Database.json or TMDL format. With **TMDL**, new models are saved as TMDL folders.

![New Model Tmdl](~/content/assets/images/new-model-tmdl.png)

## TMDL and Microsoft Fabric Git Integration

TMDL is fully compatible with Microsoft Fabric's Git integration feature. When you use the **Save with supporting files** option in Tabular Editor 3, the TMDL serialization format creates a folder structure that includes all necessary metadata files required by Fabric's Git integration.

The resulting folder structure includes:
- **.platform** file with metadata (display name, description, logical ID)
- **definition.pbism** file with semantic model settings
- **definition/** folder containing your TMDL model files

This combination allows you to commit your semantic models to Git repositories and synchronize them with Microsoft Fabric workspaces using Fabric's built-in Git integration capabilities. The human-readable nature of TMDL makes it particularly well-suited for code reviews and tracking changes in version control systems.

For detailed information on using this feature, see [Save with supporting files](xref:save-with-supporting-files).

# Next steps

- [TMDL overview (Microsoft Learn)](https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview).
- [Get started with TMDL (Microsoft Learn)](https://learn.microsoft.com/analysis-services/tmdl/tmdl-how-to)
