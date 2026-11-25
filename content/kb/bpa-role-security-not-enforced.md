---
uid: kb.bpa-role-security-not-enforced
title: Row-Level and Object-Level Security Require Read Permission
author: Morten Lønskov
updated: 2026-11-12
description: Best practice rule that flags roles whose row-level or object-level security has no effect or blocks deployment because of the role's model permission.
---

# Row-Level and Object-Level Security Require Read Permission

## Overview

This rule flags roles that hold security settings their model permission ignores or doesn't allow. Row-level security (RLS) filters and object-level security (OLS) take effect only for roles whose `ModelPermission` is `Read` or `ReadRefresh`.

- Category: Security
- Severity: High (3)

## Applies To

- Roles (models whose compatibility mode isn't Power BI)

## Why This Matters

- an `Administrator` or `Refresh` role with table permissions fails to deploy. SQL Server 2025 Analysis Services rejects it even when the table permissions hold no row filter or OLS, with an error like "... is an administrator role and therefore doesn't allow TablePermission objects under it"
- members of a role with `None` permission can't connect to the model, so the role's RLS and OLS never restrict anyone
- the security that the role's settings describe isn't the security its members get

## When This Rule Triggers

The rule triggers for a role in a model that isn't in Power BI compatibility mode when either of these is true:

- `ModelPermission` is `Administrator` or `Refresh` and the role has any table permission
- `ModelPermission` is `None` and a table permission has a row filter, a table with OLS set to `None` or, at compatibility level 1400 and higher, a column with OLS set to `None`

```csharp
Model.Database.CompatibilityMode != "PowerBI"

and

(
    ((ModelPermission == "Administrator" or ModelPermission == "Refresh") and TablePermissions.Any())
    or
    (ModelPermission == "None" and TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) or MetadataPermission == "None" or (Model.Database.CompatibilityLevel >= 1400 and ColumnPermissions.Any(it == "None"))))
)
```

An OLS setting of `Read` doesn't count as security for a `None` role. For roles in Power BI models, see @kb.bpa-powerbi-role-read-permission.

## How to Fix

The rule has no automatic fix. Changing a role's permission changes who can query which data, so decide per role.

### Manual Fix

If the role's members are report users whose data access you want to restrict:

1. In the **TOM Explorer**, select the role.
2. In the **Properties** view, set **Model Permission** to `Read`, or to `ReadRefresh` if the members also refresh the model.

If the role's members need administrator or refresh access:

1. In the **TOM Explorer**, expand the role.
2. Delete the table permissions under the role.

See @object-properties-security for the values of **Model Permission**.

## Common Causes

### Cause 1: Permission Changed After Security Was Defined

The role had `Read` permission when its row filters were added, and someone later set it to `Administrator` or `Refresh`.

### Cause 2: Role Copied from an Administrator Role

A role duplicated from an administrator or processing role kept the source role's permission when filters were added to it.

### Cause 3: New Role Without Permission

A new role has `None` permission until you set it. The role got its security settings before anyone set its permission.

## Example

### Before Fix

```text
Role:               Regional Managers
Model Permission:   Administrator
Row Level Security: 'Region'[Country] = "Denmark"
```

Deployment to SQL Server 2025 Analysis Services fails. RLS doesn't apply to administrators, so the filter has no effect on the role's members.

### After Fix

```text
Role:               Regional Managers
Model Permission:   Read
Row Level Security: 'Region'[Country] = "Denmark"
```

## Related Rules

- [Power BI Roles Must Have Read Permission](xref:kb.bpa-powerbi-role-read-permission)
- [Roles Without Security Override Secured Roles](xref:kb.bpa-role-unrestricted-read)
- [Avoid Members in Both an RLS Role and an OLS Role](xref:kb.bpa-role-mixed-rls-ols-members)

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher. Column OLS is checked at compatibility level 1400 and higher.
