---
uid: kb.bpa-translate-perspectives
title: 为所有区域设置翻译透视名称
author: Morten Lønskov
updated: 2026-01-09
description: 最佳实践规则：确保为所有已定义的区域设置翻译透视名称。
---

# 为所有区域设置翻译透视名称

## 概述

此规则用于识别在一个或多个区域设置中缺少名称翻译的模型透视。

- 类别：模型布局
- 严重性：低（1）

## 适用对象

- 模型
- 透视

## 为什么这很重要

- **本地化不完整**：透视仅以默认语言显示
- **体验不一致**：透视名称中既有已翻译的，也有未翻译的
- **用户困惑**：无法获得预期的语言支持
- **专业形象**：翻译不完整会降低模型质量

## 何时触发此规则

当透视存在以下情况时，此规则会触发：

- 模型中至少有一个区域设置的该透视名称**缺少翻译**

```csharp
Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedNames[it]))
```

## 如何修复

### 手动修复

1. 在 **TOM Explorer** 中选择该透视
2. 在 **Properties** 窗格中，展开 **Translated Names**
3. 为每个区域设置输入相应的翻译

## 常见原因

### 原因 1：新增透视

创建透视时未包含翻译。

### 原因 2：后续添加了区域设置

在定义透视之后才添加区域设置。

### 原因 3：翻译不完整

翻译工作流未覆盖透视。

## 示例

### 修复前

```
透视: "Sales Analysis"
英语: "Sales Analysis"
德语:（缺失）
```

### 修复后

```
透视: "Sales Analysis"
英语: "Sales Analysis"
德语: "Vertriebsanalyse"
```

## 兼容级别

这个规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [翻译可见名称](xref:kb.bpa-translate-visible-names) - 翻译对象名称
- [翻译描述](xref:kb.bpa-translate-descriptions) - 翻译描述
