---
uid: how-to-work-with-dependencies
title: How to Work with Dependencies
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# How to Work with Dependencies

The TOM wrapper tracks which objects reference which other objects through the `DependsOn` and `ReferencedBy` properties. Use these for impact analysis, finding unused objects and understanding DAX lineage.

> [!NOTE]
> The `DependsOn` and `ReferencedBy` properties expose the same dependency information shown in the **Dependency View** in Tabular Editor's UI.

## Quick reference

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

## DependsOn: what does this object reference?

`DependsOn` is available on (xref:TabularEditor.TOMWrapper.IDaxDependantObject) types -- objects that have a DAX expression. This includes measures, calculated columns, calculation items, KPIs, tables and partitions.

```csharp
var measure = Model.AllMeasures.First(m => m.Name == "Revenue");

// List all columns this measure references
foreach (var col in measure.DependsOn.Columns)
    Info($"References column: {col.DaxObjectFullName}");

// Check if measure depends on a specific table
var usesDate = measure.DependsOn.Tables.Any(t => t.Name == "Date");
```

## ReferencedBy: what references this object?

`ReferencedBy` is available on any (xref:TabularEditor.TOMWrapper.IDaxObject). This includes objects with no DAX expression of their own, such as `DataColumn`, which can still be referenced by name in other objects' DAX.

```csharp
var column = Model.Tables["Sales"].Columns["Amount"];

// List all measures that reference this column
foreach (var m in column.ReferencedBy.Measures)
    Info($"Referenced by: {m.DaxObjectFullName}");

// Check if column is used in any RLS expression
var usedInRLS = column.ReferencedBy.Roles.Any();
```

## Deep traversal

`Deep()` follows the dependency chain transitively. Use it for full impact analysis.

```csharp
// All upstream objects (direct + indirect) that a measure depends on
var allUpstream = measure.DependsOn.Deep();
var upstreamColumns = allUpstream.OfType<Column>();
var upstreamTables = allUpstream.OfType<Table>();

// All downstream objects that would break if this column is removed
var allDownstream = column.ReferencedBy.Deep();
var affectedMeasures = allDownstream.OfType<Measure>();
```

## 查找未使用的对象

Objects with no references are candidates for cleanup. This pattern mirrors the built-in BPA rule for detecting unused objects.

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

## Impact analysis

Before renaming or deleting an object, check what depends on it.

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

## Dynamic LINQ equivalent

In BPA rule expressions, dependency properties are accessed directly on the object in context.

| C# script                                           | Dynamic LINQ (BPA)            |
| --------------------------------------------------- | ------------------------------------------------ |
| `m.ReferencedBy.Count == 0`                         | `ReferencedBy.Count = 0`                         |
| `m.DependsOn.Any()`                                 | `DependsOn.Any()`                                |
| `!c.ReferencedBy.AllMeasures.Any(m => !m.IsHidden)` | `not ReferencedBy.AllMeasures.Any(not IsHidden)` |
| `c.UsedInRelationships.Any()`                       | `UsedInRelationships.Any()`                      |
| `c.UsedInSortBy.Any()`                              | `UsedInSortBy.Any()`                             |
| `c.UsedInHierarchies.Any()`                         | `UsedInHierarchies.Any()`                        |
| `c.ReferencedBy.AnyVisible`                         | `ReferencedBy.AnyVisible`                        |

## Common pitfalls

> [!IMPORTANT]
>
> - `DependsOn` requires a DAX expression and is only available on `IDaxDependantObject` types: `Measure`, `CalculatedColumn`, `CalculationItem`, `KPI`, `Table`, `Partition`, `TablePermission`. A `DataColumn` does not have `DependsOn` because it has no DAX expression.
> - `ReferencedBy` does not require a DAX expression. It is available on any `IDaxObject` type: `Column`, `Measure`, `Table`, `Hierarchy`. A `DataColumn` has `ReferencedBy` because other objects can reference it by name. Not every object type has both properties.
> - `UsedInRelationships`, `UsedInHierarchies` and `UsedInSortBy` are column-specific properties. They track structural usage, not DAX expression references. Check both structural and DAX references to find truly unused columns.
> - `ReferencedBy.Deep()` and `DependsOn.Deep()` can be computationally expensive on large models with deeply nested dependency chains.

## 另见

- @using-bpa-sample-rules-expressions
- @how-to-filter-query-objects-linq
- @formula-fix-up-dependencies
