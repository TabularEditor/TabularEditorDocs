---
uid: semantic-bridge-rename-objects
title: Rename Objects in a Metric View
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
# Rename objects in a Metric View

This how-to demonstrates renaming a Metric View field.
The same patterns apply to all collections in a Metric View.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not necessarily support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Rename a field

Rename a field by adding a new field under the new name, copying its other properties across, then removing the original.
[`AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A) sets only the name and expression, so copy the remaining properties (`Comment`, `DisplayName`, `Synonyms`, `Format`) yourself.

```csharp
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

**Output:**

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

## See also

- @semantic-bridge-add-object
- @semantic-bridge-remove-object
- @semantic-bridge-serialize
