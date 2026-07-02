---
uid: semantic-bridge-remove-object
title: Remove an Object from a Metric View
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
# Remove an object from a Metric View

This how-to demonstrates removing Metric View fields and measures.
Similar approaches apply to all collections in a Metric View.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

> [!NOTE]
> Each removal script here affects the currently loaded Metric View.
> If you want to run all of these, make sure to run the `Deserialize` above before each removal.

## Remove by name

Get the Metric View field and delete it.
After you delete an object, you should not attempt to modify it.
You can still read properties off of the deleted object.
It is safe to call `Delete()` on an object multiple times; after the first, these are no-ops.

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Fields before: {view.Fields.Count}");

var fieldToRemove = view.Fields["order_month"];
fieldToRemove.Delete();
fieldToRemove.Delete(); // note we can call Delete twice safely
sb.AppendLine($"Removed: {fieldToRemove.Name}");

sb.AppendLine($"Fields after: {view.Fields.Count}");
Output(sb.ToString());
```

**Output:**

```
Fields before: 6
Removed: order_month
Fields after: 5
```

Observe that there are multiple calls to `Delete()` but only one removal.

## Remove a measure

Measures are removed the same way: get a reference to the measure and delete it.

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Measures before: {view.Measures.Count}");

var measureToRemove = view.Measures["gross_margin"];
measureToRemove.Delete();
sb.AppendLine($"Removed: {measureToRemove.Name}");

sb.AppendLine($"Measures after: {view.Measures.Count}");
Output(sb.ToString());
```

**Output:**

```
Measures before: 6
Removed: gross_margin
Measures after: 5
```

## Remove multiple Metric View fields

Filter to the fields you want to remove, snapshot them with `ToList`, then delete each one.
Snapshotting first avoids modifying the collection while iterating it.

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Fields before: {view.Fields.Count}");

// Remove all date-related fields
string[] toRemove = ["order_date", "order_year", "order_month"];

foreach (var field in view.Fields.Where(f => toRemove.Contains(f.Name)).ToList())
{
    field.Delete();
}

sb.AppendLine($"Fields after: {view.Fields.Count}");
sb.AppendLine();
sb.AppendLine("Remaining fields:");
sb.AppendLine("-----------------");
foreach (var field in view.Fields)
{
    sb.AppendLine($"  {field.Name}");
}

Output(sb.ToString());
```

**Output:**

```
Fields before: 6
Fields after: 3

Remaining fields:
-----------------
  product_name
  product_category
  customer_segment
```

## Remove Metric View fields from a specific table

Remove all Metric View fields that reference the date table.

> [!WARNING]
> This example is not guaranteed to remove all and exclusively Metric View fields which reference a given Metric View Join.
> Metric View fields may include near-arbitrary SQL expressions, and may also reference previously defined Metric View fields.
> This example is for illustrative purposes only.

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Fields before: {view.Fields.Count}");

foreach (var field in view.Fields.Where(f => f.Expr.StartsWith("date.")).ToList())
{
    field.Delete();
    sb.AppendLine($"Removed: {field.Name} ({field.Expr})");
}

sb.AppendLine($"Fields after: {view.Fields.Count}");
Output(sb.ToString());
```

**Output:**

```
Fields before: 6
Removed: order_date (date.full_date)
Removed: order_year (date.year)
Removed: order_month (date.month_name)
Fields after: 3
```

## Next steps

- [Add objects to a Metric View](xref:semantic-bridge-add-object)
- [Rename a field](xref:semantic-bridge-rename-objects)
- [Serialize a Metric View to YAML](xref:semantic-bridge-serialize)

## See also

- [Metric View Object Model](xref:semantic-bridge-metric-view-object-model)
