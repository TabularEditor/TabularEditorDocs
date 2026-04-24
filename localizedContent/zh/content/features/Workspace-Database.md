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

## Workspace 数据库介绍

Tabular Editor 3 支持在编辑从磁盘加载的模型元数据时，同时连接到部署在 Analysis Services 实例上的数据库。 我们将该数据库称为 _工作区数据库_。 今后，这是在 Tabular Editor 中进行表格建模的推荐方式。

这会让开发流程简单得多，因为你只需按一次“保存” (Ctrl+S)，就能同时将更改保存到磁盘 **并** 更新工作区数据库中的元数据。 这也有一个优势：按下“保存”时，Analysis Services 返回的任何错误信息都会立即在 Tabular Editor 中可见。 在某种程度上，这与 SSDT/Visual Studio 或 Power BI Desktop 的工作方式类似，只是你可以决定何时更新工作区数据库。

当你从 Model.bim 文件或文件夹结构加载模型时，会看到以下提示：

![image](https://user-images.githubusercontent.com/8976200/58166683-a65db180-7c8a-11e9-9df3-be9a716b3ad1.png)

- **是**：从磁盘加载模型元数据，然后立即部署到某个 Analysis Services 实例。 随后，Tabular Editor 将连接到新部署的数据库。 下次从磁盘加载同一模型时，Tabular Editor 会自动重新部署并连接到该数据库。
- **否**：模型元数据会像往常一样从磁盘加载到 Tabular Editor 中，不会连接到 Analysis Services 实例。
- **否，不再询问**：与上述选项相同，但下次加载同一模型时，Tabular Editor 不会再次询问。

### 设置 Workspace 数据库

当在上面的提示中选择“是”选项时，系统将要求输入 Analysis Services 实例的服务器名称以及（可选的）凭据。 点击“确定”后，将显示该实例上已有的数据库列表。 Tabular Editor 会默认你要部署一个新数据库，并会根据你的 Windows 用户名以及当前日期和时间，为新数据库提供一个默认名称：

![image](https://user-images.githubusercontent.com/8976200/58179509-a10f5f80-7ca8-11e9-9764-4cb76b9d1a8b.png)

如果要将现有数据库用作 Workspace 数据库，只需在列表中选择它即可。 **警告：如果选择现有数据库，该数据库将被从磁盘加载的模型的元数据覆盖。 因此，不建议在生产实例上设置 workspace 数据库!**

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

从磁盘加载模型元数据时，Tabular Editor 会在已加载模型文件所在的同一目录中查找 .tmuo 文件。 .tmuo 文件的名称必须遵循以下模式：

```
<modelfilename>.<windowsusername>.tmuo
```

文件中包含用户名，是为了避免在并行开发工作流中，多位开发者无意间互相覆盖对方的 Workspace 数据库。 如果该文件存在，且文件中的 "UseWorkspace" 标志设置为 "true"，Tabular Editor 在从磁盘加载模型时将执行以下步骤：

1. 使用 .tmuo 文件中指定的服务器名称和数据库名称，将模型元数据部署到 Workspace 数据库（覆盖现有元数据）。
2. 以“工作区模式”连接到新部署的 Workspace 数据库。

在“工作区模式”下，每当你点击“保存”（Ctrl+S）时，Tabular Editor 都会同时将模型保存到磁盘并更新 Workspace 数据库。 这样，你就能快速测试新代码并查看 Analysis Services 提供的错误信息，而无需手动部署数据库或调用“文件 > 另存为……” 或 文件 > 保存到文件夹…… 当你希望将模型元数据持久化到磁盘时。

### 增量刷新表达式变更检测

打开包含 Workspace 数据库的模型时，Tabular Editor 会针对每个由 `BasicRefreshPolicy` 管理的表，将本地增量刷新 `Source Expression` 和 `Polling Expression` 与 Workspace 数据库中的对应表达式进行比较。

如果 Tabular Editor 检测到差异，它会提示你用本地版本覆盖 Workspace 数据库中的表达式。 这可以防止表达式修改被意外丢失——在通过 Git 协作时尤为重要，因为多个开发者可能会分别独立修改这些表达式。

> [!TIP]
> 如果你在团队协作中发现该提示频繁出现，请与团队成员协调，确保不要在不同分支中各自修改增量刷新表达式。
