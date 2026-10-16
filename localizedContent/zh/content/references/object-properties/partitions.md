---
uid: object-properties-partitions
title: 分区属性
author: Jeroen ter Heerdt
updated: 2026-10-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 分区属性

<!--
SUMMARY: Reference for the properties of partitions (legacy, calculated, M, entity and policy range partitions), incremental refresh policies and data coverage definitions.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍分区属性、增量刷新策略和数据覆盖范围定义。有关大多数对象共有的属性，请参阅 @object-properties-common。

分区用于定义表中一部分数据的来源。除计算组外，每个表至少有一个分区，而大多数表恰好只有一个。每种分区描述其数据来源的方式都不同：

| 类型       | 源类型           | 数据来源                                                              |
| -------- | ------------- | ----------------------------------------------------------------- |
| 旧版（查询）分区 | `Query`       | 针对旧版（提供程序）数据源的原生查询，通常为 SQL。                                       |
| 计算分区     | `Calculated`  | 计算表格的 DAX 表达式。                                                    |
| M 分区     | `M`           | Power Query (M) 表达式。 Power BI 和大多数现代模型都采用这种类型。 |
| 实体分区     | `Entity`      | 一个命名实体，例如 Lakehouse 或 Warehouse 中的 Delta 表。 Direct Lake 表采用这种类型。  |
| 策略范围分区   | `PolicyRange` | 表的增量刷新策略中的一个日期范围。这些分区由引擎自动创建。                                     |

