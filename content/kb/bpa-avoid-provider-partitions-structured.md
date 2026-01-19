---
uid: kb.bpa-avoid-provider-partitions-structured
title: Avoid Provider Partitions with Structured Data Sources
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule preventing deployment errors by identifying legacy provider partitions used with structured data sources in Power BI.
---

# Avoid Provider Partitions with Structured Data Sources

## Overview

This best practice rule identifies partitions that use legacy provider-based queries (SourceType = Query) with structured data sources in Power BI models. This combination is not supported in Power BI Service and will cause deployment failures.

- Category: **Error Prevention**

- Severity: Medium (2)

## Applies To

- Partitions

## Why This Matters

Power BI Service requires structured data sources to use Power Query (M) partitions rather than legacy provider partitions. Using provider partitions with structured data sources causes:

- **Deployment failures**: Models fail to publish to Power BI Service
- **Refresh errors**: Scheduled refresh operations fail in the service
- **Compatibility issues**: The model cannot be shared or deployed properly
- **Migration blockers**: Prevents moving from Analysis Services to Power BI

## When This Rule Triggers

The rule triggers when a partition meets all these conditions:

1. `SourceType = "Query"` (legacy provider partition)
2. `DataSource.Type = "Structured"` (Power Query/M data source)
3. `Model.Database.CompatibilityMode != "AnalysisServices"` (Power BI or Azure AS)

This combination indicates a structural mismatch that Power BI cannot process.

## How to Fix

### Manual Fix

1. In **TOM Explorer**, select the affected partition
2. In **Properties** pane, note the existing query
3. Create a new **Power Query** partition with M expression
4. Delete the old provider partition after verifying the new one works

## Common Causes

### Cause 1: Migration from Analysis Services

Models migrated from SQL Server Analysis Services retain legacy provider partitions.

### Cause 2: Mixed Partition Types

Mixing partition types during model development creates incompatible configurations.

## Example

### Before Fix

```
Partition: Sales_Partition
  SourceType: Query
  Query: SELECT * FROM Sales
  DataSource: PowerQuerySource (Type: Structured)
```

**Error**: Deployment fails to Power BI Service

### After Fix

```
Partition: Sales_Partition
  SourceType: M
  Expression: 
    let
        Source = Sql.Database("server", "database"),
        Sales = Source{[Schema="dbo",Item="Sales"]}[Data]
    in
        Sales
  DataSource: PowerQuerySource (Type: Structured)
```

**Result**: Deploys successfully to Power BI Service

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher when deployed to Power BI or Azure Analysis Services.

## Related Rules

- [Data Column Must Have Source](xref:kb.bpa-data-column-source) - Ensuring column source mappings
