---
uid: save-with-supporting-files
title: 保存并包含支持文件
author: Peer Grønnerup
updated: 2026-09-11
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

# 保存并包含支持文件

“保存并包含支持文件”是一项功能，可在保存语义模型时同时保存额外的支持文件，这些文件遵循 Microsoft Fabric 的 Git 集成所要求的源代码格式。 This feature ensures that your Tabular Editor models are fully compatible with Fabric's Git integration capabilities, allowing seamless version control and deployment workflows.

当你保存语义模型并包含支持文件时，Tabular Editor 会在保存路径中创建一个文件夹结构，其中包含 Microsoft Fabric 的 Git 集成所需的全部元数据文件。 This allows you to use Fabric Git integration to synchronize your semantic models between Fabric workspaces and Git repositories.

> [!NOTE]
> “保存并包含支持文件”仅在保存为 .bim (TMSL) 时可用，或在将“保存到文件夹”的序列化模式设置为 TMDL 时可用。

## 文件结构和模型属性

当你保存并包含支持文件时，Tabular Editor 会在保存路径中按以下命名约定创建一个新文件夹：**Database Name.SemanticModel**。 The folder name is derived from the `Name` property of the Database object in the TOM Explorer, with the **.SemanticModel** suffix appended. This suffix is required by Microsoft Fabric to recognize the folder as a semantic model item.

Database 的 `Name` 属性也会同步到 .platform 元数据文件中的 `displayName` 属性，该属性由 Microsoft Fabric 使用。

> [!TIP]
> TOM Explorer 中 Database 对象的 `Name` 属性有两个用途：
>
> 1. 决定文件夹名称（附加 .SemanticModel 后缀）
> 2. 设置 .platform 元数据文件中的 displayName
>
> `Description` 属性也会同步到 .platform 元数据文件。

<a name="power-bi-desktop-authored-pbip-projects"></a>

### Power BI Desktop authored PBIP projects

The rules above describe a model whose metadata carries a name and a description. A [Power BI Project (PBIP)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview) semantic model authored by Power BI Desktop carries neither: in those projects the item name and description live only in the `.platform` file.

Tabular Editor leaves the existing `displayName` and `description` in `.platform` as they are and names a new folder after the item, instead of creating a folder called `.SemanticModel`

> [!IMPORTANT]
> Tabular Editor versions before 3.27.0 renamed the item and cleared its description in the Fabric workspace on the next Git sync.

To let Tabular Editor control the name and the description of the item, set the `Name` and `Description` properties on the Database object as described above. Once the metadata carries them, Tabular Editor synchronizes them to `.platform` on every save.

### 包含的文件

每个已保存的模型都包含以下核心文件：

- **.platform** - Metadata about the item including its type, display name, and description. Also contains a logicalId property, an automatically generated cross-workspace identifier.
- **definition.pbism** - 语义模型的整体定义和核心设置。

在创建的文件夹中，模型的文件结构取决于所选的序列化格式：

| 格式                                                 | 模型存储                                  |
| -------------------------------------------------- | ------------------------------------- |
| **TMDL**                                           | `definition` 文件夹，里面包含带有模型元数据的 TMDL 文件 |
| **TMSL (.bim)** | `model.bim` 文件（自动保存，文件名固定）            |

名为“Sales”的数据库文件夹结构示例如下：

```
Sales.SemanticModel/
├── .platform
├── definition.pbism
├── model.bim                    (if saved as TMSL)
└── definition/                  (if saved as TMDL)
    ├── database.tmdl
    ├── tables.tmdl
    └── ...
```

## 如何连同支持文件一起保存

要将模型连同支持文件一起保存：

1. 在 Tabular Editor 3 中新建或打开现有语义模型
2. **配置模型名称** - 在 TOM Explorer 中设置 Database 对象的 `Name` 属性
   - 这会设置文件夹名称（带 .SemanticModel 后缀）以及 .platform 文件中的 displayName  
     ![设置 Database Name 属性](~/content/assets/images/common/SaveWithSupportingFilesSetName.png)
