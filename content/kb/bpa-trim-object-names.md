---
uid: kb.bpa-trim-object-names
title: Trim Leading and Trailing Spaces from Object Names
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule for removing leading and trailing spaces from object names to prevent confusion and referencing issues.
---

# Trim Leading and Trailing Spaces from Object Names

## Overview

This best practice rule identifies objects whose names contain leading or trailing spaces. These unnecessary spaces cause DAX referencing issues, display problems, and general confusion.

- Category: **Naming Conventions**
- Severity: Low (1)

## Applies To

- Model
- Tables
- Measures
- Hierarchies
- Levels
- Perspectives
- Partitions
- Provider Data Sources
- Data Columns
- Calculated Columns
- Calculated Tables
- Calculated Table Columns
- Structured Data Sources
- Named Expressions
- Model Roles
- Calculation Groups
- Calculation Items

## Why This Matters

- **DAX syntax problems**: Extra spaces require careful bracket notation
- **Display inconsistency**: Objects appear misaligned in field lists
- **Search difficulties**: Users may not find objects when searching
- **Maintenance confusion**: Developers may create duplicates not noticing spaces

## When This Rule Triggers

The rule triggers when an object name starts or ends with a space:

```csharp
Name.StartsWith(" ") or Name.EndsWith(" ")
```

## How to Fix

### Manual Fix

1. In **TOM Explorer**, locate the object
2. Right-click and select **Rename** (or press F2)
3. Remove leading/trailing spaces
4. Press Enter to confirm

## Common Causes

### Cause 1: Accidental Spacebar Presses

Accidental spacebar presses during naming.

### Cause 2: Copy/Paste from External Sources

Copy/paste from documents with formatting.

### Cause 3: Duplicating objects

When duplicating objects the name will have an added " copy" post-fixed. It is easy to miss deleting the space before "copy" 

## Example

### Before Fix

```
Measures:
  - Total Sales
  -  Total Sales  (with spaces - appears different!)
```

DAX: `[ Total Sales]` - Which one?

### After Fix

```
Measures:
  - Total Sales (single consistent measure)
```

DAX: `[Total Sales]` - Unambiguous

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Avoid Invalid Characters in Names](xref:kb.bpa-avoid-invalid-characters-names) - Related naming hygiene rule
