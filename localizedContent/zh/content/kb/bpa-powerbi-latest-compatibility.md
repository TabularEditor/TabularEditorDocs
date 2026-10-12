---
uid: kb.bpa-powerbi-latest-compatibility
title: 在 Power BI 模型中使用最新的兼容级别
author: Morten Lønskov
updated: 2026-09-23
description: 最佳实践规则：确保 Power BI 模型使用最新的兼容级别，以获得最佳功能与性能。
---

# 在 Power BI 模型中使用最新的兼容级别

## 概览

This rule flags Power BI models below the highest compatibility level that your Tabular Editor 3 version supports. New model features, such as new DAX functions and TOM properties, require the newer levels.

- 类别：治理
- 严重性：高（3）

## 适用于

- 模型（仅限 Power BI 语义模型）

## 为何这很重要

- new DAX functions and model features aren't available below the level that introduces them
- a model kept at a recent level needs smaller upgrades later

## 此规则何时会触发

The rule triggers for Power BI models whose compatibility level isn't the current maximum:

```csharp
Model.Database.CompatibilityMode=="PowerBI" 
and Model.Database.CompatibilityLevel<>[CurrentMaxLevel]
```

## 如何修复

### 自动修复

The rule's automatic fix sets the compatibility level to the highest level your installed version of Tabular Editor 3 supports. To get a newer level, update Tabular Editor 3.

```csharp
Model.Database.CompatibilityLevel = [PowerBIMaxCompatibilityLevel]
```

### 手动修复

1. In the TOM Explorer, select **Model** and expand **Database** in the **Properties** view.
2. Set **Compatibility Level** to the latest level.
3. Test the DAX expressions and features of the model.
4. Deploy to the Power BI Service.

参见 @update-compatibility-level。

## 常见原因

### 原因 1：在 Power BI Desktop 中创建模型

Power BI Desktop doesn't always create models at the latest compatibility level.

### 原因 2：模型以较低兼容级别创建

An older version of Power BI Desktop created the model.

### 原因 3：保守做法

A team policy delays upgrades.

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

The model can use [custom calendars](xref:calendars) (1701+), [DAX user-defined functions](xref:udfs) (1702+), [user-context calculated columns](xref:user-context-calculated-columns) (1705+) and the `StringIndexingBehavior` column property (1706+).

## 兼容级别

此规则适用于所有兼容级别的 Power BI 模型。