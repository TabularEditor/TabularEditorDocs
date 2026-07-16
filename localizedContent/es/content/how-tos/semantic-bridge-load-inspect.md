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
> Estas guías están dirigidas a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de Metric View v1.1 que se muestran aquí.

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
Versión: 1.1
Fuente (tabla de hechos): sales.fact.orders
```

## Inspeccionar las uniones de la Metric View (tablas de dimensiones)

La propiedad `Joins` de la Metric View contiene las tablas de dimensiones unidas a la tabla de hechos.

```csharp {run id=joins setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Número de uniones: {view.Joins.Count}");
sb.AppendLine("");

foreach (var join in view.Joins)
{
    sb.AppendLine($"Unión: {join.Name}");
    sb.AppendLine($"  Fuente: {join.Source}");
    sb.AppendLine($"  Condición: {join.On}");
    sb.AppendLine($"  Cardinalidad: {join.Cardinality?.ToString() ?? "ManyToOne (predeterminado)"}");
    sb.AppendLine("");
}

Output(sb.ToString());
```

**Salida:**

```
Número de uniones: 3

Unión: product
  Fuente: sales.dim.product
  Condición: source.product_id = product.product_id
  Cardinalidad: ManyToOne

Unión: customer
  Fuente: sales.dim.customer
  Condición: source.customer_id = customer.customer_id
  Cardinalidad: ManyToOne

Unión: date
  Fuente: sales.dim.date
  Condición: source.order_date = date.date_key
  Cardinalidad: ManyToOne
```

## Inspeccionar los campos de Metric View

La propiedad `Fields` de Metric View contiene todas las definiciones de campos.

```csharp {run id=fields setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Número de campos: {view.Fields.Count}");
sb.AppendLine("");

foreach (var field in view.Fields)
{
    sb.AppendLine($"{field.Name,-20} <- {field.Expr}");
}

Output(sb.ToString());
```

**Salida:**

```
Número de campos: 6

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

sb.AppendLine($"Número de medidas: {view.Measures.Count}");
sb.AppendLine("");

foreach (var measure in view.Measures)
{
    sb.AppendLine($"{measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

**Salida:**

```
Número de medidas: 6

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

sb.AppendLine("RESUMEN DE METRIC VIEW");
sb.AppendLine("======================");
sb.AppendLine("");
sb.AppendLine($"Versión: {view.Version}");
sb.AppendLine($"Fuente de hechos: {view.Source}");
sb.AppendLine("");

// Uniones
sb.AppendLine($"UNIONES ({view.Joins.Count})");
sb.AppendLine("---------");
foreach (var join in view.Joins)
{
    sb.AppendLine($"  {join.Name,-15} -> {join.Source}");
}
sb.AppendLine("");

// Campos
sb.AppendLine($"CAMPOS ({view.Fields.Count})");
sb.AppendLine("--------------");
foreach (var field in view.Fields)
{
    sb.AppendLine($"  {field.Name,-20} <- {field.Expr}");
}
sb.AppendLine("");

// Medidas
sb.AppendLine($"MEDIDAS ({view.Measures.Count})");
sb.AppendLine("------------");
foreach (var measure in view.Measures)
{
    sb.AppendLine($"  {measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

**Salida**

```
RESUMEN DE METRIC VIEW
======================

Versión: 1.1
Fuente de hechos: sales.fact.orders

UNIONES (3)
---------
  product         -> sales.dim.product
  customer        -> sales.dim.customer
  date            -> sales.dim.date

CAMPOS (6)
--------------
  product_name         <- product.product_name
  product_category     <- product.category
  customer_segment     <- customer.segment
  order_date           <- date.full_date
  order_year           <- date.year
  order_month          <- date.month_name

MEDIDAS (6)
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

- [Agregar objetos a Metric View](xref:semantic-bridge-add-object)
- [Quitar objetos de Metric View](xref:semantic-bridge-remove-object)
- [Cambiar el nombre de un campo](xref:semantic-bridge-rename-objects)
- [Validar Metric View](xref:semantic-bridge-validate-default)
- [Importar Metric View a un modelo tabular](xref:semantic-bridge-import)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
- [Información general de Semantic Bridge](xref:semantic-bridge)
