---
uid: semantic-bridge-add-object
title: Agregar un objeto a una Metric View
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

# Agregar un objeto a una Metric View

En esta guía práctica se muestra cómo agregar nuevos objetos a una vista de métricas cargada y establecer sus propiedades.
Este patrón se aplica a todas las colecciones de Metric View.

> [!NOTE]
> Estas guías paso a paso están pensadas para Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de la vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Agregar un campo

Use [`AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A) para crear y devolver un nuevo `Field` que pueda manipular.

```csharp {run id=addfield setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Campos antes de agregar: {view.Fields.Count}");

var field = view.AddField("customer_city", "customer.city");

sb.AppendLine($"Campos después de agregar: {view.Fields.Count}");
Output(sb.ToString());
```

**Salida**

```
Campos antes de agregar: 6
Campos después de agregar: 7
```

## Agregar y configurar un `Join`

[`AddJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddJoin%2A)
funciona de forma similar a `AddField`: construye el objeto, lo agrega a la vista de métricas y lo devuelve para que puedas establecer propiedades adicionales.
Establece la cardinalidad con la enumeración [`JoinCardinality`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.JoinCardinality).

```csharp {run id=addjoin setup=mv-sample after=none output=false}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// agrega un join y, a continuación, establece sus propiedades restantes
var supplier = view.AddJoin("supplier", "sales.dim.supplier");
supplier.On = "source.supplier_id = supplier.supplier_id";
supplier.Cardinality = MetricView.JoinCardinality.ManyToOne;
```

`AddJoin` también es un método en cualquier `Join` existente.
Puede usarlo para crear joins anidados; por ejemplo, `supplier.AddJoin("region", "sales.dim.region")`,
que modela una dimensión en copo de nieve.

## Agregar y configurar una `medida`

[`AddMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddMeasure%2A) funciona de forma similar a los demás métodos `Add`.

Algunas propiedades, como el `Format` de un campo o una medida, tienen sus propios tipos que debes crear para poder establecer la propiedad.
Crea la variante de [`Format`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format) que quieras, como `Format.Currency` o `Format.Percentage`, y asígnala.

```csharp {run id=addmeasure setup=mv-sample after=none output=true}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

// agrega una nueva medida y luego asígnale un formato de moneda
var totalCost = view.AddMeasure("total_cost", "SUM(cost)");
totalCost.Format = new MetricView.Format.Currency { CurrencyCode = "USD" };

// vuelve a leer el formato de la medida
sb.AppendLine($"{totalCost.Name} formato: {totalCost.Format}");
Output(sb.ToString());
```

**Salida**

```
total_cost formato: Currency { Type = Currency, DecimalPlaces = , HideGroupSeparator = , Abbreviation = , CurrencyCode = USD }
```

## Pasos a seguir

- [Eliminar objetos de una vista de métricas](xref:semantic-bridge-remove-object)
- [Cambiar el nombre de un campo](xref:semantic-bridge-rename-objects)
- [Serializar una vista de métricas a YAML](xref:semantic-bridge-serialize)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
