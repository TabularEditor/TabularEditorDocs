---
uid: kb.bpa-many-to-many-single-direction
title: Many-to-Many Relationships Should Use Single Direction
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule to avoid performance issues by using single-direction filtering on many-to-many relationships.
---

# Many-to-Many Relationships Should Use Single Direction

## Overview

This best practice rule identifies many-to-many relationships that use bidirectional cross-filtering. Many-to-many relationships with both-directions filtering cause significant performance degradation.

- Category: Performance
- Severity: Medium (2)

## Applies To

- Relationships

## Why This Matters

- **Severe performance impact**: Engine must evaluate filters in both directions
- **Memory consumption**: Additional filter contexts maintained
- **Ambiguous filter paths**: Multiple routes produce unexpected results
- **Complex DAX logic**: Debugging filter context becomes difficult
- **Risk circular dependencies**: Can lead to infinite evaluation loops

## When This Rule Triggers

The rule triggers when a relationship meets all conditions:

1. `FromCardinality = "Many"`
2. `ToCardinality = "Many"`
3. `CrossFilteringBehavior = "BothDirections"`

## How to Fix

### Manual Fix

1. In **TOM Explorer**, locate the flagged relationship
2. In **Properties** pane, find `Cross Filter Direction`
3. Change from **Both** to **Single**

Choose direction based on typical filter flow:
- From dimension to fact
- From lookup to data table

When opposite-direction filtering is needed, handle explicitly in measures:

```dax
SalesWithCrossFilter = 
CALCULATE(
    SUM('Sales'[Amount]),
    CROSSFILTER('BridgeTable'[Key], 'DimensionTable'[Key], Both)
)
```

## Common Causes

### Cause 1: Default Both-Direction Setting

Model designer applied bidirectional filtering by default.

### Cause 2: Misunderstood Requirements

Believed both-direction filtering was necessary for all scenarios.

### Cause 3: Quick Fix Approach

Used both-direction filtering to solve a specific problem without considering performance.

## Example

### Before Fix

```
'Sales' (Many) <--> (Many) 'ProductBridge'
Cross Filter Direction: Both  ← Problem
```

### After Fix

```
'Sales' (Many) --> (Many) 'ProductBridge'
Cross Filter Direction: Single
```

When Products need to filter Sales, use DAX:

```dax
SalesForSelectedProducts = 
VAR SelectedProducts = VALUES('Products'[ProductKey])
RETURN
CALCULATE(
    SUM('Sales'[Amount]),
    TREATAS(SelectedProducts, 'ProductBridge'[ProductKey])
)
```

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Relationship Data Types Must Match](xref:kb.bpa-relationship-same-datatype) - Ensuring relationship integrity

## Learn More

- [Many-to-Many Relationships in Power BI](https://learn.microsoft.com/power-bi/transform-model/desktop-many-to-many-relationships)
- [Relationship Cross-Filtering](https://learn.microsoft.com/power-bi/transform-model/desktop-relationships-understand)
- [DAX CROSSFILTER Function](https://dax.guide/crossfilter/)
- [DAX TREATAS Function](https://dax.guide/treatas)
