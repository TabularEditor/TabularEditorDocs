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

This how-to demonstrates renaming a Metric View field.
同样的模式也适用于指标视图中的所有集合。

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Rename a field

Rename a field by adding a new field under the new name, copying its other properties across, then removing the original.
[`AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A) sets only the name and expression, so copy the remaining properties (`Comment`, `DisplayName`, `Synonyms`, `Format`) yourself.

```csharp {run id=rename setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var old = view.Fields["order_month"];

// add the replacement, copy the remaining properties, then remove the original
var renamed = view.AddField("Order Month", old.Expr);
renamed.Comment = old.Comment;
renamed.DisplayName = old.DisplayName;
renamed.Synonyms = old.Synonyms;
renamed.Format = old.Format;
old.Delete();

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

The re-added field moves to the end of the collection.

## 后续步骤

- [Add objects to a Metric View](xref:semantic-bridge-add-object)
- [Remove objects from a Metric View](xref:semantic-bridge-remove-object)
- [Serialize a Metric View to YAML](xref:semantic-bridge-serialize)

## 另见

- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
