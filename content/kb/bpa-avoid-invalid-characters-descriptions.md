---
uid: kb.bpa-avoid-invalid-characters-descriptions
title: Avoid Invalid Characters in Descriptions
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule preventing display and deployment issues by identifying control characters in object descriptions.
---

# Avoid Invalid Characters in Descriptions

## Overview

This best practice rule identifies objects whose descriptions contain invalid control characters (non-printable characters excluding standard whitespace). These characters can cause display problems, metadata corruption, and deployment failures.

- Category: **Error Prevention**

- Severity: High (3)

## Applies To

- Tables
- Measures
- Hierarchies
- Levels
- Perspectives
- Partitions
- Data Columns
- Calculated Columns
- Calculated Table Columns
- KPIs
- Model Roles
- Calculation Groups
- Calculation Items

## Why This Matters

Control characters in descriptions cause various issues:

- **Display corruption**: Tooltips and documentation panels may show garbled text
- **Metadata problems**: TMSL/XMLA export may produce invalid XML
- **Deployment failures**: Power BI Service or Analysis Services may reject the model
- **Documentation issues**: Generated documentation may break formatting
- **Encoding errors**: Cross-platform synchronization problems
- **User confusion**: Invisible characters create confusing or corrupted descriptions

Standard whitespace (spaces, newlines, tabs) is acceptable, but non-printable control characters should be removed.

## When This Rule Triggers

The rule triggers when an object's description contains control characters that are not standard whitespace:

```csharp
Description.ToCharArray().Any(char.IsControl(it) and !char.IsWhiteSpace(it))
```

This detects problematic characters while allowing legitimate whitespace formatting.

## How to Fix

### Automatic Fix

This rule includes an automatic fix that replaces invalid characters with spaces:

```csharp
Description = string.Concat(
    it.Description.ToCharArray().Select(
        c => (char.IsControl(c) && !char.IsWhiteSpace(c)) ? ' ' : c
    )
)
```

To apply:
1. In the **Best Practice Analyzer** select flagged objects
3. Click **Apply Fix**

### Manual Fix

1. In **TOM Explorer**, select the object
2. In **Properties** pane, locate the **Description** field
3. Edit the description to remove invalid characters
4. Save changes

## Common Causes

### Cause 1: Copy/Paste from Rich Text

Copying descriptions from Word documents, web pages, or emails can introduce hidden formatting characters.

### Cause 2: Automated Documentation Generation

Scripts generating descriptions may include control characters from source systems.

### Cause 3: Data Import from External Sources

Importing metadata that contains encoding artifacts or control codes.

## Example

### Before Fix

```
Measure: [Total Revenue]
Description: "Calculates\x00total\x0Brevenue"  (contains NULL and vertical tab)
```

Tooltip displays: "Calculates□total□revenue" (with visible corruption)

### After Fix

```
Measure: [Total Revenue]
Description: "Calculates total revenue"  (control characters replaced with spaces)
```

Tooltip displays correctly: "Calculates total revenue"

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Avoid Invalid Characters in Names](xref:kb.bpa-avoid-invalid-characters-names) - Similar validation for object names
- [Visible Objects Should Have Descriptions](xref:kb.bpa-visible-objects-no-description) - Ensuring descriptions exist
