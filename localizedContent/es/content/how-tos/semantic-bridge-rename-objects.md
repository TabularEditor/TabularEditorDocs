---
uid: semantic-bridge-rename-objects
title: Renombrar objetos en una Metric View
author: Greg Baldini
updated: 2026-09-23
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

Esta guía práctica muestra cómo cambiar el nombre de un campo de una vista de métrica, y el mismo patrón se aplica a todas las colecciones de una vista de métrica: `Fields`, `Measures`, `Dimensions` y `Joins`.

> [!NOTE]
> Estas guías prácticas están dirigidas a Tabular Editor 3.26.2 y versiones posteriores, ya que las versiones anteriores no admiten las funciones de la vista de métricas v1.1 que se muestran aquí.
> Para cambiar el nombre «in situ», se requiere Tabular Editor 3.27.0 o una versión posterior.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Cambiar el nombre de un campo

Al asignar un valor a la propiedad `Name` del objeto, se cambia su nombre y se conservan las demás propiedades del objeto (expresión, comentario, nombre para mostrar, sinónimos y formato), así como su posición en la colección.

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

El índice de la colección se actualiza inmediatamente:

```csharp
var field = view.Fields["Order Month"];
```

## Reglas de nomenclatura

- Los nombres deben ser únicos dentro de su colección. Si se cambia el nombre de un campo por un nombre que ya utiliza otro campo, se produce un `ArgumentException` y el objeto y la colección permanecen sin cambios.
- La coincidencia de nombres no distingue entre mayúsculas y minúsculas, siguiendo Databricks SQL. `view.Fields["ORDER MONTH"]` encuentra el campo cuyo nombre se ha cambiado anteriormente, y un cambio de nombre solo por mayúsculas o minúsculas actualiza el nombre almacenado.
- El cambio de nombre modifica el modelo de objetos en la memoria. Serialice la vista para escribirla.

## Pasos a seguir

- [Agregar objetos a una vista de métricas](xref:semantic-bridge-add-object)
- [Quitar objetos de una vista de métricas](xref:semantic-bridge-remove-object)
- [Serializar una vista de métricas a YAML](xref:semantic-bridge-serialize)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
- @validación de Metric View en Semantic Bridge
