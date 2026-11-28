---
uid: kb.bpa-role-unrestricted-read
title: 无安全覆盖权限的角色覆盖有安全权限的角色
author: Morten Lønskov
updated: 2026-11-12
description: 最佳实践规则，用于标记在其他角色通过行级或对象级安全性限制数据的模型中授予无限制读取权限的角色。
---

# 无安全覆盖的角色的权限高于受保护角色

## 概述

此规则标记授予对所有数据的`Read`访问权限的角色，而模型中的其他角色则通过行级安全性 (RLS) 或对象级安全性 (OLS) 限制访问权限。多个角色的权限被组合在一起：同时是此角色和受保护角色的成员的用户可以查询所有数据。

- 类别：安全
- 严重程度：中（2）

## 适用于

- 角色

## 重要原因

- 将用户添加到不受限角色会移除该用户所属的每个其他角色的 RLS 和 OLS
- 属于错误角色的用户可以看到模型安全机制本应隐藏的数据，并且没有查询返回错误

## 此规则的触发时机

当所有以下条件都为真时，该规则将针对某个角色触发：

- `ModelPermission` 为 `Read` 或 `ReadRefresh`
- 该角色的表格权限中没有一个具有行筛选器、OLS 设置为 `None` 的表格，或者在兼容级别 1400 及以上时，没有一个具有 OLS 设置为 `None` 的列
- 具有 `Read` 或 `ReadRefresh` 权限的另一个角色至少具有其中一项设置

```csharp
(ModelPermission == "Read" or ModelPermission == "ReadRefresh")

and

not TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) or MetadataPermission == "None" or (Model.Database.CompatibilityLevel >= 1400 and ColumnPermissions.Any(it == "None")))

and

Model.Roles.Any(
    (ModelPermission == "Read" or ModelPermission == "ReadRefresh")
    and TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) or MetadataPermission == "None" or (Model.Database.CompatibilityLevel >= 1400 and ColumnPermissions.Any(it == "None")))
)
```

空白行筛选器和 `Read` 的 OLS 设置不会限制任何内容，该规则将仅具有这些设置的角色视为不受限制。在没有对 `Read` 或 `ReadRefresh` 角色进行保护的模型中，该规则不会触发。

## 如何修复

此规则没有自动修复。授予所有数据的角色通常是故意的，例如针对经理或支持团队。

### 手动修复

1. 在**TOM Explorer**中，选择已标记的角色并查看其**成员**。
2. 执行以下操作之一：
   - 如果允许每个成员查看所有数据，请保留该角色，然后在**最佳实践分析器**中右键单击结果，并选择**忽略项目**
   - 如果该角色的成员需要受限访问权限，请向该角色添加行筛选器或 OLS
   - 如果某个成员也因疏忽而属于某个安全角色，请将该成员从此角色中移除

请参阅@object-properties-security和@using-bpa。

## 常见原因

### 原因 1：面向可查看所有数据的用户的角色

模型中有一个角色是为需要所有数据的 Report 经理或管理员设置的。

### 原因 2：为测试而创建的角色

添加了一个不带筛选器的角色来测试模型，并且该角色被保留了下来。

### 原因 3：从角色中删除了筛选器

该角色的行筛选器已被清除，但该角色仍有成员。

## 示例

### 修复前

```text
Role: All Data      Model Permission: Read   Row Level Security: (none)
                    Members: CONTOSO\alice, CONTOSO\bob
Role: Europe        Model Permission: Read   Row Level Security: 'Region'[Continent] = "Europe"
                    Members: CONTOSO\alice
```

`CONTOSO\alice`可以看到所有区域，因为`All Data`授予了`Europe`所限制的内容。

### 修复后

```text
Role: All Data      Model Permission: Read   Row Level Security: (none)
                    Members: CONTOSO\bob
Role: Europe        Model Permission: Read   Row Level Security: 'Region'[Continent] = "Europe"
                    Members: CONTOSO\alice
```

该规则仍标记 `All Data`。如果允许 `CONTOSO\bob` 查看所有数据，则忽略该结果。

## 相关规则

- [行级和对象级安全性需要读取权限](xref:kb.bpa-role-security-not-enforced)
- [Power BI 角色必须具有读取权限](xref:kb.bpa-powerbi-role-read-permission)
- [避免成员同时属于 RLS 角色和 OLS 角色](xref:kb.bpa-role-mixed-rls-ols-members)

## 兼容级别

此规则适用于兼容级别为 **1200** 或更高的模型。在兼容级别 1400 及更高版本中检查列 OLS。
