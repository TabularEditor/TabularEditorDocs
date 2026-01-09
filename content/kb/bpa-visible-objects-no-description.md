---
uid: kb.bpa-visible-objects-no-description
title: Visible Objects Should Have Descriptions
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule ensuring visible model objects have descriptions to improve discoverability and user experience.
---

# Visible Objects Should Have Descriptions

## Overview

This best practice rule identifies visible tables, columns, measures, calculation groups, and user-defined functions that lack descriptions. Adding descriptions improves model usability, documentation quality, and user experience.

- Category: **Maintenance**

- Severity: Low (1)

## Applies To

- Tables
- Calculated Tables
- Data Columns
- Calculated Columns
- Calculated Table Columns
- Measures
- Calculation Groups
- User-Defined Functions (Compatibility Level 1702+)

## Why This Matters

Descriptions provide critical context for model users:

- **Improved discoverability**: Users understand field purpose before using them
- **Better self-service BI**: Business users can work independently with clear guidance
- **Reduced support burden**: Fewer questions about field definitions
- **Enhanced tooltips**: Power BI and Excel show descriptions in hover tooltips
- **Documentation foundation**: Descriptions form the basis for automated documentation
- **Governance and compliance**: Descriptions can include data lineage and business definitions
- **Useage by AI**: AI Agents can better infer the purpose of an object if it has a description. 
Without descriptions, users guess at field meanings, leading to incorrect analysis and increased support requests.

## When This Rule Triggers

The rule triggers when an object is **visible** AND has an empty or whitespace-only description:

```csharp
string.IsNullOrWhitespace(Description)
and
IsHidden == false
```

**Note**: Hidden objects are excluded because they are not meant for end-user consumption.

## How to Fix

### Manual Fix

1. In **TOM Explorer**, select the object
2. In **Properties** pane, locate the **Description** field
3. Enter a clear, concise description
4. Save changes

## Common Causes

### Cause 1: Missing Documentation During Development

Objects created without adding descriptions.

### Cause 2: Rapid Prototyping

Models built quickly without proper documentation.

### Cause 3: Legacy Models

Older models created before description standards were established.

## Example

### Before Fix

```
Measure: [Total Revenue]
Description: (empty)
```

**User experience**: Tooltip shows no information, users must guess measure purpose.

### After Fix

```
Measure: [Total Revenue]
Description: "Total revenue excluding taxes and discounts. Calculated as SUM(Sales[UnitPrice] * Sales[Quantity]). Use for financial reporting."
```

**User experience**: Clear tooltip helps users understand and correctly use the measure.

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

User-Defined Function descriptions are validated at compatibility level **1702** and higher.

## Related Rules

- [Avoid Invalid Characters in Descriptions](xref:kb.bpa-avoid-invalid-characters-descriptions) - Ensuring description quality
