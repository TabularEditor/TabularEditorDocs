---
uid: how-to-check-object-types
title: How to Check Object Types
author: Morten Lønskov
updated: 2026-04-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Check Object Types

The TOM hierarchy uses inheritance. `Column` is an abstract base with subtypes `DataColumn`, `CalculatedColumn` and `CalculatedTableColumn`. `Table` has the subtype `CalculationGroupTable`. This article shows how to test and filter by type in C# scripts and Dynamic LINQ.

## Quick reference

```csharp
// Pattern matching (preferred)
if (col is CalculatedColumn cc)
    Info(cc.Expression);

// Filter a collection by type
var calcCols = Model.AllColumns.OfType<CalculatedColumn>();
var calcGroups = Model.Tables.OfType<CalculationGroupTable>();

// Runtime type name
string typeName = obj.GetType().Name;   // "DataColumn", "Measure", etc.

// Null-safe cast
var dc = col as DataColumn;
if (dc != null) { /* use dc */ }
```

## Type hierarchy

The key inheritance relationships in the TOM wrapper:

| Base type | Subtypes |
|---|---|
| `Column` | `DataColumn`, `CalculatedColumn`, `CalculatedTableColumn` |
| `Table` | `CalculatedTable`, `CalculationGroupTable` |
| `Partition` | `MPartition`, `EntityPartition`, `PolicyRangePartition` |
| `DataSource` | `ProviderDataSource`, `StructuredDataSource` |

## Filtering collections by type

`OfType<T>()` filters and casts in one step. Prefer it over `Where(x => x is T)`.

```csharp
// All calculated columns in the model
var calculatedColumns = Model.AllColumns.OfType<CalculatedColumn>();

// All M partitions (Power Query)
var mPartitions = Model.AllPartitions.OfType<MPartition>();

// All calculation group tables
var calcGroups = Model.Tables.OfType<CalculationGroupTable>();

// All regular tables (exclude calculation groups)
var regularTables = Model.Tables.Where(t => t is not CalculationGroupTable);
```

## Pattern matching with is

Use C# pattern matching to test and cast in a single expression.

```csharp
foreach (var col in Model.AllColumns)
{
    if (col is CalculatedColumn cc)
        Info($"{cc.Name}: {cc.Expression}");
    else if (col is DataColumn dc)
        Info($"{dc.Name}: data column in {dc.Table.Name}");
}
```

## Checking ObjectType enum

Every TOM object has an `ObjectType` property that returns an enum value. This identifies the base type, not the subtype.

```csharp
foreach (var obj in Selected.Objects)
{
    switch (obj.ObjectType)
    {
        case ObjectType.Measure:  /* ... */ break;
        case ObjectType.Column:   /* ... */ break;
        case ObjectType.Table:    /* ... */ break;
        case ObjectType.Hierarchy: /* ... */ break;
    }
}
```

> [!WARNING]
> `ObjectType` does not distinguish subtypes. A `CalculatedColumn` and a `DataColumn` both return `ObjectType.Column`. Use `is` or `OfType<T>()` when you need subtype-level checks.

## Checking partition source type

For partitions, use the `SourceType` property to distinguish between storage modes without type-casting.

```csharp
foreach (var p in Model.AllPartitions)
{
    switch (p.SourceType)
    {
        case PartitionSourceType.M:          /* Power Query */    break;
        case PartitionSourceType.Calculated:  /* DAX calc table */ break;
        case PartitionSourceType.Entity:      /* Direct Lake */    break;
        case PartitionSourceType.Query:       /* Legacy SQL */     break;
    }
}
```

## Dynamic LINQ equivalent

In BPA rules, type filtering works differently. Set the rule's **Applies to** scope to target a specific object type. Within the expression, use `ObjectTypeName` for the base type name as a string.

```
// BPA expression context: the rule "Applies to" determines the object type
// No C#-style type casting is available in Dynamic LINQ

// Check the object type name (rarely needed since scope handles this)
ObjectTypeName = "Measure"
ObjectTypeName = "Column"
```

For subtypes like calculated columns, set the BPA rule scope to **Calculated Columns** rather than trying to filter by type in the expression.

## Common pitfalls

> [!IMPORTANT]
> - `Column` is abstract. You cannot create an instance of `Column` directly. Use `table.AddDataColumn()` or `table.AddCalculatedColumn()` on regular tables. `AddCalculatedTableColumn()` is only available on `CalculatedTable`.
> - `OfType<T>()` both filters and casts. `Where(x => x is T)` only filters, leaving you with the base type. Prefer `OfType<T>()` when you need access to subtype properties.
> - `ObjectType` and `SourceType` are base-level checks. For subtype-specific logic (e.g., accessing `Expression` on a `CalculatedColumn`), use `is` or `OfType<T>()`.

## See also

- @csharp-scripts
- @using-bpa-sample-rules-expressions
- @how-to-navigate-tom-hierarchy
