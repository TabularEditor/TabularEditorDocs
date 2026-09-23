---
uid: semantic-bridge-rename-objects
title: Renombrar objetos en una Metric View
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

# Renombrar objetos en una Metric View

Esta guía práctica muestra cómo cambiar el nombre de un campo de una vista de métricas.
The same pattern applies to every collection in a Metric View: `Fields`, `Measures`, `Dimensions` and `Joins`.

> [!NOTE]
> Estas guías prácticas están orientadas a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de la vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Cambiar el nombre de un campo

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

**Salida:**

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

## Siguientes pasos

- [Agregar objetos a una vista de métricas](xref:semantic-bridge-add-object)
- [Eliminar objetos de una vista de métricas](xref:semantic-bridge-remove-object)
- [Serializar una vista de métricas en YAML](xref:semantic-bridge-serialize)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
- @semantic-bridge-metric-view-validation
