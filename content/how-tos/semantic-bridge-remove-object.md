---
uid: semantic-bridge-remove-object
title: Remove an Object from a Metric View
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
# Remove an object from a Metric View

This how-to demonstrates how to remove Metric View dimensions from a loaded Metric View.
Similar approaches apply to all collections in a Metric View.

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

> [!NOTE]
> Each removal script here affects the currently loaded Metric View.
> If you want to run all of these, make sure to run the `Deserialize` above before each removal.

## Remove by name

Find the Metric View dimension and remove it from the collection:

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensions before: {view.Dimensions.Count}");

var dimToRemove = view.Dimensions.FirstOrDefault(d => d.Name == "order_month");
if (dimToRemove != null)
{
    view.Dimensions.Remove(dimToRemove);
    sb.AppendLine($"Removed: {dimToRemove.Name}");
}

sb.AppendLine($"Dimensions after: {view.Dimensions.Count}");
Output(sb.ToString());
```

**Output:**

```
Dimensions before: 6
Removed: order_month
Dimensions after: 5
```

Observe that if you run the script above twice in a row, there is no additional removal; the before and after counts are both 5.

## Remove multiple Metric View dimensions

Use LINQ to filter and rebuild the collection:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensions before: {view.Dimensions.Count}");

// Remove all date-related dimensions
string[] toRemove = ["order_date", "order_year", "order_month"];

var toKeep = view.Dimensions
    .Where(d => !toRemove.Contains(d.Name))
    .ToList();

// Clear and repopulate
view.Dimensions.Clear();
foreach (var dim in toKeep)
{
    view.Dimensions.Add(dim);
}

sb.AppendLine($"Dimensions after: {view.Dimensions.Count}");
sb.AppendLine();
sb.AppendLine("Remaining dimensions:");
sb.AppendLine("---------------------");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name}");
}

Output(sb.ToString());
```

**Output:**

```
Dimensions before: 3
Dimensions after: 3

Remaining dimensions:
---------------------
  product_name
  product_category
  customer_segment
```

## Remove Metric View dimensions from a specific table

Remove all Metric View dimensions that reference the date table.

> [!WARNING]
> This example is not guaranteed to remove all and exclusively Metric View dimensions which reference a given Metric View Join.
> Metric View Dimensions may include near-arbitrary SQL expressions, and may also reference previously defined Metric View Dimensions.
> This example is for illustrative purposes only.

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensions before: {view.Dimensions.Count}");

var toRemove = view.Dimensions
    .Where(d => d.Expr.StartsWith("date."))
    .ToList();

foreach (var dim in toRemove)
{
    view.Dimensions.Remove(dim);
    sb.AppendLine($"Removed: {dim.Name} ({dim.Expr})");
}

sb.AppendLine($"Dimensions after: {view.Dimensions.Count}");
Output(sb.ToString());
```

**Output:**

```
Dimensions before: 6
Removed: order_date (date.full_date)
Removed: order_year (date.year)
Removed: order_month (date.month_name)
Dimensions after: 3
```

## See also

- @semantic-bridge-add-object
- @semantic-bridge-rename-objects
- @semantic-bridge-serialize
