---
uid: kb.bpa-role-security-not-enforced
title: 行级安全性和对象级安全性需要读取权限
author: Morten Lønskov
updated: 2026-11-12
description: 最佳实践规则，用于标记行级或对象级安全性无效的角色，或因角色的模型权限而阻止部署的角色。
---

# 行级和对象级安全需要读取权限

## 概述

此规则标记具有其模型权限忽略或不允许的安全设置的角色。行级安全性 (RLS) 筛选器和对象级安全性 (OLS) 仅对 `ModelPermission` 为 `Read` 或 `ReadRefresh` 的角色生效。

- 类别：安全
- 严重程度：高 (3)

## 适用于

- 角色（兼容模式不是 Power BI 的模型）

## 这为什么重要

- 具有表权限的 `Administrator` 或 `Refresh` 角色无法部署。即使表格权限不包含行筛选器或 OLS，SQL Server 2025 Analysis Services 也会拒绝它，并显示类似“……是管理员角色，因此不允许在其下存在 TablePermission 对象”的错误。
- 具有 `None` 权限的角色的成员无法连接到模型，因此该角色的 RLS 和 OLS 从不限制任何人
- 角色设置所描述的安全级别并非其成员所获得的安全级别

## 此规则的触发时机

当以下任一条件为真时，该规则将针对不在 Power BI 兼容模式下的模型中的角色触发：

- `ModelPermission` 为 `Administrator` 或 `Refresh`，且角色具有任何表权限
- `ModelPermission` 为 `None`，且表格权限具有行筛选器、OLS 设置为 `None` 的表格，或者在兼容级别 1400 及以上时，OLS 设置为 `None` 的列

```csharp
Model.Database.CompatibilityMode != "PowerBI"

and

(
    ((ModelPermission == "Administrator" or ModelPermission == "Refresh") and TablePermissions.Any())
    or
    (ModelPermission == "None" and TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) or MetadataPermission == "None" or (Model.Database.CompatibilityLevel >= 1400 and ColumnPermissions.Any(it == "None"))))
)
```

`Read` 的 OLS 设置不被视为 `None` 角色的安全设置。有关 Power BI 模型中的角色，请参阅 @kb.bpa-powerbi-role-read-permission。

## 如何修复

此规则没有自动修复。更改角色的权限会改变谁可以查询哪些数据，因此请按角色做出决定。

### 手动修复

如果角色的成员是您希望限制其数据访问权限的报表用户：

1. 在**TOM Explorer**中，选择该角色。
2. 在**属性**视图中，将**模型权限**设置为`Read`，如果成员也会刷新模型，则设置为`ReadRefresh`。

如果角色的成员需要管理员权限或刷新权限：

1. 在 **TOM Explorer** 中，展开角色。
2. 删除该角色下的表格权限。

请参阅 @object-properties-security，了解 **模型权限**的值。

## 常见原因

### 原因 1：在定义安全性后更改了权限

添加行筛选器时，该角色具有`Read`权限，后来有人将其设置为`Administrator`或`Refresh`。

### 原因 2：角色从管理员角色复制而来

从管理员角色或处理角色复制的角色在向其添加筛选器时保留了源角色的权限。

### 原因 3：新角色没有权限

在您设置之前，新角色具有`None`权限。该角色在任何人设置其权限之前就获得了其安全设置。

## 示例

### 修复前

```text
Role:               Regional Managers
Model Permission:   Administrator
Row Level Security: 'Region'[Country] = "Denmark"
```

部署到 SQL Server 2025 Analysis Services 失败。RLS 不适用于管理员，因此筛选器对角色的成员没有影响。

### 修复后

```text
Role:               Regional Managers
Model Permission:   Read
Row Level Security: 'Region'[Country] = "Denmark"
```

## 相关规则

- [Power BI 角色必须具有读取权限](xref:kb.bpa-powerbi-role-read-permission)
- [没有安全权限的角色覆盖受保护的角色](xref:kb.bpa-role-unrestricted-read)
- [避免成员同时属于 RLS 角色和 OLS 角色](xref:kb.bpa-role-mixed-rls-ols-members)

## 兼容级别

此规则适用于兼容级别为 **1200** 或更高的模型。在兼容级别 1400 及更高版本中检查列 OLS。
