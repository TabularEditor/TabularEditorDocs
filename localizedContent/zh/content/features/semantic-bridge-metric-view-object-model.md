---
uid: semantic-bridge-metric-view-object-model
title: Semantic Bridge Metric View 对象模型
author: Greg Baldini
updated: 2025-01-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: 桌面版
          none: true
        - edition: 商业版
          none: true
        - edition: 企业版
          full: true
---

# Metric View 对象模型

<!--
SUMMARY: Overview of the Metric View object model built into the Semantic Bridge.
-->

> [!NOTE]
> 3.25.0 中发布的 Semantic Bridge 属于 MVP 功能。
> 其限制如下所述，且 API 与功能范围可能会发生变化。
> 这里的对象模型明显缺少 TOMWrapper 中提供的许多便捷功能，而这些功能你可能已经在用于操作 Tabular 模型的 C# Script 中用过并熟悉。
> 如 [Semantic Bridge 的限制](xref:semantic-bridge#mvp-limitations) 中所述，我们目前仅支持 Metric View v0.1 元数据。

Semantic Bridge 包含一个用于表示 Databricks Metric View 的对象模型。
这使你可以通过 C# Script 以编程方式处理 Metric View，类似于通过 TOMWrapper 操作 Tabular 模型。

除 [导入 GUI](xref:semantic-bridge#interface) 外，对 Metric View 的所有访问与交互都需要通过 C# Script 进行。
本文档中的所有内容均指你将在 [C# Script](xref:csharp-scripts) 中使用的 C# 代码。

## 加载并访问 Metric View

你可以使用 [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Load_System_String_) 或 [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Deserialize_System_String_) 来加载 Metric View。
这会将反序列化后的 Metric View 存储在 [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Model) 中。
该属性返回一个 [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) 对象，它是 Metric View 对象图的根对象。

```csharp
// Load a Metric View from disk
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");

// Access the loaded View
var view = SemanticBridge.MetricView.Model;
Output($"Metric View version: {view.Version}\r\nSource: {view.Source}");
```

与 Tabular 模型类似、但不同于你在 C# Script 中常用的大多数其他对象，Metric View 会在多次脚本执行之间持续保留。
这意味着你只需加载一次指标视图，后续脚本执行时即可引用它，而无需每次都重新加载。
任意时刻只会加载一个指标视图；如上所述，所有脚本都可以通过 `SemanticBridge.MetricView.Model` 访问它。
这种行为类似于 C# Script 中的表格模型，它始终可以直接通过 `Model` 访问。

## 领域对象

对象模型由四种主要类型组成，对应于指标视图 YAML 文件的结构：
我们不会在此重复完整规范，建议你参考 [Databricks 指标视图文档](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)。

| API 参考                                                                                     | 说明              |
| ------------------------------------------------------------------------------------------ | --------------- |
| [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View)           | 表示整个指标视图的根对象    |
| [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join)           | 将维度表连接到事实表的联接定义 |
| [`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) | 指标视图中的字段定义（列）   |
| [`度量值`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure)         | 表示业务逻辑的聚合定义     |

> [!NOTE]
> 在对象模型中，我们遵循 C# 的命名约定，因此，对象模型中的所有类型和属性名称都使用 `PascalCase`。
> 指标视图 YAML 规范遵循 `snake_case` 的命名约定。
> 总体而言，我们主要关注作为 Semantic Bridge 组件的 C# 对象模型。
> 除了更改大小写之外，我们不会改变 YAML 中的任何命名约定。

### View

[`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) 对象是指标视图的根对象，包含：

- `Version`：指标视图规范版本（例如 "0.1"）
- `Source`：事实表的源数据（例如 "catalog.schema.table"）
- `Filter`：可选的 SQL 布尔表达式，适用于所有查询
- `Joins`：联接定义的集合
- `Dimensions`：维度（字段）定义的集合
- `Measures`：度量值定义的集合

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Version: {view.Version}");
sb.AppendLine($"Source: {view.Source}");
sb.AppendLine($"Filter: {view.Filter ?? "(none)"}");
sb.AppendLine($"Joins: {view.Joins?.Count ?? 0}");
sb.AppendLine($"Dimensions: {view.Dimensions?.Count ?? 0}");
sb.AppendLine($"Measures: {view.Measures?.Count ?? 0}");

Output(sb.ToString());
```

#### `View` 翻译与验证

`View.Source` 属性会成为表格模型中的事实表，命名为 `'Fact'`。
如果 `Source` 是一个 3 段式表或视图引用，则会被翻译为一个 M 分区，通过名称访问该 SQL 对象。
如果 `Source` 不是一个 3 段式表或视图引用，则会被翻译为一个包含内嵌 SQL 查询的 M 分区，并将整个 `Source` 字符串作为 SQL 查询。
在翻译时会忽略 `Filter` 属性。

为了评估验证规则，会先检查 `View`，然后按顺序验证各集合：先 `Joins`，再 `Dimensions`，最后 `Measures`。
事实表 `Source` 的验证是在 `View` 对象的验证规则中完成的。

### 联接

[`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join) 表示一个与事实表联接的维度表：

- `Name`：已联接表的名称（用作别名）
- `Source`：联接的数据源表或查询（例如 "catalog.schema.dimension_table"）
- `On`：用于联接条件的可选 SQL 布尔表达式
- `Using`：用于联接的可选列名列表（可作为 `On` 的替代方案）
- `Joins`：子联接（用于雪花架构）

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var join in view.Joins ?? [])
{
    sb.AppendLine($"Join: {join.Name}");
    sb.AppendLine($"  Source: {join.Source}");
    if (!string.IsNullOrEmpty(join.On))
        sb.AppendLine($"  On: {join.On}");
    if (join.Using != null && join.Using.Count > 0)
        sb.AppendLine($"  Using: {string.Join(", ", join.Using)}");
}

Output(sb.ToString());
```

#### `Join` 翻译与验证

不支持嵌套的 `Join`，也就是说，只能翻译严格的星型架构。
仅支持对使用 `On` 的单字段等值联接进行翻译。
每个 `Join` 都会成为表格模型中的一张表，并且会按照与 `View.Source` 属性相同的规则定义一个 M 分区。

`Join` 会按照它们在 Metric View 定义中出现的顺序进行验证。

### 维度

[`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) 表示 Metric View 中的一个字段（列）：

