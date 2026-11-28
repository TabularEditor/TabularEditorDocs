---
uid: kb.bpa-role-mixed-rls-ols-members
title: 避免成员同时具有 RLS 角色和 OLS 角色
author: Morten Lønskov
updated: 2026-11-12
description: 当一个角色对同一表或直接相关表应用行级安全性，而另一个角色对同一表或直接相关表应用对象级安全性时，此最佳实践规则会标记与另一个角色共用同一成员的角色。
---

# 避免成员同时属于 RLS 角色和 OLS 角色

## 概述

当两个角色中的一个角色使用行级安全性 (RLS) 筛选表格的行，而另一个角色使用对象级安全性 (OLS) 隐藏同一表格或直接相关表格上的列或表格时，此规则会标记与另一个角色共用同一成员的角色。来自该成员的查询将失败，并显示“不支持活动角色的组合”错误。

- 类别：安全
- 严重程度：高 (3)

## 适用于

- 角色

## 问题的重要性

- 受影响用户的查询失败，因此基于该模型构建的报告对该用户不起作用
- 仅当同时属于这两个角色的用户查询模型时，才会出现此错误，因此单独测试每个角色并不会发现此错误

## 此规则的触发时机

该规则将具有`Read`或`ReadRefresh`权限的每个角色与具有`Read`或`ReadRefresh`权限的每个其他角色进行比较。当两个角色具有同名成员且以下组合之一适用时，该规则将触发：

| 一个角色 | 另一个角色 |
|---|---|
| 表上的行筛选器 | 同一表上某些列的 OLS `None`，同时表和至少一列保持可见 |
| 表上的行筛选器 | 表上或表列上的 OLS `None`，通过活动关系与筛选后的表关联，方向不限 |

该规则将两个角色都标记出来。同时具有 RLS 和 OLS 的角色被视为任一端，因此，具有行筛选器和列 OLS 的角色与相关表格上具有行筛选器的角色相邻时，也会触发该规则。成员名称的比较不区分大小写，因此 `CONTOSO\alice` 和 `contoso\Alice` 匹配。

```csharp
(ModelPermission == "Read" or ModelPermission == "ReadRefresh")

and

Model.Roles.Any(
    Name != current.Name
    and (ModelPermission == "Read" or ModelPermission == "ReadRefresh")
    and Members.Any(current.Members.Any(string.Equals(MemberName, outerIt.MemberName, StringComparison.OrdinalIgnoreCase)))
    and (
        current.TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) and outerIt.TablePermissions.Any(Table.Name == outerIt.Table.Name and MetadataPermission != "None" and ColumnPermissions.Any(it == "None") and ColumnPermissions.Any(it != "None")))
        or current.TablePermissions.Any(MetadataPermission != "None" and ColumnPermissions.Any(it == "None") and ColumnPermissions.Any(it != "None") and outerIt.TablePermissions.Any(Table.Name == outerIt.Table.Name and not string.IsNullOrWhiteSpace(FilterExpression)))
        or Model.Relationships.Any(IsActive and (
            (not string.IsNullOrWhiteSpace(current.RowLevelSecurity[FromTable.Name]) and outerIt.TablePermissions.Any(Table.Name == outerIt.ToTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))))
            or (not string.IsNullOrWhiteSpace(current.RowLevelSecurity[ToTable.Name]) and outerIt.TablePermissions.Any(Table.Name == outerIt.FromTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))))
            or (current.TablePermissions.Any(Table.Name == outerIt.FromTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))) and not string.IsNullOrWhiteSpace(outerIt.RowLevelSecurity[ToTable.Name]))
            or (current.TablePermissions.Any(Table.Name == outerIt.ToTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))) and not string.IsNullOrWhiteSpace(outerIt.RowLevelSecurity[FromTable.Name]))
        ))
    )
)
```

### 规则不会标记的组合

以下组合有效，规则不会对其进行标记：

- 在彼此之间没有关系或仅通过非活动关系联接的表上应用 RLS 和 OLS
- 表级 OLS（无论是否有列级 OLS），位于没有关系（relationship）的 RLS 表上
- 隐藏 RLS 表中所有列的列级 OLS
- `Read` 的 OLS 设置，不限制任何内容

以下组合在查询时也会失败，且该规则不会检测到它们：

- 在相隔两个或更多个活动关系的表上应用 RLS 和 OLS
- 具有活动关系的 RLS 表上的表级 OLS
- 通过一个组同时属于两个角色的用户，例如，当一个角色列出安全组，而另一个角色列出该组中的用户时，或者当两个角色列出具有共同成员的不同组时
- 不在已加载模型中的成员，例如在 Power BI 服务中管理的角色成员

> [!NOTE]
> Microsoft 的[对象级安全性文档](https://learn.microsoft.com/analysis-services/tabular-models/object-level-security#restrictions)指出，不支持来自不同角色的 RLS 和 OLS 的任何组合。该规则遵循 SQL Server 2025 Analysis Services 和 Power BI 服务的行为，其中上述列为可行的组合不会失败。

## 如何修复

此规则没有自动修复。

### 手动修复

对于两个角色都列出的每个成员，请执行以下操作之一：

- 在一个角色中定义行筛选器和 OLS，并使该成员仅成为该角色的成员。同一角色中的 RLS 和 OLS 协同工作。
- 从两个角色中的一个角色中移除该成员

在“属性”视图中设置组合角色的行筛选器和 OLS。请参阅[将 OLS 与 RLS 结合](xref:data-security-setup-ols#5-combine-ols-with-rls)和@object-properties-security。

## 常见原因

### 原因 1：行和列的角色分离

该模型有一组角色按区域筛选数据，另一组角色隐藏敏感列，而有些用户需要同时具备这两组角色。

### 原因 2：成员随着时间的推移被添加

某用户被添加到 RLS 角色，后来又被添加到另一份报表的 OLS 角色。

## 示例

### 修复前

```text
Relationship: 'Invoices'[CustomerKey] -> 'Customers'[CustomerKey] (active)

Role: Europe           Model Permission: Read
                       Row Level Security on 'Customers': [Continent] = "Europe"
                       Members: CONTOSO\alice
Role: No Sales Value   Model Permission: Read
                       Object Level Security on 'Invoices'[Value]: None
                       Members: contoso\Alice
```

来自 `CONTOSO\alice` 的查询失败并报错。

### 修复后

```text
Role: Europe No Sales Value   Model Permission: Read
                              Row Level Security on 'Customers': [Continent] = "Europe"
                              Object Level Security on 'Invoices'[Value]: None
                              Members: CONTOSO\alice
```

`CONTOSO\alice` 已从 `Europe` 和 `No Sales Value` 中删除。

## 相关规则

- [行级和对象级安全性需要读取权限](xref:kb.bpa-role-security-not-enforced)
- [Power BI 角色必须具有读取权限](xref:kb.bpa-powerbi-role-read-permission)
- [没有安全权限的角色会覆盖受保护的角色](xref:kb.bpa-role-unrestricted-read)

## 兼容级别

此规则适用于兼容级别为 **1400** 或更高的模型。
