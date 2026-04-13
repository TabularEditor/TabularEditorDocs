---
uid: how-to-dynamic-linq-vs-csharp-linq
title: How Dynamic LINQ Differs from C# LINQ
author: Morten Lønskov
updated: 2026-04-10
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
| **TOM Explorer** tree filter (`:` prefix)\* | Dynamic LINQ |

\* Tabular Editor 2 only.

## Syntax comparison

In Dynamic LINQ, the object is implicit -- there is no lambda parameter like `m.` or `c.`. In BPA, the surrounding context is the **Applies to** scope setting, which determines which object type the expression evaluates against.

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
Model.AllMeasures.Where(m => m.IsHidden && m.Description == "");
```

```
// Dynamic LINQ: implicit "it" -- properties are accessed directly
IsHidden and Description = ""
```

## Parent object navigation

Both use dot notation, but C# requires the lambda parameter.

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.Table.IsHidden);
```

```
// Dynamic LINQ
Table.IsHidden
```

## Collection methods

C# LINQ uses lambdas inside collection methods. Dynamic LINQ uses implicit context within collection methods, with `outerIt` to reference the parent object.

```csharp
// C# LINQ: count columns with no description
Model.Tables.Where(t => t.Columns.Count(c => c.Description == "") > 5);
```

```
// Dynamic LINQ: same logic
Columns.Count(Description = "") > 5
```

### The outerIt keyword

Inside a nested collection method in Dynamic LINQ, `it` refers to the inner object (e.g., a column). Use `outerIt` to reference the outer object (e.g., the table).

```
// BPA rule on Tables: find tables where any column name matches the table name
Columns.Any(Name = outerIt.Name)
```

In C#, the outer lambda parameter `t` remains in scope throughout the inner lambda body. The inner lambda `c => c.Name == t.Name` can reference `t` directly because it is captured by closure.

```csharp
// C# equivalent -- t is accessible inside the inner lambda via closure
Model.Tables.Where(t => t.Columns.Any(c => c.Name == t.Name));
```

## Type filtering

C# uses `OfType<T>()` or `is`. In BPA, the rule's **Applies to** scope handles type filtering. You do not need type checks in the expression itself.

| C# LINQ | Dynamic LINQ approach |
|---|---|
| `Model.AllColumns.OfType<CalculatedColumn>()` | Set BPA rule scope to **Calculated Columns** |
| `Model.Tables.OfType<CalculationGroupTable>()` | Set BPA rule scope to **Calculation Group Tables** |

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
Model.AllMeasures.Where(m => m.HasAnnotation("AUTOGEN"));
```

```
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
Model.AllMeasures.Where(m => m.InPerspective["Sales"]);
```

```
// Dynamic LINQ
InPerspective["Sales"]
```

| C# LINQ | Dynamic LINQ |
|---|---|
| `m.InPerspective["Sales"]` | `InPerspective["Sales"]` |
| `!m.InPerspective["Sales"]` | `not InPerspective["Sales"]` |
| `string.IsNullOrEmpty(m.TranslatedNames["da-DK"])` | `String.IsNullOrEmpty(TranslatedNames["da-DK"])` |

## BPA fix expressions

Fix expressions use `it.` as the assignment target. The `it` refers to the specific object that violated the rule -- the same object highlighted in the BPA results list.

For example, given a BPA rule with expression `IsHidden and String.IsNullOrWhitespace(Description)` applied to **Measures**, each measure that matches appears in the BPA results. When you apply the fix, `it` refers to that specific measure:

```
// Set the description on the violating measure
it.Description = "TODO: Add description"

// Unhide the violating object
it.IsHidden = false
```

While fix expressions have no direct C# LINQ equivalent, you can achieve the same result in a script:

```csharp
foreach (var m in Model.AllMeasures.Where(m => m.IsHidden && string.IsNullOrWhiteSpace(m.Description)))
{
    m.Description = "TODO: Add description";
}
```

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
