---
uid: kb.bpa-perspectives-no-objects
title: 透视应包含对象
author: Morten Lønskov
updated: 2026-01-09
description: 用于移除不含任何可见对象的空透视的最佳实践规则。
---

# 透视应包含对象

## 概览

此最佳实践规则用于识别不包含任何可见表的透视。 空透视没有任何用途，应将其移除。

- 类别：维护
- 严重性：低（1）

## 适用范围

- 透视

## 为什么这很重要

- **用户困惑**: 空透视会显示在客户端工具中，但不会展示任何数据

## 何时触发此规则

当某个透视没有任何可见表时，会触发该规则：

```csharp
Model.Tables.Any(InPerspective[current.Name]) == false
```

## 如何修复

### 自动修复

此规则包含一项自动修复，可删除空透视：

```csharp
Delete()
```

应用方法：

1. 运行 **Best Practice Analyzer**
2. 选择空透视
3. 单击 **应用修复**

### 手动修复

1. 在 **TOM Explorer** 中展开 **透视** 节点
2. 右键单击空白透视
3. 选择 **删除**

## 常见原因

### 原因 1：已移除所有表

未删除透视的情况下，从透视中移除了所有表。

### 原因 2：配置不完整

在设计时创建了透视，但从未填充任何内容。

## 示例

### 修复前

```
透视：
  - Sales（包含：Sales、Customer、Product 表）✓
  - Marketing（包含：无表）✗
```

### 修复后

```
透视：
  - Sales（包含：Sales、Customer、Product 表）✓
```

## 兼容级别

此规则适用于兼容级别 **1200** 及以上的模型。

## 了解更多

- [表格模型中的透视](https://learn.microsoft.com/analysis-services/tabular-models/perspectives-ssas-tabular)

