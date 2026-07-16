---
uid: semantic-bridge-serialize
title: Serializar una Metric View en formato YAML
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

# Serializar una Metric View en formato YAML

Este procedimiento explica cómo volver a serializar una Metric View al formato YAML, ya sea como una cadena o guardándola en un archivo.

> [!NOTE]
> Estas guías están pensadas para Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las funcionalidades de la vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Serializar como cadena

Use `Serialize()` para obtener la representación en YAML.
Esto simplemente vuelve a serializar el YAML que cargó anteriormente.

```csharp {run id=serialize setup=mv-sample after=none output=true}
var yaml = SemanticBridge.MetricView.Serialize();

var sb = new System.Text.StringBuilder();
sb.AppendLine("Salida de YAML:");
sb.AppendLine("------------");
sb.AppendLine(yaml);
Output(sb.ToString());
```

**Salida**

```
Salida en YAML:
------------
version: 1.1
source: sales.fact.orders
joins:
- name: product
  source: sales.dim.product
  on: source.product_id = product.product_id
  cardinality: many_to_one
- name: customer
  source: sales.dim.customer
  on: source.customer_id = customer.customer_id
  cardinality: many_to_one
- name: date
  source: sales.dim.date
  on: source.order_date = date.date_key
  cardinality: many_to_one
fields:
- name: product_name
  expr: product.product_name
- name: product_category
  expr: product.category
  display_name: Categoría de producto
- name: customer_segment
  expr: customer.segment
- name: order_date
  expr: date.full_date
- name: order_year
  expr: date.year
- name: order_month
  expr: date.month_name
measures:
- name: total_revenue
  expr: SUM(revenue)
  display_name: Ingresos totales
  format:
    type: currency
    decimal_places:
      type: exact
      places: 2
    currency_code: USD
- name: gross_margin
  expr: SUM(revenue) - SUM(cost)
- name: order_count
  expr: COUNT(*)
- name: avg_order_value
  expr: AVG(revenue)
- name: revenue_to_budget
  expr: (SUM(revenue) - SUM(budget)) / SUM(budget)
  display_name: Ingresos frente al presupuesto
  format:
    type: percentage
    decimal_places:
      type: max
      places: 1
- name: unique_customers
  expr: COUNT(DISTINCT customer_id)
```

## Guardar en un archivo

Use `Save(path)` para escribir el YAML directamente en disco.
Esto guardará en disco la vista de métricas que cargó anteriormente.

```csharp {compile}
var path = "C:/MetricViews/updated-sales-metrics.yaml";

SemanticBridge.MetricView.Save(path);

Output($"Metric View guardada en: {path}");
```

## Flujo de trabajo de ida y vuelta

Un flujo de trabajo habitual es cargar, modificar y guardar una Metric View:

```csharp {run id=roundtrip setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

// establecer un nombre para mostrar en un campo y luego serializar para confirmar que los cambios se conservan
view.Fields["order_month"].DisplayName = "Mes del pedido";

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
version: 1.1
source: sales.fact.orders
joins:
- name: product
  source: sales.dim.product
  on: source.product_id = product.product_id
  cardinality: many_to_one
- name: customer
  source: sales.dim.customer
  on: source.customer_id = customer.customer_id
  cardinality: many_to_one
- name: date
  source: sales.dim.date
  on: source.order_date = date.date_key
  cardinality: many_to_one
fields:
- name: product_name
  expr: product.product_name
- name: product_category
  expr: product.category
  display_name: Categoría de producto
- name: customer_segment
  expr: customer.segment
- name: order_date
  expr: date.full_date
- name: order_year
  expr: date.year
- name: order_month
  expr: date.month_name
  display_name: Mes del pedido
measures:
- name: total_revenue
  expr: SUM(revenue)
  display_name: Ingresos totales
  format:
    type: currency
    decimal_places:
      type: exact
      places: 2
    currency_code: USD
- name: gross_margin
  expr: SUM(revenue) - SUM(cost)
- name: order_count
  expr: COUNT(*)
- name: avg_order_value
  expr: AVG(revenue)
- name: revenue_to_budget
  expr: (SUM(revenue) - SUM(budget)) / SUM(budget)
  display_name: Ingresos frente al presupuesto
  format:
    type: percentage
    decimal_places:
      type: max
      places: 1
- name: unique_customers
  expr: COUNT(DISTINCT customer_id)
```

## Pasos a seguir

- [Cargar e inspeccionar una vista de métricas](xref:semantic-bridge-load-inspect)
- [Importar una vista de métricas en Tabular](xref:semantic-bridge-import)

## Ver también

- [Información general de Semantic Bridge](xref:semantic-bridge)
