---
uid: kb.bpa-powerbi-latest-compatibility
title: Use Latest Compatibility Level for Power BI Models
author: Morten Lønskov
updated: 2026-09-23
description: Best practice rule ensuring Power BI models use the latest compatibility level for optimal features and performance.
---

# Use Latest Compatibility Level for Power BI Models

## Overview

This rule flags Power BI models below the highest compatibility level that your Tabular Editor 3 version supports. New model features, such as new DAX functions and TOM properties, require the newer levels.

- Category: Governance
- Severity: High (3)

## Applies To

- Model (Power BI semantic models only)

## Why This Matters

- new DAX functions and model features aren't available below the level that introduces them
- a model kept at a recent level needs smaller upgrades later

## When This Rule Triggers

The rule triggers for Power BI models whose compatibility level isn't the current maximum:

```csharp
Model.Database.CompatibilityMode=="PowerBI" 
and Model.Database.CompatibilityLevel<>[CurrentMaxLevel]
```

## How to Fix

### Automatic Fix

The rule's automatic fix sets the compatibility level to the highest level your installed version of Tabular Editor 3 supports. To get a newer level, update Tabular Editor 3.

```csharp
Model.Database.CompatibilityLevel = [PowerBIMaxCompatibilityLevel]
```

### Manual Fix

1. In the TOM Explorer, select **Model** and expand **Database** in the **Properties** view.
2. Set **Compatibility Level** to the latest level.
3. Test the DAX expressions and features of the model.
4. Deploy to the Power BI Service.

See @update-compatibility-level.

## Common Causes

### Cause 1: Model Created in Power BI Desktop

Power BI Desktop doesn't always create models at the latest compatibility level.

### Cause 2: Model Created at Lower Level

An older version of Power BI Desktop created the model.

### Cause 3: Conservative Approach

A team policy delays upgrades.

## Example

### Before Fix

```text
Model Compatibility Level: 1500
Current Maximum Level: 1706
```

### After Fix

```text
Model Compatibility Level: 1706 (Latest)
```

The model can use [custom calendars](xref:calendars) (1701+), [DAX user-defined functions](xref:udfs) (1702+), [user-context calculated columns](xref:user-context-calculated-columns) (1705+) and the `StringIndexingBehavior` column property (1706+).

## Compatibility Level

This rule applies to Power BI models at all compatibility levels.