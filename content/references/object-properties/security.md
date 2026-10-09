---
uid: object-properties-security
title: Role and security properties
author: Jeroen ter Heerdt
updated: 2026-10-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Role and security properties

<!--
SUMMARY: Reference for the properties of roles, table permissions and role members, which define row-level and object-level security.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

This page covers the properties of roles, table permissions and role members. A table permission holds a role's security settings for one table. For properties that most objects share, see @object-properties-common.

Security in a semantic model is defined by roles. A role grants its members a level of access to the model and restricts what they see with:

- **row-level security (RLS)**, which filters the rows of a table with a DAX expression per table, for example to show a sales manager only the sales of their own region
- **object-level security (OLS)**, which hides whole tables or columns, including their metadata, for example a salary column that only HR can see. OLS needs compatibility level 1400 or higher.

The Tabular Object Model (TOM) stores both per table, in a *table permission* of the role. You can also edit them from the table side: on a table, `RowLevelSecurity` and `ObjectLevelSecurity` show the settings for every role (see @object-properties-tables), and on a column, `ObjectLevelSecurity` does the same (see @object-properties-columns). Whichever way you edit them, Tabular Editor creates the table permissions when they're needed.

See @data-security-about, @data-security-setup-rls, @data-security-setup-ols, @data-security-testing and @roles-and-rls.

## Role

A role is a named set of permissions, together with the users and groups who get them. A user who is a member of several roles gets the union of what the roles allow: if one role filters a table and another doesn't, the user sees all rows. Adding a user to an extra role can only widen what they see.

