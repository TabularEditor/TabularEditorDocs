---
uid: how-to-use-selected-object
title: How to Use the Selected Object
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# How to Use the Selected Object

The `Selected` object provides access to whatever is currently selected in the @tom-explorer-view-reference tree. Use it to write scripts that operate on user-selected objects rather than hardcoded names.

## Quick reference

```csharp
// Singular (exactly one selected, throws if 0 or 2+)
Selected.Measure
Selected.Table
Selected.Column

// Guard clause
if (Selected.Measures.Count() == 0) { Error("Select at least one measure."); return; }

// Iterate and modify
foreach (var m in Selected.Measures)
    m.FormatString = "0.00";

// Using ForEach extension
Selected.Measures.ForEach(m => m.DisplayFolder = "KPIs");
```

Plural accessors (zero or more, safe to iterate):

- `Selected.Measures`
- `Selected.Tables`
- `Selected.Columns`
- `Selected.Hierarchies`
- `Selected.Particiones`
- `Selected.Levels`
- `Selected.CalculationItems`
- `Selected.Roles`
- `Selected.DataSources`

## Singular vs plural accessors

The `Selected` object exposes both singular and plural accessors for each object type.

| Accessor            | Returns                | Behavior when count is not 1                                                                                        |
| ------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `Selected.Measure`  | single `Measure`       | Throws exception if 0 or 2+ measures selected                                                                       |
| `Selected.Measures` | `IEnumerable<Measure>` | Returns a collection that may be empty but is never null. Safe to iterate directly. |

Use the **singular** form when your script requires exactly one object. Use the **plural** form when the script should work on zero or more objects.

## Guard clauses

The plural accessor returns zero or more objects. A script may silently do nothing with an empty collection, or require a minimum count. Use a guard clause for the latter.

```csharp
// Require at least one measure
if (Selected.Measures.Count() == 0)
{
    Error("No measures selected. Select one or more measures and run again.");
    return;
}
```

```csharp
// Require exactly one table
if (Selected.Tables.Count() != 1)
{
    Error("Select exactly one table.");
    return;
}
var table = Selected.Table;
```

For scripts that accept multiple object types, combine checks:

```csharp
if (Selected.Columns.Count() == 0 && Selected.Measures.Count() == 0)
{
    Error("Select at least one column or measure.");
    return;
}
```

## Iterating selected objects

The plural accessor returns a collection you can iterate with `foreach` or LINQ.

```csharp
// Set display folder on all selected measures
foreach (var m in Selected.Measures)
    m.DisplayFolder = "Sales Metrics";

// Hide all selected columns
Selected.Columns.ForEach(c => c.IsHidden = true);

// Add to a perspective
Selected.Measures.ForEach(m => m.InPerspective["Sales"] = true);
```

## Working with the selected table

When a single table is selected, use `Selected.Table` to add new objects to it.

```csharp
var t = Selected.Table;
t.AddMeasure("Row Count", "COUNTROWS(" + t.DaxObjectFullName + ")");
```

## Mixed selections

When you need to handle multiple object types from the selection, iterate `Selected` directly. The `Selected` variable itself implements `IEnumerable<ITabularNamedObject>`.

```csharp
foreach (var desc in Selected.OfType<IDescriptionObject>())
{
    desc.Description = "Reviewed on " + DateTime.Today.ToString("yyyy-MM-dd");
}
```

See @how-to-filter-query-objects-linq for more on LINQ filtering and @how-to-tom-interfaces for interface-based object handling.

## Try/catch for selection dialogs

When using `SelectTable()`, `SelectColumn()`, or `SelectMeasure()` helper methods, wrap them in try/catch to handle user cancellation.

```csharp
try
{
    var table = SelectTable(Model.Tables, null, "Pick a table:");
    Info("You selected: " + table.Name);
}
catch
{
    Error("No table selected.");
}
```

> [!NOTE]
> The `Selected` object is only available in interactive contexts (Tabular Editor UI and macros). When running scripts via the CLI with the `-S` flag, `Selected` reflects the objects specified by `-O` arguments or is empty if none are specified.

## Ver también

- @csharp-scripts
- @advanced-scripting
- @how-to-navigate-tom-hierarchy
- @script-helper-methods
