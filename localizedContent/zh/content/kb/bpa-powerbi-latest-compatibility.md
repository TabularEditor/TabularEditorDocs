---
uid: kb.bpa-powerbi-latest-compatibility
title: 在 Power BI 模型中使用最新的兼容级别
author: Morten Lønskov
updated: 2026-09-23
description: 最佳实践规则：确保 Power BI 模型使用最新的兼容级别，以获得最佳功能与性能。
---

# 在 Power BI 模型中使用最新的兼容级别

## 概览

此规则会标记兼容级别低于你所用 Tabular Editor 3 版本支持的最高级别的 Power BI 模型。新的模型功能（如新的 DAX 函数和 TOM 属性）需要较新的级别。

- 类别：治理
- 严重性：高（3）

## 适用于

- 模型（仅限 Power BI 语义模型）

## 为何这很重要

- 兼容级别低于引入这些功能的级别时，新的 DAX 函数和模型功能将不可用
- 将模型保持在较新的级别，后续升级所需改动会更小

## 此规则何时会触发

当 Power BI 模型的兼容级别不是当前最高级别时，此规则会触发：

```csharp
Model.Database.CompatibilityMode=="PowerBI" 
and Model.Database.CompatibilityLevel<>[CurrentMaxLevel]
```

## 如何修复

### 自动修复

此规则的自动修复会将兼容级别设置为你已安装的 Tabular Editor 3 版本所支持的最高级别。如需使用更新的级别，请更新 Tabular Editor 3。

```csharp
Model.Database.CompatibilityLevel = [PowerBIMaxCompatibilityLevel]
```

### 手动修复

1. 在 TOM Explorer 中，选择 **Model**，然后在 **Properties** 视图中展开 **Database**。
2. 将 **兼容级别** 设置为最新级别。
3. 测试模型的 DAX 表达式和功能。
4. 部署到 Power BI 服务。

参见 @update-compatibility-level。

## 常见原因

### 原因 1：在 Power BI Desktop 中创建模型

Power BI Desktop 并不总是按最新兼容级别创建模型。

### 原因 2：模型以较低兼容级别创建

该模型是由较旧版本的 Power BI Desktop 创建的。

### 原因 3：保守做法

团队政策要求延后升级。

## 示例

### 修复前

```text
Model Compatibility Level: 1500
Current Maximum Level: 1706
```

### 修复后

```text
Model Compatibility Level: 1706 (Latest)
```

该模型可以使用 [自定义日历](xref:calendars)（1701+）、[DAX 用户定义函数](xref:udfs)（1702+）、[用户上下文计算列](xref:user-context-calculated-columns)（1705+）以及 `StringIndexingBehavior` 列属性（1706+）。

## 兼容级别

此规则适用于所有兼容级别的 Power BI 模型。