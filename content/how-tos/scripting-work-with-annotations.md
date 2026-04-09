---
uid: how-to-work-with-annotations
title: How to Work with Annotations and Extended Properties
author: Morten Lønskov
updated: 2026-04-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Work with Annotations and Extended Properties

Annotations and extended properties store custom metadata on TOM objects. Annotations are string key-value pairs. Extended properties support both string and JSON types. Both are persisted in the model and survive deployment.

## Quick reference

```csharp
// Annotations
obj.SetAnnotation("key", "value");          // set or create
obj.GetAnnotation("key")                    // returns string or null
obj.HasAnnotation("key")                    // returns bool
obj.RemoveAnnotation("key")                 // delete
obj.GetAnnotations()                        // IEnumerable<string> of annotation names
obj.ClearAnnotations()                      // remove all
obj.Annotations                             // AnnotationCollection (indexer access)

// Extended properties
obj.SetExtendedProperty("key", "value", ExtendedPropertyType.String);
obj.SetExtendedProperty("key", jsonStr, ExtendedPropertyType.Json);
obj.GetExtendedProperty("key")              // returns string
obj.HasExtendedProperty("key")              // returns bool
obj.RemoveExtendedProperty("key")           // delete
obj.GetExtendedPropertyType("key")          // String or Json
obj.ExtendedProperties                      // ExtendedPropertyCollection (indexer access)
```

## Setting and reading annotations

Any object implementing `IAnnotationObject` supports annotations. This includes tables, columns, measures, hierarchies, partitions, perspectives, roles, data sources and relationships.

```csharp
// Tag a measure for automation
var m = Model.AllMeasures.First(m => m.Name == "Revenue");
m.SetAnnotation("AUTOGEN", "true");
m.SetAnnotation("Owner", "Finance Team");

// Read it back
string owner = m.GetAnnotation("Owner");     // "Finance Team"
string missing = m.GetAnnotation("NoKey");   // null
```

## Checking and removing annotations

```csharp
if (m.HasAnnotation("AUTOGEN"))
{
    Info("This measure was auto-generated.");
    m.RemoveAnnotation("AUTOGEN");
}
```

## Iterating all annotations on an object

`GetAnnotations()` returns the annotation names. Use `GetAnnotation(name)` to retrieve values.

```csharp
foreach (var name in m.GetAnnotations())
{
    var value = m.GetAnnotation(name);
    Info($"{name} = {value}");
}
```

## Using the Annotations collection indexer

The `Annotations` property provides indexer access as an alternative to the method-based API.

```csharp
m.Annotations["key"] = "value";        // set
string val = m.Annotations["key"];      // get
```

## Bulk annotation operations

Tag or untag objects across the model.

```csharp
// Tag all hidden measures
Model.AllMeasures
    .Where(m => m.IsHidden)
    .ForEach(m => m.SetAnnotation("ReviewStatus", "Hidden"));

// Remove a specific annotation from all objects that have it
Model.AllMeasures
    .Where(m => m.HasAnnotation("OLD_TAG"))
    .ForEach(m => m.RemoveAnnotation("OLD_TAG"));
```

## Extended properties

Extended properties work similarly to annotations but support a typed `ExtendedPropertyType` of either `String` or `Json`.

```csharp
// Store a JSON extended property (e.g., field parameter metadata)
var table = Model.Tables["Parameter"];
string json = "{\"version\":3,\"values\":[[\"Revenue\"],[\"Cost\"]]}";
table.SetExtendedProperty("ParameterMetadata", json, ExtendedPropertyType.Json);

// Read back
string value = table.GetExtendedProperty("ParameterMetadata");
var type = table.GetExtendedPropertyType("ParameterMetadata"); // ExtendedPropertyType.Json
```

## Dynamic LINQ equivalent

In BPA rule expressions, annotation methods are called directly on the object in context.

| C# script | Dynamic LINQ (BPA) |
|---|---|
| `m.GetAnnotation("key") == "value"` | `GetAnnotation("key") = "value"` |
| `m.HasAnnotation("key")` | `HasAnnotation("key")` |
| `m.GetAnnotation("key") != null` | `GetAnnotation("key") != null` |
| `m.GetAnnotationsCount() > 0` | `GetAnnotationsCount() > 0` |

## See also

- @useful-script-snippets
- @create-field-parameter
- @how-to-navigate-tom-hierarchy