3. 确保序列化模式设置为 TMDL，或者将模型保存为 .bim 文件
   - 前往 **工具 > 偏好 > 文件格式**，配置序列化设置
4. 点击 **文件 > 另存为** 或 **文件 > 保存到文件夹**
5. 选择要保存模型的文件夹
   - 勾选 **与支持文件一起保存** 复选框
     ![与支持文件一起保存对话框](~/content/assets/images/common/SaveWithSupportingFilesDialog.png)
6. 点击 **保存**

Tabular Editor 会在保存位置以 Database 名称创建一个带 **.SemanticModel** 后缀的新文件夹（例如 `Sales.SemanticModel`），并以与 Microsoft Fabric Git 集成兼容的格式将所有必需文件写入其中。

## Microsoft Fabric 中的 Git 集成

**“保存并包含支持文件”** 功能旨在与 Microsoft Fabric 的 Git 集成功能无缝协同工作。 Git Integration is available on workspaces assigned to Microsoft Fabric F-SKU capacity, Power BI Premium capacity, or Power BI Premium Per User (PPU).

> [!WARNING]
> Git Integration for the Semantic Model item is currently in preview. 有关 Fabric Git 集成支持项的最新信息，可以查看 [Fabric Git 集成中支持的项](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration#supported-items)。

> [!CAUTION]
> 不要在用于托管 Tabular Editor 工作区数据库的 Fabric Workspace 上启用 Git 集成。
> Maintaining semantic models in both the hosted workspace and in repository files simultaneously while Git integration is enabled creates risks of uncommitted changes and conflicts. When a model is synchronized between Tabular Editor and the workspace, changes may not align properly with the Git repository state, resulting in out-of-sync uncommitted changes and potential Git conflicts.
>
> 你可以改用部署工作流，通过 Tabular Editor、Fabric REST API、Fabric CLI 或 fabric-cicd Python 库将语义模型部署到 Workspace。 This ensures clean separation between your Git repository and workspace.

### 在 Tabular Editor 中使用 Git 集成

当你的语义模型以“保存并包含支持文件”方式保存并同步到 Git repository 后，你就可以通过以下工作流将其同步到 Microsoft Fabric：

1. 在 Tabular Editor 中使用“保存并包含支持文件”选项 **保存模型**
2. 将更改 **提交** 到你的 Git repository
3. 将你的 Fabric Workspace **连接** 到 Git repository
4. 在 Workspace 源代码管理窗格中使用 **全部更新** 按钮，在 Fabric 与 Git 之间 **同步** 模型
   ![Synchronize workspace with Git](~/content/assets/images/common/WorkspaceGitSync.png)

当你的模型同步到 Microsoft Fabric/Power BI 后，Workspace 中显示的语义模型名称由 .platform 文件中的 `displayName` 属性决定，而该属性会根据 Tabular Editor 中 Database 的 `Name` 属性自动设置。 This means the name you configure in Tabular Editor will be the name displayed in Fabric/Power BI.

Tabular Editor automatically sets the model culture to **en-US** when saving with supporting files, if the model does not already have a culture specified. This ensures the model culture is present when synchronizing with Fabric, preventing uncommitted changes that can occur if the culture is not set during the initial synchronization.

更多信息见：

- [Microsoft Fabric Git 集成文档](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration?tabs=azure-devops)
- [Tabular Editor 与 Fabric Git 集成博客文章](https://tabulareditor.com/blog/tabular-editor-and-fabric-git-integration)

## 对比序列化格式

使用“保存并包含支持文件”时，你可以在两种序列化格式之间进行选择：

### TMDL（Tabular Model Definition Language，表格模型定义语言）

- 易于阅读的文本格式
- 在 Git diff 中更容易查看变更
- 更适合代码评审与协作
- 了解更多：[TMDL 文档](tmdl.md)

### TMSL/JSON（.bim）

- 基于 JSON 的格式
- 单文件形式
- 兼容较旧的工具和工作流

Microsoft Fabric Git 集成同时支持这两种格式，选择取决于团队的偏好和工作流需求。

## 另请参阅

- [保存到文件夹](save-to-folder.md)
- [TMDL - 表格模型定义语言](tmdl.md)
