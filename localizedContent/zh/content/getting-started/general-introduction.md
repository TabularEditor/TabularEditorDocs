---
uid: general-introduction
title: 总体介绍和体系结构
author: Daniel Otykier
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 总体介绍和体系结构

Tabular Editor 是一款用于开发表格模型的 Windows 桌面应用程序。 Specifically, the tool lets you edit the Tabular Object Model (TOM) metadata. The tool can load the TOM metadata from a file or from an existing Analysis Services database, and it can also deploy updated TOM metadata to Analysis Services.

> [!NOTE]
> 我们使用术语 **表格模型** 来同时表示 Analysis Services Tabular 模型和 Power BI Dataset，因为 Analysis Services Tabular 是 Power BI 使用的 Data model 引擎。 Similarly, when we use term **Analysis Services**, we mean "any instance of Analysis Services", which could be SQL Server Analysis Services, Power BI Desktop or the Power BI Service XMLA Endpoint.

## Tabular Object Model (TOM) 元数据

A data model is made up by a number of tables. Each table has one or more columns, and a table may also contain measures and hierarchies. Typically, the data model also defines relationships between tables, data sources containing connection details and table partitions containing data source expressions (SQL or M queries) for loading data, etc. 所有这些信息统称为 **模型元数据**，并以一种基于 JSON 的格式存储，该格式称为 **Tabular Object Model (TOM)**。

- 当使用 Visual Studio 创建表格模型时，用于表示 TOM 元数据的 JSON 会存储在名为 **Model.bim** 的文件中。
- 当使用 Power BI Desktop 创建 Data model 时，TOM 元数据会嵌入在 .pbix 或 .pbit 文件中 (因为这种文件格式还包含许多其他细节，例如 Visual 的定义、Bookmark 等，而这些与 Data model 本身无关)。

