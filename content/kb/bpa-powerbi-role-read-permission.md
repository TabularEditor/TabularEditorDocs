---
uid: kb.bpa-powerbi-role-read-permission
title: Power BI Roles Must Have Read Permission
author: Morten Lønskov
updated: 2026-11-12
description: Best practice rule that flags roles in Power BI semantic models whose model permission is anything other than Read.
---

# Power BI Roles Must Have Read Permission

## Overview

This rule flags roles in Power BI semantic models whose `ModelPermission` isn't `Read`. Power BI supports only the `Read` permission on model roles. Access such as refreshing or editing the model comes from workspace roles and semantic model permissions in the Power BI service.

- Category: Security
- Severity: High (3)

## Applies To

- Roles (Power BI semantic models only)

## Why This Matters

- the Power BI service rejects the deployment of a role with `None`, `ReadRefresh`, `Refresh` or `Administrator` permission, with or without table permissions, with the error "Please set the permission level for your row-level security (RLS) roles to 'Read'"
- model roles in Power BI apply row-level security (RLS) and object-level security (OLS) to their members and grant no other access

## When This Rule Triggers

The rule triggers for every role in a model in Power BI compatibility mode whose permission isn't `Read`:

```csharp
Model.Database.CompatibilityMode == "PowerBI"

and

ModelPermission != "Read"
```

Roles in models in Analysis Services compatibility mode are checked by @kb.bpa-role-security-not-enforced.

## How to Fix

The rule has no automatic fix. Setting a role to `Read` gives its members access to data, so review each role first.

### Manual Fix

1. In the **TOM Explorer**, select the role.
2. Check that the role's row filters and OLS restrict what its members see.
3. In the **Properties** view, set **Model Permission** to `Read`.
4. Grant refresh, build or edit access through workspace roles or semantic model permissions in the Power BI service.

> [!WARNING]
> If the role has no row filters and no OLS, setting it to `Read` gives its members access to all data in the model.

RLS and OLS don't apply to users with the workspace **Admin**, **Member** or **Contributor** role. See @object-properties-security.

## Common Causes

### Cause 1: Role Copied from an Analysis Services Model

The role came from an Analysis Services model, where `Administrator`, `ReadRefresh` and `Refresh` are valid permissions.

### Cause 2: Role for a Refresh Account

The role was created to let a service account refresh the model.

### Cause 3: New Role Without Permission

A new role has `None` permission until you set it.

## Example

### Before Fix

```text
Role:               Sales Refresh
Model Permission:   ReadRefresh
Row Level Security: 'Region'[Country] = "Denmark"
```

### After Fix

```text
Role:               Sales Refresh
Model Permission:   Read
Row Level Security: 'Region'[Country] = "Denmark"
```

The refresh account gets the **Contributor** workspace role in the Power BI service and isn't a member of the role.

## Related Rules

- [Row-Level and Object-Level Security Require Read Permission](xref:kb.bpa-role-security-not-enforced)
- [Roles Without Security Override Secured Roles](xref:kb.bpa-role-unrestricted-read)
- [Avoid Members in Both an RLS Role and an OLS Role](xref:kb.bpa-role-mixed-rls-ols-members)

## Compatibility Level

This rule applies to Power BI models with compatibility level **1200** and higher.
