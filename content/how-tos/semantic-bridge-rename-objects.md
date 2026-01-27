---
uid: semantic-bridge-rename-objects
title: Rename Objects in a Metric View
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
# Rename objects in a Metric View

This how-to demonstrates how to rename Metric View dimensions using a copy-modify pattern for bulk transformations.
The same patterns apply to all collections in a Metric View.

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## The copy-modify pattern

Since Metric View dimension names are properties on objects in a collection, the cleanest approach is to:

1. Create new Metric View `Dimension` objects with the modified names
2. Clear the original collection
3. Add the new objects

This avoids issues with modifying objects while iterating.

## Convert snake_case to Title Case

Transform Metric View dimension names from `product_name` to `Product Name`:

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

**Output:**

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
  Product Name
  Product Category
  Customer Segment
  Order Date
  Order Year
  Order Month
```

## Rename using a mapping dictionary

Apply specific renames using a lookup:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// Define rename mappings
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

// Create renamed dimensions
var renamed = view.Dimensions
    .Select(
        dim => new MetricView.Dimension
        {
            Name = renames.TryGetValue(dim.Name, out var newName) ? newName : dim.Name,
            Expr = dim.Expr
        })
    .ToList();

// Replace the collection
view.Dimensions.Clear();
foreach (var dim in renamed)
{
    view.Dimensions.Add(dim);
}

sb.AppendLine("Renamed dimensions:");
sb.AppendLine("-------------------");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name,-20} <- {dim.Expr}");
}

Output(sb.ToString());
```

**Output:**

```
Renamed dimensions:
-------------------
  Product              <- product.product_name
  Category             <- product.category
  Segment              <- customer.segment
  Date                 <- date.full_date
  Year                 <- date.year
  Month                <- date.month_name
```

## See also

- @semantic-bridge-add-object
- @semantic-bridge-remove-object
- @semantic-bridge-serialize