Members of the model's administrator roles and users with write access to the workspace in Power BI aren't restricted by RLS or OLS. In Power BI, RLS and OLS apply only to users with the workspace **Viewer** role, and not to the **Admin**, **Member** and **Contributor** roles, which have edit permission on the semantic model (see Microsoft's [Row-level security (RLS) with Power BI](https://learn.microsoft.com/fabric/security/service-admin-row-level-security)). Test security with a user who only has read access, or with the role impersonation features in @data-security-testing.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Table Permissions
`MetadataPermission` · per table · Security · read-only · compatibility level 1400+ · *shortcut to* the role's table permissions

The object-level security (OLS) permission of each table in this role. Expand the property to see one entry per table, and pick a value for each:

| Value | Meaning |
|---|---|
| `Default` | No permission is set. Members of the role can see the table if `ModelPermission` allows reading. |
| `Read` | Members of the role can see and query the table. |
| `None` | The table is hidden from members of the role, together with its columns, measures and relationships. Queries and measures that refer to it return an error for them. |

Calculation group tables aren't listed. Tabular Editor shows this property at compatibility level 1400 and higher. The collapsed value summarizes the settings, for example "OLS enabled on 2 out of 15 tables".

To secure individual columns, use [OLS Column Permissions](#ols-column-permissions) on the table permission or `ObjectLevelSecurity` on the column.

> [!NOTE]
> The role also has a collection of table permission objects with the same display name. See [Table Permissions](#table-permissions-1) below.

### Row Level Security
`RowLevelSecurity` · per table · Security · read-only · *shortcut to* the role's table permissions

The row-level security (RLS) filter of each table in this role. Expand the property to see one entry per table. Each entry is a DAX expression that returns `TRUE` for the rows that members of the role can see, and an empty entry leaves that table unfiltered. Calculation group tables aren't listed. The collapsed value summarizes the settings, for example "RLS enabled on 1 out of 15 tables".

A static filter hard-codes the allowed values:

```dax
'Region'[Country] = "Denmark"
```

A dynamic filter looks up the current user, so one role serves all users:

```dax
'Salesperson'[Email] = USERPRINCIPALNAME ()
```

Filters flow along relationships from the one side to the many side, so filtering a dimension such as `Region` also filters the fact tables related to it. To make a filter flow in both directions of a relationship, set `SecurityFilteringBehavior` on the relationship (see @object-properties-relationships). The expression is evaluated for every row of the table it's on, so filter the smallest table you can, usually a dimension.

Setting a filter creates a table permission for the table if there isn't one. Clearing it removes the table permission again, unless the table permission also holds OLS settings. The filter itself is stored in `FilterExpression` of the table permission.

In Tabular Editor 3, check a filter by impersonating a user or role in a @table-preview or a @pivot-grid.

### Members
`Members` · collection of role members · Translations, Perspectives, Security · read-only

The users and groups who are members of the role. Click the ellipsis button to add, remove and edit members in the collection editor, or right-click the role and choose **Edit members...** (see @data-security-setup-rls). The collection holds two kinds of members:

- **Windows AD members** for SQL Server Analysis Services with on-premises Active Directory (see [Windows role member](#windows-role-member))
- **Azure AD members** (external members) for Azure Analysis Services and Power BI, identified through Microsoft Entra ID (see [External role member](#external-role-member))

In Power BI and Fabric, role membership is often managed in the semantic model's security settings in the service. In Analysis Services, many teams manage members directly on the server. Tabular Editor deploys role members only if you select **Deploy Model Role Members**. If you clear the option, the roles in the target database keep their members, and a new database gets roles without members (see @deployment).

In Power BI, you can't add service principals as role members.

Members that someone adds on the semantic model's **Security** page in the Power BI service are ordinary role members in the model. Through the XMLA endpoint, they're identical to members added in Tabular Editor: external members with `IdentityProvider` `AzureAD` and the user's object ID as `MemberID`. When you deploy with **Deploy Model Role Members**, the members in your model replace them. To keep the members added in the service, deploy without that option.

### Model Permission
`ModelPermission` · ModelPermission · Translations, Perspectives, Security

The level of access the role gives its members to the whole model.

| Value | Meaning |
|---|---|
| `None` | No access. Members can't connect to the model, whatever the other settings in the role allow. |
| `Read` | Members can read the model's metadata and query its data, subject to the role's RLS and OLS. This is the value for almost every role for report users. |
| `ReadRefresh` | Like `Read`, and members can also refresh the model. |
| `Refresh` | Members can refresh the model and can't query it, for example accounts that only run refreshes. |
| `Administrator` | Members have full control over the model, including changing it, and RLS and OLS don't apply to them. Analysis Services only. |

A new role has no access until you set this property. If you add a row-level filter to a role whose `ModelPermission` is `None` and that has no table permissions yet, Tabular Editor sets it to `Read`.

Power BI and Fabric only support `Read` for roles in the model: Microsoft documents it as the only role permission you can set through the XMLA endpoint. Refresh, build and other permissions are managed with workspace roles and semantic model permissions in the service, and model roles in Power BI are only used for RLS and OLS. In the Power BI service, deploying a role with any other value fails with the error "Please set the permission level for your row-level security (RLS) roles to 'Read'".

### Table Permissions
`TablePermissions` · collection of table permissions · Translations, Perspectives, Security · read-only

The table permission objects of the role, one per table that has an RLS filter or OLS setting in this role (see [Table permission](#table-permission)).

The **Properties** view doesn't show this collection. Edit the same settings through [Row Level Security](#row-level-security) and [Table Permissions](#table-permissions) (OLS) above, and Tabular Editor adds and removes the table permissions. In a C# script, use the collection to loop over the secured tables of a role:

```csharp
foreach (var tp in Selected.Role.TablePermissions)
    Output(tp.Table.Name + ": " + tp.FilterExpression);
```

In Tabular Editor 3, the **TOM Explorer** shows the table permissions of a role under the role. A table permission whose settings are all back at their defaults has no effect and is shown dimmed.

## Table permission

A table permission holds the security settings of one role for one table: the RLS filter and the OLS permissions of the table and its columns. The table permission is named after its table, and you can't rename it.

Tabular Editor creates a table permission when you set an RLS filter or an OLS permission for a table in a role. When you clear the RLS filter and the table permission holds no OLS settings, Tabular Editor removes it. Setting an OLS permission back to `Default` keeps the table permission in place, without effect, until you delete it. In Tabular Editor 3, you can also add one yourself: right-click the role and choose **Add table permission...**. @data-security-setup-rls describes this, and how to test a filter expression in a DAX query before you use it.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Error Message](xref:object-properties-common#error-message)
- [State](xref:object-properties-common#state)

The **Properties** view doesn't show `Name` or `ObjectType` for table permissions. `RoleName` and `TableName` in the **Metadata** category identify the table permission.

### Role
`RoleName` · string · Metadata · read-only · *shortcut to* the name of the role

The name of the role this table permission belongs to.

### Table
`TableName` · string · Metadata · read-only · *shortcut to* the name of the table

The name of the table this table permission secures.

### Role
`Role` · ModelRole · Options · read-only

The role this table permission belongs to, for C# scripts that go from a table permission back to its role. The **Properties** view doesn't show it and shows `RoleName` in the **Metadata** category.

### OLS Column Permissions
`ColumnPermissions` · per column · Security · read-only · compatibility level 1400+

The object-level security (OLS) permission of each column of the table in this role. Expand the property to see one entry per column. The values are the same as for a table:

| Value | Meaning |
|---|---|
| `Default` | No permission is set. The column follows the table's permission. |
| `Read` | Members of the role can see and query the column. |
| `None` | The column is hidden from members of the role. Queries and measures that refer to it return an error for them. |

Use column-level OLS to hide sensitive columns, such as salaries or personal data, while the rest of the table stays available. Measures that refer to a secured column fail for members of the role. To see which objects refer to a column, right-click it in the **TOM Explorer** and choose **Show dependencies...** (see @formula-fix-up-dependencies).

This is the same setting as `ObjectLevelSecurity` on the column (see @object-properties-columns).

### Filter Expression
`FilterExpression` · string · Translations, Perspectives, Security

The row-level security filter for the table in this role: a DAX expression that returns `TRUE` for the rows that members of the role can see. An empty filter leaves the table unfiltered for this role. Edit it in the **Expression Editor**, or through `RowLevelSecurity` on the role or on the table. For examples, see [Row Level Security](#row-level-security).

The expression is evaluated in the context of each row of the table, so you refer to its columns directly, for example `'Region'[Country] = "Denmark"`. To use values from other tables, use `RELATED` or `LOOKUPVALUE`. To look up the current user, use `USERPRINCIPALNAME ()` or `USERNAME ()`.

### OLS Table Permission
`MetadataPermission` · MetadataPermission · Translations, Perspectives, Security · compatibility level 1400+

The object-level security (OLS) permission of the table in this role.

| Value | Meaning |
|---|---|
| `Default` | No permission is set. Members of the role can see the table. |
| `Read` | Members of the role can see and query the table. |
| `None` | The table is hidden from members of the role, together with its columns, measures and relationships. |

This is the same setting as [Table Permissions](#table-permissions) on the role and `ObjectLevelSecurity` on the table.

You can't combine RLS and OLS from different roles. A user who is a member of such a combination of roles gets an error at query time, in SQL Server Analysis Services, Azure Analysis Services and Power BI alike. See @data-security-about, [Combine OLS with RLS](xref:data-security-setup-ols#5-combine-ols-with-rls) and Microsoft's [object-level security restrictions](https://learn.microsoft.com/analysis-services/tabular-models/object-level-security#restrictions).

You also can't hide a table with OLS if that breaks a chain of relationships between other tables. The engine rejects it with an error.

## Windows role member

A Windows role member is a Windows user or group from Active Directory, for example `CONTOSO\SalesManagers`. SQL Server Analysis Services uses Windows members, and Azure Analysis Services and Power BI use [external role members](#external-role-member). The Power BI service rejects a Windows member at deployment with the error "Only Microsoft Entra users or groups are supported. Use 'AzureAD' as the value of the identity provider".

Add groups where you can: adding and removing people from a group doesn't require changing or redeploying the model.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

The **Properties** view doesn't show `Name` for role members. `MemberName` identifies the member.

### Member ID
`MemberID` · string · Options

The security identifier (SID) of the user or group, for example `S-1-5-21-...`. You can leave it empty and only fill in `MemberName`. In Tabular Editor 3, when you pick the member with the Windows object picker (the ellipsis button on `MemberName`), Tabular Editor fills in both the name and the SID.

When you deploy to SQL Server Analysis Services, Tabular Editor deploys `MemberID` as it is. It only removes member IDs when the target is Azure Analysis Services or Power BI (see `MemberID` under [External role member](#external-role-member)).

When you deploy a Windows member with only `MemberName` set, SQL Server Analysis Services looks up the account and stores its SID in `MemberID`. It rejects an account that doesn't exist with an error like "The 'Sales' role includes domain account that does not exist". This was observed on SQL Server 2025 Analysis Services.

### Member Name
`MemberName` · string · Options

The name of the Windows user or group in `DOMAIN\name` format, for example `CONTOSO\SalesManagers`. If the account doesn't exist in a domain the server trusts, deployment fails.

### Role
`Role` · ModelRole · Options · read-only

The role this member belongs to, for C# scripts that go from a member back to its role. The **Properties** view doesn't show it.

## External role member

An external role member is a user or group identified by an external identity provider, which in practice is Microsoft Entra ID (formerly Azure Active Directory). Azure Analysis Services and Power BI use external members. In Tabular Editor, add them as **Azure AD Member** in the role's `Members` collection (see @data-security-setup-rls).

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

The **Properties** view doesn't show `Name` for role members. `MemberName` identifies the member.

### Identity Provider
`IdentityProvider` · string · Options

The identity provider that authenticates the member. Tabular Editor sets it to `AzureAD` when you add an external member. That's the only value Azure Analysis Services and Power BI use.

### Member ID
`MemberID` · string · Options

The object ID of the user or group in Microsoft Entra ID. SQL Server Analysis Services requires it: SQL Server 2025 Analysis Services rejects an external member without a member ID with the error "MemberID must be specified when creating an External RoleMembership object". For Azure Analysis Services and Power BI, leave it empty. Microsoft's examples add external members with only `MemberName` and `IdentityProvider`.

Member IDs must not be set when you deploy to Azure Analysis Services or Power BI. When the deployment target is Azure Analysis Services or the Power BI service, Tabular Editor removes the member IDs of all role members, including the members it keeps from the target database. Deployments to SQL Server Analysis Services keep them. You can't turn this behavior on or off.

### Member Name
`MemberName` · string · Options

The name that identifies the user or group. For a user, it's the user principal name, usually the email address, for example `anna@contoso.com`. The accepted formats for groups and other members depend on the target.

In Azure Analysis Services:

- add a security group as `obj:<group object ID>@<tenant ID>` or by its email address, and a Microsoft 365 group by its email address
- add a service principal as `app:<application ID>@<tenant ID>`
- every name is checked in Microsoft Entra ID at deployment, and a display name of a user or group, or a user who doesn't exist, fails with the error "was not found in your organization's Microsoft Entra ID"
- the name is stored as you typed it, so an `obj:` name stays an `obj:` name, and `MemberID` stays empty

In the Power BI service:

- a user's user principal name works, and so does `obj:<object ID>@<tenant ID>`, which the service rewrites to the user principal name
- add a security group as `obj:<group object ID>@<tenant ID>`, which the service keeps as typed, or a mail-enabled security group by its email address
- a display name of a user or group, the address of a user who doesn't exist or a Microsoft 365 group fails with the error "There are invalid rolememberships in roles"
- the service fills in `MemberID` with the user's object ID

In the Power BI service's security settings, you add users and groups by email address or name. Those settings support distribution groups, mail-enabled groups and Microsoft Entra security groups, and don't support Microsoft 365 groups.

### Member Type
`MemberType` · RoleMemberType · Options

Whether the member is a single user or a group.

| Value | Meaning |
|---|---|
| `Auto` | The server works out whether the member is a user or a group. |
| `User` | The member is an individual user. |
| `Group` | The member is a security group, and all its members get the role. |

Windows role members don't have this property: the server works out from the account whether it's a user or a group.

Azure Analysis Services and the Power BI service ignore the value you set:

- Azure Analysis Services stores every external member as `Auto`, whether you set `Auto`, `User` or `Group`, for users and groups alike.
- the Power BI service works out the type itself and stores a user as `User` and a group as `Group`, whether you set `Auto`, `User` or `Group`. It also fills in `MemberID` for both. In Power BI, leave this property at `Auto`.

### Role
`Role` · ModelRole · Options · read-only

The role this member belongs to, for C# scripts that go from a member back to its role. The **Properties** view doesn't show it.
