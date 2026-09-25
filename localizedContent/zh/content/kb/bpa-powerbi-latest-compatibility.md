---
uid: kb.bpa-powerbi-latest-compatibility
title: 在 Power BI 模型中使用最新的兼容级别
author: Morten Lønskov
updated: 2026-09-14
description: 最佳实践规则：确保 Power BI 模型使用最新的兼容级别，以获得最佳功能与性能。
---

# 在 Power BI 模型中使用最新的兼容级别

## 概览

此规则用于识别未使用最新可用兼容级别的 Power BI 模型。 Using the latest level ensures access to newest features, performance optimizations, and bug fixes.

- 类别：治理
- 严重性：高（3）

## 适用于

- 模型（仅限 Power BI 语义模型）

## 为何这很重要

- **功能缺失**：无法使用新的 DAX 函数和模型能力
- **面向未来的兼容性**：使用较新的级别可让升级更轻松

## 此规则何时会触发

对于 Power BI 模型，当兼容级别低于当前最大值时会触发：

```csharp
Model.Database.CompatibilityMode=="PowerBI" 
and Model.Database.CompatibilityLevel<>[CurrentMaxLevel]
```

## 如何修复

### 自动修复

该最佳实践规则包含一个自动修复，会将兼容级别设置为当前安装的 Tabular Editor 3 所支持的最高可用级别。 If you have an older version of Tabular Editor 3 installed you should update your installation.

```csharp
Model.Database.CompatibilityLevel = [PowerBIMaxCompatibilityLevel]
```

### 手动修复

1. 在 Tabular Editor 中，转到 **Model** 属性页
2. 将**兼容级别**设置为最新版本
3. 测试所有 DAX 表达式和功能
4. 部署到 Power BI 服务

## 常见原因

### 原因 1：在 Power BI Desktop 中创建模型

在 Power BI Desktop 中创建的模型未必使用最新的兼容级别。

### 原因 2：模型以较低兼容级别创建

模型使用较旧版本的 Power BI Desktop 创建。

### 原因 3：保守做法

团队政策要求延后升级。

## 示例

### 修复前

```
Model Compatibility Level: 1500
Current Maximum Level: 1706
```

### 修复后

```
Model Compatibility Level: 1706 (Latest)
```

Access to newer capabilities such as [custom calendars](xref:calendars) (1701+), [DAX user-defined functions](xref:udfs) (1702+), @user-context-calculated-columns (1705+) and String Indexing Behavior on a column (1706+).

## 兼容级别

此规则适用于所有兼容级别的 Power BI 模型。