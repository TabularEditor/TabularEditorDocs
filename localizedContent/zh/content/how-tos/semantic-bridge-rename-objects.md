---
uid: semantic-bridge-rename-objects
title: 在指标视图中重命名对象
author: Greg Baldini
updated: 2026-09-14
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

这篇操作指南演示如何重命名指标视图中的字段。同样的模式适用于 Metric View 中的每个集合：`Fields`、`Measures`、`Dimensions` 和 `Joins`。

> [!NOTE]
> 这些操作指南适用于 Tabular Editor 3.26.2 及更高版本。较早版本不支持此处所示的 v1.1 指标视图功能。

[!INCLUDE [sample](includes/sample-metricview.md)]

## 重命名字段

将其赋值给对象的 `Name` 属性。对象的其他所有内容（其表达式、注释、显示名称、同义词和格式）都保持不变，同时它在集合中的位置也不会改变。

```csharp {run id=rename setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

view.Fields["order_month"].Name = "Order Month";

var sb = new System.Text.StringBuilder();
sb.AppendLine("Fields:");
foreach (var field in view.Fields)
{
    sb.AppendLine($"  {field.Name}");
}
Output(sb.ToString());
```

**输出：**

```
字段：
  product_name
  product_category
  customer_segment
  order_date
  order_year
  Order Month
```

集合的名称索引会随该对象一起更新，因此可以立即通过新名称访问该字段：

```csharp
var field = view.Fields["Order Month"];
```

## 规则

- **名称在其所属集合内必须保持唯一。** 如果将某个字段重命名为另一个字段已在使用的名称，则会引发 `ArgumentException`，并且对象和集合都不会发生更改。
- **名称匹配不区分大小写**，与 Databricks SQL 保持一致。 `view.Fields["ORDER MONTH"]` 会找到上面重命名后的字段。即使重命名仅改变大小写，也仍然值得这样做，因为这会刷新存储的名称。
- **重命名会应用到内存中的对象模型。** 要将其写出，请序列化该视图。

## 后续步骤

- [向指标视图中添加对象](xref:semantic-bridge-add-object)
- [从指标视图中移除对象](xref:semantic-bridge-remove-object)
- [将指标视图序列化为 YAML](xref:semantic-bridge-serialize)

## 另见

- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
- @semantic-bridge-metric-view-validation
