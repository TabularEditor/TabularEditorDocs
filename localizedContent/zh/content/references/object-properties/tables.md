---
uid: object-properties-tables
title: 表属性
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

# 表属性

<!--
SUMMARY: Reference for the properties of tables, calculated tables and calculation group tables.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍语义模型中三种表的属性：常规表、计算表格和计算组表。[表](#table)部分介绍这三类表共有的属性。计算表格和计算组表章节会列出它们新增的属性，并说明 **属性**视图对它们隐藏了哪些表属性。有关大多数对象共有的属性，见 @object-properties-common。

## 表

表以列的形式组织数据行，并包含属于它的度量值和层次结构。常规表从一个或多个分区获取数据，每个分区都包含针对某个数据源的查询，例如 Power Query (M) 表达式或 SQL 查询。分区的模式决定数据的加载方式：导入、DirectQuery 或 Direct Lake。

在 Tabular Editor 3 中，你可以使用 @import-tables 从数据源添加表，并用 @table-preview 查看表数据。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [隐藏](xref:object-properties-common#hidden)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [已更改的属性](xref:object-properties-common#changed-properties)
- [DAX 标识符](xref:object-properties-common#dax-identifier)
- [错误信息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [Lineage tag](xref:object-properties-common#lineage-tag)
- [Source Lineage tag](xref:object-properties-common#source-lineage-tag)
- [翻译后的名称](xref:object-properties-common#translated-names)
- [翻译描述](xref:object-properties-common#translated-descriptions)
- [同义词](xref:object-properties-common#synonyms)
- [在透视中显示](xref:object-properties-common#shown-in-perspective)

### 表格组

`TableGroup` · 字符串 · 基本 · _存储为注释_ (`TabularEditor_TableGroup`)

Tabular Editor 3 的 **TOM Explorer** 中该表所属的表格组。表格组的作用类似于表的文件夹，例如可用来区分事实表、维度表和计算组。将其留空可在顶层显示该表。表格组不能嵌套，Power BI 和 Excel 等客户端工具也会忽略它们。

该组会随模型一起保存在 `TabularEditor_TableGroup` 注释中，因此其他开发人员也会看到相同的分组。**属性**视图仅在 **TOM Explorer** 中启用表格组时显示 `TableGroup`。参见 @table-groups。

在 **TOM Explorer** 中，你还可以右键单击表并选择 **移动到组**，或将表拖到某个表格组上（请参阅 @drag-drop）。 @script-create-table-groups 脚本会根据表的类型和关系将所有表放入相应的组中。

### 启用刷新策略

`EnableRefreshPolicy` · bool · 增量刷新 · _快捷方式_：添加或移除表的 **刷新策略**

为该表启用或关闭增量刷新。将其设置为 `true` 会为该表添加刷新策略，并显示 `RefreshPolicy` 属性。将其设置为 `false` 会删除刷新策略对象，并保留该表现有的分区，包括该策略创建的任何策略范围内的分区。要将该表恢复为具有常规 M 分区的表，请按照[移除增量刷新](xref:incremental-refresh-policy#removing-incremental-refresh-using-tabular-editor)中的步骤操作。

增量刷新仅适用于 Power BI 和 Fabric 模型。在同时满足以下所有条件时，**属性**视图会显示 `EnableRefreshPolicy` 和 `RefreshPolicy`：

- 模型的兼容模式为 Power BI
- 兼容级别为 1450 或更高
- 该表尚无分区，或包含处于导入模式或双重模式的 M 分区或查询分区

对于 Analysis Services 模型，你需要自行创建和管理分区。参见 @incremental-refresh-about 和 @incremental-refresh-setup。脚本 @script-implement-incremental-refresh 会根据你选择的日期列设置刷新策略，其中包括 `RangeStart` 和 `RangeEnd` 参数。

### 刷新策略

`RefreshPolicy` · BasicRefreshPolicy · 增量刷新 · 兼容级别 1450+

该表的增量刷新策略。在 **属性**视图中展开它，以设置要保留多少历史数据、要刷新多少数据、源表达式以及其他策略设置。这些设置在 @object-properties-partitions 的“刷新策略”下有说明。另见 @incremental-refresh-policy。

首次应用该策略时，例如在 Power BI 服务中刷新该表时，引擎会创建该策略范围的分区。要在 Tabular Editor 3 中应用该策略，请在 **TOM Explorer** 中右键单击该表，然后选择 **应用刷新策略**。在 Tabular Editor 2 中，该菜单选项是 **应用刷新策略**。只有在连接到模型且已先保存所有更改后，这两个版本才会应用该策略。

要更改现有策略，参见 @incremental-refresh-modify。在 Tabular Editor 3 中，你可以在 @advanced-refresh 对话框中使用今天以外的生效日期来应用刷新策略，以测试该策略在不同时间点的行为。

### 源

`Source` · string · 元数据 · 只读 · _计算得出_

该表第一个分区查询所使用的旧式（提供程序）数据源名称。如果各分区使用不同的数据源，你只能看到第一个分区的数据源。

只有当第一个分区是查询分区或 M 分区时，**属性**视图才会显示 `Source`。对于 M 分区，该值为空，因为连接是 M 表达式的一部分。在计算表格、计算组表、Direct Lake 表或包含策略范围分区的表中，不会显示 `Source`。

若要列出使用显式（旧版）数据源的表，请运行 @script-show-data-source-dependencies 脚本。

### 源类型

`SourceType` · PartitionSourceType · 元数据 · 只读 · _指向_ 第一个分区 **源类型** 的快捷方式

该表的第一个分区所使用的源类型。对于分区类型不同的表，你看到的是第一个分区的类型。没有分区的表会显示 `None`。

在计算表格和计算组表中，**属性** 视图会隐藏 `SourceType`。在 C# 脚本中，它们会返回 `Calculated` 和 `CalculationGroup`。

| 值                  | 含义                                                                          |
| ------------------ | --------------------------------------------------------------------------- |
| `Query`            | 这些分区会针对旧版（提供程序）数据源运行查询，例如 SQL。                                              |
| `Calculated`       | 该表是计算表格，其数据来自 DAX 表达式。                                                      |
| `None`             | 未定义任何源。数据会推送到该表中，例如在 Power BI 的推送语义模型中。                                     |
| `M`                | 这些分区使用 Power Query (M) 表达式。在 Power BI 模型中最常见。兼容级别 1400+。 |
| `Entity`           | 这些分区会读取命名实体，例如 Lakehouse 或 Warehouse 中的表。 Direct Lake 表使用此类型。兼容级别 1400+。    |
| `PolicyRange`      | 这些分区由增量刷新策略创建。兼容级别 1450+。                                                   |
| `CalculationGroup` | 该表是计算组表。兼容级别 1470+。                                                         |
| `Inferred`         | 引擎生成用于填充分区的查询。兼容级别 1563+。                                                   |

<!-- TODO (not verifiable from TE3 source): which kind of partition uses Inferred. TOM only says "The data in this partition is populated by executing a query generated by the system." -->

### 备用源优先级

`AlternateSourcePrecedence` · int · 选项 · 兼容级别 1460+

引擎在查找可用于回答查询的聚合表时，考虑此表的优先顺序。它仅适用于聚合表，也就是其列的 `AlternateOf` 指向明细表中某一列的表。当多个聚合表都能回答查询时，引擎会使用值最高的那个。默认值为 `0`。

在 Power BI Desktop 中，这对应于 **管理聚合** 中的 **优先级** 设置。要在 Tabular Editor 中设置聚合表，参阅 @user-defined-aggregations。 @script-implement-user-defined-aggregations 脚本会为你选择的事实表自动执行这些步骤。

### 日历

`Calendars` · Calendar 集合 · 选项 · 兼容级别 1701+

在该表上定义的自定义日历。日历会映射日期表中存放年、季度、月、周和日期的列；基于日历的时间智能函数会使用它来处理财务、零售或其他非标准日历。自定义日历需要兼容级别 1701 或更高。参阅 @object-properties-calendars。

在 Tabular Editor 3 中，右键单击某个表并选择 **创建 > 日历...** 以添加日历，然后在 **日历编辑器** 中映射其列。参阅 @calendars。

### 数据类别

`DataCategory` · string · 选项

表所包含的数据类型，供客户端工具使用。在 Power BI 中，`Time` 值会将该表标记为日期表：Power BI 会使用表的日期列（即 `IsKey` 设置为 `true` 的列）进行时间智能分析，并为该表关闭自动日期/时间表。在 Power BI Desktop 中，可通过 **标记为日期表格** 来设置该值。

对于其他所有表，请留空或将其设置为 `Regular`。其他值来自多维模型，只有部分 Excel 功能和较旧的客户端工具会使用它们：`Geography`、`Organization`、`BillOfMaterials`、`Accounts`、`Customers`、`Products`、`Scenario`、`Quantitative`、`Utility`、`Currency`、`Rates`、`Channel` 和 `Promotion`。**属性**视图中的下拉列表会列出这些值以及 `Unknown`，你也可以手动输入一个值。

<!-- TODO (not verifiable from TE3 source): whether an empty value and "Regular" behave the same in the engine and client tools, and which client tools use the values other than Time. -->

在 Tabular Editor 中，你也可以在 @tom-explorer-view 里右键单击该表，然后选择 **标记为日期表格...**。 Best Practice Analyzer (BPA) 规则 @kb.bpa-date-table-exists 会标记没有日期表格的模型。 @script-create-date-table 脚本会根据模型中的日期列创建日期表格，并将 `DataCategory` 设为 `Time`。

### 默认详细信息行表达式

`DefaultDetailRowsExpression` · string · 选项 · 兼容级别 1400+

一个 DAX 表表达式，用于返回用户对该表中的某个度量值执行钻取时看到的行，例如在 Excel 数据透视表中使用 **显示详细信息** 时。它适用于表中所有未定义自身 `DetailRowsExpression` 的度量值（见 @object-properties-measures）。 Power BI 不使用此属性。

此表达式会显示每个销售行的订单号、客户和金额：

```dax
SELECTCOLUMNS (
    Sales,
    "Order", Sales[OrderNumber],
    "Customer", RELATED ( Customer[Name] ),
    "Amount", Sales[Amount]
)
```

见 @detail-rows-expression。在 Tabular Editor 3 中，你可以在 @dax-editor 的 **表达式编辑器** 中编写该表达式，并使用自动补全和参数信息。要删除该表达式，清空该值即可。

### Direct Lake 索引行为

`DirectLakeIndexingBehavior` · DirectLakeIndexingBehavior · 选项 · 预览兼容级别

引擎何时为 Direct Lake 表生成并保存其使用的索引。在刷新期间生成索引可以让刷新后的首次查询更快，而按需生成索引可以让刷新更快。它仅适用于 Direct Lake 模式下的表。

Tabular Object Model (TOM) 目前还没有为此属性分配正式发布的兼容级别，因此在当前版本的 Tabular Editor 3 中，**属性**视图会对所有模型隐藏该属性。

| 值          | 含义                                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------------------ |
| `Default`  | 使用模型的默认设置，可在 @object-properties-model 中通过 **Default Direct Lake Indexing Behavior** 进行设置。 |
| `Auto`     | 如 TOM 库所述，在需要时会在数据加载或查询执行过程中构建内存索引。                                                                    |
| `Full`     | 引擎会在完整刷新、计算刷新以及类型为 indexes 的刷新中构建并保存这些索引。                                                              |
| `Explicit` | 引擎仅在运行类型为 indexes 的刷新时才会构建并保存这些索引。                                                                     |

<!-- TODO (not verifiable from TE3 source): the behavior of each value and which indexes this covers; check the Microsoft documentation once the feature is out of preview. -->

### 从自动聚合中排除

`ExcludeFromAutomaticAggregations` · bool · 选项 · 兼容级别 1572+

当为 `true` 时，Power BI 在构建自动聚合时会排除此表。自动聚合是 Power BI Premium 和 Fabric 面向 DirectQuery 模型提供的一项功能，服务会根据其接收到的查询创建聚合表。可将它用于数据变化过于频繁、以至于缓存聚合难以发挥作用的表。

<!-- TODO (not verifiable from TE3 source): the exact effect. TOM only says "An indication whether the table is excluded from the automatic aggregations feature." Is the table excluded as a source for aggregations, or are queries against it never answered from aggregations? -->

### 从模型刷新中排除

`ExcludeFromModelRefresh` · bool · 选项 · 兼容级别 1480+

当为 `true` 时，如果此表的分区已包含数据，则整个模型的刷新会跳过这些分区。没有数据的分区仍会刷新，因此新建或已清空的表仍会被加载。你仍可通过显式选择该表来刷新它。适用于很少更改或加载成本较高的表，例如大型历史表，或由单独流程填充的表。

在 SQL Server 2025 Analysis Services 中，当该表的分区包含数据时，模型级刷新类型 **Full**、**Automatic**、**Data only** 和 **Calculate** 都会跳过此表。 **Clear values** 确实会清除该表的数据，随后下一次模型刷新会再次加载该表。

在 Tabular Editor 3 中，你可以在 **TOM Explorer** 中右键单击某个表，然后选择 **Refresh table** 来刷新单个表。参见 @refresh-preview-query。

### 分区

`Partitions` · 分区集合 · 选项 · 只读

该表的分区。每个分区都定义了表中部分数据的来源，例如某个 M 表达式；你也可以分别刷新每个分区。大多数表只有一个分区。大型导入表通常每个时间段对应一个分区，这些分区由你创建，或由增量刷新的刷新策略创建。

点击省略号按钮打开集合编辑器，你可以在其中添加、删除和编辑分区。参见 @object-properties-partitions。

只有当表的第一个分区为 M 分区或查询分区时，**属性**视图才会显示 `Partitions`。对于计算表格（包括字段参数）、计算组表、Direct Lake 表以及包含策略范围分区的表，该属性将被隐藏。要查看和编辑计算表格和计算组表的分区，请运行 @script-edit-hidden-partitions 脚本。

### 私有

`IsPrivate` · bool · 选项

当 `true` 时，客户端工具不会显示该表，即使是启用了隐藏对象的开发人员也看不到。 Power BI Desktop 会在“自动日期/时间”功能的日期表模板上设置此属性（表名为 `DateTableTemplate_`，后跟一个 GUID）。它在 Power BI 模型中始终可用；在 Analysis Services 模型中则需要 1400 或更高的兼容级别。

在 Power BI Desktop 中，私有表完全不会出现在 **数据** 窗格中，而隐藏表仍可在其中显示。 SQL Server 2025 Analysis Services 会存储此标志，但不会根据它执行任何操作。在这两种情况下，该表仍会列在引擎返回的架构信息中；你可以用 DAX 查询它，其他表中的度量值也可以使用它。

> [!NOTE]
> `IsPrivate` 和 `IsHidden` 不是安全功能。要保护表，请使用对象级安全性（参见 [对象级安全性](#object-level-security)）。

BPA 规则 @kb.bpa-remove-auto-date-table 会标记“自动日期/时间”创建的 `DateTableTemplate_` 和 `LocalDateTable_` 表，这样你就可以用一个单独的日期表替换它们。

### 集

`Sets` · Set 的集合 · 选项 · 只读 · 兼容级别 1400+

在表上定义的计算集。集是一个命名的 DAX 表达式，返回一组成员，客户端工具可将其显示为预定义的选择项。只有 Power BI 模型支持集：当模型的兼容模式为 Power BI 且兼容级别为 1400 或更高时，**属性**视图会显示 `Sets`。集不会作为对象显示在 **TOM Explorer** 中，因此你需要在此属性的集合编辑器中添加和编辑它们。参见 @object-properties-functions。

<!-- TODO (not verifiable from TE3 source): what calculated sets are used for, and which client tools support them. -->

### 仅显示为变体

`ShowAsVariationsOnly` · bool · 选项

当值为 `true` 时，客户端工具在字段列表中仅通过指向该表的列变体来显示它。 Power BI Desktop 会在自动日期/时间功能创建的日期表上设置此属性（这些表名为 `LocalDateTable_`，后跟 GUID），这些表会在日期列下方显示为日期层次结构。参见 @object-properties-columns 中的 `Variations`。

它在 Power BI 模型中始终可用；在 Analysis Services 模型中则需要 1400 或更高的兼容级别。 SQL Server 2025 Analysis Services 会存储此标志，但不会据此执行任何操作：客户端工具读取的架构信息中仍会列出该表，你仍可用 DAX 查询它，其他表中的度量值也可以使用它。

### 系统托管

`SystemManaged` · bool · 选项 · 兼容级别 1562+

当值为 `true` 时，由引擎或服务创建并删除该表。不要在自己的表上设置此属性，也不要编辑系统托管的表：Tabular Editor 不会阻止你进行这些编辑。

Power BI Desktop 创建的自动日期/时间表不是系统托管的。 Desktop 会在模板表上设置 `IsHidden` 和 `IsPrivate`，并在每个本地日期表上设置 `IsHidden` 和 `ShowAsVariationsOnly`。

<!-- TODO (not verifiable from TE3 source): which features create system-managed tables, for example automatic aggregations. -->

### 对象级安全性

`ObjectLevelSecurity` · 按角色 · 翻译、透视、安全性 · 兼容级别 1400+ · _指向各角色表格权限的快捷方式_

模型中每个角色对该表的对象级安全性（OLS）权限。展开此属性后，可看到每个角色各有一个条目。**属性** 视图仅在模型至少包含一个角色时才显示该属性。 Tabular Editor 会将该权限存储在每个角色的表格权限中。

| 值         | 含义                                               |
| --------- | ------------------------------------------------ |
| `Default` | 未为此角色设置任何权限。该角色的成员可以看到该表。                        |
| `Read`    | 该角色的成员可以看到并查询该表。                                 |
| `None`    | 该表及所有依赖它的内容都会对该角色成员隐藏。对该角色成员而言，引用该表的查询和度量值会返回错误。 |

选择 `None` 时，该表及其元数据对该角色成员而言都不存在，因此所有引用该表的度量值都会对他们报错。参见 @data-security-setup-ols 和 @object-properties-security。要检查 OLS 和行级安全性是否按预期工作，可以在 Tabular Editor 3 中使用身份模拟进行测试。参见 @data-security-testing。

### 行级安全性

`RowLevelSecurity` · 按角色 · 翻译、透视、安全性 · 只读 · _指向每个角色的表格权限的快捷方式_

模型中每个角色里该表的行级安全性（RLS）筛选器。展开该属性即可看到每个角色对应的一个条目。每个条目都是一个 DAX 表达式，它会对角色成员可以看到的行返回 `TRUE`，例如：

```dax
Customer[Country] = "Denmark"
```

该属性本身是只读的，你需要编辑各角色的条目，而这些条目支持多行表达式。只有当模型至少有一个角色时，**属性**视图才会显示该属性。 Tabular Editor 会将该筛选器存储在各角色的表格权限中。

空条目不会对该角色的该表应用筛选。筛选器会沿着关系传播，因此维度表上的筛选器也会筛选与之相关的事实表。参见 @roles-and-rls、@data-security-setup-rls 和 @object-properties-security。

## 计算表格

计算表格的数据来自 DAX 表达式，例如使用 [CALENDAR](https://dax.guide/calendar) 构建的日期表，或对另一张表进行汇总的表。当你刷新该表或模型时，引擎会计算该表达式，并像其他任何导入表一样存储结果。

计算表格拥有 [表](#table) 的所有属性，另加 `Expression`。它只有一个分区，由 Tabular Editor 管理，并且不能配置增量刷新策略。对于计算表格，**属性**视图会隐藏 `Partitions`、`Source`、`SourceType`、`EnableRefreshPolicy` 和 `RefreshPolicy`，并显示 `AlternateSourcePrecedence`。

Power BI 中的字段参数属于计算表格。 @create-field-parameter 脚本会根据你选择的列或度量值创建一个。

### 通用属性

与[表](#table)相同。

### 表达式

`Expression` · string · 选项 · _快捷方式，用于引用_ 该表计算分区的表达式

返回表行的 DAX 表达式。它必须返回一个表，例如：

```dax
ADDCOLUMNS (
    CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2030, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month", FORMAT ( [Date], "mmm" )
)
```

表达式返回的每一列都会成为计算表格列（参见 @object-properties-columns）。以这种方式添加、删除或重命名列，会影响引用该表的其他 DAX 表达式，以及使用其列的层次结构。

在 Tabular Editor 3 中，只要你更改表达式，列就会立即更新。 Tabular Editor 3 会通过自身的 DAX 语义分析解析出这些列；即使你在未连接到 Analysis Services 或 Power BI 的情况下编辑模型文件，也同样适用（参见 @creating-and-testing-dax）。在 Tabular Editor 2 中，只有当你将模型保存到当前连接的数据库时，列才会更新；保存后，它会从服务器重新加载该表的列。在 Tabular Editor 2 中编辑模型文件时，列不会随着表达式变化。

在 **表达式编辑器** 中编辑表达式。在 Tabular Editor 3 中，@dax-editor 的 **表达式编辑器** 提供自动完成和参数信息。在刷新该表以及刷新其依赖的表时，引擎会重新计算该表的数据。更改表达式后，先刷新该表，再在 Report 中使用它。参见 [刷新数据](xref:refresh-preview-query#refreshing-data)。

## 计算组表

计算组表包含一个计算组。它有一列包含计算项的名称，通常还会有一个序号列，用于设置这些项的顺序。 Report 的作者会像使用其他任何列一样使用该列，例如在切片器中；所选的计算项会改变 Report 中度量值的计算方式。有关计算组及其计算项的属性，请参见 @object-properties-calculation-groups。

Microsoft 文档将计算组定位为兼容级别 1500 及以上的功能——这涵盖所有 Power BI 语义模型。从兼容级别 1470 开始，Tabular Editor 3 会显示 **创建 > 计算组**；这是 TOM 添加计算组支持的级别。

除了通用属性外，计算组表还具有以下属性。其中大多数是该表中计算组属性的快捷方式，因为你无法在 **TOM Explorer** 中选中该计算组。对于其他表属性，**属性**视图仅显示 `TableGroup` 和 `DefaultDetailRowsExpression`。计算组不支持明细行表达式、行级安全性或对象级安全性，因此把 `DefaultDetailRowsExpression` 留空。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [隐藏](xref:object-properties-common#hidden)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)
- [已翻译的名称](xref:object-properties-common#translated-names)
- [已翻译的描述](xref:object-properties-common#translated-descriptions)
- [在透视中显示](xref:object-properties-common#shown-in-perspective)

### 表格组

`TableGroup` · string · 基本 · _以注释形式存储_ (`TabularEditor_TableGroup`)

与表上的 [表格组](#table-group) 相同。

### 计算组描述

`CalculationGroupDescription` · string · 基本 · _快捷方式，对应于_ 计算组的 **Description**

这是存储在计算组上的描述，与表自身的 `Description` 分开。客户端工具不会显示它。在 Power BI Desktop 的 **数据** 窗格中将鼠标悬停在计算组表上时，会显示该表的 `Description`；而 Excel 的字段列表不显示任何描述。将面向 Report 作者的文本放在表的 `Description` 中，并用此属性记录给其他开发人员的备注。

### 计算组优先级

`CalculationGroupPrecedence` · int · 基本 · _快捷方式，对应于_ 计算组的 **Precedence**

当查询使用多个计算组时，这是应用计算组的顺序。参见 @object-properties-calculation-groups 中的 `Precedence`。

### 计算组注释

`CalculationGroupAnnotations` · 名称/值对集合 · 元数据 · 只读 · _快捷方式，指向_ 计算组的 **注释**

存储在计算组上的注释。该表也有自己的注释（参见 [注释](xref:object-properties-common#annotations)）。这个属性本身是只读的。点击省略号按钮，打开注释编辑器，你可以在其中添加、更改和删除注释。此功能一次只能作用于一个选定的计算组表。

### 多选或空选择表达式

`MultipleOrEmptySelectionExpression` · 字符串 · 选项 · 兼容级别 1605+ · _快捷方式，指向_ 计算组

这是一个 DAX 表达式：当计算组上的筛选器选择了多个计算项，或者由于筛选器未匹配任何项而未选择任何计算项时，引擎会用它来代替度量值进行求值。使用 [SELECTEDMEASURE](https://dax.guide/selectedmeasure) 引用该度量值。在兼容级别低于 1605 时，**属性**视图会隐藏此属性以及下面的其他选择表达式属性。要删除这个表达式，清空这个值即可。

当这个表达式为空时，这些情况下不会应用计算组，而模型上的 [选择表达式行为](xref:object-properties-model#selection-expression-behavior) 会决定度量值返回什么：

- `Automatic` 或 `NonVisual`：度量值的正常值
- `Visual`：空白值

正常值可能会误导用户。例如，在货币转换计算组中，用户同时选择两种货币时，看到的总计可能既不属于这两种货币中的任何一种。这个表达式返回一条错误信息：

```dax
ERROR ( "Select a single currency." )
```

这个表达式返回空白值：

```dax
BLANK ()
```

在 Tabular Editor 3 中，可在 @dax-editor 的 **表达式编辑器** 中编写该表达式，并获得自动补全和参数信息提示。

### 多选或空选择表达式描述

`MultipleOrEmptySelectionDescription` · 字符串 · 选项 · 兼容级别 1605+ · _快捷方式，指向_ 计算组

这是对多选或空选择表达式的说明，供其他开发人员查看。客户端工具不会向报表作者显示它。

### 多选或空选择格式字符串表达式

`MultipleOrEmptySelectionFormatStringExpression` · 字符串 · 选项 · 兼容级别 1605+ · _计算组的快捷方式_

一个 DAX 表达式，在多选或空选择表达式生效时，返回要使用的格式字符串。它的作用类似于计算项上的 `FormatStringExpression`。在该表达式中，[SELECTEDMEASUREFORMATSTRING](https://dax.guide/selectedmeasureformatstring) 返回度量值的格式字符串。

### 无选择表达式

`NoSelectionExpression` · 字符串 · 选项 · 兼容级别 1605+ · _计算组的快捷方式_

当计算组上没有筛选器时，也就是用户尚未选择计算项时，引擎会用此 DAX 表达式替代度量值进行计算。当该表达式为空时，在未选择任何内容的情况下，度量值将返回其正常值。可用于设置默认计算；用户通过选择计算项即可覆盖该默认计算。无选择表达式要求兼容级别为 1605 或更高版本。

在这个货币换算示例中，销售金额以美元存储，`Currency Rate` 表保存每日汇率。该表达式会将金额转换为 `Currency` 表中所选的货币，而无需用户选择计算项：

```dax
IF (
    SELECTEDVALUE ( 'Currency'[CurrencyName], "US Dollar" ) = "US Dollar",
    SELECTEDMEASURE (),
    SUMX (
        VALUES ( 'Date'[Date] ),
        CALCULATE ( DIVIDE ( SELECTEDMEASURE (), MAX ( 'Currency Rate'[EndOfDayRate] ) ) )
    )
)
```

### 无选择表达式说明

`NoSelectionExpressionDescription` · 字符串 · 选项 · 兼容级别 1605+ · _计算组的快捷方式_

供其他开发者参考的无选择表达式说明。客户端工具不会向 Report 作者显示此项。

### 无选择格式字符串表达式

`NoSelectionFormatStringExpression` · 字符串 · 选项 · 兼容级别 1605+ · _计算组的快捷方式_

一个 DAX 表达式，在无选择表达式生效时，返回要使用的格式字符串。它的作用类似于计算项上的 `FormatStringExpression`。在该表达式中，[SELECTEDMEASUREFORMATSTRING](https://dax.guide/selectedmeasureformatstring) 返回度量值的格式字符串。
