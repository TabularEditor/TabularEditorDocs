---
uid: semantic-bridge-add-object
title: Agregar un objeto a una Metric View
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

# Agregar un objeto a una Metric View

En esta guía se muestra cómo agregar una nueva dimensión (campo) a una Metric View cargada.
Este patrón se aplica a todas las colecciones de Metric View.

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## Crear un nuevo objeto de dimensión de Metric View

Utiliza el constructor `Dimension` de Metric View para crear una nueva dimensión de Metric View:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var newDimension = new MetricView.Dimension
{
    Name = "customer_city",
    Expr = "customer.city"
};
```

## Agregar a la Metric View

La propiedad `Dimensions` de la Metric View es un `IList<Dimension>`, por lo que puedes usar `Add()`:

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

**Salida**

```
Dimensiones antes de agregar: 8
Dimensiones después de agregar: 9
```

## Ver también

- @semantic-bridge-remove-object
- @semantic-bridge-rename-objects
- @semantic-bridge-serialize
