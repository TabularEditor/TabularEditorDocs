---
uid: object-properties-security
title: 角色与安全属性
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

# 角色与安全属性

<!--
SUMMARY: Reference for the properties of roles, table permissions and role members, which define row-level and object-level security.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍角色、表格权限和角色成员的属性。表格权限包含角色针对单个表的安全设置。有关大多数对象共有的属性，请参见 @object-properties-common。

语义模型中的安全性由角色定义。角色会授予成员一定级别的模型访问权限，并通过以下方式限制他们能看到的内容：

- **行级安全性 (RLS)**，它会按表使用 DAX 表达式筛选表中的行，例如让销售经理只能看到自己所在区域的销售数据
- **对象级安全性 (OLS)**，它会隐藏整个表或列，包括其元数据，例如只有 HR 才能看到的薪资列。 OLS 需要 1400 或更高的兼容级别。

在 Tabular Object Model (TOM) 中，这两种设置都会按表存储在角色的 _表格权限_ 中。你也可以从表端进行编辑：在表对象上，`RowLevelSecurity` 和 `ObjectLevelSecurity` 会显示所有角色的设置（参见 @object-properties-tables）；在列对象上，`ObjectLevelSecurity` 也同样如此（参见 @object-properties-columns）。无论你通过哪种方式编辑，Tabular Editor 都会在需要时创建表格权限。

参见 @data-security-about、@data-security-setup-rls、@data-security-setup-ols、@data-security-testing 和 @roles-and-rls。

## 角色

角色是一个命名的权限集合，并包含被授予这些权限的用户和组。属于多个角色的用户会获得各角色允许内容的并集：如果一个角色对某个表进行了筛选，而另一个没有，则该用户会看到所有行。把用户添加到其他角色只会扩大他们能看到的范围。

