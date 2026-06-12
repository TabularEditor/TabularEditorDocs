---
uid: data-security-testing
title: 测试 RLS/OLS
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

# 通过模拟测试数据安全

![数据安全 Visual 摘要](~/content/assets/images/data-security/data-security-testing-visual-abstract.png)

---

**DAX 查询**、**Pivot Grid** 或 **预览数据** 可用于在 Tabular Editor 中测试数据安全。 建议每次更改配置后都_务必_测试数据安全，以降低 RLS/OLS 实施不当及其后果带来的风险。 建议每次更改配置后都_务必_测试数据安全，以降低 RLS/OLS 实施不当及其后果带来的风险。

> [!IMPORTANT]
> 在 Tabular Editor 3 中使用模拟来测试数据安全，仅适用于托管在 Analysis Services 实例或 Power BI 服务中的 Dataset。 Tabular Editor 3 桌面版许可证无法使用此功能。 Tabular Editor 3 桌面版许可证无法使用此功能。

---

- [**关于数据安全和 RLS/OLS：**](data-security-about.md) <span style="color:#01a99d">RLS</span> 与 <span style="color:#8d7bae">OLS</span> 的功能概览。
- [**修改/设置 RLS 配置：**](data-security-setup-rls.md) 如何在 Dataset 中配置 <span style="color:#01a99d">RLS</span>。
- [**修改/设置 OLS 配置：**](data-security-setup-ols.md) 如何在 Dataset 中配置 <span style="color:#8d7bae">OLS</span>。
- **使用模拟测试 RLS/OLS（本文）：** 如何使用 Tabular Editor 轻松验证数据安全。

---

## 使用模拟进行测试

**在 Tabular Editor 3 中使用 _模拟_ 功能即可轻松测试数据安全。** “模拟”是一项功能，可让你以模型角色或用户的身份查看查询结果。 它类似于 Power BI 服务中的 _“以角色查看...”_ 功能，但有两个关键区别： 它类似于 Power BI 服务中的 _“以角色查看...”_ 功能，但有两个关键区别：

1. 被模拟的最终用户除了要分配角色并有 Dataset 读取权限外，还必须拥有 **Dataset 构建权限**。
2. 在 Tabular Editor 3 中可以执行任何查询；不像 Power BI 服务那样，仅限于 Report 中现有的 Visual。

这很有价值，因为它让你可以运行预定义的测试，看看任何拥有构建权限的最终用户会如何看到结果。 这有助于确保即使面对复杂查询和 DAX 表达式，数据安全也能按预期工作，用户只会看到他们应该看到的内容。 这有助于确保即使面对复杂查询和 DAX 表达式，数据安全也能按预期工作，用户只会看到他们应该看到的内容。

> [!IMPORTANT]
> 请确保不要通过为最终用户分配 Workspace 角色（Contributor、Member、Admin）来授予 Build 权限，因为这些角色对 Dataset 具有 **Write** 权限，从而会绕过数据安全；即使配置正确，测试也会看起来像没有生效一样。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-security/data-security-impersonation-demo.gif" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 在 Tabular Editor 中使用模拟身份进行 RLS 测试的演示。 图中展示了分别使用 (A) 数据预览、(B) DAX 查询和 (C) Pivot Grid 进行的测试。</figcaption>
 图中展示了分别使用 (A) 数据预览、(B) DAX 查询和 (C) Pivot Grid 进行的测试。</figcaption>
</figure>

---

## 如何使用模拟身份进行测试

要使用模拟身份进行测试，按以下步骤操作：

1. **确保 Dataset 配置和访问权限正确:**
   被模拟的最终用户……

- _...已分配到相应的 **角色**。_
- _...已被授予 **Dataset 读取访问权限**。_
- _...已被授予 **Dataset 生成访问权限**。 (Power BI)_ (Power BI)_
- _...**不是** Workspace 的 Contributor、Member 或 Admin（Power BI）_。

2. **新建一个 DAX 查询、Pivot Grid 或“预览数据”窗口：**

- 建议先从 _预览数据_ 开始，以观察对模型表的影响
- 随后，再用 _DAX 查询_ 进行第二次验证。 随后，再用 _DAX 查询_ 进行第二次验证。 这是因为 DAX 查询可以保存，用于文档记录和后续参考；当模型发生变更需要重新测试时会很有用。

3. **选择 'Impersonation' 并输入用户电子邮件:** 如果你已实施 _Static RLS_，也可以改为测试该角色。

4. **浏览数据，验证结果是否符合预期：**（根据安全规则）。

### 测试技巧

1. **测试多个用户:** 建议每个角色至少测试 3-10 个不同用户。 **测试多个用户:** 建议每个角色至少测试 3-10 个不同用户。 你也可以将测试自动化，遍历安全表中的每个 UPN（例如使用 C# Script 和宏）。

2. **测试每个角色和表格权限：** 由于每个表格权限对应不同的 DAX 筛选表达式，因此必须分别测试。 确保对每个角色都进行了测试，并且每次测试都包含配置了筛选表达式的相关表。 例如，如果某个角色在“Customers”和“Products”表上定义了表表达式，确保你的查询同时包含这两张表的属性，以便进行验证。 确保对每个角色都进行了测试，并且每次测试都包含配置了筛选表达式的相关表。 例如，如果某个角色在“Customers”和“Products”表上定义了表表达式，确保你的查询同时包含这两张表的属性，以便进行验证。

3. **测试多种查询/度量值：** 尽量找一些复杂查询来测试，尤其是在数据安全场景下可能出现问题的那些。 **测试多种查询/度量值：** 尽量找一些复杂查询来测试，尤其是在数据安全场景下可能出现问题的那些。 例如，如果计算需要与未过滤的总体平均值（即占总计的百分比）进行比较，并且预期 _该总计_ 在 RLS 中不会被过滤，那么开发者可能需要结合模型重新审视数据安全的实现方案。