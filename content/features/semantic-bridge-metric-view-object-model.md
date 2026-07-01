---
uid: semantic-bridge-metric-view-object-model
title: Semantic Bridge Metric View Object Model
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
# Metric View Object Model

<!--
SUMMARY: Overview of the Metric View object model built into the Semantic Bridge.
-->

> [!NOTE]
> The Semantic Bridge is in public preview.
> The metric view object model is generally useful and represents the full current metric view specification as of the time of the Tabular Editor 3 3.26.2 release (June 2026).

The Semantic Bridge includes an object model representing a Databricks Metric View.
This allows you to work with Metric Views programmatically through C# scripts, similar to how you work with a Tabular model through the TOMWrapper.

Other than the [import GUI](xref:semantic-bridge#interface), all access to and interaction with a Metric View is through C# scripts.
All content in this document is referring to C# code that you would use in a [C# script](xref:csharp-scripts).

## Loading and accessing the Metric View

You can load a Metric view with [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) or [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A).
This stores the deserialized Metric View as [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model).
This property returns a [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) object, which is the root of the Metric View object graph.

```csharp
// Load a Metric View from disk
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");

// Access the loaded View
var view = SemanticBridge.MetricView.Model;
Output($"Metric View version: {view.Version}\r\nSource: {view.Source}");
```

Similar to a Tabular model and dissimilar to most other objects you may be used to in a C# script, the Metric View is persistent across multiple script executions.
This means that you can load a Metric View once, and reference it from subsequent script executions without re-loading it every time.
There is only ever a single Metric View loaded, and it is available in all scripts as `SemanticBridge.MetricView.Model` as mentioned above.
This behavior is similar to the Tabular model in C# scripts, which is always available simply as `Model`.

## Domain objects

The object model consists of four main types that correspond to the structure of a Metric View YAML file:
We do not repeat the entire specification here, so we encourage you to reference the [Databricks Metric View documentation](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)
and our [own API reference for the object model](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView).

| API Reference                                                                          | Description                                                |
|----------------------------------------------------------------------------------------|------------------------------------------------------------|
| [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View)       | The root object representing the entire Metric View        |
| [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join)       | A join definition connecting a dimension table to the fact |
| [`Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field)     | A field definition (column) in the Metric View             |
| [`Measure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) | An aggregation definition representing business logic      |

Most properties and attributes of a metric view have a structured representation in the object model,
but we defer discussion of these in this document,
as those are all direct representations of the metric view spec and documented in our API reference, mentioned above.

> [!NOTE]
> The object model was introduced in Tabular Editor 3.25.0 with support for Metric View v0.1.
> Support for Metric View v1.1 was added in Tabular Editor 3.26.2;
> this includes the `Comment` and `Materialization` properties on the `View`,
> `Cardinality` and `Rely` on `Join`,
> `Comment`, `DisplayName`, `Synonyms`, and `Format` on `Field` and `Measure`,
> `Window` on `Measure`.

> [!NOTE]
> In the object model, we follow C# naming conventions, and so use `PascalCase` for all type and property names in the object model.
> The Metric View YAML specification follows a naming convention of `snake_case`.
> Other than changing the case, we do not change any naming convention from the YAML.

### View

[The `View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) object is the root of the Metric View and contains:

- `Version`: The Metric View specification version (e.g., "1.1")
- `Source`: The source data for the fact table (e.g., "catalog.schema.table")
- `Filter`: Optional SQL boolean expression that applies to all queries
- `Comment`: Optional description of the metric view
- `Joins`: Collection of join definitions; non-null empty collection if there are no `Join`s
- `Fields`: Collection of field definitions; non-null empty collection if there are no `Field`s
- `Measures`: Collection of measure definitions; non-null empty collection if there are no `Measure`s
- `Materialization`: Materialization configuration for query acceleration when hosted on Databricks; [see the `Materialization` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Materialization)

```csharp
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

### Join

[A `Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join) represents a dimension table that is joined to the fact table:

- `Name`: Name of the joined table (used as an alias)
- `Source`: Source table or query for the join (e.g., "catalog.schema.dimension_table")
- `On`: Optional SQL boolean expression for the join condition
- `Using`: Optional list of column names for the join (alternative to `On`)
- `Joins`: Child joins (for snowflake schemas)
- `ParentJoin`: if this is a nested join, then `ParentJoin` is a pointer to the parent, otherwise null
- `Cardinality`: controls the relationship between `View.Source` or `ParentJoin` and this `Join`; [see the `JoinCardinality` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.JoinCardinality)
- `Rely`: Optimizer hints about the `Join`'s relationship to its parent; [see the `Rely` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Rely)

```csharp
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

### Field

[A `Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field) represents a field (column) in the Metric View:

- `Name`: The name of the field: referenced in metric view expressions
- `Expr`: The SQL expression defining the field (either a column reference or a SQL expression)
- `Comment`: Optional description of the field
- `DisplayName`: Optional human-readable display name for the field
- `Synonyms`: Optional alternative names for the field, used by AI and BI tools
- `Format`: Optional display format specification for the field's values; [see the `Format` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format)

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var field in view.Fields)
{
    sb.AppendLine($"Field: {field.Name}");
    sb.AppendLine($"  Expression: {field.Expr}");
}

Output(sb.ToString());
```

### Measure

[A `Measure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) represents a named aggregation with business logic:

- `Name`: The name of the measure: referenced in metric view expressions as `MEASURE(<name>)`
- `Expr`: The SQL aggregate expression defining the measure
- `Comment`: Optional description of the measure
- `DisplayName`: Optional human-readable display name for the measure
- `Synonyms`: Optional alternative names for the measure, used by AI and BI tools
- `Format`: Optional display format specification for the measure's values; [see the `Format` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format)
- `Window`: Optional list of window specifications for windowed or semi-additive aggregation; [see the `Window` API reference](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Window)

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var measure in view.Measures)
{
    sb.AppendLine($"Measure: {measure.Name}");
    sb.AppendLine($"  Expression: {measure.Expr}");
}

Output(sb.ToString());
```

## Using directives

When working with the Metric View object model in C# scripts, you may need to add a using directive to avoid naming conflicts with similarly-named types in the Tabular Object Model.
We recommend aliasing the namespace:

```csharp
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

## Complete example

Here is a complete script that loads a Metric View and outputs a summary of its contents:

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

if (view.Joins.Count > 0)
{
    sb.AppendLine($"\nJoins ({view.Joins.Count}):");
    foreach (var join in view.Joins)
    {
        sb.AppendLine($"  - {join.Name} -> {join.Source}");
    }
}

if (view.Fields.Count > 0)
{
    sb.AppendLine($"\nFields ({view.Fields.Count}):");
    foreach (var field in view.Fields)
    {
        sb.AppendLine($"  - {field.Name}: {field.Expr}");
    }
}

if (view.Measures.Count > 0)
{
    sb.AppendLine($"\nMeasures ({view.Measures.Count}):");
    foreach (var measure in view.Measures)
    {
        sb.AppendLine($"  - {measure.Name}: {measure.Expr}");
    }
}

Output(sb.ToString());
```

## References

- [`MetricView` namespace API documentation](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
- @semantic-bridge-fields-and-dimensions
- @semantic-bridge-metric-view-validation
- @semantic-bridge-metric-view-tabular-translation
- @semantic-bridge-how-tos
- [Databricks Metric View documentation](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)
- [Databricks Metric View YAML specification](https://learn.microsoft.com/en-us/azure/databricks/metric-views/data-modeling/syntax)
