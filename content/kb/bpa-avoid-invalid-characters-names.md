---
uid: kb.bpa-avoid-invalid-characters-names
title: Avoid Invalid Characters in Object Names
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule preventing deployment errors by identifying control characters in object names.
---

# Avoid Invalid Characters in Object Names

## Overview

This best practice rule identifies objects whose names contain invalid control characters (non-printable characters excluding standard whitespace). These characters can cause deployment failures, rendering issues, and data corruption.

<<<<<<< HEAD
- Category: Error Prevention
=======
- Category: **Error Prevention**
>>>>>>> Added Knowledge base for built in BPA rules
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

Control characters in object names cause serious issues:

- **Deployment failures**: Power BI Service and Analysis Services may reject models with invalid characters
- **Rendering problems**: Client tools may display garbled or invisible names
- **DAX parsing errors**: Invalid characters can break DAX expressions referencing the object
- **XML corruption**: Model metadata (TMSL/XMLA) may become malformed
- **Copy/paste issues**: Names may not transfer correctly between applications
- **Encoding problems**: Cross-platform compatibility issues

Standard whitespace (spaces, newlines, carriage returns) is allowed, but control characters should be removed.

## When This Rule Triggers

The rule triggers when an object's name contains control characters that are not standard whitespace:

```csharp
Name.ToCharArray().Any(char.IsControl(it) and !char.IsWhiteSpace(it))
```

This detects problematic characters while allowing legitimate whitespace formatting.

## How to Fix

### Automatic Fix

This rule includes an automatic fix that replaces invalid characters with spaces:

```csharp
Name = string.Concat(
    it.Name.ToCharArray().Select(
        c => (char.IsControl(c) && !char.IsWhiteSpace(c)) ? ' ' : c
    )
)
```

To apply:
1. In the **Best Practice Analyzer** select flagged objects
2. Click **Apply Fix**

### Manual Fix

1. In **TOM Explorer**, select the object
2. In **Properties** pane, locate the **Name** field
3. Edit the name to remove invalid characters
4. Save changes

## Common Causes

### Cause 1: Copy/Paste from Rich Text

Copying names from Word documents, web pages, or emails can introduce hidden formatting characters.

### Cause 2: Automated Name Generation

Scripts generating names may include control characters from source systems.

### Cause 3: Data Import from External Sources

Importing metadata that contains encoding artifacts or control codes.

## Example

### Before Fix

```
Measure Name: "Total\x00Sales"  (contains NULL character)
```

Deployment fails with "Invalid character in object name"

### After Fix

```
Measure Name: "Total Sales"  (NULL replaced with space)
```

Deploys successfully and displays correctly in all tools.

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Avoid Invalid Characters in Descriptions](xref:kb.bpa-avoid-invalid-characters-descriptions) - Similar validation for description properties
- [Trim Object Names](xref:kb.bpa-trim-object-names) - Removing leading/trailing spaces

## Learn More

- [DAX Naming Rules](https://learn.microsoft.com/dax/dax-syntax-reference)
