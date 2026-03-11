---
uid: kb.bpa-perspectives-no-objects
title: Perspectives Should Contain Objects
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule for removing empty perspectives that contain no visible objects.
---

# Perspectives Should Contain Objects

## Overview

This best practice rule identifies perspectives that don't contain any visible tables. Empty perspectives serve no purpose and should be removed.

- Category: Maintenance
- Severity: Low (1)

## Applies To

- Perspectives

## Why This Matters

- **User confusion**: Empty perspectives appear in client tools but show no data

## When This Rule Triggers

The rule triggers when a perspective has no visible tables:

```csharp
Model.Tables.Any(InPerspective[current.Name]) == false
```

## How to Fix

### Automatic Fix

This rule includes an automatic fix that deletes the empty perspective:

```csharp
Delete()
```

To apply:
1. Run the **Best Practice Analyzer**
2. Select the empty perspectives
3. Click **Apply Fix**

### Manual Fix

1. In **TOM Explorer**, expand the **Perspectives** node
2. Right-click the empty perspective
3. Select **Delete**

## Common Causes

### Cause 1: Removed All Tables

All tables removed from perspective without deleting it.

### Cause 2: Incomplete Configuration

Perspective created during design but never populated.

## Example

### Before Fix

```
Perspectives:
  - Sales (contains: Sales, Customer, Product tables) ✓
  - Marketing (contains: NO TABLES) ✗
```

### After Fix

```
Perspectives:
  - Sales (contains: Sales, Customer, Product tables) ✓
```

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Learn More

- [Perspectives in Tabular Models](https://learn.microsoft.com/analysis-services/tabular-models/perspectives-ssas-tabular)

