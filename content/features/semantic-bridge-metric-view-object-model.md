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
> It has limitations as documented below, and the API and feature surface area are subject to change.

The Semantic Bridge includes an object model representing a Databricks Metric View.
This allows you to work with Metric Views programmatically through C# scripts, similar to how you work with a Tabular model through the TOMWrapper.

Other than the [import GUI](xref:semantic-bridge#interface), all access to and interaction with a Metric View is through C# scripts.
All content in this document is referring to C# code that you would use in a [C# script](xref:csharp-scripts).

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
as those are all direct representations of the metric view spec.
Where these attributes are relevant to translation, we mention those in this document.

> [!NOTE]
> The object model was introduced in Tabular Editor 3.25.0 with support for Metric View v0.1.
> Support for Metric View v1.1 was added in Tabular Editor 3.26.2;
> this includes the `Comment` and `Materialization` properties on the `View`,
> `Cardinality` and `Rely` on `Join`,
> `Comment`, `DisplayName`, `Synonyms`, and `Format` on `Field` and `Measure`,
> `Window` on `Measure`,
> and the related translation behaviors documented below.

> [!NOTE]
> In the object model, we follow C# naming conventions, and so use `PascalCase` for all type and property names in the object model.
> The Metric View YAML specification follows a naming convention of `snake_case`.
> Other than changing the case, we do not change any naming convention from the YAML.

### View

[The `View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) object is the root of the Metric View and contains:

- `Version`: The Metric View specification version (e.g., "0.1")
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

#### `View` translation and validation

The `View.Source` property becomes the fact table in the Tabular model, named `'Fact'`.
If the `Source` is a 3-part table or view reference, it is translated to an M partition that accesses the SQL object by name.
If the `Source` is not a 3-part table or view reference, it is translated to an M partition with an embedded SQL query, with the entirety of the `Source` string as the SQL query.
The `View.Comment` becomes the TOM model `Description` property.

For purposes of evaluating validation rules, the `View` is checked first, then each collection is validated in order: `Joins`, then `Fields`, then `Measures`.
Validation of the fact table, `Source` is done in a validation rule for the `View` object.

The `Filter` property is ignored for purposes of translation;
if you need the logic included in `Filter`, you will have to manually add this.
Any defined `Materialization` is ignored for the purposes of translation;
these are query optimization metadata for executing queries on Databricks and not relevant to a TOM model.

> [!NOTE]
> Databricks has recently introduced a new multi-fact pattern.
> See the note about translation for `Join`s for more detail.

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

#### `Join` translation and validation

`Join`s each become a Tabular table, with an M partition defined according to the same rules as for the `View.Source` property.
Chains of `Join`s with `Join.Cardinality = Cardinality.ManyToOne` are translated as snowflake models in TOM, with equivalent relationship chains.

Only `On` joins with a single-field equijoin are supported for translation;
`Using` joins are skipped: the tables are created, but no TOM relationships are created.
`Rely` is not propagated into the TOM model in any way.
`Cardinality` of `OneToMany` is not translated; only the tables are created.

`Join`s are validated in the order they appear in the Metric View definition.

> [!NOTE]
> Databricks has recently introduced a new pattern using `one_to_many` cardinality against multiple `Join` sub-trees to implement a multi-fact model.
> We do not yet translate this pattern fully: we bring over all tables, fields, and measures, but do not create all relationships.
> A diagnostic warning is shown when importing a model following this pattern.

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

#### `Field` translation and validation

Each `Field` becomes a column in the Tabular model.
The TOM column's `Name` is `Field.DisplayName` if it is populated,
otherwise it is `Field.Name`.
`Field.Comment` becomes the TOM `Description`.
If the `Expr` is an unqualified field reference, it is added to the fact table.
If the `Expr` is a qualified reference (e.g., `table.field`),
then it is added to the table created for the `Join` with the same name as the table-part of the qualified reference;
if the table-part is `source`, it is added to the fact table.
In both the qualified and unqualified field reference cases,
the field is added as a [`TOMWrapper.DataColumn`](xref:TabularEditor.TOMWrapper.DataColumn).
If the `Expr` is a SQL expression,
then it is added as [`TOMWrapper.CalculatedColumn`](xref:TabularEditor.TOMWrapper.CalculatedColumn).
When the `Expr` is a SQL expression, we extract all field references;
if all field references share the same table-part,
then we add it to the table created for that `Join`,
otherwise we add it to the fact table.
We identify all field references in the SQL expression and add those to the Tabular model as `DataColumn`s if they do not already exist as a Metric View `Field`.
See the note below about `Format` translation.

We do not translate SQL expressions for `Field.Expr` properties; the SQL expression is included as a comment in the DAX expression for the `CalculatedColumn`.
It is up to the user to translate these expressions.

Some examples:

| `Expr`                                                | Translated as type | Added to table  | Note                                                                         |
|-------------------------------------------------------|--------------------|-----------------|------------------------------------------------------------------------------|
| `field1`                                              | `DataColumn`       | `'Fact'`        | unqualified field references are equivalent to those qualified with `source` |
| `source.field2`                                       | `DataColumn`       | `'Fact'`        | `source` is a reference to the `View.Source` property, aka the fact table    |
| `dimCustomer.key`                                     | `DataColumn`       | `'dimCustomer'` | there must be a `Join` whose `Name` property is `dimCustomer`                |
| `CONCAT(dimCustomer.FirstName, dimCustomer.LastName)` | `CalculatedColumn` | `'dimCustomer'` | all table-parts of the qualified name refer to the same name                 |
| `CONCAT(dimGeo.Country, dimCustomer.Address)`         | `CalculatedColumn` | `'Fact'`        | there are multiple distinct table-parts                                      |

`Field`s are validated in the order they appear in the Metric View definition.

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

#### `Measure` translation and validation

All measures are added to the fact table.
The TOM measure's `Name` is the metric view's `Measure.DisplayName` if it exists,
otherwise it is the metric view's `Measure.Name`.
The metric view `Measure.Comment` becomes the TOM measure's `Description`.
Simple aggregations are translated into equivalent DAX functions.
Supported aggregations are sum, count, distinct count, max, min, and average.
Basic arithmetic, common counting patterns, measure references, and parenthesis precedence are all supported for SQL->DAX translation.
Other expressions are passed through as a comment in the DAX expression of the Tabular measure.
We identify all field references in the SQL expression and add those to the Tabular model as `DataColumn`s if they do not already exist as a Metric View `Field`.
See the note below on `Format` translation.

Window specifications are not translated and cause fallback to a DAX comment.


> [!WARNING]
> SQL and DAX are different languages with different semantics.
> It is possible that an automatically translated measure does not express the same computation in both Databricks Metric Views and Tabular models.
> It is up to the user to verify all code works as expected.

`Measure`s are validated in the order they appear in the Metric View definition.

### `Format` translation

A metric view `Format` is translated to a TOM `FormatString` on the column or measure that carries it.
The target is a VBA-style format string, as used in TOM models.
The translation is best-effort:
if we can create a format string that exactly matches the configuration of the `Format`, then we do so;
if we cannot create an exact equivalent, then we fall back to an approximate equivalent and emit a warning you can review after import.

Currency, percentage, and number formats translate cleanly:
currency becomes a currency-symbol prefix on a grouped numeric format,
percentage becomes a percent format that honors the declared decimal places,
and number honors the declared decimal places and group separator, with the scientific abbreviation becoming an exponential format.

Year-month-day dates translate cleanly to an ISO date format;
locale long-month and locale numeric-month dates translate cleanly to the `Long Date` and `Short Date` named formats;
and hour-minute and hour-minute-second times translate cleanly to the `Short Time` and `Long Time` named formats.

The remaining formats cannot be precisely translated and emit a warning:
the compact number abbreviation and the byte format fall back to a plain numeric format;
the locale short-month date falls back to `Long Date`;
the year-week date falls back to an ISO date;
and a combined date-and-time format falls back to an ISO composite.

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
- @semantic-bridge-how-tos
- [Databricks Metric View documentation](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)
- [Databricks Metric View YAML specification](https://learn.microsoft.com/en-us/azure/databricks/metric-views/data-modeling/syntax)