- `Name`：维度的显示名称
- `Expr`：定义该维度的 SQL 表达式（可以是列引用或 SQL 表达式）

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var dim in view.Dimensions ?? [])
{
    sb.AppendLine($"Dimension: {dim.Name}");
    sb.AppendLine($"  Expression: {dim.Expr}");
}

Output(sb.ToString());
```

#### `Dimension` 的翻译与验证

每个 `Dimension` 都会成为 Tabular 模型中的一列。
如果 `Expr` 是未限定的字段引用，则该字段会添加到事实表中。
如果 `Expr` 是限定引用（例如 `table.field`），则会将其添加到为该 `Join` 创建的表中，该表名与限定引用中“表名部分”的名称相同；如果表名部分为 `source`，则会将其添加到事实表中。
无论是限定还是非限定的字段引用，该字段都会以 [`TOMWrapper.DataColumn`](xref:TabularEditor.TOMWrapper.DataColumn) 的形式添加。
如果 `Expr` 是 SQL 表达式，则会以 [`TOMWrapper.CalculatedColumn`](xref:TabularEditor.TOMWrapper.CalculatedColumn) 的形式添加。
当 `Expr` 为 SQL 表达式时，我们会尝试提取其中所有字段引用；如果所有字段引用的表名部分都相同，则将其添加到为该 `Join` 创建的表中；否则将其添加到事实表中。
我们不会翻译 `Dimension.Expr` 属性中的 SQL 表达式；该 SQL 表达式会作为注释包含在 `CalculatedColumn` 的 DAX 表达式中。
这些表达式需要用户自行翻译。
我们会尝试识别 SQL 表达式中的所有字段引用；如果这些字段尚未作为 Metric View `Dimension` 存在于 Tabular 模型中，就将它们作为 `DataColumn` 添加。

一些示例：

| `Expr`                                                | 翻译后的类型             | 添加到的表           | 说明                                       |
| ----------------------------------------------------- | ------------------ | --------------- | ---------------------------------------- |
| `field1`                                              | `DataColumn`       | `'Fact'`        | 未限定字段引用等同于用 `source` 进行限定的字段引用           |
| `source.field2`                                       | `DataColumn`       | `'Fact'`        | `source` 是对 `View.Source` 属性的引用，即事实表     |
| `dimCustomer.key`                                     | `DataColumn`       | `'dimCustomer'` | 必须存在一个 `Join`，其 `Name` 属性为 `dimCustomer` |
| `CONCAT(dimCustomer.FirstName, dimCustomer.LastName)` | `CalculatedColumn` | `'dimCustomer'` | 限定名称中的所有表部分都指向同一个名称                      |
| `CONCAT(dimGeo.Country, dimCustomer.Address)`         | `CalculatedColumn` | `'Fact'`        | 存在多个彼此不同的表部分                             |

`Dimension` 会按其在 Metric View 定义中出现的顺序进行验证。

### 度量值

[`度量值`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) 表示一个带业务逻辑的命名聚合：

- `Name`：度量值的显示名称
- `Expr`：定义度量值的 SQL 聚合表达式

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var measure in view.Measures ?? [])
{
    sb.AppendLine($"度量值: {measure.Name}");
    sb.AppendLine($"  表达式: {measure.Expr}");
}

Output(sb.ToString());
```

