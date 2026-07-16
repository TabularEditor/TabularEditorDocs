---
uid: semantic-bridge-metric-view-object-model
title: Modelo de objetos de la Metric View de Semantic Bridge
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

# Modelo de objetos de la Metric View

<!--
SUMMARY: Overview of the Metric View object model built into the Semantic Bridge.
-->

> [!NOTE]
> The Semantic Bridge is in public preview.
> The 3.25.0 release supports Metric View v0.1 metadata, and the 3.26.2 release supports Metric View v1.1 metadata.

The Semantic Bridge includes an object model representing a [Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/).
Esto te permite trabajar con Metric Views mediante programación a través de C# Scripts, de forma similar a como trabajas con un modelo tabular a través de TOMWrapper.

Aparte de la [GUI de importación](xref:semantic-bridge#interface), todo el acceso y la interacción con una Metric View se realizan mediante C# Scripts.
All content in this document is referring to C# code that you would use in a [C# script](xref:csharp-scripts).

## Carga y acceso a la Metric View

You can load a Metric View with [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) or [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A).
This stores the deserialized Metric View as [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model).
Esta propiedad devuelve un objeto [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View), que es la raíz del grafo de objetos de la Metric View.

```csharp {compile}
// Cargar una Metric View desde el disco
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");

// Acceder a la View cargada
var view = SemanticBridge.MetricView.Model;
Output($"Versión de Metric View: {view.Version}\r\nOrigen: {view.Source}");
```

Al igual que un modelo tabular —y a diferencia de la mayoría de los demás objetos a los que quizá esté acostumbrado en un C# Script—, Metric View es persistente entre varias ejecuciones del script.
Esto significa que puedes cargar una Metric View una sola vez y hacer referencia a ella en ejecuciones posteriores de scripts sin tener que volver a cargarla cada vez.
Solo se carga una única Metric View y está disponible en todos los scripts como `SemanticBridge.MetricView.Model`, como se mencionó anteriormente.
Este comportamiento es similar al del modelo tabular en scripts de C#, que siempre está disponible simplemente como `Model`.

[!INCLUDE [sample](../how-tos/includes/sample-metricview.md)]

## Objetos de dominio

The object model consists of four main types that correspond to the structure of a Metric View YAML file.
We do not repeat the entire specification here, so we encourage you to reference the [Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/)
and our [own API reference for the object model](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView).

| Referencia de la API                                                                  | Descripción                                                                         |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View)      | El objeto raíz que representa la Metric View completa                               |
| [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join)      | Una definición de unión que conecta una tabla de dimensiones con la tabla de hechos |
| [`Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field)    | Una definición de campo (columna) en la Metric View              |
| [`Medida`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) | Una definición de agregación que representa la lógica de negocio                    |

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
> La especificación YAML de Metric View sigue una convención de nomenclatura `snake_case`.
> Serialization and deserialization convert between these, so C# scripts use `PascalCase` and the YAML we read and write stays spec-compliant `snake_case`.

### Vista

[The `View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) object is the root of the Metric View and contains:

- `Version`: The Metric View specification version (e.g., "1.1")
- `Source`: Los datos de origen de la tabla de hechos (p. ej., "catalog.schema.table")
- `Filter`: Expresión booleana SQL opcional que se aplica a todas las consultas
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

**Salida**

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

- `Name`: Nombre de la tabla unida (se usa como alias)
- `Source`: Tabla de origen o consulta para el join (p. ej., "catalog.schema.dimension_table")
- `On`: Expresión booleana SQL opcional para la condición del join
- `Using`: Lista opcional de nombres de columna para el join (alternativa a `On`)
- `Joins`: Uniones secundarias (para esquemas en copo de nieve)
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

**Salida**

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

### Campo

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

**Salida**

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

### Medida

[A `Measure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) represents a named aggregation with business logic:

- `Name`: The name of the measure, referenced in Metric View expressions as `MEASURE(<name>)`
- `Expr`: La expresión de agregación SQL que define la medida
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

**Salida**

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

## Directivas using

Al trabajar con el modelo de objetos de Metric View en C# Script, es posible que necesite agregar una directiva using para evitar conflictos de nombres con tipos que tienen nombres similares en el Tabular Object Model.
Recomendamos asignar un alias al espacio de nombres:

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

### Acceso a objetos por nombre

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

## Referencias

- [Documentación de la API del espacio de nombres `MetricView`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-metric-view-validation
- @semantic-bridge-metric-view-tabular-translation
- [Semantic Bridge how-tos for detailed examples](xref:semantic-bridge-how-tos)
- [Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/)
- [Metric View YAML specification](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference)
