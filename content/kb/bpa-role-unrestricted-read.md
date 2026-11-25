---
uid: kb.bpa-role-unrestricted-read
title: Roles Without Security Override Secured Roles
author: Morten Lønskov
updated: 2026-11-12
description: Best practice rule that flags roles granting unrestricted Read access in a model where other roles restrict data with row-level or object-level security.
---

# Roles Without Security Override Secured Roles

## Overview

This rule flags roles that grant `Read` access to all data while other roles in the model restrict access with row-level security (RLS) or object-level security (OLS). Permissions from several roles are combined: a user who is a member of this role and of a secured role can query all data.

- Category: Security
- Severity: Medium (2)

## Applies To

- Roles

## Why This Matters

- adding a user to an unrestricted role removes the RLS and OLS of every other role the user belongs to
- a user who belongs to the wrong role sees data that the model's security is meant to hide, and no query returns an error

## When This Rule Triggers

The rule triggers for a role when all of these are true:

- `ModelPermission` is `Read` or `ReadRefresh`
- none of the role's table permissions has a row filter, a table with OLS set to `None` or, at compatibility level 1400 and higher, a column with OLS set to `None`
- another role with `Read` or `ReadRefresh` permission has at least one of those settings

```csharp
(ModelPermission == "Read" or ModelPermission == "ReadRefresh")

and

not TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) or MetadataPermission == "None" or (Model.Database.CompatibilityLevel >= 1400 and ColumnPermissions.Any(it == "None")))

and

Model.Roles.Any(
    (ModelPermission == "Read" or ModelPermission == "ReadRefresh")
    and TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) or MetadataPermission == "None" or (Model.Database.CompatibilityLevel >= 1400 and ColumnPermissions.Any(it == "None")))
)
```

A blank row filter and an OLS setting of `Read` restrict nothing, and the rule treats a role that has only those as unrestricted. In a model where no `Read` or `ReadRefresh` role is secured, the rule doesn't trigger.

## How to Fix

The rule has no automatic fix. A role that grants all data is often intentional, for example for managers or a support team.

### Manual Fix

1. In the **TOM Explorer**, select the flagged role and review its **Members**.
2. Do one of the following:
   - if every member is allowed to see all data, keep the role and right-click the result in the **Best Practice Analyzer** and choose **Ignore item**
   - if the role's members need restricted access, add row filters or OLS to the role
   - if a member also belongs to a secured role by mistake, remove the member from this role

See @object-properties-security and @using-bpa.

## Common Causes

### Cause 1: Role for Users Who See All Data

The model has a role for managers or administrators of the report who need all data.

### Cause 2: Role Created for Testing

A role without filters was added to test the model and kept.

### Cause 3: Filters Removed from a Role

The role's row filters were cleared, and the role still has members.

## Example

### Before Fix

```text
Role: All Data      Model Permission: Read   Row Level Security: (none)
                    Members: CONTOSO\alice, CONTOSO\bob
Role: Europe        Model Permission: Read   Row Level Security: 'Region'[Continent] = "Europe"
                    Members: CONTOSO\alice
```

`CONTOSO\alice` sees all regions, because `All Data` grants what `Europe` restricts.

### After Fix

```text
Role: All Data      Model Permission: Read   Row Level Security: (none)
                    Members: CONTOSO\bob
Role: Europe        Model Permission: Read   Row Level Security: 'Region'[Continent] = "Europe"
                    Members: CONTOSO\alice
```

The rule still flags `All Data`. Ignore the result if `CONTOSO\bob` is allowed to see all data.

## Related Rules

- [Row-Level and Object-Level Security Require Read Permission](xref:kb.bpa-role-security-not-enforced)
- [Power BI Roles Must Have Read Permission](xref:kb.bpa-powerbi-role-read-permission)
- [Avoid Members in Both an RLS Role and an OLS Role](xref:kb.bpa-role-mixed-rls-ols-members)

## Compatibility Level

This rule applies to models with compatibility level **1200** and higher. Column OLS is checked at compatibility level 1400 and higher.
