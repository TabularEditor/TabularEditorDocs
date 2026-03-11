---
uid: kb.bpa-remove-unused-data-sources
title: Remove Unused Data Sources
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule for removing orphaned data sources to reduce model complexity and improve maintainability.
---

# Remove Unused Data Sources

## Overview

This best practice rule identifies data sources that are not referenced by any partitions or table expressions. Removing unused data sources reduces model complexity, improves maintainability, and prevents confusion.

- Category: Maintenance
- Severity: Low (1)

## Applies To

- Provider Data Sources
- Structured Data Sources

## Why This Matters

Unused data sources create unnecessary overhead:

- **Maintenance burden**: Credentials and connection strings must be maintained for unused connections
- **Security concerns**: Unnecessary connection strings may expose sensitive information
- **Model complexity**: Extra objects clutter the data source list
- **Confusion**: Developers may mistakenly use obsolete data sources
- **Deployment issues**: Unused data sources may reference systems that no longer exist
- **Documentation overhead**: Extra objects require explanation in model documentation

Unused data sources typically result from:
- Refactoring partitions to use different sources
- Consolidating multiple sources into one
- Removing tables without cleaning up their data sources
- Testing alternative connection methods

## When This Rule Triggers

The rule triggers when a data source meets all these conditions:

```csharp
UsedByPartitions.Count() == 0
and not Model.Tables.Any(SourceExpression.Contains(OuterIt.Name))
and not Model.AllPartitions.Any(Query.Contains(OuterIt.Name))
```

In other words:
1. No partitions directly reference the data source
2. No table source expressions (M queries) reference the data source by name
3. No partition queries contain the data source name

## How to Fix

### Automatic Fix

This rule includes an automatic fix that deletes the unused data source:

```csharp
Delete()
```

To apply:
1. In the **Best Practice Analyzer** select flagged objects
3. Click **Apply Fix**

### Manual Fix

1. In **TOM Explorer**, expand the **Data Sources** node
2. Right-click the unused data source
3. Select **Delete**
4. Confirm the deletion

### Before Deleting

Verify the data source is truly unused:
- Check all partitions in all tables
- Search M expressions for references to the data source name
- Review custom expressions and calculated tables
- Ensure no documentation references the connection

## Example

### Before Fix

```
Data Sources:
  - SQLServer_Production (Provider, used by Sales partition)
  - SQLServer_Staging (Provider, NOT USED)  ← Remove
  - AzureSQL_Archive (Structured, NOT USED)  ← Remove
  - PowerQuery_Web (Structured, used by Product partition)
```

### After Fix

```
Data Sources:
  - SQLServer_Production (Provider, used by Sales partition)
  - PowerQuery_Web (Structured, used by Product partition)
```

**Result**: Simpler model with only necessary data sources

## False Positives

The rule may flag data sources that are:
- Referenced through dynamic M expressions using variables
- Used in commented-out partition queries
- Referenced by name in annotations or descriptions

**Solution**: Manually verify before deleting; add comments or annotations if the data source should be kept for documentation purposes.

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.