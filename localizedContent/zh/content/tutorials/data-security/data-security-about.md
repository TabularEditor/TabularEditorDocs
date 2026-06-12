---
uid: data-security-about
title: 什么是数据安全？
author: Kurt Buhler
updated: 2023-03-02
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

# 什么是数据安全？

![数据安全 Visual 摘要](~/content/assets/images/data-security/data-security-visual-abstract.png)

---

已发布的 Dataset 可通过 <span style="color:#01a99d">[行级安全性 (RLS)](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls)</span>（适用于表）或 <span style="color:#8d7bae">[对象级安全性 (OLS)](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-ols?tabs=table)</span>（适用于表和列）来配置数据安全。 已发布的 Dataset 可通过 <span style="color:#01a99d">[行级安全性 (RLS)](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls)</span>（适用于表）或 <span style="color:#8d7bae">[对象级安全性 (OLS)](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-ols?tabs=table)</span>（适用于表和列）来配置数据安全。 **数据安全旨在确保用户只能查看和使用其获准访问的数据——无论是在已发布的 Report 中，还是在构建自助式数据解决方案时。** 为此，系统会将用户分配到已配置 <span style="color:#01a99d">**RLS**</span> 或 <span style="color:#8d7bae">**OLS**</span> 规则的 **角色** 中；这些规则会对由 Report 以及 Power BI Desktop、Excel 等客户端工具生成的查询进行 <span style="color:#01a99d">**FILTER（RLS）**</span> 或 <span style="color:#8d7bae">**限制（OLS）**</span>。

