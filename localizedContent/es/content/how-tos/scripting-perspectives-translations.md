---
uid: how-to-work-with-perspectives-translations
title: Cómo trabajar con perspectivas y traducciones
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo trabajar con perspectivas y traducciones

Las perspectivas controlan qué objetos son visibles en determinadas vistas del cliente. Las traducciones (configuraciones regionales) proporcionan nombres y descripciones localizados, además de carpetas de visualización localizadas. Ambas usan propiedades de indexador en objetos TOM. Consulta @how-to-navigate-tom-hierarchy para obtener más información sobre cómo acceder a los objetos TOM y a sus indexadores.

## Referencia rápida

```csharp
// Perspectives
measure.InPerspective["Sales"] = true;              // include in perspective
measure.InPerspective["Sales"] = false;             // exclude from perspective
var isIn = measure.InPerspective["Sales"];           // check membership

// Translations
measure.TranslatedNames["da-DK"] = "Omsætning";    // set translated name
measure.TranslatedDescriptions["da-DK"] = "...";    // set translated description
measure.TranslatedDisplayFolders["da-DK"] = "Salg"; // set translated folder

var name = measure.TranslatedNames["da-DK"];     // read translation (empty string if unset)

// Iterate cultures
foreach (var culture in Model.Cultures)
    Info(culture.Name);                              // "da-DK", "de-DE", etc.
```

## Configurar la pertenencia a perspectivas

El indexador de perspectiva `InPerspective` está disponible en tablas, columnas, medidas y jerarquías (es decir, en cualquier objeto (xref:TabularEditor.TOMWrapper.ITabularPerspectiveObject)).

```csharp
// Add all measures in a table to a perspective
Model.Tables["Sales"].Measures.ForEach(m => m.InPerspective["Sales Report"] = true);

// Remove a table and its children from a perspective
var table = Model.Tables["Internal"];
table.InPerspective["Sales Report"] = false;
```

## Copiar la pertenencia a perspectivas

Copia la visibilidad en las perspectivas de un objeto a otro.

```csharp
var source = Model.AllMeasures.First(m => m.Name == "Revenue");
var target = Model.AllMeasures.First(m => m.Name == "Revenue YTD");

foreach (var p in Model.Perspectives)
    target.InPerspective[p.Name] = source.InPerspective[p.Name];
```

## Crear y eliminar perspectivas

```csharp
// Create a new perspective (empty upon creation -- add objects as shown above)
var p = Model.AddPerspective("Executive Dashboard");

// Remove a perspective
Model.Perspectives["Old View"].Delete();
```

## Establecer traducciones

Los indexadores de traducción están disponibles en los objetos que implementan (xref:TabularEditor.TOMWrapper.ITranslatableObject) (tablas, columnas, medidas, jerarquías y niveles). Las traducciones de carpetas de visualización requieren objetos que implementen (xref:TabularEditor.TOMWrapper.IFolderObject) (medidas, columnas y jerarquías).

```csharp
var m = Model.AllMeasures.First(m => m.Name == "Revenue");
m.TranslatedNames["da-DK"] = "Omsætning";
m.TranslatedDescriptions["da-DK"] = "Total omsætning i DKK";
m.TranslatedDisplayFolders["da-DK"] = "Salg";
```

## Encontrar traducciones faltantes

```csharp
foreach (var culture in Model.Cultures)
{
    var missing = Model.AllMeasures
        .Where(m => string.IsNullOrEmpty(m.TranslatedNames[culture.Name]));

    Info($"{culture.Name}: {missing.Count()} measures without translated names");
}
```

## Establecer traducciones en bloque a partir de una convención de nomenclatura

```csharp
// Copy the default name as the translation for cultures that are missing it
foreach (var culture in Model.Cultures)
{
    Model.AllMeasures
        .Where(m => string.IsNullOrEmpty(m.TranslatedNames[culture.Name]))
        .ForEach(m => m.TranslatedNames[culture.Name] = m.Name);
}
```

## Crear y eliminar configuraciones regionales

```csharp
// Add a new culture
var culture = Model.AddTranslation("fr-FR");

// Remove a culture
Model.Cultures["fr-FR"].Delete();
```

## Equivalente en LINQ dinámico

En las expresiones de reglas de BPA, se accede directamente a los indexadores de perspectiva y de traducción.

| C# Script                                          | LINQ dinámico (BPA)           |
| -------------------------------------------------- | ------------------------------------------------ |
| `m.InPerspective["Sales"]`                         | `InPerspective["Sales"]`                         |
| `!m.InPerspective["Sales"]`                        | `not InPerspective["Sales"]`                     |
| `string.IsNullOrEmpty(m.TranslatedNames["da-DK"])` | `String.IsNullOrEmpty(TranslatedNames["da-DK"])` |

## Ver también

- @perspectivas-traducciones
- @importar-exportar-traducciones
- @how-to-navigate-tom-hierarchy
