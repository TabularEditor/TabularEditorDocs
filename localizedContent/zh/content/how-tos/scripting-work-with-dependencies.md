---
uid: how-to-work-with-dependencies
title: 如何使用依赖关系
author: Morten Lønskov
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何使用依赖关系

The TOM wrapper tracks which objects reference which other objects through the `DependsOn` and `ReferencedBy` properties. Use these for impact analysis, finding unused objects and understanding DAX lineage.

> [!NOTE]
> The `DependsOn` and `ReferencedBy` properties expose the same dependency information shown in the [**DAX Dependencies** view](xref:creating-and-testing-dax#dax-dependencies) in Tabular Editor's UI.

## 快速参考

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

## `DependsOn`：这个对象引用了什么？

`DependsOn` is available on (xref:TabularEditor.TOMWrapper.IDaxDependantObject) types -- objects that have a DAX expression. This includes measures, calculated columns, calculation items, KPIs, tables and partitions.

```csharp
var measure = Model.AllMeasures.First(m => m.Name == "Revenue");

// List all columns this measure references
foreach (var col in measure.DependsOn.Columns)
    Info($"References column: {col.DaxObjectFullName}");

// Check if measure depends on a specific table
var usesDate = measure.DependsOn.Tables.Any(t => t.Name == "Date");
```

## `ReferencedBy`：哪些对象引用了这个对象？

`ReferencedBy` is available on any (xref:TabularEditor.TOMWrapper.IDaxObject). 这也包括自身不含 DAX 表达式的对象，例如 `DataColumn`；它们仍可在其他对象的 DAX 中通过名称被引用。

```csharp
var column = Model.Tables["Sales"].Columns["Amount"];

// List all measures that reference this column
foreach (var m in column.ReferencedBy.Measures)
    Info($"Referenced by: {m.DaxObjectFullName}");

// Check if column is used in any RLS expression
var usedInRLS = column.ReferencedBy.Roles.Any();
```

## 深度遍历

`Deep()` 会以传递方式沿着依赖链继续遍历。 Use it for full impact analysis.

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

## 影响分析

在重命名或删除对象之前，先检查哪些对象依赖它。

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

## Dynamic LINQ 等价写法

在 BPA 规则表达式中，可直接在当前上下文对象上访问这些依赖属性。

| C# Script                                           | Dynamic LINQ（BPA）                                |
| --------------------------------------------------- | ------------------------------------------------ |
| `m.ReferencedBy.Count == 0`                         | `ReferencedBy.Count = 0`                         |
| `m.DependsOn.Any()`                                 | `DependsOn.Any()`                                |
| `!c.ReferencedBy.AllMeasures.Any(m => !m.IsHidden)` | `not ReferencedBy.AllMeasures.Any(not IsHidden)` |
| `c.UsedInRelationships.Any()`                       | `UsedInRelationships.Any()`                      |
| `c.UsedInSortBy.Any()`                              | `UsedInSortBy.Any()`                             |
| `c.UsedInHierarchies.Any()`                         | `UsedInHierarchies.Any()`                        |
| `c.ReferencedBy.AnyVisible`                         | `ReferencedBy.AnyVisible`                        |

## 常见误区

> [!IMPORTANT]
>
> - `DependsOn` 需要 DAX 表达式，并且仅适用于 `IDaxDependantObject` 类型：`Measure`、`CalculatedColumn`、`CalculationItem`、`KPI`、`Table`、`Partition`、`TablePermission`。 A `DataColumn` does not have `DependsOn` because it has no DAX expression.
> - `ReferencedBy` 不需要 DAX 表达式。 It is available on any `IDaxObject` type: `Column`, `Measure`, `Table`, `Hierarchy`. A `DataColumn` has `ReferencedBy` because other objects can reference it by name. Not every object type has both properties.
> - `UsedInRelationships`, `UsedInHierarchies` and `UsedInSortBy` are column-specific properties. 它们追踪的是结构性使用情况，而不是对 DAX 表达式的引用。 Check both structural and DAX references to find truly unused columns.
> - 在依赖链层级很深、嵌套复杂的大型模型中，`ReferencedBy.Deep()` 和 `DependsOn.Deep()` 的计算开销可能会非常高。

## 另见

- @using-bpa-sample-rules-expressions
- @how-to-filter-query-objects-linq
- @formula-fix-up-dependencies
