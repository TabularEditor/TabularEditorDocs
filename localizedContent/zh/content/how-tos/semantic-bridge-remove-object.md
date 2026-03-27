---
uid: semantic-bridge-remove-object
title: 从 Metric View 中移除对象
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

# 从 Metric View 中移除对象

本文演示如何从已加载的 Metric View 中移除其维度。
类似的方法适用于 Metric View 中的所有集合。

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

> [!NOTE]
> 这里的每个移除脚本都会影响当前已加载的 Metric View。
> 如果你想把这些脚本都运行一遍，请确保在每次移除操作前都先运行上面的 `Deserialize`。

## 按名称移除

找到要移除的 Metric View 维度，并将其从集合中移除：

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensions before: {view.Dimensions.Count}");

var dimToRemove = view.Dimensions.FirstOrDefault(d => d.Name == "order_month");
if (dimToRemove != null)
{
    view.Dimensions.Remove(dimToRemove);
    sb.AppendLine($"Removed: {dimToRemove.Name}");
}

sb.AppendLine($"Dimensions after: {view.Dimensions.Count}");
Output(sb.ToString());
```

**输出：**

```
Dimensions before: 6
Removed: order_month
Dimensions after: 5
```

注意：如果你连续运行两次上述脚本，不会再移除任何内容；移除前后计数都会是 5。

## 移除多个 Metric View 维度

使用 LINQ 进行筛选并重建集合：

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensions before: {view.Dimensions.Count}");

// Remove all date-related dimensions
string[] toRemove = ["order_date", "order_year", "order_month"];

var toKeep = view.Dimensions
    .Where(d => !toRemove.Contains(d.Name))
    .ToList();

// Clear and repopulate
view.Dimensions.Clear();
foreach (var dim in toKeep)
{
    view.Dimensions.Add(dim);
}

sb.AppendLine($"Dimensions after: {view.Dimensions.Count}");
sb.AppendLine();
sb.AppendLine("Remaining dimensions:");
sb.AppendLine("---------------------");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name}");
}

Output(sb.ToString());
```

**输出：**

```
移除前维度数：6
移除后维度数：3

剩余维度：
---------------------
  product_name
  product_category
  customer_segment
```

## 从指定表中移除 Metric View 维度

移除所有引用日期表的 Metric View 维度。

> [!WARNING]
> 此示例不保证能够移除所有且仅移除引用给定 Metric View Join 的 Metric View 维度。
> Metric View 维度可能包含近乎任意的 SQL 表达式，也可能引用先前定义的 Metric View 维度。
> 此示例仅用于说明。

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensions before: {view.Dimensions.Count}");

var toRemove = view.Dimensions
    .Where(d => d.Expr.StartsWith("date."))
    .ToList();

foreach (var dim in toRemove)
{
    view.Dimensions.Remove(dim);
    sb.AppendLine($"Removed: {dim.Name} ({dim.Expr})");
}

sb.AppendLine($"Dimensions after: {view.Dimensions.Count}");
Output(sb.ToString());
```

**输出：**

```
移除前维度数：6
已移除：order_date (date.full_date)
已移除：order_year (date.year)
已移除：order_month (date.month_name)
移除后维度数：3
```

## 另请参阅

- @semantic-bridge-add-object
- @semantic-bridge-rename-objects
- @semantic-bridge-serialize