模型的管理员角色成员，以及在 Power BI 中对 Workspace 具有写入权限的用户，不受 RLS 或 OLS 的限制。在 Power BI 中，RLS 和 OLS 仅适用于在 Workspace 中具有 **Viewer** 角色的用户，而不适用于具有 **Admin**、**Member** 和 **Contributor** 角色的用户，因为这些角色对语义模型拥有编辑权限 (参见 Microsoft 的 [使用 Power BI 的行级安全性 (RLS)](https://learn.microsoft.com/fabric/security/service-admin-row-level-security))。请使用仅具读取权限的用户进行安全性测试，或使用 @data-security-testing 中的角色模拟功能。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

### 表格权限

`MetadataPermission` · 每个表 · 安全性 · 只读 · 兼容级别 1400+ · _作为该角色表格权限的快捷方式_

此角色中每个表的对象级安全性 (OLS) 权限。展开该属性，即可看到每个表对应的一项，并为每项选择一个值：

| 值    | 含义                                           |
| ---- | -------------------------------------------- |
| `默认` | 未设置权限。如果 `ModelPermission` 允许读取，角色成员就可以看到该表。 |
| `读取` | 角色成员可以看到并查询该表。                               |
| `无`  | 该表及其列、度量值和关系都会对角色成员隐藏。任何引用该表的查询和度量值都会返回错误。   |

不会列出计算组表。 Tabular Editor 会在兼容级别 1400 及更高级别时显示此属性。折叠后的值会汇总这些设置，例如“15 个表中有 2 个已启用 OLS”。

要保护单个列，可在表格权限中使用 [OLS 列权限](#ols-column-permissions)，或在列上使用 `ObjectLevelSecurity`。

> [!NOTE]
> 该角色还包含一个显示名称相同的表格权限对象集合。请参阅下方的[表格权限](#table-permissions-1)。

### 行级安全性

`RowLevelSecurity` · 每张表 · 安全性 · 只读 · _角色的表格权限的快捷入口_

此角色中每个表的行级安全性（RLS）筛选器。展开此属性可查看每个表对应的一个条目。每个条目都是一个 DAX 表达式：对于角色成员可以看到的行，它返回 `TRUE`；如果条目为空，则该表不应用筛选。此处不会列出计算组表。折叠后的值会汇总这些设置，例如“15 个表中有 1 个启用了 RLS”。

静态筛选器将允许的值硬编码为：

```dax
'Region'[Country] = "Denmark"
```

动态筛选器会查找当前用户，因此一个角色就能适用于所有用户：

```dax
'Salesperson'[Email] = USERPRINCIPALNAME ()
```

筛选器会沿着关系从“一”端传播到“多”端，因此对 `Region` 这样的维度进行筛选时，也会筛选与其相关的事实表。若要让筛选器沿关系的两个方向传播，请在该关系上设置 `SecurityFilteringBehavior`（参见 @object-properties-relationships）。表达式会针对其所在表的每一行进行计算，因此应尽量筛选最小的表，通常是维度表。

设置筛选器时，如果该表还没有表格权限，则会为其创建一个。清除后会移除该表格权限，除非该表格权限还包含 OLS 设置。筛选器本身存储在表格权限的 `FilterExpression` 中。

在 Tabular Editor 3 中，可在 @table-preview 或 @pivot-grid 中模拟某个用户或角色，以检查筛选器效果。

### 成员

`Members` · 角色成员集合 · 翻译、透视、安全性 · 只读

属于该角色的用户和组。单击省略号按钮，在集合编辑器中添加、删除和编辑成员；或者右键单击该角色并选择 **编辑成员...**（参见 @data-security-setup-rls）。该集合包含两类成员：

- **Windows AD 成员**：适用于使用本地 Active Directory 的 SQL Server Analysis Services（参见 [Windows 角色成员](#windows-role-member)）
- **Azure AD 成员**（外部成员）：适用于 Azure Analysis Services 和 Power BI，通过 Microsoft Entra ID 标识（参见 [外部角色成员](#external-role-member)）

在 Power BI 和 Fabric 中，角色成员资格通常通过服务端的语义模型安全设置进行管理。在 Analysis Services 中，许多团队直接在服务器上管理成员。 Tabular Editor 仅在你选中 **部署模型角色成员** 时才会部署角色成员。如果清除此选项，目标数据库中的角色会保留其成员，而新数据库中的角色将不包含成员（见 @deployment）。

在 Power BI 中，不能将服务主体添加为角色成员。

在 Power BI 服务中，通过语义模型的 **安全性** 页面添加的成员，在模型中会被视为普通角色成员。通过 XMLA endpoint，它们与在 Tabular Editor 中添加的成员完全相同：都是外部成员，`IdentityProvider` 为 `AzureAD`，并以用户的对象 ID 作为 `MemberID`。使用 **部署模型角色成员** 进行部署时，模型中的成员会替换它们。想保留在服务中添加的成员，就在不选中该选项的情况下部署。

### 模型权限

`ModelPermission` · ModelPermission · 翻译、透视图和安全性

角色授予其成员对整个模型的访问级别。

| 值               | 含义                                                                  |
| --------------- | ------------------------------------------------------------------- |
| `None`          | 无访问权限。无论角色中的其他设置如何，成员都无法连接到模型。                                      |
| `Read`          | 成员可以读取模型的元数据并查询其数据，但会受该角色的 RLS 和 OLS 约束。这是几乎所有面向 Report 用户的角色所使用的值。 |
| `ReadRefresh`   | 与 `Read` 类似，但成员还可以刷新模型。                                             |
| `Refresh`       | 成员可以刷新模型，但不能查询模型；例如，仅用于执行刷新的账户。                                     |
| `Administrator` | 成员对模型拥有完全控制权，包括更改模型；并且 RLS 和 OLS 不对其生效。仅适用于 Analysis Services。      |

新角色在设置此属性之前没有任何访问权限。如果你为 `ModelPermission` 为 `None` 且尚未设置任何表格权限的角色添加行级筛选器，Tabular Editor 会将其 `ModelPermission` 设为 `Read`。

对于模型中的角色，Power BI 和 Fabric 仅支持 `Read`：Microsoft 文档指出，这是唯一可以通过 XMLA endpoint 设置的角色权限。刷新、构建及其他权限由服务中的 Workspace 角色和语义模型权限进行管理，而 Power BI 中的模型角色仅用于 RLS 和 OLS。在 Power BI 服务中，如果部署角色时使用了任何其他值，部署都会失败，并显示错误：“请将行级安全性 (RLS) 角色的权限级别设为 'Read'”。

### 表格权限

`TablePermissions` · 表格权限的集合 · 翻译、透视、安全性 · 只读

该角色的表格权限对象集合；在此角色中，每个具有 RLS 筛选器或 OLS 设置的表各对应一个对象（参见 [表格权限](#table-permission)）。

**属性**视图不显示此集合。这些设置可通过上面的 [行级安全性](#row-level-security) 和 [表格权限](#table-permissions) (OLS) 进行编辑，Tabular Editor 会自动添加和删除表格权限。在 C# Script 中，可使用此集合遍历角色中受保护的表：

```csharp
foreach (var tp in Selected.Role.TablePermissions)
    Output(tp.Table.Name + ": " + tp.FilterExpression);
```

在 Tabular Editor 3 中，**TOM Explorer** 会在该角色下显示其表格权限。如果某个表格权限的所有设置都恢复为默认值，它就不会生效，并会以灰显方式显示。

## 表格权限

表格权限保存一个角色针对一张表的安全设置：包括 RLS 筛选器，以及该表及其列的 OLS 权限。表格权限以其所属表命名，且不能重命名。

当你在角色中为某个表设置 RLS 筛选器或 OLS 权限时，Tabular Editor 会创建一个表格权限。当你清除 RLS 筛选器，且该表格权限不包含任何 OLS 设置时，Tabular Editor 会将其移除。将 OLS 权限设回 `Default` 后，表格权限会保留，但不会生效，直到你将其删除。在 Tabular Editor 3 中，你也可以手动添加：右键单击该角色，然后选择 **添加表格权限...**。 @data-security-setup-rls 介绍了这一点，以及如何在使用前先在 DAX 查询中测试筛选表达式。

### 通用属性

- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [错误消息](xref:object-properties-common#error-message)
- [状态](xref:object-properties-common#state)

对于表格权限，**属性**视图不显示 `Name` 或 `ObjectType`。**元数据** 类别中的 `RoleName` 和 `TableName` 用于标识此表格权限。

### 角色

`RoleName` · string · 元数据 · 只读 · _指向角色名称的快捷方式_

此表格权限所属角色的名称。

### 表

`TableName` · string · 元数据 · 只读 · _指向表名称的快捷方式_

此表格权限所保护的表名称。

### 角色

`Role` · ModelRole · 选项 · 只读

此表格权限所属的角色，供 C# Script 在从表格权限回溯到其角色时使用。**属性**视图不会显示它，而会在 **元数据** 类别中显示 `RoleName`。

### OLS 列权限

`ColumnPermissions` · 每列 · 安全性 · 只读 · 兼容级别 1400+

该角色中此表每一列的对象级安全性 (OLS) 权限。展开此属性可查看每列一个条目。其取值与表的设置相同：

| 值         | 含义                                  |
| --------- | ----------------------------------- |
| `Default` | 未设置任何权限。该列遵循表的权限设置。                 |
| `Read`    | 角色成员可以查看并查询该列。                      |
| `None`    | 该列对角色成员隐藏。对角色成员而言，引用该列的查询和度量值将返回错误。 |

使用列级 OLS 隐藏敏感列，例如工资或个人数据，同时保持表的其余部分仍可用。对于角色成员，引用受保护列的度量值会失败。要查看哪些对象引用了某列，请在 **TOM Explorer** 中右键单击该列，然后选择 **显示依赖项...**（参见 @formula-fix-up-dependencies）。

这与列上的 `ObjectLevelSecurity` 设置相同（参见 @object-properties-columns）。

### 筛选表达式

`FilterExpression` · string · 翻译、透视、安全性

这是此角色中该表的行级安全性筛选器：一个会对角色成员可见的行返回 `TRUE` 的 DAX 表达式。空筛选器会使该表在此角色中不受筛选。你可以在 **表达式编辑器** 中编辑它，也可以通过角色或表的 `RowLevelSecurity` 属性进行编辑。示例见 [行级安全性](#row-level-security)。

该表达式会在表的每一行上下文中进行求值，因此可直接引用其列，例如 `'Region'[Country] = "Denmark"`。如果要使用其他表中的值，可以用 `RELATED` 或 `LOOKUPVALUE`。如果要查找当前用户，可以用 `USERPRINCIPALNAME ()` 或 `USERNAME ()`。

### OLS 表格权限

`MetadataPermission` · MetadataPermission · 翻译、透视、安全性 · 兼容级别 1400+

此角色中该表的对象级安全性 (OLS) 权限。

| 值     | 含义                          |
| ----- | --------------------------- |
| `默认值` | 未设置任何权限。角色成员可以看到该表。         |
| `读取`  | 角色成员可以看到并查询该表。              |
| `无`   | 该表会对角色成员隐藏，其列、度量值和关系也会一并隐藏。 |

这与角色上的 [表格权限](#table-permissions) 以及表上的 `ObjectLevelSecurity` 是同一项设置。

不能将来自不同角色的 RLS 和 OLS 组合使用。属于这类角色组合的用户在查询时会报错，在 SQL Server Analysis Services、Azure Analysis Services 和 Power BI 中均是如此。另见 @data-security-about、[将 OLS 与 RLS 结合使用](xref:data-security-setup-ols#5-combine-ols-with-rls) 以及 Microsoft 的 [对象级安全性限制](https://learn.microsoft.com/analysis-services/tabular-models/object-level-security#restrictions)。

如果使用 OLS 隐藏某个表会破坏其他表之间的关系链，则也不能这样做。引擎会返回错误并拒绝该操作。

## Windows 角色成员

Windows 角色成员是来自 Active Directory 的 Windows 用户或组，例如 `CONTOSO\SalesManagers`。 SQL Server Analysis Services 使用 Windows 成员，而 Azure Analysis Services 和 Power BI 使用 [外部角色成员](#external-role-member)。 Power BI 服务在部署时会拒绝 Windows 成员，并显示错误：“仅支持 Microsoft Entra 用户或组。请将标识提供者的值设为 'AzureAD'。"

尽可能添加组：向组中添加或移除人员无需更改或重新部署模型。

### 常见属性

- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

**属性** 视图不会显示角色成员的 `Name`。 `MemberName` 用于标识该成员。

### 成员 ID

`MemberID` · 字符串 · 选项

用户或组的安全标识符 (SID)，例如 `S-1-5-21-...`。可以将其留空，只填写 `MemberName`。在 Tabular Editor 3 中，使用 Windows 对象选取器选择成员时（`MemberName` 上的省略号按钮），Tabular Editor 会同时填入名称和 SID。

部署到 SQL Server Analysis Services 时，Tabular Editor 会按原样部署 `MemberID`。只有当目标是 Azure Analysis Services 或 Power BI 时，它才会移除成员 ID（请参阅[外部角色成员](#external-role-member)中的 `MemberID`）。

部署仅设置了 `MemberName` 的 Windows 成员时，SQL Server Analysis Services 会查找该账户，并将其 SID 存储在 `MemberID` 中。如果账户不存在，它会拒绝该账户，并显示类似于“'Sales' 角色包含一个不存在的域账户”这样的错误。这是在 SQL Server 2025 Analysis Services 上观察到的行为。

### 成员名称

`MemberName` · 字符串 · 选项

Windows 用户或组的名称，采用 `DOMAIN\name` 格式，例如 `CONTOSO\SalesManagers`。如果该帐户不存在于服务器信任的域中，部署将失败。

### 角色

`角色` · ModelRole · 选项 · 只读

此成员所属的角色，供 C# Script 从成员反查到其角色时使用。在 **属性** 视图中不会显示该项。

## 外部角色成员

外部角色成员是由外部标识提供者标识的用户或组；在实际场景中，这通常是 Microsoft Entra ID（前称 Azure Active Directory）。 Azure Analysis Services 和 Power BI 使用外部成员。在 Tabular Editor 中，将其作为 **Azure AD Member** 添加到角色的 `Members` 集合中（参见 @data-security-setup-rls）。

### 通用属性

- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

**属性**视图中不显示角色成员的 `Name`。 `MemberName` 用于标识该成员。

### 标识提供者

`IdentityProvider` · string · 选项

对该成员进行身份验证的标识提供者。添加外部成员时，Tabular Editor 会将其设置为 `AzureAD`。这是 Azure Analysis Services 和 Power BI 使用的唯一值。

### 成员 ID

`MemberID` · string · 选项

Microsoft Entra ID 中用户或组的对象 ID。 SQL Server Analysis Services 要求这样：SQL Server 2025 Analysis Services 会拒绝未设置成员 ID 的外部成员，并报错“MemberID must be specified when creating an External RoleMembership object”，即在创建 External RoleMembership 对象时必须指定 MemberID。对于 Azure Analysis Services 和 Power BI，把它留空即可。 Microsoft 的示例仅使用 `MemberName` 和 `IdentityProvider` 添加外部成员。

部署到 Azure Analysis Services 或 Power BI 时，不得设置成员 ID。当部署目标为 Azure Analysis Services 或 Power BI 服务时，Tabular Editor 会移除所有角色成员的成员 ID，包括它从目标数据库中保留下来的那些成员的成员 ID。部署到 SQL Server Analysis Services 时会保留这些 ID。你无法启用或关闭此行为。

### 成员名称

`MemberName` · string · 选项

用于标识用户或组的名称。对于用户，它是用户主体名称，通常就是电子邮件地址，例如 `anna@contoso.com`。组和其他成员支持的格式取决于目标。

在 Azure Analysis Services 中：

- 可将安全组以 `obj:<group object ID>@<tenant ID>` 的形式添加，或通过其电子邮件地址添加；Microsoft 365 组则通过其电子邮件地址添加
- 可将服务主体以 `app:<application ID>@<tenant ID>` 的形式添加
- 部署时会在 Microsoft Entra ID 中检查每个名称；如果使用用户或组的显示名称，或使用不存在的用户，则会失败，并显示错误 "was not found in your organization's Microsoft Entra ID"
- 名称会按你输入的内容原样存储，因此 `obj:` 名称仍会保持为 `obj:`，而 `MemberID` 仍为空

在 Power BI 服务中：

- 用户的用户主体名称可用，`obj:<object ID>@<tenant ID>` 也可用，但服务会将其改写为用户主体名称
- 可将安全组以 `obj:<group object ID>@<tenant ID>` 的形式添加，服务会按输入原样保留；也可通过其电子邮件地址添加启用邮件的安全组
- 使用用户或组的显示名称、使用不存在的用户地址，或使用 Microsoft 365 组都会失败，并显示错误 "There are invalid rolememberships in roles"
- 服务会用用户的对象 ID 填充 `MemberID`

在 Power BI 服务的安全设置中，你可以按电子邮件地址或名称添加用户和组。这些设置支持通讯组、启用邮件的组和 Microsoft Entra 安全组，不支持 Microsoft 365 组。

### 成员类型

`MemberType` · RoleMemberType · 选项

指定成员是单个用户还是组。

| 值       | 含义                    |
| ------- | --------------------- |
| `Auto`  | 服务器会判断该成员是用户还是组。      |
| `User`  | 该成员是单个用户。             |
| `Group` | 该成员是安全组，其所有成员都会获得该角色。 |

Windows 角色成员没有此属性：服务器会根据账户判断其是用户还是组。

Azure Analysis Services 和 Power BI 服务会忽略你设置的值：

- Azure Analysis Services 会将每个外部成员都存储为 `Auto`，无论你将其设置为 `Auto`、`User` 还是 `Group`，对用户和组都一样。
- the Power BI 服务会自行判断类型，并将用户存储为 `User`、将组存储为 `Group`，无论你将其设置为 `Auto`、`User` 还是 `Group`。它还会为两者填入 `MemberID`。在 Power BI 中，将此属性保留为 `Auto`。

### 角色

`角色` · ModelRole · 选项 · 只读

此成员所属的角色，供在 C# Script 中从成员反查其角色时使用。**属性** 视图不会显示该项。