借助名为 [AMO/TOM](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 的客户端库，Tabular Editor 能够从这种基于 JSON 的格式加载元数据，并将其保存回该格式。 In addition, the client library allows Tabular Editor to connect directly to any instance of Analysis Services, in order to obtain the model metadata from an existing database. This is illustrated in the figure below.

![架构](~/content/assets/images/architecture.png)

> [!NOTE]
> In the paragraph above, we used the term **database** to represent a model that has been deployed to Analysis Services. 在 Power BI 服务中，术语 **dataset** 用来表示同一事物，即表格模型。

Tabular Editor 可从以下来源加载模型元数据：

- [1] Model.bim 文件
- [2] Database.json 文件（更多信息见 @parallel-development）
- [3] .pbit 文件（Power BI 模板）
- [4] SQL Server Analysis Services（表格模式）上的数据库
- [5] Azure Analysis Services 上的数据库
- [6] A semantic model in a Power BI workspace assigned to a capacity\*
- [7] Import/DirectQuery 模式下的 Power BI Desktop Report

\*Third party tools connect to Power BI semantic models through the [XMLA endpoint](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools). It requires a Microsoft Fabric capacity (F SKU), a Power BI Embedded capacity (A or EM SKU), a legacy Premium capacity (P SKU) or a Premium Per User license. XMLA read/write is enabled by default on all capacity SKUs since June 2025; see @xmla-as-connectivity if you can't connect.

> [!IMPORTANT]
> Tabular Editor 2.x supports all sources 1-7 above. Tabular Editor 3 仅支持其中部分来源，具体取决于你使用的是哪种 [Tabular Editor 3 版本](xref:editions)。

Once the model metadata has been loaded in Tabular Editor, the user is free to add/edit/remove **objects** and change **object properties**. Modifications are not saved back to the source until the user explicitly saves the model, either by choosing **File > Save** or by hitting CTRL+S. If the model metadata was loaded from a file source (sources 1-3 above), that file will then be updated. If the model metadata was loaded from Analysis Services (sources 4-7 above), then the changes are saved back to Analysis Services. Note that certain changes may cause objects to enter a state where they can no longer be queried by end-users. For example, if you add a column to a table, you will need to [refresh the table](xref:refresh-preview-query#refreshing-data) before users can query the contents of that table or any measures that dependent on the table.

> [!WARNING]
> 将模型元数据的更改保存回 Power BI Desktop（以上来源 7）时，会有一些限制。 See @desktop-limitations for more information.

### TOM 对象和属性

TOM 元数据由 **对象** 和 **属性** 组成。

TOM **对象** 示例：

- 数据源
- 表
- 分区
- 度量值
- KPI
- 列
- 模型角色

TOM **对象属性**示例：

- `Name`（文本）
- `显示文件夹`（文本）
- `Description`（文本）
- `Hidden`（true/false）
- `Summarize By`（可选项之一：None、Sum、Min、Max、...）

大多数属性都是简单值（文本、true/false、从选项中选择其一，也称为。 enums), but properties can also reference other objects (for example, the `Sort By Column` property should reference a column). Properties can also be arrays of objects, such as the `Members` property on the Model Role object.

Tabular Editor 通常沿用 [Microsoft.AnalysisServices.Tabular 命名空间](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet) 中定义的对象和属性名称。 If you want to learn more about specific TOM objects or properties, always consult the namespace documentation. For example, to learn what the "Summarize By" column property does, first locate the "Column" class in Microsoft's documentation, then expand "Properties" and scroll to "SummarizeBy". You should then get to [this article](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.column.summarizeby?view=analysisservices-dotnet).

![Microsoft 文档中的 SummarizeBy](~/content/assets/images/asdocs-summarizyby.png)

### 编辑属性值

Tabular Editor 的两个版本都会以层级视图显示对象模型元数据，这个视图称为 **TOM Explorer**，其结构大致对应 JSON 元数据的层级结构：

![TOM Explorer](~/content/assets/images/tom-explorer.png)

通常情况下，Tabular Editor 允许你先在 TOM Explorer 中选择一个对象（按住 SHIFT 或 CTRL 可一次选择多个对象），然后直接在 **属性视图** 中编辑属性值（见下图）。

![属性视图](~/content/assets/images/properties-view.png)

Tabular Editor 不会对修改后的属性值进行显式验证，除了少数基本规则（例如，对象名称不能为空、度量值名称必须唯一等）。 It is your responsibility as a tabular model developer to know which properties to set and what values to use.

如果你在编辑属性值时出错，随时都可以按 CTRL+Z（编辑 > 撤销）撤销上一次属性更改。

## 架构

As hinted above, Tabular Editor has two different modes of operation: Metadata from file (aka. **file mode**) and metadata from Analysis Services (aka. **connected mode**). In addition, Tabular Editor 3 introduces a hybrid approach called [**workspace mode**](xref:workspace-mode).

在继续之前，了解这些模式之间的差异很重要：

- In **file mode**, Tabular Editor loads and saves all model metadata from and to a file on disk. In this mode, Tabular Editor cannot interact with model **data** (that is, table previews, DAX queries, Pivot Grids, and data refresh operations are not enabled). This mode can be used entirely offline, even when no instance of Analysis Services is available. The supported file formats for model metadata are:
  - Model.bim（与 Visual Studio 使用的格式相同）
  - Database.json（仅 Tabular Editor 使用的文件夹结构格式）
  - .pbit（Power BI 模板）
- 在 **连接模式** 下，Tabular Editor 会从 Analysis Services 加载模型元数据，并将元数据保存回 Analysis Services。 In this mode, it is possible to interact with model **data** using Tabular Editor 3 (table previews, DAX queries, Pivot Grids and data refresh). This mode requires connectivity to an instance of Analysis Services.
- 在 **工作区模式** 下，Tabular Editor 3 会从磁盘上的文件加载模型元数据，并将元数据部署到 Analysis Services。 On subsequent saves (CTRL+S), updates are saved both to disk and to the connected instance of Analysis Services. It is possible to interact with model **data** similar to **connected mode**.

### 元数据同步

One of the major benefits of Tabular Editor over the standard tools (Visual Studio, Power BI Desktop), is that model metadata is only saved upon request. In other words, you can make multiple changes to objects and properties without having to wait for any Analysis Services instance to become synchronized between each change. The synchronization of the Analysis Services database is an operation that may take several seconds to complete, depending on the size and complexity of the data model. In Power BI Desktop, this synchronization happens every time the notorious "Working on it" spinner appears on the screen. In Tabular Editor, this only happens when you explicitly save your changes (CTRL+S).

当然，缺点是：在测试任何元数据修改带来的影响之前，你必须记得先显式保存这些更改。

## 后续步骤

- @installation-activation-basic
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2