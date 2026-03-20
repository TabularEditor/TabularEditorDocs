---
uid: kb.bpa-translate-display-folders
title: 为所有区域设置提供显示文件夹翻译
author: Morten Lønskov
updated: 2026-01-09
description: 最佳实践规则：确保为所有已定义的区域设置翻译显示文件夹。
---

# 为所有区域设置提供显示文件夹翻译

## 概述

此规则用于识别已设置显示文件夹但在一个或多个区域设置中缺少翻译的可见对象。

- 类别：模型布局
- 严重性：低（1）

## 适用于

- 度量值
- 层次结构
- 数据列
- 计算列
- 计算表格的列

## 为什么这很重要

- **本地化不完整**：显示文件夹只会以默认语言显示
- **导航不一致**：文件夹结构仅部分翻译
- **用户困惑**：组织结构看起来不完整
- **专业形象**：缺失翻译会降低模型质量

## 此规则何时会触发

当某个对象同时满足以下三项条件时，此规则会触发：

1. 该对象对最终用户**可见**（未隐藏）
2. 该对象已设置**显示文件夹**（用于将其组织到文件夹结构中）
3. 模型中至少有一个区域设置未为该显示文件夹**提供翻译**

通俗地说：如果可见对象是按显示文件夹来组织的，那么这些文件夹名称就应该为模型中的所有区域设置都提供翻译。

```csharp
IsVisible
and not string.IsNullOrEmpty(DisplayFolder)
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedDisplayFolders[it]))
```

## 如何修复

### 自动修复

```csharp
TranslatedDisplayFolders.Reset()
```

将翻译重置为使用默认的显示文件夹。

### 手动修复

1. 在 **TOM Explorer** 中选择对象
2. 在属性中展开 **已翻译的显示文件夹**
3. 为每个区域设置输入翻译

## 常见原因

### 原因 1：新增了显示文件夹

创建显示文件夹时未提供翻译。

### 原因 2：后续才添加区域设置

在定义显示文件夹之后才添加了区域设置。

### 原因 3：翻译不完整

翻译流程没有覆盖显示文件夹。

## 示例

### 修复前

```
度量值：[Total Sales]
显示文件夹（英语）：“Sales Metrics”
显示文件夹（法语）：（缺失）
```

### 修复后

```
度量值：[Total Sales]
显示文件夹（英语）：“Sales Metrics”
显示文件夹（法语）：“Métriques de Vente”
```

## 兼容级别

这个规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [翻译可见名称](xref:kb.bpa-translate-visible-names) — 翻译对象名称
- [翻译描述](xref:kb.bpa-translate-descriptions) — 翻译描述
