---
uid: semantic-bridge-add-object
title: Add an Object to a Metric View
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
# Add an object to a Metric View

This how-to demonstrates how to add a new Metric View dimension (field) to a loaded Metric View.
Similar patterns apply to all Metric View collections.

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## Create a new Metric View Dimension object

Use the Metric View `Dimension` constructor to create a new Metric View dimension:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var newDimension = new MetricView.Dimension
{
    Name = "customer_city",
    Expr = "customer.city"
};
```

## Add to the Metric View

The Metric View `Dimensions` property is an `IList<Dimension>`, so you can use `Add()`:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensions before adding: {SemanticBridge.MetricView.Model.Dimensions.Count}");

var newDimension = new MetricView.Dimension
{
    Name = "customer_city",
    Expr = "customer.city"
};

SemanticBridge.MetricView.Model.Dimensions.Add(newDimension);

sb.AppendLine($"Dimensions after adding: {SemanticBridge.MetricView.Model.Dimensions.Count}");
Output(sb.ToString());
```

**Output**

```
Dimensions before adding: 8
Dimensions after adding: 9
```

## See also

- @semantic-bridge-remove-object
- @semantic-bridge-rename-objects
- @semantic-bridge-serialize
