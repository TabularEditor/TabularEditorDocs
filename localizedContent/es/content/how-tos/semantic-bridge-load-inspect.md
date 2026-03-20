---
uid: semantic-bridge-load-inspect
title: Cargar e inspeccionar una Metric View
author: Greg Baldini
updated: 2025-01-27
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

## Metric View de ejemplo

[!INCLUDE [Sample Metric View](includes/sample-metricview.md)]

## Cargar una Metric View desde un archivo

Use `SemanticBridge.MetricView.Load` para cargar una Metric View desde un archivo YAML almacenado en el disco.

```csharp
// Load from a file path
SemanticBridge.MetricView.Load("C:/MetricViews/sales-metrics.yaml");

// Confirm it loaded
Output($"Loaded Metric View version: {SemanticBridge.MetricView.Model.Version}");
```

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## Acceder a la Metric View cargada

Después de cargarla, la Metric View está disponible en cualquier script en `SemanticBridge.MetricView.Model`.
Esto devuelve un objeto [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View), que es la raíz del [grafo de objetos de Metric View](xref:semantic-bridge-metric-view-object-model).

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Version: {view.Version}");
sb.AppendLine($"Source (fact table): {view.Source}");
Output(sb.ToString());
```

## Inspeccionar las uniones de la Metric View (tablas de dimensiones)

La propiedad `Joins` de la Metric View contiene las tablas de dimensiones unidas a la tabla de hechos.

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Número de joins: {view.Joins?.Count ?? 0}");
sb.AppendLine("");

foreach (var join in view.Joins ?? [])
{
    sb.AppendLine($"Join: {join.Name}");
    sb.AppendLine($"  Origen: {join.Source}");
    sb.AppendLine($"  On: {join.On}");
    sb.AppendLine("");
}

Output(sb.ToString());
```

**Salida:**

```
Número de joins: 3

Join: product
  Origen: sales.dim.product
  On: product_id = product.product_id

Join: customer
  Origen: sales.dim.customer
  On: customer_id = customer.customer_id

Join: date
  Origen: sales.dim.date
  On: order_date = date.date_key
```

## Inspeccionar las dimensiones (campos) de la Metric View

La propiedad `Dimensions` de la Metric View contiene todas las definiciones de campos.

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Número de dimensiones: {view.Dimensions?.Count ?? 0}");
sb.AppendLine("");

foreach (var dim in view.Dimensions ?? [])
{
    sb.AppendLine($"{dim.Name,-20} <- {dim.Expr}");
}

Output(sb.ToString());
```

**Salida:**

```
Número de dimensiones: 6

product_name         <- product.product_name
product_category     <- product.category
customer_segment     <- customer.segment
order_date           <- date.full_date
order_year           <- date.year
order_month          <- date.month_name
```

## Inspeccionar las medidas de la Metric View

La propiedad `Measures` de la Metric View contiene todas las definiciones de medidas, junto con sus expresiones de agregación.

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Número de medidas: {view.Measures?.Count ?? 0}");
sb.AppendLine("");

foreach (var measure in view.Measures ?? [])
{
    sb.AppendLine($"{measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

**Salida:**

```
Número de medidas: 4

total_revenue        = SUM(revenue)
order_count          = COUNT(order_id)
avg_order_value      = AVG(revenue)
unique_customers     = COUNT(DISTINCT customer_id)
```

## Generar un resumen completo

Aquí tienes un script completo que genera un resumen con formato de la Metric View completa.

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine("RESUMEN DE LA METRIC VIEW");
sb.AppendLine("=========================");
sb.AppendLine("");
sb.AppendLine($"Versión: {view.Version}");
sb.AppendLine($"Fuente de hechos: {view.Source}");
sb.AppendLine("");

// Joins
sb.AppendLine($"JOINS ({view.Joins?.Count ?? 0})");
sb.AppendLine("---------");
foreach (var join in view.Joins ?? [])
{
    sb.AppendLine($"  {join.Name,-15} -> {join.Source}");
}
sb.AppendLine("");

// Dimensions
sb.AppendLine($"DIMENSIONES ({view.Dimensions?.Count ?? 0})");
sb.AppendLine("--------------");
foreach (var dim in view.Dimensions ?? [])
{
    sb.AppendLine($"  {dim.Name,-20} <- {dim.Expr}");
}
sb.AppendLine("");

// Measures
sb.AppendLine($"MEDIDAS ({view.Measures?.Count ?? 0})");
sb.AppendLine("------------");
foreach (var measure in view.Measures ?? [])
{
    sb.AppendLine($"  {measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

## Pasos siguientes

Ahora que puedes cargar e inspeccionar una Metric View, puedes:

- [Validar la Metric View](xref:semantic-bridge-metric-view-validation) para detectar problemas
- [Importar la Metric View a Tabular](xref:semantic-bridge) para crear tablas, columnas y medidas

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
- [Información general de Semantic Bridge](xref:semantic-bridge)
