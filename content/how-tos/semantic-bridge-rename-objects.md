---
uid: semantic-bridge-rename-objects
title: Rename Objects in a Metric View
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
# Rename objects in a Metric View

This how-to demonstrates renaming a Metric View field.
The same pattern applies to every collection in a Metric View: `Fields`, `Measures`, `Dimensions` and `Joins`.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Rename a field

Assign to the object's `Name` property. Everything else about the object (its expression, comment, display name, synonyms and format) is left alone, and it keeps its place in the collection.

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

The collection's name index is updated with the object, so the field is reachable under its new name straight away:

```csharp
var field = view.Fields["Order Month"];
```
## Rules

- **Names must stay unique within their collection.** Renaming a field to a name another field already uses throws an `ArgumentException`, and neither the object nor the collection is changed.
- **Name matching is case-insensitive**, following Databricks SQL. `view.Fields["ORDER MONTH"]` finds the field renamed above. A rename that only changes casing is still worth doing, since it refreshes the stored name.
- **The rename applies to the object model in memory.** Serialize the view to write it out.

## Next steps

- [Add objects to a Metric View](xref:semantic-bridge-add-object)
- [Remove objects from a Metric View](xref:semantic-bridge-remove-object)
- [Serialize a Metric View to YAML](xref:semantic-bridge-serialize)

## See also

- [Metric View Object Model](xref:semantic-bridge-metric-view-object-model)
- @semantic-bridge-metric-view-validation
