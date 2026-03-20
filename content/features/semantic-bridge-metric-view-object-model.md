---
uid: semantic-bridge-metric-view-object-model
title: Semantic Bridge Metric View Object Model
author: Greg Baldini
updated: 2025-01-23
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
> The Semantic Bridge as released in 3.25.0 is an MVP feature.
> It has limitations as documented below, and the API and feature surface area are subject to change.
> The object model here conspicuously lacks many affordances available in the TOMWrapper which users may be familiar with from C# scripts that manipulate a Tabular model.
> As noted in the [limitations of the Semantic Bridge](xref:semantic-bridge#mvp-limitations), we currently only support Metric View v0.1 metadata.

The Semantic Bridge includes an object model representing a Databricks Metric View.
This allows you to work with Metric Views programmatically through C# scripts, similar to how you work with a Tabular model through the TOMWrapper.

Other than the [import GUI](xref:semantic-bridge#interface), all access to and interaction with a Metric View is through C# scripts.
All content in this document is referring to C# code that you will use in a [C# script](xref:csharp-scripts).

## Loading and accessing the Metric View

You can load a Metric view with [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Load_System_String_) or [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Deserialize_System_String_).
This stores the deserialized Metric View as [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Model).
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
We do not repeat the entire specification here, so we encourage you to reference the [Databricks Metric View documentation](https://learn.microsoft.com/en-us/azure/databricks/metric-views/).

| API Reference                                                                              | Description                                                |
|--------------------------------------------------------------------------------------------|------------------------------------------------------------|
| [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View)           | The root object representing the entire Metric View        |
| [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join)           | A join definition connecting a dimension table to the fact |
| [`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) | A field definition (column) in the Metric View             |
| [`Measure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure)     | An aggregation definition representing business logic      |

> [!NOTE]
> In the object model, we follow C# naming conventions, and so use `PascalCase` for all type and property names in the object model.
> The Metric View YAML specification follows a naming convention of `snake_case`.
> In general, we focus on the C# object model that is a component of the Semantic Bridge.
> Other than changing the case, we do not change any naming convention from the YAML.

### View

The [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) object is the root of the Metric View and contains:

- `Version`: The Metric View specification version (e.g., "0.1")
- `Source`: The source data for the fact table (e.g., "catalog.schema.table")
- `Filter`: Optional SQL boolean expression that applies to all queries
- `Joins`: Collection of join definitions
- `Dimensions`: Collection of dimension (field) definitions
- `Measures`: Collection of measure definitions

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

#### `View` translation and validation

The `View.Source` property becomes the fact table in the Tabular model, named `'Fact'`.
If the `Source` is a 3-part table or view reference, it is translated to an M partition that accesses the SQL object by name.
If the `Source` is not a 3-part table or view reference, it is translated to an M partition with an embedded SQL query, with the entirety of the `Source` string as the SQL query.
The `Filter` property is ignored for purposes of translation.

For purposes of evaluating validation rules, the `View` is checked first, then each collection is validated in order: `Joins`, then `Dimensions`, then `Measures`.
Validation of the fact table, `Source` is done in a validation rule for the `View` object.

### Join

A [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join) represents a dimension table that is joined to the fact table:

- `Name`: Name of the joined table (used as an alias)
- `Source`: Source table or query for the join (e.g., "catalog.schema.dimension_table")
- `On`: Optional SQL boolean expression for the join condition
- `Using`: Optional list of column names for the join (alternative to `On`)
- `Joins`: Child joins (for snowflake schemas)

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

#### `Join` translation and validation

Nested `Join`s are not supported, i.e., only a strict star schema can be translated.
Only `On` joins with a single-field equijoin are supported for translation.
`Join`s each become a Tabular table, with an M partition defined according to the same rules as for the `View.Source` property.

`Join`s are validated in the order they appear in the Metric View definition.

### Dimension

A [`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) represents a field (column) in the Metric View:

- `Name`: The display name for the dimension
- `Expr`: The SQL expression defining the dimension (either a column reference or a SQL expression)

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

#### `Dimension` translation and validation

Each `Dimension` becomes a column in the Tabular model.
If the `Expr` is an unqualified field reference, it is added to the fact table.
If the `Expr` is a qualified reference (e.g., `table.field`), then it is added to the table created for the `Join` with the same name as the table-part of the qualified reference; if the table-part is `source`, it is added to the fact table.
In both the qualified and unqualified field reference cases, the field is added as a [`TOMWrapper.DataColumn`](xref:TabularEditor.TOMWrapper.DataColumn).
If the `Expr` is a SQL expression, then it is added as [`TOMWrapper.CalculatedColumn`](xref:TabularEditor.TOMWrapper.CalculatedColumn).
When the `Expr` is a SQL expression, we attempt to extract all field references; if all field references share the same table-part, then we add it to the table created for that `Join`, otherwise we add it to the fact table.
We do not translate SQL expressions for `Dimension.Expr` properties; the SQL expression is included as a comment in the DAX expression for the `CalculatedColumn`.
It is up to the user to translate these expressions.
We attempt to identify all field references in the SQL expression and add those to the Tabular model as `DataColumn`s if they do not already exist as a Metric View `Dimension`.

Some examples:

| `Expr`                                                | Translated as type | Added to table  | Note                                                                         |
|-------------------------------------------------------|--------------------|-----------------|------------------------------------------------------------------------------|
| `field1`                                              | `DataColumn`       | `'Fact'`        | unqualified field references are equivalent to those qualified with `source` |
| `source.field2`                                       | `DataColumn`       | `'Fact'`        | `source` is a reference to the `View.Source` property, aka the fact table    |
| `dimCustomer.key`                                     | `DataColumn`       | `'dimCustomer'` | there must be a `Join` whose `Name` property is `dimCustomer`                |
| `CONCAT(dimCustomer.FirstName, dimCustomer.LastName)` | `CalculatedColumn` | `'dimCustomer'` | all table-parts of the qualified name refer to the same name                 |
| `CONCAT(dimGeo.Country, dimCustomer.Address)`         | `CalculatedColumn` | `'Fact'`        | there are multiple distinct table-parts                                      |

`Dimension`s are validated in the order they appear in the Metric View definition.

### Measure

A [`Measure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) represents a named aggregation with business logic:

- `Name`: The display name for the measure
- `Expr`: The SQL aggregate expression defining the measure

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var measure in view.Measures ?? [])
{
    sb.AppendLine($"Measure: {measure.Name}");
    sb.AppendLine($"  Expression: {measure.Expr}");
}

Output(sb.ToString());
```

#### `Measure` translation and validation

All measures are added to the fact table.
Simple aggregations are translated into DAX expressions.
A simple aggregation is a single aggregation of a single field (e.g. `SUM(table.field)`).
Supported aggregations are sum, count, distinct count, max, min, and average.
Other expressions are passed through as a comment in the DAX expression of the Tabular measure.
We attempt to identify all field references in the SQL expression and add those to the Tabular model as `DataColumn`s if they do not already exist as a Metric View `Dimension`.

> [!WARNING]
> SQL and DAX are different languages with different semantics.
> It is possible that an automatically translated measure does not express the same computation in both Databricks Metric Views and Tabular models.
> It is up to the user to verify all code works as expected.

`Measure`s are validated in the order they appear in the Metric View definition.

## Using directives

When working with the Metric View object model in C# scripts, you may need to add a using directive to avoid naming conflicts with similarly-named types in the Tabular Object Model.
We recommend aliasing the namespace:

```csharp
// Alias to avoid conflicts with TOM types like Measure
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var view = SemanticBridge.MetricView.Model;

// Now you can reference types explicitly
foreach (MetricView.Dimension dim in view.Dimensions ?? [])
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

## References

- [`MetricView` namespace API documentation](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
- @semantic-bridge-how-tos
- [Databricks Metric View documentation](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)
- [Databricks Metric View YAML specification](https://learn.microsoft.com/en-us/azure/databricks/metric-views/data-modeling/syntax)
