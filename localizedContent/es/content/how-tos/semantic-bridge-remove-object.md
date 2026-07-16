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

En este tutorial se muestra cómo eliminar campos y medidas de Metric View.
El mismo enfoque se aplica a todas las colecciones de una Metric View.

> [!NOTE]
> Estos procedimientos están pensados para Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de Metric View v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

> [!NOTE]
> Cada script de eliminación que se muestra aquí afecta a la Metric View cargada en ese momento.
> Si quieres ejecutar todos estos scripts, asegúrate de ejecutar el comando `Deserialize` anterior antes de cada eliminación.

## Eliminar por nombre

Obtén el campo de Metric View y elimínalo.
Después de eliminar un objeto, no debes intentar modificarlo.
Aun así, puedes seguir leyendo propiedades del objeto eliminado.
Puedes llamar a `Delete()` en un objeto varias veces sin problema; después de la primera, las demás llamadas no hacen nada.

```csharp {run id=removefield setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Campos antes: {view.Fields.Count}");

var fieldToRemove = view.Fields["order_month"];
fieldToRemove.Delete();
fieldToRemove.Delete(); // nota: podemos llamar a Delete dos veces sin problema
sb.AppendLine($"Eliminado: {fieldToRemove.Name}");

sb.AppendLine($"Campos después: {view.Fields.Count}");
Output(sb.ToString());
```

**Salida:**

```
Campos antes: 6
Eliminado: order_month
Campos después: 5
```

Observa que hay varias llamadas a `Delete()`, pero solo una eliminación.

## Eliminar una medida

Las medidas se eliminan de la misma forma: obtén una referencia a la medida y elimínala.

```csharp {run id=removemeasure setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Medidas antes: {view.Measures.Count}");

var measureToRemove = view.Measures["gross_margin"];
measureToRemove.Delete();
sb.AppendLine($"Eliminado: {measureToRemove.Name}");

sb.AppendLine($"Medidas después: {view.Measures.Count}");
Output(sb.ToString());
```

**Salida:**

```
Medidas antes: 6
Eliminado: gross_margin
Medidas después: 5
```

## Eliminar varios campos de Metric View

Filtra los campos que quieres eliminar, crea una instantánea con `ToList` y luego elimina cada uno.
Crear primero esa instantánea evita modificar la colección mientras la iteras.

```csharp {run id=removemultiple setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Campos antes: {view.Fields.Count}");

// Eliminar todos los campos relacionados con fechas
string[] toRemove = ["order_date", "order_year", "order_month"];

foreach (var field in view.Fields.Where(f => toRemove.Contains(f.Name)).ToList())
{
    field.Delete();
}

sb.AppendLine($"Campos después: {view.Fields.Count}");
sb.AppendLine();
sb.AppendLine("Campos restantes:");
sb.AppendLine("-----------------");
foreach (var field in view.Fields)
{
    sb.AppendLine($"  {field.Name}");
}

Output(sb.ToString());
```

**Salida:**

```
Campos antes: 6
Campos después: 3

Campos restantes:
-----------------
  product_name
  product_category
  customer_segment
```

## Eliminar campos de Metric View de una tabla específica

Elimina todos los campos de Metric View que hacen referencia a la tabla de fechas.

> [!WARNING]
> No se garantiza que este ejemplo elimine todos los campos de Metric View que hagan referencia a un Metric View Join determinado, y solo esos.
> Los campos de Metric View pueden incluir expresiones SQL casi arbitrarias y también pueden hacer referencia a campos de Metric View definidos anteriormente.
> Este ejemplo es solo con fines ilustrativos.

```csharp {run id=remove-by-table setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Campos antes: {view.Fields.Count}");

foreach (var field in view.Fields.Where(f => f.Expr.StartsWith("date.")).ToList())
{
    field.Delete();
    sb.AppendLine($"Eliminado: {field.Name} ({field.Expr})");
}

sb.AppendLine($"Campos después: {view.Fields.Count}");
Output(sb.ToString());
```

**Salida:**

```
Campos antes: 6
Eliminado: order_date (date.full_date)
Eliminado: order_year (date.year)
Eliminado: order_month (date.month_name)
Campos después: 3
```

## Siguientes pasos

- [Agregar objetos a una vista de métricas](xref:semantic-bridge-add-object)
- [Cambiar el nombre de un campo](xref:semantic-bridge-rename-objects)
- [Serializar una vista de métricas en YAML](xref:semantic-bridge-serialize)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
