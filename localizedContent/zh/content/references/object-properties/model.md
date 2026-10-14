---
uid: object-properties-model
title: 模型属性
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

# 模型属性

<!--
SUMMARY: Reference for the properties of the model object, such as culture, collation, default storage mode and Direct Lake behavior.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍模型对象的属性。每个条目都给出该属性在 Tabular Object Model (TOM) 中的名称、类型和类别。有关大多数对象共有的属性，请参阅 @object-properties-common。

## 模型

模型是语义模型的根对象。所有表、关系、角色、透视和区域设置都归属于该模型。其属性适用于整个模型，例如用于格式设置的区域设置、默认存储模式，以及会改变 Power BI 和引擎行为的选项。要查看这些属性，请在 **TOM Explorer** 顶部选择 **模型** 节点。

许多模型属性要求最低兼容级别，某些属性仅适用于 Power BI 和 Fabric 模型，或仅适用于 Analysis Services。属性视图会隐藏不适用于当前模型的属性。参见 @update-compatibility-level。

**数据访问选项** 类别中的属性用于控制 Power Query (M) 引擎（也称为 mashup 引擎）在刷新期间如何获取数据。它们仅适用于模型通过 M 加载的数据，也就是 Structured数据源和 M 分区。它们对旧式（提供程序）数据源或 DirectQuery 查询没有影响。三者的 TOM 默认值均为 `false`，而 Power BI Desktop 会在新模型上启用 `LegacyRedirects` 和 `ReturnErrorValuesAsNull`。

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM reference only says these are "options for the M data engine". Confirm that they have no effect on provider data sources and DirectQuery, and that the Power BI service honors all three. -->

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)
- [翻译后的名称](xref:object-properties-common#translated-names)
- [翻译后的描述](xref:object-properties-common#translated-descriptions)

### 数据库

`Database` · 数据库 · 基本 · 只读

包含该模型的数据库。展开该属性可查看和更改数据库级别的设置，例如 **兼容级别**，它决定模型支持的功能和属性。

在 Tabular Editor 3 中，可以在 `Database` 下编辑以下设置：

- **名称** 和 **ID**：数据库的名称和 ID。更改它们不会影响已部署的数据库。
- **兼容级别** 与 **兼容模式**。连接到服务器时，Tabular Editor 3 会拒绝服务器不支持的兼容级别。
- **描述**、**Unicode 字符行为** 和 **可见**。

这些设置为只读，且仅在连接到服务器时才有值：**版本**、**估计大小**（MB）、**最后处理时间**、**最后更新时间**、**最后架构更新时间**、**创建时间戳**、**服务器名称** 和 **服务器版本**。

Tabular Editor 2 也会在 `Database` 下显示相同的设置，但不包括 **Unicode 字符行为**，并且会将 **估计大小** 显示为 `EstimatedSize`。

兼容级别提高后，无法再将其调低。参见 @update-compatibility-level 和 @change-compatibility-mode。 Best Practice Analyzer (BPA) 规则 @kb.bpa-powerbi-latest-compatibility 会标记未使用最新兼容级别的 Power BI 模型。

### 启用 Fast Combine

`FastCombine` · bool · 数据访问选项 · 兼容级别 1400+

当值为 `true` 时，Power Query 会忽略数据源的隐私级别。这与 Power BI Desktop 中的 **“忽略隐私级别并可能提高性能”** 选项相同。

隐私级别会阻止 Power Query 在不同数据源之间传递数据，例如将 Excel 文件中的值通过查询折叠并入 SQL 查询中。启用隐私级别后，刷新可能会变慢；当查询合并多个数据源时，也可能因 `Formula.Firewall` 错误而失败。仅在你信任模型中的所有数据源时才启用此选项。

### 启用旧版重定向

`LegacyRedirects` · bool · 数据访问选项 · 兼容级别 1400+

为 `true` 时，Power Query 会跟随从 HTTPS 地址到 HTTP 地址的重定向，之后数据将以未加密方式传输。 TOM 的默认值为 `false`。 Power BI Desktop 会在新模型中启用此选项。

### 将错误值返回为 Null

`ReturnErrorValuesAsNull` · bool · 数据访问选项 · 兼容级别 1400+

为 `true` 时，刷新期间导致错误的值（例如无法转换为数字的文本）会作为空白值加载。为 `false`（TOM 默认值）时，该错误会导致刷新失败。 Power BI Desktop 会在新模型中启用此选项。设为 `true` 时，错误值会在不报错的情况下变为空白，从而掩盖数据质量问题。

### 排序规则

`Collation` · string · 选项

引擎用于比较和排序文本的规则，以 Windows 排序规则名称表示。排序规则决定比较是否区分大小写以及是否区分重音符号。例如，使用 `Latin1_General_CI_AS`（不区分大小写）时，`apple` 和 `Apple` 在列、关系和 DAX 比较中被视为相同的值。使用 `Latin1_General_CS_AS`（区分大小写）时，它们是不同的值。

为空时，将应用服务器或服务的默认排序规则。如果数据区分大小写，请设置此项，例如产品代码中 `ab1` 和 `AB1` 表示不同的产品；或在区分大小写的 Fabric Warehouse 上使用 Direct Lake 模型时（见 @direct-lake-guidance）。

在创建模型时，或在添加任何表之前，设置排序规则。 TOM API 提供了单独的操作 `UpdateCollation` 和 `UpdateCulture`，用于更改服务器上已存在模型的排序规则和区域设置。在 SQL Server Analysis Services 和 Azure Analysis Services 上，进行此类更改后，必须重新设置数据源凭据。

Tabular Editor 不使用这些操作。如果你在属性视图中更改 `Collation` 并保存到已包含表的数据库中，该更改会被拒绝，并显示错误 "Culture and Collation properties of the Model object may be changed only before any other object has been created"。 SQL Server 2025 Analysis Services、Azure Analysis Services 和 Power BI 服务都会返回此错误；而在 SQL Server 2025 Analysis Services 中，数据库仍会保留旧的排序规则。

### 区域设置

`Culture` · 字符串 · 选项

模型的语言和地区，以区域设置名称表示，例如 `en-US` 或 `de-DE`。引擎会用它来格式化值，例如当你未为 `FORMAT` 函数指定区域设置时，它决定使用的小数分隔符和日期格式；它还会按语言规则对文本进行排序和比较。它也是模型中未翻译的名称和说明所使用的语言。其他语言的翻译则是 `Cultures` 集合中的各个区域设置。在属性视图的列表中选择区域设置。

根据 Microsoft 的说法，一旦某个子对象使用了该区域设置，就无法再更改它。实际上，只要模型包含任何其他对象（例如表格），这一限制就会生效。 Tabular Editor 3 会在属性视图中接受此更改，但引擎会在保存时拒绝，并报错 "Culture and Collation properties of the Model object may be changed only before any other object has been created"。 SQL Server 2025 Analysis Services、Power BI 服务和 Azure Analysis Services 都会返回此错误。若要更改服务器上已存在模型的区域设置，TOM API 提供了单独的 `UpdateCulture` 操作。

### 源查询区域设置

`SourceQueryCulture` · string · 选项 · 兼容级别 1520+

Power Query 在刷新期间用于解释值的区域设置，例如将文本 `1.234,5` 转换为数字，或将 `03/04/2026` 解析为日期。这和 Power BI Desktop 中 **区域设置** 下的 **导入区域设置** 是同一项设置。

当源数据使用的格式与 `Culture` 不同时，就设置这一项；例如，某个 `en-US` 模型加载的是按 `de-DE` 格式编写的 CSV 文件。为空时，Power Query 会使用 `Culture`。设置后，它在刷新期间会优先于 `Culture`。例如，在 `Culture` 设置为 `en-US` 的模型中，当 `SourceQueryCulture` 为空时，`Date.FromText ( "01/02/2024" )` 返回 2 January 2024，当其为 `nl-NL` 时，则返回 1 February 2024。在从 Power BI Desktop 保存的新模型中，它保存的是该文件的 **导入区域设置**，例如 `en-NL`。

### 默认模式

`DefaultMode` · ModeType · 选项

自身 `Mode` 为 `Default` 的分区所使用的存储模式。当此属性更改时，具有显式模式的分区会保留其模式。参见 @object-properties-partitions。

| 值             | 含义                                                                                             |
| ------------- | ---------------------------------------------------------------------------------------------- |
| `Import`      | 刷新时，数据会加载到模型内存中。查询不会提交到数据源。                                                                    |
| `DirectQuery` | 数据保留在数据源中。每个查询都会转换为针对数据源的查询。                                                                   |
| `DirectLake`  | 数据直接从 OneLake 中的 Delta 表读取。仅适用于 Fabric，兼容级别 1604 及更高版本。参见 @direct-lake-sql-model。 |

存储模式类型还可以取值为 `Dual`、`Push` 和 `Default`。在 Tabular Editor 3 中，模型仅支持 `Import`、`DirectQuery` 或 `DirectLake`，并且 `DirectLake` 仅在支持 Direct Lake 的版本中可用。 `Default` 仅适用于分区，在这里它表示“使用模型的 `DefaultMode`”。

在 Analysis Services 中，将 `DefaultMode` 设置为 `DirectQuery`，即可使整个模型成为 DirectQuery 模型。 Power BI Desktop 会在每个分区上设置模式。

要将 Import 表转换为 OneLake 上的 Direct Lake 模式，请使用 @script-convert-import-to-dlol 脚本。

### 默认数据视图

`DefaultDataView` · DataViewType · 选项

对于 Analysis Services 中的 DirectQuery 模型，这是引擎用于响应查询的分区。示例分区保存数据的一个子集，用于在 Visual Studio 中设计 DirectQuery 模型。 `DataView` 设置为 `Default` 的分区会继承此设置。

| 值         | 含义                                                                     |
| --------- | ---------------------------------------------------------------------- |
| `Full`    | 查询会使用 `DataView` 为 `Full` 或 `Default` 的分区。用于内存模型以及已部署的 DirectQuery 模型。 |
| `Sample`  | 在设计模型时，查询会使用 `DataView` 为 `Sample` 或 `Default` 的分区。                    |
| `Default` | 仅对分区有效，表示“使用模型的 `DefaultDataView`”。                                    |

Power BI 不使用数据视图。

SQL Server 2025 Analysis Services 在兼容级别 1700 下支持 `Sample`。包含一个 `DirectQuery` 分区以及若干 `DataView` 为 `Sample` 的 `Import` 分区的表可以成功保存且不会报错。

<!-- TODO (not verifiable from TE3 source): whether the engine still uses sample partitions anywhere at compatibility level 1400 and higher (the save is accepted, the effect isn't observable). -->

### 默认度量值

`DefaultMeasure` · 度量值 · 选项 · 兼容级别 1400+

当查询未指定度量值时，Excel 等 MDX 客户端会使用此度量值。从模型中的度量值列表中选择。留空时，由引擎选择度量值。 Power BI 和 DAX 查询不使用默认度量值。

### 默认 Power BI 数据源版本

`DefaultPowerBIDataSourceVersion` · PowerBIDataSourceVersion · 选项 · 兼容级别 1450+

Power BI 在模型中存储数据源定义时使用的格式。

| 值            | 含义                                                                               |
| ------------ | -------------------------------------------------------------------------------- |
| `PowerBI_V1` | 旧版格式。 M 表达式直接存储在数据源的连接字符串中。                                                      |
| `PowerBI_V2` | 旧版格式。数据源使用共享的 M 表达式。                                                             |
| `PowerBI_V3` | 支持基本分区管理操作的 _增强元数据_ 格式。需要兼容级别为 1465 或更高。自 2020 年起，Power BI Desktop 一直在所有新模型中使用它。 |

Power BI 在将模型从旧格式转换时会使用此属性。通过 XMLA endpoint 编辑模型需要 `PowerBI_V3`。不要更改 Power BI 创建的模型中的该设置。

当你创建兼容级别为 1450 或更高的 Power BI 模型时，Tabular Editor 3 会将此属性设置为 `PowerBI_V3`。对于设置为 `PowerBI_V3` 且兼容模式未知的模型，Tabular Editor 3 会将其视为 Power BI 模型。如果你启用了“将编辑限制为 Power BI 支持的功能”设置并打开 Power BI Desktop 模型或 .pbit 文件，非 `PowerBI_V3` 模型会以只读方式打开。

### 数据源默认最大连接数

`DataSourceDefaultMaxConnections` · int · 选项 · 兼容级别 1510+

刷新期间，引擎同时向单个数据源打开的最大连接数。默认值为 `10`。它适用于 `MaxConnections` 为 `-1` 的数据源，也适用于模型中没有数据源对象的数据源；大多数 Power BI 模型都属于这种情况，因为其数据源是在 M 中定义的。

如果数据源能够承受负载，可以增大此值，以并行刷新更多表或分区；如果数据源较为繁忙，则可以减小此值，以保护它。服务仍可能限制连接数。

<!-- TODO (not verifiable from TE3 source): whether 0 or -1 have a special meaning on this property during refresh. SSAS 2025 accepts both on save without validation. -->

### 数据源变量覆盖行为

`DataSourceVariablesOverrideBehavior` · DataSourceVariablesOverrideBehaviorType · 选项 · 兼容级别 1475+

是否允许刷新命令覆盖模型的数据源变量，例如让刷新指向模型中定义的服务器或数据库之外的其他服务器或数据库。

| 值          | 含义             |
| ---------- | -------------- |
| `Disallow` | 对数据源变量的覆盖会被拒绝。 |
| `Allow`    | 允许覆盖数据源变量。     |

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM reference only says "Queries won't allow / allow data source variables override". Confirm what "data source variables" are and which commands can override them (possibly related to @refresh-overrides). -->

### Direct Lake 行为

`DirectLakeBehavior` · DirectLakeBehavior · 选项 · 兼容级别 1604+

定义当查询无法在 Direct Lake 模式下得到回答时，Direct Lake 模型应采取的行为，例如表超出容量的防护限制、表为 SQL 视图，或 SQL analytics endpoint 强制执行行级安全性时。在这种情况下，模型可&#x4EE5;_&#x56DE;&#x9000;_&#x4E3A;针对 SQL analytics endpoint 的 DirectQuery。

| 值                 | 含义                                   |
| ----------------- | ------------------------------------ |
| `自动`              | 查询会在需要时回退到 DirectQuery。这是默认值。        |
| `DirectLakeOnly`  | 已禁用回退功能。无法在 Direct Lake 模式下运行的查询会报错。 |
| `DirectQueryOnly` | 所有查询都使用 DirectQuery。用它来测试或比较性能。      |

回退通常比 Direct Lake 慢得多，而 `DirectLakeOnly` 会把这种缓慢的回退直接变成错误。这个属性只适用于 SQL 上的 Direct Lake。 OneLake 上的 Direct Lake 绝不会回退到 DirectQuery。参见 @direct-lake-guidance 和 @direct-lake-sql-model。

### 默认 Direct Lake 索引行为

`DefaultDirectLakeIndexingBehavior` · DirectLakeIndexingBehavior · 选项 · 预览兼容级别

引擎如何构建并持久化模型的 Direct Lake 专用索引。 Microsoft 的 TOM 库对这些值的说明如下：

| 值    | 含义                                                |
| ---- | ------------------------------------------------- |
| `自动` | 按照 TOM 库的说明，在需要时在数据加载或查询执行期间构建内存索引。               |
| `显式` | 只有在你通过 _刷新索引_ 操作明确请求时，模型才会构建并持久化该索引。其他刷新类型不会构建索引。 |
| `完全` | 模型会在执行 _完全刷新_、_计算刷新_ 和 _刷新索引_ 操作时构建并持久化索引。        |
| `默认` | 使用模型默认的索引构建和持久化行为。                                |

该属性需要预览版兼容级别，而 Tabular Editor 3 不会在属性视图中显示它。你可以在 C# Script 中设置它。

### 不建议使用复合模型

`DiscourageCompositeModels` · bool · 选项 · 兼容级别 1560+

当为 `true` 时，Report 作者无法基于此模型构建复合模型，也就是说，无法通过 DirectQuery 连接到该模型并将其与其他数据组合。当 Report 作者连接到已发布且此属性设为 `true` 的模型时，Power BI Desktop 不会显示 **对此模型进行更改**，并且该作者无法向该 Report 添加其他数据。这样就只能对该模型使用实时连接。

### 不建议使用隐式度量值

`DiscourageImplicitMeasures` · bool · 选项 · 兼容级别 1470+

当为 `true` 时，Power BI 中的 Report 作者无法创建 _隐式度量值_，也就是把数值列拖到 Visual 中时由 Power BI 自动计算的 SUM 或计数。 Report 作者只能使用模型中定义的度量值，而且列的 `SummarizeBy` 设置在 Report 中不再生效。

包含计算组的模型必须启用此选项，因为计算组仅适用于显式度量值。添加计算组时，Power BI Desktop 和 Tabular Editor 3 会自动启用它。只要模型中包含计算组，你就无法在 Tabular Editor 3 中将其重新设为 `false`。

### 不建议使用 Report 级度量值

`DiscourageReportMeasures` · bool · 选项

当为 `true` 时，Power BI 会提示 Report 作者不要在实时连接到此模型的 Report 中创建 Report 级度量值。

你无法设置此属性。 TOM 库仅在内部兼容级别 (2147483647) 下才允许设置该属性，因此 Tabular Editor 以及任何其他使用 TOM 的工具都会在所有已发布的兼容级别下拒绝此更改。 Tabular Editor 3 不会在属性视图中显示它。

### 强制唯一名称

`ForceUniqueNames` · bool · 选项 · 兼容级别 1465+

当为 `true` 时，度量值不能与模型中任何表里的任何列重名，因此诸如 `[Amount]` 这样的 DAX 引用始终只会指向一个对象。当设为 `false` 时，度量值可以与其他表中的列同名，而列引用需要带上表名，才能与该度量值区分开。

在 SQL Server 2025 Analysis Services 中，引擎允许将其改回 `false`。设为 `false` 时，度量值仍然不能与其所在表中的列同名。当某个度量值与另一张表中的列同名时，引擎会拒绝将其设为 `true`，因此请先重命名这些同名项。比较时不区分大小写。

Power BI Desktop 中的新模型会将 `ForceUniqueNames` 设为 `false`，而且 Power BI Desktop 允许把它改成 `true` 或 `false`。

### 每个查询的最大并行度

`MaxParallelismPerQuery` · int · 选项 · 兼容级别 1569+

对于单个 DAX 查询，引擎并行运行的存储引擎操作的最大数量。这对 DirectQuery 尤其重要，因为每个操作都会作为针对数据源的独立查询执行。当数据源能够处理这些额外查询时，较高的值可让 Visual 呈现更快；较低的值则有助于保护数据源。

默认值为 `0`，表示由服务决定。 Power BI 服务不会验证输入值，任何值都可接受，包括负数以及高达 `100000` 的值。

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM reference describes this as "maximum degree of parallelism for query in formula engine". Confirm that 0 means "let the service decide", the valid range, and whether it applies to Import models too. -->

### 每次刷新的最大并行度

`MaxParallelismPerRefresh` · int · 选项 · 兼容级别 1568+

一次刷新可并行处理的最大任务数，例如表或分区。服务仍可能根据容量资源限制该数量。将其调低可减轻数据源负载；当数据源和容量都能承受时，将其调高可加快刷新速度。

默认值为 `-1`，表示该数量由服务决定。 Power BI 服务不会验证输入值，任何值都可接受。

<!-- TODO (not verifiable from TE3 source): confirm that -1 means "let the service decide", and the valid range. -->

在 Tabular Editor 3 中，你还可以在 [高级刷新对话框](xref:advanced-refresh) 中设置单次刷新操作的最大并行度。

### 元数据访问策略

`MetadataAccessPolicy` · MetadataCategory · 选项 · 兼容级别 1703+

控制具有读取权限的用户在查询模型元数据时可以看到哪些元数据，例如通过 DMV 或 DAX `INFO` 函数。它不适用于具有写入权限或管理员权限的用户。

| 值                        | 含义                               |
| ------------------------ | -------------------------------- |
| `继承`                     | 使用系统定义的行为。                       |
| `基本`                     | 读者无法访问模型中的敏感元数据，例如度量值定义或其他计算表达式。 |
| `CalculationDefinitions` | 读者还可以读取与计算定义相关的元数据。              |

如果模型中的逻辑较为敏感，而读者只需要使用它，就设置为 `基本`。 `MetadataAccessPolicy` 不会隐藏任何数据。要保护数据，请参阅 @roles-and-rls。

<!-- TODO (not verifiable from TE3 source): the meanings above come from Microsoft's TOM library. Confirm what the system-defined behavior for Inherited is (workspace, tenant or service setting) and exactly which metadata Basic hides. -->

### 选择表达式行为

`SelectionExpressionBehavior` · SelectionExpressionBehaviorType · 选项 · 兼容级别 1609+

当用户选择多个计算项或未选择任何计算项，且该计算组没有 `MultipleOrEmptySelectionExpression` 时，模型中的计算组会返回什么，以及当 Visual 按计算组分组时小计会如何处理。

| 值           | 含义                                                                   |
| ----------- | -------------------------------------------------------------------- |
| `自动`        | 默认值。当前与 `NonVisual` 相同。根据 Microsoft 的说明，达到未来某个更高兼容级别的模型将使用 `Visual`。 |
| `Visual`    | 多选或未选中任何项时，返回 `BLANK()`。当 Visual 按计算组分组时，小计会通过在计算组上下文中评估所选度量值来计算。    |
| `NonVisual` | 多选或未选择任何项时，返回 `SELECTEDMEASURE()`。当 Visual 按计算组分组时，小计会被隐藏。           |

见 @object-properties-calculation-groups。

### 值筛选行为

`ValueFilterBehavior` · ValueFilterBehaviorType · 选项 · 兼容级别 1606+

`SUMMARIZECOLUMNS` 如何在同一张表的两个或多个列上应用筛选器。 Power BI 会为几乎每个 Visual 生成 `SUMMARIZECOLUMNS`，因此此属性会影响大多数 Report 查询。

| 值             | 含义                                                                                           |
| ------------- | -------------------------------------------------------------------------------------------- |
| `Automatic`   | 默认值。根据 Microsoft 的说法，它目前表示 `Coalesced`。 Microsoft 计划未来让设置为 `Automatic` 的新模型改用 `Independent`。 |
| `Coalesced`   | 同一表中各列上的筛选器会被合并，只有表中实际存在的组合会保留下来。这称为 _auto-exist_。这可能导致度量值返回意外结果，例如某个度量值使用 `ALL` 移除其中一个筛选器时。 |
| `Independent` | 每个筛选器都会独立应用，不受 auto-exist 影响。                                                                |

更改此属性可能会影响现有 Report 中的数值，因此在更改前，请先测试正在使用的模型所对应的 Report。从 Power BI Desktop 保存的新模型会将 `ValueFilterBehavior` 设置为 `Independent`。

### M 属性

`MAttributes` · string · 选项 · 兼容级别 1535+

作为一个 M 记录，表示承载模型 M 表达式的 Power Query 区段文档的属性。从 Power BI Desktop 保存的新模型会将其留空。

<!-- TODO (not verifiable from TE3 source): which tools or scenarios fill in M Attributes, with an example value. -->

### 存储位置

`StorageLocation` · string · 选项

仅适用于 Analysis Services：这是服务器磁盘上引擎存储模型数据文件的文件夹。为空时，将使用服务器的默认数据文件夹。 Power BI 和 Fabric 不使用此属性。 Azure Analysis Services 接受该值，不会报错。

<!-- TODO (not verifiable from TE3 source): whether SQL Server Analysis Services 2016 and later or Azure Analysis Services still use Storage Location (the value is accepted, the effect isn't observable). -->

### 具有本地更改

`HasLocalChanges` · bool · 选项 · 只读

模型是否存在尚未保存到引擎的更改。这是 TOM 自身的状态，独立于 Tabular Editor 中未保存的更改。对于未连接到引擎的模型，例如你从文件打开的模型，该值始终为 `false`。 Tabular Editor 3 不会在属性视图中显示此属性。你可以在 C# Script 中读取该属性。

在 Tabular Editor 3 中，@unsaved-changes 会显示哪些对象和属性与上次保存的模型版本不同。

### 表达式

`Expressions` · 共享表达式集合 · 选项 · 只读 · 兼容级别 1400+

模型的共享表达式，例如 Power Query 参数，以及供其他查询引用的查询。选择 **...** 以编辑该集合，或者在 **TOM Explorer** 的 **共享表达式** 文件夹中管理它们。参见 @object-properties-data-sources。 @script-create-m-parameter 脚本会通过 C# Script 添加一个 Power Query 参数。

### Query Group

`QueryGroups` · Query Group 集合 · 选项 · 只读 · 兼容级别 1480+

用于对 Power Query 查询和参数进行分组的文件夹，与 Power BI Desktop 的 **查询** 窗格中显示的内容一致。参见 @object-properties-data-sources。

### 绑定信息集合

`BindingInfoCollection` · 绑定信息对象集合 · 选项 · 只读 · 兼容级别 1608+

用于提示 Fabric 为模型中的数据源使用哪个数据连接，例如在将模型部署到另一个 Workspace 后。参见 @object-properties-data-sources 中的 **数据绑定提示**。

### 函数

`Functions` · 函数集合 · 选项 · 只读 · 兼容级别 1702+

模型中的 DAX 用户自定义函数（UDF）。参见 @object-properties-functions 和 @udfs。 BPA 规则 @kb.bpa-udf-use-compound-names 会标记名称中不包含 `.` 或 `_` 分隔符的函数。

### 区域设置

`Cultures` · 区域设置集合 · 翻译、透视、安全性 · 只读

模型的区域设置或翻译。每个区域设置都保存一种语言的已翻译名称、说明和显示文件夹。选择 **...** 以添加或删除区域设置。要编辑翻译，可以使用每个对象上的翻译属性，或者在 Tabular Editor 3 中使用 @metadata-translation-editor。见 @object-properties-perspectives-cultures 和 @how-to-work-with-perspectives-translations。要将某个区域设置的翻译导出为 JSON 文件并重新导入，见 @import-export-translations。

### 透视

`Perspectives` · 透视集合 · 翻译、透视、安全性 · 只读

模型的透视。选择 **...** 以添加或删除透视。要选择每个透视显示哪些对象，可以使用每个对象上的 `InPerspective`，或者在 Tabular Editor 3 中使用 @perspective-editor。见 @object-properties-perspectives-cultures。 BPA 规则 @kb.bpa-perspectives-no-objects 会标记不包含任何可见表的透视。

### 角色

`Roles` · 角色集合 · 翻译、透视、安全性 · 只读

模型的安全角色。角色通过行级和对象级安全性控制谁可以查询模型，以及他们可以看到哪些数据。选择 **...** 以添加或删除角色。见 @object-properties-security 和 @roles-and-rls。如需分步操作说明，请参见 @data-security-setup-rls 和 @data-security-setup-ols。
