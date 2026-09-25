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

En este procedimiento se explica cómo agregar nuevos objetos a una vista de métricas ya cargada y configurar sus propiedades.
Este patrón se aplica a todas las colecciones de Metric View.

> [!NOTE]
> Estos procedimientos están dirigidos a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de la vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Agregar un campo

Use [`AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A) para crear y devolver un nuevo `Field` que luego pueda manipular.

```csharp {run id=addfield setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Fields before adding: {view.Fields.Count}");

var field = view.AddField("customer_city", "customer.city");

sb.AppendLine($"Fields after adding: {view.Fields.Count}");
Output(sb.ToString());
```

**Salida**

```
Fields before adding: 6
Fields after adding: 7
```

## Agregar y configurar un `Join`

[`AddJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddJoin%2A)
Funciona de forma similar a `AddField`: construye el objeto, lo agrega a la vista de métricas y lo devuelve para que pueda configurar propiedades adicionales.
Establezca la cardinalidad con la enumeración [`JoinCardinality`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.JoinCardinality).

```csharp {run id=addjoin setup=mv-sample after=none output=false}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// add a join, then set its remaining properties
var supplier = view.AddJoin("supplier", "sales.dim.supplier");
supplier.On = "source.supplier_id = supplier.supplier_id";
supplier.Cardinality = MetricView.JoinCardinality.ManyToOne;
```

`AddJoin` también es un método en cualquier `Join` existente.
Puede usarlo para crear `Join` anidados; por ejemplo, `supplier.AddJoin("region", "sales.dim.region")`,
que modela una dimensión de copo de nieve.

## Agregar y configurar una `medida`

[`AddMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddMeasure%2A) funciona de forma similar a los demás métodos `Add`.

Algunas propiedades, como el `Format` de un campo o una medida, tienen sus propios tipos, que debe crear para poder configurarlas.
Cree la variante de [`Format`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format) que desee, como `Format.Currency` o `Format.Percentage`, y asígnela.

```csharp {run id=addmeasure setup=mv-sample after=none output=true}
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

**Salida**

```
total_cost format: Currency { Type = Currency, DecimalPlaces = , HideGroupSeparator = , Abbreviation = , CurrencyCode = USD }
```

## Pasos a seguir

- [Eliminar objetos de una vista de métricas](xref:semantic-bridge-remove-object)
- [Cambiar el nombre de un campo](xref:semantic-bridge-rename-objects)
- [Serializar una vista de métricas a YAML](xref:semantic-bridge-serialize)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
