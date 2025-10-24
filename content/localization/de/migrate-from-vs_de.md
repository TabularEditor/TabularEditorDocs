---
uid: migrate-from-vs
title: Migrating from Visual Studio
author: Daniel Otykier
updated: 2021-09-30
---

# Migrating from Visual Studio / SQL Server Data Tools

This article assumes that you are familiar with Tabular model development using [Analysis Services Projects for Visual Studio](https://marketplace.visualstudio.com/items?itemName=ProBITools.MicrosoftAnalysisServicesModelingProjects) (formerly known as SQL Server Data Tools). This is common among developers using SQL Server Analysis Services (Tabular) or Azure Analysis Services.

- If you have never used Visual Studio for Tabular model development, you can safely skip this topic.
- If you previously used Tabular Editor 2.x for Tabular model development, we recommend you skip directly to the @migrate-from-te2 article.

## Partial migration

Tabular Editor 3 contains features that allow you to completely migrate away from Visual Studio for tabular model development. This is in contrast to Tabular Editor 2.x, where some users still preferred using Visual Studio for things like table import, visualization of relationships and preview of data.

However, as you familiarize yourself with Tabular Editor 3, you might still find it useful to open your tabular models in Visual Studio from time to time. This is possible at any time, since Tabular Editor 3 does not modify the **Model.bim** file format (aka. the [TOM JSON](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)) used by Visual Studio, thus ensuring compatibility with Visual Studio.

The only exception is, if you decide to use Tabular Editor's [Save-to-folder](xref:parallel-development#what-is-save-to-folder) feature, as this file format is not supported by Visual Studio. However, you can easily recreate a Model.bim file for use with Visual Studio, using the **File > Save As...** option in Tabular Editor. The opposite conversion can also be performed by loading a Model.bim file in Tabular Editor and then using the **File > Save to Folder...** option.

### Automating file format conversion

If you often face the need to convert back and forth between Tabular Editor's (database.json) folder-based format and Visual Studio's (model.bim) file format, consider writing a small Windows command script using [Tabular Editor 2.x CLI](xref:command-line-options) to automate the conversion process.

# [Model.bim to folder](#tab/frombim)

To convert from model.bim to database.json (folder-based format):

```cmd
tabulareditor.exe model.bim -F database.json
```

# [Folder to model.bim](#tab/fromfolder)

To convert from database.json (folder-based format) to model.bim:

```cmd
tabulareditor.exe database.json -B model.bim
```

***

> [!NOTE]
> The command line script above assumes you have [Tabular Editor 2.x](xref:getting-started-te2) installed. The installation location of Tabular Editor 2.x should also be specified as part of your [PATH environment variable](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/path).

## Integrated Workspace server

When starting a new Analysis Services (Tabular) project in Visual Studio, you are prompted to choose if you want to use Visual Studio's Integrated workspace server or provide your own instance of Analysis Services. In addition, you must decide the compatibility level of the tabular model (see screenshot below).

![VS New Project](~/content/assets/images/vs-new-project.png)

In contrast, when creating a new model in Tabular Editor, using a workspace server is completely optional (but recommended - see [workspace mode](xref:workspace-mode)).

Below is the dialog box shown when creating a new model in Tabular Editor 3:

![New model dialog](~/content/assets/images/new-model.png)

If you enable the **Use workspace database** option, Tabular Editor will prompt you for an Analysis Services instance and database name that will be used as as workspace database while working on the model. If you do not enable this option, you will be able to create and work on your model in "offline" mode, which still allows you to add tables, relationships, author DAX expressions, etc. However, you will have to deploy your offline model to an instance of Analysis Services before you can refresh, preview and query the data in the model.

> [!IMPORTANT]
> Tabular Editor 3 does not provide a feature equivalent to the **Integrated workspace** option of Visual Studio. Essentially, the integrated workspace is an Analysis Services instance managed by Visual Studio. Since Analysis Services is proprietary software from Microsoft, we cannot ship it alongside Tabular Editor 3. Instead, if you would like to run a local instance of Analysis Services for use with Tabular Editor, we recommend that you install [SQL Server Developer Edition](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

### Compatibility level requirements

Tabular Editor lets you choose the following compatibility levels for creating Analysis Services databases:

- 1200 (Azure Analysis Services / SQL Server 2016+)
- 1400 (Azure Analysis Services / SQL Server 2017+)
- 1500 (Azure Analysis Services / SQL Server 2019+)

In addition, Tabular Editor lets you choose compatibility levels suitable for Power BI datasets that will be deployed to the Power BI service through the [XMLA endpoint](xref:powerbi-xmla).

> [!NOTE]
> Tabular Editor does not support compatibility levels below 1200, as these do not use the [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) metadata format. If you plan on migrating development from Visual Studio to Tabular Editor for a model in compatibility level 1100 or 1103, **you must upgrade the compatibility level to at least 1200** before migrating to Tabular Editor. By doing so, you will no longer be able to deploy the model to SQL Server 2014 Analysis Services.

## Visual Studio projects

When creating an Analysis Services (Tabular) project in Visual Studio, a number of files are created in the project folder next to the Model.bim file. These files contain project- and user-specific information which is not related to the Tabular Object Model (TOM). The screenshot below shows the files resulting from creating a new tabular project in Visual Studio.

![VS Project File Structure](~/content/assets/images/vs-file-structure.png)

When migrating to Tabular Editor, you only need to bring the Model.bim file, as the concept of "project" does not exist here. Instead, Tabular Editor simply loads the model metadata directly from the Model.bim file. In some cases, a file called the [Tabular Model User Options (tmuo) file](xref:user-options) is created next to the Model.bim file. This file is used by Tabular Editor to store user- and model specific settings, such as whether or not to use a workspace database, (encrypted) user credentials for data sources, etc.

To keep the "project" directory clean, we therefore recommend to copy the Model.bim file created by Visual Studio into a new directory, before loading the file in Tabular Editor.

![Te File Structure](~/content/assets/images/te-file-structure.png)

If you want to use the [Save-to-folder](xref:parallel-development#what-is-save-to-folder) feature, which is recommended for parallel development and integration with version control systems, now is the time to save the model as a folder from within Tabular Editor (**File > Save To Folder...**).

![Te Folder Structure](~/content/assets/images/te-folder-structure.png)

## Version control

Tabular Editor does not have any integrated version control of model metadata. However, since all model metadata is stored as simple text (JSON) files on the disk, it is straightforward to include the tabular model metadata in any type of version control system. For this reason, most Tabular Editor users prefer to still keep Visual Studio installed, in order to have access to the [Visual Studio Team Explorer](https://docs.microsoft.com/en-us/azure/devops/user-guide/work-team-explorer?view=azure-devops) or, specifically for git, the new [Git Changes window](https://docs.microsoft.com/en-us/visualstudio/version-control/git-with-visual-studio?view=vs-2019) of Visual Studio 2019.

> [!NOTE]
> These days, it seems that [git](https://git-scm.com/) is the preferred version control system by most developers. Git integration in Tabular Editor 3 is planned for a future update.

Once you migrate to Tabular Editor, you do not need to keep the original Tabular model project and supporting files created by Visual Studio. You can still use the Visual Studio Team Explorer or Git Changes window to look at code changes, manage version control branches, perform code check-ins, merges, etc.

Of course, most version control systems also have their own set of tools that you can use without relying on Visual Studio. For example, git has its command line and many popular tools that integrate directly with the Windows Explorer, such as [TortoiseGit](https://tortoisegit.org/).

### Save-to-folder and version control

The main advantage of using the [Save-to-folder](xref:parallel-development#what-is-save-to-folder) option, is that the model metadata is broken out into multiple small files, instead of storing everything in a large JSON document. Many properties in the TOM are arrays of objects (for example tables, measures and columns). Since all such objects have explicit names, their order in the array does not matter. Sometimes it happens that the order is changed during serialization to JSON, and this causes most version control system to indicate that a change was made to the file. However, since this ordering does not have any semantic meaning, we should not bother handling merge conflicts that may arise from this type of change.

With Save-to-folder serialization, the number of arrays used in the JSON files are greatly reduced, as objects that would otherwise be stored as arrays, are now broken out into individual files stored within a subfolder. When Tabular Editor loads the model metadata from disk, it traverses all these subfolders to ensure all objects are deserialized correctly into the TOM.

As such, Save-to-folder serialization greatly reduces the chance that merge conflicts are ever encountered, when two or more developers make parallel changes to the same tabular model.

## UI differences

This section lists the most important differences between the user interfaces of Tabular Editor 3 and Visual Studio for tabular model development. If you are an avid Visual Studio user, you should feel quite comfortable with Tabular Editor 3's user interface. If you would like a more detailed walkthrough, please see <xref:user-interface>.

### Tabular Model Explorer vs. TOM Explorer

In Visual Studio, a hierarchical overview of the model metadata can be found in the **Tabular Model Explorer**.

![Vs Tom Explorer](~/content/assets/images/vs-tom-explorer.png)

In Tabular Editor, this is called the **TOM Explorer** view. In Tabular Editor, all data modeling generally revolves around locating the relevant objects in the TOM Explorer and then performing certain actions by invoking the right-click context menu, by navigating to the main menu, or by editing object properties in the **Properties** view. In Tabular Editor, you can use intuitive operations such as multi-select, drag-drop, copy-paste and undo-redo for all data modeling operations.

![Vs Tom Explorer](~/content/assets/images/tom-explorer.png)

The TOM Explorer in Tabular Editor also has shortcut options for showing/hiding certain types of objects, hidden objects, display folders, and for quickly searching and filtering the metadata hierarchy.

See @tom-explorer-view for more information.

### Property Grid

Both Visual Studio and Tabular Editor include a property grid that allows you to edit most object properties of whatever object is currently selected. Below is a comparison between the Visual Studio property grid (left) and the Tabular Editor property grid (right) for the same measure:

![Property grid in Visual Studio and Tabular Editor](~/content/assets/images/property-grid-vs-te.png)

The two generally work the same way, except that Tabular Editor uses property names that are closely aligned with the TOM object properties. Tabular Editor also adds a number of properties that are not found in the TOM, to make certain modeling operations easier. For example, by expanding the **Translated Names** property, you can compare and edit object name translations across all model cultures.

### Editing DAX expressions

In Visual Studio, you can use the formula bar or open a DAX editor window by right-clicking on a measure in the Tabular Model Explorer and choosing "Edit formula".

Tabular Editor works quite similar, with the formula bar being replaced by the **Expression Editor** view. In addition, if you want to edit the DAX expressions for one or more objects in a standalone document, you can right-click on those objects (measures, calculated columns, calculated tables), and choose **Script DAX**.

The DAX code editor in Tabular Editor 3 is one of the main reasons for using the tool. You can read more about it [here](xref:dax-editor).

### Error List vs. Messages View

In Visual Studio, DAX syntax errors are shown as warnings within the **Error List** (see screenshot below). In addition, measures that have errors are indicated with a warning triangle in the measures grid.

![Vs Error List](~/content/assets/images/vs-error-list.png)

In Tabular Editor, we use the Messages View to consolidate all error, warning and informational messages posted by different sources during model development. Specifically for DAX syntax errors, these are shown as errors in the Messages View, and any measures that have an error are indicated with a red dot in the TOM Explorer (see screenshot below).

![Te Messages](~/content/assets/images/te-messages.png)

In the screenshot above, notice how there are three different message-posting sources:

- **Analysis Services**: When metadata changes are saved to a connected instance of Analysis Services, the server updates the TOM metadata to indicate if any objects are in an erroneous state. Specifically, the [State](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure.state?view=analysisservices-dotnet#Microsoft_AnalysisServices_Tabular_Measure_State) and [ErrorMessage](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure.errormessage?view=analysisservices-dotnet#Microsoft_AnalysisServices_Tabular_Measure_ErrorMessage) properties are updated. Tabular Editor displays these error messages in the Messages View. These messages are not shown when Tabular Editor is used offline (i.e. without a connection to Analysis Services).
- **Tabular Editor Semantic Analysis**: In addition, Tabular Editor 3 performs its own semantic analysis of all DAX expressions in the model. Any syntax or semantic errors encountered are reported here.
- **Expression Editor**: Lastly, if any documents are open in Tabular Editor 3, such as the Expression Editor, any DAX syntax or semantic errors encountered in the document are reported here.

### Previewing table data

In Visual Studio, tables and their content are displayed in a tabbed view once you load the Model.bim file. In Tabular Editor 3, you can preview table data by right-clicking on a table in the TOM Explorer, and chooseing **Preview Data**. This opens a new document tab that lets you scroll through all rows of the table, as well as filter and sort the columns. It even works for model using DirectQuery!

Also, you can freely rearrange the documents, to view the content of several tables at once (see screenshot below).

![Te3 Table Preview](~/content/assets/images/te3-table-preview.png)

### Importing tables

To import new tables with Tabular Editor 3, use the **Model > Import tables...** option. This launches Tabular Editor 3's Import Table Wizard, which guides you through the process of connecting to a data source and selecting tables to import. The process is relatively similar to the legacy table import in Visual Studio.

One important difference is that Tabular Editor 3 does not include a visual Power Query Editor. You can still edit Power Query (M) expressions as text, but if your model relies heavily on complex data transformation expressed as Power Query queries, you should consider to keep using Visual Studio for purposes of editing the Power Query queries.

> [!NOTE]
> Performing complex data transformations using Power Query is generally not recommended for enterprise data modeling, due to the increased overhead of data refresh operations. Instead, prepare your data into a star schema using other ETL tools, and store the star schema data in a relational database, such as SQL Server or Azure SQL Database. Then, import tables to your tabular model from that database.

#### Editing partitions and updating table schema

In Tabular Editor 3, you can update the schema of a table without forcing a table refresh. Partitions are displayed in the TOM Explorer as individual objects. Click on a partition to edit its expression (M or SQL) in the Expression Editor.

Once a partition expression has been updated, Tabular Editor can automatically detect if the table schema resulting from the updated expression, is different from the set of columns defined in the model. To perform a schema update, right-click on the partition or table in the TOM Explorer and choose **Update table schema...**.

For more information about table import and schema updates, see @importing-tables.

### Visualizing relationships

Visual Studio includes a diagram tool that lets you visualize and create relationships between tables.

Tabular Editor 3 also includes a diagram tool, that can be accessed using **File > New > Diagram**. A new diagram document tab will be created, at which point you can add tables from the TOM Explorer by dragging and dropping, or from the **Diagram > Add tables...** menu.

Once tables have been added to the diagram, you can create relationship between columns simply by dragging from one column to another.

![Te3 Diagram View](~/content/assets/images/te3-diagram-view.png)

> [!NOTE]
> For performance reasons, the diagram tool does not inspect the data of the model, nor does it validate the uniqueness or directionality of any relationships you create. It is up to you to ensure that relationships are created correctly. If a relationship has been incorrectly defined, Analysis Services will return an error state which is shown in the **Messages View**.

### Model deployment

Tabular Editor lets you easily deploy the model metadata to any instance of Analysis Services. You can invoke Tabular Editor's Deployment Wizard under **Model > Deploy...** or by hitting CTRL+SHIFT+D.

For more information, see <xref:deployment>.

## Next steps

- @migrate-from-te2
- @parallel-development
- @boosting-productivity-te3