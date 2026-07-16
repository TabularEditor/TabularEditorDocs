---
uid: semantic-bridge-load-inspect
title: 加载并检查指标视图
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

# 加载并检查指标视图

本操作指南演示如何将 Databricks Metric View 加载到 Tabular Editor 中，并使用 C# Script 探索其结构。
这是进行其他所有 Metric View 操作的基础。

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [Sample Metric View](includes/sample-metricview.md)]

## 访问已加载的 Metric View

加载完成后，可在任何脚本中通过 `SemanticBridge.MetricView.Model` 访问该 Metric View。
这会返回一个 Metric View 的 [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) 对象，它是 [Metric View 对象图](xref:semantic-bridge-metric-view-object-model) 的根节点。

```csharp {run id=basic setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"版本：{view.Version}");
sb.AppendLine($"来源（事实表）：{view.Source}");
Output(sb.ToString());
```

**输出**

```
Version: 1.1
Source (fact table): sales.fact.orders
```

## 检查 Metric View 的连接（维度表）

Metric View 的 `Joins` 属性包含与事实表连接的维度表。

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

**输出：**

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

**输出：**

```
Number of fields: 6

product_name         <- product.product_name
product_category     <- product.category
customer_segment     <- customer.segment
order_date           <- date.full_date
order_year           <- date.year
order_month          <- date.month_name
```

## 查看 Metric View 度量值

Metric View 的 `Measures` 属性包含所有 Metric View 度量值定义及其聚合表达式。

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

**输出：**

```
Number of measures: 6

total_revenue        = SUM(revenue)
gross_margin         = SUM(revenue) - SUM(cost)
order_count          = COUNT(*)
avg_order_value      = AVG(revenue)
revenue_to_budget    = (SUM(revenue) - SUM(budget)) / SUM(budget)
unique_customers     = COUNT(DISTINCT customer_id)
```

## 生成完整摘要

下面是一段完整脚本，用于输出整个 Metric View 的格式化摘要。

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

**输出**

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

## 后续步骤

现在你已经能够加载并检查 Metric View 了，你还可以：

- [Add objects to a Metric View](xref:semantic-bridge-add-object)
- [Remove objects from a Metric View](xref:semantic-bridge-remove-object)
- [Rename a field](xref:semantic-bridge-rename-objects)
- [Validate the Metric View](xref:semantic-bridge-validate-default)
- [Import the Metric View to Tabular](xref:semantic-bridge-import)

## 另见

- [Metric View 对象模型](xref:semantic-bridge-metric-view-object-model)
- [Semantic Bridge 概述](xref:semantic-bridge)
