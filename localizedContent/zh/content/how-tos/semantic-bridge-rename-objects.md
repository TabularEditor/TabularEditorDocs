---
uid: semantic-bridge-rename-objects
title: 在指标视图中重命名对象
author: Greg Baldini
updated: 2026-09-23
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

本操作指南演示了如何重命名指标视图字段，相同的模式也适用于指标视图中的每个集合：`Fields`、`Measures`、`Dimensions`和`Joins`。

> [!NOTE]
> 这些操作说明适用于 Tabular Editor 3.26.2 及更高版本，因为早期版本不支持此处所示的 v1.1 度量视图功能。
> 原地重命名需要 Tabular Editor 3.27.0 或更高版本。

[!INCLUDE [sample](includes/sample-metricview.md)]

## 重命名字段

对对象的 `Name` 属性进行赋值会对其重命名，并保留对象的其他属性（表达式、注释、显示名称、同义词和格式）及其在集合中的位置。

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
Fields:
  product_name
  product_category
  customer_segment
  order_date
  order_year
  Order Month
```

集合索引将立即更新：

```csharp
var field = view.Fields["Order Month"];
```

## 命名规则

- 名称在其集合中必须是唯一的。将字段重命名为另一个字段已使用的名称将引发 `ArgumentException`，并且对象和集合保持不变。
- 名称匹配不区分大小写，遵循 Databricks SQL。`view.Fields["ORDER MONTH"]` 找到上面重命名的字段，仅大小写不同的重命名会更新存储的名称。
- 重命名会更改内存中的对象模型。序列化视图以将其写入。

## 后续步骤

- [向指标视图中添加对象](xref:semantic-bridge-add-object)
- [从指标视图中移除对象](xref:semantic-bridge-remove-object)
- [将指标视图序列化为 YAML](xref:semantic-bridge-serialize)

## 另见

- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
- @semantic-bridge-metric-view-validation
