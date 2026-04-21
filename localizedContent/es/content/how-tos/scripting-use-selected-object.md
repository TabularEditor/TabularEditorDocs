---
uid: how-to-use-selected-object
title: Cómo usar el objeto `Selected`
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo usar el objeto `Selected`

El objeto `Selected` proporciona acceso a lo que esté seleccionado en ese momento en el árbol de @tom-explorer-view-reference. Úselo para escribir scripts que operen sobre los objetos seleccionados por el usuario, en lugar de sobre nombres codificados de forma rígida.

## Referencia rápida

```csharp
// Singular (exactly one selected, throws if 0 or 2+)
Selected.Measure
Selected.Table
Selected.Column

// Guard clause
if (Selected.Measures.Count() == 0) { Error("Select at least one measure."); return; }

// Iterate and modify
foreach (var m in Selected.Measures)
    m.FormatString = "0.00";

// Using ForEach extension
Selected.Measures.ForEach(m => m.DisplayFolder = "KPIs");
```

Accesores plurales (cero o más; seguros para iterar):

- `Selected.Measures`
- `Selected.Tables`
- `Selected.Columns`
- `Selected.Hierarchies`
- `Selected.Particiones`
- `Selected.Levels`
- `Selected.CalculationItems`
- `Selected.Roles`
- `Selected.DataSources`

## Accesores singulares y plurales

El objeto `Selected` expone accesores tanto en singular como en plural para cada tipo de objeto.

| Accesor             | Devuelve               | Comportamiento cuando el recuento no es 1                                                                                                     |
| ------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `Selected.Measure`  | una única `medida`     | Lanza una excepción si se seleccionan 0 medidas o 2 o más medidas                                                                             |
| `Selected.Measures` | `IEnumerable<Measure>` | Devuelve una colección que puede estar vacía, pero nunca es nula. Puedes iterarla directamente con seguridad. |

Usa la forma **singular** cuando tu script requiera exactamente un objeto. Usa la forma **plural** cuando el script deba funcionar con cero o más objetos.

## Cláusulas de guarda

El accesor plural devuelve cero o más objetos. Un script puede no hacer nada silenciosamente con una colección vacía, o bien requerir una cantidad mínima. Para este último caso, usa una cláusula de guarda.

```csharp
// Require at least one measure
if (Selected.Measures.Count() == 0)
{
    Error("No measures selected. Select one or more measures and run again.");
    return;
}
```

```csharp
// Require exactly one table
if (Selected.Tables.Count() != 1)
{
    Error("Select exactly one table.");
    return;
}
var table = Selected.Table;
```

En los scripts que aceptan varios tipos de objeto, combina las comprobaciones:

```csharp
if (Selected.Columns.Count() == 0 && Selected.Measures.Count() == 0)
{
    Error("Select at least one column or measure.");
    return;
}
```

## Iterar sobre los objetos seleccionados

El accesor en plural devuelve una colección que puedes iterar con `foreach` o LINQ.

```csharp
// Set display folder on all selected measures
foreach (var m in Selected.Measures)
    m.DisplayFolder = "Sales Metrics";

// Hide all selected columns
Selected.Columns.ForEach(c => c.IsHidden = true);

// Add to a perspective
Selected.Measures.ForEach(m => m.InPerspective["Sales"] = true);
```

## Trabajar con la tabla seleccionada

Cuando hay una sola tabla seleccionada, usa `Selected.Table` para agregar nuevos objetos a esa tabla.

```csharp
var t = Selected.Table;
t.AddMeasure("Row Count", "COUNTROWS(" + t.DaxObjectFullName + ")");
```

## Selecciones mixtas

Cuando necesites manejar varios tipos de objeto de la selección, itera `Selected` directamente. La propia variable `Selected` implementa `IEnumerable<ITabularNamedObject>`.

```csharp
foreach (var desc in Selected.OfType<IDescriptionObject>())
{
    desc.Description = "Reviewed on " + DateTime.Today.ToString("yyyy-MM-dd");
}
```

Consulta @how-to-filter-query-objects-linq para más información sobre el filtrado con LINQ y @how-to-tom-interfaces para el manejo de objetos basado en interfaces.

## Try/catch para diálogos de selección

Al usar los métodos auxiliares `SelectTable()`, `SelectColumn()` o `SelectMeasure()`, encapsúlalos en un bloque try/catch para controlar la cancelación por parte del usuario.

```csharp
try
{
    var table = SelectTable(Model.Tables, null, "Pick a table:");
    Info("You selected: " + table.Name);
}
catch
{
    Error("No table selected.");
}
```

> [!NOTE]
> El objeto `Selected` solo está disponible en contextos interactivos (la interfaz de usuario de Tabular Editor y las macros). Al ejecutar scripts mediante la CLI con la opción `-S`, `Selected` refleja los objetos especificados por los argumentos `-O` o queda vacío si no se especifica ninguno.

## Ver también

- @csharp-scripts
- @advanced-scripting
- @how-to-navigate-tom-hierarchy
- @script-helper-methods
