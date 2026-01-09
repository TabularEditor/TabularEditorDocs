---
uid: kb.bpa-hide-foreign-keys
title: Hide Foreign Key Columns
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule for hiding foreign key columns to simplify the model for end users.
---

# Hide Foreign Key Columns

## Overview

This best practice rule identifies foreign key columns (many-side of relationships) that are visible to end users. Foreign keys should be hidden because they serve only as relationship connectors and provide no analytical value when displayed.

- Category: Formatting

- Severity: Medium (2)

## Applies To

- Data Columns
- Calculated Columns
- Calculated Table Columns

## Why This Matters

Visible foreign key columns create unnecessary clutter:

- **User confusion**: Foreign keys look like useful data but duplicate dimension attributes
- **Redundant fields**: Users see both the key and the related dimension attributes
- **Larger field lists**: More objects to scroll through finding relevant fields
- **Incorrect usage**: Users may group by keys instead of proper dimension attributes
- **Poor visualizations**: Charts showing key values instead of descriptive names

Foreign keys exist only to create relationships between tables. Once relationships are established, users should work with dimension attributes, not the foreign keys themselves.

## When This Rule Triggers

The rule triggers when a column is:

1. Used as the "from" column in a relationship (many-side)
2. The relationship has many cardinality on the from-side
3. The column is visible (`IsHidden = false`)

```csharp
UsedInRelationships.Any(FromColumn.Name == current.Name and FromCardinality == "Many")
and
IsHidden == false
```

## How to Fix

### Automatic Fix

This rule includes an automatic fix:

```csharp
IsHidden = true
```

To apply:
1. In the **Best Practice Analyzer** select flagged foreign key columns
2. Click **Apply Fix**

### Manual Fix

1. In **TOM Explorer**, locate the foreign key column
2. In **Properties** pane, set **IsHidden** to **true**
3. Save changes

## Common Causes

### Cause 1: Incomplete Model Setup

Foreign keys remain visible after creating relationships.

### Cause 2: Bulk Import

Tables imported without post-processing to hide foreign keys.

### Cause 3: Legacy Models

Older models where foreign key hiding wasn't enforced.

## Example

### Before Fix

```
Sales Table Fields (visible):
  - OrderDate
  - CustomerKey  ← Foreign key (should be hidden)
  - ProductKey   ← Foreign key (should be hidden)
  - SalesAmount
  - Quantity
```

**User experience**: Field list is cluttered. Users might mistakenly use `Sales[CustomerKey]` instead of `Customer[CustomerName]`.

### After Fix

```
Sales Table Fields (visible):
  - OrderDate
  - SalesAmount
  - Quantity
```

**User experience**: Clean field list. Users naturally use dimension attributes, relationship filtering works automatically.

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Set SummarizeBy to None for Numeric Columns](xref:kb.bpa-do-not-summarize-numeric) - Related column configuration
- [Format String for Columns](xref:kb.bpa-format-string-columns) - Column display settings
