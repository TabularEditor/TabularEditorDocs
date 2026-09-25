---
uid: data-security-setup-rls
title: 设置或修改 RLS
author: Kurt Buhler
updated: 2023-03-14
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

# 配置行级安全性 (RLS)

![数据安全 Visual 摘要](~/content/assets/images/data-security/data-security-configure-rls-visual-abstract.png)

---

**通过调整为表定义的角色或表格权限即可更改 RLS。** 在特定角色中选择某个表格权限时，可在“表达式编辑器”窗口中查看此 DAX _筛选表达式_。 This Filter Expression is the most important piece of the RLS configuration that determines what data is seen by a user.

---

- [**关于数据安全和 RLS/OLS：**](data-security-about.md) <span style="color:#01a99d">RLS</span> 与 <span style="color:#8d7bae">OLS</span> 的功能概览。
- **设置/修改 RLS 配置（本文）：** 如何在 Dataset 中配置 <span style="color:#01a99d">RLS</span>。
- [**修改/设置 OLS 配置：**](data-security-setup-ols.md) 如何在 Dataset 中配置 <span style="color:#8d7bae">OLS</span>。
- [**使用模拟身份测试 RLS/OLS：**](data-security-testing.md) 如何使用 Tabular Editor 轻松验证数据安全。

---

## 在 Tabular Editor 3 中配置 RLS

_下面概述了对现有 RLS 常见的一些修改：_

---

### 1. 删除角色

要从模型中删除角色，只需选中角色对象后按 `Del`，或右键并选择“删除”。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-delete-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 在模型中删除角色。</figcaption>
</figure>

> [!NOTE]
> 只要模型中至少还存在另一个角色，原本分配到该角色的所有用户将无法再查看模型数据。

---

### 2. 添加新角色

要在模型中添加角色：

1. **右键单击“角色”对象类型：** 这将打开一个对话框，供你创建新角色。
2. **选择“Create” > “角色”：** 给新角色命名。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong> 在模型中创建新角色。</figcaption>
</figure>

3. **将 `Model Permission` 属性设置为 `Read`：** 这是确保该角色的所有成员都能访问 Dataset 的必要设置。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-model-permission-read.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 3：</strong> 必须设置 Model Permission 属性。</figcaption>
</figure>

4. **设置权限：** 按下文所述设置 RLS 表格权限和/或 OLS 对象权限。

---

### 3。移除 RLS

要从模型中移除 RLS，必须删除所有表格权限。 To remove Data Security from the model, all Roles must be deleted.

> [!NOTE]
> 删除所有角色后，只要用户对 Dataset 具有 _Read_ 权限，就能看到所有数据。

---

### 4. 修改表格权限

要修改某个角色的现有表格权限：

1. **展开角色：** 这将显示表格权限。
2. **选择表格权限:** 这会在表达式编辑器中显示筛选权限 FILTER 的 DAX。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions-dax.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 4：</strong> 选择表格权限时，表达式编辑器会显示 DAX FILTER 表达式。</figcaption>
</figure>

3. **调整 FILTER 表达式 / RLS 表格权限：** 建议你在使用前先测试 / 验证 DAX：

- 将 FILTER 表达式复制到新的 DAX 查询窗口，并放在 `EVALUATE` 语句下方。
- 在 `ADDCOLUMNS` 语句中，将其作为 Expression，用于遍历某个表或其子集。
- 执行并观察结果。
- 在动态 RLS 中，将 `USERNAME()` 或 `USERPRINCIPALNAME()` 替换为安全表中的已知值。
- 重新运行 DAX 查询，并验证结果是否符合预期。 Repeat until satisfied.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-rls-validation.png" alt="Data Security Validation" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 5：</strong>演示如何在 DAX 查询窗口中，通过在针对表（或表的一部分，例如用户别名）的迭代器中使用 FILTER 筛选表达式来验证 RLS。 In this example, the original RLS Filter Expression in the Table Permission has been modified (Yellow) where an explicit User Principal Name in the dataset is added instead, to test (Green). The RLS code is executed inside of the ADDCOLUMNS iterator over a relevant part of the table. The checkmark indicates any row that evaluates to TRUE. The test demonstrates that the RLS is - for this UPN - working as expected, since <i>Gal Aehad</i> is the only user returning TRUE when their UPN is given.</figcaption>
</figure>

```dax
EVALUATE

// Create a table to test your RLS
ADDCOLUMNS ( 
  VALUES ( 'Regions'[Territory Directors] ),
  "@RLS-Validation",

    // RLS Code
    VAR _CurrentUser = 
      SELECTCOLUMNS (
        FILTER ( 
          'Employees', 
          'Employees'[Employee Email]

            // Replace USERPRINCIPALNAME() with a user email to test
            = "gal.aehad@spaceparts.co" // USERPRINCIPALNAME ()
        ),
        "@Name", 'Employees'[Employee Name]
      )
    RETURN
      'Regions'[Territory Directors] IN _CurrentUser

)

// Order from TRUE() to FALSE()
// Where it is TRUE() the data will be visible
ORDER BY [@RLS-Validation] DESC
```

---

### 5. 为角色添加新的表格权限

要添加新的表格权限：

1. **右键单击角色：** 选择“添加表格权限……”

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-table-permissions.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 6：</strong>在 Tabular Editor 中，RLS 的表格权限显示在角色下。 New table permissions can be created by right-clicking a Role and selecting <i>'Add Table Partition...'</i></figcaption>
</figure>

2. **选择表并点击“确定”：** 选择要为其创建权限的表。
3. **编写 FILTER 筛选表达式 / RLS 表格权限：** 为 FILTER 筛选表达式编写 DAX。 As above, you want to validate this filter expression (See **Figure 5**):

- 将 FILTER 筛选表达式复制到新的 DAX 查询窗口，并放在 `EVALUATE` 语句下。
- 将其作为 `ADDCOLUMNS` 语句的表达式，并对表或表的一部分进行迭代。
- 执行并查看结果。
- 将动态 RLS 中的 `USERNAME()` 或 `USERPRINCIPALNAME()` 替换为安全表中的已知值。
- 重新运行 DAX 查询，并验证结果是否符合预期。 Repeat until satisfied.

---

### 6. 为角色分配或移除用户

你可以在 Tabular Editor 中为角色分配或移除用户/组。

1. 右键单击__角色__，选择__编辑成员__……

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 7：</strong>通过右键单击某个角色并选择<i>“编辑成员……”</i>即可将用户分配到该角色</figcaption>
</figure>

2. 在“添加 Windows AD 成员”按钮上单击__下拉按钮__，然后选择__Azure AD 成员__：

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-edit-members-dialog.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 8：</strong>对于 AAS/SSAS 模型，可以通过 <i>“编辑成员...”</i> 对话框添加用户。</figcaption>
</figure>

3. 在__成员名称__属性中指定 Azure AD 用户标识（通常是用户电子邮件地址）。
4. 单击__确定__。
5. __保存__模型。

> [!IMPORTANT]
> 如果您的组织在 SQL Server Analysis Services 中使用本地 Active Directory，则需要使用__Windows AD 成员__选项，而不是__Azure AD 成员__。

> [!NOTE]
> 将 Power BI Dataset 发布到 Power BI 服务后，您还可以通过[Dataset 安全设置](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls#manage-security-on-your-model)来管理角色成员。 Alternatively, you can manage role members through [SQL Server Management Studio](https://learn.microsoft.com/en-us/analysis-services/tabular-models/manage-roles-by-using-ssms-ssas-tabular?view=asallproducts-allversions) (this applies to AAS/SSAS models in addition to Power BI dataset).

---
