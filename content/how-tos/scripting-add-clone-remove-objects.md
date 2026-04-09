---
uid: how-to-add-clone-remove-objects
title: How to Add, Clone and Remove Objects
author: Morten Lønskov
updated: 2026-04-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Add, Clone and Remove Objects

C# scripts can create new model objects, clone existing ones and delete objects. This article covers the Add, Clone and Delete patterns.

## Quick reference

```csharp
// Add objects
table.AddMeasure("Name", "DAX Expression", "Display Folder");
table.AddCalculatedColumn("Name", "DAX Expression", "Display Folder");
table.AddDataColumn("Name", "SourceColumn", "Display Folder", DataType.String);
table.AddHierarchy("Name", "Display Folder", col1, col2, col3);
Model.AddCalculatedTable("Name", "DAX Expression");
Model.AddPerspective("Name");
Model.AddRole("Name");
Model.AddTranslation("da-DK");

// Relationships
var rel = Model.AddRelationship();
rel.FromColumn = Model.Tables["Sales"].Columns["ProductKey"];
rel.ToColumn = Model.Tables["Product"].Columns["ProductKey"];

// Clone
var clone = measure.Clone("New Name");                         // same table
var clone = measure.Clone("New Name", true, targetTable);      // different table

// Delete (always materialize first when deleting in a loop)
measure.Delete();
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

## Adding measures

`AddMeasure()` creates a new measure on a table. All parameters except the first are optional.

```csharp
var table = Model.Tables["Sales"];

// Simple measure
var m = table.AddMeasure("Revenue", "SUM('Sales'[Amount])");
m.FormatString = "#,##0.00";
m.Description = "Total sales amount";

// With display folder
var m2 = table.AddMeasure("Cost", "SUM('Sales'[Cost])", "Financial");
```

## Adding columns

```csharp
// Calculated column (DAX expression)
var cc = table.AddCalculatedColumn("Profit", "'Sales'[Amount] - 'Sales'[Cost]");
cc.DataType = DataType.Decimal;
cc.FormatString = "#,##0.00";

// Data column (maps to a source column)
var dc = table.AddDataColumn("Region", "RegionName", "Geography", DataType.String);
```

## Adding hierarchies

Pass columns as parameters to automatically create levels.

```csharp
var dateTable = Model.Tables["Date"];
var h = dateTable.AddHierarchy(
    "Calendar",
    "",
    dateTable.Columns["Year"],
    dateTable.Columns["Quarter"],
    dateTable.Columns["Month"]
);
```

Or add levels one at a time:

```csharp
var h = dateTable.AddHierarchy("Fiscal");
h.AddLevel(dateTable.Columns["FiscalYear"]);
h.AddLevel(dateTable.Columns["FiscalQuarter"]);
h.AddLevel(dateTable.Columns["FiscalMonth"]);
```

## Adding calculated tables

```csharp
var ct = Model.AddCalculatedTable("DateKey List", "VALUES('Date'[DateKey])");
```

## Adding relationships

`AddRelationship()` creates an empty relationship. You must set the columns explicitly.

```csharp
var rel = Model.AddRelationship();
rel.FromColumn = Model.Tables["Sales"].Columns["ProductKey"];
rel.ToColumn = Model.Tables["Product"].Columns["ProductKey"];
rel.CrossFilteringBehavior = CrossFilteringBehavior.OneDirection;
rel.IsActive = true;
```

## Cloning objects

`Clone()` creates a copy with all properties, annotations and translations.

```csharp
// Clone within the same table
var original = Model.AllMeasures.First(m => m.Name == "Revenue");
var copy = original.Clone("Revenue Copy");

// Clone to a different table (with translations)
var copy2 = original.Clone("Revenue Copy", true, Model.Tables["Reporting"]);
```

## Generating measures from columns

A common pattern: iterate selected columns and create derived measures.

```csharp
foreach (var col in Selected.Columns)
{
    var m = col.Table.AddMeasure(
        "Sum of " + col.Name,
        "SUM(" + col.DaxObjectFullName + ")",
        col.DisplayFolder
    );
    m.FormatString = "0.00";
    col.IsHidden = true;
}
```

## Deleting objects

Call `Delete()` on any named object to remove it. When deleting inside a loop, always call `.ToList()` first to avoid modifying the collection during iteration.

```csharp
// Delete a single object
Model.AllMeasures.First(m => m.Name == "Temp").Delete();

// Delete multiple objects safely
Model.AllMeasures
    .Where(m => m.HasAnnotation("DEPRECATED"))
    .ToList()
    .ForEach(m => m.Delete());
```

## Common pitfalls

> [!WARNING]
> - Always call `.ToList()` before deleting objects in a loop. Without it, modifying the collection during iteration causes an exception.
> - `AddRelationship()` creates an incomplete relationship. You must assign both `FromColumn` and `ToColumn` before the model validates. Failing to do so results in a validation error.
> - New objects have default property values. Set `DataType`, `FormatString`, `IsHidden` and other properties explicitly after creation.
> - `Clone()` copies all metadata including annotations, translations and perspective membership. If you do not want to inherit these, remove them after cloning.

## See also

- @useful-script-snippets
- @script-create-sum-measures-from-columns
- @how-to-navigate-tom-hierarchy
- @how-to-use-selected-object
