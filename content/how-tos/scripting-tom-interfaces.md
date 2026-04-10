---
uid: how-to-tom-interfaces
title: Key TOM Interfaces
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# Key TOM Interfaces

The TOM wrapper defines several cross-cutting interfaces that multiple object types implement. Use these interfaces when writing generic code that operates on any object with a given capability, such as setting descriptions, checking visibility or reading annotations.

## Quick reference

```csharp
// Set description on any object that supports it
foreach (var obj in Selected.OfType<IDescriptionObject>())
    obj.Description = "Reviewed";

// Hide any hideable object
foreach (var obj in Selected.OfType<IHideableObject>())
    obj.IsHidden = true;

// Read annotations on any annotatable object
foreach (var obj in Model.AllMeasures.OfType<IAnnotationObject>())
    if (obj.HasAnnotation("Status")) Info(obj.GetAnnotation("Status"));
```

## Interface reference

| Interface | Key members | Implemented by |
|---|---|---|
| (xref:TabularEditor.TOMWrapper.IDescriptionObject) | `Description` | Tables, columns, measures, hierarchies, partitions, relationships, perspectives, roles, data sources |
| (xref:TabularEditor.TOMWrapper.IHideableObject) | `IsHidden`, `IsVisible` | Tables, columns, measures, hierarchies, levels |
| (xref:TabularEditor.TOMWrapper.ITabularPerspectiveObject) | `InPerspective` indexer | Tables, columns, measures, hierarchies |
| (xref:TabularEditor.TOMWrapper.ITranslatableObject) | `TranslatedNames`, `TranslatedDescriptions` | Tables, columns, measures, hierarchies, levels |
| (xref:TabularEditor.TOMWrapper.IFolderObject) | `DisplayFolder`, `TranslatedDisplayFolders` | Measures, columns, hierarchies |
| (xref:TabularEditor.TOMWrapper.IAnnotationObject) | `GetAnnotation()`, `SetAnnotation()`, `HasAnnotation()`, `RemoveAnnotation()`, `Annotations` | Almost all TOM objects |
| (xref:TabularEditor.TOMWrapper.IExtendedPropertyObject) | `GetExtendedProperty()`, `SetExtendedProperty()`, `ExtendedProperties` | Tables, columns, measures, hierarchies, partitions |
| (xref:TabularEditor.TOMWrapper.IExpressionObject) | `Expression` (TE2); `GetExpression()`, `SetExpression()` (TE3) | Measures, calculated columns, calculation items, partitions, KPIs |
| (xref:TabularEditor.TOMWrapper.IDaxObject) | `DaxObjectName`, `DaxObjectFullName`, `ReferencedBy` | Tables, columns, measures |
| (xref:TabularEditor.TOMWrapper.IDaxDependantObject) | `DependsOn` | Measures, calculated columns, calculation items, KPIs, tables, partitions |

## When to use interfaces

Use interfaces when you need to write generic code that applies to multiple object types. Instead of checking each type individually:

```csharp
// Without interfaces -- repetitive
foreach (var m in Selected.Measures)
    m.Description = "Reviewed";
foreach (var c in Selected.Columns)
    c.Description = "Reviewed";
foreach (var t in Selected.Tables)
    t.Description = "Reviewed";
```

Use `OfType<T>()` with an interface to handle all types in one pass:

```csharp
// With interfaces -- handles any object that has a Description
foreach (var obj in Selected.OfType<IDescriptionObject>())
    obj.Description = "Reviewed";
```

## Common interface patterns

### Check and set visibility

```csharp
// Hide all selected objects that support hiding
Selected.OfType<IHideableObject>().ForEach(obj => obj.IsHidden = true);
```

### Set display folder across types

```csharp
// Move all selected folder-bearing objects to a display folder
Selected.OfType<IFolderObject>().ForEach(obj => obj.DisplayFolder = "Archive");
```

### Tag objects with annotations

```csharp
// Tag any annotatable object
Selected.OfType<IAnnotationObject>().ForEach(obj =>
    obj.SetAnnotation("ReviewDate", DateTime.Today.ToString("yyyy-MM-dd")));
```

### Find all objects with a DAX expression

```csharp
// List all objects that have a DAX expression and depend on a specific table
var dependents = Model.AllMeasures.Cast<IDaxDependantObject>()
    .Concat(Model.AllColumns.OfType<CalculatedColumn>().Cast<IDaxDependantObject>())
    .Where(obj => obj.DependsOn.Tables.Any(t => t.Name == "Date"));
```

## See also

- @how-to-check-object-types
- @how-to-filter-query-objects-linq
- @how-to-annotations-extended-properties
- @how-to-work-with-dependencies
