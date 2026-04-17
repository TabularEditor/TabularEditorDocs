---
uid: semantic-bridge-serialize
title: Serializar una Metric View en formato YAML
author: Greg Baldini
updated: 2026-04-17
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

# Serializar una Metric View en formato YAML

Este procedimiento explica cómo volver a serializar una Metric View al formato YAML, ya sea como una cadena o guardándola en un archivo.

> [!WARNING]
> The public preview only supports v0.1 Metric View properties. Cualquier metadato v1.1 presente en una Metric View cargada se omite sin avisar y se perderá al serializar.
> No sobrescriba un archivo YAML de origen que contenga metadatos v1.1.

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## Serializar como cadena

Use `Serialize()` para obtener la representación en YAML:

```csharp
var yaml = SemanticBridge.MetricView.Serialize();

var sb = new System.Text.StringBuilder();
sb.AppendLine("Salida de YAML:");
sb.AppendLine("------------");
sb.AppendLine(yaml);
Output(sb.ToString());
```

## Guardar en un archivo

Use `Save(path)` para escribir el YAML directamente en el disco:

```csharp
var path = "C:/MetricViews/updated-sales-metrics.yaml";

SemanticBridge.MetricView.Save(path);

Output($"Metric View guardada en: {path}");
```

## Flujo de trabajo de ida y vuelta

Un flujo de trabajo habitual es cargar, modificar y guardar una Metric View:

```csharp
using System.Globalization;
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// La Metric View ya está cargada desde la inclusión anterior

var view = SemanticBridge.MetricView.Model;
var textInfo = CultureInfo.CurrentCulture.TextInfo;

// Modificar: renombrar las dimensiones de snake_case a Title Case
var renamed = view.Dimensions.Select(dim => new MetricView.Dimension
{
    Name = textInfo.ToTitleCase(dim.Name.Replace('_', ' ')),
    Expr = dim.Expr
}).ToList();

view.Dimensions.Clear();
foreach (var dim in renamed)
{
    view.Dimensions.Add(dim);
}

// Serializar para ver el resultado
var yaml = SemanticBridge.MetricView.Serialize();

var sb = new System.Text.StringBuilder();
sb.AppendLine("YAML modificado:");
sb.AppendLine("--------------");
sb.AppendLine(yaml);
Output(sb.ToString());
```

**Salida:**

```
YAML modificado:
--------------
version: 0.1
source: sales.fact.orders
joins:
- name: product
  source: sales.dim.product
  on: source.product_id = product.product_id
- name: customer
  source: sales.dim.customer
  on: source.customer_id = customer.customer_id
- name: date
  source: sales.dim.date
  on: source.order_date = date.date_key
dimensions:
- name: Product Name
  expr: product.product_name
- name: Product Category
  expr: product.category
- name: Customer Segment
  expr: customer.segment
- name: Order Date
  expr: date.full_date
- name: Order Year
  expr: date.year
- name: Order Month
  expr: date.month_name
measures:
- name: total_revenue
  expr: SUM(revenue)
- name: order_count
  expr: COUNT(order_id)
- name: avg_order_value
  expr: AVG(revenue)
- name: unique_customers
  expr: COUNT(DISTINCT customer_id)
```

## Ver también

- @semantic-bridge-load-inspect
- @semantic-bridge-import
- @semantic-bridge
