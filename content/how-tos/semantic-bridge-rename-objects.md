---
uid: semantic-bridge-rename-objects
title: Rename Objects in a Metric View
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
# Rename objects in a Metric View

This how-to demonstrates renaming a Metric View field, and the same pattern applies to every collection in a Metric View: `Fields`, `Measures`, `Dimensions` and `Joins`.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later, as earlier versions do not support the v1.1 Metric View features shown here.
> Renaming in place requires Tabular Editor 3.27.0 or later.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Rename a field

Assigning to the object's `Name` property renames it and keeps the object's other properties (expression, comment, display name, synonyms and format) and its position in the collection.

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

```text
Fields:
  product_name
  product_category
  customer_segment
  order_date
  order_year
  Order Month
```

The collection index updates immediately:

```csharp
var field = view.Fields["Order Month"];
```

## Naming rules

- Names must be unique within their collection. Renaming a field to a name another field already uses throws an `ArgumentException` and leaves the object and the collection unchanged.
- Name matching is case-insensitive, following Databricks SQL. `view.Fields["ORDER MONTH"]` finds the field renamed above, and a case-only rename updates the stored name.
- The rename changes the object model in memory. Serialize the view to write it out.

## Next steps

- [Add objects to a Metric View](xref:semantic-bridge-add-object)
- [Remove objects from a Metric View](xref:semantic-bridge-remove-object)
- [Serialize a Metric View to YAML](xref:semantic-bridge-serialize)

## See also

- [Metric View Object Model](xref:semantic-bridge-metric-view-object-model)
- @semantic-bridge-metric-view-validation
