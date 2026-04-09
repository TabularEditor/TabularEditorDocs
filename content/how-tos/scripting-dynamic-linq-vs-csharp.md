---
uid: how-to-dynamic-linq-vs-csharp-linq
title: How Dynamic LINQ Differs from C# LINQ
author: Morten Lønskov
updated: 2026-04-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How Dynamic LINQ Differs from C# LINQ

C# scripts use standard C# LINQ with lambda expressions. Best Practice Analyzer (BPA) rules and Explorer tree filters use [Dynamic LINQ](https://dynamic-linq.net/expression-language), a string-based expression language with different syntax. This article is a translation guide between the two.

## Where each is used

| Context | Syntax |
|---|---|
| C# scripts and macros | C# LINQ |
| BPA rule expressions | Dynamic LINQ |
| BPA fix expressions | Dynamic LINQ (with `it.` prefix for assignments) |
| **TOM Explorer** tree filter (`:` prefix) | Dynamic LINQ |

## Syntax comparison

| Concept | C# LINQ (scripts) | Dynamic LINQ (BPA / filter) |
|---|---|---|
| Boolean AND | `&&` | `and` |
| Boolean OR | `\|\|` | `or` |
| Boolean NOT | `!` | `not` |
| Equals | `==` | `=` |
| Not equals | `!=` | `!=` or `<>` |
| Greater/less | `>`, `<`, `>=`, `<=` | `>`, `<`, `>=`, `<=` |
| String contains | `m.Name.Contains("Sales")` | `Name.Contains("Sales")` |
| String starts with | `m.Name.StartsWith("Sum")` | `Name.StartsWith("Sum")` |
| String ends with | `m.Name.EndsWith("YTD")` | `Name.EndsWith("YTD")` |
| Null/empty check | `string.IsNullOrEmpty(m.Description)` | `String.IsNullOrEmpty(Description)` |
| Whitespace check | `string.IsNullOrWhiteSpace(m.Description)` | `String.IsNullOrWhitespace(Description)` |
| Regex match | `Regex.IsMatch(m.Name, "pattern")` | `RegEx.IsMatch(Name, "pattern")` |

## Enum comparison

C# uses typed enum values. Dynamic LINQ uses string representations.

| C# LINQ | Dynamic LINQ |
|---|---|
| `c.DataType == DataType.String` | `DataType = "String"` |
| `p.SourceType == PartitionSourceType.M` | `SourceType = "M"` |
| `p.Mode == ModeType.DirectLake` | `Mode = "DirectLake"` |
| `r.CrossFilteringBehavior == CrossFilteringBehavior.BothDirections` | `CrossFilteringBehavior = "BothDirections"` |

## Lambda expressions vs implicit context

C# LINQ uses explicit lambda parameters. Dynamic LINQ evaluates properties on an implicit `it` context object.

```csharp
// C# LINQ: explicit lambda parameter
Model.AllMeasures.Where(m => m.IsHidden && m.Description == "")

// Dynamic LINQ: implicit "it" -- properties are accessed directly
IsHidden and Description = ""
```

## Parent object navigation

Both use dot notation, but C# requires the lambda parameter.

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.Table.IsHidden)

// Dynamic LINQ
Table.IsHidden
```

## Collection methods

C# LINQ uses lambdas inside collection methods. Dynamic LINQ uses implicit context within collection methods, with `outerIt` to reference the parent object.

```csharp
// C# LINQ: count columns with no description
Model.Tables.Where(t => t.Columns.Count(c => c.Description == "") > 5)

// Dynamic LINQ: same logic
Columns.Count(Description = "") > 5
```

### The outerIt keyword

Inside a nested collection method in Dynamic LINQ, `it` refers to the inner object (e.g., a column). Use `outerIt` to reference the outer object (e.g., the table).

```
// BPA rule on Tables: find tables where any column name matches the table name
Columns.Any(Name = outerIt.Name)
```

In C#, this is handled naturally by lambda closure:

```csharp
// C# equivalent
Model.Tables.Where(t => t.Columns.Any(c => c.Name == t.Name))
```

## Type filtering

C# uses `OfType<T>()` or `is`. Dynamic LINQ relies on the BPA rule's **Applies to** scope setting.

| C# LINQ | Dynamic LINQ approach |
|---|---|
| `Model.AllColumns.OfType<CalculatedColumn>()` | Set BPA rule scope to **Calculated Columns** |
| `Model.Tables.OfType<CalculationGroupTable>()` | Set BPA rule scope to **Calculation Group Tables** |
| `obj is Measure` | Rule scope handles this; use `ObjectTypeName = "Measure"` if needed |

## Dependency properties

These work identically in both syntaxes, but Dynamic LINQ omits the object prefix.

| C# LINQ | Dynamic LINQ |
|---|---|
| `m.ReferencedBy.Count == 0` | `ReferencedBy.Count = 0` |
| `m.DependsOn.Any()` | `DependsOn.Any()` |
| `c.UsedInRelationships.Any()` | `UsedInRelationships.Any()` |
| `c.ReferencedBy.AnyVisible` | `ReferencedBy.AnyVisible` |

## Annotation methods

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.HasAnnotation("AUTOGEN"))

// Dynamic LINQ
HasAnnotation("AUTOGEN")
```

| C# LINQ | Dynamic LINQ |
|---|---|
| `m.GetAnnotation("key") == "value"` | `GetAnnotation("key") = "value"` |
| `m.HasAnnotation("key")` | `HasAnnotation("key")` |

## Perspective and translation indexers

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.InPerspective["Sales"])

// Dynamic LINQ
InPerspective["Sales"]
```

| C# LINQ | Dynamic LINQ |
|---|---|
| `m.InPerspective["Sales"]` | `InPerspective["Sales"]` |
| `!m.InPerspective["Sales"]` | `not InPerspective["Sales"]` |
| `string.IsNullOrEmpty(m.TranslatedNames["da-DK"])` | `String.IsNullOrEmpty(TranslatedNames["da-DK"])` |

## BPA fix expressions

Fix expressions use `it.` as the assignment target. The left side of the assignment refers to the object that violated the rule.

```
// Set IsHidden to true on the violating object
it.IsHidden = true

// Set description
it.Description = "TODO: Add description"
```

There is no C# LINQ equivalent -- fix expressions are a BPA-specific feature.

## Complete example: same rule in both syntaxes

**Goal:** Find measures that are hidden, have no references and have no description.

C# script:
```csharp
var unused = Model.AllMeasures
    .Where(m => m.IsHidden
        && m.ReferencedBy.Count == 0
        && string.IsNullOrWhiteSpace(m.Description));

foreach (var m in unused)
    Info(m.DaxObjectFullName);
```

BPA rule expression (applies to Measures):
```
IsHidden and ReferencedBy.Count = 0 and String.IsNullOrWhitespace(Description)
```

## See also

- @using-bpa-sample-rules-expressions
- @advanced-filtering-explorer-tree
- @bpa
- @how-to-filter-query-objects-linq
