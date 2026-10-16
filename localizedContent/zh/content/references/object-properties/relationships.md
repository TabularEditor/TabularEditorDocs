---
uid: object-properties-relationships
title: 关系属性
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

# 关系属性

<!--
SUMMARY: Reference for the properties of relationships, such as cardinality, cross filtering behavior and security filtering behavior.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍关系的属性。有关大多数对象共有的属性，请参阅 @object-properties-common。

## 关系

关系将一个表中的列连接到另一个表中的列，因此对其中一个表的筛选也会应用到另一个表。例如，从 `Sales[ProductKey]` 到 `Product[ProductKey]` 的关系会使对 `Product[Color]` 的筛选也会筛选 `Sales` 的行。

每个关系都有一个 _from_ 端和一个 _to_ 端。在典型的一对多关系中，from 端是每个键对应多行的表(如事实表)，to 端则是每个键对应单行的表(如维度表)。

Tabular Editor 3 在 **TOM Explorer** 中显示关系时，会将 from 列放在左侧、to 列放在右侧，例如 `'Sales'[ProductKey] ∞←1 'Product'[ProductKey]`。中间的符号表示各端的基数（`∞` 表示 `Many`，`1` 表示 `One`）以及筛选方向（`←` 表示单向，`↔` 表示双向）。当你更改列、基数或交叉筛选行为时，名称会自动更新。 Tabular Editor 2 使用相同的列顺序，但不显示基数符号；其箭头使用 `-->` 表示单向筛选，使用 `<-->` 表示双向筛选，例如 `'Sales'[ProductKey] --> 'Product'[ProductKey]`。

你可以在 **属性**视图中创建和编辑关系；如果使用 Tabular Editor 3，也可以在 @diagram-view 中进行操作。要根据 Databricks Unity Catalog 中定义的主键和外键创建关系，可以使用 @script-create-databricks-relationships 脚本。

### 常见属性

