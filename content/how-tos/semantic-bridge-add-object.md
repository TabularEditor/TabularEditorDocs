---
uid: semantic-bridge-add-object
title: Add an Object to a Metric View
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
# Add an object to a Metric View

This how-to demonstrates adding new objects to a loaded Metric View and setting their properties.
Similar patterns apply to all Metric View collections.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Add a field

Use [`AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A) to create and return a new `Field` you can manipulate.

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Fields before adding: {view.Fields.Count}");

var field = view.AddField("customer_city", "customer.city");

sb.AppendLine($"Fields after adding: {view.Fields.Count}");
Output(sb.ToString());
```

**Output**

```
Fields before adding: 6
Fields after adding: 7
```

## Add and configure a `Join`

[`AddJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddJoin%2A)
works similarly to `AddField`: it constructs the object, adds it to the Metric View, and returns it so you can set further properties.
Set the cardinality with the [`JoinCardinality`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.JoinCardinality) enum.

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// add a join, then set its remaining properties
var supplier = view.AddJoin("supplier", "sales.dim.supplier");
supplier.On = "source.supplier_id = supplier.supplier_id";
supplier.Cardinality = MetricView.JoinCardinality.ManyToOne;
```

`AddJoin` is also a method on any existing `Join`.
You would use this to create nested joins, for example, `supplier.AddJoin("region", "sales.dim.region")`,
which models a snowflake dimension.

## Add and configure a `Measure`

[`AddMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddMeasure%2A) works similarly to the other `Add` methods.

Some properties, such as a field or measure `Format`, have their own types you need to construct to set the property.
Create the [`Format`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format) variant you want, such as `Format.Currency` or `Format.Percentage`, and assign it.

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

// add a new measure, then give it a currency format
var totalCost = view.AddMeasure("total_cost", "SUM(cost)");
totalCost.Format = new MetricView.Format.Currency { CurrencyCode = "USD" };

// read the format back off the measure
sb.AppendLine($"{totalCost.Name} format: {totalCost.Format}");
Output(sb.ToString());
```

**Output**

```
total_cost format: <!-- TODO: capture record ToString() from a run -->
```

## Next steps

- [Remove objects from a Metric View](xref:semantic-bridge-remove-object)
- [Rename a field](xref:semantic-bridge-rename-objects)
- [Serialize a Metric View to YAML](xref:semantic-bridge-serialize)

## See also

- [Metric View Object Model](xref:semantic-bridge-metric-view-object-model)
