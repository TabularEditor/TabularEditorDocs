---
uid: kb.bpa-translate-hierarchy-levels
title: Translate Hierarchy Level Names for All Cultures
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring hierarchy level names are translated for all defined cultures.
---

# Translate Hierarchy Level Names for All Cultures

## Overview

This rule identifies hierarchy levels in visible hierarchies that lack name translations for one or more cultures.

- Category: Model Layout
- Severity: Low (1)

## Applies To

- Levels (within hierarchies)

## Why This Matters

- **Incomplete localization**: Level names display in default language only
- **Inconsistent experience**: Partially translated hierarchies
- **User confusion**: Navigation appears incomplete
- **Professional appearance**: Missing translations reduce quality

## When This Rule Triggers

This rule triggers when a hierarchy level meets both of these conditions:

1. The hierarchy containing the level is **visible** to end users
2. At least one culture in the model is **missing a translation** for the level name

That is if you have visible hierarchies with multiple cultures, all the level names within those hierarchies should be translated for each culture.

```csharp
Hierarchy.IsVisible 
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedNames[it]))
```

## How to Fix

### Manual Fix

1. In **TOM Explorer**, select the level
2. In **Properties** pane, expand **Translated Names**
3. Enter translation for each culture

## Common Causes

### Cause 1: New Levels Added

Levels created without translations.

### Cause 2: Culture Added Later

Culture added after hierarchy was created.

### Cause 3: Incomplete Translation

Translation process didn't cover all hierarchy levels.

## Example

### Before Fix

```
Hierarchy: Geography
  Level: Country
    English: "Country"
    Spanish: (missing)
```

### After Fix

```
Hierarchy: Geography
  Level: Country
    English: "Country"
    Spanish: "País"
```

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Translate Visible Names](xref:kb.bpa-translate-visible-names) - Translating object names
- [Translate Perspectives](xref:kb.bpa-translate-perspectives) - Translating perspective names
