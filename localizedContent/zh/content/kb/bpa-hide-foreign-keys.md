---
uid: kb.bpa-hide-foreign-keys
title: 隐藏外键列
author: Morten Lønskov
updated: 2026-01-09
description: 用于隐藏外键列的最佳实践规则，可为最终用户简化模型。
---

# 隐藏外键列

## 概述

此最佳实践规则会识别对最终用户可见的外键列（关系的多方）。 外键应隐藏，因为它们仅用于建立关系连接，展示出来没有分析价值。

- 类别：格式设置

- 严重性：中（2）

## 适用于

- 数据列
- 计算列
- 计算表格列

## 为何这很重要

可见的外键列会造成不必要的杂乱：

- **用户困惑**：外键看起来像有用的数据，但其实只是重复了维度属性
- **字段冗余**：用户会同时看到键值以及相关的维度属性
- **字段列表更长**：用户为了找到相关字段，需要滚动浏览更多对象
- **误用风险**：用户可能按键值分组，而不是按正确的维度属性分组
- **可视化效果差**：图表显示的是键值，而不是易读的名称

外键的存在仅用于在表之间建立关系。 一旦关系建立完成，用户就应使用维度属性，而不是外键本身。

## 何时触发此规则

当某列满足以下条件时，将触发该规则：

1. 在关系中用作“from”列（多端）使用
2. 该关系的“from”端基数为多
3. 该列可见（`IsHidden = false`）

```csharp
UsedInRelationships.Any(FromColumn.Name == current.Name and FromCardinality == "Many")
and
IsHidden == false
```

## 如何修复

### 自动修复

这条规则包含一个自动修复：

```csharp
IsHidden = true
```

应用步骤：

1. 在 **Best Practice Analyzer** 中选择被标记的外键列
2. 点击 **Apply Fix**

### 手动修复

1. 在 **TOM Explorer** 中找到外键列
2. 在 **属性** 窗格中，将 **IsHidden** 设置为 **true**
3. 保存更改

## 常见原因

### 原因 1：模型设置不完整

创建关系后，外键仍然可见。

### 原因 2：批量导入

导入表后未进行隐藏外键的后处理。

### 原因 3：旧版模型

在较早的模型中，并未强制隐藏外键。

## 示例

### 修复前

```
Sales 表字段 (可见):
  - OrderDate
  - CustomerKey  ← 外键 (应隐藏)
  - ProductKey   ← 外键 (应隐藏)
  - SalesAmount
  - Quantity
```

**用户体验**：字段列表显得很杂乱。 用户可能会误用 `Sales[CustomerKey]`，而不是 `Customer[CustomerName]`。

### 修复后

```
Sales 表字段 (可见):
  - OrderDate
  - SalesAmount
  - Quantity
```

**用户体验**：字段列表很清晰。 用户会自然使用维度属性，关系筛选会自动生效。

## 兼容级别

这个规则适用于兼容级别 **1200** 及以上的模型。

## 相关规则

- [将数值列的 SummarizeBy 设为 None](xref:kb.bpa-do-not-summarize-numeric)——相关列配置
- [列的格式字符串](xref:kb.bpa-format-string-columns)——列显示设置
