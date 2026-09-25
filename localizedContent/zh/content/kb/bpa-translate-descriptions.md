---
uid: kb.bpa-translate-descriptions
title: 为所有区域设置翻译描述
author: Morten Lønskov
updated: 2026-01-09
description: 一条最佳实践规则，用于确保所有已定义的区域设置中都提供了对象描述的翻译。
---

# 为所有区域设置翻译描述

## 概览

此规则会识别在一个或多个区域设置中缺少描述翻译的对象。

- 类别：模型布局
- 严重性：低 (1)

## 适用于

- 模型
- 表
- 度量值
- 层次结构
- 级别
- 透视
- 数据列
- 计算列
- 计算表格
- 计算表格列

## 为何这很重要

- **本地化不完整**：描述只会以默认语言显示
- **帮助文本不一致**：用户会看到多种语言混用
- **用户困惑**：文档看起来不完整
- **专业形象**：缺失翻译会降低模型质量

## 此规则何时会触发

```csharp
not string.IsNullOrEmpty(Description) 
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedDescriptions[it]))
```

当某个对象同时满足下面两个条件时，这个规则就会触发：

1. 该对象有说明（不为空）
2. 模型中至少有一个区域设置缺少该说明的翻译

换言之，如果你已编写描述并定义了多个区域设置，则应为每个区域设置翻译所有描述。

## 如何修复

### 手动修复

1. 在 **TOM Explorer** 中，选择该对象
2. 在 **Properties** 窗格中，展开 **Translated Descriptions**
3. 为每个区域设置输入翻译

## 常见原因

### 原因 1：新增了说明

创建说明时未提供翻译。

### 原因 2：后续添加了区域设置

在编写描述之后才添加了区域设置。

### 原因 3：翻译不完整

翻译流程没有覆盖说明。

## 示例

### 修复前

```
Measure: [Total Revenue]
Description (English): "Sum of all revenue"
Description (Spanish): (missing)
```

### 修复后

```
Measure: [Total Revenue]
Description (English): "Sum of all revenue"
Description (Spanish): "Suma de todos los ingresos"
```

## 兼容级别

该规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [翻译可见名称](xref:kb.bpa-translate-visible-names) - 翻译对象名称
- [翻译显示文件夹](xref:kb.bpa-translate-display-folders) - 翻译显示文件夹
