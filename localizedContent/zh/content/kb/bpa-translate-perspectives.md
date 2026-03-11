---
uid: kb.bpa-translate-perspectives
title: Translate Perspective Names for All Cultures
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring perspective names are translated for all defined cultures.
---

# Translate Perspective Names for All Cultures

## Overview

This rule identifies model perspectives that lack name translations for one or more cultures.

- Category: Model Layout
- Severity: Low (1)

## Applies To

- Model
- Perspectives

## Why This Matters

- **Incomplete localization**: Perspectives display in default language only
- **Inconsistent experience**: Mix of translated and untranslated perspective names
- **User confusion**: Expected language support not available
- **Professional appearance**: Incomplete translations reduce model quality

## When This Rule Triggers

This rule triggers when a perspective has:

- At least one culture in the model that is **missing a translation** for the perspective name

```csharp
Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedNames[it]))
```

## How to Fix

### Manual Fix

1. In **TOM Explorer**, select the perspective
2. In **Properties** pane, expand **Translated Names**
3. Enter translation for each culture

## Common Causes

### Cause 1: New Perspectives Added

Perspectives created without translations.

### Cause 2: Culture Added Later

Culture added after perspectives were defined.

### Cause 3: Incomplete Translation

Translation workflow didn't cover perspectives.

## Example

### Before Fix

```
Perspective: "Sales Analysis"
English: "Sales Analysis"
German: (missing)
```

### After Fix

```
Perspective: "Sales Analysis"
English: "Sales Analysis"
German: "Vertriebsanalyse"
```

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Translate Visible Names](xref:kb.bpa-translate-visible-names) - Translating object names
- [Translate Descriptions](xref:kb.bpa-translate-descriptions) - Translating descriptions
