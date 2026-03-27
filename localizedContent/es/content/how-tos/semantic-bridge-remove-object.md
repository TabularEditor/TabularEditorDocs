---
uid: semantic-bridge-remove-object
title: Eliminar un objeto de una Metric View
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

# Eliminar un objeto de una Metric View

Este procedimiento muestra cómo eliminar dimensiones de Metric View de una Metric View cargada.
El mismo enfoque se aplica a todas las colecciones de una Metric View.

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

> [!NOTE]
> Cada script de eliminación que se muestra aquí afecta a la Metric View cargada en ese momento.
> Si quieres ejecutar todos estos scripts, asegúrate de ejecutar el comando `Deserialize` anterior antes de cada eliminación.

## Eliminar por nombre

Localiza la dimensión de la Metric View y elimínala de la colección:

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensiones antes: {view.Dimensions.Count}");

var dimToRemove = view.Dimensions.FirstOrDefault(d => d.Name == "order_month");
if (dimToRemove != null)
{
    view.Dimensions.Remove(dimToRemove);
    sb.AppendLine($"Eliminada: {dimToRemove.Name}");
}

sb.AppendLine($"Dimensiones después: {view.Dimensions.Count}");
Output(sb.ToString());
```

**Salida:**

```
Dimensiones antes: 6
Eliminada: order_month
Dimensiones después: 5
```

Observa que, si ejecutas el script anterior dos veces seguidas, no se elimina nada más; los recuentos de antes y después son ambos 5.

## Eliminar varias dimensiones de una Metric View

Usa LINQ para filtrar y reconstruir la colección:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensiones antes: {view.Dimensions.Count}");

// Eliminar todas las dimensiones relacionadas con fechas
string[] toRemove = ["order_date", "order_year", "order_month"];

var toKeep = view.Dimensions
    .Where(d => !toRemove.Contains(d.Name))
    .ToList();

// Vaciar y volver a rellenar
view.Dimensions.Clear();
foreach (var dim in toKeep)
{
    view.Dimensions.Add(dim);
}

sb.AppendLine($"Dimensiones después: {view.Dimensions.Count}");
sb.AppendLine();
sb.AppendLine("Dimensiones restantes:");
sb.AppendLine("---------------------");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name}");
}

Output(sb.ToString());
```

**Salida:**

```
Dimensiones antes: 6
Dimensiones después: 3

Dimensiones restantes:
---------------------
  product_name
  product_category
  customer_segment
```

## Eliminar dimensiones de Metric View de una tabla específica

Elimina todas las dimensiones de Metric View que hacen referencia a la tabla de fechas.

> [!WARNING]
> No se garantiza que este ejemplo elimine todas, y solo, las dimensiones de Metric View que hagan referencia a un Metric View Join determinado.
> Las dimensiones de Metric View pueden incluir expresiones SQL casi arbitrarias y también pueden hacer referencia a dimensiones de Metric View definidas anteriormente.
> Este ejemplo es solo con fines ilustrativos.

```csharp
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensiones antes: {view.Dimensions.Count}");

var toRemove = view.Dimensions
    .Where(d => d.Expr.StartsWith("date."))
    .ToList();

foreach (var dim in toRemove)
{
    view.Dimensions.Remove(dim);
    sb.AppendLine($"Eliminado: {dim.Name} ({dim.Expr})");
}

sb.AppendLine($"Dimensiones después: {view.Dimensions.Count}");
Output(sb.ToString());
```

**Salida:**

```
Dimensiones antes: 6
Eliminado: order_date (date.full_date)
Eliminado: order_year (date.year)
Eliminado: order_month (date.month_name)
Dimensiones después: 3
```

## Ver también

- @semantic-bridge-add-object
- @semantic-bridge-rename-objects
- @semantic-bridge-serialize
