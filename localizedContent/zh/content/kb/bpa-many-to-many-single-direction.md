---
uid: kb.bpa-many-to-many-single-direction
title: 多对多关系应采用单向交叉筛选
author: Morten Lønskov
updated: 2026-01-09
description: 最佳实践规则：在多对多关系上使用单向筛选，以避免性能问题。
---

# 多对多关系应采用单向交叉筛选

## 概述

此最佳实践规则用于识别使用双向交叉筛选的多对多关系。 采用双向筛选的多对多关系会导致性能显著下降。

- 类别：性能
- 严重性：中等（2）

## 适用范围

- 关系

## 为什么这很重要

- **性能影响严重**：引擎必须在两个方向上评估筛选条件
- **内存消耗**：需要维护额外的筛选语境
- **筛选路径不明确**：多条路径可能产生意外结果
- **DAX 逻辑更复杂**：调试 FILTER 的筛选语境变得困难
- **循环依赖风险**：可能导致无限评估循环

## 何时触发此规则

当某个关系同时满足以下所有条件时，就会触发这个规则：

1. `FromCardinality = "Many"`
2. `ToCardinality = "Many"`
3. `CrossFilteringBehavior = "BothDirections"`

## 如何修复

### 手动修复

1. 在 **TOM Explorer** 中，找到被标记的关系
2. 在 **属性** 窗格中，找到 `Cross Filter Direction` 设置
3. 将其从 **双向** 改为 **单向**

根据典型的筛选流向选择方向：

- 从维度表到事实表
- 从查找表到数据表

如果确实需要反向筛选，就在度量值里显式处理：

```dax
SalesWithCrossFilter = 
CALCULATE(
    SUM('Sales'[Amount]),
    CROSSFILTER('BridgeTable'[Key], 'DimensionTable'[Key], Both)
)
```

## 常见原因

### 原因 1：默认双向设置

模型设计器默认启用了双向筛选。

### 原因 2：误解了需求

误以为所有场景都需要双向筛选。

### 原因 3：快速修复做法

为解决某个具体问题而使用双向筛选，但没有考虑性能影响。

## 示例

### 修复前

```
'Sales' (Many) <--> (Many) 'ProductBridge'
Cross Filter Direction: Both  ← 问题
```

### 修复后

```
'Sales' (Many) --> (Many) 'ProductBridge'
Cross Filter Direction: Single
```

当需要让 Products 筛选 Sales 时，可使用 DAX：

```dax
SalesForSelectedProducts = 
VAR SelectedProducts = VALUES('Products'[ProductKey])
RETURN
CALCULATE(
    SUM('Sales'[Amount]),
    TREATAS(SelectedProducts, 'ProductBridge'[ProductKey])
)
```

## 兼容级别

这个规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [关系数据类型必须匹配](xref:kb.bpa-relationship-same-datatype)——确保关系完整性

## 了解更多

- [Power BI 中的多对多关系](https://learn.microsoft.com/power-bi/transform-model/desktop-many-to-many-relationships)
- [关系交叉筛选](https://learn.microsoft.com/power-bi/transform-model/desktop-relationships-understand)
- [DAX CROSSFILTER 函数](https://dax.guide/crossfilter/)
- [DAX TREATAS 函数](https://dax.guide/treatas)
