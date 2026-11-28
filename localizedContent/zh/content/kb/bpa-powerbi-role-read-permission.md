---
uid: kb.bpa-powerbi-role-read-permission
title: Power BI 角色必须具有读取权限
author: Morten Lønskov
updated: 2026-11-12
description: 最佳实践规则，用于标记 Power BI 语义模型中模型权限不是“读取”的角色。
---

# Power BI 角色必须具有读取权限

## 概述

此规则会标记 Power BI 语义模型中 `ModelPermission` 不是 `Read` 的角色。Power BI 仅支持模型角色上的 `Read` 权限。刷新或编辑模型等访问权限来自 Power BI 服务中的工作区角色和语义模型权限。

- 类别：安全
- 严重性：高 (3)

## 适用于

- 角色（仅限 Power BI 语义模型）

## 这为何重要

- Power BI 服务拒绝部署具有 `None`、`ReadRefresh`、`Refresh` 或 `Administrator` 权限的角色（无论是否具有表格权限），并显示错误“请将行级安全性 (RLS) 角色的权限级别设置为“读取””
- Power BI 中的模型角色对其成员应用行级安全性 (RLS) 和对象级安全性 (OLS)，且不授予其他访问权限

## 此规则的触发时机

对于 Power BI 兼容模式下模型中权限不是 `Read` 的每个角色，都会触发此规则：

```csharp
Model.Database.CompatibilityMode == "PowerBI"

and

ModelPermission != "Read"
```

Analysis Services 兼容模式下模型中的角色由 @kb.bpa-role-security-not-enforced 检查。

## 如何修复

此规则没有自动修复。将角色设置为 `Read` 会让其成员有权访问数据，因此请先检查每个角色。

### 手动修复

1. 在 **TOM Explorer** 中，选择角色。
2. 检查角色的行筛选器和 OLS 是否限制了其成员所能看到的内容。
3. 在**属性**视图中，将**模型权限**设置为 `Read`。
4. 通过 Power BI 服务中的工作区角色或语义模型权限授予刷新、构建或编辑访问权限。

> [!WARNING]
> 如果角色没有行筛选器，也没有 OLS，将其设置为 `Read` 会让其成员有权访问模型中的所有数据。

RLS 和 OLS 不适用于具有工作区**管理员**、**成员**或**贡献者**角色的用户。请参阅@object-properties-security。

## 常见原因

### 原因 1：角色是从 Analysis Services 模型复制的

该角色来自 Analysis Services 模型，其中 `Administrator`、`ReadRefresh` 和 `Refresh` 是有效权限。

### 原因 2：刷新账户的角色

创建该角色的目的是让服务账户刷新模型。

### 原因 3：没有权限的新角色

在您设置之前，新角色具有 `None` 权限。

## 示例

### 修复前

```text
Role:               Sales Refresh
Model Permission:   ReadRefresh
Row Level Security: 'Region'[Country] = "Denmark"
```

### 修复后

```text
Role:               Sales Refresh
Model Permission:   Read
Row Level Security: 'Region'[Country] = "Denmark"
```

刷新账户在 Power BI 服务中获得**贡献者**工作区角色，但不是该角色的成员。

## 相关规则

- [行级和对象级安全性需要读取权限](xref:kb.bpa-role-security-not-enforced)
- [没有安全权限的角色会覆盖受保护的角色](xref:kb.bpa-role-unrestricted-read)
- [避免成员同时属于 RLS 角色和 OLS 角色](xref:kb.bpa-role-mixed-rls-ols-members)

## 兼容级别

此规则适用于兼容级别为 **1200** 或更高的 Power BI 模型。
