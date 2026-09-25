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
> The Semantic Bridge is in public preview.
> The 3.25.0 release supports Metric View v0.1 metadata, and the 3.26.2 release supports Metric View v1.1 metadata.

The Semantic Bridge includes an object model representing a [Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/).
This allows you to work with Metric Views programmatically through C# scripts, similar to how you work with a Tabular model through the TOMWrapper.

除 [导入 GUI](xref:semantic-bridge#interface) 之外，对 Metric View 的所有访问与交互都通过 C# Script 完成。
All content in this document is referring to C# code that you would use in a [C# script](xref:csharp-scripts).

## 加载并访问 Metric View

You can load a Metric View with [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) or [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A).
This stores the deserialized Metric View as [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model).
This property returns a [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) object, which is the root of the Metric View object graph.

```csharp {compile}
// Load a Metric View from disk
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");

// Access the loaded View
var view = SemanticBridge.MetricView.Model;
Output($"Metric View version: {view.Version}\r\nSource: {view.Source}");
```

与 Tabular 模型类似，但不同于你在 C# Script 中常见的多数其他对象，Metric View 会在多次脚本执行之间保持持久化。
This means that you can load a Metric View once, and reference it from subsequent script executions without re-loading it every time.
There is only ever a single Metric View loaded, and it is available in all scripts as `SemanticBridge.MetricView.Model` as mentioned above.
This behavior is similar to the Tabular model in C# scripts, which is always available simply as `Model`.

[!INCLUDE [sample](../how-tos/includes/sample-metricview.md)]

## 领域对象

The object model consists of four main types that correspond to the structure of a Metric View YAML file.
We do not repeat the entire specification here, so we encourage you to reference the [Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/)
and our [own API reference for the object model](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView).

| API 参考                                                                             | 说明              |
| ---------------------------------------------------------------------------------- | --------------- |
| [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View)   | 表示整个指标视图的根对象    |
| [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join)   | 将维度表连接到事实表的联接定义 |
| [`Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field) | 指标视图中的字段定义（列）   |
| [`度量值`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) | 表示业务逻辑的聚合定义     |

Most properties and attributes of a Metric View have a structured representation in the object model,
but we defer discussion of these in this document,
as those are all direct representations of the Metric View spec and documented in our API reference, mentioned above.

> [!NOTE]
> The object model was introduced in Tabular Editor 3.25.0 with support for Metric View v0.1.
> Support for Metric View v1.1 was added in Tabular Editor 3.26.2;
> this includes the `Comment` and `Materialization` properties on the `View`,
> `Cardinality` and `Rely` on `Join`,
> `Comment`, `DisplayName`, `Synonyms`, and `Format` on `Field` and `Measure`,
> `Window` on `Measure`.

> [!NOTE]
> In the object model, we follow C# naming conventions: `PascalCase` for all type and property names.
> The Metric View YAML specification follows a naming convention of `snake_case`.
> Serialization and deserialization convert between these, so C# scripts use `PascalCase` and the YAML we read and write stays spec-compliant `snake_case`.

### 视图

[The `View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) object is the root of the Metric View and contains:

- `Version`: The Metric View specification version (e.g., "1.1")
- `Source`：事实表的源数据（例如 "catalog.schema.table"）
- `Filter`：可选的 SQL 布尔表达式，适用于所有查询
- `Comment`: Optional description of the Metric View
- `Joins`: Collection of join definitions; non-null empty collection if there are no `Join`s
- `Fields`: Collection of field definitions; non-null empty collection if there are no `Field`s
- `Measures`: Collection of measure definitions; non-null empty collection if there are no `Measure`s
- `Materialization`: Materialization configuration for query acceleration when hosted on Databricks; [see the `Materialization` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Materialization)

```csharp {run id=view-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Version: {view.Version}");
sb.AppendLine($"Source: {view.Source}");
sb.AppendLine($"Filter: {view.Filter ?? "(none)"}");
sb.AppendLine($"Joins: {view.Joins.Count}");
sb.AppendLine($"Fields: {view.Fields.Count}");
sb.AppendLine($"Measures: {view.Measures.Count}");

Output(sb.ToString());
```

**输出**

```
Version: 1.1
Source: sales.fact.orders
Filter: (none)
Joins: 3
Fields: 6
Measures: 6
```

### Join

[A `Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join) represents a dimension table that is joined to the fact table:

- `Name`：已联接表的名称（用作别名）
- `Source`：联接的数据源表或查询（例如 "catalog.schema.dimension_table"）
- `On`：用于联接条件的可选 SQL 布尔表达式
- `Using`：用于联接的可选列名列表（可作为 `On` 的替代方案）
- `Joins`：子联接（用于雪花架构）
- `ParentJoin`: if this is a nested join, then `ParentJoin` is a pointer to the parent, otherwise null
- `Cardinality`: controls the relationship between `View.Source` or `ParentJoin` and this `Join`; [see the `JoinCardinality` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.JoinCardinality)
- `Rely`: Optimizer hints about the `Join`'s relationship to its parent; [see the `Rely` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Rely)

```csharp {run id=join-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var join in view.Joins)
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

**输出**

```
Join: product
  Source: sales.dim.product
  On: source.product_id = product.product_id
Join: customer
  Source: sales.dim.customer
  On: source.customer_id = customer.customer_id
Join: date
  Source: sales.dim.date
  On: source.order_date = date.date_key
```

### 字段

[A `Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field) represents a field (column) in the Metric View:

- `Name`: The name of the field, referenced in Metric View expressions
- `Expr`: The SQL expression defining the field (either a column reference or a SQL expression)
- `Comment`: Optional description of the field
- `DisplayName`: Optional human-readable display name for the field
- `Synonyms`: Optional alternative names for the field, used by AI and BI tools
- `Format`: Optional display format specification for the field's values; [see the `Format` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format)

```csharp {run id=field-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var field in view.Fields)
{
    sb.AppendLine($"Field: {field.Name}");
    sb.AppendLine($"  Expression: {field.Expr}");
}

Output(sb.ToString());
```

**输出**

```
Field: product_name
  Expression: product.product_name
Field: product_category
  Expression: product.category
Field: customer_segment
  Expression: customer.segment
Field: order_date
  Expression: date.full_date
Field: order_year
  Expression: date.year
Field: order_month
  Expression: date.month_name
```

### 度量值

[A `Measure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) represents a named aggregation with business logic:

- `Name`: The name of the measure, referenced in Metric View expressions as `MEASURE(<name>)`
- `Expr`：定义度量值的 SQL 聚合表达式
- `Comment`: Optional description of the measure
- `DisplayName`: Optional human-readable display name for the measure
- `Synonyms`: Optional alternative names for the measure, used by AI and BI tools
- `Format`: Optional display format specification for the measure's values; [see the `Format` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format)
- `Window`: Optional list of window specifications for windowed or semi-additive aggregation; [see the `Window` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Window)

```csharp {run id=measure-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var measure in view.Measures)
{
    sb.AppendLine($"Measure: {measure.Name}");
    sb.AppendLine($"  Expression: {measure.Expr}");
}

Output(sb.ToString());
```

**输出**

```
Measure: total_revenue
  Expression: SUM(revenue)
Measure: gross_margin
  Expression: SUM(revenue) - SUM(cost)
Measure: order_count
  Expression: COUNT(*)
Measure: avg_order_value
  Expression: AVG(revenue)
Measure: revenue_to_budget
  Expression: (SUM(revenue) - SUM(budget)) / SUM(budget)
Measure: unique_customers
  Expression: COUNT(DISTINCT customer_id)
```

## Using 指令

在 C# Script 中使用 Metric View 对象模型时，你可能需要添加 using 指令，以避免与 Tabular Object Model 中同名或名称相近的类型发生命名冲突。
We recommend aliasing the namespace:

```csharp {compile}
// Alias to avoid conflicts with TOM types like Measure
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var view = SemanticBridge.MetricView.Model;

// Now you can reference types explicitly
foreach (MetricView.Field field in view.Fields)
{
    // ...
}
```

## Interacting with the object model

This document describes the patterns of using the object model.
See [the Semantic Bridge how-tos for detailed copy and paste-able examples](xref:semantic-bridge-how-tos).

### `View` parent pointer

All core Metric View objects described in this document inherit from [`MetricViewObjectBase`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.MetricViewObjectBase) for their core functionality.
Among other things, this means that each holds a `View` pointer back up to the Metric View they are defined in.
This allows you to inspect the whole Metric View when holding any of these objects.

```csharp {compile}
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var v = SemanticBridge.MetricView.Model; // alias the Metric View as v just for concision
var f = v.Fields.FirstOrDefault(); // f is the first field defined in the Metric View
Output(f.View == v); // the field, f, lets you navigate up to the containing view
```

### Adding objects

You never instantiate a `View`, `Join`, `Field`, or `Measure` directly.
Instead, deserialize or load a base `View`, or use the various `Add` methods:

- New Metric View:
  - [`Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A) YAML in a string
  - [`Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) a YAML file from disk
- Add objects
  - [`view.AddJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddJoin%2A)
  - [`view.AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A)
  - [`view.AddMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddMeasure%2A)

`Deserialize` and `Load` both set the global `SemanticBridge.MetricView.Model` so you can interact with it in scripts.
The `Add` methods all return the new object just added so that you can interact with it and set additional properties;
this mirrors the interaction with TOM objects you are already familiar with in C# scripts.

### Modify properties

The Metric View object model is mutable throughout, so you can simply set properties directly.
C# autocompletion in Tabular Editor 3 will help with finding the right properties and types to use.
All properties and their types are in [the API documentation](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView).

### 按名称访问对象

The root `View` contains collections for `Joins`, `Fields`, and `Measures`.
Each `Join` contains a child `Joins` collection.
Each of these can be indexed by name;
this looks up the child object by its `Name` property.
This lookup is case insensitive, matching the default in Databricks SQL.

### Metric View versions

We track the [Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/) to stay up to date with the specification.
All properties are annotated with the version that they were introduced.
Thanks to this, the object model will raise exceptions and surface diagnostics if you attempt to set a property that is not allowed for a given version of the spec.
We recommend always running [`SemanticBridge.MetricView.Validate();`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate) after modifying a Metric View in a C# script;
this will check all default validation rules for correctness.

## 参考资料

- [`MetricView` 命名空间 API 文档](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-metric-view-validation
- @semantic-bridge-metric-view-tabular-translation
- [Semantic Bridge how-tos for detailed examples](xref:semantic-bridge-how-tos)
- [Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/)
- [Metric View YAML specification](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference)
