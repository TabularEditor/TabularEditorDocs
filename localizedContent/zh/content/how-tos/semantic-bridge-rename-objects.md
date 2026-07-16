---
uid: semantic-bridge-rename-objects
title: 在指标视图中重命名对象
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

# 在指标视图中重命名对象

这篇操作指南演示如何重命名指标视图中的字段。
同样的模式也适用于指标视图中的所有集合。

> [!NOTE]
> 这些操作指南适用于 Tabular Editor 3.26.2 及更高版本。
> 较早版本不支持此处所示的 v1.1 指标视图功能。

[!INCLUDE [sample](includes/sample-metricview.md)]

## 重命名字段

要重命名字段，可以先用新名称添加一个新字段，复制其余属性，然后删除原字段。
[`AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A) 仅会设置名称和表达式，因此其余属性（`Comment`, `DisplayName`, `Synonyms`, `Format`）请自行复制。

```csharp {run id=rename setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var old = view.Fields["order_month"];

// 添加替代字段，复制其余属性，然后删除原字段
var renamed = view.AddField("Order Month", old.Expr);
renamed.Comment = old.Comment;
renamed.DisplayName = old.DisplayName;
renamed.Synonyms = old.Synonyms;
renamed.Format = old.Format;
old.Delete();

var sb = new System.Text.StringBuilder();
sb.AppendLine("字段：");
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

重新添加的字段会出现在集合末尾。

## 后续步骤

- [向指标视图中添加对象](xref:semantic-bridge-add-object)
- [从指标视图中移除对象](xref:semantic-bridge-remove-object)
- [将指标视图序列化为 YAML](xref:semantic-bridge-serialize)

## 另见

- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