所有类型都共享 [所有分区的属性](#properties-of-all-partitions) 中列出的属性。后续各节列出了各类型特有的属性。

## 所有分区的属性

这些属性适用于每一种分区类型。**属性**视图只显示适用于所选类型的属性。例如，`Query` 只会在旧版分区上显示，`QueryGroup` 只会在 M 分区上显示。如果表只有一个分区，且该分区与表同名，则重命名表时也会重命名该分区。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [错误消息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [状态](xref:object-properties-common#state)

### 数据源

`DataSource` · DataSource · 基本

分区查询所使用的数据源。 Tabular Editor 会在旧式（查询）分区和实体分区中显示此属性，你可以从下拉列表中选择模型中的一个数据源。策略范围分区也会列出此属性，但该处始终为空。

M 分区不使用此属性。它们的 M 表达式会直接指定数据源，例如 `Sql.Database("myserver", "mydb")`，或者引用 Structured数据源或共享表达式。见 @object-properties-data-sources。

### 表达式

`Expression` · string · 基本

用于向分区填充数据的表达式。**属性**视图仅在计算分区上显示此属性，此时保存的是计算表格的 DAX 表达式。在旧式分区上，同一内容显示为 `Query`；在 M 分区上则显示为 `MExpression`。

**TOM Explorer** 不显示计算表格（包括字段参数）或计算组的分区。你可以通过计算表格上的 `Expression` 编辑 DAX 表达式，或者用 @script-edit-hidden-partitions 脚本打开分区的属性。

在 C# Script 中，`Expression` 同样可读取和写入旧式分区、计算分区和 M 分区的表达式。如果在任何其他类型的分区上设置它，例如实体分区，就会引发错误。

### Query

`Query` · string · 基本

引擎为填充分区而发送到旧式数据源的原生查询，例如：

```sql
SELECT * FROM dbo.FactSales WHERE OrderDate >= '2024-01-01'
```

`Query` 仅出现在旧式（查询）分区上。它是 `Expression` 的别名，这两个名称读写的是同一个值。引擎会原样发送该查询，所以要用数据源自己的方言来编写。如果你将一个大表拆分为多个旧式分区，而它们的 `WHERE` 子句彼此重叠或留有空档，某些行就会被加载两次，或者完全不被加载。

在 Tabular Editor 3 中，刷新覆盖配置文件会在单次刷新时替换分区的查询，例如在开发期间只加载前 10,000 行。见 @refresh-overrides。

### 上次处理时间

`RefreshedTime` · DateTime · 元数据 · 只读

引擎上次刷新该分区的日期和时间。可用来确认某次刷新是否已刷新到某个分区，例如在计划刷新之后，或在仅刷新最新分区的增量刷新之后。

如果文件中存有该值，从文件打开的模型会显示该值。只有在连接到服务器或以 @workspace-mode 模式工作时，该值才可靠。

当 **忽略时间戳** 序列化选项开启时（默认设置，参见 @preferences），Tabular Editor 在将模型保存为 `.bim` 文件或 JSON 格式的文件夹时，会省略时间戳。这些时间戳包括 `RefreshedTime` 以及模型及其对象的修改时间。 Tabular Model Definition Language (TMDL) 从不存储时间戳，因此无论该选项如何设置，保存为 TMDL 的模型都不会有 `RefreshedTime` 值。

在 Tabular Editor 3 中，要刷新单个分区，请在 **TOM Explorer** 中右键单击该分区，选择 **Refresh partition**，然后选择刷新类型。 @data-refresh-view 会显示刷新进度。

### DataCoverageDefinition

`DataCoverageDefinition` · DataCoverageDefinition · 选项 · 兼容级别 1603+

分区的可选 [数据覆盖定义](#data-coverage-definition)，用于描述 DirectQuery 分区包含哪些行。当查询只请求该范围之外的行时，引擎会跳过对数据源的查询。混合表格会在保存最近数据的 DirectQuery 分区上使用它，该分区与保存较旧数据的导入分区并存。

在兼容级别 1603 及更高版本中，Tabular Editor 会在处于 `DirectQuery` 或 `Dual` 模式的分区上，以及任何已具有数据覆盖定义的分区上显示此属性。使用该属性的操作可添加或移除此定义，或编辑其表达式。在这些分区上，**表达式编辑器** 会列出数据覆盖定义表达式；如果某个分区尚无定义，在此处输入表达式就会添加一个定义。

### 数据视图

`DataView` · DataViewType · 选项

对于 Analysis Services 中的 DirectQuery 模型：该分区包含全部数据还是仅包含样本数据。样本分区保存从 DirectQuery 表导入的一小部分数据，用于在 Visual Studio 中设计模型。来自客户端工具的查询会使用完整数据。

| 值        | 含义                          |
| -------- | --------------------------- |
| `Full`   | 该分区包含完整数据。                  |
| `Sample` | 该分区保存一部分示例数据，供设计模型时使用。      |
| `默认值`    | 该分区使用模型的 `DefaultDataView`。 |

Tabular Object Model (TOM) 只定义了这三个值。根据 Microsoft 关于 DirectQuery 模式的文档，Visual Studio 模型设计器的 **设为示例** 功能目前不受支持。 Power BI 不使用数据视图，因此在 Power BI 和 Fabric 模型中，将此属性保留为默认值即可。

### 模式

`Mode` · ModeType · 选项

分区的存储模式，用于确定引擎如何访问其中的数据。

| 值             | 含义                                                                                                                                                   |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `导入`          | 数据会在刷新时加载到模型内存中。查询不会发送到数据源。                                                                                                                          |
| `DirectQuery` | 数据保留在数据源中。每个查询都会转换为针对数据源的查询，例如 SQL。                                                                                                                  |
| `双`           | 该分区会作为导入或 DirectQuery 运行，具体取决于在复合模型中哪种方式能生成更优的查询。通常用于同时关联导入模式事实表和 DirectQuery 事实表的维度表。兼容级别 1455+。                                                    |
| `DirectLake`  | 数据直接从 OneLake 中的 Delta 表读取，并按需加载到内存中。仅限 Fabric。与实体分区配合使用。兼容级别 1604+。在不支持 Direct Lake 的 Tabular Editor 版本中不可用。请参阅 @direct-lake-guidance。 |
| `推送`          | 数据通过 Power BI REST API 推送到分区中，与推送语义模型中的方式相同。没有源查询。只有 Power BI 服务支持此功能。                                                                               |
| `默认`          | 该分区使用模型的 `DefaultMode` 设置。参见 @object-properties-model。                                                                                  |

模式按分区设置，而一个表的所有分区通常都使用相同的模式。主要的例外情况是混合表格：增量刷新策略会导入历史分区，并将最新分区保留为 DirectQuery 模式（请参阅[刷新策略](#refresh-policy)中的 `Mode`）。

将表从 `Import` 切换为 `DirectQuery` 会删除其已导入的数据，而且某些功能，例如使用某些 DAX 函数的计算列，在 DirectQuery 中无法使用。要将 Direct Lake 表转换为导入模式，或反向转换，请参阅 @script-convert-dlol-to-import 和 @script-convert-import-to-dlol。

Tabular Editor 允许任意模式组合。保存时，引擎会拒绝它不支持的组合，而 SQL Server Analysis Services 比 Power BI 严格得多。 SQL Server 2025 Analysis Services：

- 会拒绝 `Dual` 分区，并报错 `may not operate in Dual mode`
- 会拒绝在单个表内或跨表混合导入数据与 DirectQuery 的模型，因此无法实现复合模型或混合表格
- 每个表只允许一个 `DirectQuery` 分区

它唯一接受的混合方式，是较早的 DirectQuery 模式：一个 `DirectQuery` 分区，加上 `DataView` 设为 `Sample` 的 `Import` 分区。

Power BI 服务接受同一个表中同时包含 `Import` 和 `DirectQuery` 分区，即使没有刷新策略也是如此。在该服务中，`Dual` 表以及导入表与 DirectQuery 表之间任一方向的关系也都受支持。该服务仍然遵循每个表只允许一个 `DirectQuery` 分区的规则，并且会拒绝表达式未引用数据源的 `DirectQuery` 或 `Dual` 分区，例如用 `#table` 中的字面量数据构建的分区。

### Query Group

`QueryGroup` · QueryGroup · 选项 · 兼容级别 1480+

在 Power BI Desktop 的 Power Query 编辑器中，包含该分区 M 查询的 Query Group（文件夹）。它只用于在该编辑器中组织查询，不影响刷新或字段列表。 Tabular Editor 仅在 M 分区上显示此属性；你可以从下拉列表中选择模型的某个 Query Group，也可以留空。有关 Query Group，请参阅 @object-properties-data-sources。

### 源类型

`SourceType` · PartitionSourceType · 选项 · 只读

分区的类型，会在创建分区时设置。要更改类型，请创建一个正确类型的新分区，再删除旧分区。

| 值                  | 含义                                                   |
| ------------------ | ---------------------------------------------------- |
| `Query`            | 一种旧式分区，包含针对 Provider数据源的原生查询。                        |
| `Calculated`       | 计算表格的分区，由 DAX 表达式填充。                                 |
| `None`             | 该分区没有源。数据会被推送到该分区中，例如在推送式语义模型中。                      |
| `M`                | 带有 Power Query (M) 表达式的 M 分区。     |
| `Entity`           | 一种实体分区，用于读取命名实体，例如 Lakehouse 中的表。 Direct Lake 使用此类型。 |
| `PolicyRange`      | 由增量刷新策略生成的分区。                                        |
| `CalculationGroup` | 计算组表的分区。它不包含源；引擎会根据计算项填充它。                           |
| `Inferred`         | 引擎自行生成查询的分区。兼容级别为 1563+。                             |

TOM 还定义了值 `Parquet`，对应一个 Microsoft 未发布的内部兼容级别，因此它不会出现在你的模型中。

<!-- TODO (not verifiable from TE3 source): which kind of table or model feature creates Inferred partitions. TOM only says "populated by executing a query generated by the system" (CL 1563+), and TE3 has no special handling for it. Same open question as on @object-properties-tables. -->

## 旧版分区和计算分区

旧式（查询）分区和计算分区除了[所有分区的属性](#properties-of-all-partitions)下列出的属性外，没有其他属性。

- **旧式分区**（`Query`）使用 `DataSource` 和 `Query`。它通常与 Provider数据源一起使用，这种情况多见于兼容级别低于 1400 的 Analysis Services 模型。参见 @import-tables。 Best Practice Analyzer (BPA) 规则 @kb.bpa-avoid-provider-partitions-structured 会标记使用 Structured数据源的旧式分区；这种组合不受 Power BI 支持。
- **计算分区**（`Calculated`）属于计算表格，并使用 `Expression`。在计算表格本身编辑 DAX 表达式（参见 @object-properties-tables 中的 `Expression`）。 **TOM Explorer** 不会显示计算表格的分区。要打开其中一个分区，请使用 @script-edit-hidden-partitions 脚本。

## M 分区

M 分区会将 Power Query (M) 表达式的结果填充到表中。它是 Power BI 模型以及兼容级别为 1400 或更高的 Analysis Services 模型中的默认分区类型。 M 表达式通常从源函数（例如 `Sql.Database`）或共享表达式开始，并以要加载的表结束。

### 通用属性

与[所有分区](#properties-of-all-partitions)相同。

### 属性

`Attributes` · string · 选项

与分区源一起存储的额外 M 属性。大多数模型都会将其留空；Power BI Desktop 也会将其留空，即使表设置了增量刷新策略也是如此。

<!-- TODO (not verifiable from TE3 source): which tools or scenarios fill in Attributes on an M partition. -->

### M 表达式

`MExpression` · string · 选项

返回分区数据的 Power Query (M) 表达式。在 **表达式编辑器** 中进行编辑。比如：

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data]
in
    Sales
```

该表达式必须返回一个表，该表的列必须与表中数据列的 `SourceColumn` 值匹配（见 @object-properties-columns）。如果源中的列被重命名或删除，刷新会失败，直到你更新该表的列，例如使用 **更新表架构**（见 @import-tables）。

多个分区共用的部分（如服务器名称）可以放在共享表达式或 M 参数中，然后由各表达式按名称引用。见 @script-create-m-parameter。在 Tabular Editor 3 中，@script-create-and-replace-parameter 还会在所有 M 分区中将该值替换为新参数。

在 Tabular Editor 3 中，@script-format-power-query 脚本会通过外部格式化服务格式化所选分区的 M 表达式。

## 实体分区

实体分区从一个命名对象（即 _实体_）读取其数据。每个 Direct Lake 表都有一个实体分区，指向 Fabric Lakehouse 或 Warehouse 中的某个 Delta 表。共享表达式保存与 Lakehouse 或 Warehouse 的连接，分区通过 `ExpressionSource` 引用它。

见 @direct-lake-sql-model 和 @direct-lake-guidance。在 Tabular Editor 3 中，@import-tables 向导可从 Fabric Lakehouse 或 Warehouse 创建 Direct Lake 表。

### 通用属性

与[所有分区](#properties-of-all-partitions)相同。

### 实体名称

`EntityName` · 字符串 · 选项

分区读取的源对象名称，例如 Lakehouse 中的 Delta 表 `FactSales`。和列的 `SourceColumn` 一样，它必须与源完全一致。在模型中重命名该表不会更改实体名称，因此该表可以使用比源更易读的名称。如果源表被重命名，请更新 `EntityName` 以匹配，否则该分区将在下次对模型执行 framed 或刷新时失败。

<!-- TODO (not verifiable from TE3 source): whether Entity Name is case-sensitive for Direct Lake. -->

如果你在 Power BI 中刷新模型后，对 `EntityName` 的更改被还原，见 @direct-lake-entity-updates-reverting。

### 表达式来源

`ExpressionSource` · NamedExpression · 选项

用于保存与源连接的共享表达式。在 Direct Lake 模型中，这通常是一个名为 `DatabaseQuery` 的共享表达式，这是 Tabular Editor 3 导入向导为其指定的名称。它的 M 表达式取决于 Direct Lake 的类型：

- **SQL 上的 Direct Lake**：`Sql.Database("<SQL endpoint>", "<Lakehouse 或 Warehouse 名称>")`
- **OneLake 上的 Direct Lake**：`AzureStorage.DataLake("https://onelake.dfs.fabric.microsoft.com/<workspace ID>/<item ID>", [HierarchicalNavigation=true])`

Tabular Editor 会通过此共享表达式中的 M 函数区分这两种类型，并将没有表达式源的实体分区视为 SQL 上的 Direct Lake。模型中的所有 Direct Lake 表通常都指向同一个共享表达式。

要让 Direct Lake 模型指向不同的 Lakehouse 或 Warehouse (例如把它从开发环境移到生产环境时)，请更改该共享表达式的 M 表达式。各分区会继续指向它。 @script-convert-dlsql-to-dlol 脚本通过更改同一个 M 表达式，将模型从基于 SQL 的 Direct Lake 切换为基于 OneLake 的 Direct Lake。

### 架构名称

`SchemaName` · 字符串 · 选项 · 兼容级别 1604+

源对象的架构。适用于使用架构的 Lakehouse 和 Warehouse，例如 `dbo` 或 `sales`。如果源没有架构，就将其留空。它与 `EntityName` 一起标识源表。

Microsoft 文档称此属性保留以供将来使用。 Tabular Editor 会在兼容级别 1604 及以上时显示该属性。

<!-- TODO (not verifiable from TE3 source): whether Direct Lake now uses Schema Name for schema-enabled lakehouses, despite the "reserved for future use" description in TOM. -->

## 策略范围分区

策略范围分区包含使用增量刷新的表中的一个日期范围。引擎在应用表的刷新策略时会创建、合并并删除这些分区，例如在 Power BI 服务中执行刷新时，或在 Tabular Editor 中选择 **应用刷新策略** 时。每个分区覆盖一个时间段，例如一天、一个月、一个季度或一年；随着时间推移，较早的时间段会合并为更大的分区。策略范围分区的 M 查询是刷新策略的 `SourceExpression`，并使用该分区的 `Start` 和 `End` 作为 `RangeStart` 和 `RangeEnd` 的值。

参见 @incremental-refresh-about、@incremental-refresh-setup 和 @incremental-refresh-modify。在 Tabular Editor 3 中，@advanced-refresh 对话框会在刷新过程中使用你选择的生效日期来应用刷新策略，以测试该策略在其他时间点的行为。从 Tabular Editor 3 部署时，你可以省略由刷新策略管理的分区。参见 @deployment。

### 通用属性

与 [所有分区](#properties-of-all-partitions) 上的属性相同。

### End

`End` · DateTime · 刷新策略

分区所涵盖日期范围的结束时间。分区包含日期早于 `End` 的行，刷新该分区时，引擎会将该值作为 `RangeEnd` 传入。引擎在应用刷新策略时设置此值。

### 粒度

`Granularity` · RefreshGranularityType · 刷新策略

分区所涵盖时间段的长度。

| 值    | 含义      |
| ---- | ------- |
| `日`  | 一天。     |
| `月`  | 一个自然月。  |
| `季度` | 一个自然季度。 |
| `年`  | 一个自然年。  |
| `无效` | 未设置粒度。  |

最近的时间段通常较小（按天或按月），随着它们移出增量刷新窗口，会合并为更大的时间段（先按季度，再按年）。

### RefreshBookmark

`RefreshBookmark` · string · 刷新策略 · 只读

该值表示此分区上次刷新时，刷新策略的 `PollingExpression` 返回的结果，例如分区范围内的最新修改日期。如果策略未定义 `PollingExpression`，则该值为空。下次刷新时，引擎会再次计算 `PollingExpression`，并且仅在该值发生变化时才刷新分区。在 Power BI Desktop 中，**检测数据更改** 的工作原理也是如此。

该属性在 Tabular Editor 和 TOM 库中为只读，但可以使用 Tabular Model Scripting Language (TMSL) `alter` 命令在分区上设置 `refreshBookmark`，例如将其设为空字符串。在下次应用刷新策略进行刷新时，引擎会将轮询结果与存储的 Bookmark 进行比较，并仅刷新二者不一致的分区。因此，更改 Bookmark 会强制刷新该分区。将 `applyRefreshPolicy` 设为 `false` 时，会在不读取或更新 Bookmark 的情况下刷新分区。

### 开始

`Start` · DateTime · 刷新策略

该分区涵盖的日期范围的起始点。该分区包含日期为 `Start` 或之后的行，刷新该分区时，引擎会将该值作为 `RangeStart` 传入。与 `End` 一样，引擎会在应用刷新策略时设置它。

## 刷新策略

刷新策略定义了引擎如何对表进行分区并以增量方式刷新：保留多少历史数据（_滚动窗口_）、每次刷新更新多少最新数据（_增量窗口_），以及每个分区的 M 查询。引擎使用该策略创建并维护表的[策略范围分区](#policy-range-partition)。

可在该表的 **属性** 视图中的 **增量刷新** 下找到刷新策略。在表上将 **启用** (`EnableRefreshPolicy`) 设置为 `true`，然后展开 **刷新策略** 以编辑以下属性。见 @object-properties-tables 中的 `RefreshPolicy`。

将 `RollingWindowPeriods` 设为 `5`、`RollingWindowGranularity` 设为 `Year`、`IncrementalPeriods` 设为 `10`，并将 `IncrementalGranularity` 设为 `Day` 时，该表会保留五年的历史数据，且每次刷新仅重新加载最近十天的数据。

见 @incremental-refresh-about、@incremental-refresh-policy、@incremental-refresh-setup、@incremental-refresh-modify 和 @incremental-refresh-schema。 @script-implement-incremental-refresh 脚本会根据你选择的日期列，为导入表设置刷新策略，其中包括 `RangeStart` 和 `RangeEnd` 参数。

### 通用属性

- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

### 增量粒度

`IncrementalGranularity` · RefreshGranularityType · 选项

`IncrementalPeriods` 的单位：`Day`、`Month`、`Quarter` 或 `Year`。 `Invalid` 表示该策略尚未配置。该单位也是增量窗口中各分区的大小，例如当设置为 `Day` 时，刷新范围内每天对应一个分区。

### 增量周期

`IncrementalPeriods` · int · 选项

指定引擎每次刷新时从今天往前回溯并刷新的周期数。当 `IncrementalGranularity` 设为 `Day` 且 `IncrementalPeriods` 设为 `10` 时，每次刷新都会重新加载最近十天的数据，而较早的分区保持不变。窗口越大，刷新越慢；窗口过小，则会漏掉对较旧行所做的更改。

### 增量周期偏移量

`IncrementalPeriodsOffset` · int · 选项

以 `IncrementalGranularity` 为单位，相对于今天偏移增量窗口：

- `0` 表示窗口截至当前周期
- 负值会将其移到过去。例如，在 `Day` 下设为 `-1` 时，会刷新到并包括昨天为止，因此表中只保留完整的天数据
- 正值会将窗口移向未来，适用于包含未来日期行的源，例如预测数据

Power BI Desktop 的增量刷新对话框中的 **仅刷新完整天数** 选项会将 `IncrementalPeriodsOffset` 设为 `-1`。

### 模式

`Mode` · RefreshPolicyMode · 选项 · 兼容级别 1565+

决定是否也将最新周期导入，还是将其保留为 DirectQuery 以显示实时数据。

| 值        | 含义                                                                                                                             |
| -------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `Import` | 包括最新分区在内的所有分区都会被导入。数据的新鲜度取决于上次刷新。                                                                                              |
| `Hybrid` | 历史分区会被导入，而引擎会为增量窗口之后的行添加一个 DirectQuery 分区。查询始终能看到源中的最新行，该表也会成为混合表格。仅适用于 Power BI Premium、Premium Per User 和 Power BI Embedded。 |

混合表格会将针对当前周期的查询发送到源。 DirectQuery 分区上的 [数据覆盖范围定义](#data-coverage-definition) 可避免针对当前周期之外的行向源发出查询。 Microsoft 建议与混合表格相关的表使用 Dual 存储模式。

### 策略类型

`PolicyType` · RefreshPolicyType · 选项 · 只读

刷新策略的类型。唯一的值是 `Basic`，即本页介绍的策略，而且你无法在 Tabular Editor 中更改它。

### 轮询表达式

`PollingExpression` · string · 选项

一个可选的 M 表达式。引擎会在刷新分区之前，对增量窗口中的每个分区评估该表达式。它通常返回该分区范围内最新的修改日期或行数。引擎会将结果存储在分区的 `RefreshBookmark` 中，并且仅当该值自上次刷新以来发生变化时才刷新该分区。当该属性为空时，增量窗口中的每个分区每次都会刷新。

该表达式可以像 `SourceExpression` 一样使用 `RangeStart` 和 `RangeEnd`。以下示例返回分区范围内最新的修改日期：

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data],
    InRange = Table.SelectRows(Sales, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd),
    LastModified = List.Max(InRange[ModifiedDate])
in
    LastModified
```

当你在增量刷新对话框中选择 **检测数据更改** 时，Power BI Desktop 会自动填充此属性。在 Tabular Editor 中，选择表，然后从下拉列表中选择 **轮询表达式**，就能在 **表达式编辑器** 中编辑轮询表达式。请参阅 [配置“检测数据更改”](xref:incremental-refresh-modify#configure-detect-data-changes)。

### 滚动窗口粒度

`RollingWindowGranularity` · RefreshGranularityType · 选项

`RollingWindowPeriods` 的单位：`Day`、`Month`、`Quarter` 或 `Year`。 `Invalid` 表示该策略尚未配置。

### 滚动窗口周期数

`RollingWindowPeriods` · int · 选项

除当前未完成的周期外，表还会保留从今天往前回溯计算的多少个完整历史周期。如果将 `RollingWindowGranularity` 设为 `Year`，并将 `RollingWindowPeriods` 设为 `5`，则该表会以年度分区保留过去五个完整年份的数据，另外还会以季度、月或日分区保留当年截至目前的数据。当某个周期移出窗口时，引擎会在下次刷新时删除其分区及其中的数据。

滚动窗口必须大于增量窗口，后者是滚动窗口中最新的一部分。

### 源表达式

`SourceExpression` · 字符串 · 选项

引擎为其创建的每个策略范围分区所使用的查询 M 表达式。它必须在源中的某个日期列上使用 M 参数 `RangeStart` 和 `RangeEnd` 进行筛选；引擎会将这两个参数分别设置为每个分区的 `Start` 和 `End`。比如：

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data],
    InRange = Table.SelectRows(Sales, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd)
in
    InRange
```

一个参数使用 `>=`，另一个参数使用 `<`。如果同时使用 `>=` 和 `<=`，恰好落在边界上的一行会加载到两个分区中。

模型中必须存在 `RangeStart` 和 `RangeEnd`，并且它们是类型为 `DateTime` 的 M 参数（共享表达式）。如果源中的日期列是类似 `20240131` 的整数键，就在筛选步骤中将参数转换为该格式。如果筛选未能折叠到数据源，数据源会为每个分区返回所有行。

策略范围分区不会存储自己的查询；每次刷新任一分区时，都会使用当前的 `SourceExpression`。更改会在下一次刷新时生效，但仅适用于该次刷新会重新处理的分区。应用了刷新策略的刷新(这也是 Power BI 服务执行的方式)只会重新处理增量分区，而历史分区会保留使用旧表达式加载的数据。若要使用新表达式重新加载所有这些分区，请对表执行一次完整刷新，并将 `applyRefreshPolicy` 设为 `false`。

## 数据覆盖定义

数据覆盖定义使用 DAX 表达式来描述某个分区包含哪些行。当查询只请求该分区不可能包含的行时，引擎会用它来跳过相应的 DirectQuery 分区。在没有此定义的混合表格中，即使查询只请求已导入的去年数据，对该表的每次查询也都会通过 DirectQuery 分区查询数据源。

该定义属于单个分区。可通过分区上的 [DataCoverageDefinition](#datacoveragedefinition) 添加。

### 通用属性

- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [错误消息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [状态](xref:object-properties-common#state)

### 表达式

`Expression` · 字符串 · 选项

一个 DAX 表达式，对分区所涵盖的行返回 `TRUE`。例如，对于一个仅包含当前年份数据的 DirectQuery 分区：

```dax
RELATED ( 'Date'[Year] ) = 2026
```

引擎会信任该表达式，不会根据数据对其进行检查。如果该表达式排除了分区实际包含的某一行，查询会在不提示的情况下将该行排除在外，因此当分区的查询发生变化时，请更新该表达式。

要编辑它，请在 **TOM Explorer** 中选择该分区，然后在 **表达式编辑器** 的下拉列表中选择“数据覆盖范围定义”表达式。

保存时，引擎不会验证该表达式。 SQL Server 2025 Analysis Services 会接受所有尝试过的表达式，包括列筛选器、`IN` 列表、`RELATED`，甚至完全不是 DAX 的文本；它还允许在 `Import` 分区上定义此项，而在这种情况下该定义并无用途。部署前请自行检查该表达式。

<!-- TODO (not verifiable from TE3 source): which DAX constructs are honored at query time in Power BI hybrid tables, and that a wrong definition silently leaves rows out of query results (needs a real hybrid table, which SSAS doesn't support). -->

### 分区

`Partition` · 分区 · 选项 · 只读

此数据覆盖范围定义所属的分区。在 **属性** 视图中不会显示它。在 C# Script 中，可以用它从该定义反向获取其所属分区。
