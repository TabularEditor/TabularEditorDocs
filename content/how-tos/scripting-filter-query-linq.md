---
uid: how-to-filter-query-objects-linq
title: How to Filter and Query Objects with LINQ
author: Morten Lønskov
updated: 2026-04-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Filter and Query Objects with LINQ

C# scripts use standard LINQ methods to filter, search and transform TOM object collections. This article covers the essential LINQ patterns for querying semantic model objects.

## Quick reference

```csharp
// Filter
Model.AllMeasures.Where(m => m.Expression.Contains("CALCULATE"))

// Find one
Model.Tables.First(t => t.Name == "Sales")
Model.Tables.FirstOrDefault(t => t.Name == "Sales")   // returns null if not found

// Existence checks
table.Measures.Any(m => m.IsHidden)                    // true if at least one
table.Columns.All(c => c.Description != "")            // true if every one

// Count
Model.AllColumns.Count(c => c.DataType == DataType.String)

// Project
Model.AllMeasures.Select(m => m.Name).ToList()

// Sort
Model.AllMeasures.OrderBy(m => m.Name)
Model.AllMeasures.OrderByDescending(m => m.Table.Name)

// Mutate
Model.AllMeasures.Where(m => m.FormatString == "").ForEach(m => m.FormatString = "0.00")

// Type filter
Model.AllColumns.OfType<CalculatedColumn>()

// Materialize before deleting
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete())
```

## Filtering with Where

`Where()` returns all objects matching a predicate. Chain multiple conditions with `&&` and `||`.

```csharp
// Measures that use CALCULATE and are hidden
var matches = Model.AllMeasures
    .Where(m => m.Expression.Contains("CALCULATE") && m.IsHidden);

// Columns with no description in a specific table
var undocumented = Model.Tables["Sales"].Columns
    .Where(c => string.IsNullOrEmpty(c.Description));
```

## Finding a single object

`First()` returns the first match or throws if none exist. `FirstOrDefault()` returns null instead of throwing.

```csharp
// Throws if "Sales" does not exist
var sales = Model.Tables.First(t => t.Name == "Sales");

// Returns null if not found (safe)
var table = Model.Tables.FirstOrDefault(t => t.Name == "Sales");
if (table == null) { Error("Table not found."); return; }
```

## Existence and count checks

```csharp
// Does any measure reference CALCULATE?
bool usesCalc = Model.AllMeasures.Any(m => m.Expression.Contains("CALCULATE"));

// Are all columns documented?
bool allDocs = table.Columns.All(c => !string.IsNullOrEmpty(c.Description));

// How many string columns?
int count = Model.AllColumns.Count(c => c.DataType == DataType.String);
```

## Projection with Select

`Select()` transforms each element. Use it to extract property values or build new structures.

```csharp
// List of measure names
var names = Model.AllMeasures.Select(m => m.Name).ToList();

// Table name + measure count pairs
var summary = Model.Tables.Select(t => new { t.Name, Count = t.Measures.Count() });
```

## Mutation with ForEach

The `ForEach()` extension method applies an action to every element.

```csharp
// Set format string on all currency measures
Model.AllMeasures
    .Where(m => m.Name.EndsWith("Amount"))
    .ForEach(m => m.FormatString = "#,##0.00");

// Move all measures in a table to a display folder
Model.Tables["Sales"].Measures.ForEach(m => m.DisplayFolder = "Sales Metrics");
```

## Materializing with ToList before deletion

When you delete objects inside a loop, you modify the collection being iterated. This causes a collection-modified exception. Always call `.ToList()` first to create a snapshot.

```csharp
// WRONG: modifying collection during iteration
table.Measures.Where(m => m.IsHidden).ForEach(m => m.Delete()); // throws

// CORRECT: materialize first, then delete
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

> [!WARNING]
> Always call `.ToList()` before `.ForEach(x => x.Delete())` or any operation that adds/removes objects from the collection being iterated.

## Combining collections

Use `Concat()` to merge collections and `Distinct()` to remove duplicates.

```csharp
// All hidden objects (measures + columns) in a table
var hidden = table.Measures.Where(m => m.IsHidden).Cast<ITabularNamedObject>()
    .Concat(table.Columns.Where(c => c.IsHidden).Cast<ITabularNamedObject>());
```

## Dynamic LINQ equivalent

In BPA rule expressions, the syntax differs from C# LINQ. Dynamic LINQ has no lambda arrows, uses keyword operators and compares enums as strings.

| C# LINQ (scripts) | Dynamic LINQ (BPA / Explorer filter) |
|---|---|
| `m.IsHidden` | `IsHidden` |
| `m.DataType == DataType.String` | `DataType = "String"` |
| `&&` / `\|\|` / `!` | `and` / `or` / `not` |
| `==` / `!=` | `=` / `!=` or `<>` |
| `table.Columns.Count(c => c.IsHidden)` | `Columns.Count(IsHidden)` |
| `table.Measures.Any(m => m.IsHidden)` | `Measures.Any(IsHidden)` |
| `table.Columns.All(c => c.Description != "")` | `Columns.All(Description != "")` |
| `string.IsNullOrEmpty(m.Description)` | `String.IsNullOrEmpty(Description)` |

> [!NOTE]
> Dynamic LINQ expressions evaluate against a single object in context. There is no equivalent to `Model.AllMeasures` or cross-table queries. Each BPA rule runs its expression once per object in its scope.

## See also

- @advanced-scripting
- @using-bpa-sample-rules-expressions
- @how-to-navigate-tom-hierarchy
- @how-to-dynamic-linq-vs-csharp-linq
