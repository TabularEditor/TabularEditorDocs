---
uid: kb.bpa-translate-display-folders
title: Translate Display Folders for All Cultures
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring display folders are translated for all defined cultures.
---

# Translate Display Folders for All Cultures

## Overview

This rule identifies visible objects with display folders that lack translations for one or more cultures.

<<<<<<< HEAD
- Category: Model Layout
=======
- Category: **Model Layout**
>>>>>>> Added Knowledge base for built in BPA rules
- Severity: Low (1)

## Applies To

- Measures
- Hierarchies
- Data Columns
- Calculated Columns
- Calculated Table Columns

## Why This Matters

- **Incomplete localization**: Display folders show in default language only
- **Inconsistent navigation**: Partially translated folder structure
- **User confusion**: Organization appears incomplete
- **Professional appearance**: Missing translations reduce model quality

## When This Rule Triggers

This rule triggers when an object meets all three of these conditions:

1. The object is **visible** to end users (not hidden)
2. The object has a **display folder** assigned (organizing it into a folder structure)
3. At least one culture in the model is **missing a translation** for that display folder

In plain language: visible objects that are organized in display folders should have those folder names translated for all cultures in your model.

```csharp
IsVisible
and not string.IsNullOrEmpty(DisplayFolder)
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedDisplayFolders[it]))
```

## How to Fix

### Automatic Fix

```csharp
TranslatedDisplayFolders.Reset()
```

Resets translations to use the default display folder.

### Manual Fix

1. Select object in **TOM Explorer**
2. Expand **Translated Display Folders** in properties
3. Enter translation for each culture

## Common Causes

### Cause 1: New Display Folders Added

Display folders created without translations.

### Cause 2: Culture Added Later

Culture added after display folders were defined.

### Cause 3: Incomplete Translation

Translation workflow didn't cover display folders.

## Example

### Before Fix

```
Measure: [Total Sales]
Display Folder (English): "Sales Metrics"
Display Folder (French): (missing)
```

### After Fix

```
Measure: [Total Sales]
Display Folder (English): "Sales Metrics"
Display Folder (French): "Métriques de Vente"
```

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Translate Visible Names](xref:kb.bpa-translate-visible-names) - Translating object names
- [Translate Descriptions](xref:kb.bpa-translate-descriptions) - Translating descriptions
