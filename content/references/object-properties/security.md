---
uid: object-properties-security
title: Role and security properties
author: Jeroen ter Heerdt
updated: 2026-09-23
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

This page covers the properties of roles, of the table permissions that hold a role's security settings per table, and of role members. For properties that most objects share, see @object-properties-common.

Security in a semantic model is defined by roles. A role grants its members a level of access to the model, and can restrict what they see in two ways:

- **Row-level security (RLS)** filters the rows of a table. For example, a sales manager only sees the sales of their own region. The filter is a DAX expression per table.
- **Object-level security (OLS)** hides whole tables or columns, including their metadata. For example, only HR can see the salary column. OLS needs compatibility level 1400 or higher.

TOM stores both per table, in a *table permission* of the role. Tabular Editor also lets you edit them from the other side: on a table, **Row Level Security** and **Object Level Security** show the settings for every role (see @object-properties-tables), and on a column, **Object Level Security** does the same (see @object-properties-columns). Whichever way you edit them, Tabular Editor creates the table permissions for you when they're needed.

See @data-security-about, @data-security-setup-rls, @data-security-setup-ols, @data-security-testing and @roles-and-rls.

## Role

A role is a named set of permissions, together with the users and groups who get them. A user who is a member of several roles gets the union of what the roles allow: if one role filters a table and another doesn't, the user sees all rows. Keep that in mind when you design roles, because adding a user to an extra role can only widen what they see.

