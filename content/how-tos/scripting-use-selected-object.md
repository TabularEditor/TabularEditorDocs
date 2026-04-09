---
uid: how-to-use-selected-object
title: How to Use the Selected Object
author: Morten Lønskov
updated: 2026-04-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Use the Selected Object

The `Selected` object provides access to whatever is currently selected in the **TOM Explorer** tree. Use it to write scripts that operate on user-selected objects rather than hardcoded names.

## Quick reference

```csharp
// Singular (exactly one selected, throws if 0 or 2+)
Selected.Measure
Selected.Table
Selected.Column

// Plural (zero or more, safe to iterate)
Selected.Measures
Selected.Tables
Selected.Columns
Selected.Hierarchies
Selected.Partitions
Selected.Levels
Selected.CalculationItems
Selected.Roles
Selected.DataSources

// Guard clause
if (Selected.Measures.Count() == 0) { Error("Select at least one measure."); return; }

// Iterate and modify
foreach (var m in Selected.Measures)
    m.FormatString = "0.00";

// Using ForEach extension
Selected.Measures.ForEach(m => m.DisplayFolder = "KPIs");
```

## Singular vs plural accessors

The `Selected` object exposes both singular and plural accessors for each object type.

| Accessor | Returns | Behavior when count is not 1 |
|---|---|---|
| `Selected.Measure` | single `Measure` | Throws exception if 0 or 2+ measures selected |
| `Selected.Measures` | `IEnumerable<Measure>` | Returns empty collection if none selected |

Use the **singular** form when your script requires exactly one object. Use the **plural** form when the script should work on one or more objects.

## Guard clauses

Always validate the selection before performing operations. This prevents confusing error messages.

```csharp
// Require at least one measure
if (Selected.Measures.Count() == 0)
{
    Error("No measures selected. Select one or more measures and run again.");
    return;
}

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
if (Selected.Tables.Count() != 1) { Error("Select one table."); return; }

var table = Selected.Table;
var newMeasure = table.AddMeasure(
    "Row Count",
    "COUNTROWS(" + table.DaxObjectFullName + ")"
);
```

## Mixed selections

When you need to handle multiple object types from the selection, use `Selected.Objects` which returns all selected items as `ITabularNamedObject`.

```csharp
foreach (var obj in Selected.Objects)
{
    if (obj is IDescriptionObject desc)
        desc.Description = "Reviewed on " + DateTime.Today.ToString("yyyy-MM-dd");
}
```

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

## See also

- @csharp-scripts
- @advanced-scripting
- @how-to-navigate-tom-hierarchy
- @script-helper-methods
