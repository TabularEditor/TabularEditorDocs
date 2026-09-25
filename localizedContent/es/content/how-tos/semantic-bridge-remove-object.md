---
uid: semantic-bridge-remove-object
title: Eliminar un objeto de una Metric View
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

# Eliminar un objeto de una Metric View

Este procedimiento muestra cómo eliminar los campos y las medidas de Metric View.
El mismo enfoque se aplica a todas las colecciones de una Metric View.

> [!NOTE]
> Estos procedimientos se aplican a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de Metric View v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

> [!NOTE]
> Cada script de eliminación que se muestra aquí afecta a la Metric View cargada en ese momento.
> Si quieres ejecutar todos estos scripts, asegúrate de ejecutar el comando `Deserialize` anterior antes de cada eliminación.

## Eliminar por nombre

Obtén el campo de Metric View y elimínalo.
Después de eliminar un objeto, no debes intentar modificarlo.
Aun así, puedes leer las propiedades del objeto eliminado.
Es seguro llamar a `Delete()` en un objeto varias veces; después de la primera, las siguientes llamadas no tienen efecto.

```csharp {run id=removefield setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Fields before: {view.Fields.Count}");

var fieldToRemove = view.Fields["order_month"];
fieldToRemove.Delete();
fieldToRemove.Delete(); // note we can call Delete twice safely
sb.AppendLine($"Removed: {fieldToRemove.Name}");

sb.AppendLine($"Fields after: {view.Fields.Count}");
Output(sb.ToString());
```

**Salida:**

```
Fields before: 6
Removed: order_month
Fields after: 5
```

Observa que hay varias llamadas a `Delete()`, pero solo se realiza una eliminación.

## Eliminar una medida

Las medidas se eliminan de la misma manera: obtén una referencia a la medida y elimínala.

```csharp {run id=removemeasure setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Measures before: {view.Measures.Count}");

var measureToRemove = view.Measures["gross_margin"];
measureToRemove.Delete();
sb.AppendLine($"Removed: {measureToRemove.Name}");

sb.AppendLine($"Measures after: {view.Measures.Count}");
Output(sb.ToString());
```

**Salida:**

```
Measures before: 6
Removed: gross_margin
Measures after: 5
```

## Eliminar varios campos de Metric View

Filtra los campos que quieras eliminar, crea una instantánea con `ToList` y, después, elimina cada uno.
Crear primero la instantánea evita modificar la colección mientras la iteras.

```csharp {run id=removemultiple setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Fields before: {view.Fields.Count}");

// Remove all date-related fields
string[] toRemove = ["order_date", "order_year", "order_month"];

foreach (var field in view.Fields.Where(f => toRemove.Contains(f.Name)).ToList())
{
    field.Delete();
}

sb.AppendLine($"Fields after: {view.Fields.Count}");
sb.AppendLine();
sb.AppendLine("Remaining fields:");
sb.AppendLine("-----------------");
foreach (var field in view.Fields)
{
    sb.AppendLine($"  {field.Name}");
}

Output(sb.ToString());
```

**Salida:**

```
Fields before: 6
Fields after: 3

Remaining fields:
-----------------
  product_name
  product_category
  customer_segment
```

## Eliminar campos de Metric View de una tabla específica

Elimina todos los campos de Metric View que hacen referencia a la tabla de fechas.

> [!WARNING]
> No se garantiza que este ejemplo elimine todos y únicamente los campos de Metric View que hagan referencia a un Metric View Join determinado.
> Los campos de Metric View pueden incluir expresiones SQL casi arbitrarias y también pueden hacer referencia a campos de Metric View definidos anteriormente.
> Este ejemplo es solo con fines ilustrativos.

```csharp {run id=remove-by-table setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Fields before: {view.Fields.Count}");

foreach (var field in view.Fields.Where(f => f.Expr.StartsWith("date.")).ToList())
{
    field.Delete();
    sb.AppendLine($"Removed: {field.Name} ({field.Expr})");
}

sb.AppendLine($"Fields after: {view.Fields.Count}");
Output(sb.ToString());
```

**Salida:**

```
Fields before: 6
Removed: order_date (date.full_date)
Removed: order_year (date.year)
Removed: order_month (date.month_name)
Fields after: 3
```

## Siguientes pasos

- [Añadir objetos a una vista de métricas](xref:semantic-bridge-add-object)
- [Cambiar el nombre de un campo](xref:semantic-bridge-rename-objects)
- [Serializar una vista de métricas a YAML](xref:semantic-bridge-serialize)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
