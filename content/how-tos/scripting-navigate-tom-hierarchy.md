---
uid: how-to-navigate-tom-hierarchy
title: How to Navigate the TOM Object Hierarchy
author: Morten Lønskov
updated: 2026-04-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Navigate the TOM Object Hierarchy

Every C# script starts from the `Model` object, which is the root of the Tabular Object Model (TOM) hierarchy. This article shows how to reach any object in a semantic model.

## Quick reference

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

## Accessing objects by name

Use the indexer `["name"]` on any collection to retrieve an object by its exact name. This throws an exception if the name does not exist.

```csharp
var salesTable = Model.Tables["Sales"];
var revenueM  = salesTable.Measures["Revenue"];
var amountCol = salesTable.Columns["Amount"];
```

Use `FirstOrDefault()` when the object may not exist:

```csharp
var table = Model.Tables.FirstOrDefault(t => t.Name == "Sales");
if (table == null) { Error("Table not found"); return; }
```

## Navigating from child to parent

Every object holds a reference to its parent. Use these to walk up the hierarchy.

```csharp
var measure = Model.AllMeasures.First(m => m.Name == "Revenue");
var parentTable = measure.Table;          // Table that contains this measure
var model = measure.Model;                // The Model root

var level = Model.AllLevels.First();
var hierarchy = level.Hierarchy;           // parent hierarchy
var table = level.Table;                   // parent table (via hierarchy)
```

## Navigating table children

Each `Table` exposes typed collections for its child objects.

```csharp
var table = Model.Tables["Sales"];

table.Columns                              // ColumnCollection
table.Measures                             // MeasureCollection
table.Hierarchies                          // HierarchyCollection
table.Partitions                           // PartitionCollection
```

## Searching with predicates

Use LINQ methods on any collection to find objects by property values.

```csharp
// Find all fact tables
var factTables = Model.Tables.Where(t => t.Name.StartsWith("Fact"));

// Find all hidden measures
var hiddenMeasures = Model.AllMeasures.Where(m => m.IsHidden);

// Find the first column with a specific data type
var dateCol = Model.AllColumns.First(c => c.DataType == DataType.DateTime);
```

## Calculation groups and calculation items

Calculation group tables are a subtype of `Table`. Access them through `Model.CalculationGroups` and iterate their items.

```csharp
foreach (var cg in Model.CalculationGroups)
{
    foreach (var item in cg.CalculationItems)
    {
        // item.Name, item.Expression, item.Ordinal
    }
}
```

## Relationships

Relationships live on the `Model`, not on tables. Each relationship references its from/to columns and tables.

```csharp
foreach (var rel in Model.Relationships)
{
    var fromTable  = rel.FromTable;
    var fromColumn = rel.FromColumn;
    var toTable    = rel.ToTable;
    var toColumn   = rel.ToColumn;
}
```

## Dynamic LINQ equivalent

In Best Practice Analyzer (BPA) rule expressions and **TOM Explorer** tree filters, you access properties directly on the object in context. Parent navigation uses dot notation.

| C# script | Dynamic LINQ (BPA) |
|---|---|
| `measure.Table.Name` | `Table.Name` |
| `column.Table.IsHidden` | `Table.IsHidden` |
| `table.Columns.Count()` | `Columns.Count()` |
| `table.Measures.Any(m => m.IsHidden)` | `Measures.Any(IsHidden)` |

> [!NOTE]
> Dynamic LINQ expressions in BPA rules evaluate against a single object at a time. You do not have access to `Model` or cross-table collections. Use the rule's **Applies to** scope to select which object type the expression runs against.

## See also

- @csharp-scripts
- @advanced-scripting
- @how-to-filter-query-objects-linq
