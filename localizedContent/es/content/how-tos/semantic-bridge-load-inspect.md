---
uid: semantic-bridge-load-inspect
title: Cargar e inspeccionar una Metric View
author: Greg Baldini
updated: 2026-07-02
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

# Cargar e inspeccionar una Metric View

Esta guía práctica muestra cómo cargar una Metric View de Databricks en Tabular Editor y explorar su estructura mediante C# Scripts.
Esta es la habilidad fundamental para todas las demás operaciones con una Metric View.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [Sample Metric View](includes/sample-metricview.md)]

## Acceder a la Metric View cargada

Después de cargarla, la Metric View está disponible en cualquier script en `SemanticBridge.MetricView.Model`.
Esto devuelve un objeto [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View), que es la raíz del [grafo de objetos de Metric View](xref:semantic-bridge-metric-view-object-model).

```csharp {run id=basic setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Version: {view.Version}");
sb.AppendLine($"Source (fact table): {view.Source}");
Output(sb.ToString());
```

**Salida**

```
Version: 1.1
Source (fact table): sales.fact.orders
```

## Inspeccionar las uniones de la Metric View (tablas de dimensiones)

La propiedad `Joins` de la Metric View contiene las tablas de dimensiones unidas a la tabla de hechos.

```csharp {run id=joins setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Number of joins: {view.Joins.Count}");
sb.AppendLine("");

foreach (var join in view.Joins)
{
    sb.AppendLine($"Join: {join.Name}");
    sb.AppendLine($"  Source: {join.Source}");
    sb.AppendLine($"  On: {join.On}");
    sb.AppendLine($"  Cardinality: {join.Cardinality?.ToString() ?? "ManyToOne (default)"}");
    sb.AppendLine("");
}

Output(sb.ToString());
```

**Salida:**

```
Number of joins: 3

Join: product
  Source: sales.dim.product
  On: source.product_id = product.product_id
  Cardinality: ManyToOne

Join: customer
  Source: sales.dim.customer
  On: source.customer_id = customer.customer_id
  Cardinality: ManyToOne

Join: date
  Source: sales.dim.date
  On: source.order_date = date.date_key
  Cardinality: ManyToOne
```

## Inspect Metric View fields

The Metric View `Fields` property contains all field definitions.

```csharp {run id=fields setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Number of fields: {view.Fields.Count}");
sb.AppendLine("");

foreach (var field in view.Fields)
{
    sb.AppendLine($"{field.Name,-20} <- {field.Expr}");
}

Output(sb.ToString());
```

**Salida:**

```
Number of fields: 6

product_name         <- product.product_name
product_category     <- product.category
customer_segment     <- customer.segment
order_date           <- date.full_date
order_year           <- date.year
order_month          <- date.month_name
```

## Inspeccionar las medidas de la Metric View

La propiedad `Measures` de la Metric View contiene todas las definiciones de medidas, junto con sus expresiones de agregación.

```csharp {run id=measures setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Number of measures: {view.Measures.Count}");
sb.AppendLine("");

foreach (var measure in view.Measures)
{
    sb.AppendLine($"{measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

**Salida:**

```
Number of measures: 6

total_revenue        = SUM(revenue)
gross_margin         = SUM(revenue) - SUM(cost)
order_count          = COUNT(*)
avg_order_value      = AVG(revenue)
revenue_to_budget    = (SUM(revenue) - SUM(budget)) / SUM(budget)
unique_customers     = COUNT(DISTINCT customer_id)
```

## Generar un resumen completo

Aquí tienes un script completo que genera un resumen con formato de la Metric View completa.

```csharp {run id=summary setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine("METRIC VIEW SUMMARY");
sb.AppendLine("===================");
sb.AppendLine("");
sb.AppendLine($"Version: {view.Version}");
sb.AppendLine($"Fact Source: {view.Source}");
sb.AppendLine("");

// Joins
sb.AppendLine($"JOINS ({view.Joins.Count})");
sb.AppendLine("---------");
foreach (var join in view.Joins)
{
    sb.AppendLine($"  {join.Name,-15} -> {join.Source}");
}
sb.AppendLine("");

// Fields
sb.AppendLine($"FIELDS ({view.Fields.Count})");
sb.AppendLine("--------------");
foreach (var field in view.Fields)
{
    sb.AppendLine($"  {field.Name,-20} <- {field.Expr}");
}
sb.AppendLine("");

// Measures
sb.AppendLine($"MEASURES ({view.Measures.Count})");
sb.AppendLine("------------");
foreach (var measure in view.Measures)
{
    sb.AppendLine($"  {measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

**Salida**

```
METRIC VIEW SUMMARY
===================

Version: 1.1
Fact Source: sales.fact.orders

JOINS (3)
---------
  product         -> sales.dim.product
  customer        -> sales.dim.customer
  date            -> sales.dim.date

FIELDS (6)
--------------
  product_name         <- product.product_name
  product_category     <- product.category
  customer_segment     <- customer.segment
  order_date           <- date.full_date
  order_year           <- date.year
  order_month          <- date.month_name

MEASURES (6)
------------
  total_revenue        = SUM(revenue)
  gross_margin         = SUM(revenue) - SUM(cost)
  order_count          = COUNT(*)
  avg_order_value      = AVG(revenue)
  revenue_to_budget    = (SUM(revenue) - SUM(budget)) / SUM(budget)
  unique_customers     = COUNT(DISTINCT customer_id)
```

## Pasos siguientes

Ahora que puedes cargar e inspeccionar una Metric View, puedes:

- [Add objects to a Metric View](xref:semantic-bridge-add-object)
- [Remove objects from a Metric View](xref:semantic-bridge-remove-object)
- [Rename a field](xref:semantic-bridge-rename-objects)
- [Validate the Metric View](xref:semantic-bridge-validate-default)
- [Import the Metric View to Tabular](xref:semantic-bridge-import)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
- [Información general de Semantic Bridge](xref:semantic-bridge)
