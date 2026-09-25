---
uid: direct-lake-guidance
title: Direct Lake 指南
author: Daniel Otykier
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
    - product: Tabular Editor 3
      since: 3.22.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Direct Lake 指南

随着 Tabular Editor 3.22.0 的发布，我们在支持 SQL 上的 Direct Lake 的基础上，新增了对 OneLake 上的 Direct Lake 的支持。 This article provides a short overview of the differences between these two modes, and how they compare to other storage modes available in Power BI semantic models.

## 存储模式概览

下表汇总了 Power BI 语义模型中可用的存储模式：

| 存储模式                     | 说明                                                                                                                     | 推荐使用场景                                                |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 导入                       | 数据将导入语义模型，并存储在模型的内存缓存（VertiPaq）中。                                                                                      | 适用于需要快速查询性能，且可以定期刷新数据的场景。                             |
| DirectQuery              | 数据会在查询时直接从数据源中获取，而不会导入到模型中。 Supports various sources, such as SQL, KQL and even other semantic models. | 适用于需要实时访问数据，或数据量过大而无法装入内存的场景。                         |
| 双重                       | 一种混合模式：引擎会根据查询上下文，在返回已导入的数据与将查询委派给 DirectQuery 之间进行选择。                                                                 | 当你的模型同时包含 DirectQuery 表和导入表（例如使用聚合时），并且存在同时与两者相关联的表时。 |
| 在 OneLake 上的 Direct Lake | 利用 Delta Parquet 存储格式，在需要时可快速将数据换入语义模型内存。                                                                              | 当你的数据已以表或物化视图的形式存在于 Fabric Warehouse 或 Lakehouse 中时。  |
| 在 SQL 上的 Direct Lake     | Direct Lake 的旧版本，使用 Fabric Warehouse 或 Lakehouse 的 SQL analytics endpoint。                                             | 不建议用于新开发（改用在 OneLake 上的 Direct Lake）。                 |

> [!NOTE]
> It is also possible to create tables that contain a mix of partitions in **Import** and **DirectQuery** mode (also known as "hybrid tables"). This is commonly done on large fact tables that require incremental refresh while some data is queried directly from the source. See [this article](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla) for more information.

## 在 OneLake 上的 Direct Lake 与在 SQL 上的 Direct Lake

