---
uid: workspace-databases
title: Introducing Workspace Databases
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

## Introducing Workspace Databases

Tabular Editor 3.0 supports editing model metadata loaded from disk with a simultaneous connection to a database deployed to an instance of Analysis Services. 我们将该数据库称为 _工作区数据库_。 今后，这是在 Tabular Editor 中进行表格建模的推荐方式。

这会让开发流程简单得多，因为你只需按一次“保存” (Ctrl+S)，就能同时将更改保存到磁盘 **并** 更新工作区数据库中的元数据。 这也有一个优势：按下“保存”时，Analysis Services 返回的任何错误信息都会立即在 Tabular Editor 中可见。 在某种程度上，这与 SSDT/Visual Studio 或 Power BI Desktop 的工作方式类似，只是你可以决定何时更新工作区数据库。

When you load a model from a Model.bim file or folder structure, you will see the following prompt:

![image](https://user-images.githubusercontent.com/8976200/58166683-a65db180-7c8a-11e9-9df3-be9a716b3ad1.png)

- **是**：从磁盘加载模型元数据，然后立即部署到某个 Analysis Services 实例。 随后，Tabular Editor 将连接到新部署的数据库。 下次从磁盘加载同一模型时，Tabular Editor 会自动重新部署并连接到该数据库。
- **No**: Model metadata is loaded from disk into Tabular Editor as usual, without connecting to an instance of Analysis Services.
- **No, don't ask again**: Same as the option above, but Tabular Editor will not ask again the next time the same model is loaded.

### Setting up a Workspace Database

当在上面的提示中选择“是”选项时，系统将要求输入 Analysis Services 实例的服务器名称以及（可选的）凭据。 点击“确定”后，将显示该实例上已有的数据库列表。 Tabular Editor 会默认你要部署一个新数据库，并会根据你的 Windows 用户名以及当前日期和时间，为新数据库提供一个默认名称：

![image](https://user-images.githubusercontent.com/8976200/58179509-a10f5f80-7ca8-11e9-9764-4cb76b9d1a8b.png)

If you want to use and existing database as your workspace database, simply select it on the list. **警告：如果选择现有数据库，该数据库将被从磁盘加载的模型的元数据覆盖。 因此，不建议在生产实例上设置 workspace 数据库!**

### The User Options file (.tmuo)

To track the workspace settings for each model in your file system, Tabular Editor 3.0 introduces a new file of type .tmuo (short for Tabular Model User Options), which will be placed next to the Model.bim or Database.json file.

The .tmuo file is just a simple JSON document with the following content:

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": "Data Provider=MSOLAP;Data Source=localhost",
  "WorkspaceDatabase": "AdventureWorks_WS_Feature123"
}
```

When loading model metadata from disk, Tabular Editor looks for the presence of a .tmuo file within the same directory as the loaded model file. .tmuo 文件的名称必须遵循以下模式：

```
<modelfilename>.<windowsusername>.tmuo
```

文件中包含用户名，是为了避免在并行开发工作流中，多位开发者无意间互相覆盖对方的 Workspace 数据库。 If the file is present and the "UseWorkspace" flag in the file is set to "true", Tabular Editor will perform the following steps when loading a model from disk:

1. Deploy the model metadata to the workspace database (overwriting existing metadata), using the server- and database name specified in the .tmuo file.
2. Connect to the newly deployed database in "workspace mode".

When in "workspace mode", Tabular Editor simultaneously saves your model to disk and updates the workspace database, whenever you hit Save (ctrl+s). 这样，你就能快速测试新代码并查看 Analysis Services 提供的错误信息，而无需手动部署数据库或调用“文件 > 另存为……” or File > Save to Folder... whenever you want to persist model metadata to disk.

### Incremental Refresh Expression Change Detection

When opening a model with a workspace database, Tabular Editor compares the local incremental refresh `Source Expression` and `Polling Expression` with those on the workspace database, for each table governed by a `BasicRefreshPolicy`.

If Tabular Editor detects differences, it prompts you to overwrite the workspace database expressions with your local version. 这可以防止表达式修改被意外丢失——在通过 Git 协作时尤为重要，因为多个开发者可能会分别独立修改这些表达式。

> [!TIP]
> If you are working in a team and notice the prompt appearing frequently, coordinate with your team members to ensure incremental refresh expressions are not modified independently in different branches.
