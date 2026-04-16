---
uid: how-to-check-object-types
title: How to Check Object Types
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Check Object Types

The TOM hierarchy uses inheritance. `Column` is an abstract base with subtypes `DataColumn`, `CalculatedColumn` and `CalculatedTableColumn`. `Table` has subtypes `CalculatedTable` and `CalculationGroupTable`. Use the base type when working with shared properties like `Name`, `Description`, `IsHidden`, `FormatString` or `DisplayFolder`. Cast to a concrete subtype when you need type-specific properties, such as `Expression` on `CalculatedColumn` or `SourceColumn` on `DataColumn`.

## Quick reference

```csharp
// Pattern matching -- checks type AND casts in one step
if (col is CalculatedColumn cc)
    Info(cc.Expression);  // Expression is only on CalculatedColumn, not base Column

// Filter a collection by type
var calcCols = Model.AllColumns.OfType<CalculatedColumn>();
var calcGroups = Model.Tables.OfType<CalculationGroupTable>();

// Runtime type name (use only for display/logging, not for logic)
var typeName = obj.GetType().Name;   // "DataColumn", "Measure", etc.
```

> [!NOTE]
> Pattern matching with variable declaration (`col is CalculatedColumn cc`) requires the Roslyn compiler in Tabular Editor 2. Configure it under **File > Preferences > General > Compiler path**. See [Compiling with Roslyn](xref:advanced-scripting#compiling-with-roslyn) for details. Tabular Editor 3 supports this by default.

## Type hierarchy

The key inheritance relationships in the TOM wrapper:

| Base type | Subtypes |
|---|---|
| (xref:TabularEditor.TOMWrapper.Column) | (xref:TabularEditor.TOMWrapper.DataColumn), (xref:TabularEditor.TOMWrapper.CalculatedColumn), (xref:TabularEditor.TOMWrapper.CalculatedTableColumn) |
| (xref:TabularEditor.TOMWrapper.Table) | (xref:TabularEditor.TOMWrapper.CalculatedTable), (xref:TabularEditor.TOMWrapper.CalculationGroupTable) |
| (xref:TabularEditor.TOMWrapper.Partition) | (xref:TabularEditor.TOMWrapper.MPartition), (xref:TabularEditor.TOMWrapper.EntityPartition), (xref:TabularEditor.TOMWrapper.PolicyRangePartition) |
| (xref:TabularEditor.TOMWrapper.DataSource) | (xref:TabularEditor.TOMWrapper.ProviderDataSource), (xref:TabularEditor.TOMWrapper.StructuredDataSource) |

## Filtering collections by type

`OfType<T>()` works on any collection and returns a filtered sequence containing only items that are the specified type. It returns an empty sequence if no items match.

```csharp
// All calculated columns in the model (empty if model has none)
var calculatedColumns = Model.AllColumns.OfType<CalculatedColumn>();

// All M partitions (Power Query)
var mPartitions = Model.AllPartitions.OfType<MPartition>();

// All calculation group tables
var calcGroups = Model.Tables.OfType<CalculationGroupTable>();

// All regular tables (exclude calculation groups and calculated tables)
var regularTables = Model.Tables.Where(t => t is not CalculationGroupTable && t is not CalculatedTable);
```

## Pattern matching with is

Pattern matching does two things: it checks whether a value is a given type and optionally casts it into a new variable. The form `x is Type xx` asks "is `x` of type `Type`?" and, if true, gives you `xx` as a variable of that exact type.

This is equivalent to:

```csharp
if (col is CalculatedColumn)
{
    var cc = (CalculatedColumn)col; // explicit cast
    // use cc...
}
```

If you only need the boolean check, use `x is Type` without the variable. If you also need subtype-specific properties, use `x is Type xx`.

```csharp
foreach (var col in Model.AllColumns)
{
    // Expression is only available on CalculatedColumn, not the base Column type
    if (col is CalculatedColumn cc)
        Info($"{cc.Name}: {cc.Expression}");
    else if (col is DataColumn dc)
        Info($"{dc.Name}: data column in {dc.Table.Name}");
}
```

## Dynamic LINQ equivalent

In BPA rules, type filtering is handled by the rule's **Applies to** scope. Set it to the target object type (e.g., **Calculated Columns**) rather than filtering by type in the expression. No C#-style type casting is available in Dynamic LINQ.

## Common pitfalls

> [!IMPORTANT]
> - `Column` is abstract, but you can access all properties defined on the base type (`Name`, `DataType`, `FormatString`, `IsHidden`, `Description`, `DisplayFolder`) without casting. Only cast to a subtype when you need subtype-specific properties like `Expression` on `CalculatedColumn`.
> - `OfType<T>()` both filters and casts. `Where(x => x is T)` only filters, leaving you with the base type. Prefer `OfType<T>()` when you need access to subtype properties.
> - Calculated table columns are managed automatically. Edit the calculated table's `Expression` to add or change columns. You cannot add them directly.

## See also

- @csharp-scripts
- @using-bpa-sample-rules-expressions
- @how-to-navigate-tom-hierarchy
- @how-to-tom-interfaces
