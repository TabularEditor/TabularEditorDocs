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
> The 3.25.0 release supports Metric View v0.1 metadata, and the 3.26.2 release supports Metric View v1.1 metadata.

The Semantic Bridge includes an object model representing a Databricks Metric View.
This allows you to work with Metric Views programmatically through C# scripts, similar to how you work with a Tabular model through the TOMWrapper.

Other than the [import GUI](xref:semantic-bridge#interface), all access to and interaction with a Metric View is through C# scripts.
All content in this document is referring to C# code that you would use in a [C# script](xref:csharp-scripts).

## Loading and accessing the Metric View

You can load a Metric View with [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) or [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A).
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

The object model consists of four main types that correspond to the structure of a Metric View YAML file.
We do not repeat the entire specification here, so we encourage you to reference the [Databricks Metric View documentation](https://learn.microsoft.com/en-us/azure/databricks/business-semantics/)
and our [own API reference for the object model](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView).

| API Reference                                                                          | Description                                                |
|----------------------------------------------------------------------------------------|------------------------------------------------------------|
| [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View)       | The root object representing the entire Metric View        |
| [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join)       | A join definition connecting a dimension table to the fact |
| [`Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field)     | A field definition (column) in the Metric View             |
| [`Measure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) | An aggregation definition representing business logic      |

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

### View

[The `View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) object is the root of the Metric View and contains:

- `Version`: The Metric View specification version (e.g., "1.1")
- `Source`: The source data for the fact table (e.g., "catalog.schema.table")
- `Filter`: Optional SQL boolean expression that applies to all queries
- `Comment`: Optional description of the Metric View
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

- `Name`: The name of the field, referenced in Metric View expressions
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

- `Name`: The name of the measure, referenced in Metric View expressions as `MEASURE(<name>)`
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

## Interacting with the object model

This document describes the patterns of using the object model.
See [the Semantic Bridge how-tos for detailed copy and paste-able examples](xref:semantic-bridge-how-tos).

### `View` parent pointer

All core Metric View objects described in this document inherit from [`MetricViewObjectBase`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.MetricViewObjectBase) for their core functionality.
Among other things, this means that each holds a `View` pointer back up to the Metric View they are defined in.
This allows you to inspect the whole Metric View when holding any of these objects.

```csharp
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

### Accessing objects by name

The root `View` contains collections for `Joins`, `Fields`, and `Measures`.
Each `Join` contains a child `Joins` collection.
Each of these can be indexed by name;
this looks up the child object by its `Name` property.
This lookup is case insensitive, matching the default in Databricks SQL.

### Metric View versions

We track the [Databricks Metric View documentation](https://learn.microsoft.com/en-us/azure/databricks/business-semantics/) to stay up to date with the specification.
All properties are annotated with the version that they were introduced.
Thanks to this, the object model will raise exceptions and surface diagnostics if you attempt to set a property that is not allowed for a given version of the spec.
We recommend always running [`SemanticBridge.MetricView.Validate();`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate) after modifying a Metric View in a C# script;
this will check all default validation rules for correctness.

## References

- [`MetricView` namespace API documentation](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-metric-view-validation
- @semantic-bridge-metric-view-tabular-translation
- [Semantic Bridge how-tos for detailed examples](xref:semantic-bridge-how-tos)
- [Databricks Metric View documentation](https://learn.microsoft.com/en-us/azure/databricks/business-semantics/)
- [Databricks Metric View YAML specification](https://learn.microsoft.com/en-us/azure/databricks/business-semantics/metric-views/yaml-reference)
