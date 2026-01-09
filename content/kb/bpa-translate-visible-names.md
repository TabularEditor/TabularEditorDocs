---
uid: kb.bpa-translate-visible-names
title: Translate Visible Object Names for All Cultures
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring visible object names are translated for all defined cultures.
---

# Translate Visible Object Names for All Cultures

## Overview

This rule identifies visible objects whose names lack translations for one or more cultures defined in the model.

<<<<<<< HEAD
- Category: Model Layout
=======
- Category: **Model Layout**
>>>>>>> Added Knowledge base for built in BPA rules
- Severity: Low (1)

## Applies To

- Tables
- Measures
- Hierarchies
- Data Columns
- Calculated Columns
- Calculated Tables
- Calculated Table Columns

## Why This Matters

- **Incomplete localization**: Users in different cultures see untranslated names
- **Inconsistent experience**: Mix of translated and untranslated content
- **User confusion**: Expected language support not provided
- **Professional appearance**: Incomplete translations appear unpolished

## When This Rule Triggers

This rule triggers when an object meets both of these conditions:

1. The object is **visible** to end users (not hidden)
2. At least one culture in the model is **missing a translation** for the object name

In other words visible objects with multiple cultures defined should have their names translated for each culture.

```csharp
IsVisible 
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedNames[it]))
```

## How to Fix

### Manual Fix

1. In **TOM Explorer**, select the object
2. In **Properties** pane, expand **Translated Names**
3. Enter translation for each culture
4. Save changes

## Common Causes

### Cause 1: New Objects Added

New objects created without translations.

### Cause 2: Culture Added Later

Culture added to model after objects were created.

### Cause 3: Incomplete Translation Process

Translation workflow didn't cover all objects.

## Example

### Before Fix

```
Measure: [Total Sales]
English: "Total Sales"
Spanish: (missing)
French: (missing)
```

### After Fix

```
Measure: [Total Sales]
English: "Total Sales"
Spanish: "Total de Ventas"
French: "Total des Ventes"
```

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Translate Perspectives](xref:kb.bpa-translate-perspectives) - Translating perspective names
- [Translate Descriptions](xref:kb.bpa-translate-descriptions) - Translating descriptions
