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

在 **工作区模式** 下，Tabular Editor 3 会将从文件加载的模型连接到一个 **Workspace 数据库**。创建新模型，或加载现有模型的 Model.bim 或 Database.json 文件时，都可以使用工作区模式。

当你保存 (**Ctrl+S**) 时，Tabular Editor 会将元数据更改写入磁盘上的文件，并将其同步到 Workspace 数据库。

为每位模型开发者分配各自的 Workspace 数据库，因为共享同一个数据库会导致开发者之间发生冲突。

> [!WARNING]
> 不要在用于托管 Tabular Editor Workspace 数据库的 Fabric Workspace 中启用 Git 集成。 Tabular Editor 会通过 XMLA endpoint 修改 Workspace 数据库，而这些更改会与所连接的分支产生 Git 冲突。

> [!NOTE]
> 对于兼容级别为 1200、1400 或 1500 的模型，请将 Workspace 数据库托管在本地的 Analysis Services 实例上，例如 [SQL Server Developer Edition 2019](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) 中附带的实例。

## 创建新模型

在 Tabular Editor 中创建新模型时，**使用 Workspace 数据库** 默认处于选中状态：

![新模型](~/content/assets/images/new-model.png)

选中该选项后，单击 **确定**，系统会提示你连接到一个 Analysis Services 实例。 Tabular Editor 会将 Workspace 数据库部署到该实例。

> [!IMPORTANT]
> 如果要将 Workspace 数据库部署到 Power BI 服务的 XMLA endpoint，请在上方对话框中选择兼容级别 **1706（Power BI / Fabric）**。

输入服务器详细信息以及可选的凭据后，系统会显示该服务器上的数据库列表。对于 Power BI Workspace，该列表会显示已部署到该 Workspace 的语义模型：

![选择 Workspace 数据库](~/content/assets/images/select-workspace-database.png)

Tabular Editor 会根据你的 Windows 用户名以及当前日期和时间，为 Workspace 数据库建议一个唯一名称；你也可以自行修改。

单击 **确定** 以创建模型，并部署并连接 Workspace 数据库。然后按 **Ctrl+S** 将模型保存为 Model.bim 文件，或选择 **文件 > 保存到文件夹...**，以将元数据存储到 Git 等版本控制系统中。

![保存新内容到文件夹](~/content/assets/images/save-new-to-folder.png)

现在，你可以定义数据源并向模型添加表。每次保存都会同时更新 Workspace 数据库以及你选择的文件或文件夹。

Tabular Editor 会将该模型的 Workspace 数据库详细信息存储在模型元数据文件旁边的 Tabular Model User Options (.tmuo) 文件中。参见 @user-options。

## 打开 Model.bim 或 Database.json 文件

打开现有的 Model.bim 或 Database.json 文件时，系统会提示你是否要将其连接到某个 Workspace 数据库。

![连接到 Workspace 数据库](~/content/assets/images/connect-to-wsdb.png)

选项如下：

- **是**：连接到一个 Analysis Services 实例，并选择一个现有的 Workspace 数据库或创建一个新的 Workspace 数据库。 Tabular Editor 会将该文件的元数据部署到所选的 Workspace 数据库，并在你下次加载该文件时连接到同一个 Workspace 数据库。
- **否**：离线加载元数据，不连接到 Analysis Services。
- **不再询问**：离线加载，并且不再为此文件显示此提示。
- **取消**：不加载文件。

Tabular Editor 会将你的选择以及 Workspace 服务器和数据库信息存储在 [Tabular Model User Options (.tmuo) 文件](xref:user-options) 中。

> [!WARNING]
> Tabular Editor 3 会将已加载的模型元数据部署到你选择的 Workspace 数据库。绝不要将生产数据库用作 Workspace 数据库。为 Workspace 数据库使用单独的 Analysis Services 实例或 Power BI 工作区。

## 工作区模式的优势

在工作区模式下，Tabular Editor 会持续连接到 Analysis Services 实例，从而启用 Tabular Editor 3 的 [连接功能](xref:migrate-from-te2#connected-features)。每次保存（**Ctrl+S**）也会将你的更改部署到该实例以进行测试。直接从 Analysis Services 打开模型时，行为方式相同；不同之处在于，工作区模式还会将元数据保存到磁盘。

> [!NOTE]
> 当刷新操作正在进行时，Tabular Editor 无法与 Analysis Services 实例同步，因为刷新操作会阻止其他写入操作。在刷新期间保存仍会将模型元数据写入磁盘。

## 为模型禁用工作区模式

你可以永久禁用某个模型的工作区模式，也可以仅对当前会话禁用，然后离线编辑模型文件。

### 永久禁用工作区模式

1. 在文件资源管理器中，找到与 `.bim`、`.tmdl` 或 `.json` 文件位于同一目录下的模型 `.tmuo` 文件。

2. 删除 `.tmuo` 文件，或用文本编辑器打开它，并设置：

   ```json
   {
     "UseWorkspaceDatabase": false
   }
   ```

3. 从 `.bim`、`.tmdl` 或 `.json` 文件打开模型。

此后，Tabular Editor 会以离线方式加载该模型。

### 仅为当前会话禁用工作区模式

1. 在“**打开语义模型**”对话框中，选择“**不使用 Workspace 数据库加载**”。

![不加载 Workspace 数据库](~/content/assets/images/load-without-wsdb.png)

该模型会在当前会话中离线加载，下次打开时会重新启用工作区模式。
