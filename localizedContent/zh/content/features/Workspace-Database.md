---
uid: workspace-databases
title: Workspace 数据库介绍
author: Morten Lønskov
updated: 2026-03-19
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

# Workspace 数据库介绍

Tabular Editor 3 支持在编辑从磁盘加载的模型元数据时，同时连接到部署在 Analysis Services 实例上的数据库。 We call this database the _workspace database_. Going forward, this is the recommended approach to tabular modeling within Tabular Editor.

This makes the development workflow a lot simpler, since you only need to hit Save (Ctrl+S) once, to simultaneously save your changes to the disk **and** update the metadata in the workspace database. This also has the advantage, that any error messages returned from Analysis Services, are immediately visible in Tabular Editor upon hitting Save. In a sense, this is similar to the way SSDT / Visual Studio or Power BI Desktop does, except that you are in control of when the workspace database is updated.

当你从 Model.bim 文件或文件夹结构加载模型时，会看到以下提示：

![image](~/content/assets/images/workspace-database-01.png)

- **Yes**: Model metadata is loaded from disk and then immediately deployed to an instance of Analysis Services. Tabular Editor will then connect to the newly deployed database. The next time the same model is loaded from disk, Tabular Editor will redeploy and connect to the database automatically.
- **否**：模型元数据会像往常一样从磁盘加载到 Tabular Editor 中，不会连接到 Analysis Services 实例。
- **否，不再询问**：与上述选项相同，但下次加载同一模型时，Tabular Editor 不会再次询问。

### 设置 Workspace 数据库

When you select the "Yes" option in the prompt shown above, you will be asked for a servername and (optional) credentials to an instance of Analysis Services. Hitting "OK" will show you a list of databases already on the instance. Tabular Editor assumes that you want to deploy a new database and provides a default name for the new database, based on your Windows username and the current date and time:

![image](~/content/assets/images/workspace-database-02.png)

如果要将现有数据库用作 Workspace 数据库，只需在列表中选择它即可。 **Warning: If you choose an existing database, it will be overwritten with the metadata of the model loaded from disk. For this reason it is not recommended to set up workspace databases on a production instance!**

### 用户选项文件（.tmuo）

为跟踪文件系统中每个模型的 Workspace 设置，Tabular Editor 3 引入了一种新的 .tmuo 文件类型（Tabular Model User Options 的缩写），该文件将与 Model.bim 或 Database.json 文件放在同一目录下。

.tmuo 文件只是一个包含以下内容的简单 JSON 文档：

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": "Data Provider=MSOLAP;Data Source=localhost",
  "WorkspaceDatabase": "AdventureWorks_WS_Feature123"
}
```

从磁盘加载模型元数据时，Tabular Editor 会在已加载模型文件所在的同一目录中查找 .tmuo 文件。 The name of the .tmuo file must follow the pattern:

```
<modelfilename>.<windowsusername>.tmuo
```

The reason that the file contains a username, is to prevent multiple developers from inadvertently overwriting each others workspace databases in parallel development workflows. 如果该文件存在，且文件中的 "UseWorkspace" 标志设置为 "true"，Tabular Editor 在从磁盘加载模型时将执行以下步骤：

1. 使用 .tmuo 文件中指定的服务器名称和数据库名称，将模型元数据部署到 Workspace 数据库（覆盖现有元数据）。
2. 以“工作区模式”连接到新部署的 Workspace 数据库。

在“工作区模式”下，每当你点击“保存”（Ctrl+S）时，Tabular Editor 都会同时将模型保存到磁盘并更新 Workspace 数据库。 This lets you rapidly test new code and see error messages provided by Analysis Services, without having to manually deploy the database or invoking File > Save As... 或 文件 > 保存到文件夹……当你希望将模型元数据持久化到磁盘时。

### 增量刷新表达式变更检测

打开包含 Workspace 数据库的模型时，Tabular Editor 会针对每个由 `BasicRefreshPolicy` 管理的表，将本地增量刷新 `Source Expression` 和 `Polling Expression` 与 Workspace 数据库中的对应表达式进行比较。

如果 Tabular Editor 检测到差异，它会提示你用本地版本覆盖 Workspace 数据库中的表达式。 This prevents accidental loss of expression changes, which is particularly important when collaborating via Git where multiple developers may modify these expressions independently.

> [!TIP]
> 如果你在团队协作中发现该提示频繁出现，请与团队成员协调，确保不要在不同分支中各自修改增量刷新表达式。
