---
uid: workspace-mode
title: 工作区模式
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

Tabular Editor 3 在工具内创建新模型，或加载现有模型的 Model.bim 或 Database.json 文件时，引入了 **Workspace 工作区模式** 的概念。

使用工作区模式时，每当你按下保存 (Ctrl+S)，Tabular Editor 都会将模型元数据更改同步到 **Workspace 数据库**，并同时将这些更改保存到磁盘上的文件(们)中。

理想情况下，每位模型开发人员都应使用各自的 Workspace 数据库，以避免开发过程中的冲突。

> [!WARNING]
> 不要在用于托管 Tabular Editor Workspace 数据库的 Fabric Workspace 上启用 Git 集成。 This is to avoid Git conflicts as you develop the model, since Tabular Editor makes changes to the workspace database through the XMLA endpoint, and these changes will not be in sync with any underlying Git branch.

> [!NOTE]
> 对于兼容级别为 1200、1400 或 1500 的模型，我们建议使用本地 Analysis Services 实例来托管 Workspace 数据库，例如 [SQL Server Developer Edition 2019](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) 中附带的实例。

# 创建新模型

在 Tabular Editor 中创建新模型时，“使用 Workspace 数据库”选项默认处于选中状态：

![新模型](~/content/assets/images/new-model.png)

Leaving this checked, you will be prompted to connect to an instance of Analysis Services after hitting "OK". 这就是你的 Workspace 数据库将要部署到的 Analysis Services 实例。

> [!IMPORTANT]
> If you plan to deploy your workspace database to the Power BI Service XMLA endpoint, make sure you choose Compatibility Level 1706 (Power BI / Fabric) in the dialog above.

输入 Analysis Services 服务器信息并（可选）提供凭据后，你会看到服务器上当前所有数据库的列表（如果是 Power BI Workspace，则会显示已部署到该 Workspace 的 Dataset 列表）：

![选择 Workspace 数据库](~/content/assets/images/select-workspace-database.png)

Tabular Editor 会基于你的 Windows 用户名以及当前日期和时间，为你的 Workspace 数据库建议一个新的唯一名称；当然，你也可以将其改成更有意义的名称。

点击“确定”后，新模型会被创建，同时 Workspace 数据库会被部署并建立连接。 At this point, hit save (Ctrl+S) to save your model as a Model.bim file. You may also choose the File > Save to Folder... 如果你打算将模型元数据存储在 Git 等版本控制系统中，请使用此菜单项。

![保存新内容到文件夹](~/content/assets/images/save-new-to-folder.png)

At this point, you are ready to define data sources and add new tables to your model. 之后每次点击“保存”(Ctrl+S)，都会将更改写入并更新 Workspace 数据库，同时也会更新你之前选择的文件/文件夹。

与此模型关联的 Workspace 数据库信息，会存储在模型元数据文件旁边的 Tabular Model User Options (.tmuo) 文件中。 See @user-options for more information.

# 打开 Model.bim 或 Database.json 文件

如果你打开现有的 Model.bim 或 Database.json 文件，Tabular Editor 3 会提示你是否要为该文件初始化一个 Workspace 数据库。

![连接到 Workspace 数据库](~/content/assets/images/connect-to-wsdb.png)

可选项包括：

- **Yes**: Connect to an instance of Analysis Services and choose an existing workspace database or create a new one. The next time you load the same Model.bim or Database.json file, Tabular Editor will connect to the same workspace database. Tabular Editor 会将 Model.bim 或 Database.json 文件部署到所选的 Workspace 数据库上。
- **否**：Tabular Editor 将以离线方式加载文件中的元数据，不与 Analysis Services 建立连接。
- **不再询问**：与上面相同，但下次打开同一个 Model.bim 或 Database.json 文件时，Tabular Editor 将不再询问你是否连接到 Workspace 数据库。
- **取消**：不加载该文件。

有关某个模型是否连接到 Workspace 数据库，以及要使用的 Workspace 服务器和数据库的信息，存储在 [Tabular Model User Options (.tmuo) 文件](xref:user-options) 中。

> [!WARNING]
> 在选择 Workspace 数据库时，Tabular Editor 3 会将已加载的模型元数据部署到该 Workspace 数据库上。 For this reason, you should never use a production database as your workspace database. Moreover, we recommend using a separate Analysis Services instance/Power BI workspace for your workspace databases.

# 工作区模式的优势

工作区模式的主要优势是它允许 Tabular Editor 始终保持与某个 Analysis Services 实例的连接。 In other words, Tabular Editor 3's new [connected features](xref:migrate-from-te2#connected-features) are enabled. But even if you choose not to use these features, it is much easier to synchronize an instance of Analysis Services for purposes of testing your changes. All you have to do is hit Save (CTRL+S). This is similar to when Tabular Editor opens model metadata directly from an instance of Analysis Services, but with workspace mode, the model metadata is simultaneously saved to disk.

> [!NOTE]
> 当刷新操作正在进行时，Tabular Editor 无法与 Analysis Services 实例同步（刷新操作会阻止其他写入操作）。 However, hitting Save (CTRL+S) while such an operation is under way will still save the model metadata to disk, while using workspace mode.

# 为模型禁用工作区模式

如果你希望 _禁用工作区模式_ 并完全脱机编辑模型文件，请选择下面的方法之一。

## 永久禁用工作区模式

1. 在文件资源管理器中找到模型的 `.tmuo` Workspace 文件（它与 `.bim`、`.tmdl` 或 `.json` 文件位于同一目录）。

2. Do **either** of the following:
   - **删除** `.tmuo` 文件，**或**
   - 用文本编辑器打开它，并将其设置为：

     ```json
     {
       "UseWorkspaceDatabase": false
     }
     ```

3. 像平常一样，从 `.bim`、`.tmdl` 或 `.json` 文件打开模型。

从此以后，每次加载该模型时，Tabular Editor 都会保持脱机状态。

## 仅为当前会话禁用工作区模式

1. 在“**打开语义模型**”对话框中，勾选“**不加载 Workspace 数据库**”。

![不加载 Workspace 数据库](~/content/assets/images/load-without-wsdb.png)

模型会在本次会话中以脱机方式加载；下次打开时将重新启用工作区模式，除非你重复这些步骤。
