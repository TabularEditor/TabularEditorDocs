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
> 这些操作指南适用于 Tabular Editor 3.26.2 及更高版本。
> 较早版本不支持本文所示的 v1.1 指标视图功能。

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
版本: 1.1
源（事实表）: sales.fact.orders
```

## 检查 Metric View 的连接（维度表）

Metric View 的 `Joins` 属性包含与事实表连接的维度表。

```csharp {run id=joins setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"联接数量: {view.Joins.Count}");
sb.AppendLine("");

foreach (var join in view.Joins)
{
    sb.AppendLine($"联接: {join.Name}");
    sb.AppendLine($"  来源: {join.Source}");
    sb.AppendLine($"  连接条件: {join.On}");
    sb.AppendLine($"  基数: {join.Cardinality?.ToString() ?? "ManyToOne（默认）"}");
    sb.AppendLine("");
}

Output(sb.ToString());
```

**输出：**

```
联接数量: 3

联接: product
  来源: sales.dim.product
  连接条件: source.product_id = product.product_id
  基数: ManyToOne

联接: customer
  来源: sales.dim.customer
  连接条件: source.customer_id = customer.customer_id
  基数: ManyToOne

联接: date
  来源: sales.dim.date
  连接条件: source.order_date = date.date_key
  基数: ManyToOne
```

## 检查指标视图字段

指标视图的 `Fields` 属性包含所有字段定义。

```csharp {run id=fields setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"字段数量: {view.Fields.Count}");
sb.AppendLine("");

foreach (var field in view.Fields)
{
    sb.AppendLine($"{field.Name,-20} <- {field.Expr}");
}

Output(sb.ToString());
```

**输出：**

```
字段数量: 6

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

sb.AppendLine($"度量值数量: {view.Measures.Count}");
sb.AppendLine("");

foreach (var measure in view.Measures)
{
    sb.AppendLine($"{measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

**输出：**

```
度量值数量: 6

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

sb.AppendLine("指标视图摘要");
sb.AppendLine("===================");
sb.AppendLine("");
sb.AppendLine($"版本: {view.Version}");
sb.AppendLine($"事实数据源: {view.Source}");
sb.AppendLine("");

// Joins
sb.AppendLine($"联接 ({view.Joins.Count})");
sb.AppendLine("---------");
foreach (var join in view.Joins)
{
    sb.AppendLine($"  {join.Name,-15} -> {join.Source}");
}
sb.AppendLine("");

// Fields
sb.AppendLine($"字段 ({view.Fields.Count})");
sb.AppendLine("--------------");
foreach (var field in view.Fields)
{
    sb.AppendLine($"  {field.Name,-20} <- {field.Expr}");
}
sb.AppendLine("");

// Measures
sb.AppendLine($"度量值 ({view.Measures.Count})");
sb.AppendLine("------------");
foreach (var measure in view.Measures)
{
    sb.AppendLine($"  {measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

**输出**

```
指标视图摘要
===================

版本: 1.1
事实数据源: sales.fact.orders

联接 (3)
---------
  product         -> sales.dim.product
  customer        -> sales.dim.customer
  date            -> sales.dim.date

字段 (6)
--------------
  product_name         <- product.product_name
  product_category     <- product.category
  customer_segment     <- customer.segment
  order_date           <- date.full_date
  order_year           <- date.year
  order_month          <- date.month_name

度量值 (6)
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

- [向指标视图添加对象](xref:semantic-bridge-add-object)
- [从指标视图中移除对象](xref:semantic-bridge-remove-object)
- [重命名字段](xref:semantic-bridge-rename-objects)
- [验证指标视图](xref:semantic-bridge-validate-default)
- [将指标视图导入 Tabular](xref:semantic-bridge-import)

## 另见

- [Metric View 对象模型](xref:semantic-bridge-metric-view-object-model)
- [Semantic Bridge 概述](xref:semantic-bridge)
