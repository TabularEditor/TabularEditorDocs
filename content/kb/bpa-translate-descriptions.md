---
uid: kb.bpa-translate-descriptions
title: Translate Descriptions for All Cultures
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring object descriptions are translated for all defined cultures.
---

# Translate Descriptions for All Cultures

## Overview

This rule identifies objects with descriptions that lack translations for one or more cultures.

<<<<<<< HEAD
- Category: Model Layout
=======
- Category: **Model Layout**
>>>>>>> Added Knowledge base for built in BPA rules
- Severity: Low (1)

## Applies To

- Model
- Tables
- Measures
- Hierarchies
- Levels
- Perspectives
- Data Columns
- Calculated Columns
- Calculated Tables
- Calculated Table Columns

## Why This Matters

- **Incomplete localization**: Descriptions display in default language only
- **Inconsistent help text**: Users see mix of languages
- **User confusion**: Documentation appears incomplete
- **Professional appearance**: Missing translations reduce model quality

## When This Rule Triggers

```csharp
not string.IsNullOrEmpty(Description) 
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedDescriptions[it]))
```
This rule triggers when an object meets both of these conditions:

1. The object has a description (not empty)
2. At least one culture in the model is missing a translation for that description

In other words, if you have descriptions and multiple cultures defined, all descriptions should be translated for all cultures.


## How to Fix

### Manual Fix

1. In **TOM Explorer**, select the object
2. In **Properties** pane, expand **Translated Descriptions**
3. Enter translation for each culture

## Common Causes

### Cause 1: New Descriptions Added

Descriptions created without translations.

### Cause 2: Culture Added Later

Culture added after descriptions were written.

### Cause 3: Incomplete Translation

Translation process didn't cover descriptions.

## Example

### Before Fix

```
Measure: [Total Revenue]
Description (English): "Sum of all revenue"
Description (Spanish): (missing)
```

### After Fix

```
Measure: [Total Revenue]
Description (English): "Sum of all revenue"
Description (Spanish): "Suma de todos los ingresos"
```

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Translate Visible Names](xref:kb.bpa-translate-visible-names) - Translating object names
- [Translate Display Folders](xref:kb.bpa-translate-display-folders) - Translating display folders
