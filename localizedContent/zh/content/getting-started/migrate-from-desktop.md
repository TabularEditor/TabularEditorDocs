---
uid: migrate-from-desktop
title: 从 Power BI Desktop 迁移
author: Daniel Otykier
updated: 2021-09-30
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 从 Power BI Desktop 迁移

如果你已经熟悉 Power BI Desktop 中的 Data model 概念，本文将帮助你将数据建模迁移到 Tabular Editor。 因此，我们假定你已扎实掌握 Power Query 编辑器、导入表与计算表格的区别、计算列、度量值等概念。

## Power BI 与 Tabular Editor

从历史上看，Tabular Editor 被设计为面向 SQL Server Analysis Services（表格模式）和 Azure Analysis Services 开发者的工具。 在 Power BI 刚发布时，并没有受支持的方法让第三方工具访问承载 Power BI Data model 的 Analysis Services 实例，因此创建和编辑 Power BI Dataset 的唯一方式是通过 Power BI Desktop。

这一情况在 2020 年三月发生了变化，当时 [Microsoft 宣布在 Power BI Premium 中推出可读写的 XMLA endpoint](https://powerbi.microsoft.com/en-us/blog/announcing-read-write-xmla-endpoints-in-power-bi-premium-public-preview/)。 几个月后，随着 [External Tools 功能的推出](https://powerbi.microsoft.com/en-us/blog/announcing-public-preview-of-external-tools-in-power-bi-desktop/)，甚至可以在 Power BI Desktop 中配合使用第三方工具。

Power BI Premium 提供 XMLA endpoint，使 Data model 开发者能够继续使用既有技能与工具；同时也不难看出，Microsoft 正在大力投入，将 [Power BI Premium 打造成 Analysis Services 的超集](https://community.powerbi.com/t5/Webinars-and-Video-Gallery/Power-BI-Premium-as-a-superset-of-Analysis-Services-the-XMLA/m-p/1434121)。 换句话说，不管是社区工具还是商业工具，与 Power BI 的集成都将长期存在。 事实上，Microsoft Analytics 的 CTO Amir Netz 还与 SQLBI 创始人 Marco Russo 共同发表了 [联合声明](https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices/)，以进一步确认这一点。

在 Tabular Editor ApS，我们坚信 Tabular Editor 3 是目前可用的最佳表格 Data model 建模工具；得益于上述集成，它也不再只是 SQL Server 或 Azure Analysis Services 开发者的专属工具。

在继续之前，需要先了解：Tabular Editor 与 Power BI 搭配使用时，主要有两种截然不同的场景：

- \*\*场景 1：\*\*将 Tabular Editor 作为 Power BI Desktop 的外部工具。
- \*\*场景 2：\*\*Tabular Editor 连接 Power BI Premium 的 XMLA endpoint。

> [!IMPORTANT]
> 你无法使用 Tabular Editor 直接加载 .pbix 文件。 如需了解更多信息，请参阅 <xref:desktop-limitations#power-bi-file-types>。

### 场景 1：将 Tabular Editor 作为 Power BI Desktop 的外部工具

一般而言，本场景面向自助分析师以及无法使用 Power BI Premium 的 Power BI Desktop 用户，旨在简化某些 Data model 建模操作（例如添加和编辑度量值），并解锁其他方式无法使用的高级建模选项（计算组、透视和元数据翻译）。

外部工具连接到由 Power BI Desktop 托管的 Analysis Services 模型。 这使该工具能够对 Data model 进行某些更改。 不过目前，Power BI Desktop 并不支持所有类型的 Data model 建模操作。 理解这一限制，以及将 Tabular Editor 用作 Power BI Desktop 的外部工具时它的行为方式，非常重要。 有关此内容的更多信息，请参阅 <xref:desktop-limitations>。

此方案的典型工作流如下：

1. 在 Power BI Desktop 中打开 .pbit 或 .pbix 文件
2. 通过“外部工具”功能区启动 Tabular Editor
3. 根据需要进行的更改类型，在 Tabular Editor 与 Power BI Desktop 之间来回切换。 例如，你可以通过 Tabular Editor 添加和编辑度量值，但如果需要向模型添加新表，则必须使用 Power BI Desktop。
4. 每次在 Tabular Editor 中完成更改后，用 **文件 > 保存**（CTRL+S）将更改写回 Power BI Desktop。
5. 完成所有更改后，关闭 Tabular Editor。 然后，在 Power BI Desktop 中照常发布或保存 Report。

> [!NOTE]
> 截至 2021 年十月，Power BI Desktop 存在一个缺陷：有时会阻止 Power BI Desktop 自动刷新字段列表和 Visual，以反映通过外部工具所做的更改。 出现这种情况时，保存 .pbix 文件并重新打开，或在模型中手动刷新某个表，通常会使字段列表和所有 Visual 正确更新。

适用于外部工具的[建模限制](xref:desktop-limitations)仅与写入操作或模型修改相关。 如本指南后续所述，你仍可使用 Tabular Editor 3 的连接功能，通过表数据预览、Pivot Grid 或 DAX 查询来浏览模型中的数据。

### 场景 2：Tabular Editor 与 Power BI Premium XMLA endpoint 配合使用

此方案面向在使用 Power BI Premium Capacity 或 Power BI Premium-Per-User Workspace 的组织里的 BI 专业人员，他们想在进行 Dataset 开发时彻底替代 Power BI Desktop。

本质上，Power BI Premium XMLA endpoint 会提供一个 Analysis Services（Tabular）实例。 在此方案中，Tabular Editor 的行为与连接到 Azure Analysis Services 或 SQL Server Analysis Services（Tabular）时没有区别。

此方案的典型工作流如下：

1. 首次迁移到 Tabular Editor 时，请使用 XMLA endpoint 在 Tabular Editor 中打开 Power BI Dataset，然后将模型元数据保存为文件（Model.bim）或文件夹（Database.json）。 有关详细信息，请参阅 @parallel-development。
2. 接下来，在 Tabular Editor 中从你在步骤 1 保存的文件或文件夹打开模型元数据。 也可以选择使用[工作区模式](xref:workspace-mode)。
3. 使用 Tabular Editor 应用更改。
4. 如果使用工作区模式，那么你每次在 Tabular Editor 中单击“保存”（CTRL+S）时，更改都应立即在 Power BI 服务中可见。
5. 如果未使用工作区模式，或完成更改后，请使用 Tabular Editor 的 **Model > Deploy...** 选项将更改发布到 Power BI 服务。

在此场景中，磁盘上存储的文件或文件夹结构是模型元数据的“事实来源”。这不仅支持与版本控制集成的并行开发，还支持使用 Azure DevOps 等自动化构建服务器进行持续集成/持续部署 (CI/CD)。

> [!WARNING]
> 一旦你通过 Power BI 服务的 XMLA endpoint 对 Power BI Dataset 应用更改，该 Dataset 将无法再下载为 .pbix 文件。 有关详细信息，请参阅[使用 XMLA endpoint 的 Dataset 连接](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#power-bi-desktop-authored-datasets)。

使用 Tabular Editor 通过 XMLA endpoint 连接到 Dataset 时，可执行的写入操作或模型修改类型不受限制。

本文其余部分将重点介绍 Power BI Desktop 与 Tabular Editor 在 Data model 开发方面的差异。 由于将 Tabular Editor 作为 Power BI Desktop 的外部工具（场景 1）时存在[建模限制](xref:desktop-limitations)，因此部分章节仅适用于场景 2。

## Tabular Editor 3 用户界面

如果你刚开始使用 Tabular Editor，我们建议阅读以下资源，以了解 Tabular Editor 3 的用户界面：

- [了解 Tabular Editor 3 的用户界面](xref:user-interface)
- [TOM Explorer 视图](xref:tom-explorer-view)
- [属性视图](xref:properties-view)
- [DAX 编辑器](xref:dax-editor)

## Tabular Editor 3 操作指南

下面将快速演示如何在 Tabular Editor 3 中完成常见任务。

### 如何添加度量值

要向模型添加新的度量值，请在 **TOM Explorer** 中右键单击要放置该度量值的表，然后选择 **创建 > 度量值**（快捷键 ALT+1）。 添加度量值后，你可以立即输入度量值名称。

![添加度量值](~/content/assets/images/add-measure.png)

### 如何重命名度量值

如果你需要编辑度量值（或任何其他对象）的名称，只需选中该度量值并按 F2（或双击度量值名称）。 如果同时选中了多个对象，你会看到“批量重命名”对话框，可让你一次性轻松重命名多个对象。

![批量重命名](~/content/assets/images/batch-rename.png)

> [!WARNING]
> 如果在 Data model 中更改对象名称，而 Report 中的一个或多个 Visual 依赖于这些被重命名的对象，则这些 Visual 可能会停止工作。 外部工具无法访问 Power BI Visual 的相关信息，因此当在 Visual 中使用的对象被重命名或删除时，Tabular Editor 无法事先提醒你。

### 如何创建度量值的副本

在 Tabular Editor 3 中，你可以使用熟悉的剪切 (CTRL+X)、复制 (CTRL+C) 和粘贴 (CTRL+V) 操作，快速移动对象并创建副本。 你也可以使用 **TOM Explorer** 在表和显示文件夹之间拖动对象。 如果过程中出现失误，你可以（反复）使用撤销 (CTRL+Z) 和重做 (CTRL+Y) 选项，在已应用的更改历史中前后切换。

### 如何修改度量值的 DAX 表达式

在 **TOM Explorer** 中找到要修改的度量值并选中它。 你可以使用 TOM Explorer 顶部附近的工具栏按钮，切换显示隐藏对象 (CTRL+6) 和显示文件夹 (CTRL+5)。 你也可以在搜索框中输入度量值名称的一部分，来筛选 **TOM Explorer**。

选中度量值后，你会在 **表达式编辑器** 中看到该度量值的 DAX 表达式，并在 **属性** 网格中看到 `Description`、`Format String`、`Hidden` 等各种属性。

![修改度量值](~/content/assets/images/modify-measure.png)

要修改 DAX 表达式，只需将光标置于 **表达式编辑器** 中并更新 DAX 代码。 按 F6 自动格式化代码。 如果你在 TOM Explorer 中选择了其他对象，或点击绿色对勾按钮 **Expression > Accept** (F5)，表达式更改会先保存在 Tabular Editor 本地。 你也可以点击红色“X”按钮 **Expression > Cancel**，取消刚才的修改。 如果你不小心点了 **Accept**，也可以随时通过 **Edit > Undo** (CTRL+Z) 撤销该更改。

要将更改保存回 Power BI Desktop、Power BI XMLA endpoint，或保存回加载模型所用的磁盘文件，请点击 **File > Save** (CTRL+S)。

想了解在编写 DAX 代码时表达式编辑器的更多功能，可以看看 <xref:dax-editor>。

### 如何可视化度量值之间的依赖关系

在 **TOM Explorer** 中选中某个度量值后，使用 **度量值 > 显示依赖关系** (SHIFT+F12)。 这会弹出一个新窗口，用于可视化该度量值 DAX 表达式的依赖关系树。 你可以在查看上游依赖项和下游依赖项之间切换。

![Show Dependencies](~/content/assets/images/show-dependencies.png)

在依赖关系视图中双击某个项，就会跳转到 **TOM Explorer** 中对应的对象。

### 如何更改度量值的格式字符串

在 **TOM Explorer** 中找到要修改的度量值并选中它。 你可以使用 TOM Explorer 顶部附近工具栏上的按钮，切换是否显示隐藏对象（CTRL+6）和显示文件夹（CTRL+5）。 你也可以在搜索框中输入度量值名称的一部分，以筛选 **TOM Explorer** 中的对象。

选中度量值后，在 **属性** 网格中找到 `Format String` 属性，展开它，并按你的偏好设置格式字符串相关属性。 注意 `Format` 属性右侧的下拉按钮。 你也可以直接在 `Format String` 属性中自由输入格式字符串。

![Format String](~/content/assets/images/format-string.png)

### 如何修改多个度量值的 DAX 表达式

Tabular Editor 3 允许你选择多个度量值来创建一个 **DAX脚本**，从而一次性修改所有选中度量值的 DAX 表达式以及各种属性。

要基于现有度量值创建 DAX脚本，只需在 **TOM Explorer** 中选择这些度量值（按住 CTRL 键可选择多个对象，或按住 SHIFT 键可选择一段连续范围内的对象）。 然后右键单击，选择 **Script DAX**。

![Script Dax](~/content/assets/images/script-dax.png)

你可以在脚本中直接添加或修改 `Description`、`FormatString`、`Visible`、`DetailRows` 等属性。

按 F5 将脚本应用到 Data model。 注意，与 **表达式编辑器** 不同，跳转到其他对象不会自动应用你对脚本所做的任何更改。 你仍然可以使用 **编辑 > 撤销**（CTRL+Z）来回退 DAX脚本已应用的更改。

有关更多信息，请参阅 @dax-script-introduction。

### 如何预览表中的数据

要查看表的内容（类似于 Power BI Desktop 中的“数据”选项卡），只需右键单击表并选择“预览数据”。 这会打开一个新选项卡，其中包含该表内容的预览。 你可以滚动浏览表中的所有行，也可以对列进行排序或筛选。 与 Power BI Desktop 不同，你可以打开任意数量的预览选项卡，并在用户界面中将它们并排排列。 预览功能也适用于处于 [DirectQuery 模式](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-use-directquery) 的表（不过预览内容最多仅限前 100 条记录）。

![预览数据](~/content/assets/images/preview-data.png)

> [!NOTE]
> **预览数据** 功能仅在 Tabular Editor 连接到 Power BI Desktop 或 Power BI XMLA endpoint 上的 Dataset 时才可用。

更多信息见 @refresh-preview-query。

### 如何添加计算组

[计算组](https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions) 可用于在模型的所有度量值中定义并复用修改后的 DAX 筛选语境或其他类型的业务逻辑。 要使用 Tabular Editor 添加计算组，只需选择 **模型 > 新建计算组**（ALT+7）。

![添加计算组](~/content/assets/images/add-calc-group.png)

为计算组命名，然后在 **TOM Explorer** 中选中该计算组，使用 **计算组表 > 创建 > 计算项** 选项来添加新的计算项。 你可以通过复制 (CTRL+C) 并粘贴 (CTRL+V) 计算项，加快创建更多计算项的过程。

![添加计算项](~/content/assets/images/add-calc-item.png)

### 如何添加新表

要向模型添加新表，请使用 **模型 > 导入表...** 选项。 Tabular Editor 的 [导入表向导](xref:importing-tables) 将引导你完成该过程。

> [!NOTE]
> Tabular Editor 3 并不支持 Power BI 所支持的所有数据源。 如果你的模型使用了 Tabular Editor 不支持的数据源，从同一数据源导入新表的最简单方式是在 Tabular Editor 中复制现有表 (CTRL+C / CTRL+V)，然后修改分区表达式并按下方所示更新表架构。 要让它生效，确保已启用 **工具 > 偏好 > 架构比较 > 使用 Analysis Services 进行更改检测** 选项。 更多信息见 <xref:importing-tables#updating-table-schema-through-analysis-services>。

> [!IMPORTANT]
> 当将 Tabular Editor 用作外部工具时，此选项默认不可用，因为通过外部工具添加/编辑表在 [Power BI Desktop 中不受支持](xref:desktop-limitations)。

更多信息见 @importing-tables-data-modeling。

### 如何修改表上的 Power Query 表达式

定义每个表要加载哪些内容的 Power Query (M) 表达式位于对应表的 **分区** 中。 你可以在 **TOM Explorer** 中找到这些分区。 选中某个分区后，Tabular Editor 会在 **表达式编辑器** 中显示该分区的 M 表达式，便于你进行编辑。 在编辑并接受表达式更改后，你可以在 **TOM Explorer** 中右键单击该分区，并选择 **更新表架构...** 选项，以便根据更新后的 Power Query 表达式检测表中导入的列是否需要更改。

![Power Query 更新架构](~/content/assets/images/power-query-update-schema.png)

> [!NOTE]
> 目前，Tabular Editor 3 不会对分区表达式执行任何验证。 对于 Power Query (M) 表达式，这项功能计划在 Tabular Editor 3 的后续更新中提供。

> [!IMPORTANT]
> 将 Tabular Editor 用作外部工具时，分区表达式默认是只读的，因为 Power BI Desktop [不支持](xref:desktop-limitations)通过外部工具编辑分区。

如果 Power Query 表达式的更改导致导入表的列发生变化，会弹出一个对话框，让你查看这些更改：

![应用架构更改](~/content/assets/images/combine-sourcecolumn-update.png)

### 如何修改共享 Power Query 表达式

共享表达式是不会直接用于将数据加载到表中的 M 查询。 例如，当你在 Power BI Desktop 中创建 Power Query 参数时，该参数的 M 表达式会存储为共享表达式。 在 Tabular Editor 中，你可以通过 **TOM Explorer** 的“共享表达式”文件夹访问并编辑它们，方式与编辑分区上的 M 查询相同。

![共享表达式](~/content/assets/images/shared-expression.png)

> [!IMPORTANT]
> 将 Tabular Editor 用作外部工具时，共享表达式默认是只读的，因为 Power BI Desktop [不支持](xref:desktop-limitations)通过外部工具编辑分区。

### 如何在表之间添加关系

在两个表之间添加关系最简单的方法是：新建一个图表，把这两个表添加到图表中，然后以 Visual 方式将一张表中的一列拖到另一张表中的对应列上，以指明哪些列应参与该关系。 这与在 Power BI Desktop 中创建关系的方式类似。

1. 要创建新图表，请使用 **文件 > 新建 > 图表**。
2. 要将表添加到图表中，可从 **TOM Explorer** 拖放表，或使用 **图表 > 添加表...**。
3. 添加表后，在（多端）事实表中找到相应列，并将它拖到（一端）维度表中的对应列上。
4. 确认关系设置并点击“确定”。

![通过图表创建关系](~/content/assets/images/create-relationship-through-diagram.gif)

更多信息，请参阅 [使用图表](xref:importing-tables-data-modeling#working-with-diagrams)。

> [!IMPORTANT]
> 将 Tabular Editor 用作外部工具时，无法修改关系，因为 Power BI Desktop [不支持](xref:desktop-limitations)通过外部工具编辑关系。

### 如何发布到 Power BI 服务

要在 Power BI 服务中发布或更新 Dataset，请使用 **模型 > 部署...** 选项，并使用要将 Dataset 发布到的 Workspace 的 XMLA endpoint。

如果你是直接从 XMLA endpoint 加载模型元数据，那么只需点击 **文件 > 保存**（CTRL+S），即可更新加载到 Tabular Editor 中的 Dataset。

> [!NOTE]
> 由于 Tabular Editor 3 桌面版仅用于作为 Power BI Desktop 的外部工具，因此该版本不提供 **Model > Deploy...** 选项。 [更多信息](xref:editions)。

## 后续步骤

- <xref:user-interface>
- @parallel-development
- @boosting-productivity-te3
- <xref:new-pbi-model>