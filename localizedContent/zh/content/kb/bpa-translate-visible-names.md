---
uid: kb.bpa-translate-visible-names
title: 为所有区域设置翻译可见对象名称
author: Morten Lønskov
updated: 2026-01-09
description: 最佳实践规则：确保为所有已定义的区域设置提供可见对象名称的翻译。
---

# 为所有区域设置翻译可见对象名称

## 概览

此规则用于识别在模型中定义的一个或多个区域设置中缺少名称翻译的可见对象。

- 类别：模型布局
- 严重性：低 (1)

## 适用于

- 表
- 度量值
- 层次结构
- 数据列
- 计算列
- 计算表格
- 计算表格列

## 为何这很重要

- **本地化不完整**：不同区域设置的用户会看到未翻译的名称
- **体验不一致**：翻译与未翻译内容混杂
- **用户困惑**：未提供预期的语言支持
- **专业形象**：翻译不完整会显得不够专业

## 此规则何时会触发

当对象同时满足以下两个条件时，此规则会触发：

1. 该对象对终端用户**可见**（未隐藏）
2. 在模型中，至少有一个区域设置**缺少该对象名称的翻译**

换句话说，对于定义了多个区域设置的可见对象，应为每个区域设置分别翻译其名称。

```csharp
IsVisible 
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedNames[it]))
```

## 如何修复

### 手动修复

1. 在 **TOM Explorer** 中，选择该对象
2. 在 **Properties** 窗格中，展开 **Translated Names**
3. 为每个区域设置输入翻译
4. 保存更改

## 常见原因

### 原因 1：添加了新对象

新建对象时未提供翻译。

### 原因 2：后续添加了区域设置

在对象创建后才添加到模型中的区域设置。

### 原因 3：翻译流程不完整

翻译流程未覆盖所有对象。

## 示例

### 修复前

```
Measure: [Total Sales]
English: "Total Sales"
Spanish: (missing)
French: (missing)
```

### 修复后

```
Measure: [Total Sales]
English: "Total Sales"
Spanish: "Total de Ventas"
French: "Total des Ventes"
```

## 兼容级别

该规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [翻译透视](xref:kb.bpa-translate-perspectives) - 如何翻译透视名称
- [翻译描述](xref:kb.bpa-translate-descriptions) - 如何翻译描述
