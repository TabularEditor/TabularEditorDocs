---
uid: data-security-setup-ols
title: 设置或修改 OLS
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

# 设置或修改对象级安全性 (OLS)

![数据安全 Visual 摘要](~/content/assets/images/data-security/data-security-configure-ols-visual-abstract.png)

---

**通过调整针对表或列定义的角色或对象权限来更改 OLS。** 对象权限是 TOM 属性，可通过 `Object Level Security` 属性查看，其取值可以是 `Default`（不启用 OLS；功能上类似于 `Read`）、`Read` 或 `None`。 OLS differs from RLS in that it does not filter data, but prevents execution of the object **and all dependents.** This means any relationship or measure that references the object where `Object Level Security` is set to `None` will return an error upon evaluation.

---

- [**关于数据安全和 RLS/OLS：**](data-security-about.md) <span style="color:#01a99d">RLS</span> 与 <span style="color:#8d7bae">OLS</span> 的功能概览。
- [**修改/设置 RLS 配置：**](data-security-setup-rls.md) 如何在 Dataset 中配置 <span style="color:#01a99d">RLS</span>。
- **修改/设置 OLS 配置（本文）：** 如何在 Dataset 中配置 <span style="color:#8d7bae">OLS</span>。
- [**使用模拟身份测试 RLS/OLS：**](data-security-testing.md) 如何使用 Tabular Editor 轻松验证数据安全。

---

## 在 Tabular Editor 3 中配置 OLS

_Below is an overview of common changes one might make to existing OLS. 此外，下文还介绍了针对非典型对象（度量值、计算组）配置 OLS 的策略：_

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

3. **将 `Model Permission` 属性设置为 `Read`：** 这是 Power BI Dataset 所必需的设置。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 3：</strong>为使用 Power BI，必须设置 Model Permission 属性。</figcaption>
</figure>

4. **设置权限：** 按下文所述设置 RLS 表格权限和/或 OLS 对象权限。

---

### 3。移除 OLS

要从模型中移除 OLS，必须将所有列和表在所有角色下的 `Object Level Security` 属性都配置为 `Default`。 To remove Data Security from the model, all Roles must be deleted.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-ols-default.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 4：</strong>选择某一列或表时，可在 <i>Properties</i> 窗格中找到“对象级安全性”属性。 The property does not exist for Measures, Relationships and other Object Types.</figcaption>
</figure>

> [!NOTE]
> 删除所有角色后，只要用户对 Dataset 拥有 _Read_ 权限，就能查看所有数据。

---

### 4. 设置或更改 OLS

Setup or Modification of OLS is trivial for Columns and Table. 只需选择对象并找到 `Object Level Security` 属性，然后使用下拉列表将该属性更改为所需值即可。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-ols-change.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 4：</strong>可通过旁边的下拉列表更改“对象级安全性”属性，并选择 <i>Default</i>、<i>None</i> 或 <i>Read</i>。</figcaption>
</figure>

---

### 5. 将 OLS 与 RLS 结合使用

要将 RLS 与 OLS 成功结合使用，需要让模型设计与数据安全/访问管理策略相互匹配。 Since RLS and OLS cannot combine across roles, this means if you plan on implementing both RLS and OLS, users are limited to a single role.

---

### 6. 为度量值配置 OLS

Natively, OLS works only on Columns, Tables and their dependents; there is no `Object-Level Security` property for measures. However, since OLS also applies to dependents, it is possible to design OLS that works on measures via disconnected tables or calculation groups. To do this, the measure DAX has to be altered to evaluate a column or calculation group configured with RLS. If the `Object-Level Security` property of that object is `None`, then the Measure will not evaluate.

另请参阅 SQLBI 的[这篇关于隐藏度量值的文章](https://www.sqlbi.com/articles/hiding-measures-by-using-object-level-security-in-power-bi/)，其中对这种方法做了详细说明。