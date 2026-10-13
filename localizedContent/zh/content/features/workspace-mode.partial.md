---
uid: workspace-mode
title: 工作区模式
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

## Workspace 工作区模式

In **workspace mode**, Tabular Editor 3 connects a model loaded from a file to a **workspace database**. Workspace mode is available when you create a new model or load the Model.bim or Database.json file of an existing model.

When you save (**Ctrl+S**), Tabular Editor writes the metadata changes to the file(s) on disk and synchronizes them to the workspace database.

Give each model developer their own workspace database, because a shared one causes conflicts between developers.

> [!WARNING]
> Don't enable Git integration on the Fabric workspace that hosts your Tabular Editor workspace databases. Tabular Editor changes the workspace database through the XMLA endpoint, and these changes cause Git conflicts with the connected branch.

> [!NOTE]
> For models at compatibility level 1200, 1400 or 1500, host the workspace database on a local instance of Analysis Services, such as the one included with [SQL Server Developer Edition 2019](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

## 创建新模型

When you create a new model in Tabular Editor, **Use workspace database** is selected by default:

![新模型](~/content/assets/images/new-model.png)

With the option selected, a prompt to connect to an instance of Analysis Services appears after you click **OK**. Tabular Editor deploys the workspace database to this instance.

> [!IMPORTANT]
> If you deploy your workspace database to the Power BI Service XMLA endpoint, select compatibility level **1706 (Power BI / Fabric)** in the dialog above.

After you enter the server details and, optionally, credentials, a list of the databases on the server appears. For a Power BI workspace, the list shows the semantic models deployed to the workspace:

![选择 Workspace 数据库](~/content/assets/images/select-workspace-database.png)

Tabular Editor suggests a unique name for the workspace database, based on your Windows user name and the current date and time, which you can change.

Click **OK** to create the model and deploy and connect the workspace database. Then press **Ctrl+S** to save the model as a Model.bim file, or select **File > Save to Folder...** to store the metadata in a version control system such as Git.

![保存新内容到文件夹](~/content/assets/images/save-new-to-folder.png)

You can now define data sources and add tables to the model. Every save updates both the workspace database and the file or folder you chose.

Tabular Editor stores the workspace database details for the model in a Tabular Model User Options (.tmuo) file next to the model metadata file. See @user-options.

## 打开 Model.bim 或 Database.json 文件

When you open an existing Model.bim or Database.json file, a prompt asks whether to connect a workspace database to it.

![连接到 Workspace 数据库](~/content/assets/images/connect-to-wsdb.png)

The options are:

- **Yes**: connect to an instance of Analysis Services and choose an existing workspace database or create one. Tabular Editor deploys the file's metadata to the selected workspace database, and connects to the same database the next time you load the file.
- **No**: load the metadata offline, with no connection to Analysis Services.
- **Don't ask again**: load offline, and don't show the prompt again for this file.
- **Cancel**: don't load the file.

Tabular Editor stores the choice, and the workspace server and database, in the [Tabular Model User Options (.tmuo) file](xref:user-options).

> [!WARNING]
> Tabular Editor 3 deploys the loaded model metadata to the workspace database you choose. Never use a production database as a workspace database. Use a separate Analysis Services instance or Power BI workspace for workspace databases.

## 工作区模式的优势

In workspace mode, Tabular Editor stays connected to an instance of Analysis Services, which enables the [connected features](xref:migrate-from-te2#connected-features) of Tabular Editor 3. Each save (**Ctrl+S**) also deploys your changes to the instance for testing. Opening a model directly from Analysis Services works the same way, except that workspace mode also saves the metadata to disk.

> [!NOTE]
> While a refresh operation is in progress, Tabular Editor can't synchronize the Analysis Services instance, because refresh operations block other write operations. Saving during a refresh still writes the model metadata to disk.

## 为模型禁用工作区模式

You can disable workspace mode for a model permanently or for the current session, and edit the model file offline.

### 永久禁用工作区模式

1. In File Explorer, locate the model's `.tmuo` file next to your `.bim`, `.tmdl` or `.json` file.

2. Delete the `.tmuo` file, or open it in a text editor and set:

   ```json
   {
     "UseWorkspaceDatabase": false
   }
   ```

3. Open the model from the `.bim`, `.tmdl` or `.json` file.

Tabular Editor loads the model offline from then on.

### 仅为当前会话禁用工作区模式

1. In the **Open Semantic Model** dialog, select **Load without workspace database**.

![不加载 Workspace 数据库](~/content/assets/images/load-without-wsdb.png)

The model loads offline for this session, and workspace mode is enabled again the next time you open it.
