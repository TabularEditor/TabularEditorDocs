---
uid: semantic-bridge-metric-view-object-model
title: Semantic Bridge Metric View 对象模型
author: Greg Baldini
updated: 2026-06-29
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Metric View 对象模型

<!--
SUMMARY: Overview of the Metric View object model built into the Semantic Bridge.
-->

> [!NOTE]
> Semantic Bridge 目前为公共预览版。
> 3.25.0 版本支持 Metric View v0.1 元数据，3.26.2 版本支持 Metric View v1.1 元数据。

Semantic Bridge 包含一个用于表示 [Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/) 的对象模型。
这使你可以通过 C# Script 以编程方式处理 Metric View，类似于通过 TOMWrapper 操作 Tabular 模型。

除 [导入 GUI](xref:semantic-bridge#interface) 之外，对 Metric View 的所有访问与交互都通过 C# Script 完成。
本文档中的所有内容均指你将在 [C# Script](xref:csharp-scripts) 中使用的 C# 代码。

## 加载并访问 Metric View

你可以通过 [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) 或 [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A) 来加载 Metric View。
这会将反序列化后的 Metric View 存储在 [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model) 中。
该属性返回一个 [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) 对象，它是 Metric View 对象图的根对象。

```csharp {compile}
// Load a Metric View from disk
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");

// Access the loaded View
var view = SemanticBridge.MetricView.Model;
Output($"Metric View version: {view.Version}\r\nSource: {view.Source}");
```

与 Tabular 模型类似，但不同于你在 C# Script 中常见的多数其他对象，Metric View 会在多次脚本执行之间保持持久化。
这意味着你只需加载一次指标视图，后续脚本执行时即可引用它，而无需每次都重新加载。
任意时刻只会加载一个指标视图；如上所述，所有脚本都可以通过 `SemanticBridge.MetricView.Model` 访问它。
这种行为类似于 C# Script 中的表格模型，它始终可以直接通过 `Model` 访问。

[!INCLUDE [sample](../how-tos/includes/sample-metricview.md)]

## 领域对象

对象模型由四种主要类型组成，对应于 Metric View YAML 文件的结构。
本文不再重复完整规范，因此建议你参考 [Metric View 文档](https://learn.microsoft.com/azure/databricks/business-semantics/)
以及我们的 [对象模型 API 参考](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)。

| API 参考                                                                             | 说明              |
| ---------------------------------------------------------------------------------- | --------------- |
| [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View)   | 表示整个指标视图的根对象    |
| [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join)   | 将维度表连接到事实表的联接定义 |
| [`Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field) | 指标视图中的字段定义（列）   |
| [`度量值`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) | 表示业务逻辑的聚合定义     |

Metric View 的大多数属性和特性在对象模型中都有结构化表示，
但本文档不再展开讨论，
因为这些内容都是对 Metric View 规范的直接映射，并已记录在上文提到的 API 参考中。

> [!NOTE]
> 该对象模型在 Tabular Editor 3.25.0 中引入，并支持 Metric View v0.1。
> 在 Tabular Editor 3.26.2 中加入了对 Metric View v1.1 的支持；
> 其中包括 `View` 上的 `Comment` 和 `Materialization` 属性，
> `Join` 上的 `Cardinality` 和 `Rely`，
> `Field` 和 `Measure` 上的 `Comment`、`DisplayName`、`Synonyms` 和 `Format`，
> 以及 `Measure` 上的 `Window`。

> [!NOTE]
> 在对象模型中，我们遵循 C# 命名约定：所有类型名和属性名均使用 `PascalCase`。
> 指标视图 YAML 规范遵循 `snake_case` 的命名约定。
> 序列化和反序列化会在两者之间转换，因此在 C# Script 中使用 `PascalCase`，而我们读取和写入的 YAML 则保持符合规范的 `snake_case`。

### View

[`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) 对象是 Metric View 的根对象，包含：

- `Version`：Metric View 规范版本（例如 "1.1"）
- `Source`：事实表的源数据（例如 "catalog.schema.table"）
- `Filter`：可选的 SQL 布尔表达式，适用于所有查询
- `Comment`：Metric View 的可选描述
- `Joins`：Join 定义的集合；如果没有 `Join`s，则为非 null 的空集合
- `Fields`：Field 定义的集合；如果没有 `Field`s，则为非 null 的空集合
- `Measures`：度量值定义的集合；如果没有 `Measure`s，则为非 null 的空集合
- `Materialization`：在 Databricks 上托管时用于查询加速的物化配置；[参阅 `Materialization` API 参考](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Materialization)

```csharp {run id=view-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"版本: {view.Version}");
sb.AppendLine($"来源: {view.Source}");
sb.AppendLine($"筛选条件: {view.Filter ?? "(无)"}");
sb.AppendLine($"联接数: {view.Joins.Count}");
sb.AppendLine($"字段数: {view.Fields.Count}");
sb.AppendLine($"度量值数: {view.Measures.Count}");

Output(sb.ToString());
```

**输出**

```
版本: 1.1
来源: sales.fact.orders
筛选条件: (无)
联接数: 3
字段数: 6
度量值数: 6
```

### 联接

[`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join) 表示一个与事实表联接的维度表：

- `Name`：已联接表的名称（用作别名）
- `Source`：联接的数据源表或查询（例如 "catalog.schema.dimension_table"）
- `On`：用于联接条件的可选 SQL 布尔表达式
- `Using`：用于联接的可选列名列表（可作为 `On` 的替代方案）
- `Joins`：子联接（用于雪花架构）
- `ParentJoin`：如果这是嵌套联接，则 `ParentJoin` 指向父联接；否则为 null
- `Cardinality`：控制 `View.Source` 或 `ParentJoin` 与此 `Join` 之间的关系；[参见 `JoinCardinality` API 参考](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.JoinCardinality)
- `Rely`：关于该 `Join` 与其父联接之间关系的优化器提示；[参见 `Rely` API 参考](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Rely)

```csharp {run id=join-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var join in view.Joins)
{
    sb.AppendLine($"联接: {join.Name}");
    sb.AppendLine($"  来源: {join.Source}");
    if (!string.IsNullOrEmpty(join.On))
        sb.AppendLine($"  条件: {join.On}");
    if (join.Using != null && join.Using.Count > 0)
        sb.AppendLine($"  Using: {string.Join(", ", join.Using)}");
}

Output(sb.ToString());
```

**输出**

```
联接: product
  来源: sales.dim.product
  条件: source.product_id = product.product_id
联接: customer
  来源: sales.dim.customer
  条件: source.customer_id = customer.customer_id
联接: date
  来源: sales.dim.date
  条件: source.order_date = date.date_key
```

### 字段

[`Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field) 表示 Metric View 中的一个字段（列）：

- `Name`：字段名称，可在 Metric View 表达式中引用
- `Expr`：定义该字段的 SQL 表达式（可以是列引用或 SQL 表达式）
- `Comment`：字段的可选说明
- `DisplayName`：字段的可选、便于阅读的显示名称
- `Synonyms`：字段的可选别名，用于 AI 和 BI 工具
- `Format`：字段值的可选显示格式规范；[参见 `Format` API 参考](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format)

```csharp {run id=field-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var field in view.Fields)
{
    sb.AppendLine($"字段: {field.Name}");
    sb.AppendLine($"  表达式: {field.Expr}");
}

Output(sb.ToString());
```

**输出**

```
字段: product_name
  表达式: product.product_name
字段: product_category
  表达式: product.category
字段: customer_segment
  表达式: customer.segment
字段: order_date
  表达式: date.full_date
字段: order_year
  表达式: date.year
字段: order_month
  表达式: date.month_name
```

### 度量值

[`度量值`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) 表示一个带业务逻辑的命名聚合：

- `Name`：度量值名称，可在 Metric View 表达式中通过 `MEASURE(<name>)` 引用
- `Expr`：定义度量值的 SQL 聚合表达式
- `Comment`：度量值的可选说明
- `DisplayName`：度量值的可选、便于阅读的显示名称
- `Synonyms`：度量值的可选别名，用于 AI 和 BI 工具
- `Format`：度量值的可选显示格式规范；[参见 `Format` API 参考](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format)
- `Window`：用于窗口聚合或半可加聚合的可选窗口规范列表；[参见 `Window` API 参考](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Window)

```csharp {run id=measure-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var measure in view.Measures)
{
    sb.AppendLine($"度量值: {measure.Name}");
    sb.AppendLine($"  表达式: {measure.Expr}");
}

Output(sb.ToString());
```

**输出**

```
度量值: total_revenue
  表达式: SUM(revenue)
度量值: gross_margin
  表达式: SUM(revenue) - SUM(cost)
度量值: order_count
  表达式: COUNT(*)
度量值: avg_order_value
  表达式: AVG(revenue)
度量值: revenue_to_budget
  表达式: (SUM(revenue) - SUM(budget)) / SUM(budget)
度量值: unique_customers
  表达式: COUNT(DISTINCT customer_id)
```

## Using 指令

在 C# Script 中使用 Metric View 对象模型时，你可能需要添加 using 指令，以避免与 Tabular Object Model 中同名或名称相近的类型发生命名冲突。
我们建议为命名空间设置别名：

```csharp {compile}
// 为避免与 TOM 类型（如 Measure 度量值）冲突而设置别名
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var view = SemanticBridge.MetricView.Model;

// 现在你可以显式引用类型
foreach (MetricView.Field field in view.Fields)
{
    // ...
}
```

## 与对象模型交互

本文档介绍使用对象模型的常见模式。
你可以在 [Semantic Bridge 操作指南](xref:semantic-bridge-how-tos) 中查看可直接复制粘贴的详细示例。

### 指向父级 `View` 的指针

本文档中介绍的所有核心 Metric View 对象都继承自 [`MetricViewObjectBase`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.MetricViewObjectBase)，并由此获得核心功能。
这也意味着，每个对象都持有一个 `View` 指针，指回其定义所在的 Metric View。
因此，当你持有其中任一对象时，都可以检查整个 Metric View。

```csharp {compile}
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var v = SemanticBridge.MetricView.Model; // 为简洁起见，将 Metric View 别名为 v
var f = v.Fields.FirstOrDefault(); // f 是 Metric View 中定义的第一个字段
Output(f.View == v); // 字段 f 允许你向上导航到其所属的视图
```

### 添加对象

不要直接实例化 `View`、`Join`、`Field` 或 `Measure` 度量值。
而应反序列化或加载一个基础 `View`，或者使用各种 `Add` 方法：

- 新建 Metric View：
  - 使用 [`Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A) 反序列化字符串中的 YAML
  - 使用 [`Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) 从磁盘加载 YAML 文件
- 添加对象
  - [`view.AddJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddJoin%2A)
  - [`view.AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A)
  - [`view.AddMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddMeasure%2A)

`Deserialize` 和 `Load` 都会设置全局 `SemanticBridge.MetricView.Model`，这样你就可以在脚本中与其交互。
所有 `Add` 方法都会返回刚添加的新对象，方便你与其交互并设置其他属性；
这与你在 C# Script 中已经熟悉的 TOM 对象交互方式一致。

### 修改属性

Metric View 对象模型整体上是可变的，因此你可以直接设置属性。
Tabular Editor 3 中的 C# 自动补全可帮助你找到要使用的正确属性和类型。
所有属性及其类型均可在 [API 文档](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView) 中查阅。

### 按名称访问对象

根 `View` 包含 `Joins`、`Fields` 和 `Measures` 三个集合。
每个 `Join` 都包含一个子 `Joins` 集合。
这些集合都可以按名称进行索引；
即通过子对象的 `Name` 属性来查找。
这种查找不区分大小写，与 Databricks SQL 的默认行为一致。

### Metric View 版本

我们持续跟踪 [Metric View 文档](https://learn.microsoft.com/azure/databricks/business-semantics/)，以确保与规范保持同步。
所有属性都标注了其引入的版本。
因此，如果你尝试设置在某个规范版本中不被允许的属性，对象模型会引发异常并提供诊断信息。
我们建议在 C# Script 中修改 Metric View 后，始终运行 [`SemanticBridge.MetricView.Validate();`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate)；
这会检查所有默认验证规则是否正确。

## 参考资料

- [`MetricView` 命名空间 API 文档](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-metric-view-validation
- @semantic-bridge-metric-view-tabular-translation
- [Semantic Bridge 操作指南，含详细示例](xref:semantic-bridge-how-tos)
- [Metric View 文档](https://learn.microsoft.com/azure/databricks/business-semantics/)
- [Metric View YAML 规范](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference)
