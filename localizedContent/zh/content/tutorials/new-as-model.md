---
uid: new-as-model
title: 创建 Analysis Services 模型
author: Daniel Otykier
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "仅限 SQL Server Standard Edition"
        - edition: Enterprise
          full: true
---

# （教程）创建您的第一个 Analysis Services 模型

本页将指导您使用 Tabular Editor 3 从零开始创建一个新的 Analysis Services 表格模型。

> [!NOTE]
> Tabular Editor 3 商业版仅限于 [SQL Server Standard Edition](https://docs.microsoft.com/en-us/analysis-services/analysis-services-features-supported-by-the-editions-of-sql-server-2016?view=asallproducts-allversions#tabular-models) 和 [Azure Analysis Services Basic Tier](https://docs.microsoft.com/en-us/azure/analysis-services/analysis-services-overview#basic-tier)。请注意，在这些层级中不支持某些建模功能。

##### 创建新模型

- 在“文件”菜单中，选择“新建” > “模型……”或按 `CTRL+N`

![新建模型](~/content/assets/images/new-as-model-new-model.png)

- 为模型命名，或使用默认名称。然后，根据你要面向的 Analysis Services 版本选择相应的兼容级别。可选项如下：

  - 1200（Azure Analysis Services / SQL Server 2016+）
  - 1400（Azure Analysis Services / SQL Server 2017+）
  - 1500（Azure Analysis Services / SQL Server 2019+）
  - 1600 (Azure Analysis Services / SQL Server 2022+)
  - 1700 (Azure Analysis Services / SQL Server 2025+)
  - 1706 (Power BI / Fabric)

  1700 is the highest level Analysis Services supports. 1706 is for Power BI and Fabric only, and is the level to choose when you deploy the model through the Power BI XMLA endpoint.

- 为了获得最佳的开发体验，请选中“使用 Workspace 数据库”选项。这要求你拥有一个可用的 Analysis Services 实例，以便将 Workspace 数据库部署到其上。它可以是本地或远程的 SQL Server Analysis Services 实例，也可以是 Azure Analysis Services 实例。单击“确定”后，系统会提示你输入连接字符串，以连接要在其中创建 Workspace 数据库的 Analysis Services 实例。

  [了解有关 Workspace 数据库的详细信息](xref:workspace-mode)。

> [!NOTE]
> 使用 Workspace 数据库时，你可以验证 Power Query（M 表达式），并从 Power Query 表达式导入表架构。你还可以在 Workspace 数据库中刷新和查询数据，从而更轻松地调试和测试你的 DAX 表达式。

模型创建完成后，下一步是添加一个数据源和一些表。

#### 添加数据源和表

在将数据导入到表格模型之前，你必须先设置一个或多个数据源。在 TOM Explorer 中，右键单击“数据源”文件夹，然后选择“创建”。对于使用兼容级别 1400 或更高版本的模型，我们有两个选项：旧版数据源和 Power Query 数据源。想详细了解这两类数据源的差异，可以参阅 [Microsoft Analysis Services 博客](https://docs.microsoft.com/en-us/archive/blogs/analysisservices/using-legacy-data-sources-in-tabular-1400)。

![添加数据源](~/content/assets/images/new-as-model-add-data-source.png)

在此示例中，我们将创建一个 Power Query 数据源，用它从 SQL Server 关系数据库导入几个表。创建数据源后，按 F2 将其重命名，然后使用属性网格配置该数据源，如下图所示：

![设置数据源属性](~/content/assets/images/new-as-model-data-source-properties.png)

在本示例中，我们设置了以下属性：

| 属性                 | 值                      |
| ------------------ | ---------------------- |
| 名称                 | `AdventureWorks`       |
| 协议                 | `tds`                  |
| 数据库                | `AdventureWorksDW2017` |
| 服务器                | `localhost`            |
| AuthenticationKind | `ServiceAccount`       |

点击“保存”（Ctrl+S）。系统会提示你为 Model.bim 文件指定路径和文件名，该文件将保存你迄今为止创建的模型元数据。你也可以改为将模型保存为文件夹结构（文件 > 保存到文件夹...）。如果你计划将模型元数据集成到版本控制环境中，建议使用此方式。如果你使用的是 Workspace 数据库，Tabular Editor 3 还会将元数据同步到已连接的 Analysis Services 实例。

接下来，右键单击“Tables”文件夹并选择“Create > Table”（也可以按 Alt+5），以向模型添加一个新表。为该表命名，在我们的示例中为 `Internet Sales`。展开该表，找到表上的分区，并将以下 M 查询作为分区表达式，以便向表中填充数据：

```M
let
    Source = #"AdventureWorks",
    Data = Source{[Schema="dbo",Item="FactInternetSales"]}[Data]
in
    Data
```

这假设关系型 SQL Server 数据库在“dbo”架构下包含一个名为“FactInternetSales”的表。

![M 分区表达式](~/content/assets/images/new-as-model-m-partition.png)

接下来，右键单击新建的表并选择“更新表架构...”。这样 Tabular Editor 就能根据分区查询自动填充表中的列。

> [!NOTE]
> 如果你未使用 Workspace 数据库，此操作仅在 Tabular Editor 3.1.0 或更高版本中可用。

![架构对比](~/content/assets/images/new-as-model-schema-compare.png)

点击“确定”将列添加到表中。再次点击“保存”（Ctrl+S）。如果你使用的是 Workspace 数据库，可以在刷新操作完成后在服务器上刷新该表，并浏览表中的数据。为此，右键单击该表并选择“刷新表 > 自动（表）”。等待“数据刷新”选项卡上的操作完成，然后右键单击该表并选择“预览”（也可以在 TOM Explorer 中执行），以查看表中的实际数据：

![数据刷新](~/content/assets/images/new-as-model-data-refresh.png)

如果你导入的表是维度表，我们建议将该表主键列的“Key”属性设置为“true”。这样可以更轻松地定义该表与其他表之间的关系，我们稍后会看到这一点。

对要导入到表格模型的每张表，都重复此操作。你无需逐个刷新每个表中的数据——可以直接在模型级别运行刷新操作。

#### 定义关系

当你导入了多张表后，在 Tabular Editor 3 中定义它们之间关系的最简单方法是新建一个图表。选择“文件 > 新建 > 图表”。然后，多选并将表拖到图表视图中，或右键单击表并选择“添加到图表”：

![添加到图表](~/content/assets/images/new-as-model-add-to-diagram.png)

要在两张表之间创建关系，请在事实表上找到外键列，然后将该列“拖动”到维度表的主键列上。在弹出的对话框中，单击“确定”以确认关系设置。

![图表视图](~/content/assets/images/new-as-model-diagram-view.png)

关闭图表视图（不用保存，因为你之后随时都可以重建该图表）。再次按 Ctrl+S 保存模型。现在该添加一些业务逻辑了。如果你使用的是 Workspace Database，现在正适合在模型级别执行一次刷新（automatic 或 calculate），以确保服务器已为这些关系创建相应的支撑结构，从而使模型处于可查询状态。

#### 添加度量值

在 TOM Explorer 中选择一张表，然后按 Alt+1（或选择“创建 > 新建度量值”）将度量值添加到该表。为度量值命名，并为该度量值提供 DAX 表达式。

![添加度量值](~/content/assets/images/new-as-model-add-measure.png)

按 Ctrl+S 保存模型元数据。

如果你使用的是 Workspace Database，现在可以直接在 Tabular Editor 3 中测试新建的度量值。最简单的测试方法是使用 Pivot Grid。选择“文件 > 新建 > Pivot Grid”，然后将刚创建的度量值从 TOM Explorer 拖到网格中。你也可以将列和层次结构从 TOM Explorer 拖到 Pivot Grid 的“筛选器”、“行”或“列”区域，按不同的维度属性对度量值进行切片：

![Pivot Grid](~/content/assets/images/new-as-model-pivot-grid.png)

如果你没有使用 Workspace Database，则必须先将模型部署到某个 Analysis Services 实例，之后才能执行数据刷新并查询模型。

#### 部署 Data model

要将模型元数据部署到任意 Analysis Services 实例，请单击“Model”菜单并选择“Deploy...”。这将启动 Tabular Editor 3 的 Deployment Wizard，它与 Tabular Editor 2.X 的 Deployment Wizard 类似。按照向导各个页面上的说明操作，即可将模型元数据部署到 Analysis Services 的某个实例。你也可以使用 Deployment Wizard 生成 TMSL/XMLA 脚本，然后交由 Analysis Services 服务器管理员手动部署。

![部署](~/content/assets/images/new-as-model-deployment.png)

要刷新并测试已部署的数据库，你可以使用 Microsoft 提供的标准管理工具和客户端工具；也可以使用另一个 Tabular Editor 3 实例（前提是你在已部署模型所在的 Analysis Services 实例上具有管理员访问权限）。

上面的段落很好地说明了为什么要采用前文所述的 Workspace Database 方法。连接到 Workspace 数据库后，你可以在同一个 Tabular Editor 3 实例中完成所有开发操作，包括数据刷新和业务逻辑测试，而无需依赖其他工具。
