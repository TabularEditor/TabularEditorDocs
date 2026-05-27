---
uid: how-to-navigate-tom-hierarchy
title: Cómo navegar por la jerarquía de objetos de TOM
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo navegar por la jerarquía de objetos de TOM

Todo C# Script empieza con el objeto `Model` o con el objeto `Selected` de @csharp-scripts. Estos objetos exponen el wrapper TOM de Tabular Editor, que encapsula el Microsoft Analysis Services Tabular Object Model (TOM). Consulta la referencia de la API (xref:TabularEditor.TOMWrapper) para ver la documentación completa de TOMWrapper.

## Referencia rápida

```csharp
// Direct path to a specific object
var table    = Model.Tables["Sales"];
var measure  = Model.Tables["Sales"].Measures["Revenue"];
var column   = Model.Tables["Sales"].Columns["Amount"];
var hierarchy = Model.Tables["Date"].Hierarchies["Calendar"];
var partition = Model.Tables["Sales"].Partitions["Sales-Part1"];

// Cross-table shortcut collections
Model.AllMeasures          // every measure across all tables
Model.AllColumns           // every column across all tables
Model.AllHierarchies       // every hierarchy across all tables
Model.AllPartitions        // every partition across all tables
Model.AllLevels            // every level across all hierarchies
Model.AllCalculationItems  // every calculation item across all calculation groups

// Top-level collections
Model.Tables               // all tables
Model.Relationships        // all relationships
Model.Perspectives         // all perspectives
Model.Roles                // all security roles
Model.Cultures             // all translation cultures
Model.DataSources          // all data sources
Model.CalculationGroups    // all calculation group tables
```

## Acceso a objetos por nombre

Usa el indexador `["name"]` en cualquier colección para recuperar un objeto por su nombre exacto. Esto genera una excepción si ese nombre no existe.

```csharp
var salesTable = Model.Tables["Sales"];
var revenueM  = salesTable.Measures["Revenue"];
var amountCol = salesTable.Columns["Amount"];
```

Usa `FirstOrDefault()` cuando el objeto pueda no existir:

```csharp
var table = Model.Tables.FirstOrDefault(t => t.Name == "Sales");
if (table == null) { Error("Table not found"); return; } // return exits the script early
```

## Navegar del hijo al padre

Cada objeto mantiene una referencia a su objeto padre. Úsalas para recorrer la jerarquía hacia arriba.

```csharp
var measure = Model.AllMeasures.First(m => m.Name == "Revenue");
var parentTable = measure.Table;          // Table that contains this measure
var model = measure.Model;                // The Model root

var level = Model.AllLevels.First();
var hierarchy = level.Hierarchy;           // parent hierarchy
var table = level.Table;                   // parent table (via hierarchy)

// Navigate up to Model and back down to a different table
var m = Model.AllMeasures.First(m => m.Name == "Revenue");
var otherCol = m.Table.Model.Tables["Product"].Columns.First();
```

> [!NOTE]
> El último ejemplo muestra que puedes subir hasta `Model` desde cualquier objeto hijo y volver a bajar hasta cualquier tabla del modelo.

## Navegar por los objetos secundarios de una tabla

Cada `Table` expone colecciones tipadas para sus objetos secundarios.

```csharp
var table = Model.Tables["Sales"];

Output(table.Columns);                     // ColumnCollection
Output(table.Measures);                    // MeasureCollection
Output(table.Hierarchies);                 // HierarchyCollection
Output(table.Partitions);                  // PartitionCollection
```

## Búsqueda con predicados

Usa métodos LINQ en cualquier colección para buscar objetos por valores de las propiedades.

```csharp
// Find all fact tables
var factTables = Model.Tables.Where(t => t.Name.StartsWith("Fact"));

// Find all hidden measures
var hiddenMeasures = Model.AllMeasures.Where(m => m.IsHidden);

// Find the first column with a specific data type
var dateCol = Model.AllColumns.First(c => c.DataType == DataType.DateTime);
```

## Grupos de cálculo y elementos de cálculo

Las tablas de grupos de cálculo son un subtipo de `Table`. Accede a ellas mediante `Model.CalculationGroups` y recorre sus elementos.

```csharp
foreach (var cg in Model.CalculationGroups)
{
    foreach (var item in cg.CalculationItems)
    {
        Info(item.Name + ": " + item.Expression);
    }
}
```

## Relaciones

Las relaciones residen en `Model`, no en las tablas. Cada relación hace referencia a sus columnas y tablas de origen y destino.

```csharp
foreach (var rel in Model.Relationships)
{
    var fromTable  = rel.FromTable;
    var fromColumn = rel.FromColumn;
    var toTable    = rel.ToTable;
    var toColumn   = rel.ToColumn;
}
```

## Equivalente de LINQ dinámico

En las expresiones de reglas de Best Practice Analyzer (BPA) y en los filtros del árbol del **Explorador TOM**, puedes acceder directamente a las propiedades del objeto en el contexto. La navegación al elemento padre utiliza la notación de puntos.

| C# Script                             | LINQ dinámico (BPA) |
| ------------------------------------- | -------------------------------------- |
| `measure.Table.Name`                  | `Table.Name`                           |
| `column.Table.IsHidden`               | `Table.IsHidden`                       |
| `table.Columns.Count()`               | `Columns.Count()`                      |
| `table.Measures.Any(m => m.IsHidden)` | `Measures.Any(IsHidden)`               |

> [!NOTE]
> Las expresiones de LINQ dinámico en las reglas de BPA se evalúan sobre un único objeto a la vez. No tienes acceso a `Model` ni a colecciones entre tablas. Usa el ámbito **Se aplica a** de la regla para seleccionar el tipo de objeto sobre el que se ejecuta la expresión.

## Ver también

- @csharp-scripts
- @advanced-scripting
- @how-to-filter-query-objects-linq
