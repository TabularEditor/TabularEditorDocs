---
uid: supported-files
title: Supported file types
author: Morten Lønskov
updated: 2023-10-17
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Supported file types

Tabular Editor 3 uses a number of different file formats and document types, some of which are not used by Analysis Services or Power BI. This article provides an overview and a description of each of these file types.

![Supported File Types](~/images/file-types/te3-supported-file-types.png)

## Dataset file types

Tabular Editor supports four file types for semantic models, 

> [!NOTE]
> Since **Tabular Editor 3 Desktop Edition** is only intended to be used as an External Tool for Power BI Desktop, this edition does not allow loading and saving files. You may however still use Tabular Editor 2.x for this purpose. See <xref:editions> to learn more about the difference between the Tabular Editor 3 editions.

### [Tabular Model Files (.bim)](#tab/BIM)
A .bim file is a single file consisting of nested JSON. It is the original format for a semantic model that Microsoft supports. However, it has a large drawback: as it is a single large file, it is difficult to track changes and use good team development practices such as git source control.

![Supported File Types BIM](~/images/file-types/te3-supported-file-bim.png)

### [Power BI](#tab/PowerBI)

Tabular Editor can handle two types of Power BI files the Power BI Template file (.pbit) and the Power BI Project file (.pbip).

The main difference between the two, is that the **.pbip file contains model data**, where as the **.pbit file contains no data**. Both file types contain model **metadata** in the JSON-based [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) format, which can be loaded by Tabular Editor.

#### Power BI Project file (.pbip ) *in Preview*
A Power BI Project file (.pbip) is a new kind of Power BI file that is currently in preview mode. It lets you store both a model (.bim) file and a report file structure in one place. You can open and save .pbip files from Tabular Editor, as well as from Power BI Desktop.

#### Power BI Template file (.pbit)
> [!WARNING]
> Even though it is technically possible to load and save model metadata to and from a .pbit file, this approach is unsupported by Power BI Desktop. As such, there is always a risk of making changes to the .pbit file which would cause the file to become unloadable in Power BI Desktop, or cause stability issues once loaded. In this case, Microsoft support will be unable to assist you.

### [Tabular Model Folder (.json)](#tab/JSON)

Tabular Editor allows you to save your dataset objects as separate JSON files, which is a custom serialization format. This format preserves the structure and properties of your objects, such as tables, columns, measures, and relationships.This has been supported in Tabular Editor from the early days and is a proven, though by Microsoft unsupported, method for storing your dataset objects as individual files. Thereby enabling developers to track changes in source control and collaborate on building semantic models.
There is full compatibility between Tabular Editor 2 and 3 with regards to the the JSON file structure.

In order to save a semantic model to JSON you must use the 'Save to Folder' option when saving the first time. Subsequent saves to a model loaded from a JSON structured model maintains the setting. It is always possible to convert a model that is in JSON to a .bim file using 'File > Save As'


![Supported File Types JSON](~/images/file-types/te3-supported-file-json.png)

1. The overall model has a database json and each TOM headline has its own folder
2. In tables, each table exist in its own folder
3. An individual table as a TableName json file with folders for measures, columns and partitions
4. The measures on the table each have their own json file.

The depth of which json objects that will be created are handled by the serialization settings. 
For more information on Save to Folder and serialization settings please refer to: [Save to Folder](xref:save-to-folder)


### [TMDL](#tab/TMDL)

TMDL stands for Tabular Model Definition Language and it is a new format for defining and managing datasets in a human readable format using YAML like syntax. Microsoft introduced TMDL as a preview feature in April 2023, aiming to provide a unified and consistent way of working with datasets across different platforms and tools. TMDL is designed to support dataset source control, enabling users to track changes, collaborate, and automate workflows with semantic models. TMDL is still in preview mode, which means that it is not fully stable or supported and may have some limitations or issues. 
For further reading please see: [TMDL](@tmdl)


***
## Supporting files

Supporting files are files which are not used by Analysis Services or Power BI. Instead, these files all support different kinds of development workflow in Tabular Editor 3 and other tools.

All supporting files can be saved individually using either Ctrl+S or 'File > Save' while having the specific dialog box open and selected. 

### Diagram file (.te3diag)

A .te3diag file is a file format that stores the diagram of a model created with TE3. 

These file can be useful for documenting the model structure and logic for other developers who work on the same project. A .te3diag file can be saved in the same folder as the model file for easy access and reference.


### DAX files (.dax)

DAX queries are expressions that can be used to manipulate and analyze data in tabular models. A DAX file is a text file that contains one or more DAX queries. You can save a DAX file in Tabular Editor 3 and use it later to run the queries again. You can also open a DAX file in other tools that support DAX, such as [DAX Studio](https://daxstudio.org).

### C# Scripts (.csx)

Creating and editing C# Scripts is one of Tabular Editor's biggest productivity features.

These scripts can be saved as files with the .csc extension and loaded into Tabular Editor as well as saved as Macros. 

This way, scripts can be reused without having to write them from scratch every time. The [script library](xref:csharp-script-library) is a good place investigate and reuse various examples of scripts as they demonstrate different features and functionalities of C#. 

### DAX Scripts (.te3daxs)

These files are saved DAX scripts (not queries) which are used in Tabular Editor to manipulate many DAX objects at once. For example, modifying multiple measures in a semantic model.

### Vertipaq Analyzer Files (.vpax)
With Tabular Editor, you can export and import .vpax files using the Vertipaq Analyzer feature. A .vpax file is a compressed file that contains information about the size and structure of your semantic model, but not the actual data. 

You can use this file to analyze and optimize your model performance, without exposing sensitive data. For example, you can use the [DAX optimizer](https://www.daxoptimizer.com/) tool to get suggestions on how to improve your DAX formulas based on the .vpax file.

Unlike other supporting file types creating a .vpax file is done within Vertipaq Analyzer window using the 'Import' and 'Export' buttons. 

![VPAX](~/images/file-types/te3-supported-file-vpax.png)


For more documentation on Vertipaq Analyzer please see: [sqlbi Vertipaq Analyzer](https://www.sqlbi.com/tools/vertipaq-analyzer) and [sqlbi Docs: Vertipaq Analyzer](https://docs.sqlbi.com/vertipaq-analyzer/)