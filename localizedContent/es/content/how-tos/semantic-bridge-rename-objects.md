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
El mismo patrón se aplica a todas las colecciones en una Metric View: `Fields`, `Measures`, `Dimensions` y `Joins`.

> [!NOTE]
> Estas guías prácticas están orientadas a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de la vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Cambiar el nombre de un campo

Asigna a la propiedad `Name` del objeto. Todo lo demás del objeto (su expresión, comentario, nombre para mostrar, sinónimos y formato) se mantiene intacto, y conserva su lugar en la colección.

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

El índice de nombres de la colección se actualiza con el objeto, por lo que se puede acceder al campo de inmediato con su nuevo nombre:

```csharp
var field = view.Fields["Order Month"];
```

## Reglas

- **Los nombres deben seguir siendo únicos dentro de su colección.** Si le cambias el nombre a un campo por uno que ya usa otro campo, se produce una `ArgumentException` y no se modifica ni el objeto ni la colección.
- **La coincidencia de nombres no distingue entre mayúsculas y minúsculas**, igual que en Databricks SQL. `view.Fields["ORDER MONTH"]` encuentra el campo al que le cambiaste el nombre antes. Un cambio de nombre que solo modifica las mayúsculas y minúsculas sigue siendo útil, ya que actualiza el nombre almacenado.
- **El cambio de nombre se aplica al modelo de objetos en memoria.** Serializa la vista para escribirla.

## Siguientes pasos

- [Agregar objetos a una vista de métricas](xref:semantic-bridge-add-object)
- [Eliminar objetos de una vista de métricas](xref:semantic-bridge-remove-object)
- [Serializar una vista de métricas en YAML](xref:semantic-bridge-serialize)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
- @semantic-bridge-metric-view-validation
