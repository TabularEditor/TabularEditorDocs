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

**通过调整针对表或列定义的角色或对象权限来更改 OLS。** 对象权限是 TOM 属性，可通过 `Object Level Security` 属性查看，其取值可以是 `Default`（不启用 OLS；功能上类似于 `Read`）、`Read` 或 `None`。 OLS 与 RLS 的不同之处在于：它不会筛选数据，而是阻止该对象__及其所有依赖项__的执行。这意味着，任何引用 `Object Level Security` 设置为 `None` 的对象的关系或度量值，在计算时都会返回错误。 OLS 与 RLS 的不同之处在于：它不会筛选数据，而是阻止该对象__及其所有依赖项__的执行。这意味着，任何引用 `Object Level Security` 设置为 `None` 的对象的关系或度量值，在计算时都会返回错误。

---

- [**关于数据安全与 RLS/OLS：**](data-security-about.md) <span style="color:#01a99d">RLS</span> 与 <span style="color:#8d7bae">OLS</span> 的功能概览。
- [**修改/设置 RLS 配置：**](data-security-setup-rls.md) 如何在 Dataset 中配置 <span style="color:#01a99d">RLS</span>。
- **修改/设置 OLS 配置（本文）：** 如何在 Dataset 中配置 <span style="color:#8d7bae">OLS</span>。
- [**使用模拟身份测试 RLS/OLS：**](data-security-testing.md) 如何使用 Tabular Editor 轻松验证数据安全。

---

## 在 Tabular Editor 3 中配置 OLS

_下面概述了对现有 OLS 可能进行的一些常见修改。 _下面概述了对现有 OLS 可能进行的一些常见修改。 此外，下文还介绍了针对非典型对象（度量值、计算组）配置 OLS 的策略：_

---

### 1。 1。 删除角色

要从模型中删除角色，你可以直接按下 `Del` 键删除角色对象，或右键单击并选择“删除”。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-delete-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 在模型中删除角色。</figcaption>
</figure>

> [!NOTE]
> 只要至少还存在一个其他角色，分配到此角色的所有用户将无法再查看模型数据。

---

### 2。 2。 添加新角色

要向模型添加角色：

1. **右键单击“Roles”对象类型：** 这将打开对话框，以便你创建新角色。
2. **选择“Create” > “Role”：** 为新角色命名。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong>在模型中创建新角色。</figcaption>
</figure>

3. **将 `Model Permission` 属性设置为 `Read`：** 这是 Power BI Dataset 所必需的设置。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-create-role.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 3：</strong>为使用 Power BI，必须设置 Model Permission 属性。</figcaption>
</figure>

4. **设置权限：** 按下文说明设置 RLS 表格权限和/或 OLS 对象权限。

---

### 3。 3。 移除 OLS

要从模型中移除 OLS，必须将所有列和表在所有角色下的 `Object Level Security` 属性都配置为 `Default`。 要从模型中移除数据安全性，必须删除所有角色。 要从模型中移除数据安全性，必须删除所有角色。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-ols-default.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 4：</strong>选择某一列或表时，可在 <i>Properties</i> 窗格中找到“对象级安全性”属性。 度量值、关系以及其他对象类型不提供此属性。</figcaption>
 度量值、关系以及其他对象类型不提供此属性。</figcaption>
</figure>

> [!NOTE]
> 删除所有角色后，只要用户对 Dataset 拥有 _Read_ 权限，就能查看所有数据。

---

### 4。 4。 设置或更改 OLS

对于列和表，设置或修改 OLS 非常简单。 对于列和表，设置或修改 OLS 非常简单。 只需选择对象并找到 `Object Level Security` 属性，然后使用下拉列表将该属性更改为所需值即可。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-ols-change.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 4：</strong>可通过旁边的下拉列表更改“对象级安全性”属性，并选择 <i>Default</i>、<i>None</i> 或 <i>Read</i>。</figcaption>
</figure>

---&#x20;

### 5。 5。 将 OLS 与 RLS 结合使用

要将 RLS 与 OLS 成功结合使用，需要让模型设计与数据安全/访问管理策略相互匹配。 由于 RLS 与 OLS 无法跨角色组合，这意味着如果你计划同时实施 RLS 和 OLS，那么用户只能被分配到一个角色。 由于 RLS 与 OLS 无法跨角色组合，这意味着如果你计划同时实施 RLS 和 OLS，那么用户只能被分配到一个角色。

---

### 6。 6。 为度量值配置 OLS

默认情况下，OLS 仅适用于列、表及其依赖对象；度量值没有 `对象级安全性` 属性。 不过，由于 OLS 也会应用于依赖对象，因此可以通过断开连接的表或计算组来设计让 OLS 作用于度量值的方案。 要实现这一点，需要修改度量值的 DAX，使其在计算时评估一个已配置 RLS 的列或计算组。 如果该对象的 `对象级安全性` 属性为 `None`，那么该度量值就无法计算。

另请参阅 SQLBI 的[这篇关于隐藏度量值的文章](https://www.sqlbi.com/articles/hiding-measures-by-using-object-level-security-in-power-bi/)，其中对这种方法做了详细说明。