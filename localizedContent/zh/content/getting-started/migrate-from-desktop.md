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

如果你已经熟悉 Power BI Desktop 中的 Data model 概念，本文将帮助你将数据建模迁移到 Tabular Editor。 Thus, we assume you have a solid understanding of concepts such as the Power Query Editor, imported vs. calculated tables, calculated columns, measures, etc.

## Power BI 与 Tabular Editor

Historically, Tabular Editor was designed as a tool for SQL Server Analysis Services (Tabular) and Azure Analysis Services developer. 在 Power BI 刚发布时，并没有受支持的方法让第三方工具访问承载 Power BI Data model 的 Analysis Services 实例，因此创建和编辑 Power BI Dataset 的唯一方式是通过 Power BI Desktop。

这一情况在 2020 年三月发生了变化，当时 [Microsoft 宣布在 Power BI Premium 中推出可读写的 XMLA endpoint](https://powerbi.microsoft.com/en-us/blog/announcing-read-write-xmla-endpoints-in-power-bi-premium-public-preview/)。 A few months later, it even became possible to use third party tools in conjunction with Power BI Desktop, with the [announcement of the External Tools feature](https://powerbi.microsoft.com/en-us/blog/announcing-public-preview-of-external-tools-in-power-bi-desktop/).

Power BI Premium 提供 XMLA endpoint，使 Data model 开发者能够继续使用既有技能与工具；同时也不难看出，Microsoft 正在大力投入，将 [Power BI Premium 打造成 Analysis Services 的超集](https://community.powerbi.com/t5/Webinars-and-Video-Gallery/Power-BI-Premium-as-a-superset-of-Analysis-Services-the-XMLA/m-p/1434121)。 In other words, the integration of third party tools, community as well as commercial, with Power BI is something that is here to stay. In fact, Amir Netz, CTO of Microsoft Analytics, made a [joint statement](https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices/) with Marco Russo, founder of SQLBI, to affirm this point.

在 Tabular Editor ApS，我们坚信 Tabular Editor 3 是目前可用的最佳表格 Data model 建模工具；得益于上述集成，它也不再只是 SQL Server 或 Azure Analysis Services 开发者的专属工具。

在继续之前，需要先了解：Tabular Editor 与 Power BI 搭配使用时，主要有两种截然不同的场景：

- \*\*场景 1：\*\*将 Tabular Editor 作为 Power BI Desktop 的外部工具。
- \*\*场景 2：\*\*Tabular Editor 连接 Power BI Premium 的 XMLA endpoint。

> [!IMPORTANT]
> 你无法使用 Tabular Editor 直接加载 .pbix 文件。 For more information, see <xref:desktop-limitations#power-bi-file-types>.

### 场景 1：将 Tabular Editor 作为 Power BI Desktop 的外部工具

一般而言，本场景面向自助分析师以及无法使用 Power BI Premium 的 Power BI Desktop 用户，旨在简化某些 Data model 建模操作（例如添加和编辑度量值），并解锁其他方式无法使用的高级建模选项（计算组、透视和元数据翻译）。

外部工具连接到由 Power BI Desktop 托管的 Analysis Services 模型。 This allows the tool to make certain changes to the data model. Currently, however, not all types of data modeling operations are supported by Power BI Desktop. It is important to understand this limitation and how Tabular Editor behaves when used as an external tool for Power BI Desktop. See <xref:desktop-limitations> for more information about this.

此方案的典型工作流如下：

1. 在 Power BI Desktop 中打开 .pbit 或 .pbix 文件
2. 通过“外部工具”功能区启动 Tabular Editor
3. 根据需要进行的更改类型，在 Tabular Editor 与 Power BI Desktop 之间来回切换。 For example, you can add and edit measures through Tabular Editor, but you must use Power BI Desktop if you need to add a new table to the model.
4. 每次在 Tabular Editor 中完成更改后，用 **文件 > 保存**（CTRL+S）将更改写回 Power BI Desktop。
5. When you are done making changes, close Tabular Editor. 然后，在 Power BI Desktop 中照常发布或保存 Report。

> [!NOTE]
> 截至 2021 年十月，Power BI Desktop 存在一个缺陷：有时会阻止 Power BI Desktop 自动刷新字段列表和 Visual，以反映通过外部工具所做的更改。 When this happens, saving the .pbix file and reopening it, or manually refreshing a table within the model, usually causes the field list and all visuals to update correctly.

适用于外部工具的[建模限制](xref:desktop-limitations)仅与写入操作或模型修改相关。 You can still use Tabular Editor 3's connected features to browse the data within the model through table data previews, Pivot Grids or DAX queries, as described later in this guide.

### 场景 2：Tabular Editor 与 Power BI Premium XMLA endpoint 配合使用

此方案面向在使用 Power BI Premium Capacity 或 Power BI Premium-Per-User Workspace 的组织里的 BI 专业人员，他们想在进行 Dataset 开发时彻底替代 Power BI Desktop。

本质上，Power BI Premium XMLA endpoint 会提供一个 Analysis Services（Tabular）实例。 In this scenario, Tabular Editor behaves no different than it would when connected to Azure Analysis Services or SQL Server Analysis Services (Tabular).

此方案的典型工作流如下：

1. 首次迁移到 Tabular Editor 时，请使用 XMLA endpoint 在 Tabular Editor 中打开 Power BI Dataset，然后将模型元数据保存为文件（Model.bim）或文件夹（Database.json）。 See @parallel-development for more information.
2. Going forward, open the model metadata in Tabular Editor from the file or folder you saved in step 1. Optionally use [workspace mode](xref:workspace-mode).
3. 使用 Tabular Editor 应用更改。
4. 如果使用工作区模式，那么你每次在 Tabular Editor 中单击“保存”（CTRL+S）时，更改都应立即在 Power BI 服务中可见。
5. 如果未使用工作区模式，或完成更改后，请使用 Tabular Editor 的 **Model > Deploy...** 选项将更改发布到 Power BI 服务。

在此场景中，磁盘上存储的文件或文件夹结构是模型元数据的“事实来源”。这不仅支持与版本控制集成的并行开发，还支持使用 Azure DevOps 等自动化构建服务器进行持续集成/持续部署 (CI/CD)。

> [!WARNING]
> 一旦你通过 Power BI 服务的 XMLA endpoint 对 Power BI Dataset 应用更改，该 Dataset 将无法再下载为 .pbix 文件。 See [Dataset connectivity with the XMLA endpoint](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#power-bi-desktop-authored-datasets) for more information.

使用 Tabular Editor 通过 XMLA endpoint 连接到 Dataset 时，可执行的写入操作或模型修改类型不受限制。

The remainder of this article focuses on differences between Power BI Desktop and Tabular Editor for data model development. 由于将 Tabular Editor 作为 Power BI Desktop 的外部工具（场景 1）时存在[建模限制](xref:desktop-limitations)，因此部分章节仅适用于场景 2。

## Tabular Editor 3 用户界面

如果你刚开始使用 Tabular Editor，我们建议阅读以下资源，以了解 Tabular Editor 3 的用户界面：

- [了解 Tabular Editor 3 的用户界面](xref:user-interface)
- [TOM Explorer 视图](xref:tom-explorer-view)
- [属性视图](xref:properties-view)
- [DAX 编辑器](xref:dax-editor)

## Tabular Editor 3 操作指南

下面将快速演示如何在 Tabular Editor 3 中完成常见任务。

### 如何添加度量值

要向模型添加新的度量值，请在 **TOM Explorer** 中右键单击要放置该度量值的表，然后选择 **创建 > 度量值**（快捷键 ALT+1）。 After the measure is added, you can immediately type the name of the measure.

![添加度量值](~/content/assets/images/add-measure.png)

### 如何重命名度量值

如果你需要编辑度量值（或任何其他对象）的名称，只需选中该度量值并按 F2（或双击度量值名称）。 If multiple objects are selected, you will see the Batch rename dialog, that makes it easy to rename multiple objects in one go.

![批量重命名](~/content/assets/images/batch-rename.png)

> [!WARNING]
> 如果在 Data model 中更改对象名称，而 Report 中的一个或多个 Visual 依赖于这些被重命名的对象，则这些 Visual 可能会停止工作。 External tools cannot access information about Power BI visuals, so Tabular Editor is not able to warn you before an object that is used in a visual is renamed or deleted.

### 如何创建度量值的副本

In Tabular Editor 3, you can use the familiar Cut (CTRL+X), Copy (CTRL+C) and Paste (CTRL+V) operations to quickly move around and make copies of objects. You can also drag objects between tables and display folders using the **TOM Explorer**. If you make a mistake along the way, you can use the Undo (CTRL+Z) and Redo (CTRL+Y) options (repeatedly) to navigate back and forth through the history of changes applied.

### 如何修改度量值的 DAX 表达式

在 **TOM Explorer** 中找到要修改的度量值并选中它。 You can toggle the display of hidden objects (CTRL+6) and display folders (CTRL+5) using the toolbar buttons near the top of the TOM Explorer. You may also type the partial name of the measure in the search box, to filter the **TOM explorer**.

选中度量值后，你会在 **表达式编辑器** 中看到该度量值的 DAX 表达式，并在 **属性** 网格中看到 `Description`、`Format String`、`Hidden` 等各种属性。

![修改度量值](~/content/assets/images/modify-measure.png)

要修改 DAX 表达式，只需将光标置于 **表达式编辑器** 中并更新 DAX 代码。 Hit F6 to automatically format the code. If you select a different object in the TOM Explorer or click the green checkmark button **Expression > Accept** (F5), the expression change is stored locally in Tabular Editor. You can also cancel the modification you made by hitting the red "X", **Expression > Cancel**. If you accidentally hit **Accept**, you can always undo the change by using the **Edit > Undo** (CTRL+Z) option.

要将更改保存回 Power BI Desktop、Power BI XMLA endpoint，或保存回加载模型所用的磁盘文件，请点击 **File > Save** (CTRL+S)。

想了解在编写 DAX 代码时表达式编辑器的更多功能，可以看看 <xref:dax-editor>。

### 如何可视化度量值之间的依赖关系

While a measure is selected in the **TOM Explorer** use the **Measure > Show dependencies** (SHIFT+F12) option. This causes a new window to pop up, visualizing the dependency tree of the DAX expression for that measure. You can switch between viewing both upstream and downstream dependencies.

![Show Dependencies](~/content/assets/images/show-dependencies.png)

在依赖关系视图中双击某个项，就会跳转到 **TOM Explorer** 中对应的对象。

### 如何更改度量值的格式字符串

在 **TOM Explorer** 中找到要修改的度量值并选中它。 You can toggle the display of hidden objects (CTRL+6) and display folders (CTRL+5) using the toolbar buttons near the top of the TOM Explorer. You may also type the partial name of the measure in the search box, to filter the **TOM explorer**.

Once the measure is selected, locate the `Format String` property in the **Properties** grid, expand it, and set the format string properties according to your preferences. Note the dropdown button at the right of the `Format` property. You may also freely enter a format string in the `Format String` property itself.

![Format String](~/content/assets/images/format-string.png)

### 如何修改多个度量值的 DAX 表达式

Tabular Editor 3 允许你选择多个度量值来创建一个 **DAX脚本**，从而一次性修改所有选中度量值的 DAX 表达式以及各种属性。

要基于现有度量值创建 DAX脚本，只需在 **TOM Explorer** 中选择这些度量值（按住 CTRL 键可选择多个对象，或按住 SHIFT 键可选择一段连续范围内的对象）。 Then, right click and hit **Script DAX**.

![Script Dax](~/content/assets/images/script-dax.png)

你可以在脚本中直接添加或修改 `Description`、`FormatString`、`Visible`、`DetailRows` 等属性。

Hit F5 to apply the script to the data model. Note that unlike the **Expression Editor**, navigating to a different object will not automatically apply any changes made to the script. 你仍然可以使用 **编辑 > 撤销**（CTRL+Z）来回退 DAX脚本已应用的更改。

有关更多信息，请参阅 @dax-script-introduction。

### 如何预览表中的数据

To view the contents of a table (similar to the Data Tab in Power BI Desktop), simply right-click on a table and choose "Preview data". This will open a new tab containing a preview of the table content. You can scroll through all rows of the table, as well as apply sorting or filtering to columns. Unlike Power BI Desktop, you can open as many of these preview tabs as you like and arrange them next to each other in the user interface. The preview also works for tables in [DirectQuery mode](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-use-directquery) (although the preview will be limited to the first 100 records).

![预览数据](~/content/assets/images/preview-data.png)

> [!NOTE]
> **预览数据** 功能仅在 Tabular Editor 连接到 Power BI Desktop 或 Power BI XMLA endpoint 上的 Dataset 时才可用。

更多信息见 @refresh-preview-query。

### 如何添加计算组

[计算组](https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions) 可用于在模型的所有度量值中定义并复用修改后的 DAX 筛选语境或其他类型的业务逻辑。 To add a calculation group using Tabular Editor, simply use the **Model > New Calculation Group** (ALT+7) option.

![添加计算组](~/content/assets/images/add-calc-group.png)

为计算组命名，然后在 **TOM Explorer** 中选中该计算组，使用 **计算组表 > 创建 > 计算项** 选项来添加新的计算项。 You can copy (CTRL+C) and paste (CTRL+V) calculation items to speed up this process for additional items.

![添加计算项](~/content/assets/images/add-calc-item.png)

### 如何添加新表

要向模型添加新表，请使用 **模型 > 导入表...** 选项。 Tabular Editor's [Import Table Wizard](xref:importing-tables) will guide you through the process.

> [!NOTE]
> Tabular Editor 3 并不支持 Power BI 所支持的所有数据源。 If your model uses a data source not supported by Tabular Editor, the easiest way to import a new table from the same source is to copy an existing table in Tabular Editor (CTRL+C / CTRL+V), and then modify the partition expression and update the table schema as shown below. For this to work, make sure that the **Tools > Preferences > Schema Compare > Use Analysis Services for change detection** option is enabled. See <xref:importing-tables#updating-table-schema-through-analysis-services> for more information.

> [!IMPORTANT]
> 当将 Tabular Editor 用作外部工具时，此选项默认不可用，因为通过外部工具添加/编辑表在 [Power BI Desktop 中不受支持](xref:desktop-limitations)。

更多信息见 @importing-tables-data-modeling。

### 如何修改表上的 Power Query 表达式

Power Query (M) expressions that define what is loaded into each table reside in the corresponding table's **Partition**. The partitions can be located in the **TOM Explorer**. When selecting a partition, Tabular Editor displays the M expression for that partition in the **Expression Editor**, allowing you to edit it. 在编辑并接受表达式更改后，你可以在 **TOM Explorer** 中右键单击该分区，并选择 **更新表架构...** 选项，以便根据更新后的 Power Query 表达式检测表中导入的列是否需要更改。

![Power Query 更新架构](~/content/assets/images/power-query-update-schema.png)

> [!NOTE]
> 目前，Tabular Editor 3 不会对分区表达式执行任何验证。 For Power Query (M) expressions, this is planned for a later update of Tabular Editor 3.

> [!IMPORTANT]
> 将 Tabular Editor 用作外部工具时，分区表达式默认是只读的，因为 Power BI Desktop [不支持](xref:desktop-limitations)通过外部工具编辑分区。

如果 Power Query 表达式的更改导致导入表的列发生变化，会弹出一个对话框，让你查看这些更改：

![应用架构更改](~/content/assets/images/combine-sourcecolumn-update.png)

### 如何修改共享 Power Query 表达式

Shared Expressions are M queries that are not directly used to load data into a table. For example, when you create a Power Query parameter in Power BI Desktop, the M expression for this parameter is stored as a Shared Expression. In Tabular Editor, These can be accessed through the Shared Expressions folder of the **TOM Explorer** and edited just like M queries on partitions.

![共享表达式](~/content/assets/images/shared-expression.png)

> [!IMPORTANT]
> 将 Tabular Editor 用作外部工具时，共享表达式默认是只读的，因为 Power BI Desktop [不支持](xref:desktop-limitations)通过外部工具编辑分区。

### 如何在表之间添加关系

在两个表之间添加关系最简单的方法是：新建一个图表，把这两个表添加到图表中，然后以 Visual 方式将一张表中的一列拖到另一张表中的对应列上，以指明哪些列应参与该关系。 This is similar to how you would create a relationship in Power BI Desktop.

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
> 由于 Tabular Editor 3 桌面版仅用于作为 Power BI Desktop 的外部工具，因此该版本不提供 **Model > Deploy...** 选项。[更多信息](xref:editions)。

## 后续步骤

- <xref:user-interface>
- @并行开发
- @boosting-productivity-te3
- <xref:new-pbi-model>