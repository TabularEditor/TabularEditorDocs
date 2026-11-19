---
uid: getting-started-te2
title: Getting Started with Tabular Editor 2
author: Morten Lønskov
updated: 2026-11-19
description: Install Tabular Editor 2, the free open-source editor for Analysis Services and Power BI semantic models, then open, edit and deploy a model. Tabular Editor 3 is the commercial version, with a free 30-day trial.
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---
# Getting Started with Tabular Editor 2

Tabular Editor 2 is a free, open-source Windows application for editing Analysis Services and Power BI semantic models. This page covers installation, opening and editing a model, deployment, the command line and C# scripting.

[!include[te2-te3-note](../includes/te2-te3-note.partial.md)]

## Tools by task

Tabular Editor 2, Tabular Editor 3 and the [Tabular Editor CLI](xref:te-cli) cover different tasks:

| Task | Tool | Documentation |
|------|------|---------------|
| Edit model metadata in a free desktop application | Tabular Editor 2 | This page |
| Write DAX with auto-complete and step through it in a debugger | Tabular Editor 3 | @dax-debugger |
| Run DAX queries and preview table data | Tabular Editor 3 | @refresh-preview-query |
| Deploy from a CI/CD pipeline | Tabular Editor 2 or Tabular Editor CLI | @command-line-options, @te-cli-cicd |
| Run Best Practice Analyzer checks | All three | @best-practice-analyzer |
| Let an AI agent read, query and change the model open in a desktop application | Tabular Editor 3 | @mcp-server |
| Let an AI agent change model files or deployed models from a terminal | Tabular Editor CLI | @te-cli-skill |

## Installation

