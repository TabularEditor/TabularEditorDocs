---
uid: how-to-work-with-expressions
title: How to Work with Expressions and DAX Properties
author: Morten Lønskov
updated: 2026-04-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Work with Expressions and DAX Properties

Measures, calculated columns, calculation items, KPIs and partitions all have expressions. This article covers reading, modifying and generating DAX expressions and working with the `IExpressionObject` interface.

## Quick reference

```csharp
// Read and set expressions
measure.Expression                                    // DAX formula string
measure.Expression = "SUM('Sales'[Amount])"           // set formula
measure.FormatString = "#,##0.00"                     // static format
measure.FormatStringExpression = "..."                // dynamic format (DAX)

// Calculated column
calcCol.Expression                                    // DAX formula

// Partition (M query)
partition.Expression                                  // M/Power Query expression

// DAX object names for code generation
column.DaxObjectFullName    // 'Sales'[Amount]
column.DaxObjectName        // [Amount]
measure.DaxObjectFullName   // 'Sales'[Revenue]
measure.DaxObjectName       // [Revenue]
table.DaxObjectFullName     // 'Sales'
table.DaxTableName          // 'Sales'

// Formatting
FormatDax(measure);         // queue for formatting
CallDaxFormatter();         // execute queued formatting

// Tokenizing
measure.Tokenize().Count    // DAX token count (complexity metric)
```

## Reading and modifying measure expressions

```csharp
var m = Model.AllMeasures.First(m => m.Name == "Revenue");

// Read the current DAX
string dax = m.Expression;

// Replace a table reference in the expression
m.Expression = m.Expression.Replace("'Old Table'", "'New Table'");

// Set format string
m.FormatString = "#,##0.00";
```

## DAX object name properties

Every `IDaxObject` (table, column, measure, hierarchy) has properties that return its name in DAX-safe format with proper quoting.

| Property | Column example | Measure example | Table example |
|---|---|---|---|
| `DaxObjectName` | `[Amount]` | `[Revenue]` | `'Sales'` |
| `DaxObjectFullName` | `'Sales'[Amount]` | `[Revenue]` | `'Sales'` |
| `DaxTableName` | `'Sales'` | `'Sales'` | `'Sales'` |

> [!NOTE]
> For measures, `DaxObjectFullName` returns the same value as `DaxObjectName` (unqualified). Measures do not require table qualification in DAX. For columns, `DaxObjectFullName` includes the table prefix.

Use these when generating DAX to avoid quoting errors:

```csharp
// Generate a SUM measure for each selected column
foreach (var col in Selected.Columns)
{
    col.Table.AddMeasure(
        "Sum of " + col.Name,
        "SUM(" + col.DaxObjectFullName + ")",
        col.DisplayFolder
    );
}
```

## The IExpressionObject interface

Objects that hold expressions implement `IExpressionObject`. In Tabular Editor 2, this interface provides only the `Expression` property. In Tabular Editor 3, it adds `GetExpression()`, `SetExpression()` and `GetExpressionProperties()` for working with multiple expression types on a single object.

```csharp
// Tabular Editor 2: use the Expression property directly
measure.Expression = "SUM('Sales'[Amount])";
string dax = measure.Expression;
```

> [!NOTE]
> The following `GetExpression`/`SetExpression` pattern is only available in Tabular Editor 3. In Tabular Editor 2, access the `Expression` property directly on the object.

```csharp
// Tabular Editor 3 only: list all expression types on an object
var exprObj = (IExpressionObject)measure;
foreach (var prop in exprObj.GetExpressionProperties())
{
    string expr = exprObj.GetExpression(prop);
    if (!string.IsNullOrEmpty(expr))
        Info($"{prop}: {expr}");
}

// Set an expression by type
exprObj.SetExpression(ExpressionProperty.Expression, "SUM('Sales'[Amount])");
exprObj.SetExpression(ExpressionProperty.FormatStringExpression, "\"$#,##0.00\"");
```

The `ExpressionProperty` enum (Tabular Editor 3 only) includes:

| Value | Used on |
|---|---|
| `Expression` | Measures, calculated columns, calculation items |
| `DetailRowsExpression` | Measures |
| `FormatStringExpression` | Measures, calculation items |
| `TargetExpression` | KPIs |
| `StatusExpression` | KPIs |
| `TrendExpression` | KPIs |
| `MExpression` | M partitions |

## Formatting DAX

Use `FormatDax()` to queue objects for formatting and `CallDaxFormatter()` to execute.

```csharp
// Format all measures in the model
foreach (var m in Model.AllMeasures)
    FormatDax(m);
CallDaxFormatter();
```

## Tokenizing for complexity analysis

`Tokenize()` returns the DAX tokens in an expression. Use it to measure expression complexity.

```csharp
foreach (var m in Model.AllMeasures.OrderByDescending(m => m.Tokenize().Count))
    Info($"{m.Name}: {m.Tokenize().Count} tokens");
```

## Find and replace in expressions

```csharp
// Replace a column reference across all measures
foreach (var m in Model.AllMeasures.Where(m => m.Expression.Contains("[Old Column]")))
{
    m.Expression = m.Expression.Replace("[Old Column]", "[New Column]");
}
```

## Dynamic LINQ equivalent

In BPA rule expressions, expression properties are accessed directly on the object in context.

| C# script | Dynamic LINQ (BPA) |
|---|---|
| `string.IsNullOrWhiteSpace(m.Expression)` | `String.IsNullOrWhitespace(Expression)` |
| `m.Expression.Contains("CALCULATE")` | `Expression.Contains("CALCULATE")` |
| `m.FormatString == ""` | `FormatString = ""` |
| `m.Expression.StartsWith("SUM")` | `Expression.StartsWith("SUM")` |

## Common pitfalls

> [!IMPORTANT]
> - `DataColumn` does not have an `Expression` property. Only `CalculatedColumn`, `Measure`, `CalculationItem` and `Partition` have expressions. Accessing `Expression` on a `DataColumn` causes a compile error or runtime exception depending on context.
> - `DaxObjectName` returns the unqualified name (e.g., `[Revenue]`) while `DaxObjectFullName` includes the table prefix (e.g., `'Sales'[Revenue]`). Use `DaxObjectFullName` for column references in DAX and `DaxObjectName` for measure references where table qualification is optional.
> - `FormatDax()` only queues the object. You must call `CallDaxFormatter()` to actually format the expressions. The formatter requires an internet connection (it calls the daxformatter.com API).

## See also

- @csharp-scripts
- @using-bpa-sample-rules-expressions
- @how-to-filter-query-objects-linq
- @script-find-replace
