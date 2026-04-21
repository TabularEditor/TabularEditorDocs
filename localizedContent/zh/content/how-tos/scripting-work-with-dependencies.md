---
uid: how-to-work-with-dependencies
title: 如何使用依赖关系
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何使用依赖关系

TOM 封装器会通过 `DependsOn` 和 `ReferencedBy` 属性跟踪对象之间的引用关系。 可用它们进行影响分析、查找未使用对象，以及理解 DAX 血缘关系。

> [!NOTE]
> `DependsOn` 和 `ReferencedBy` 属性公开的依赖信息与 Tabular Editor 界面中的 **依赖关系视图** 所显示的信息相同。

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

`DependsOn` 适用于 (xref:TabularEditor.TOMWrapper.IDaxDependantObject) 类型，即具有 DAX 表达式的对象。 这包括度量值、计算列、计算项、KPI、表和分区。

```csharp
var measure = Model.AllMeasures.First(m => m.Name == "Revenue");

// List all columns this measure references
foreach (var col in measure.DependsOn.Columns)
    Info($"References column: {col.DaxObjectFullName}");

// Check if measure depends on a specific table
var usesDate = measure.DependsOn.Tables.Any(t => t.Name == "Date");
```

## `ReferencedBy`：哪些对象引用了这个对象？

`ReferencedBy` 适用于任何 (xref:TabularEditor.TOMWrapper.IDaxObject) 对象。 `ReferencedBy` 适用于任何 (xref:TabularEditor.TOMWrapper.IDaxObject) 对象。 这也包括自身没有 DAX 表达式的对象，例如 `DataColumn`；它们仍然可以在其他对象的 DAX 中通过名称被引用。

```csharp
var column = Model.Tables["Sales"].Columns["Amount"];

// List all measures that reference this column
foreach (var m in column.ReferencedBy.Measures)
    Info($"Referenced by: {m.DaxObjectFullName}");

// Check if column is used in any RLS expression
var usedInRLS = column.ReferencedBy.Roles.Any();
```

## 深度遍历

`Deep()` 会以传递方式沿着依赖链继续遍历。 可用于完整的影响分析。 可用于完整的影响分析。

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

没有任何引用的对象是清理的候选对象。 这种模式与用于检测未使用对象的内置 BPA 规则一致。

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

| C# Script                                           | Dynamic LINQ (BPA)            |
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
> - `DependsOn` 需要 DAX 表达式，并且仅适用于 `IDaxDependantObject` 类型：`Measure`、`CalculatedColumn`、`CalculationItem`、`KPI`、`Table`、`Partition`、`TablePermission`。 `DataColumn` 没有 `DependsOn`，因为它没有 DAX 表达式。 `DataColumn` 没有 `DependsOn`，因为它没有 DAX 表达式。
> - `ReferencedBy` 不需要 DAX 表达式。 它适用于任何 `IDaxObject` 类型：`Column`、`Measure`、`Table`、`Hierarchy`。 `DataColumn` 有 `ReferencedBy`，因为其他对象可以按名称引用它。 并非每种对象类型都同时具有这两个属性。 它适用于任何 `IDaxObject` 类型：`Column`、`Measure`、`Table`、`Hierarchy`。 `DataColumn` 有 `ReferencedBy`，因为其他对象可以按名称引用它。 并非每种对象类型都同时具有这两个属性。
> - `UsedInRelationships`、`UsedInHierarchies` 和 `UsedInSortBy` 是列专有的属性。 `UsedInRelationships`、`UsedInHierarchies` 和 `UsedInSortBy` 是列专有的属性。 它们追踪的是结构性使用情况，而不是对 DAX 表达式的引用。 要找出真正未使用的列，请同时检查结构性引用和 DAX 引用。 要找出真正未使用的列，请同时检查结构性引用和 DAX 引用。
> - 在依赖链层级很深、嵌套复杂的大型模型中，`ReferencedBy.Deep()` 和 `DependsOn.Deep()` 的计算开销可能会非常高。

## 另见

- @using-bpa-sample-rules-expressions
- @how-to-filter-query-objects-linq
- @formula-fix-up-dependencies
