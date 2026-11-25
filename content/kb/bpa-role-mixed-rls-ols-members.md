---
uid: kb.bpa-role-mixed-rls-ols-members
title: Avoid Members in Both an RLS Role and an OLS Role
author: Morten Lønskov
updated: 2026-11-12
description: Best practice rule that flags roles sharing a member with another role when one role applies row-level security and the other object-level security to the same or directly related tables.
---

# Avoid Members in Both an RLS Role and an OLS Role

## Overview

This rule flags roles that share a member with another role when one of the two roles filters rows of a table with row-level security (RLS) and the other hides columns or tables with object-level security (OLS) on the same table or a directly related table. Queries from that member fail with an error that the combination of active roles isn't supported.

- Category: Security
- Severity: High (3)

## Applies To

- Roles

## Why This Matters

- queries from an affected user fail, so reports built on the model don't work for that user
- the error appears only when a user who belongs to both roles queries the model, so testing each role on its own doesn't reveal it

## When This Rule Triggers

The rule compares each role with `Read` or `ReadRefresh` permission to every other role with `Read` or `ReadRefresh` permission. It triggers when the two roles have a member with the same name and one of these combinations applies:

| One role | Other role |
|---|---|
| a row filter on a table | OLS `None` on some columns of the same table, while the table and at least one column stay visible |
| a row filter on a table | OLS `None` on a table, or on columns of a table, joined to the filtered table by an active relationship, in either direction |

The rule flags both roles. A role that has both RLS and OLS counts as either side, so a role with a row filter and column OLS next to a role with a row filter on the related table also triggers the rule. Member names are compared without regard to case, so `CONTOSO\alice` and `contoso\Alice` match.

```csharp
(ModelPermission == "Read" or ModelPermission == "ReadRefresh")

and

Model.Roles.Any(
    Name != current.Name
    and (ModelPermission == "Read" or ModelPermission == "ReadRefresh")
    and Members.Any(current.Members.Any(string.Equals(MemberName, outerIt.MemberName, StringComparison.OrdinalIgnoreCase)))
    and (
        current.TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) and outerIt.TablePermissions.Any(Table.Name == outerIt.Table.Name and MetadataPermission != "None" and ColumnPermissions.Any(it == "None") and ColumnPermissions.Any(it != "None")))
        or current.TablePermissions.Any(MetadataPermission != "None" and ColumnPermissions.Any(it == "None") and ColumnPermissions.Any(it != "None") and outerIt.TablePermissions.Any(Table.Name == outerIt.Table.Name and not string.IsNullOrWhiteSpace(FilterExpression)))
        or Model.Relationships.Any(IsActive and (
            (not string.IsNullOrWhiteSpace(current.RowLevelSecurity[FromTable.Name]) and outerIt.TablePermissions.Any(Table.Name == outerIt.ToTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))))
            or (not string.IsNullOrWhiteSpace(current.RowLevelSecurity[ToTable.Name]) and outerIt.TablePermissions.Any(Table.Name == outerIt.FromTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))))
            or (current.TablePermissions.Any(Table.Name == outerIt.FromTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))) and not string.IsNullOrWhiteSpace(outerIt.RowLevelSecurity[ToTable.Name]))
            or (current.TablePermissions.Any(Table.Name == outerIt.ToTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))) and not string.IsNullOrWhiteSpace(outerIt.RowLevelSecurity[FromTable.Name]))
        ))
    )
)
```

### Combinations the Rule Doesn't Flag

These combinations work, and the rule doesn't flag them:

- RLS and OLS on tables with no relationship between them, or joined only by an inactive relationship
- table-level OLS, with or without column OLS, on an RLS table that has no relationships
- column OLS that hides every column of the RLS table
- an OLS setting of `Read`, which restricts nothing

These combinations also fail at query time, and the rule doesn't detect them:

- RLS and OLS on tables two or more active relationships apart
- table-level OLS on an RLS table that has active relationships
- users who belong to both roles through a group, for example when one role lists a security group and the other lists a user in that group, or when the two roles list different groups with a member in common
- members that aren't in the loaded model, such as role members managed in the Power BI service

> [!NOTE]
> Microsoft's [object-level security documentation](https://learn.microsoft.com/analysis-services/tabular-models/object-level-security#restrictions) states that any combination of RLS and OLS from different roles is unsupported. The rule follows the behavior of SQL Server 2025 Analysis Services and the Power BI service, where the combinations listed above as working don't fail.

## How to Fix

The rule has no automatic fix.

### Manual Fix

Do one of the following for each member that both roles list:

- define the row filter and the OLS in one role, and make the member a member of only that role. RLS and OLS in the same role work together.
- remove the member from one of the two roles

Set the row filters and OLS of the combined role in the **Properties** view. See [Combine OLS with RLS](xref:data-security-setup-ols#5-combine-ols-with-rls) and @object-properties-security.

## Common Causes

### Cause 1: Separate Roles for Rows and Columns

The model has one set of roles that filters data by region and another that hides sensitive columns, and some users need both.

### Cause 2: Members Added Over Time

A user was added to an RLS role and later to an OLS role for another report.

## Example

### Before Fix

```text
Relationship: 'Invoices'[CustomerKey] -> 'Customers'[CustomerKey] (active)

Role: Europe           Model Permission: Read
                       Row Level Security on 'Customers': [Continent] = "Europe"
                       Members: CONTOSO\alice
Role: No Sales Value   Model Permission: Read
                       Object Level Security on 'Invoices'[Value]: None
                       Members: contoso\Alice
```

Queries from `CONTOSO\alice` fail with an error.

### After Fix

```text
Role: Europe No Sales Value   Model Permission: Read
                              Row Level Security on 'Customers': [Continent] = "Europe"
                              Object Level Security on 'Invoices'[Value]: None
                              Members: CONTOSO\alice
```

`CONTOSO\alice` is removed from `Europe` and `No Sales Value`.

## Related Rules

- [Row-Level and Object-Level Security Require Read Permission](xref:kb.bpa-role-security-not-enforced)
- [Power BI Roles Must Have Read Permission](xref:kb.bpa-powerbi-role-read-permission)
- [Roles Without Security Override Secured Roles](xref:kb.bpa-role-unrestricted-read)

## Compatibility Level

This rule applies to models with compatibility level **1400** and higher.
