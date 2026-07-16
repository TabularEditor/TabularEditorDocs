---
uid: semantic-bridge-serialize
title: 将 Metric View 序列化为 YAML
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

# 将 Metric View 序列化为 YAML

本操作指南演示如何将 Metric View 序列化回 YAML 格式：既可以作为字符串获取，也可以保存到文件中。

> [!NOTE]
> 这些操作指南面向 Tabular Editor 3.26.2 及更高版本。
> 较早的版本不支持此处展示的 v1.1 指标视图功能。

[!INCLUDE [sample](includes/sample-metricview.md)]

## 序列化为字符串

使用 `Serialize()` 获取 YAML 表示形式。
这只是将上面加载的 YAML 重新序列化。

```csharp {run id=serialize setup=mv-sample after=none output=true}
var yaml = SemanticBridge.MetricView.Serialize();

var sb = new System.Text.StringBuilder();
sb.AppendLine("YAML output:");
sb.AppendLine("------------");
sb.AppendLine(yaml);
Output(sb.ToString());
```

**输出**

```
YAML 输出：
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
  display_name: Product Category
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
  display_name: Total Revenue
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
  display_name: Revenue vs Budget
  format:
    type: percentage
    decimal_places:
      type: max
      places: 1
- name: unique_customers
  expr: COUNT(DISTINCT customer_id)
```

## 保存到文件

使用 `Save(path)` 将 YAML 直接写入磁盘。
这会将上面加载的指标视图写入磁盘。

```csharp {compile}
var path = "C:/MetricViews/updated-sales-metrics.yaml";

SemanticBridge.MetricView.Save(path);

Output($"Metric View saved to: {path}");
```

## 往返式工作流

一种常见的工作流是加载、修改并保存 Metric View：

```csharp {run id=roundtrip setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

// 为字段设置显示名称，然后序列化以确认序列化/反序列化后保持一致
view.Fields["order_month"].DisplayName = "Order Month";

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
  display_name: Product Category
- name: customer_segment
  expr: customer.segment
- name: order_date
  expr: date.full_date
- name: order_year
  expr: date.year
- name: order_month
  expr: date.month_name
  display_name: Order Month
measures:
- name: total_revenue
  expr: SUM(revenue)
  display_name: Total Revenue
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
  display_name: Revenue vs Budget
  format:
    type: percentage
    decimal_places:
      type: max
      places: 1
- name: unique_customers
  expr: COUNT(DISTINCT customer_id)
```

## 后续步骤

- [加载并检查指标视图](xref:semantic-bridge-load-inspect)
- [将指标视图导入到 Tabular](xref:semantic-bridge-import)

## 另见

- [Semantic Bridge 概述](xref:semantic-bridge)
