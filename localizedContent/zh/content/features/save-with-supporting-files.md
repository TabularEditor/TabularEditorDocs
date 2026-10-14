---
uid: save-with-supporting-files
title: 保存并包含支持文件
author: Peer Grønnerup
updated: 2026-10-12
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

“保存并包含支持文件”会在保存语义模型的同时，一并保存 Microsoft Fabric Git 集成所需的元数据文件。它用于在 Fabric Workspace 与 Git repository 之间同步由 Tabular Editor 保存的模型。

> [!NOTE]
> “保存并包含支持文件”仅在将模型保存为 .bim (TMSL) 文件，或以 TMDL 作为序列化模式保存到文件夹时可用。

## 文件结构和模型属性

Tabular Editor 会在保存路径中创建一个名为 **数据库名称.SemanticModel** 的文件夹。该名称来自 TOM Explorer 中 Database 对象的 `Name` 属性。只有当文件夹名称以 **.SemanticModel** 结尾时，Fabric 才会将其识别为语义模型项。

Tabular Editor 还会将 Database 的 `Name` 属性写入 .platform 元数据文件中的 `displayName` 属性，并将 Database 的 `Description` 属性写入其中的 `description`。

<a name="power-bi-desktop-authored-pbip-projects"></a>

### 在 Power BI Desktop 中创作的 PBIP 项目

在由 Power BI Desktop 创建的 [Power BI Project (PBIP)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview) 语义模型中，项的名称和说明仅存储在 `.platform` 文件中，模型元数据本身不包含这两项。

对于这些模型，Tabular Editor 会保留 `.platform` 中现有的 `displayName` 和 `description`，并按该项的名称为新文件夹命名。

> [!NOTE]
> 在 Tabular Editor 3.27.0 之前，保存这些模型会在下一次 Git 同步时重命名 Fabric workspace 中的该项，并清空其说明。

如果在 Database 对象上设置了 `Name` 和 `Description` 属性，Tabular Editor 会在每次保存时将它们同步到 `.platform`。

### 包含的文件

每个已保存的模型都包含以下文件：

- **.platform**: 项元数据，包括其类型、显示名称、说明和 `logicalId`（自动生成的跨 Workspace 标识符）。
- **definition.pbism**：语义模型的定义及核心设置。

模型本身按序列化格式存储：

| 格式                                                 | 模型存储                                  |
| -------------------------------------------------- | ------------------------------------- |
| **TMDL**                                           | `definition` 文件夹，里面包含带有模型元数据的 TMDL 文件 |
| **TMSL (.bim)** | `model.bim` 文件（文件名是固定的）               |

名为“Sales”的数据库的文件夹结构如下：

```text
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

1. 在 Tabular Editor 3 中创建或打开一个语义模型。
2. 在 TOM Explorer 中设置 Database 对象的 `Name` 属性。这会设置文件夹名称以及 .platform 文件中的 `displayName`。
   ![设置 Database 的 Name 属性](~/content/assets/images/common/SaveWithSupportingFilesSetName.png)
3. 如果保存到文件夹，请在 **工具 > 偏好 > 文件格式** 下将序列化模式设置为 TMDL。
4. 选择 **文件 > 另存为** 或 **文件 > 保存到文件夹**。
5. 选择一个文件夹，然后选择 **保存并包含支持文件**。
   ![“保存并包含支持文件”对话框](~/content/assets/images/common/SaveWithSupportingFilesDialog.png)
6. 点击 **保存**。

Tabular Editor 会在保存位置创建 **.SemanticModel** 文件夹，例如 `Sales.SemanticModel`，并将文件写入其中。

## Microsoft Fabric 中的 Git 集成

Git 集成适用于分配了 Microsoft Fabric F-SKU 容量、Power BI Premium 容量或 Power BI Premium Per User (PPU) 的 Workspace。

> [!WARNING]
> 语义模型项的 Git 集成功能目前处于预览版。有关 Fabric Git 集成所支持项目的最新信息，请参阅 [Fabric Git 集成中支持的项](https://learn.microsoft.com/fabric/cicd/git-integration/intro-to-git-integration#supported-items)。

> [!CAUTION]
> 不要在托管你的 Tabular Editor Workspace 数据库的 Fabric Workspace 中启用 Git 集成。如果 Tabular Editor 将模型同步到已连接 Git 的 Workspace，该 Workspace 会显示与 Git repository 不一致的未提交更改；同步这些更改会导致 Git 冲突。
>
> 将 Git repository 与 Workspace 分开，并使用 Tabular Editor、Fabric REST API、Fabric CLI 或 fabric-cicd Python 库将语义模型部署到 Workspace。

### 在 Tabular Editor 中使用 Git 集成

保存模型并包含支持文件后，将其同步到 Microsoft Fabric：

1. 在 Tabular Editor 中保存模型，并选中 **保存并包含支持文件**。
2. 将更改提交到你的 Git repository。
3. 将你的 Fabric Workspace 连接到 Git repository。
4. 在 Workspace 源代码管理窗格中点击 **全部更新**。
   ![将 Workspace 与 Git 同步](~/content/assets/images/common/WorkspaceGitSync.png)

Workspace 会使用 .platform 文件中的 `displayName` 来显示语义模型，即你在 Tabular Editor 中设置的数据库 `Name`。

如果模型没有区域设置，Tabular Editor 在连同支持文件一起保存时会将其设置为 **en-US**。如果没有区域设置，首次与 Fabric 同步后会留下未提交的更改。

更多信息见：

- [Microsoft Fabric Git 集成文档](https://learn.microsoft.com/fabric/cicd/git-integration/intro-to-git-integration?tabs=azure-devops)
- [Tabular Editor 与 Fabric Git 集成博客文章](https://tabulareditor.com/blog/tabular-editor-and-fabric-git-integration)

## 对比序列化格式

Fabric Git 集成支持以下两种序列化格式：

- **[TMDL](xref:tmdl)** 是一种便于人工阅读的文本格式。在 Git 中更容易查看它的差异。
- **TMSL (.bim)** 将模型存储为单个 JSON 文件，旧版工具和工作流可以读取它。

## 后续步骤

- [保存到文件夹](xref:save-to-folder)
- [TMDL - 表格模型定义语言](xref:tmdl)
