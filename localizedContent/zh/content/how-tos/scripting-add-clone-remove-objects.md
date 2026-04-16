---
uid: how-to-add-clone-remove-objects
title: How to Add, Clone and Remove Objects
author: Morten Lønskov
updated: 2026-04-10
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
var table = Model.Tables["Sales"];
var measure = table.Measures["Revenue"];

// Add objects -- all parameters after the first are optional.
// See sections below for parameter details.
table.AddMeasure("Name", "DAX Expression", "Display Folder");
table.AddCalculatedColumn("Name", "DAX Expression", "Display Folder");
table.AddDataColumn("Name", "SourceColumn", "Display Folder", DataType.String);
table.AddHierarchy("Name", "Display Folder", table.Columns["Year"], table.Columns["Month"]);
Model.AddCalculatedTable("Name", "DAX Expression");
Model.AddPerspective("Name");
Model.AddRole("Name");
Model.AddTranslation("da-DK");

// Relationships
var rel = Model.AddRelationship();
rel.FromColumn = Model.Tables["Sales"].Columns["ProductKey"];   // many (N) side
rel.ToColumn = Model.Tables["Product"].Columns["ProductKey"];   // one (1) side

// Clone
var clone = measure.Clone("New Name");                         // same table
var cloneToOther = measure.Clone("New Name", true, Model.Tables["Reporting"]); // different table

// Delete (always materialize with ToList() before modifying a collection in a loop)
measure.Delete();
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

## Adding measures

`AddMeasure()` creates and returns a new `Measure` on a table. The first parameter is the name, the second is a DAX expression and the third is the display folder. All parameters except the first are optional.

Capture the returned object in a variable to set additional properties. This pattern is the same across all `Add*` methods.

```csharp
var table = Model.Tables["Sales"];

// Create a measure and set properties on the returned object
var m = table.AddMeasure(
    "Revenue",                   // name
    "SUM('Sales'[Amount])"       // DAX expression
);
m.FormatString = "#,##0.00";
m.Description = "Total sales amount";

// With display folder
var m2 = table.AddMeasure(
    "Cost",                      // name
    "SUM('Sales'[Cost])",        // DAX expression
    "Financial"                  // display folder
);
```

## Adding columns

```csharp
// Calculated column -- first parameter is the name, second is a DAX expression
var cc = table.AddCalculatedColumn(
    "Profit",                              // name
    "'Sales'[Amount] - 'Sales'[Cost]"      // DAX expression
);
cc.DataType = DataType.Decimal;
cc.FormatString = "#,##0.00";

// Data column -- maps to a source column in the partition query
var dc = table.AddDataColumn(
    "Region",              // name
    "RegionName",          // source column name
    "Geography",           // display folder
    DataType.String        // data type
);
```

> [!WARNING]
> Adding a data column does not modify the table's partition query. You must update the M expression or SQL query separately to include a source column that matches the `sourceColumn` parameter.

## Adding hierarchies

The `levels` parameter is variadic. Pass any number of columns in a single call to create the corresponding levels automatically.

```csharp
var dateTable = Model.Tables["Date"];
var h = dateTable.AddHierarchy(
    "Calendar",                        // name
    "",                                // display folder
    dateTable.Columns["Year"],         // level 1
    dateTable.Columns["Quarter"],      // level 2
    dateTable.Columns["Month"]         // level 3
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
var ct = Model.AddCalculatedTable(
    "DateKey List",                    // name
    "VALUES('Date'[DateKey])"          // DAX expression
);
```

## Adding relationships

`AddRelationship()` creates and returns an empty relationship. You must set the columns explicitly.

`FromColumn` is the many (N) side and `ToColumn` is the one (1) side. Tabular Editor does not detect the direction automatically. A useful mnemonic: F for From, F for Fact table (the many side).

New relationships default to `CrossFilteringBehavior.OneDirection` and `IsActive = true`. Set these only if you need a different value.

```csharp
var rel = Model.AddRelationship();
rel.FromColumn = Model.Tables["Sales"].Columns["ProductKey"];   // many side (fact)
rel.ToColumn = Model.Tables["Product"].Columns["ProductKey"];   // one side (dimension)

// Only set these if you need non-default values:
// rel.CrossFilteringBehavior = CrossFilteringBehavior.BothDirections;
// rel.IsActive = false;
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

A common pattern: iterate selected columns and create derived measures. Note the use of `DaxObjectFullName` which returns the fully qualified, properly quoted DAX reference (e.g., `'Sales'[Amount]`) to avoid quoting errors.

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

Call `Delete()` on any named object to remove it. When modifying a collection in a loop (deleting, adding or moving objects), always call `.ToList()` first to materialize a snapshot.

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
>
> - Always call `.ToList()` or `.ToArray()` before modifying objects in a loop. Without it, modifying the collection during iteration causes: `"Collection was modified; enumeration operation may not complete."`
> - `AddRelationship()` creates an incomplete relationship. You must assign both `FromColumn` and `ToColumn` before the model validates.
> - `Column` is abstract, but you can access all base properties (`Name`, `DataType`, `FormatString`, `IsHidden`) without casting. Only cast to a subtype for type-specific properties.
> - `Clone()` copies all metadata including annotations, translations and perspective membership. Remove unwanted metadata after cloning.

## 另见

- @实用脚本片段
- @script-create-sum-measures-from-columns
- @how-to-navigate-tom-hierarchy
- @how-to-use-selected-object
- (xref:TabularEditor.TOMWrapper.Measure) -- Measure API reference
- (xref:TabularEditor.TOMWrapper.Column) -- Column API reference
- (xref:TabularEditor.TOMWrapper.Hierarchy) -- Hierarchy API reference
- (xref:TabularEditor.TOMWrapper.SingleColumnRelationship) -- Relationship API reference
