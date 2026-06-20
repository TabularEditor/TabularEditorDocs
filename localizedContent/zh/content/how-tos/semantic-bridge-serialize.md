---
uid: semantic-bridge-serialize
title: 将 Metric View 序列化为 YAML
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

# 将 Metric View 序列化为 YAML

本操作指南演示如何将 Metric View 序列化回 YAML 格式：既可以作为字符串获取，也可以保存到文件中。

> [!WARNING]
> 公共预览版仅支持 v0.1 版的 Metric View 属性。 如果加载的 Metric View 中包含任何 v1.1 元数据，系统会静默忽略；在序列化时，这些元数据将会丢失。
> 不要覆盖包含 v1.1 元数据的源 YAML 文件。

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## 序列化为字符串

使用 `Serialize()` 获取 YAML 表示形式：

```csharp
var yaml = SemanticBridge.MetricView.Serialize();

var sb = new System.Text.StringBuilder();
sb.AppendLine("YAML output:");
sb.AppendLine("------------");
sb.AppendLine(yaml);
Output(sb.ToString());
```

## 保存到文件

使用 `Save(path)` 将 YAML 直接写入磁盘：

```csharp
var path = "C:/MetricViews/updated-sales-metrics.yaml";

SemanticBridge.MetricView.Save(path);

Output($"Metric View saved to: {path}");
```

## 往返式工作流

一种常见的工作流是加载、修改并保存 Metric View：

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

**输出：**

```
修改后的 YAML：
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
- name: 客户分段
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

## 另见

- @semantic-bridge-load-inspect
- @semantic-bridge-import
- @semantic-bridge
