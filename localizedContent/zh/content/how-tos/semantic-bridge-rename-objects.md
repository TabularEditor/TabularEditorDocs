---
uid: semantic-bridge-rename-objects
title: 在指标视图中重命名对象
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

# 在指标视图中重命名对象

本操作指南演示如何使用“复制-修改”模式，对指标视图的维度进行批量重命名。
同样的模式也适用于指标视图中的所有集合。
同样的模式也适用于指标视图中的所有集合。

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## 复制-修改模式

由于指标视图的维度名称是集合中对象的属性，最简单的做法是：

1. 创建新的指标视图 `Dimension` 对象，并使用修改后的名称
2. 清空原始集合
3. 将新对象添加回集合

这样可以避免在迭代时修改对象所带来的问题。

## 将 snake_case 转换为 Title Case

将指标视图维度名称从 `product_name` 转换为 `Product Name`：

```csharp
using System.Globalization;
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;
var textInfo = CultureInfo.CurrentCulture.TextInfo;

var sb = new System.Text.StringBuilder();
sb.AppendLine("BEFORE");
sb.AppendLine("------");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name}");
}

// Create renamed dimensions
var renamed = view.Dimensions.Select(dim => new MetricView.Dimension
{
    Name = textInfo.ToTitleCase(dim.Name.Replace('_', ' ')),
    Expr = dim.Expr
}).ToList();

// Replace the collection
view.Dimensions.Clear();
foreach (var dim in renamed)
{
    view.Dimensions.Add(dim);
}

sb.AppendLine();
sb.AppendLine("AFTER");
sb.AppendLine("-----");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name}");
}

Output(sb.ToString());
```

**输出：**

```
BEFORE
------
  product_name
  product_category
  customer_segment
  order_date
  order_year
  order_month

AFTER
-----
  产品名称
  产品类别
  客户分段
  订单日期
  订单年份
  订单月份
```

## 使用映射字典进行重命名

使用查找表应用特定重命名：

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// 定义重命名映射
var renames = new Dictionary<string, string>
{
    { "product_name", "Product" },
    { "product_category", "Category" },
    { "customer_segment", "Segment" },
    { "order_date", "Date" },
    { "order_year", "Year" },
    { "order_month", "Month" }
};

var sb = new System.Text.StringBuilder();

// 创建已重命名的维度
var renamed = view.Dimensions
    .Select(
        dim => new MetricView.Dimension
        {
            Name = renames.TryGetValue(dim.Name, out var newName) ? newName : dim.Name,
            Expr = dim.Expr
        })
    .ToList();

// 替换集合
view.Dimensions.Clear();
foreach (var dim in renamed)
{
    view.Dimensions.Add(dim);
}

sb.AppendLine("重命名后的维度：");
sb.AppendLine("-------------------");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name,-20} <- {dim.Expr}");
}

Output(sb.ToString());
```

**输出：**

```
重命名后的维度：
-------------------
  Product              <- product.product_name
  Category             <- product.category
  分段                  <- customer.segment
  Date                 <- date.full_date
  Year                 <- date.year
  Month                <- date.month_name
```

## 另见

- @semantic-bridge-add-object
- @semantic-bridge-remove-object
- @semantic-bridge-serialize
