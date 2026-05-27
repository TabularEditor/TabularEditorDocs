---
uid: how-to-work-with-dependencies
title: Cómo trabajar con las dependencias
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo trabajar con las dependencias

El wrapper de TOM realiza el seguimiento de qué objetos hacen referencia a qué otros objetos mediante las propiedades `DependsOn` y `ReferencedBy`. Úsalas para analizar el impacto, encontrar objetos sin usar y comprender el linaje de DAX.

> [!NOTE]
> Las propiedades `DependsOn` y `ReferencedBy` exponen la misma información de dependencias que se muestra en la **Vista de dependencias** de la interfaz de Tabular Editor.

## Referencia rápida

```csharp
// What does this measure depend on? (direct)
measure.DependsOn.Columns     // columns referenced in DAX
measure.DependsOn.Measures    // measures referenced in DAX
measure.DependsOn.Tables      // tables referenced in DAX
measure.DependsOn.Count       // total direct dependency count

// Transitive (all levels deep)
measure.DependsOn.Deep()      // HashSet<IDaxObject> of all upstream objects

// Who references this column? (direct)
column.ReferencedBy.Measures   // measures that reference this column
column.ReferencedBy.Columns    // calculated columns that reference this column
column.ReferencedBy.Tables     // calculated tables that reference this column
column.ReferencedBy.Roles      // roles (RLS) that reference this column
column.ReferencedBy.Count      // total direct reference count

// Transitive (all levels deep)
column.ReferencedBy.Deep()           // HashSet<IDaxDependantObject> of all downstream
column.ReferencedBy.AllMeasures      // all measures downstream (deep)
column.ReferencedBy.AllColumns       // all calculated columns downstream (deep)
column.ReferencedBy.AllTables        // all calculated tables downstream (deep)
column.ReferencedBy.AnyVisible       // true if any downstream object is visible

// Column-specific structural usage
column.UsedInRelationships     // relationships using this column
column.UsedInHierarchies       // hierarchies containing this column
column.UsedInSortBy            // columns using this as SortByColumn
```

## `DependsOn`: ¿a qué hace referencia este objeto?

`DependsOn` está disponible en los tipos (xref:TabularEditor.TOMWrapper.IDaxDependantObject); es decir, en objetos que tienen una expresión DAX. Esto incluye medidas, columnas calculadas, elementos de cálculo, KPI, tablas y particiones.

```csharp
var measure = Model.AllMeasures.First(m => m.Name == "Revenue");

// List all columns this measure references
foreach (var col in measure.DependsOn.Columns)
    Info($"References column: {col.DaxObjectFullName}");

// Check if measure depends on a specific table
var usesDate = measure.DependsOn.Tables.Any(t => t.Name == "Date");
```

## `ReferencedBy`: ¿qué hace referencia a este objeto?

`ReferencedBy` está disponible en cualquier (xref:TabularEditor.TOMWrapper.IDaxObject). Esto incluye objetos sin una expresión DAX propia, como `DataColumn`, a los que se puede seguir haciendo referencia por nombre en el DAX de otros objetos.

```csharp
var column = Model.Tables["Sales"].Columns["Amount"];

// List all measures that reference this column
foreach (var m in column.ReferencedBy.Measures)
    Info($"Referenced by: {m.DaxObjectFullName}");

// Check if column is used in any RLS expression
var usedInRLS = column.ReferencedBy.Roles.Any();
```

## Recorrido en profundidad

`Deep()` sigue la cadena de dependencias de forma transitiva. Úsalo para un análisis de impacto completo.

```csharp
// All upstream objects (direct + indirect) that a measure depends on
var allUpstream = measure.DependsOn.Deep();
var upstreamColumns = allUpstream.OfType<Column>();
var upstreamTables = allUpstream.OfType<Table>();

// All downstream objects that would break if this column is removed
var allDownstream = column.ReferencedBy.Deep();
var affectedMeasures = allDownstream.OfType<Measure>();
```

## Búsqueda de objetos sin usar

Los objetos sin referencias son candidatos a ser eliminados. Este patrón refleja la regla de BPA integrada para detectar objetos sin usar.

```csharp
// Measures not referenced by any other DAX expression
var unusedMeasures = Model.AllMeasures
    .Where(m => m.ReferencedBy.Count == 0);

// Hidden columns not referenced by anything (DAX, relationships, hierarchies, sort-by)
var unusedColumns = Model.AllColumns
    .Where(c => c.IsHidden
        && c.ReferencedBy.Count == 0
        && !c.UsedInRelationships.Any()
        && !c.UsedInHierarchies.Any()
        && !c.UsedInSortBy.Any());
```

## Análisis de impacto

Antes de cambiar el nombre o eliminar un objeto, comprueba qué depende de él.

```csharp
var col = Model.Tables["Sales"].Columns["ProductKey"];

Info($"Direct references: {col.ReferencedBy.Count}");
Info($"Relationships: {col.UsedInRelationships.Count()}");
Info($"Hierarchies: {col.UsedInHierarchies.Count()}");
Info($"Sort-by: {col.UsedInSortBy.Count()}");
Info($"Any visible downstream: {col.ReferencedBy.AnyVisible}");

// Full downstream tree
var allAffected = col.ReferencedBy.Deep();
Info($"Total objects affected (deep): {allAffected.Count}");
```

## Equivalente en LINQ dinámico

En las expresiones de reglas de BPA, se accede directamente a las propiedades de dependencia del objeto en cuestión.

| C# Script                                           | LINQ dinámico (BPA)           |
| --------------------------------------------------- | ------------------------------------------------ |
| `m.ReferencedBy.Count == 0`                         | `ReferencedBy.Count = 0`                         |
| `m.DependsOn.Any()`                                 | `DependsOn.Any()`                                |
| `!c.ReferencedBy.AllMeasures.Any(m => !m.IsHidden)` | `not ReferencedBy.AllMeasures.Any(not IsHidden)` |
| `c.UsedInRelationships.Any()`                       | `UsedInRelationships.Any()`                      |
| `c.UsedInSortBy.Any()`                              | `UsedInSortBy.Any()`                             |
| `c.UsedInHierarchies.Any()`                         | `UsedInHierarchies.Any()`                        |
| `c.ReferencedBy.AnyVisible`                         | `ReferencedBy.AnyVisible`                        |

## Errores comunes

> [!IMPORTANT]
>
> - `DependsOn` requiere una expresión DAX y solo está disponible para los tipos `IDaxDependantObject`: `medida`, `CalculatedColumn`, `CalculationItem`, `KPI`, `Table`, `partición`, `TablePermission`. Una `DataColumn` no tiene `DependsOn` porque no tiene ninguna expresión DAX.
> - `ReferencedBy` no requiere una expresión DAX. Está disponible en cualquier tipo de `IDaxObject`: `Column`, `medida`, `Table`, `Hierarchy`. Una `DataColumn` tiene `ReferencedBy` porque otros objetos pueden hacer referencia a ella por su nombre. No todos los tipos de objeto tienen ambas propiedades.
> - `UsedInRelationships`, `UsedInHierarchies` y `UsedInSortBy` son propiedades específicas de columna. Registran el uso estructural, no las referencias en expresiones DAX. Compruebe tanto las referencias estructurales como las de DAX para encontrar columnas realmente sin usar.
> - `ReferencedBy.Deep()` y `DependsOn.Deep()` pueden ser computacionalmente costosos en modelos grandes con cadenas de dependencias muy anidadas.

## Ver también

- @using-bpa-sample-rules-expressions
- @how-to-filter-query-objects-linq
- @formula-fix-up-dependencies