虽然[并非强制](https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance#when-to-avoid-using-rls)，但[数据安全是健壮、安全且合规的企业级 BI 解决方案中的常见功能](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-report-consumer-planning#enforce-data-security-based-on-consumer-identity)。 本系列将从功能角度介绍数据安全，以及它在表格建模与 Tabular Editor 中的应用。 本系列将从功能角度介绍数据安全，以及它在表格建模与 Tabular Editor 中的应用。

_在 Tabular Editor 中，可以轻松配置、修改并测试 RLS 和 OLS。_

---

- **关于数据安全与 RLS/OLS（本文）：** 从功能角度概览 <span style="color:#01a99d">RLS</span> 和 <span style="color:#8d7bae">OLS</span>。
- [**修改/设置 RLS 配置：**](data-security-setup-rls.md) 如何在 Dataset 中配置 <span style="color:#01a99d">RLS</span>。
- [**修改/设置 OLS 配置：**](data-security-setup-ols.md) 如何在 Dataset 中配置 <span style="color:#8d7bae">OLS</span>。
- [**使用模拟身份测试 RLS/OLS：**](data-security-testing.md) 如何使用 Tabular Editor 轻松验证数据安全。

<div class="NOTE">
  <h5>为什么要配置行级安全性或对象级安全性？</h5>
  配置 RLS 或 OLS 可为您的模型和 Report 带来益处：  
  <li> 通过确保用户只能看到其有权访问的数据，降低风险并强化治理。
  <li> 使用集中式角色表配置动态 RLS，以确保一致性并便于轻量维护。
  <li> 精细控制可查询的数据和对象范围。
</div>

---

### 它是如何工作的？

数据安全在模型层级生效。 按以下步骤进行配置： 按以下步骤进行配置：

#### 1。 1。 **创建角色：**

_角色_ 是一组拥有相同权限或数据安全逻辑的用户。 _角色_ 是一组拥有相同权限或数据安全逻辑的用户。 此处的 _用户_ 通过其邮箱地址识别，也可以使用 [Azure AD 安全组](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-tenant-level-planning#integration-with-azure-ad) 的邮箱地址进行识别。 角色示例： 角色示例：

- 同一地区、团队或部门的用户（_EMEA_、_UA Sales Team_）。
- 具有相同角色、职能或访问级别的用户（_Key Account Managers_、_SC Clearance_）。
- 按其他业务逻辑或任意规则定义的组（_Externals_、_Build Users_）。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 在 Tabular Editor 中，角色是顶级对象类型之一（类似于表、关系等）。</figcaption>
</figure>

> [!IMPORTANT]
> 在 Tabular Editor 中创建新角色后，必须先将 `Model Permission` 属性设置为 `Read`。

#### 2。 2。 **指定规则：**

根据安全类型，_规则_ 会按每个角色应用到一个或多个对象上：

- _<span style="color:#01a99d">RLS 表格权限：</span>_ DAX 表表达式——返回计算结果为 `True` 的行。 这些权限会沿着关系传播；**模型设计对良好的 RLS 规则至关重要。** 这些权限会沿着关系传播；**模型设计对良好的 RLS 规则至关重要。**

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong> 在 Tabular Editor 中，RLS 的表格权限显示在该角色下。 右键单击角色，然后选择 <i>'添加表分区...'</i>，即可创建新的表格权限。</figcaption>
 右键单击角色，然后选择 <i>'添加表分区...'</i>，即可创建新的表格权限。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions-dax.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 3：</strong> 选择某个表格权限时，可在表达式编辑器中查看其 DAX 表达式。</figcaption>
</figure>

- _<span style="color:#8d7bae">OLS 对象权限：</span>_ 这些权限既适用于主要对象，也适用于所有下游依赖对象。
  - `Read`（可查看/查询）
  - `None`（不可查看/查询）
  - `Default`（未配置策略；等同于 `Read`）

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions-dax.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 4：</strong> 在 Tabular Editor 中，可在“属性”窗口中“翻译、透视、安全”标题下访问对象权限。</figcaption>
</figure>

#### 3。 3。 **将用户分配到角色：**

在 Dataset 中完成配置后，需要将用户添加到其对应的角色中。

- _Power BI:_ 可通过 Tabular Editor 或 **Power BI/Fabric 服务** 分配角色；操作入口在 Workspace 的 Dataset 设置中：[详见此处](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security#manage-security-on-your-model)。
- _SSAS / AAS:_ 在角色对象上右键单击并选择“编辑成员...”，即可分配角色成员……
- _Power BI Embedded:_ 你必须[生成嵌入令牌](https://learn.microsoft.com/en-us/power-bi/developer/embedded/cloud-rls#generate-an-embed-token)。

你可以通过 Tabular Editor 按以下方式将用户/组添加到角色中或从角色中移除：

1. 右键单击 **角色**，选择 **编辑成员**……

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 7：</strong>通过右键单击某个角色并选择 <i>'编辑成员...'</i>，即可将用户分配到角色中</figcaption>
</figcaption>
</figure>

2. 单击“Add Windows AD Member”按钮上的__下拉按钮__，然后选择__Azure AD Member__：

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members-dialog.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 8：</strong>对于 AAS/SSAS 模型，可在 <i>'编辑成员...'</i> 对话框中添加用户。</figcaption>
</figure>

3. 在 **Member Name** 属性中指定 Azure AD 用户标识（通常是用户的电子邮件地址）。
4. 单击 **确定**。
5. **保存** 模型。

> [!IMPORTANT]
> 如果你的组织在 SQL Server Analysis Services 中使用本地 Active Directory，则需要使用 **Windows AD Member** 选项，而不是 **Azure AD Member**。

> [!NOTE]
> [建议](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-tenant-level-planning#strategy-for-using-groups)使用 [Azure Active Directory 组](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/how-to-manage-groups) 来管理数据安全与访问控制。 <br>推荐采用这种方式，以便集中管理安全性和用户分群。 <br>推荐采用这种方式，以便集中管理安全性和用户分群。

#### 4。 4。 **为用户开通 Dataset 访问权限：**

_Power BI:_ 必须根据[使用场景](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-overview)为用户授予 Dataset 访问权限。

- _App Audience:_ 将用户/其 Azure AD 组添加到相应的 [App Audience](https://data-goblins.com/power-bi/app-audiences)。
- _Workspace Viewer:_ 将用户/其 Azure AD 组添加为 [Workspace Viewer](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-workspaces-workspace-level-planning#workspace-access)
- _Dataset 读取者:_ 可通过 Dataset 或其依赖项向用户 / 其 Azure AD 组授予 [Dataset 专属权限](https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-manage-access-permissions)（即。 Report）。 Report）。

> [!WARNING]
> 被分配为[管理员、成员或参与者 Workspace 角色](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-roles-new-workspaces#workspace-roles)的用户对 Dataset 拥有___写入权限___。 因此，RLS 和 OLS 等数据安全机制不会对具有这些角色的用户进行数据筛选或阻止访问。 <br><br>
> **_如果用户是管理员、成员或参与者，他们将能够看到所有数据_**。 <br><br>
> 在合理范围内，尽量通过 Power BI 应用来分发和管理权限。 因此，RLS 和 OLS 等数据安全机制不会对具有这些角色的用户进行数据筛选或阻止访问。 <br><br>
> **_如果用户是管理员、成员或参与者，他们将能够看到所有数据_**。 <br><br>
> 在合理范围内，尽量通过 Power BI 应用来分发和管理权限。

#### 5。 5。 **验证安全性：**

只有在添加用户组并授予其访问权限后，才能通过用户模拟来测试 RLS 和 OLS。 可通过以下方式验证安全性： 可通过以下方式验证安全性：

- _Tabular Editor：_ 使用[用户模拟](data-security-testing.md)。
- _Power BI 服务：_ 在 [Dataset 安全设置](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls#validating-the-role-within-the-power-bi-service) 中。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-impersonation.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 5：</strong>使用 Tabular Editor 通过用户模拟来测试数据安全性，是最简单的方法。 任何数据查询功能 (DAX Queries, Pivot Grid, Preview Data) 均可使用“Impersonation”选项.</figcaption>
 任何数据查询功能 (DAX Queries, Pivot Grid, Preview Data) 均可使用“Impersonation”选项.</figcaption>
</figure>

> [!NOTE]
> 要通过用户模拟验证数据安全性，必须同时满足以下条件：
>
> - 必须为用户分配一个角色。
> - 用户必须对 Dataset 具有读取权限。
> - 用户必须对 Dataset 具有__构建权限__。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-impersonation-demo.gif" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 6：</strong>演示在 Tabular Editor 中使用用户模拟进行 RLS 测试。 图中展示了在 (A) 数据预览、(B) DAX 查询和 (C) Pivot Grid 中进行测试。</figcaption>
 图中展示了在 (A) 数据预览、(B) DAX 查询和 (C) Pivot Grid 中进行测试。</figcaption>
</figure>

> [!IMPORTANT]
> 使用 Tabular Editor 3 通过用户模拟测试数据安全性，仅适用于托管在 Power BI Datasets 服务中的 Dataset。 TE3 Desktop 许可证无法使用此功能。 这是因为角色是在 Power BI 服务中分配的。 TE3 Desktop 许可证无法使用此功能。 这是因为角色是在 Power BI 服务中分配的。

---

### 效果如何？

根据数据安全性的设计与配置方式不同，用户体验可能有所差异。
以下是在 Dataset 中实施 RLS 和/或 OLS 的常见场景示例
以下是在 Dataset 中实施 RLS 和/或 OLS 的常见场景示例

_点击选项卡查看示例，并了解每个示例的说明：_

---

# [无](#tab/nodatasecurity)

**未启用安全性时，任何有权访问该 Dataset 的人都能看到全部数据。**

唯一的限制在于他们是否有权访问这些 Report / Dataset。

![无安全性](~/content/assets/images/data-security/data-security-no-security.png)

_在该示例中，Jack 和 Janet 都能看到全部数据。_

# [静态 RLS](#tab/staticrls)

**配置 RLS 后，数据会被筛选为仅包含用户被允许查看的行。** 这取决于在模型中为相应表和角色配置的 _表格权限_。 这些表格权限是在特定模型表上配置的 DAX 表表达式。 计算结果为 `True` 的行会被返回；返回 `False` 的行会因 RLS 被筛除。 这些表格权限是在特定模型表上配置的 DAX 表表达式。 计算结果为 `True` 的行会被返回；返回 `False` 的行会因 RLS 被筛除。

最简单的表格权限是 _静态_：

```dax
// 'Regions' 表的表格权限，适用于 'CTG' 角色
'Regions'[Territory] = "Central Transit Gate"
```

![静态 RLS 配置](~/content/assets/images/data-security/data-security-static-rls.png)

_在该示例中：_

1. _Jack 只能看到满足 'Region'[Territory] = "Central Transit Gate" 的行，因为他属于 'CTG' 角色。_
2. _可查看全部数据的高管会被加入一个不包含任何表格权限的角色。_
3. _Tommy 可以访问该 Dataset，但不属于任何角色，所以看不到任何数据。 所有 Visual 和查询都会显示一个“灰色死亡框”。_

_即使存在像高管这样拥有不受限制数据访问权限的用户，使用数据安全性时也必须创建角色。_

# [动态 RLS](#tab/dynamicrls)

**配置 RLS 后，数据会被筛选为仅包含用户被允许查看的行。**
这取决于在模型中为相应表和角色配置的 _表格权限_。

这些表格权限是在特定模型表上配置的 DAX 表表达式。
计算结果为 `True` 的行会被返回；返回 `False` 的行会因 RLS 被筛除。

**_动态_ RLS 依赖 `USERPRINCIPALNAME()` 或 `USERNAME()` 函数，并将其与安全表进行比较。**
随后，安全表会返回相应逻辑，将表筛选器应用到该表或模型中的另一张表。

之所以称为 _动态_ RLS，是因为结果会随用户而变化；即 `USERPRINCIPALNAME()`。
下面是一个动态 RLS 表格权限示例：
下面是一个动态 RLS 表格权限示例：

```dax
// “Regions”表与“Territory Directors”角色的表格权限。

// 获取当前用户
VAR _CurrentUser = 
SELECTCOLUMNS (
	FILTER ( 
		'Employees',
		'Employees'[Employee Email] = USERPRINCIPALNAME ()
	), 
	"@Name", 'Employees'[Employee Name]
)
RETURN 
'Regions'[Territory Directors] IN _CurrentUser
```

上述表格权限会从“Employees”表中获取 Employee Name 的别名，并在未与“Regions”表建立关系的情况下应用到“Regions”表。
把任何用户加到这个角色后，结果是：他们只会看到满足以下条件的数据：
把任何用户加到这个角色后，结果是：他们只会看到满足以下条件的数据：

1. 他们的电子邮件地址位于 'Employees'[Employee Email] 列中
2. 他们在 'Employees'[Employee Name] 中的别名与 'Regions'[Territory Directors] 中的某个值匹配

![动态 RLS 配置](~/content/assets/images/data-security/data-security-dynamic-rls.png)

_在该示例中，每位 Territory Director 只能看到自己负责的 Territory：_

1. _Jack 看到 “Central Transit Gate” 和 “Io”。_
2. _Janet 看到 “Arcadia III”。_
3. _Elisa 可以看到所有数据，因为 Execs 角色未设置任何表格权限。_

_动态 RLS 是保护企业级 Dataset 最常见的方式。 它通常需要配置并维护一张集中式 **安全表**，供所有企业级 Dataset 共享使用。_ 它通常需要配置并维护一张集中式 **安全表**，供所有企业级 Dataset 共享使用。\*

# [RLS（多个角色）](#tab/multipleroles)

**当用户被分配到多个角色，且这些角色具有不同的表格权限时，他们将看到任一角色允许的数据。** 用户会看到满足以下条件的数据：至少有一个表格权限 DAX 表达式对模型表行求值为 `True`；也就是说采用逻辑 `or`。

如果这不是预期行为，就会很危险；有些开发者可能以为会取交集——也就是只显示 **两者** 的表格权限都返回 `True` 的行。 如果这不是预期行为，就会很危险；有些开发者可能以为会取交集——也就是只显示 **两者** 的表格权限都返回 `True` 的行。 只有在为模型中的多张表配置了表格权限时才会出现这种情况；在 **同一个角色** 内，会对模型中的所有表格权限取交集。

![RLS 角色使用逻辑 OR 合并表格权限](~/content/assets/images/data-security/data-security-combining-rls-roles.png)

_在该示例中：_

1. _Jack 被分配到“CTG”和“FTL”两个角色。 他会看到满足以下任一条件的行：'Products'[Type] = "FTL" **或** 'Regions'[Territory] = "Central Transit Gate"。 这很可能不是预期行为；开发者大概率想要得到“CTG/FTL”角色的结果，即只返回两者都为 True 的行。_
2. _Elijah 拥有“FTL”角色，只会看到 'Products'[Type] = "FTL" 的行。
3. _Abdullah 拥有“CTG/FTL”角色，只会看到 **两者都** 满足以下条件的行：'Products'[Type] = "FTL" **并且** 'Regions'[Territory] = "Central Transit Gate"。_

_类似的情况说明，在模型设计阶段制定清晰的数据安全配置很重要，也要确保其与组织策略以及现有的数据安全/访问管理实践保持一致。_

# [OLS](#tab/ols)

**当 OLS 配置为 `None` 时，查询将被阻止执行，并会返回错误。** 这与 RLS 的一个重要区别在于：RLS 会过滤数据，而 OLS 会阻止查询求值。 如果 OLS 权限设置为 `Read`，则不会产生任何影响。 这取决于列或表的 OLS 权限级别，并且会__影响所有下游依赖项__，例如关系和度量值。 如果 OLS 权限设置为 `Read`，则不会产生任何影响。 这取决于列或表的 OLS 权限级别，并且会__影响所有下游依赖项__，例如关系和度量值。

![为 Cost 列配置的 OLS](~/content/assets/images/data-security/data-security-ols.png)

_在此示例中，列“Territory Sales”[Cost] 在角色“Sales”下的 OLS 权限为 `None`。 原因是下面这个需求：_ 原因是下面这个需求：_

`“Sales”用户可以查看 Sales 数据，但不能查看 Cost 或 Margin 数据。`

_这意味着，例如 Jack 这样属于“Sales”角色的用户将无法看到：_

1. _任何直接引用“Territory Sales”[Cost] 列的查询或可视化对象_
2. _任何直接引用“Territory Sales”[Cost] 列的 DAX 度量值或计算项，例如 [Margin %]_
3. _任何以 _间接_（下游）方式引用“Territory Sales”[Cost] 列的 DAX 度量值或计算项。_
4. _任何其列与“Territory Sales”[Cost] 存在关系的对象_

_上述 1-4 的任一情况都会在查询求值时返回__错误__。 Power BI Visual 会显示一个__灰色死亡框__。_

> [!WARNING]
> __业务用户往往会把预期的 OLS 结果当成 Report、Visual 或查询“坏了”。 __ <br>如果使用 OLS，且用户预计会遇到这些求值错误，请尝试以下做法：<br> __ <br>如果使用 OLS，且用户预计会遇到这些求值错误，请尝试以下做法：<br>
>
> 1. 向用户讲清楚安全机制。
> 2. 尝试处理错误，并返回更有意义的信息。
> 3. 在 Build 场景中，考虑隐藏该对象。
> 4. 另一个可测试的优化是将 `IsPrivate` 设为 `True`，或将 `IsAvailableInMDX` 设为 `False`。

# [RLS+OLS（单个角色）](#tab/rlsols)

同时配置 RLS 和 OLS 时，会有两种可能结果：

1. **用户只有_一个角色_同时配置了 RLS 和 OLS：** 只要配置正确，安全性就会按预期工作。
2. **用户有_多个角色_分别配置了 RLS 和 OLS：** 这种角色组合不受支持，用户将收到错误。

鉴于第 2 点，如果你预计要同时使用 RLS 和 OLS，就必须在模型设计阶段谨慎考虑这一点。

下面是 #1 的示例：

![在同一角色中同时配置 OLS 和 RLS 会得到预期结果](~/content/assets/images/data-security/data-security-ols-and-rls-functional.png)

_在该示例中：_

1. _Jack 被分配到“CTG”角色：_
   - _由于在 'Regions' 上配置了 RLS 表格权限，他只能看到 "Central Transit Gate" 的数据。_
   - _只能查看 Sales 数据，无法查看 [Margin %]。 _只能查看 Sales 数据，无法查看 [Margin %]。 这是因为对 'Territory Sales'[Cost] 设置了 OLS 对象权限 `None`，从而影响其依赖的度量值 [Margin %]_
2. _Elisa 被分配到“Execs”角色，可以查看所有数据。 _Elisa 被分配到“Execs”角色，可以查看所有数据。 “Execs”未配置任何 RLS 表格权限，也未配置 OLS 对象权限（保持为 `Default`）。_
3. _Tommy 未被分配任何角色，无法看到任何数据。_

> [!WARNING]
> 同时使用 RLS 和 OLS 的场景并不少见。 <br>但正确使用它们的场景却不多。 <br>如果你确实需要同时使用 RLS 和 OLS，一定要在模型设计阶段仔细评估。

# [❌ RLS+OLS（合并角色）](#tab/rlsolscombined)

同时配置 RLS 和 OLS 时，可能出现两种结果：

1. **用户只有 _一个角色_ 同时配置了 RLS 和 OLS：** 只要配置正确，安全性将按预期工作。
2. **用户有 _多个角色_，且分别配置了 RLS 和 OLS：** 不支持这种角色组合，用户会报错。

鉴于 #2，若你计划同时使用 RLS 和 OLS，务必在模型设计阶段慎重评估。

下面是 #2 的示例：

![❌ 跨角色组合 OLS 和 RLS 会产生错误](~/content/assets/images/data-security/data-security-ols-and-rls-dysfunctional.png)

_在上述示例中：_

1. _Jack 被分配到“Read Users”角色：_
   - _由于在 'Regions' 上配置了 RLS 表格权限，他只能看到 "Central Transit Gate" 的数据。_
   - _只能查看 Sales 数据，无法查看 [Margin %]。 _只能查看 Sales 数据，无法查看 [Margin %]。 这是因为对 'Territory Sales'[Cost] 设置了 OLS 对象权限 `None`，从而影响其依赖的度量值 [Margin %]_
2. _同时被分配了“Read Users”和“Build Users”角色的 Janet：_
   - _看不到任何数据。 跨多个角色的 RLS / OLS 权限组合无效。_

_被授予该 Dataset 的 Build 权限的用户会被添加到 Build Azure AD 安全组，该安全组已为“Build Users”角色设置。 _被授予该 Dataset 的 Build 权限的用户会被添加到 Build Azure AD 安全组，该安全组已为“Build Users”角色设置。 Build 用户可以看到现有 Report 中未包含的表，因此在“Employees”表上配置了 `None` 的 OLS 权限。 这会导致 RLS 与 OLS 权限无法协调，从而引发错误。_ 这会导致 RLS 与 OLS 权限无法协调，从而引发错误。_

> [!WARNING]
> 同时组合 RLS 和 OLS 的场景并不罕见。 <br>但能正确使用它们的场景却不多。 <br>如果你需要同时使用 RLS 和 OLS，请在模型设计阶段谨慎评估。 <br>但能正确使用它们的场景却不多。 <br>如果你需要同时使用 RLS 和 OLS，请在模型设计阶段谨慎评估。

# [❌ 无角色](#tab/role)

**只要在 Dataset 中配置了数据安全，任何用户在加入该角色之前都无法读取任何数据**。

![无访问权限或无角色](~/content/assets/images/data-security/data-security-no-role.png)

> [!NOTE]
> 别忘了同时为用户授予对 Dataset 的访问权限，并把他们添加到安全角色中。

# [❌ 无访问权限](#tab/access)

**将用户添加到安全角色并不会自动授予他们对 Dataset 的读取权限**。他们仍然无法访问任何 Dataset 或 Report。

![无访问权限或无角色](~/content/assets/images/data-security/data-security-no-access.png)

> [!NOTE]
> 别忘了同时为用户授予对 Dataset 的访问权限，并把他们添加到安全角色中。

> [!WARNING]
> **在可行的情况下，最佳实践是避免通过 Workspace 角色进行授权。** <br> 如有必要，请确保遵循__最小权限原则__：用户应仅拥有完成其工作所需的最低访问权限。

# [❌ 通过 Workspace 角色访问](#tab/workspace)

**如果用户通过 Admin、Member 或 Contributor 角色获得对某个 Dataset 的访问权限，那么无论数据安全配置如何、也无论其被分配了哪些角色，他们都能查看所有数据。** 这在扩展或自助式 Power BI 生态中很常见，会导致数据泄露和不合规。

![Workspace 角色带来的问题](~/content/assets/images/data-security/data-security-workspace-roles.png)

> [!WARNING]
> **在可行的情况下，最佳实践是避免通过 Workspace 角色进行授权。** <br> 如有必要，请确保遵循__最小权限原则__：用户应仅拥有完成其工作所需的最低访问权限。

---

---

### 硬性限制

某些 Report 或 Data model 功能在启用 RLS 或 OLS 后将无法使用。 例如： 例如：

1. [RLS 限制](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls#considerations-and-limitations)
   - 已添加到 RLS 角色的服务主体
   - 使用 SSO 测试 DirectQuery 模型
   - [Power BI 中的“发布到 Web”](https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance#when-to-avoid-using-rls)

2. [OLS 限制](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-ols?tabs=table#considerations-and-limitations)
   - 合并单独的 RLS 角色和 OLS 角色（如上所述）
   - 问答功能
   - 快速见解
   - 智能叙述
   - Excel 数据类型库

---

### 延伸阅读与参考资料

如需进一步深入了解数据安全，请参阅以下资料：

1. [Power BI 安全白皮书](https://learn.microsoft.com/en-us/power-bi/guidance/whitepaper-powerbi-security)
2. [Power BI 文档 - 安全性](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-power-bi-security)
3. [Analysis Services 文档 - 对象级安全性](https://learn.microsoft.com/en-us/analysis-services/tabular-models/object-level-security?view=asallproducts-allversions)
4. [Power BI 实施规划 - 安全性](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-security-report-consumer-planning)
5. [(相关) Power BI 实施规划 - 信息保护与数据丢失防护（DLP）](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-info-protection-data-loss-prevention-overview)