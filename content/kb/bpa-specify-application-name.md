---
uid: kb.bpa-specify-application-name
title: Specify Application Name in Connection Strings
author: Morten Lønskov
updated: 2026-01-09
description: Best practice rule for including application name in SQL Server connection strings to enable monitoring and troubleshooting.
---

# Specify Application Name in Connection Strings

## Overview

This rule identifies SQL Server provider data sources that lack an Application Name parameter in their connection strings. Including the application name enables better monitoring and troubleshooting.

<<<<<<< HEAD
- Category: Performance
=======
- Category: **Performance**
>>>>>>> Added Knowledge base for built in BPA rules
- Severity: Low (1)

## Applies To

- Provider Data Sources

## Why This Matters

- **Query tracking**: DBAs can identify which application generated queries
- **Performance monitoring**: Isolate tabular model queries for analysis
- **Troubleshooting**: Quickly identify source of problem queries
- **Auditing**: Track data access by application

## When This Rule Triggers

This rule triggers when a data source meets both of these conditions:

1. The connection string uses a SQL Server provider (contains `SQLNCLI`, `SQLOLEDB`, or `MSOLEDBSQL`)
2. The connection string does NOT include an `Application Name` parameter

In other words, the rule identifies SQL Server connections that are missing the application name identifier.

## How to Fix

### Manual Fix

Add Application Name to your connection string:

```
Provider=MSOLEDBSQL;Data Source=ServerName;Initial Catalog=DatabaseName;Application Name=Tabular Editor;Integrated Security=SSPI;
```

## Example

### Before Fix

```
Provider=MSOLEDBSQL;Data Source=localhost;Initial Catalog=AdventureWorks;
```

### After Fix

```
Provider=MSOLEDBSQL;Data Source=localhost;Initial Catalog=AdventureWorks;Application Name=Sales Model;
```

Result: Queries now identifiable in SQL Server monitoring tools.

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher.

## Related Rules

- [Remove Unused Data Sources](xref:kb.bpa-remove-unused-data-sources) - Data source maintenance
