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
> Tabular Editor 3 商业版仅限于 [SQL Server Standard Edition](https://docs.microsoft.com/en-us/analysis-services/analysis-services-features-supported-by-the-editions-of-sql-server-2016?view=asallproducts-allversions#tabular-models) 和 [Azure Analysis Services Basic Tier](https://docs.microsoft.com/en-us/azure/analysis-services/analysis-services-overview#basic-tier)。 Note that certain modeling features are not supported at these tiers.

##### 创建新模型

- 在“文件”菜单中，选择“新建” > “模型……”或按 `CTRL+N`

![New model](~/content/assets/images/new-as-model-new-model.png)

- Provide a name for your model or use the default value. 然后，根据你要面向的 Analysis Services 版本选择相应的兼容级别。 Your options are the following:

  - 1200（Azure Analysis Services / SQL Server 2016+）
  - 1400（Azure Analysis Services / SQL Server 2017+）
  - 1500（Azure Analysis Services / SQL Server 2019+）
  - 1600 (Azure Analysis Services / SQL Server 2022+)
  - 1700 (Azure Analysis Services / SQL Server 2025+)
  - 1706 (Power BI / Fabric)

  1700 is the highest level Analysis Services supports. 1706 is for Power BI and Fabric only, and is the level to choose when you deploy the model through the Power BI XMLA endpoint.

- For the best development experience, check the "Use workspace database" option. 这要求你拥有一个可用的 Analysis Services 实例，以便将 Workspace 数据库部署到其上。 This could be a local or a remote instance of SQL Server Analysis Services or it could be an instance of Azure Analysis Services. When you click OK, you will be prompted to enter the connection string for the Analysis Services instance in which you want the workspace database created.

  [了解有关 Workspace 数据库的详细信息](xref:workspace-mode)。

> [!NOTE]
> 使用 Workspace 数据库，你可以验证 Power Query（M 表达式），并从 Power Query 表达式中导入表架构。 You can also refresh and query data in the workspace database, making it easier to debug and test your DAX expressions.

模型创建完成后，下一步是添加一个数据源和一些表。

#### 添加数据源和表

Before you can import data to your tabular model, you have to set up one or more data sources. Locate the TOM Explorer, right-click on the "Data Sources" folder and choose "Create". For a model that uses compatibility level 1400 or higher, we have two options: Legacy and Power Query data sources. To learn more about the differences between these two types of data sources, [consult the Microsoft Analysis Services blog](https://docs.microsoft.com/en-us/archive/blogs/analysisservices/using-legacy-data-sources-in-tabular-1400).

![Add data source](~/content/assets/images/new-as-model-add-data-source.png)

在此示例中，我们将创建一个 Power Query 数据源，用它从 SQL Server 关系数据库导入几个表。 Once the data source is created, hit F2 to rename it and configure the data source using the Property Grid as seen in the screenshot below:

![Set data source properties](~/content/assets/images/new-as-model-data-source-properties.png)

在本示例中，我们设置了以下属性：

| 属性                 | 值                      |
| ------------------ | ---------------------- |
| 名称                 | `AdventureWorks`       |
| 协议                 | `tds`                  |
| 数据库                | `AdventureWorksDW2017` |
| 服务器                | `localhost`            |
| AuthenticationKind | `ServiceAccount`       |

Hit Save (Ctrl+S). You will be prompted to provide a path and file name for the Model.bim file which will hold the model metadata that you have created so far. You may also save the model as a folder structure instead (File > Save to folder...), which is recommended if you plan to integrate your model metadata into a version controlled environment. If you are using a Workspace Database, Tabular Editor 3 will also synchronize the metadata to the connected instance of Analysis Services.

Next, add a new table to the model by right-clicking on the "Tables" folder and choosing "Create > Table" (you can also hit Alt+5). Give the table a name, in our example `Internet Sales`. Expand the table, locate the partition on the table and provide the following M query as the partition expression, in order to populate the table with data:

```M
let
    Source = #"AdventureWorks",
    Data = Source{[Schema="dbo",Item="FactInternetSales"]}[Data]
in
    Data
```

这假设关系型 SQL Server 数据库在“dbo”架构下包含一个名为“FactInternetSales”的表。

![M partition expression](~/content/assets/images/new-as-model-m-partition.png)

Next, right-click on the newly created table and choose "Update table schema...". This allows Tabular Editor to automatically populate the table columns based on the partition query.

> [!NOTE]
> 如果你未使用 Workspace 数据库，此操作仅在 Tabular Editor 3.1.0 或更高版本中可用。

![Schema compare](~/content/assets/images/new-as-model-schema-compare.png)

Hit "OK" to add the columns to the table. Hit Save again (Ctrl+S). 如果你使用的是 Workspace 数据库，可以在刷新操作完成后在服务器上刷新该表，并浏览表中的数据。 To do so, right-click the table and choose "Refresh table > Automatic (table)". Wait for the operation on the "Data Refresh" tab to complete, then right-click the table and choose "Preview" (you can do so from the TOM Explorer as well), to view the actual data within the table:

![Data refresh](~/content/assets/images/new-as-model-data-refresh.png)

如果你导入的表是维度表，我们建议将该表主键列的“Key”属性设置为“true”。 This makes it easier to define relationships between this and other tables, as we shall see later.

Repeat this process for any table you wish to import to your Tabular model. 你无需逐个刷新每个表中的数据——可以直接在模型级别运行刷新操作。

#### 定义关系

当你导入了多张表后，在 Tabular Editor 3 中定义它们之间关系的最简单方法是新建一个图表。 Choose "File > New > Diagram". Then, multi-select and drag the tables into the diagram view or right-click on the tables and choose "Add to diagram":

![Add to diagram](~/content/assets/images/new-as-model-add-to-diagram.png)

要在两张表之间创建关系，请在事实表上找到外键列，然后将该列“拖动”到维度表的主键列上。 Hit "OK" to confirm the relationship settings in the dialog that appears.

![Diagram view](~/content/assets/images/new-as-model-diagram-view.png)

Close the diagram view (no need to save it, as you can always reconstruct the diagram later). Hit Ctrl+S once again to save the model. Now it's time to add some business logic. 如果你使用的是 Workspace Database，现在正适合在模型级别执行一次刷新（automatic 或 calculate），以确保服务器已为这些关系创建相应的支撑结构，从而使模型处于可查询状态。

#### 添加度量值

Select one of the tables in the TOM Explorer and hit Alt+1 (or choose Create > New Measure) to add a measure to that table. Give the measure a name and provide a DAX expression for the measure.

![Add measure](~/content/assets/images/new-as-model-add-measure.png)

按 Ctrl+S 保存模型元数据。

如果你使用的是 Workspace Database，现在可以直接在 Tabular Editor 3 中测试新建的度量值。 The easiest way to test it is by using a Pivot Grid. Choose File > New > Pivot Grid, then drag the newly created measure from the TOM Explorer into the grid. You can also drag columns and hierarchies from the TOM Explorer into the Filter, Row or Column area of the Pivot Grid, to slice your measure by different dimension attributes:

![Pivot Grid](~/content/assets/images/new-as-model-pivot-grid.png)

如果你没有使用 Workspace Database，则必须先将模型部署到某个 Analysis Services 实例，之后才能执行数据刷新并查询模型。

#### 部署 Data model

To deploy the model metadata to any instance of Analysis Services, click on the "Model" menu and choose "Deploy...". This brings up the Tabular Editor 3 Deployment Wizard which is similar to the Deployment Wizard of Tabular Editor 2.X. Follow the instructions on the various pages of the wizard, to deploy the model metadata to an instance of Analysis Services. You can also use the Deployment Wizard to generate a TMSL/XMLA script, that can be handed over to an Analysis Services server administrator for manual deployment.

![Deployment](~/content/assets/images/new-as-model-deployment.png)

要刷新并测试已部署的数据库，你可以使用 Microsoft 提供的标准管理工具和客户端工具；也可以使用另一个 Tabular Editor 3 实例（前提是你在已部署模型所在的 Analysis Services 实例上具有管理员访问权限）。

The paragraph above provides a good reason for using the Workspace Database approach described above. When connected to a workspace database, you will be able to perform all development operations, including data refresh and testing of business logic within the same instance of Tabular Editor 3, without having to rely on other tools.
