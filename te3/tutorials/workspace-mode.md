---
uid: workspace-mode
title: (Walkthrough) Workspace Mode
author: Daniel Otykier
updated: 2021-09-06
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
    - edition: Enterprise
---
# (Walkthrough) Workspace Mode

Tabular Editor 3 introduces the concept of **workspace mode** when creating a new model inside the tool, or when loading a Model.bim or Database.json file of an existing model.

Using workspace mode, Tabular Editor will synchronize your model metadata changes to a **workspace database**, whenever you hit Save (Ctrl+S), while also saving the metadata changes to the file(s) on disk.

Ideally, each model developer should use their own workspace database to avoid conflicts while developing.

> [!NOTE]
> We recommend using a local instance of Analysis Services to host the workspace database, such as the one included with [SQL Server Developer Edition 2019](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

## Creating a new model

When you create a new model in Tabular Editor, the "Use workspace database" option is checked by default:

![New Model](~/images/new-model.png)

Leaving this checked, you will be prompted to connect to an instance of Analysis Services after hitting "OK". This is the instance of Analysis Services to which your workspace database will be deployed.

> [!IMPORTANT]
> If you plan to deploy your workspace database to the Power BI Service XMLA endpoint, make sure you choose Compatibility Level 1560 (Power BI Dataset) in the dialog above.

After entering the Analysis Services server details and (optional) credentials, you are shown a list of all databases currently reciding on the server (or for a Power BI workspace, the list of datasets deployed to the workspace):

![Select Workspace Database](~/images/select-workspace-database.png)

Tabular Editor suggests a new unique name for your workspace database, based on your Windows user name and the current date and time, but you are free to change this to a more meaningful name.

After hitting OK, your new model is created and the workspace database is deployed and connected. At this point, hit save (Ctrl+S) to save your model as a Model.bim file. You may also choose the File > Save to Folder... menu item if you intend to store the model metadata in a version control system such as Git.

![Save New To Folder](~/images/save-new-to-folder.png)

At this point, you are ready to define data sources and add new tables to your model. Every time you subsequently hit Save (Ctrl+S), the workspace database is updated with the changes, and the file/folder you chose previously will be updated as well.

Information about the workspace database tied to this model is stored in a Tabular Model User Options (.tmuo) file next to the model metadata file. See @user-options for more information.

## Opening a Model.bim or Database.json file

If you open an existing Model.bim or Database.json file, Tabular Editor 3 will prompt you whether you want to initiate a workspace database for that file.

![Connect To Workspace database](~/images/connect-to-wsdb.png)

Your options are:

- **Yes**: Connect to an instance of Analysis Services and choose an existing workspace database or create a new one. The next time you load the same Model.bim or Database.json file, Tabular Editor will connect to the same workspace database.
- **No**: Tabular Editor will load the metadata in the file offline with no connectivity to Analysis Services.
- **Don't ask again**: Same as above, but Tabular Editor will no longer ask you to connect to a workspace database the next time you open the same Model.bim or Database.json file.
- **Cancel**: The file is not loaded at all.

Information about whether to connect to a workspace database for a given model, and which workspace server and database to use is stored in the [Tabular Model User Options (.tmuo) file](xref:user-options).