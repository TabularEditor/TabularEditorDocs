---
uid: kb.bpa-do-not-summarize-numeric
title: 将数值列的 SummarizeBy 设置为 None
author: Morten Lønskov
updated: 2026-01-09
description: 最佳实践规则：防止对不应求和的数值列进行错误的默认聚合。
---

# 将数值列的 SummarizeBy 设置为 None

## 概述

此最佳实践规则会识别可见的数值列（Int64、Decimal、Double），其默认聚合行为（`SummarizeBy`）不为 `None`。 大多数数值列不应被自动聚合，因为对 ID、非可加语境下的数量或代码等数值求和会产生毫无意义的结果。

- 类别：格式设置

- 严重性：高（3）

## 适用于

- 数据列
- 计算列
- 计算表格的列

## 为什么这很重要

对不合适的列进行默认聚合会带来严重问题：

- **错误分析**：用户会得到毫无意义的汇总（例如 CustomerID 的求和等）
- **误导性的 Dashboard**：Visual 默认会显示错误的数值
- **用户困惑**：用户必须在每个 Visual 中手动更改聚合方式
- **错误决策**：基于错误的自动聚合做出业务决策
- **数据可信度**：用户会对模型和数据失去信任

常见的“不应聚合”列包括 ID、键、代码、比率、百分比，以及不可加的数量。

## 此规则何时触发

当某列同时满足以下 ALL 项条件时，此规则会触发：

```csharp
(DataType = "Int64" or DataType="Decimal" or DataType="Double")
and
SummarizeBy <> "None"
and not (IsHidden or Table.IsHidden)
```

换句话说：可见的数值列，且其汇总方式不是“None”。

## 如何修复

### 自动修复

此规则提供自动修复：

```csharp
SummarizeBy = AggregateFunction.None
```

应用方法：

1. 在 **Best Practice Analyzer** 中选择被标记的对象
2. 单击 **Apply Fix**

### 手动修复

1. 在 **TOM Explorer** 中找到该列
2. 在 **Properties** 窗格中，找到 **Summarize By**
3. 将 **Sum**、**Average**、**Min**、**Max**、**Count** 或 **DistinctCount** 改为 **None**
4. 保存更改

## 常见原因

### 原因 1：默认导入行为

导入时，数值列默认使用 Sum 聚合。

### 原因 2：未审查列设置

模型部署时未检查列的聚合设置。

### 原因 3：ID 列未隐藏

数值型 ID 列保持可见，并沿用默认的 Sum 聚合。

## 示例

### 修复前

```
Column: CustomerID
  DataType: Int64
  SummarizeBy: Sum
```

**结果**：Visual 显示“CustomerID 的总和：12,456,789”（毫无意义的数字）

### 修复后

```
Column: CustomerID
  DataType: Int64
  SummarizeBy: None
```

**结果**：Visual 需要显式聚合，否则会逐个显示 Customer ID

## 兼容级别

这个规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [隐藏外键](xref:kb.bpa-hide-foreign-keys) - 相关的列清理规则
- [列格式字符串](xref:kb.bpa-format-string-columns) - 列格式设置

## 了解更多

- [列属性](https://learn.microsoft.com/analysis-services/tabular-models/column-properties-ssas-tabular)
- [何时使用度量值与计算列](https://learn.microsoft.com/power-bi/transform-model/desktop-tutorial-create-measures)