[OneLake 上的 Direct Lake](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview#key-concepts-and-terminology) 于 2025 年三月推出，作为 SQL 上的 Direct Lake 的替代方案。 With Direct Lake on OneLake, there is no dependency on the SQL endpoint and no fallback to DirectQuery mode. This also means that the [usual restrictions that apply to DirectQuery models](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about#modeling-limitations) do not apply to Direct Lake on OneLake models.

> [!NOTE]
> Direct Lake on OneLake is currently in public preview. 在使用此表存储模式创建语义模型之前，你必须先在 Fabric 管理门户中启用租户设置 **User can create Direct Lake on OneLake semantic models (preview)**。

不过，与 SQL 上的 Direct Lake 一样，仍然存在一些[确实适用的限制](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview#considerations-and-limitations)。 Key limitations include:

- 两种 Direct Lake 模式都不支持计算列。
- Calculated tables cannot reference columns or tables in Direct Lake storage mode. 支持计算组、What-if 参数和字段参数，因为它们会创建不引用 Direct Lake 列的隐式计算表格。
- 不支持将非物化 SQL 视图用作 OneLake 上的 Direct Lake 表的数据源。 Use materialized views or ensure the source Delta table contains the columns you need.
- 在 Direct Lake on OneLake 公开预览期间，不支持将 Lakehouse 中的快捷方式用作数据源。

有关完整且最新的限制列表，请参阅 [Microsoft 的 Direct Lake 注意事项和限制文档](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview#considerations-and-limitations)。

### 复合模型

针对计算列限制，一种变通方案是将 Direct Lake 表与导入表组合起来，创建一个 **复合模型**。 This is supported with Direct Lake on OneLake, but not with Direct Lake on SQL. In a composite model, you typically keep larger fact tables in Direct Lake mode while using Import mode for smaller dimension tables where you need calculated columns or custom groupings.

OneLake 上的 Direct Lake 还支持通过 Tabular Editor 等基于 XMLA 的工具与 DirectQuery 表组合使用。 Import tables can be added through Power BI web modeling, Power BI Desktop (live editing) or through XMLA tools.

> [!NOTE]
> SQL 上的 Direct Lake 不支持复合模型。 You cannot combine Direct Lake on SQL tables with Import, DirectQuery or Dual storage mode tables in the same semantic model. However, you can use Power BI Desktop to create a composite model _on top of_ a Direct Lake on SQL semantic model and extend it with new tables. See [Build a composite model on a semantic model](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models#building-a-composite-model-on-a-semantic-model-or-model) for more information.

## Collation

使用 **OneLake 上的 Direct Lake** 时，模型的排序规则和导入模式一样，默认不区分大小写。

对于 **SQL 上的 Direct Lake** 模型，如果查询不会回退到 DirectQuery，则排序规则不区分大小写。 If the query does fallback, the collation depends on the collation of the source. For a Fabric Warehouse, the collation might be case-sensitive, in which case you should specify a [case-sensitive collation on the model](https://data-goblins.com/power-bi/case-specific).

> [!NOTE]
> You cannot change the collation of a model once the metadata has been deployed to Analysis Services / Power BI. 因此，如果你打算将 SQL 上的 Direct Lake 与区分大小写的 Fabric Warehouse 搭配使用，则必须在部署前先在模型元数据中设置排序规则：
>
> 1. 在 Tabular Editor 3 中创建一个新模型（File > New > Model...）
> 2. 取消选中“使用 Workspace 数据库”
> 3. 将模型的 **Collation** 属性设置为 `Latin1_General_100_BIN2_UTF8`
> 4. 保存模型（Ctrl+S）。
> 5. Now, open the model from the file you just saved. 当系统提示连接到 Workspace 数据库时，请选择“Yes”。
>
> 采用这种方式，模型元数据会从一开始就以正确的排序规则部署。之后你就可以在 SQL 上的 Direct Lake 模式下添加表，而不会遇到排序规则问题。

## 表导入向导

要使用 Tabular Editor 3 的表导入向导添加 Direct Lake 表，请选择 **Microsoft Fabric Lakehouse**、**Microsoft Fabric Warehouse**、**Microsoft Fabric SQL Database** 或 **Microsoft Fabric Mirrored Database** 作为数据源：

![Fabric 表导入向导](../assets/images/import-table-wizard-fabric.png)

登录后，系统会显示一个列表，列出你有权访问的各个 Workspace 中所有可用的 Fabric Lakehouse/Warehouse。 Select the one you want to connect to and hit **OK**:

![表导入向导：选择 Lakehouse](../assets/images/import-table-wizard-select-lakehouse.png)

除非你想指定自定义 SQL 查询，或将表配置为 DirectQuery 模式，否则直接点击 **Next**，从数据源的表/视图列表中选择：

![表导入向导：从列表选择 vs 自定义查询](../assets/images/import-table-wizard-select-vs-custom-query.png)

Select the tables/views you wish to import. Note that **non-materialized views** are not supported in Direct Lake on OneLake mode. Attempting to add such a view to the model will result in an error upon saving the model metadata.

![导入表向导：选择对象](../assets/images/import-table-wizard-select-objects.png)

在最后一页，选择要用哪种模式来配置表分区：

![表导入向导：分区模式](../assets/images/table-import-wizard-partition-mode.png)

可选项包括：

- 在 OneLake 上的 Direct Lake
- 在 SQL 上的 Direct Lake
- 导入 (M)

> [!NOTE]
> 如果你正在处理的模型已经包含表，而该模型又不支持组合不同存储模式的表，那么上述一个或多个选项可能不可用。 For example, if the model contains a table in Direct Lake on SQL mode, you cannot add tables in other modes.

The imported table arrives with its columns already in place, in the same order as in the source. Where Tabular Editor cannot read the schema, because the SQL analytics endpoint of the Lakehouse or Warehouse could not be determined and none was given in the import settings, it reports that and names what it needs instead of creating a table with no columns. There is no follow-up **Update Table Schema** to run after a successful import.

## Inspecting a Direct Lake partition

Selecting a Direct Lake partition in the @tom-explorer-view shows its **Data Coverage Definition Expression** in the **Expression Editor** where one is defined, and leaves the editor empty otherwise. A Direct Lake partition has no query expression of its own, so there is nothing else to show. The same applies to partitions generated by an incremental refresh policy.

## Power Query (M) 表达式

本节会更偏技术性地说明：如果你想在不使用“表导入向导”的情况下，手动将表设置为 Direct Lake 模式，需要如何配置 TOM 对象和属性。

### 在 OneLake 上的 Direct Lake

要手动将表设置为 **OneLake 上的 Direct Lake** 模式，需要执行以下操作：

1. **创建共享表达式**：Direct Lake 表使用“Entity”分区，该分区必须引用模型中的共享表达式。 Start by creating this shared expression, if you do not have it already. Name it `DatabaseQuery`:

![创建共享表达式](../assets/images/create-shared-expression.png)

2. **配置共享表达式**：将你在步骤 1 中创建的表达式的 **Kind** 属性设为“ M ”，并将 **Expression** 属性设置为以下 M 查询，同时将 URL 中的 ID 替换为你的 Fabric Workspace 和 Lakehouse/Warehouse 对应的 ID：

```m
let
    Source = AzureStorage.DataLake("https://onelake.dfs.fabric.microsoft.com/<workspace-id>/<resource-id>", [HierarchicalNavigation=true])
in
    Source
```

3. **创建表和 Entity 分区**：在模型中创建一个新表（Alt+5），然后在 TOM Explorer 中展开该表的分区，并创建一个新的 _Entity 分区_：

![创建 Entity 分区](../assets/images/create-entity-partition.png)

删除你创建表时自动生成的常规导入分区。

4. **配置 Entity 分区**：为 Entity 分区设置以下属性：

| 属性    | 值                                                                                                      |
| ----- | ------------------------------------------------------------------------------------------------------ |
| 姓名    | （推荐）设置为与表相同的名称                                                                                         |
| 实体名称  | （必填）设置为 Lakehouse/Warehouse 中该表的名称                                                                     |
| 表达式来源 | （必填）设置为在步骤 1 中创建的共享表达式，通常为 `DatabaseQuery`                                                             |
| 模式    | （必填）`DirectLake`                                                                                       |
| 架构名称  | （可选）如适用，将其设置为 Lakehouse/Warehouse 中的架构名称。 If not set, the default schema will be used. |

最终结果应如下所示：

![配置实体分区](../assets/images/configure-entity-partition.png)

5. **更新列元数据**：在此阶段，你应该可以使用 Tabular Editor 的 **Update Table Schema** 功能来更新该表的列元数据。 This will automatically retrieve the column names and data types from the Lakehouse/Warehouse:

![更新表架构实体](../assets/images/update-table-schema-entity.png)

或者，手动向表中添加数据列（Alt+4），并为每一列指定 `Name`、`Data Type`、`Source Column` 以及其他相关属性。

> [!NOTE]
> 将 Direct Lake 表添加到模型后，在首次部署元数据后需要手动“刷新”一次。 Otherwise, the table will not contain any data when queried. This refresh only needs to be performed once. Tabular Editor 3 will automatically refresh the table when the model metadata is saved, if the **Auto-refresh when saving new tables** under **Tools > Preferences > Model Deployment > Data Refresh**.

### 在 SQL 上的 Direct Lake

要手动将表设置为 **SQL 上的 Direct Lake** 模式，请按照上文“在 OneLake 上使用 Direct Lake”一节的步骤操作，但在共享表达式中改用以下 M 查询：

```m
let
    database = Sql.Database("<sql-endpoint>", "<warehouse/lakehouse name>")
in
    database
```

将 `<sql-endpoint>` 替换为 [Fabric Warehouse 的 SQL analytics endpoint](https://learn.microsoft.com/en-us/fabric/data-warehouse/query-warehouse) 或 [Lakehouse 的 SQL analytics endpoint](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint) 的连接字符串；将 `<warehouse/lakehouse name>` 替换为相应的 Warehouse 或 Lakehouse 名称。

### 从 Lakehouse / Warehouse 导入

如果你希望在从 Fabric Lakehouse 或 Warehouse 获取数据的同时，将表配置为 **导入** 模式，可按以下步骤操作：

1. **创建表**：在模型中创建一个新表（Alt+5），然后在 TOM Explorer 中展开该表的分区。 By default, you should see a single partition of type "Import" created automatically:

![M 导入分区](../assets/images/m-import-partition.png)

2. **配置 Import 分区**：在 Import 分区上设置以下 M 查询：

```m
let
    Source = Sql.Database("<sql-endpoint>","<warehouse/lakehouse name>"),
    Data = Source{[Schema="<schema-name>",Item="<table/view-name>"]}[Data]
in
    Data
```

将 `<sql-endpoint>` 替换为 [Fabric Warehouse 的 SQL analytics endpoint](https://learn.microsoft.com/en-us/fabric/data-warehouse/query-warehouse) 或 [Lakehouse 的 SQL analytics endpoint](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint) 的连接字符串；将 `<warehouse/lakehouse name>` 替换为相应的 Warehouse 或 Lakehouse 名称。

将 `<schema-name>` 替换为 Warehouse/Lakehouse 中的架构名称，并将 `<table/view-name>` 替换为你要导入的表或视图名称。 Note that tables in Import Mode can use non-materialized views as the data source, since the data is queried through the SQL endpoint during refresh operations.

3. **Update column metadata**: A partition you configured by hand has no columns yet, so use Tabular Editor's **Update Table Schema** feature to retrieve the column names and data types from the Lakehouse/Warehouse. Alternatively, create Data Columns manually (**Alt+4**) and specify the `Name`, `Data Type`, `Source Column` and any other relevant properties for each column. This step belongs to the manual route only. A table added through the Table Import Wizard already has its columns.

## 在不同存储模式之间转换

根据本文中的信息，在 Direct Lake on SQL 与 Direct Lake on OneLake 之间转换很简单，因为你只需要修改 Direct Lake 分区所引用的共享表达式的 M 查询。

如果你想从导入模式转换为 Direct Lake，会稍微复杂一些，因为涉及不同的分区类型。

为简化操作，我们准备了一组 C# Script，可帮助你在不同存储模式之间进行转换：

- [将 Direct Lake on SQL 转换为 Direct Lake on OneLake](xref:script-convert-dlsql-to-dlol)
- [将导入模式转换为 Direct Lake on OneLake](xref:script-convert-import-to-dlol)