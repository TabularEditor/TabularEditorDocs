---
uid: semantic-bridge-load-inspect
title: Load and Inspect a Metric View
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
# Load and Inspect a Metric View

This how-to demonstrates how to load a Databricks Metric View into Tabular Editor and explore its structure using C# scripts.
This is the foundational skill for all other Metric View operations.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not necessarily support the v1.1 Metric View features shown here.

[!INCLUDE [Sample Metric View](includes/sample-metricview.md)]

## Access the loaded Metric View

After loading, the Metric View is available in any script as `SemanticBridge.MetricView.Model`.
This returns a Metric View [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) object, the root of the [Metric View object graph](xref:semantic-bridge-metric-view-object-model).

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Version: {view.Version}");
sb.AppendLine($"Source (fact table): {view.Source}");
Output(sb.ToString());
```

## Inspect Metric View joins (dimension tables)

The Metric View `Joins` property contains the dimension tables joined to the fact.

```csharp
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

**Output:**

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

```csharp
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

**Output:**

```
Number of fields: 6

product_name         <- product.product_name
product_category     <- product.category
customer_segment     <- customer.segment
order_date           <- date.full_date
order_year           <- date.year
order_month          <- date.month_name
```

## Inspect Metric View measures

The Metric View `Measures` property contains all Metric View measure definitions with their aggregation expressions.

```csharp
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

**Output:**

```
Number of measures: 6

total_revenue        = SUM(revenue)
gross_margin         = SUM(revenue) - SUM(cost)
order_count          = COUNT(*)
avg_order_value      = AVG(revenue)
revenue_to_budget    = (SUM(revenue) - SUM(budget)) / SUM(budget)
unique_customers     = COUNT(DISTINCT customer_id)
```

## Generate a complete summary

Here is a complete script that outputs a formatted summary of the entire Metric View.

```csharp
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

## Next steps

Now that you can load and inspect a Metric View, you can:

- [Validate the Metric View](xref:semantic-bridge-metric-view-validation) to check for issues
- [Import the Metric View to Tabular](xref:semantic-bridge) to create tables, columns, and measures

## See also

- [Metric View Object Model](xref:semantic-bridge-metric-view-object-model)
- [Semantic Bridge Overview](xref:semantic-bridge)