#### `度量值` 的翻译与验证

所有度量值都会添加到事实表中。
简单聚合会被翻译为 DAX 表达式。
简单聚合是对单个字段进行的一次聚合（例如 `SUM(table.field)`）。
支持的聚合包括 sum、count、distinct count、max、min 和 average。
其他表达式会以注释的形式原样保留在 Tabular 度量值的 DAX 表达式中。
我们会尝试识别 SQL 表达式中引用的所有字段；如果这些字段尚未作为 Metric View 的 `Dimension` 存在，则将其作为 `DataColumn` 添加到表格模型中。

> [!WARNING]
> SQL 和 DAX 是两种不同的语言，语义也不同。
> 自动翻译得到的度量值，可能无法在 Databricks Metric View 和表格模型中表达完全相同的计算逻辑。
> 你需要自己验证所有代码是否按预期工作。

这些 `Measure` 会按它们在 Metric View 定义中出现的顺序进行验证。

## Using 指令

在 C# Script 中使用 Metric View 对象模型时，你可能需要添加 using 指令，以避免与 Tabular Object Model 中同名或名称相近的类型发生命名冲突。
我们建议为命名空间设置别名：

```csharp
// 为避免与 TOM 类型（如 Measure）冲突而设置别名
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var view = SemanticBridge.MetricView.Model;

// Now you can reference types explicitly
foreach (MetricView.Dimension dim in view.Dimensions ?? [])
{
    // ...
}
```

## 完整示例

下面是一个完整的脚本示例，用于加载一个 Metric View，并输出其内容摘要：

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// Load the Metric View
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

// sb.AppendLine summary
sb.AppendLine("=== Metric View Summary ===");
sb.AppendLine($"Version: {view.Version}");
sb.AppendLine($"Source: {view.Source}");

if (view.Joins != null && view.Joins.Count > 0)
{
    sb.AppendLine($"\nJoins ({view.Joins.Count}):");
    foreach (var join in view.Joins)
    {
        sb.AppendLine($"  - {join.Name} -> {join.Source}");
    }
}

if (view.Dimensions != null && view.Dimensions.Count > 0)
{
    sb.AppendLine($"\nDimensions ({view.Dimensions.Count}):");
    foreach (var dim in view.Dimensions)
    {
        sb.AppendLine($"  - {dim.Name}: {dim.Expr}");
    }
}

if (view.Measures != null && view.Measures.Count > 0)
{
    sb.AppendLine($"\nMeasures ({view.Measures.Count}):");
    foreach (var measure in view.Measures)
    {
        sb.AppendLine($"  - {measure.Name}: {measure.Expr}");
    }
}

Output(sb.ToString());
```

## 参考资料

- [`MetricView` 命名空间 API 文档](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
- @semantic-bridge-how-tos
- [Databricks Metric View 文档](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)
- [Databricks Metric View YAML 规范](https://learn.microsoft.com/en-us/azure/databricks/metric-views/data-modeling/syntax)