Download the .msi installer or the portable .zip file from the [release page](https://github.com/TabularEditor/TabularEditor/releases/latest). Run the .msi, or extract the .zip to a folder and run `TabularEditor.exe`.

The .msi registers Tabular Editor 2 as an [External Tool](xref:desktop-integration) in Power BI Desktop.

## Prerequisites

Tabular Editor 2 requires [.NET Framework 4.8](https://dotnet.microsoft.com/download/dotnet-framework/net48). The .msi installer stops if .NET Framework 4.8 is missing and links to the download.

> [!NOTE]
> Tabular Editor 2 uses the [Tabular Object Model](https://learn.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo) (TOM) to load and save metadata to and from Model.bim files or existing databases. The installer includes the [Analysis Services client libraries](https://learn.microsoft.com/analysis-services/client-libraries).

## System requirements

- **Operating system:** Windows version supported by .NET Framework 4.8
- **.NET Framework:** [4.8](https://dotnet.microsoft.com/download/dotnet-framework/net48)

## Open a model

Open a model from disk with **File > Open > From File...** (**Ctrl+O**). Supported formats are Model.bim files, folders saved with [Save to folder](xref:save-to-folder) (database.json), [TMDL](xref:tmdl) folders, .pbit files and .pbip projects.

Open a deployed database with **File > Open > From DB...** (**Ctrl+Shift+O**). The **Connect to Tabular Server** dialog asks for a server name and authentication:

![Connecting to an already deployed Tabular Model](~/content/assets/images/getting-started-te-01.png)

The server name accepts Analysis Services instances and Azure Analysis Services servers (`asazure://<servername>`). The **Local instance** dropdown lists running instances of Power BI Desktop, Visual Studio integrated workspaces and local Analysis Services. From the June 2025 Power BI Desktop update, external tools can change any part of a model hosted in Power BI Desktop. See @desktop-integration.

Select **OK**, then select a database from the list on the server.

## Edit the model

The main window looks like this after a model loads:

![The main UI of Tabular Editor](~/content/assets/images/getting-started-te-02.png)

The tree on the left lists all tables in the model. Expand a table to see its columns, measures and hierarchies, grouped by display folder. The buttons above the tree toggle display folders, hidden objects and object types, and the text box filters objects by name. Right-click in the tree for common actions such as adding measures, hiding, duplicating and deleting objects. Press **F2** to rename the selected object. When you select several objects, **F2** opens **Batch Rename**:

![Batch Renaming lets you rename multiple objects simultaneously](~/content/assets/images/getting-started-te-03.png)

The **Expression Editor** in the upper right edits the DAX expression of the selected measure or calculated column. **Format DAX** formats the expression through [DAX Formatter](https://www.daxformatter.com).

The property grid in the lower right shows and sets object properties such as `FormatString`, `Description`, translations and perspective membership. To change `DisplayFolder` for several objects at once, select them with **Ctrl** or **Shift** and drag them to a folder in the tree.

To edit perspectives or translations, select the **Model** object in the tree and select the ellipsis button next to the `Perspectives` or `Cultures` property. A collection editor opens for adding, removing and editing items:

![Editing perspectives - click the ellipsis button to the right](~/content/assets/images/getting-started-te-04.png)

Press **Ctrl+S** to save. A model opened from a file saves back to that file, and a model opened from a database saves back to the database. If someone changed the deployed database after you loaded it, a **Change conflict** prompt asks whether to overwrite it. Press **Ctrl+Z** to undo and **Ctrl+Y** to redo.

## Deployment

**Model > Deploy...** opens the deployment wizard, which deploys the loaded model to a server. After you select a server and a database, choose which parts of the model to deploy:

![Deployment Wizard](~/content/assets/images/getting-started-te-05.png)

| Option | When cleared |
|--------|--------------|
| **Deploy Data Sources** | Data sources on the target database stay as they are. The deployment fails if a table uses a data source that doesn't exist on the target. |
| **Deploy Table Partitions** | Partitions on the target stay as they are, and so does their data. |
| **Deploy partitions governed by Incremental Refresh Policies** | Partitions created by incremental refresh stay as they are. Requires **Deploy Table Partitions**. |
| **Deploy Shared Expressions** | Shared expressions on the target stay as they are. Requires compatibility level 1400 or higher. |
| **Deploy Roles** | Roles on the target stay as they are. |
| **Deploy Role Members** | Role members on the target stay as they are. Requires **Deploy Roles**. |

**Deploy Model Structure** is always selected when the target is an existing database. The other options are selected by default when the model contains that type of object, and **Deploy Roles** when the model contains role members. If the database doesn't exist yet, the wizard deploys data sources, partitions and shared expressions with the model, and only the role options apply. The summary page also has **Export Build...** to write deployment files for the Analysis Services Deployment Wizard and **TMSL Script** to show the deployment as a TMSL script.

## Command line

`TabularEditor.exe` runs deployments, scripts and Best Practice Analyzer checks from the command line. The following examples deploy a model:

`TabularEditor.exe c:\Projects\Model.bim`

Opens Tabular Editor 2 and loads the Model.bim file without deploying anything.

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

Creates the AdventureWorks database on the Analysis Services instance on localhost, without opening the user interface. If the database already exists, the deployment fails.

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks -O -P -R -M`

Overwrites the existing AdventureWorks database, including its partitions, roles and role members.

Add these switches after the database name to control what the deployment overwrites:

- `-O` overwrite an existing database
- `-C` overwrite data sources (**c**onnections)
- `-P` overwrite **p**artitions
- `-Y` skip partitions with incremental refresh policies (with `-P`)
- `-S` overwrite **s**hared expressions
- `-R` overwrite **r**oles
- `-M` overwrite role **m**embers (with `-R`)

Without these switches, data sources, partitions, shared expressions and roles on the target stay as they are. @command-line-options lists every switch, including scripts, Best Practice Analyzer checks and output for Azure DevOps and GitHub Actions.

> [!NOTE]
> `TabularEditor.exe` is a Windows Forms application, so a command-line call returns before the deployment finishes. In a batch job that waits for the deployment, use `start /wait`:
>
> `start /wait TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

The [Tabular Editor CLI](xref:te-cli) runs on Windows, macOS and Linux and accepts most `TabularEditor.exe` switches. See @te-cli-migrate.

## C# scripting

The **C# Script** tab runs C# code against the loaded model. Use it to apply the same change to many objects at once. Scripts have access to two objects:

- `Selected` holds the objects selected in the tree.
- `Model` holds the entire Tabular Object Model.

The script editor has basic IntelliSense:

![IntelliSense helps you create scripts for Tabular Editor](~/content/assets/images/getting-started-te-06.png)

Tabular Editor 2 calls this feature Advanced Scripting. See @advanced-scripting for the scripting API and examples.

## Feature comparison

The table compares Tabular Editor 2, Tabular Editor 3 and the Tabular Editor CLI:

[!include[feature-comparison](../includes/feature-comparison.partial.md)]

## Next steps

- @migrate-from-te2 describes the feature differences between Tabular Editor 2 and Tabular Editor 3.
- @getting-started covers installing Tabular Editor 3 and starting the free trial.
- @te-cli-skill installs a skill that teaches AI coding agents the Tabular Editor CLI commands.
