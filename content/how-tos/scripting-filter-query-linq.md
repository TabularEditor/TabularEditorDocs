---
uid: how-to-filter-query-objects-linq
title: How to Filter and Query Objects with LINQ
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Filter and Query Objects with LINQ

C# scripts use standard LINQ methods to filter, search and transform TOM object collections. These patterns are building blocks. Use collection-returning methods in `foreach` loops, bool-returning methods in `if` conditions and scalar-returning methods in variable assignments.

## Quick reference

```csharp
// Filter -- returns a collection for use in foreach or further chaining
Model.AllMeasures.Where(m => m.Name.EndsWith("Amount"));

// Find one -- returns a single object for assignment to a variable
var table = Model.Tables.First(t => t.Name == "Sales");
var tableOrNull = Model.Tables.FirstOrDefault(t => t.Name == "Sales");

// Existence checks -- returns bool for use in if conditions
if (table.Measures.Any(m => m.IsHidden)) { /* ... */ }
if (table.Columns.All(c => c.Description != "")) { /* ... */ }

// Count
int count = Model.AllColumns.Count(c => c.DataType == DataType.String);

// Project -- returns a List<string> of only the measure names
var names = Model.AllMeasures.Select(m => m.Name).ToList();

// Sort
var sorted = Model.AllMeasures.OrderBy(m => m.Name);

// Mutate
Model.AllMeasures.Where(m => m.FormatString == "").ForEach(m => m.FormatString = "0.00");

// Type filter
var calcCols = Model.AllColumns.OfType<CalculatedColumn>();

// Materialize before modifying the collection
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

## Filtering with Where

`Where()` returns all objects matching a predicate. Chain multiple conditions with `&&` and `||`.

```csharp
// Columns with no description in a specific table
var undocumented = Model.Tables["Sales"].Columns
    .Where(c => string.IsNullOrEmpty(c.Description));
```

> [!WARNING]
> String matching with `Contains()` finds the text anywhere in the expression, including inside string literals and comments. To detect actual DAX function usage, analyze the tokenized expression instead.

> [!TIP]
> When checking expression content with `Contains()`, consider case-insensitive comparison: `m.Expression.Contains("calculate", StringComparison.OrdinalIgnoreCase)`.

## Finding a single object

`First()` returns the first match or throws if none exist. `FirstOrDefault()` returns null instead of throwing.

```csharp
// Throws if "Sales" does not exist
var sales = Model.Tables.First(t => t.Name == "Sales");

// Returns null if not found (safe)
var table = Model.Tables.FirstOrDefault(t => t.Name == "Sales");
if (table == null) { Error("Table not found."); return; } // return exits the script
```

## Existence and count checks

```csharp
// Are all columns documented?
bool allDocs = table.Columns.All(c => !string.IsNullOrEmpty(c.Description));

// How many string columns?
int count = Model.AllColumns.Count(c => c.DataType == DataType.String);
```

## Projection with Select

`Select()` transforms each element. Use it to extract property values or build new structures.

```csharp
// List of measure names only (returns List<string>)
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

## Materializing before modifying a collection

When you modify objects inside a loop (delete, add, move), you change the collection being iterated. Always call `.ToList()` or `.ToArray()` first to create a snapshot.

```csharp
// WRONG: modifying collection during iteration
table.Measures.Where(m => m.IsHidden).ForEach(m => m.Delete()); // throws

// CORRECT: materialize first, then modify
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

> [!WARNING]
> Failing to materialize causes: `"Collection was modified; enumeration operation may not complete."` This applies to any modification, not just deletion.

## Combining collections

Use `Concat()` to merge collections and `Distinct()` to remove duplicates.

```csharp
// All hidden objects (measures + columns) in a table
var hidden = table.Measures.Where(m => m.IsHidden).Cast<ITabularNamedObject>()
    .Concat(table.Columns.Where(c => c.IsHidden).Cast<ITabularNamedObject>());

// All unique tables referenced by selected measures
var tables = Selected.Measures
    .Select(m => m.Table)
    .Distinct();
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
