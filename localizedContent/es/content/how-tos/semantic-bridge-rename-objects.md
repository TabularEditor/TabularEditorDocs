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

Este procedimiento muestra cómo cambiar el nombre de un campo de una vista de métricas.
El mismo patrón se aplica a todas las colecciones de una vista de métricas: `Fields`, `Measures`, `Dimensions` y `Joins`.

> [!NOTE]
> Estos procedimientos están dirigidos a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las funcionalidades de la vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Cambiar el nombre de un campo

Asigna la propiedad `Name` del objeto. Todo lo demás del objeto (su expresión, comentario, nombre para mostrar, sinónimos y formato) se mantiene sin cambios, y conserva su lugar en la colección.

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

El índice de nombres de la colección se actualiza con el objeto, de modo que se puede acceder al campo de inmediato con su nuevo nombre:

```csharp
var field = view.Fields["Order Month"];
```

## Reglas

- **Los nombres deben ser únicos dentro de su colección.** Si cambias el nombre de un campo por uno que ya usa otro campo, se produce una `ArgumentException` y no se modifica ni el objeto ni la colección.
- **La coincidencia de nombres no distingue entre mayúsculas y minúsculas**, de acuerdo con Databricks SQL. `view.Fields["ORDER MONTH"]` encuentra el campo cuyo nombre se cambió anteriormente. Aunque un cambio de nombre solo modifique las mayúsculas y minúsculas, sigue siendo útil, ya que actualiza el nombre almacenado.
- **El cambio de nombre se aplica al modelo de objetos en memoria.** Serializa la vista para escribirla.

## Pasos a seguir

- [Agregar objetos a una vista de métricas](xref:semantic-bridge-add-object)
- [Quitar objetos de una vista de métricas](xref:semantic-bridge-remove-object)
- [Serializar una vista de métricas a YAML](xref:semantic-bridge-serialize)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
- @validación de Metric View en Semantic Bridge
