---
uid: new-as-model
title: 创建 Analysis Services 模型
author: Daniel Otykier
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
          partial: true
          note: "Limited to SQL Server Standard Edition"
        - edition: Enterprise
          full: true
---
# （教程）创建您的第一个 Analysis Services 模型

本页将引导您使用 Tabular Editor 3 从头开始创建新的 Analysis Services 表格模型。

> [!NOTE]
> Tabular Editor 3 Business Edition 仅限于 [SQL Server Standard Edition](https://docs.microsoft.com/analysis-services/analysis-services-features-supported-by-the-editions-of-sql-server-2016?view=asallproducts-allversions#tabular-models) 和 [Azure Analysis Services Basic Tier](https://docs.microsoft.com/azure/analysis-services/analysis-services-overview#basic-tier)。请注意，这些级别不支持某些建模功能。

## 创建新模型

- 从“文件”菜单中，选择“新建”>“模型…”或按 `CTRL+N` 

![新建模型](~/content/assets/images/new-as-model-new-model.png)

- 为您的模型提供一个名称，或使用默认值。您输入的名称将用于数据库名称、数据库 ID 和模型名称。然后，选择您所针对的 Analysis Services 版本的兼容级别。对话框列出了以下选项：
  - 1200（Azure Analysis Services / SQL Server 2016+）
  - 1400（Azure Analysis Services / SQL Server 2017+）
  - 1500（Azure Analysis Services / SQL Server 2019+）
  - 1600（Azure Analysis Services / SQL Server 2022+）
  - 1700（Azure Analysis Services / SQL Server 2025+）
  - 1706（Power BI/Fabric）

  1700 是 Analysis Services 支持的最高级别。仅将 1706 用于 Power BI 和 Fabric，例如，当您通过 Power BI XMLA endpoint 部署模型时。

- 为获得最佳开发体验，请勾选“使用工作区数据库”选项。这要求您有一个可用的 Analysis Services 实例，您的工作区数据库将部署在该实例上。这可以是 SQL Server Analysis Services 的本地或远程实例，也可以是 Azure Analysis Services 的实例。单击“确定”后，系统将提示您输入要在其中创建工作区数据库的 Analysis Services 实例的连接字符串。

  [了解有关工作区数据库的更多信息](xref:workspace-mode)。

> [!NOTE]
> 使用工作区数据库，您可以验证 Power Query（M 表达式），并从 Power Query 表达式导入表架构。您还可以刷新和查询工作区数据库中的数据，从而更轻松地调试和测试 DAX 表达式。

创建模型后，下一步是添加数据源和一些表。

## 添加数据源和表格

在将数据导入到表格模型之前，您必须设置一个或多个数据源。找到 TOM Explorer，右键单击“数据源”文件夹，然后选择“创建”。对于使用兼容级别 1400 或更高版本的模型，我们有两个选项：旧版数据源和 Power Query 数据源。要详细了解这两种数据源之间的差异，请[参阅 Microsoft Analysis Services 博客](https://docs.microsoft.com/archive/blogs/analysisservices/using-legacy-data-sources-in-tabular-1400)。

![添加数据源](~/content/assets/images/new-as-model-add-data-source.png)

在本例中，我们将创建一个 Power Query 数据源，用于从 SQL Server 关系数据库导入一些表。创建数据源后，按 F2 重命名数据源，然后使用属性网格配置数据源，如下图所示：

![设置数据源属性](~/content/assets/images/new-as-model-data-source-properties.png)

在我们的示例中，我们设置了以下属性：

| 属性 | 值 |
|---|---|
| 名称 | `AdventureWorks` |
| 协议 | `tds` |
| 数据库 | `AdventureWorksDW2017` |
| 服务器 | `localhost` |
| AuthenticationKind | `ServiceAccount` |

点击“保存” (Ctrl+S)。系统将提示您为 Model.bim 文件提供路径和文件名，该文件将保存您迄今为止创建的模型元数据。您也可以将模型另存为文件夹结构（“文件”>“保存到文件夹…”）。如果您计划将模型元数据集成到版本控制环境中，则建议您这样做。如果你使用的是工作区数据库，Tabular Editor 3 还会将元数据同步到连接的 Analysis Services 实例。

接下来，右键单击“Tables”（表格）文件夹并选择“Create > Table”（创建 > 表格）（您也可以按 Alt+5），向模型添加新表。为表命名，在我们的示例中为`Internet Sales`。展开表格，找到表格上的分区，并提供以下 M 查询作为分区表达式，以便向表格中填充数据：

```M
let
    Source = #"AdventureWorks",
    Data = Source{[Schema="dbo",Item="FactInternetSales"]}[Data]
in
    Data
```

这假设关系 SQL Server 数据库在“dbo”架构中包含名为“FactInternetSales”的表。

![M 分区表达式](~/content/assets/images/new-as-model-m-partition.png)

接下来，右键单击新创建的表格，然后选择“更新表格架构...”。这允许 Tabular Editor 根据分区查询自动填充表格列。

> [!NOTE]
> 如果您未使用工作区数据库，则此操作仅在 Tabular Editor 3.1.0 或更高版本中可用。

![架构比较](~/content/assets/images/new-as-model-schema-compare.png)

点击“确定”将列添加到表中。再次按“保存” (Ctrl+S)。如果您正在使用工作区数据库，则可以在服务器上刷新表格，并在刷新操作完成后浏览表格中的数据。为此，请右键单击表格，然后选择“刷新表格 > 自动(表格)”。等待“数据刷新”选项卡上的操作完成，然后右键单击表格并选择“预览”（您也可以从 TOM Explorer 中执行此操作），以查看表格中的实际数据：

![数据刷新](~/content/assets/images/new-as-model-data-refresh.png)

如果您导入的表是维度表，我们建议将表上主键列的“Key”属性设置为“true”。正如我们稍后将看到的那样，这使得定义此表与其他表之间的关系更加容易。

对于要导入到表格模型的任何表，请重复此过程。您不必逐一刷新每个表格中的数据，而是可以在模型层面运行刷新操作。

## 定义关系

导入多张表后，使用 Tabular Editor 3 定义它们之间关系的最简单方法是创建新图表。选择“文件 > 新建 > 图表”。然后，多选并拖动表格到关系图视图，或右键单击表格并选择“添加到关系图” ：

![添加到关系图](~/content/assets/images/new-as-model-add-to-diagram.png)

要创建两个表之间的关系，请在事实表中找到外键列，然后将该列“拖动”到维度表的主键列。点击“确定”，在弹出的对话框中确认关系设置。

![图视图](~/content/assets/images/new-as-model-diagram-view.png)

关闭图表视图（无需保存，因为您可以稍后随时重建图表）。再次按 Ctrl+S 保存模型。现在是时候添加一些业务逻辑了。如果您正在使用工作区数据库，现在是在模型层面执行刷新（自动或计算）的好时机，以确保在服务器上创建关系的支持结构，从而使模型进入可查询状态。

## 添加度量值

在 TOM Explorer 中选择一个表格，然后按 Alt+1（或选择“创建”>“新建度量值”），即可向该表格添加度量值。为度量值命名，并为其提供 DAX 表达式。

![添加度量值](~/content/assets/images/new-as-model-add-measure.png)

按 Ctrl+S 保存模型元数据。

如果您使用的是工作区数据库，现在可以直接在 Tabular Editor 3 中测试您的新度量值。最简单的测试方法是使用 Pivot Grid。选择“文件”>“新建”>“Pivot Grid”，然后将新创建的度量值从 TOM Explorer 拖入网格。您还可以将列和层次结构从 TOM Explorer 拖到 Pivot Grid 的“筛选器”、“行”或“列”区域，以便按不同的维度属性对度量值进行切片：

![Pivot Grid](~/content/assets/images/new-as-model-pivot-grid.png)

如果你未使用工作区数据库，则必须将模型部署到 Analysis Services 实例，然后才能执行数据刷新和查询模型。

## 部署数据模型

要将模型元数据部署到任何 Analysis Services 实例，请点击“模型”菜单，然后选择“部署……”。这将打开 Tabular Editor 3 部署向导，该向导与 Tabular Editor 2.X 的部署向导类似。请按照向导各页面的说明，将模型元数据部署到 Analysis Services 实例。您还可以使用部署向导生成 TMSL/XMLA 脚本，该脚本可以移交给 Analysis Services 服务器管理员进行手动部署。

![部署](~/content/assets/images/new-as-model-deployment.png)

要刷新和测试已部署的数据库，您可以使用 Microsoft 提供的标准管理工具和客户端工具，也可以使用另一个 Tabular Editor 3 实例（假设您对已部署模型所在的 Analysis Services 实例具有管理员访问权限）。

上段提供了使用上述工作区数据库方法的充分理由。连接到工作区数据库后，您将能够在同一个 Tabular Editor 3 实例中执行所有开发操作，包括数据刷新和业务逻辑测试，而无需依赖其他工具。
