---
uid: supported-files
title: Supported file types
author: Morten Lønskov
updated: 2023-10-17
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "Desktop Edition does not support model metadata files"
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Supported file types

Tabular Editor 3 uses a number of different file formats and document types, some of which are not used by Analysis Services or Power BI. This article provides an overview and a description of each of these file types.

![Supported File Types](~/content/assets/images/file-types/te3-supported-file-types.png)

Example files are available for each several file type, based on the [learn.tabulareditor.com](https://tabulareditor.com/learn) course 2 Business Case.

## Dataset file types

Tabular Editor supports four file types for semantic models: .bim, Power BI files (.pbit and.pbip), .json and .tmdl. Each file type has different features and limitations, which are explained below.

> [!NOTE]
> Since **Tabular Editor 3 Desktop Edition** is only intended to be used as an External Tool for Power BI Desktop, this edition does not allow loading and saving semantic model files. You may however still use Tabular Editor 2.x for this purpose. See <xref:editions> to learn more about the difference between the Tabular Editor 3 editions.

### [Tabular Model Files (.bim)](#tab/BIM)
A .bim file is a single file consisting of nested JSON that is known as TMSL. 

It's the original format for a semantic model that Microsoft supports. 

However, it has a large drawback: as it's a single large file, it's difficult to track changes and use good team development practices such as git source control.

#### .bim file in a folder
![Supported File Types BIM](~/content/assets/images/file-types/te3-supported-file-bim.png)

[Download example .bim file ](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/bim-file-example.bim)


### [Power BI](#tab/PowerBI)

Tabular Editor can handle two types of Power BI storage formats:

- Power BI Template files (.pbit)
- Power BI Project folders (.pbip)



#### Power BI Project folders (.pbip ) *(Preview)*
Power BI Project folders were introduced in June 2023 and is available in Power BI Desktop as a preview feature (also known as "Developer Mode"). The storage format is an alternative way to store the contents of a .pbix file, in a format that is more friendly to version control and 3rd party reading/editing of the content.

> [!WARNING]
> Just like a .pbix file, a Power BI Project folder may contain model **data** in addition to **metadata**, so the folder should be treated as sensitive in the same way as a .pbix file should be.

At the root of the Power BI Project folders sits a .pbip file. The file is essentially a pointer to a Power BI report definition file, which may then in turn point to a Power BI dataset, either locally in the same folder structure (stored as a model.bim file), or a dataset published to the Power BI service (in this case, the report is said to be in *Live connect* mode). If a dataset (model.bim file) is present in the Power BI Project folder, Tabular Editor will be able to load this model metadata when opening the .pbip file.

To learn more about Power BI Project folders, please read [this official blog post from Microsoft](https://powerbi.microsoft.com/en-us/blog/deep-dive-into-power-bi-desktop-developer-mode-preview/).

> [!IMPORTANT]
> Power BI Project file is the recommended format when using Power BI with Tabular Editor, as it supports the [widest range of modeling operations](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview#model-authoring). Making other types of changes to the model metadata than those listed, may cause your model to become unloadable in Power BI Desktop, and in this case, Microsoft Support will not be able to help you.

#### Power BI Template file (.pbit)
Power BI Template files are similar to .pbix files, with the exception that they do not contain any model **data** - only model **metadata**. As such, this model metadata can be opened and edited in Tabular Editor.

> [!WARNING]
> Even though it's technically possible to load and save model metadata to and from a .pbit file, this approach is unsupported by Power BI Desktop. Tabular Editor will show a warning and block changes by default. Use Power BI Project folders instead, if you intend to make changes to your Power BI model through Tabular Editor.

### [Tabular Model Folder (.json)](#tab/JSON)

Tabular Editor allows you to save your dataset objects as separate JSON files, which is a custom serialization format. 

This format preserves the structure and properties of your objects, such as tables, columns, measures, and relationships.

This format has been supported in Tabular Editor from the early days and is a proven, though by Microsoft unsupported, method for storing your dataset objects as individual files. Thereby enabling developers to track changes in source control and collaborate on building semantic models.

There is full compatibility between Tabular Editor 2 and 3 with regards to the the JSON file structure.

In order to save a semantic model to JSON you must use the 'Save to Folder' option when saving the first time. Subsequent saves to a model loaded from a JSON structured model maintains the setting. it's always possible to convert a model that is in JSON to a .bim file using 'File > Save As'


![Supported File Types JSON](~/content/assets/images/file-types/te3-supported-file-json.png)

1. The overall model has a database json and each TOM headline has its own folder
2. In tables, each table exist in its own folder
3. An individual table as a TableName json file with folders for measures, columns and partitions
4. The measures on the table each have their own json file.

The depth of which json objects that will be created are handled by the serialization settings. 

A single JSON file for a measure contains all the properties of that measure:
 
![Supported File Types JSON File](~/content/assets/images/file-types/te3-supported-file-json-measure.png)


For more information on Save to Folder and serialization settings please refer to: [Save to Folder](xref:save-to-folder)

[Download example JSON Folder Structure](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/json-model-example.zip)

### [TMDL](#tab/TMDL)

TMDL stands for Tabular Model Definition Language and it's a new format for defining and managing datasets in a human readable format using YAML like syntax. 

Microsoft introduced TMDL as a preview feature in April 2023, aiming to provide a unified and consistent way of working with datasets across different platforms and tools. 

TMDL is designed to support dataset source control, enabling users to track changes, collaborate, and automate workflows with semantic models. 
> [!Note]
> TMDL is in preview, which means that it's not fully stable and may have some limitations or issues. 

![Supported File Types TMDL](~/content/assets/images/file-types/te3-supported-file-tmdl.png)

1. The overall serialization is on the top object level from the TOM
2. Each table is a single file
3. The TMDL file consist of a YAML like indentation with each column and measure inside the file.

For further reading please see: [TMDL](xref:tmdl)

[Download example TMDL Folder Structure](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/tmdl-model-example.zip)

***

## Tabular Editor Supporting files

Supporting files are files which are not used by Analysis Services or Power BI. Instead, these files all support different kinds of development workflow in Tabular Editor 3 and other tools.

All supporting files can be saved individually using either Ctrl+S or 'File > Save' while having the corresponding document or window open and focused. 

### Diagram file (.te3diag)

A .te3diag file is a file format that stores the diagram of a model created with TE3. 

These file can be useful for documenting the model structure and logic for other developers who work on the same project. A .te3diag file can be saved in the same folder as the model file for easy access and reference.

Diagram files are actually JSON that is stored in a Tabular Editor 3 extension.

[Download example Diagram File](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/te3-diagram.te3diag)

### DAX query files (.dax or .msdax)

DAX queries are expressions that can be used to manipulate and analyze data in semantic models. A DAX file is a text file that contains one or more DAX queries. 

You can save a DAX file in Tabular Editor 3 and use it later to run the queries again. You can also open a DAX file in other tools that support DAX, such as [DAX Studio](https://daxstudio.org).

[Download example DAX File](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-query-example.dax)

These files can only be opened while Tabular Editor 3 is connected to an instance of Analysis Services or the Power BI / Fabric XMLA endpoint.

### Pivot Grid layouts (.te3pivot)

These files contain the layout of a Pivot Grid in Tabular Editor 3. They are simple JSON files specifying which fields (measures, columns, hierarchies) are displayed in the Pivot Grid, and how they are arranged.

These files can only be opened while Tabular Editor 3 is connected to an instance of Analysis Services or the Power BI / Fabric XMLA endpoint.

### DAX Scripts (.te3daxs)

These files are saved DAX scripts (not queries) which are used in Tabular Editor to manipulate many DAX objects at once. For example, modifying multiple measures in a semantic model.

### C# Scripts (.csx)

Creating and editing C# Scripts is one of Tabular Editor's biggest productivity features.

These scripts can be saved as files with the .csc extension and loaded into Tabular Editor as well as saved as Macros. A [MacroActions.json local setting file](xref:supported-files#macroactionsjson) is maintained by Tabular Editor.

This way, scripts can be reused without having to write them from scratch every time. The [script library](xref:csharp-script-library) is a good place investigate and reuse various examples of scripts as they demonstrate different features and functionalities of C#. 

[Download example C# Script File](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/create-sum-measures-csharp.csx)

### Vertipaq Analyzer Files (.vpax)

With Tabular Editor, you can export and import .vpax files using the Vertipaq Analyzer feature. A .vpax file is a compressed file that contains information about the size and structure of your semantic model, but not the actual data. 

You can use this file to analyze and optimize your model performance, without exposing sensitive data. For example, you can use the [DAX optimizer](https://www.daxoptimizer.com/) tool to get suggestions on how to improve your DAX formulas based on the .vpax file.

[Download example DAX Script File](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-script-example.te3daxs)

Unlike other supporting file types creating a .vpax file is done within the Vertipaq Analyzer window using the 'Import' and 'Export' buttons. 

![VPAX](~/content/assets/images/file-types/te3-supported-file-vpax.png)

[Download example VPAX file](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/vpaq-example.vpax)

> [!WARNING]
> If your model metadata is confidential, a .vpax file should also be considered confidential and only shared with that in mind. If you are concerned about protecting IP, Tabular Editor 3 has an option to obfuscate VPAX files.

#### Obfuscation

If you need to hand off the VPAX file to a 3rd party, such as a consultant or a tool vendor, you can obfuscate the file to hide the model metadata. This is done by selecting the 'Obfuscated Export...' option under the drop-down button next to the 'Export' button in the Vertipaq Analyzer window.

An obfuscated VPAX file uses the .ovpax file extension.

![Export obfuscated VPAX](~/content/assets/images/obfuscated-vpax.png)

For more documentation on Vertipaq Analyzer please see: [sqlbi Vertipaq Analyzer](https://www.sqlbi.com/tools/vertipaq-analyzer) and [sqlbi Docs: Vertipaq Analyzer](https://docs.sqlbi.com/vertipaq-analyzer/)

For more information about obfuscation of VPAX files, please see: [VPAX Obfuscator](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/)

## Local Setting Files

Tabular Editor maintains several local files in the "%localappdata%\TabularEditor3" folder. These files are functionally relevant for Tabular Editor 3 and are useful to know.

It can be helpful to share these files across a team so that all developers have the same Macros and BPA rules.

> [!TIP]
> A windows native way of syncing a version controlled file into the "%localappdata%\TabularEditor3" folder is to use [SymLink](https://www.howtogeek.com/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/).
>
> Store the required files in Git or OneDrive and create a Symlink to the "%localappdata%\TabularEditor3" folder, but be aware that this could end up with synchronization issues, if multiple users update the same file version.
> However, this is not supported by Tabular Editor directly, so implement it at your own discretion. 


### MacroActions.json
This file stores all the macros that you have created or imported. It can be useful to share this file with your colleagues or backup it in a version control system and can also be configured to sync with a remote repository that contains macros (See tip above).

This file contains the index of each macro that is used in the software. If you need to change the order or the name of any macro, you can edit this file manually with a text editor. However, be careful not to introduce any errors or inconsistencies in the file thereby corrupting so make sure to create a backup.

[Download example MacroActions File](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


### BPARules.json
The file contains the [Best Practice Analyzer rules](xref:using-bpa) and fix expressions. The only place to add and edit  fix expressions is inside this JSON file.
It is recommended to store the PBA rule file in version control, which also enables the possibility of running the BPA rules against the semantic model before deployment. 

You can download the official Microsoft BPA rules here: [PBA Rules](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json)

### RecentServers.json
Contains all the servers a user has been connected to. It can be advisable to edit it manually to 'forget' past servers no longer relevant.

### Layouts.json
The Layouts file is automatically generated by Tabular Editor when starting the application. It contains all information to how Tabular Editor 3's UI layout is configured.

> [!TIP]
> Deleting this file will reset Tabular Editor's layout. If the Tabular Editor layout does not behave as expected a good first step is to backup this file somewhere else, delete the original and restart Tabular Editor 3.
