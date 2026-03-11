---
uid: semantic-bridge-serialize
title: Serialize a Metric View to YAML
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
# Serialize a Metric View to YAML

This how-to demonstrates how to serialize a Metric View back to YAML format, either as a string or saved to a file.

> [!WARNING]
> The MVP only supports v0.1 Metric View properties. Any v1.1 metadata present in a loaded Metric View is silently ignored and will be lost when you serialize.
> Do not overwrite a source YAML file that contains v1.1 metadata.


[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## Serialize to a string

Use `Serialize()` to get the YAML representation:

```csharp
var yaml = SemanticBridge.MetricView.Serialize();

var sb = new System.Text.StringBuilder();
sb.AppendLine("YAML output:");
sb.AppendLine("------------");
sb.AppendLine(yaml);
Output(sb.ToString());
```

## Save to a file

Use `Save(path)` to write the YAML directly to disk:

```csharp
var path = "C:/MetricViews/updated-sales-metrics.yaml";

SemanticBridge.MetricView.Save(path);

Output($"Metric View saved to: {path}");
```

## Round-trip workflow

A common workflow is to load, modify, and save a Metric View:

```csharp
using System.Globalization;
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// The Metric View is already loaded from the include above

var view = SemanticBridge.MetricView.Model;
var textInfo = CultureInfo.CurrentCulture.TextInfo;

// Modify: rename dimensions from snake_case to Title Case
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

// Serialize to see the result
var yaml = SemanticBridge.MetricView.Serialize();

var sb = new System.Text.StringBuilder();
sb.AppendLine("Modified YAML:");
sb.AppendLine("--------------");
sb.AppendLine(yaml);
Output(sb.ToString());
```

**Output:**

```
Modified YAML:
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

## See also

- @semantic-bridge-load-inspect
- @semantic-bridge-import
- @semantic-bridge
