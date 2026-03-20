---
uid: semantic-bridge-load-inspect
title: 加载并检查指标视图
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

# 加载并检查指标视图

本操作指南演示如何将 Databricks Metric View 加载到 Tabular Editor 中，并使用 C# Script 探索其结构。
这是进行其他所有 Metric View 操作的基础。

## 示例 Metric View

[!INCLUDE [Sample Metric View](includes/sample-metricview.md)]

## 从文件加载 Metric View

使用 `SemanticBridge.MetricView.Load` 从磁盘上的 YAML 文件加载 Metric View。

```csharp
// 从文件路径加载
SemanticBridge.MetricView.Load("C:/MetricViews/sales-metrics.yaml");

// 确认已加载
Output($"已加载的 Metric View 版本：{SemanticBridge.MetricView.Model.Version}");
```

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## 访问已加载的 Metric View

加载完成后，可在任何脚本中通过 `SemanticBridge.MetricView.Model` 访问该 Metric View。
这会返回一个 Metric View 的 [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) 对象，它是 [Metric View 对象图](xref:semantic-bridge-metric-view-object-model) 的根节点。

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"版本：{view.Version}");
sb.AppendLine($"来源（事实表）：{view.Source}");
Output(sb.ToString());
```

## 检查 Metric View 的连接（维度表）

Metric View 的 `Joins` 属性包含与事实表连接的维度表。

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"连接数量: {view.Joins?.Count ?? 0}");
sb.AppendLine("");

foreach (var join in view.Joins ?? [])
{
    sb.AppendLine($"连接: {join.Name}");
    sb.AppendLine($"  来源: {join.Source}");
    sb.AppendLine($"  条件: {join.On}");
    sb.AppendLine("");
}

Output(sb.ToString());
```

**输出：**

```
联接数量: 3

联接: product
  来源: sales.dim.product
  On: product_id = product.product_id

联接: customer
  来源: sales.dim.customer
  On: customer_id = customer.customer_id

联接: date
  来源: sales.dim.date
  On: order_date = date.date_key
```

## 查看 Metric View 维度（字段）

Metric View 的 `Dimensions` 属性包含所有字段定义。

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"维度数量: {view.Dimensions?.Count ?? 0}");
sb.AppendLine("");

foreach (var dim in view.Dimensions ?? [])
{
    sb.AppendLine($"{dim.Name,-20} <- {dim.Expr}");
}

Output(sb.ToString());
```

**输出：**

```
维度数量: 6

product_name         <- product.product_name
product_category     <- product.category
customer_segment     <- customer.segment
order_date           <- date.full_date
order_year           <- date.year
order_month          <- date.month_name
```

## 查看 Metric View 度量值

Metric View 的 `Measures` 属性包含所有 Metric View 度量值定义及其聚合表达式。

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"度量值数量: {view.Measures?.Count ?? 0}");
sb.AppendLine("");

foreach (var measure in view.Measures ?? [])
{
    sb.AppendLine($"{measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

**输出：**

```
度量值数量: 4

total_revenue        = SUM(revenue)
order_count          = COUNT(order_id)
avg_order_value      = AVG(revenue)
unique_customers     = COUNT(DISTINCT customer_id)
```

## 生成完整摘要

下面是一段完整脚本，用于输出整个 Metric View 的格式化摘要。

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine("METRIC VIEW 摘要");
sb.AppendLine("===================");
sb.AppendLine("");
sb.AppendLine($"版本: {view.Version}");
sb.AppendLine($"事实数据源: {view.Source}");
sb.AppendLine("");

// Joins
sb.AppendLine($"连接 ({view.Joins?.Count ?? 0})");
sb.AppendLine("---------");
foreach (var join in view.Joins ?? [])
{
    sb.AppendLine($"  {join.Name,-15} -> {join.Source}");
}
sb.AppendLine("");

// Dimensions
sb.AppendLine($"维度 ({view.Dimensions?.Count ?? 0})");
sb.AppendLine("--------------");
foreach (var dim in view.Dimensions ?? [])
{
    sb.AppendLine($"  {dim.Name,-20} <- {dim.Expr}");
}
sb.AppendLine("");

// Measures
sb.AppendLine($"度量值 ({view.Measures?.Count ?? 0})");
sb.AppendLine("------------");
foreach (var measure in view.Measures ?? [])
{
    sb.AppendLine($"  {measure.Name,-20} = {measure.Expr}");
}

Output(sb.ToString());
```

## 后续步骤

现在你已经能够加载并检查 Metric View 了，你还可以：

- [验证 Metric View](xref:semantic-bridge-metric-view-validation)，以检查是否存在问题
- [将 Metric View 导入到 Tabular](xref:semantic-bridge)，以创建表、列和度量值

## 另见

- [Metric View 对象模型](xref:semantic-bridge-metric-view-object-model)
- [Semantic Bridge 概述](xref:semantic-bridge)
