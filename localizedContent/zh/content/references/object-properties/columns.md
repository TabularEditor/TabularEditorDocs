---
uid: object-properties-columns
title: 列属性
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

# 列属性

<!--
SUMMARY: Reference for the properties of data columns, calculated columns, calculated table columns, and the Alternate Of and Variation objects that belong to columns.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页列出了三种列的属性，以及属于列的两个对象 Alternate Of 和 Variation 的属性。有关大多数对象共有的属性，参见 @object-properties-common。

一个表包含三种列：

- **数据列**的值来自表的分区，例如来自 Power Query (M) 查询或 SQL 查询
- **计算列**的值来自针对表中每一行计算的 DAX 表达式
- **计算表格列**是计算表格中的列，由该计算表格的 DAX 表达式定义

[所有列的属性](#properties-of-all-columns)介绍了这三种列共有的属性。后续各节列出了各类列特有的属性。

## 所有列的属性

这些属性适用于数据列、计算列和计算表格列。

### 通用属性

- [名称](xref:object-properties-common#name)
- [说明](xref:object-properties-common#description)
- [显示文件夹](xref:object-properties-common#display-folder)
- [隐藏](xref:object-properties-common#hidden)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [已更改属性](xref:object-properties-common#changed-properties)
- [DAX 标识符](xref:object-properties-common#dax-identifier)
- [错误消息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [状态](xref:object-properties-common#state)
- [Lineage tag](xref:object-properties-common#lineage-tag)
- [源 Lineage tag](xref:object-properties-common#source-lineage-tag)
- [翻译后的名称](xref:object-properties-common#translated-names)
- [翻译后的描述](xref:object-properties-common#translated-descriptions)
- [翻译显示文件夹](xref:object-properties-common#translated-display-folders)
- [同义词](xref:object-properties-common#synonyms)
- [在透视视图中显示](xref:object-properties-common#shown-in-perspective)

### 数据类型

`DataType` · DataType · 基本

列值的数据类型。它决定引擎如何存储这些值，以及哪些 DAX 函数和运算符可接受这些值。关系中的两列必须具有相同的数据类型。

| 值           | 含义                                                       |
| ----------- | -------------------------------------------------------- |
| `String`    | 文本。在 Power BI 中称为 **文本**。                                |
| `Int64`     | 64 位整数。在 Power BI 中称为 **整数**。                            |
| `Double`    | 64 位浮点数。在 Power BI 中称为 **小数**。总计可能会显示细微的舍入差异。            |
| `Decimal`   | 具有四位小数的定点数。在 Power BI 中称为 **固定小数位数**。用于货币金额。             |
| `DateTime`  | 日期和时间。 Power BI 会根据格式字符串将其显示为 **日期**、**时间** 或 **日期/时间**。 |
| `Boolean`   | `TRUE` 或 `FALSE`。                                        |
| `Binary`    | 二进制数据，例如图像的字节。 DAX 不能使用二进制值，Power BI 也不会加载二进制列。          |
| `Automatic` | 仅供内部使用。                                                  |
| `Unknown`   | 新列的初始值。将列保存到服务器时，引擎会将其替换为实际的数据类型。                        |
| `Variant`   | 可以是不同类型的值。仅用于度量值。                                        |

**属性视图** 会用更长的名称显示某些值，例如将 `Int64` 显示为 **整数 / 整数 (int64)**，将 `Decimal` 显示为 **货币 / 固定小数位数 (decimal)**。下拉列表会列出表中的所有值，包括 `Automatic`、`Unknown` 和 `Variant`，并接受所有这些值。对于数据列，请选择前七个值之一。

对于数据列，数据类型必须与分区查询返回的数据匹配，否则引擎会在刷新期间转换这些值。如果转换失败(例如在不是数字的文本上进行转换时)，刷新就会失败。在 Tabular Editor 中更改数据类型不会更改分区查询：如果你将某列从 `String` 改为 `Int64`，也要让查询返回整数，例如在 Power Query 中更改类型。

对于计算列和计算表格的列，数据类型由表达式决定。参见 [Data Type Inferred](#data-type-inferred)。

Best Practice Analyzer (BPA) 规则 @kb.bpa-relationship-same-datatype 会标记数据类型不同的列之间的关系。

### 格式字符串

`FormatString` · 字符串 · 基本

客户端工具在显示此列的值时应用的格式，例如 `#,0`、`0.00%` 或 `yyyy-mm-dd`。其语法与 DAX [FORMAT](https://dax.guide/format) 函数相同。 DAX 查询返回未格式化的值。当 Report 作者将数值列拖入 Visual 时，Power BI 会创建隐式度量值，该格式同样适用。

可见的数值列和日期列如果没有格式字符串，就会显示原始值，例如 `1234567.891`，或者显示带时间部分的日期。参见 @kb.bpa-format-string-columns。

### 按列排序

`SortByColumn` · 列 · 基本

同一表中的另一列，其值用于确定此列值的排序顺序。例如，可按 `Month Number` 列对 `Month Name` 列排序，以按日历顺序显示月份。

此列中的每个值在排序列中都必须恰好对应一个值。例如，`January` 必须始终对应月份编号 `1`。如果某个值有多个排序值，则引擎会在刷新或重新计算该列时报告错误。

> [!NOTE]
> 当 Report 按某列分组，而该列设置了排序列时，Power BI 也会按该排序列进行分组。因此，`CALCULATE ( [Sales], REMOVEFILTERS ( 'Date'[Month Name] ) )` 会保留对 `'Date'[Month Number]` 的筛选，并返回不变的结果。移除这两列上的筛选，或移除整个表上的筛选。

C# Script @script-create-date-table 会创建日期表，并为其中的名称列设置 `SortByColumn`。

### 汇总方式

`SummarizeBy` · 聚合函数 · 基本

当 Report 作者在没有度量值的情况下将该列作为值拖入 Visual 时，客户端工具会应用的聚合方式。 Power BI 将这称为 _默认汇总_，并将它即时创建的度量值称为 _隐式度量值_。

| 值               | 含义                                         |
| --------------- | ------------------------------------------ |
| `Default`       | 由客户端工具决定。数值列会求和，其他列不会汇总。                   |
| `None`          | 不要汇总。 Power BI 会将其显示为 **Don't summarize**。 |
| `Sum`           | 值的总和。                                      |
| `最小值`           | 最小值。                                       |
| `最大值`           | 最大值。                                       |
| `Count`         | 值的数量。                                      |
| `平均值`           | 值的平均值。                                     |
| `DistinctCount` | 不同值的数量。                                    |

在 Power BI Desktop 中，设置为 `默认` 的数值列会表现得像 `SUM`：它会在 **数据** 窗格中显示为 Σ 图标，并在添加到 Visual 时显示为该列的 **Sum of**。设置为 `Default` 的文本列不会被汇总。 Excel 会忽略此属性，而数据透视表只能通过度量值进行聚合。

对于不适合求和的数值列，例如键、年份、电话号码或单价，请将其设置为 `None`，否则报表作者可能会得到诸如所有客户 ID 的总和之类的总计。参见 @kb.bpa-do-not-summarize-numeric。

`SummarizeBy` 对 DAX 或显式度量值不起作用。在模型上启用 `DiscourageImplicitMeasures` 时（参见 @object-properties-model），Power BI 不会创建隐式度量值，因此此属性不起作用。 `C# Script` @script-create-sum-measures-from-columns 会为每个所选列创建一个 `SUM` 度量值，并隐藏该列。

### Alignment

`Alignment` · 对齐 · 选项

列值在支持此功能的客户端工具中的水平对齐方式。

| 值        | 含义                            |
| -------- | ----------------------------- |
| `默认`     | 由客户端工具决定。大多数工具会将数字右对齐，将文本左对齐。 |
| `Left`   | 左对齐。                          |
| `Right`  | 右对齐。                          |
| `Center` | 将值居中对齐。                       |

Power BI 会忽略此属性。表格和矩阵 Visual 始终将文本左对齐、数字右对齐；其他对齐方式需要在该 Visual 的格式选项中设置。在连接到模型的 Excel 数据透视表中，右对齐或居中对齐的列也会以默认对齐方式显示。

### 替代项

`AlternateOf` · AlternateOf · 选项 · 兼容级别 1460+

将此列纳入用户定义的聚合中。聚合表保存预先聚合的数据，例如按客户和产品汇总的销售额。 `AlternateOf` 会将此列映射到它所替代的明细表列，并设置值的聚合方式；这样一来，引擎会在可能的情况下使用更小的聚合表来响应查询。

该属性在兼容级别 1460 或更高版本中可用，并在添加 Alternate Of 之前一直为空。在 Tabular Editor 2 和 Tabular Editor 3 中，点击该空属性的 **...** 按钮，或右键单击该属性并选择 **Add Alternate Of**。新的 Alternate Of 包含 `Summarization` `Sum`。展开该属性，设置 [Alternate Of](#alternate-of-1) 中介绍的各项属性。要移除它，请右键单击该属性并选择 **Remove Alternate Of**。分步说明见 @user-defined-aggregations。

C# Script @script-implement-user-defined-aggregations 会为选定的聚合表创建明细表，并在其数值列上配置 `AlternateOf`。

### 数据类别

`DataCategory` · string · 选项

列所包含的值类型，客户端工具会据此以特殊方式处理该列。例如，Power BI 会将类别为 `City` 的列放到地图上，将类别为 `ImageUrl` 的列显示为图像，并将类别为 `WebUrl` 的列显示为可点击的链接。普通列留空即可。

在 Tabular Editor 3 中，下拉列表按字母顺序列出协议定义的所有类别，你也可以输入任何其他值。该值不会经过验证，所以一定要按列表中的拼写输入。 Power BI 使用以下类别：

| 值                 | 在 Power BI 中显示为 | 用途                                            |
| ----------------- | --------------- | --------------------------------------------- |
| `Address`         | 地址              | 街道地址。                                         |
| `City`            | 城市              | 城市名称。                                         |
| `County`          | 县               | 县名称。                                          |
| `StateOrProvince` | 州或省             | 州或省名称。                                        |
| `PostalCode`      | 邮政编码            | 邮政编码或 ZIP 代码。                                 |
| `Country`         | 国家/地区           | 国家/地区名称或代码。                                   |
| `Continent`       | 大洲              | 大洲名称。                                         |
| `Place`           | 地点              | 不适合归入其他类别的地点名称或描述。                            |
| `Latitude`        | 纬度              | 以十进制度数表示的纬度，例如 `51.5072`。                     |
| `Longitude`       | 经度              | 以十进制度数表示的经度，例如 `-0.1276`。                     |
| `WebUrl`          | Web URL         | 用户可点击的链接。                                     |
| `ImageUrl`        | 图像 URL          | 在 Visual 中以图像形式显示的图像 URL。                     |
| `Barcode`         | 条形码             | 供 Power BI 移动应用扫描，用于使用 FILTER 筛选 Report 的条形码。 |

地理类别会告诉地图 Visual 某个值代表哪类位置，例如 `Paris` 是 `City`。

下拉列表将其中两个类别写作 `WebURL` 和 `ImageURL`，且没有 `Barcode` 项。 Power BI 不区分大小写，因此 `ImageUrl` 和 `ImageURL` 都会在表格 Visual 中将该值显示为图像，而 `WebUrl` 和 `WebURL` 都会将其显示为链接。 Tabular Object Model (TOM) 会按你输入的样子精确存储该值。 Power BI 接受 `Barcode`，但表格 Visual 会将该值显示为纯文本；只有 Power BI 移动应用会使用它。

该协议还定义了更多类别，例如 `Id`、`Image`，以及 `Years`、`Months` 等旧版工具使用的时间类别。 Power BI 会忽略其中的大多数。下拉列表中还会列出 `PaddedDateTableDates`，这是 Power BI 使用但协议中未定义的一个类别。 Power BI Desktop 会在其自动日期/时间表的各列上写入这些时间类别：日期列为 `PaddedDateTableDates`，其他列为 `Years`、`Quarters`、`QuarterOfYear`、`Months`、`MonthOfYear` 和 `DayOfMonth`。

<!-- TODO (not verifiable from TE3 source): whether Power BI uses these column categories for anything, or only writes them. -->

要将表标记为日期表，请将表的 `DataCategory` 设置为 `Time`（参见 @object-properties-tables），并将该表日期列的 `IsKey` 设置为 `true`。

### 显示序号

`DisplayOrdinal` · int · 选项

客户端工具可用来为表中列排序的数字，例如 `10`、`20`、`30`。只有相对顺序重要，因此保留间隔便于以后插入列。

Power BI 会忽略它，而在 Power BI Desktop 的 **数据** 窗格中，无论 `DisplayOrdinal` 是什么值，列都会按字母顺序列出。要在该窗格中对列分组，可以使用显示文件夹。

### 编码提示

`EncodingHint` · EncodingHintType · 选项 · 兼容级别 1400+

向引擎提示如何在内存中压缩数值列。如果没有提示，引擎会在首次加载数据时选择一种编码方式，之后在刷新期间也可能重新编码该列，这会耗费时间。有了提示后，引擎会先使用提示的编码方式。

| 值         | 含义                                                   |
| --------- | ---------------------------------------------------- |
| `Default` | 由引擎决定。                                               |
| `Hash`    | 将每个不同的值在字典中只存储一次，并通过其位置来引用。适用于不同值较少，或值之间间隔较大的列，例如键列。 |
| `Value`   | 直接存储值本身，并通过少量算术处理来缩小存储空间。适用于需要聚合且数值彼此接近的数值列，例如数量或金额。 |

引擎仍可能选择不同的编码方式，而文本列始终使用哈希编码。只有在你已经看到(例如在 VertiPaq分析器中)引擎的编码会导致刷新变慢或模型过大时，才设置此提示。

### 分组依据列

`GroupByColumns` · GroupingColumnCollection · 选项 · 只读 · 兼容级别 1400+

每当查询使用此列时，引擎也会按同一表中的这些其他列分组。如果某些行在此列中的值相同，但在某个分组依据列中的值不同，那么这些行仍会保持分开。

Power BI 将此属性用于字段参数。包含字段名称的列会按包含字段引用的列进行分组，这样显示名称相同的两个字段就会保留在不同的行中。参见 @create-field-parameter。

MDX 客户端(如 Excel)会将这些列视为复合键，因此，在数据透视表中，若不同时包含其分组依据的列，就无法放入带有分组列的列。

该属性会显示在兼容级别为 1400 或更高的 Power BI 和 Fabric 模型中。你可以更改集合中的列：在 Tabular Editor 3 中，单击 **...** 按钮，打开一个显示该表其他列的对话框，然后选择要作为分组依据的列。 TOM 会将这些列保存在该列的 `RelatedColumnDetails` 对象中；当你移除最后一列时，Tabular Editor 会删除该对象。

### 在 MDX 中可用

`IsAvailableInMDX` · bool · 选项

引擎是否为该列构建 MDX 查询所需&#x7684;_&#x5C5E;性层次结构_。默认值为 `true`。 Excel 数据透视表使用 MDX，只有当该值为 `true` 时，才能将列放到行区域或列区域中。 Power BI 使用 DAX，不依赖属性层次结构也能正常工作。

对于 MDX 查询不会使用的隐藏列(例如外键和仅用于度量值的列)，将其设置为 `false` 可节省内存并缩短刷新时间。用于层次结构、排序列、变体或日历的列，以及 Excel 用户需要的列，都要保留为 `true`。参见 @kb.bpa-set-isavailableinmdx-false 和 @kb.bpa-set-isavailableinmdx-true-necessary。规则 @kb.bpa-hide-foreign-keys 会标记未隐藏的外键列。

### 已推断数据类型

`IsDataTypeInferred` · bool · 选项

引擎是否自行推导该列的数据类型，并忽略 `DataType` 的值。这主要适用于计算列和计算表格列；它们的数据类型由 DAX 表达式推导而来。

在 Tabular Editor 3 中，若在计算列或计算表格列上将此属性设为 `true`，`DataType` 将为只读；即使未连接到服务器，Tabular Editor 也会在你编辑表达式时根据表达式更新它。将其设为 `false`，即可自行选择数据类型。当你在计算表格列上将其重新设为 `true` 时，`DataType` 会重置为表达式从中取值的列的数据类型。

<!-- TODO (not verifiable from TE3 source): document the effect of this property on data columns. TE3 has no special handling for data columns. -->

### 默认图像

`IsDefaultImage` · bool · 选项

将该列标记为表示表中某一行的图像，例如产品照片。这是 Power View 曾使用的 _表行为_ 设置之一。目前没有任何客户端会使用它：Power View 已停用，Power BI 会忽略它，Excel 数据透视表也会忽略表行为设置。

### 默认标签

`IsDefaultLabel` · bool · 选项

将该列标记为用户用来识别表中某一行的标签，例如产品名称。这是 Power View 曾使用的一项表行为设置。目前没有任何客户端使用它。 Power View 和 Power BI Q&A 都支持过它，但两者现已停用。

### 键

`IsKey` · bool · 选项

将该列标记为表的键，即其值用于标识每一行的列。一个表最多只能有一个键列：当你将某列的 `IsKey` 设为 `true` 时，Tabular Editor 会将该表中其他列的 `IsKey` 设为 `false`，并保持 `IsUnique` 和 `IsNullable` 不变。键列不能包含重复值或空白值，因此如果刷新时加载了重复值，就会失败。

当你在 Power BI 中将某个表标记为日期表时，日期列上的 `IsKey` 会被设置，且该表的 `DataCategory` 为 `Time`。

BPA 规则 @kb.bpa-date-table-exists 会标记以下模型：没有日历、没有 `DataCategory` 为 `Time` 的表，也没有 `DateTime` 键列。

### 可为空值

`IsNullable` · bool · 选项

该列是否可以包含空白值（null）。默认值为 `true`。如果将其设为 `false`，当源返回空白值时，刷新会失败，这可作为数据质量检查。键列始终不允许空白值，无论此属性的值是什么。

### 唯一

`IsUnique` · bool · 选项

此列是否只包含唯一值。引擎会强制执行此设置，重复值会导致数据列刷新失败。对于计算表格中的列，保存操作本身就会失败，因为引擎会立即重新计算该表。错误消息为“表 'Sales' 中的列 'Key' 包含重复值 'a'，而这对于多对一关系中“一”端的列，或用作表主键的列来说都是不允许的”。仅在保证唯一的列上设置它，例如维度表的键。

要查看连接模式下模型中某列的去重值，请运行 C# Script @script-display-unique-column-values。

### 保留唯一行

`KeepUniqueRows` · bool · 选项

这是一个来自 Power View 的表行为设置，用于在此列中的值相同但键不同的情况下，仍将这些行分开显示，例如两个同名客户。当其为 `false` 时，这些行会按值分组。

目前没有任何客户端会遵循此设置。 Power BI 会忽略它。在 SQL Server 2025 Analysis Services 的 Excel 数据透视表中，无论 `KeepUniqueRows` 是 `true` 还是 `false`，两个同名客户都会显示为一行。要把它们分开显示，就让这些值唯一，例如把客户编号加到名称中。

### 源提供程序类型

`SourceProviderType` · string · 选项

此列在数据源中的数据类型，按源本身的术语表示，例如 `nvarchar` 或 `WChar`。在 DirectQuery 模式下，引擎可用它来生成针对源的查询。 Tabular Editor 3 从不为其赋值，即使在导入表时也是如此；因此，只有在你或其他工具设置了它时，它才会有值。大多数模型（包括 Power BI 模型）都会将其留空。

<!-- TODO (not verifiable from TE3 source): confirm which other tools fill in Source Provider Type (for example the Visual Studio table import wizard) and in which format (OLE DB type names or SQL type names). -->

### 字符串索引行为

`StringIndexingBehavior` · IndexingBehavior · 选项 · 兼容级别 1706+

引擎是否会在文本列上构建索引，以及是否会保存该索引以便重启后重用。

| 值          | 含义                                       |
| ---------- | ---------------------------------------- |
| `Off`      | 不生成索引。                                   |
| `Auto`     | 默认选项。在需要时生成索引，但不保存。                      |
| `Explicit` | 仅当运行 `RefreshIndex` 类型的刷新时，才会生成并保存索引。    |
| `Full`     | 在完全刷新、重新计算或执行 `RefreshIndex` 刷新时生成并保存索引。 |

在支持 1706 兼容级别的 Power BI Desktop 中，引擎接受 `Off` 和 `Auto`，并拒绝 `Explicit` 和 `Full`，同时报错“Persist String Index feature is disabled”。较新的 TOM 库版本仅从 1707 兼容级别开始允许使用 `Auto` 以外的值。

<!-- TODO (not verifiable from TE3 source): document what the string index is used for (text search such as CONTAINSSTRING?) and when Explicit and Full become available. -->

### 全文索引行为

`FullTextIndexingBehavior` · IndexingBehavior · 选项 · 兼容级别 1708+

引擎是否在文本列上生成全文索引并将其保存。全文索引支持 DAX 函数 `TEXTCONTAINS` 和 `TEXTSIMILARITY`。默认值为 `Off`。

| 值          | 含义                                    |
| ---------- | ------------------------------------- |
| `Off`      | 默认选项。不生成全文索引。                         |
| `Auto`     | 对于全文索引，TOM 库未对该值作出说明。                 |
| `Explicit` | 仅当运行 `RefreshIndex` 类型的刷新时，才会生成并保存索引。 |
| `Full`     | 在刷新期间生成并保存索引。                         |

<!-- TODO (not verifiable from TE3 source): what Auto does for full-text indexing, and which engines support compatibility level 1708. -->

### 表详细信息显示位置

`TableDetailPosition` · int · 选项

将该列添加到表&#x7684;_&#x9ED8;认字段&#x96C6;_&#x4E2D;。默认字段集是指当用户将整个表添加到 Report，或向下钻取查看详细信息时，客户端工具所显示的列集合。将该值设为正数时会包含该列，列会按该数字的升序显示。默认值为 `-1`，表示不包含该列。 Power View 和 Excel 中的 **显示详细信息** 使用默认字段集。

Excel 不再将其用于钻取：在 Excel 数据透视表中，无论 `TableDetailPosition` 如何设置，**显示详细信息** 都会返回该表的列。要选择钻取时显示的列，请在表上设置 `DefaultDetailRowsExpression`（参见 @object-properties-tables），或在度量值上设置 `DetailRowsExpression`（参见 @object-properties-measures）。

### 变体

`Variations` · VariationCollection · 选项 · 只读

此列的变体。变体是指当用户选择此列时，客户端工具显示的另一项内容。 Power BI 将变体用&#x4E8E;_&#x81EA;动日期/时&#x95F4;_&#x529F;能。参见 [Variation](#variation)。

### 对象级安全性

`ObjectLevelSecurity` · ColumnOLSIndexer · 翻译、透视和安全性 · 只读 · 兼容级别 1400+ · _快捷方式_：用于访问每个角色的列权限

此列在模型各个角色中的对象级安全性（OLS）设置。当模型至少有一个角色时，此属性会在兼容级别达到 1400 或更高时显示。展开后，可看到每个角色各有一项，其值为以下之一：

| 值         | 含义                                                   |
| --------- | ---------------------------------------------------- |
| `Default` | 没有列专用设置。该列遵循其表在该角色中的设置。在 TOM 中，该角色未针对该列定义列权限。        |
| `None`    | 该角色中的用户无法查看或查询该列。对他们来说，该列就像不存在一样，使用该列的 Visual 会显示错误。 |
| `读取`      | 该角色中的用户可以查看并查询该列。                                    |

你可以为每个角色更改该值。选择 `无` 或 `读取` 时，Tabular Editor 会将该列的列权限添加到角色在该列所属表上的表格权限中；如果该角色尚未设置该表格权限，则会创建一个。选择 `默认` 时，Tabular Editor 会移除列权限。你也可以在角色的 **OLS 列权限** 下设置相同的值（参见 @object-properties-security）。参见 @data-security-setup-ols。

你不能将一个角色的行级安全性与另一个角色的对象级安全性组合使用。如果用户同时属于这种角色组合，引擎会在查询时返回错误。

在 SQL Server 2025 Analysis Services 中观察到的情况是，这些设置会按以下方式组合：

- `默认` 遵循表格设置：当角色的表格权限为 `读取` 时，该列可见；当其为 `无` 时，整个表都会被隐藏，包括此列
- 列的限制不能比其所属表更宽松；当表为 `无` 时，引擎会拒绝将该列设置为 `读取`
- 当用户属于多个都使用 OLS 的角色时，权限会累加；只要其中任一角色允许，用户就能看到表或列
- 同一角色中的行级安全性和对象级安全性会协同工作。例如，即使角色通过 OLS 隐藏了某个表，该表上的行筛选仍会筛选相关表

## 数据列

数据列从表的分区获取其值；在 Power BI 模型中，这通常是一个 Power Query (M) 查询。该列具有[所有列的属性](#properties-of-all-columns)中列出的属性，以及下面这一项。

在 Tabular Editor 3 中，@import-tables 向导会创建数据列，并设置其数据类型和源列映射，而 **更新表架构** 会在源发生变化时更新这些列。

### 源列

`SourceColumn` · 字符串 · 基本

此列获取值所依据的分区查询结果中的列名。它必须与查询返回的列名一致。如果不一致，例如有人在 Power Query 中重命名了列，刷新就会失败。

该列的 `Name` 与 `SourceColumn` 是彼此独立的，因此你可以在不更改查询的情况下重命名模型中的列，反之亦然。在 Tabular Editor 中重命名列不会更改 `SourceColumn`。启用公式修复后，Tabular Editor 会更新引用已重命名列的 DAX 表达式。参见 @formula-fix-up-dependencies。

每个数据列都需要对应的源列。参见 @kb.bpa-data-column-source。

当源中的某一列被重命名时，Tabular Editor 3 中的 **更新表架构** 会将其报告为删除了一列并新增了一列。将两者合并为一次 `SourceColumn` 更新，以保持使用该列的 DAX 公式继续正常工作。

## 计算列

计算列的值来自一个 DAX 表达式，该表达式会在表刷新时针对表中的每一行计算一次。引擎会像存储数据列的值一样存储结果，这会占用内存，但能让这些值更快被读取。对于需要切片、筛选或分组的值，使用计算列；对于只用于聚合的值，使用度量值。

该列具有 [所有列的属性](#properties-of-all-columns) 中的属性，以及以下属性。要在 Tabular Editor 3 中添加计算列，参见 @creating-and-testing-dax。

### 表达式

`Expression` · string · 选项

用于计算每一行值的 DAX 表达式，例如：

```dax
Sales[Quantity] * Sales[Unit Price]
```

该表达式会在 _行语境_ 中计算，因此会直接引用当前行的各列。若要从相关表获取值，请使用 [RELATED](https://dax.guide/related)，例如 `RELATED ( Product[Category] )`。

当表刷新时，或者当你更改表达式并将模型保存到已连接的服务器时，引擎会重新计算该列。在 Tabular Editor 3 中，你可以在 @dax-editor 的 **表达式编辑器** 中编辑该表达式。 @table-preview 会显示计算后的值；如果该列必须先重新计算，则显示 **（需要计算）**。

### 表达式上下文

`ExpressionContext` · ExpressionContext · 选项 · 兼容级别 1705+

该列的值是对所有人都相同，还是按用户分别计算。

| 值             | 含义                                         |
| ------------- | ------------------------------------------ |
| `Standard`    | 默认选项。该列会在刷新期间计算，并且每一行对所有用户的值都相同。           |
| `UserContext` | 该列按用户计算，并且表达式可以调用 `USERPRINCIPALNAME` 等函数。 |

常规计算列、计算表格、行级安全性筛选器和关系都不能使用用户上下文列。参见 @user-context-calculated-columns。

## 计算表格列

计算表格列是计算表格中的列。该表的 DAX 表达式定义了存在哪些列、它们的数据类型及其值；你可以通过更改该表达式来添加或删除列。

你一更改表达式，Tabular Editor 3 就会分析它，并据此添加、删除和更新列。这一过程无需连接到服务器，因此即使你离线编辑模型，这些列也会保持最新。 Tabular Editor 2 仅会在你将模型保存到所连接的数据库时更新这些列：保存后，它会从服务器重新加载该表的列。在 Tabular Editor 2 中编辑模型文件时，这些列会保持原样；你可以通过 **新建 > 计算表格列** 添加一列，但不能删除它们。

你可以更改列的显示属性，例如 `FormatString`、`IsHidden` 和 `SortByColumn`。要重命名该列，先将 `IsNameInferred` 设置为 `false`。此列具有 [所有列的属性](#properties-of-all-columns) 中列出的属性，以及下面这些属性。

### 源列

`SourceColumn` · string · 基本 · 只读

这是计算表格表达式结果中的列名，此列从该列获取值。 Tabular Editor 3 会在分析表达式时设置该属性，而在模型保存到服务器时，引擎也会设置该属性。重命名该列不会更改此值，因此会保留该列与表达式之间的关联。

该值有以下两种格式之一：

- `Table[Column]`，表名不加引号，用于表示表达式从其他表中获取的列，例如在 `SUMMARIZE ( 'Date', 'Date'[Year] )` 中为 `Date[Year]`
- `[Column]` 用于表示表达式创建的列，例如在 `ADDCOLUMNS ( ..., "Sales Amount", ...` 中为 `[Sales Amount]`…… )`，或对于表构造函数或 `UNION`，则为 `[Value]\`

### 名称自动推断

`IsNameInferred` · bool · 选项

列名是否与计算表格表达式中的名称一致。当它为 `true` 时，引擎和 Tabular Editor 3 会将列重命名为与表达式保持一致，例如在表达式更改时。将其设为 `false`，即可保留你自己为该列指定的名称。

在 Tabular Editor 3 中，当 `IsNameInferred` 为 `true` 时，`Name` 为只读。当你将其重新设为 `true` 时，如果表达式取自某一列，当前列就会使用那个源列的名称。

例如，用于创建字段参数的 C# Script 会将其各列的 `IsNameInferred` 设为 `false`，以保留脚本为这些列指定的名称。参见 @create-field-parameter。

## 替代项

Alternate Of 对象挂在聚合表的某一列上。它将该列映射到其汇总的明细表中的某一列，或映射到整个表，并设置值的聚合方式。配置好这些映射后，引擎会在可能的情况下直接从聚合表响应查询，并跳过通常大得多且往往处于 DirectQuery 模式的明细表。这种设置称为 _用户定义聚合_。有关分步说明，请参见 @user-defined-aggregations。

Alternate Of 需要 1460 或更高的兼容级别。它不会作为单独的对象显示在 **TOM Explorer** 中。若要设置以下属性，请在 **属性视图** 中展开该列的 `AlternateOf` 属性。

### 常见属性

- [注释](xref:object-properties-common#annotations)
- [对象类型](xref:object-properties-common#object-type)

### 基列

`BaseColumn` · 列 · 选项

此列所聚合的明细表中的列。例如，`Sales Agg` 表的 `Sales Amount` 列，其基础列为 `Sales[Sales Amount]`，汇总方式为 `Sum`。

设置 `BaseColumn` 或 `BaseTable` 其中之一。设置 `BaseColumn` 会清除 `BaseTable`。

### 基表

`BaseTable` · 表 · 选项

该列所统计行数的明细表。将其与 `Summarization` 的 `COUNT` 配合使用，用于存储明细行数的列，使引擎能够从聚合表直接回答 `COUNTROWS ( Sales )`。

设置 `BaseColumn` 或 `BaseTable` 之一。设置 `BaseTable` 会清除 `BaseColumn`，并将 `Summarization` 设为 `Count`；而将 `Summarization` 更改为任何其他值则会清除 `BaseTable`。只有当 `Summarization` 为 `Count` 时，**属性视图**才会显示 `BaseTable`。

### 列

`Column` · Column · 选项 · 只读

此 Alternate Of 所在聚合表中的列。**属性视图**会隐藏它，但你可以在 C# Script 中使用它。

### 汇总方式

`Summarization` · SummarizationType · 选项

此列中的值如何从基列或基表汇总而来。

| 值         | 含义                                                     |
| --------- | ------------------------------------------------------ |
| `GroupBy` | 一个分组依据列，保存与基列相同的值。当聚合表未与维度表建立关系时，此项必需，例如明细表是一张宽而扁平的表时。 |
| `Sum`     | 基列的总和。                                                 |
| `Count`   | 基表的行数，或基列中非空白值的数量。                                     |
| `Min`     | 基列中的最小值。                                               |
| `Max`     | 基列中的最大值。                                               |

除 `Count` 外，所有汇总方式都要求该列与其基列具有相同的数据类型，因此，`Decimal` 基列的 `Sum` 列也会是 `Decimal`。无论基列的数据类型是什么，`Count` 列都必须是整数 (`Int64`)。要让引擎能够从聚合表直接回答 `DISTINCTCOUNT`，请以 `GroupBy` 方式添加该列；即使聚合表与维度表建立了关系，也同样适用。不存在“非重复计数”汇总。

## 变体

变体是指当用户选择某一列时，客户端工具会显示的另一个项目。 Power BI 会把变体用于自动日期/时间：对于每个日期列，Power BI Desktop 都会创建一个隐藏的日期表、建立与该表的关系，并在该日期列上创建一个变体。当 Report 作者选择该日期列时，Power BI 会显示隐藏日期表的 **日期层次结构**。

变体主要出现在 Power BI 和 Fabric 模型中。在兼容级别为 1400 或更高的 Analysis Services 模型中，Tabular Editor 也会显示列的 `Variations` 属性。如果你的模型有自己的日期表，关闭 Power BI Desktop 中的自动日期/时间，以移除隐藏的日期表及其变体。见 @kb.bpa-remove-auto-date-table。

### 常见属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

### 父列

`Column` · 列 · 基本 · 只读

此变体所属的列。

### 默认列

`DefaultColumn` · 列 · 选项

当用户选择父列时，客户端工具显示的相关表中的某一列。设置此属性或 `DefaultHierarchy`，二选一。 Power BI Desktop 为自动日期/时间创建的变体会使用 `DefaultHierarchy`，并将 `DefaultColumn` 留空。

<!-- TODO (not verifiable from TE3 source): confirm whether Default Column and Default Hierarchy are mutually exclusive, and when Power BI uses Default Column. TE3 doesn't enforce either rule. -->

### 默认层次结构

`DefaultHierarchy` · 层次结构 · 选项

用户选择父列时，客户端工具会显示相关表的层级结构。对于自动日期/时间功能，这是隐藏的 `LocalDateTable_...` 表的 **日期层级结构**。

### 默认值

`IsDefault` · bool · 选项

指示这是否为该列的默认变体。当某列有多个变体时，用户选择该列时，客户端工具会显示默认变体。

### 关系

`Relationship` · 关系 · 选项

从父列到包含默认列或默认层次结构的表的关系。对于自动日期/时间，它指从日期列到其隐藏的日期表的关系。