- [名称](xref:object-properties-common#name)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [已更改的属性](xref:object-properties-common#changed-properties)
- [错误消息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [状态](xref:object-properties-common#state)

### 源端列

`FromColumn` · 列 · 基本

关系源端的列。在一对多关系中，这通常是事实表中的外键列，例如 `Sales[ProductKey]`。选择列也会设置 `FromTable`。

### 源端基数

`FromCardinality` · RelationshipEndCardinality · 基本

源端在 `FromColumn` 中允许有多少行具有相同的值。

| 值      | 含义                                                                                            |
| ------ | --------------------------------------------------------------------------------------------- |
| `Many` | 多行可以具有相同的值。这是源端的常用设置。                                                                         |
| `One`  | 每个值在该列中最多出现一次。                                                                                |
| `None` | 基数未指定。不要使用此值。 Tabular Editor 3 的关系对话框只列出 `One` 和 `Many`，而 **TOM Explorer** 会将 `None` 显示为 `0`。 |

### 目标端列

`ToColumn` · 列 · 基本

关系目标端的列。在一对多关系中，这是维度表的键列，例如 `Product[ProductKey]`。选择列时也会设置 `ToTable`。

Best Practice Analyzer (BPA) 的 @kb.bpa-relationship-same-datatype 规则会标记 `FromColumn` 与 `ToColumn` 数据类型不同的关系。

### 目标端基数

`ToCardinality` · RelationshipEndCardinality · 基本

在目标端，`ToColumn` 中同一值最多可以出现在多少行中。可用值与 `FromCardinality` 相同，通常使用 `One`。这两个基数共同决定关系类型：

| 源端     | 目标端    | 关系                              |
| ------ | ------ | ------------------------------- |
| `Many` | `One`  | 多对一。这是事实表和维度表之间的标准关系。           |
| `One`  | `One`  | 一对一。两列都必须包含唯一值。                 |
| `Many` | `Many` | 多对多。两列都不需要唯一值。需要兼容级别为 1500 或更高。 |

如果 `One` 端的列包含重复值，刷新会报错并失败。多对多关系&#x662F;_&#x53D7;&#x9650;_&#x5173;系：它们不会为缺失的键添加空白行，而且通常比多对一关系更慢。仅当数据没有唯一键时才使用它们。

在 Tabular Object Model (TOM) 中，From 端始终是一对多关系中的“多”端。 Tabular Editor 会接受将 `FromCardinality` 设为 `One` 且将 `ToCardinality` 设为 `Many` 的设置，但在保存时引擎会拒绝，并报错：“From 端基数必须始终设置为 Many，除非该关系为 One-To-One”。如果要按相反方向关联这些表，请交换 From 列和 To 列。

### 启用

`IsActive` · bool · 基本

关系是否自动筛选数据。如果活动关系在两个表之间创建了多于一条路径，引擎会拒绝该模型。这种情况最常见于多个关系使用双向交叉筛选时。

对于同一对表之间的第二个关系，例如在从 `Sales[OrderDate]` 出发的活动关系旁边，再建立一个从 `Sales[ShipDate]` 到 `Date[Date]` 的关系，请将 `IsActive` 设为 `false`，并在度量值中使用 [USERELATIONSHIP](https://dax.guide/userelationship) 启用该关系：

```dax
Sales by Ship Date =
CALCULATE ( [Total Sales], USERELATIONSHIP ( Sales[ShipDate], 'Date'[Date] ) )
```

在 Tabular Editor 3 的图表视图中，你也可以右键单击某个关系来将其激活或停用。

### ID

`ID` · string · 基本 · 只读

关系的内部标识符，在 TOM 中就是该关系的名称。 Power BI Desktop 使用 GUID。 Tabular Editor 3 和 Tabular Editor 2 会为新关系分配一个唯一名称，名称以 `New Single Column Relationship` 开头。在 C# Script 或 Tabular Model Scripting Language (TMSL) 命令中，可以使用 ID 来引用特定关系。

### 源表

`FromTable` · 表 · 选项 · 只读

包含 `FromColumn` 的表。要更改它，请选择其他 `FromColumn`。 Tabular Editor 3 会在 **属性** 视图中隐藏此属性，因为 `FromColumn` 已经显示了该表。不过，你仍然可以在 C# Script 中读取它。

### 目标表

`ToTable` · 表 · 选项 · 只读

包含 `ToColumn` 的表。若要更改，请选择其他 `ToColumn`。 Tabular Editor 3 会在 **Properties** 视图中隐藏此属性。你仍然可以在 C# Script 中读取该属性。

### 交叉筛选行为

`CrossFilteringBehavior` · CrossFilteringBehavior · 选项

筛选沿关系传播的方向。

| 值                | 含义                                                                           |
| ---------------- | ---------------------------------------------------------------------------- |
| `OneDirection`   | 对 to 表的筛选会传递到 from 表。例如，对 `Product` 的筛选会传递到 `Sales`。默认值。                     |
| `BothDirections` | 筛选会双向传播。对 `Sales` 的筛选也会传递到 `Product`，因此 `Product` 上的切片器只会显示在当前筛选条件下有销售记录的产品。 |
| `Automatic`      | 引擎会分析这些关系，并通过启发式方法从其他行为中选择一种。                                                |

SQL Server 2025 Analysis Services 和 Power BI Desktop 都会将以 `Automatic` 保存的关系存储为 `BothDirections`。在 Power BI Desktop 中，和 `BothDirections` 一样，对 from 表的筛选也会传递到 to 表。如果你希望筛选双向传播，请显式将其设置为 `BothDirections`。

`BothDirections` 会降低查询速度，还会增加活动关系在两个表之间创建多条路径的可能性，而这是引擎不接受的。对于单个度量值，如需双向筛选，请将关系保持为单向，并在该度量值中使用 [CROSSFILTER](https://dax.guide/crossfilter)，例如 `CROSSFILTER ( Sales[ProductKey], Product[ProductKey], BOTH )`。

只有同时设置 `SecurityFilteringBehavior` 时，双向筛选才会应用于行级安全性。 BPA 规则 @kb.bpa-many-to-many-single-direction 会标记双向筛选的多对多关系。

### 安全筛选行为

`SecurityFilteringBehavior` · SecurityFilteringBehavior · 选项

行级安全性筛选器通过关系传播的方向。它对应于 Power BI Desktop 中的 **在两个方向上应用安全筛选器** 选项。

| 值                | 含义                                                                                                            |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |
| `OneDirection`   | 安全筛选器只会从 to 表传播到 from 表，即使 `CrossFilteringBehavior` 为 `BothDirections` 也是如此。默认值。                              |
| `BothDirections` | 安全筛选器双向传播。仅当 `CrossFilteringBehavior` 为 `BothDirections` 时有效。                                                 |
| `None`           | 阻止安全筛选器从“一”侧传播到“多”侧。仅适用于复合模型中的受限关系，其中一个表来自 Power BI 语义模型或 Analysis Services 数据库，另一个表来自不同的数据源。需要兼容级别 1561 或更高。 |

当 `CrossFilteringBehavior` 为 `OneDirection` 时，Tabular Editor 会接受 `BothDirections`，但在保存时引擎会拒绝，并报错“cannot have SecurityFilterBehavior set to BothDirections when the CrossFilterBehavior is set to OneDirection”。如果某个关系当前以双向方式传播安全筛选器，而你将 `CrossFilteringBehavior` 改回 `OneDirection`，也会出现同样的错误，因此请先更改 `SecurityFilteringBehavior`。

`BothDirections` 的典型用法之一是动态行级安全性：用户表上的筛选器通过桥接表传播到维度表。见 @roles-and-rls 和 @data-security-setup-rls。要检查安全筛选器是否传播到正确的表，请使用模拟身份来测试该角色。见 @data-security-testing。

### 基于日期的联接行为

`JoinOnDateBehavior` · DateTimeRelationshipBehavior · 选项

当两列都具有 `DateTime` 数据类型时，引擎如何匹配值。

| 值              | 含义                                                            |
| -------------- | ------------------------------------------------------------- |
| `DateAndTime`  | 日期和时间都必须匹配。默认值。                                               |
| `DatePartOnly` | 引擎只比较日期部分，忽略时间。例如，`2026-09-23 14:30` 会匹配日期表中的日期 `2026-09-23`。 |

当 From 列包含日期和时间，而 To 列是每天一行的日期表时，使用 `DatePartOnly`。使用 `DateAndTime` 时，只有恰好在午夜的值才会匹配。 Power BI Desktop 对日期/时间列与其自动日期/时间表之间的关系使用 `DatePartOnly`。

<!-- TODO (not verifiable from TE3 source): whether DatePartOnly works in DirectQuery. -->

### 依赖参照完整性

`RelyOnReferentialIntegrity` · bool · 选项

对于 DirectQuery：当 `true` 时，引擎会假定 `FromColumn` 中的每个值都存在于 `ToColumn` 中，并且发送到数据源的 SQL 查询会使用 `INNER JOIN`。当 `false` 时，这些查询会使用 `OUTER JOIN`。 `INNER JOIN` 通常更快。它对应于 Power BI Desktop 中的 **假定参照完整性**。此属性对导入表没有影响。

仅当数据源保证每个键都有匹配项时才启用它，例如通过外键约束。如果 From 端的行没有匹配项，它们将不会出现在结果中，且不会报错。

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM documentation says this property is "unused; reserved for future use", while the TOM library's own description (shown in Tabular Editor) says DirectQuery queries use INNER JOIN when it's true. Confirm which engines and storage modes honor it. -->

### 类型

`Type` · RelationshipType · 选项 · 只读

关系的类型。唯一的值是 `SingleColumn`，表示两端各一列之间的关系。 Tabular Editor 3 会在 **属性** 视图中隐藏此属性。
