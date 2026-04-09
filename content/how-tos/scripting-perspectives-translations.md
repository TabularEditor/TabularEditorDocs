---
uid: how-to-work-with-perspectives-translations
title: How to Work with Perspectives and Translations
author: Morten Lønskov
updated: 2026-04-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Work with Perspectives and Translations

Perspectives control which objects are visible in specific client views. Translations (cultures) provide localized names, descriptions and display folders. Both use indexer properties on TOM objects.

## Quick reference

```csharp
// Perspectives
measure.InPerspective["Sales"] = true;              // include in perspective
measure.InPerspective["Sales"] = false;             // exclude from perspective
bool isIn = measure.InPerspective["Sales"];          // check membership

// Translations
measure.TranslatedNames["da-DK"] = "Omsætning";    // set translated name
measure.TranslatedDescriptions["da-DK"] = "...";    // set translated description
measure.TranslatedDisplayFolders["da-DK"] = "Salg"; // set translated folder

string name = measure.TranslatedNames["da-DK"];     // read translation (empty string if unset)

// Iterate cultures
foreach (var culture in Model.Cultures)
    Info(culture.Name);                              // "da-DK", "de-DE", etc.
```

## Setting perspective membership

The `InPerspective` indexer is available on tables, columns, measures and hierarchies (any `ITabularPerspectiveObject`).

```csharp
// Add all measures in a table to a perspective
Model.Tables["Sales"].Measures.ForEach(m => m.InPerspective["Sales Report"] = true);

// Remove a table and its children from a perspective
var table = Model.Tables["Internal"];
table.InPerspective["Sales Report"] = false;
```

## Copying perspective membership

Copy the perspective visibility from one object to another.

```csharp
var source = Model.AllMeasures.First(m => m.Name == "Revenue");
var target = Model.AllMeasures.First(m => m.Name == "Revenue YTD");

foreach (var p in Model.Perspectives)
    target.InPerspective[p.Name] = source.InPerspective[p.Name];
```

## Creating and removing perspectives

```csharp
// Create a new perspective
var p = Model.AddPerspective("Executive Dashboard");

// Remove a perspective
Model.Perspectives["Old View"].Delete();
```

## Setting translations

Translation indexers are available on objects implementing `ITranslatableObject` (tables, columns, measures, hierarchies, levels). Display folder translations require `IFolderObject` (measures, columns, hierarchies).

```csharp
var m = Model.AllMeasures.First(m => m.Name == "Revenue");
m.TranslatedNames["da-DK"] = "Omsætning";
m.TranslatedDescriptions["da-DK"] = "Total omsætning i DKK";
m.TranslatedDisplayFolders["da-DK"] = "Salg";
```

## Finding missing translations

```csharp
foreach (var culture in Model.Cultures)
{
    var missing = Model.AllMeasures
        .Where(m => string.IsNullOrEmpty(m.TranslatedNames[culture.Name]));

    Info($"{culture.Name}: {missing.Count()} measures without translated names");
}
```

## Bulk-setting translations from a naming convention

```csharp
// Copy the default name as the translation for cultures that are missing it
foreach (var culture in Model.Cultures)
{
    Model.AllMeasures
        .Where(m => string.IsNullOrEmpty(m.TranslatedNames[culture.Name]))
        .ForEach(m => m.TranslatedNames[culture.Name] = m.Name);
}
```

## Creating and removing cultures

```csharp
// Add a new culture
var culture = Model.AddTranslation("fr-FR");

// Remove a culture
Model.Cultures["fr-FR"].Delete();
```

## Dynamic LINQ equivalent

In BPA rule expressions, perspective and translation indexers are accessed directly.

| C# script | Dynamic LINQ (BPA) |
|---|---|
| `m.InPerspective["Sales"]` | `InPerspective["Sales"]` |
| `!m.InPerspective["Sales"]` | `not InPerspective["Sales"]` |
| `string.IsNullOrEmpty(m.TranslatedNames["da-DK"])` | `String.IsNullOrEmpty(TranslatedNames["da-DK"])` |

## See also

- @perspectives-translations
- @import-export-translations
- @how-to-navigate-tom-hierarchy