Members of the model's administrator roles, and users with write access to the workspace in Power BI, aren't restricted by RLS or OLS at all. In Power BI, RLS and OLS only apply to users with the workspace **Viewer** role. They don't apply to the **Admin**, **Member** and **Contributor** roles, which have edit permission on the semantic model. See Microsoft's [Row-level security (RLS) with Power BI](https://learn.microsoft.com/fabric/security/service-admin-row-level-security). Test security with a user who only has read access, or use the role impersonation features described in @data-security-testing.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Security

#### Table Permissions
`MetadataPermission` · per table · read-only · *shortcut to* the role's table permissions

The object-level security (OLS) permission of each table in this role. Expand the property to see one entry per table, and pick a value for each:

| Value | Meaning |
|---|---|
| `Default` | No permission is set. Members of the role can see the table, as long as **Model Permission** allows reading. |
| `Read` | Members of the role can see and query the table. |
| `None` | The table is hidden from members of the role, together with its columns, measures and relationships. Queries and measures that refer to it return an error for them. |

Calculation group tables aren't listed. Tabular Editor shows this property at compatibility level 1400 and higher. The collapsed value summarizes the settings, for example *OLS enabled on 2 out of 15 tables*.

To secure individual columns rather than a whole table, use **OLS Column Permissions** on the table permission, or **Object Level Security** on the column.

Don't confuse this property with the collection of table permission objects, also named **Table Permissions**, described below.

#### Row Level Security
`RowLevelSecurity` · per table · read-only · *shortcut to* the role's table permissions

The row-level security (RLS) filter of each table in this role. Expand the property to see one entry per table. Each entry is a DAX expression that returns `TRUE` for the rows that members of the role may see. Leave an entry empty to not filter that table. Calculation group tables aren't listed. The collapsed value summarizes the settings, for example *RLS enabled on 1 out of 15 tables*.

A static filter hard-codes the allowed values:

```dax
'Region'[Country] = "Denmark"
```

A dynamic filter looks up the current user, so one role serves everyone:

```dax
'Salesperson'[Email] = USERPRINCIPALNAME ()
```

Filters flow along relationships, from the one side to the many side. Filtering a dimension such as `Region` therefore also filters the fact tables related to it. To make a filter flow in both directions of a relationship, set **Security Filtering Behavior** on the relationship (see @object-properties-relationships). Filter the smallest table you can, usually a dimension, rather than a large fact table: the expression is evaluated for every row of the table it's on.

Setting a filter creates a table permission for the table if there isn't one. Clearing it removes the table permission again, unless it also holds OLS settings. The filter itself is stored in **Filter Expression** of the table permission.

In Tabular Editor 3, you can check a filter by impersonating a user or role in a @table-preview or a @pivot-grid.

### Translations, Perspectives, Security

#### Members
`Members` · collection of role members · read-only

The users and groups who are members of the role. Click the ellipsis button to open the collection editor, where you can add, remove and edit members. There are two kinds of members:

- **Windows AD members** for SQL Server Analysis Services with on-premises Active Directory. See [Windows role member](#windows-role-member).
- **Azure AD members** (external members) for Azure Analysis Services and Power BI, identified through Microsoft Entra ID. See [External role member](#external-role-member).

In Power BI and Fabric, role membership is often managed in the service, in the semantic model's security settings, rather than in the model. Many teams also manage members directly on the server in Analysis Services. When you deploy, Tabular Editor only deploys role members if you select **Deploy Model Role Members**. If you clear the option, Tabular Editor keeps the members that the roles already have in the target database, and a new database gets roles without members. See @deployment.

You can also add and remove members by right-clicking the role and choosing **Edit members...**. See @data-security-setup-rls.

In Power BI, you can't add service principals as role members.

Members that someone adds on the semantic model's **Security** page in the Power BI service are ordinary role members in the model. Through the XMLA endpoint they look exactly like members added in Tabular Editor: external members with **Identity Provider** `AzureAD` and the user's object ID as **Member ID**. So when you deploy with **Deploy Model Role Members**, the members in your model replace them. Deploy without that option to keep the members that were added in the service.

#### Model Permission
`ModelPermission` · ModelPermission

The level of access the role gives its members to the whole model.

| Value | Meaning |
|---|---|
| `None` | No access. Members can't connect to the model, even if other settings in the role would allow it. |
| `Read` | Members can read the model's metadata and query its data, subject to the role's RLS and OLS. This is the value for almost every role you create for report users. |
| `ReadRefresh` | Like `Read`, and members can also refresh the model. |
| `Refresh` | Members can refresh the model, but can't query it. Use it for accounts that only run refreshes. |
| `Administrator` | Members have full control over the model, including changing it. RLS and OLS don't apply to them. Analysis Services only. |

A new role has no access until you set this property. Set it to `Read` for a role that report users should use. If you add a row-level filter to a role whose **Model Permission** is `None` and that has no table permissions yet, Tabular Editor sets it to `Read` for you.

Power BI and Fabric only support `Read` for roles in the model: Microsoft documents it as the only role permission you can set through the XMLA endpoint. Other permissions, such as refresh and build, are managed with workspace roles and semantic model permissions in the service. Model roles in Power BI are only used for RLS and OLS.

In the Power BI service, deploying a role with any other value fails with the error *Please set the permission level for your row-level security (RLS) roles to 'Read'*.

#### Table Permissions
`TablePermissions` · collection of table permissions · read-only

The table permission objects of the role: one per table that has an RLS filter or OLS setting in this role. See [Table permission](#table-permission) below.

Tabular Editor doesn't show this collection in the Properties view, because you edit the same settings through **Row Level Security** and **Table Permissions** (OLS) above, and Tabular Editor adds and removes table permissions for you. In a C# script, use it to loop over the secured tables of a role:

```csharp
foreach (var tp in Selected.Role.TablePermissions)
    Output(tp.Table.Name + ": " + tp.FilterExpression);
```

In Tabular Editor 3, the table permissions of a role are also shown under the role in the TOM Explorer. A table permission whose settings are all back to their defaults, so it has no effect, is shown dimmed.

## Table permission

A table permission holds the security settings of one role for one table: the RLS filter and the OLS permissions of the table and its columns. The table permission is named after its table, and you can't rename it.

You rarely need to work with table permissions directly. Tabular Editor creates one when you set an RLS filter or an OLS permission for a table in a role. When you clear the RLS filter and the table permission holds no OLS settings, Tabular Editor removes it. Setting an OLS permission back to `Default` doesn't remove the table permission; it stays in place without effect until you delete it. In Tabular Editor 3, you can also add one yourself: right-click the role and choose **Add table permission...**. @data-security-setup-rls describes this, and how to test a filter expression in a DAX query before you use it.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Error Message](xref:object-properties-common#error-message)
- [State](xref:object-properties-common#state)

Tabular Editor doesn't show **Name** or **Object Type** for table permissions. Use **Role** and **Table** under **Metadata** instead.

### Metadata

#### Role
`RoleName` · string · read-only · *shortcut to* the name of the role

The name of the role this table permission belongs to.

#### Table
`TableName` · string · read-only · *shortcut to* the name of the table

The name of the table this table permission secures.

### Options

#### Role
`Role` · ModelRole · read-only

The role this table permission belongs to. Tabular Editor doesn't show it in the Properties view; use **Role** under **Metadata** there. It's useful in C# scripts to get from a table permission back to its role.

### Security

#### OLS Column Permissions
`ColumnPermissions` · per column · read-only

The object-level security (OLS) permission of each column of the table in this role. Expand the property to see one entry per column. The values are the same as for a table:

| Value | Meaning |
|---|---|
| `Default` | No permission is set. The column follows the table's permission. |
| `Read` | Members of the role can see and query the column. |
| `None` | The column is hidden from members of the role. Queries and measures that refer to it return an error for them. |

Use column-level OLS to hide sensitive columns, such as salaries or personal data, while the rest of the table stays available. Measures that refer to a secured column fail for members of the role, so check which measures depend on it, or give them a version that doesn't. To see which objects refer to a column, right-click it in the TOM Explorer and choose **Show dependencies...**. See @formula-fix-up-dependencies.

This is the same setting as **Object Level Security** on the column. See @object-properties-columns. Compatibility level 1400 or higher.

#### Filter Expression
`FilterExpression` · string

The row-level security filter for the table in this role: a DAX expression that returns `TRUE` for the rows that members of the role may see. Edit it in the Expression Editor, or through **Row Level Security** on the role or on the table. See **Row Level Security** under [Role](#role) above for examples.

The expression is evaluated in the context of each row of the table, so you can refer to its columns directly, for example `'Region'[Country] = "Denmark"`. Use `RELATED` or `LOOKUPVALUE` to use values from other tables, and `USERPRINCIPALNAME ()` or `USERNAME ()` to look up the current user.

An empty filter means the table isn't filtered for this role.

#### OLS Table Permission
`MetadataPermission` · MetadataPermission · compatibility level 1400+

The object-level security (OLS) permission of the table in this role.

| Value | Meaning |
|---|---|
| `Default` | No permission is set. Members of the role can see the table. |
| `Read` | Members of the role can see and query the table. |
| `None` | The table is hidden from members of the role, together with its columns, measures and relationships. |

This is the same setting as **Table Permissions** on the role and **Object Level Security** on the table.

You can't combine RLS and OLS from different roles, because the combination could give unintended access to secured data. A user who is a member of such a combination of roles gets an error at query time. This applies to SQL Server Analysis Services, Azure Analysis Services and Power BI alike. See @data-security-about, [Combine OLS with RLS](xref:data-security-setup-ols#5-combine-ols-with-rls) and Microsoft's [object-level security restrictions](https://learn.microsoft.com/analysis-services/tabular-models/object-level-security#restrictions).

You also can't hide a table with OLS if that breaks a chain of relationships between other tables. The engine reports an error if you try.

## Windows role member

A Windows role member is a Windows user or group from Active Directory, for example `CONTOSO\SalesManagers`. SQL Server Analysis Services uses Windows members. Azure Analysis Services and Power BI use [external role members](#external-role-member) instead. The Power BI service rejects a Windows member when you deploy, with the error *Only Microsoft Entra users or groups are supported. Use 'AzureAD' as the value of the identity provider*.

Prefer groups over individual users. Adding and removing people from a group doesn't require changing or redeploying the model.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

Tabular Editor doesn't show **Name** for role members. **Member Name** identifies the member instead.

### Options

#### Member ID
`MemberID` · string

The security identifier (SID) of the user or group, for example `S-1-5-21-...`. You can leave it empty and only fill in **Member Name**. In Tabular Editor 3, when you pick the member with the Windows object picker (the ellipsis button on **Member Name**), Tabular Editor fills in both the name and the SID for you.

When you deploy to SQL Server Analysis Services, Tabular Editor deploys the Member ID as it is. It only removes member IDs when the target is Azure Analysis Services or Power BI (see **Member ID** under [External role member](#external-role-member)).

When you deploy a Windows member with only **Member Name** set, SQL Server Analysis Services looks up the account and stores its SID in **Member ID** itself. It rejects an account that doesn't exist, with an error like *The 'Sales' role includes domain account that does not exist*. This was observed on SQL Server 2025 Analysis Services.

#### Member Name
`MemberName` · string

The name of the Windows user or group, in `DOMAIN\name` format, for example `CONTOSO\SalesManagers`. The account must exist in a domain the server trusts, or deployment fails.

#### Role
`Role` · ModelRole · read-only

The role this member belongs to. Tabular Editor doesn't show it in the Properties view. It's useful in C# scripts to get from a member back to its role.

## External role member

An external role member is a user or group that's identified by an external identity provider, which is Microsoft Entra ID (formerly Azure Active Directory) in practice. Azure Analysis Services and Power BI use external members. In Tabular Editor, you add them as **Azure AD Member** in the role's **Members** collection. See @data-security-setup-rls.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

Tabular Editor doesn't show **Name** for role members. **Member Name** identifies the member instead.

### Options

#### Identity Provider
`IdentityProvider` · string

The identity provider that authenticates the member. Tabular Editor sets it to `AzureAD` when you add an external member, which is the only value Azure Analysis Services and Power BI use. You don't need to change it.

#### Member ID
`MemberID` · string

The object ID of the user or group in Microsoft Entra ID. For Azure Analysis Services and Power BI you can leave it empty: Microsoft's examples add external members with only **Member Name** and **Identity Provider**. SQL Server Analysis Services requires it. SQL Server 2025 Analysis Services rejects an external member without a Member ID with the error *MemberID must be specified when creating an External RoleMembership object*.

Member IDs must not be set when you deploy to Azure Analysis Services or Power BI. For that reason, Tabular Editor removes the member IDs of all role members when the deployment target is Azure Analysis Services or the Power BI service, including members it keeps from the target database. Deployments to SQL Server Analysis Services keep them. You can't turn this behavior on or off yourself.

#### Member Name
`MemberName` · string

The name that identifies the user or group. For a user, this is their user principal name, usually their email address, for example `anna@contoso.com`. In Azure Analysis Services, add a security group as `obj:<group object ID>@<tenant ID>`, or by its email address, and a service principal as `app:<application ID>@<tenant ID>`. Azure Analysis Services checks every name in Microsoft Entra ID when you deploy: a display name, or a user who doesn't exist, fails with the error *was not found in your organization's Microsoft Entra ID*. Unlike Power BI, it keeps the name as you typed it, so an `obj:` name stays an `obj:` name, and it leaves **Member ID** empty. Groups work by `obj:<group object ID>@<tenant ID>` or by email address, and Azure Analysis Services also accepts a Microsoft 365 group by its email address. A group's display name is rejected, like a user's. In the Power BI service's security settings, you add users and groups by email address or name. Power BI supports distribution groups, mail-enabled groups and Microsoft Entra security groups, but not Microsoft 365 groups.

In the Power BI service, a user's user principal name works, and so does `obj:<object ID>@<tenant ID>`, which the service then rewrites to the user principal name. A display name, or the address of a user who doesn't exist, fails with the error *There are invalid rolememberships in roles*. The service fills in **Member ID** with the user's object ID itself.

For groups, the Power BI service accepts a security group as `obj:<group object ID>@<tenant ID>`, which it keeps as typed, and a mail-enabled security group by its email address. It rejects a Microsoft 365 group and a group's display name, with the same *invalid rolememberships* error.

#### Member Type
`MemberType` · RoleMemberType

Whether the member is a single user or a group.

| Value | Meaning |
|---|---|
| `Auto` | The server works out whether the member is a user or a group. |
| `User` | The member is an individual user. |
| `Group` | The member is a security group, and all its members get the role. |

Set it explicitly when the server can't tell, for example for a group with an email address that looks like a user's.

Windows role members don't have this property. For them, the server works out from the account whether it's a user or a group.

In the Power BI service, the service works out the type itself: for a user account, `Auto` and even `Group` are stored as `User`.

Azure Analysis Services ignores this property: it stores every external member as `Auto`, whether you set `Auto`, `User` or `Group`, for users and groups alike.

The Power BI service always works out the type itself and ignores what you set: a user is stored as `User` and a group as `Group`, whether you set `Auto`, `User` or `Group`. It also fills in **Member ID** for both. So in Power BI, you can leave this property at `Auto`.

#### Role
`Role` · ModelRole · read-only

The role this member belongs to. Tabular Editor doesn't show it in the Properties view. It's useful in C# scripts to get from a member back to its role.
