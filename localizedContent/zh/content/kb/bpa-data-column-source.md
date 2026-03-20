---
uid: kb.bpa-data-column-source
title: 数据列必须指定源列
author: Morten Lønskov
updated: 2026-01-09
description: 一条最佳实践规则，确保数据列具有有效的源列映射，以防止刷新错误。
---

# 数据列必须指定源列

## 概述

此最佳实践规则用于识别缺少有效的 `SourceColumn` 属性的数据列。 每个数据列都必须引用底层数据源中的某个源列，才能在刷新时正常工作。

- 类别：错误预防
- 严重性：高（3）

## 适用范围

- 数据列

## 为何重要

- **刷新失败**：数据刷新操作会因“找不到列”错误而失败
- **部署问题**：在 Power BI 服务或 Analysis Services 中，模型验证失败
- **数据完整性**：列可能一直为空，或包含陈旧数据
- **依赖项损坏**：度量值和关系可能产生不正确的结果

## 此规则何时触发

当数据列满足以下条件时，会触发此规则：

```csharp
string.IsNullOrWhitespace(SourceColumn)
```

## 如何修复

### 手动修复

1. 在 **TOM Explorer** 中找到被标记的数据列
2. 在 **属性** 窗格中，找到 `Source Column` 属性
3. 请输入数据源查询中正确的源列名称
4. 验证映射是否与分区查询匹配

源列名称必须完全匹配：

- 对于 Power Query：M 表达式输出中的列名称
- 对于 SQL：SELECT 语句中的列名称或别名
- 对于 Direct Lake：Delta Lake 表中的列名称

## 常见原因

### 原因 1：源列已重命名

源查询已修改，列已重命名。

### 原因 2：手动创建列

列是手动创建的，但未指定源列。

### 原因 3：复制/粘贴导致损坏

从另一张表复制列，但未保留元数据。

## 示例

### 修复前

```
表：Sales
列：ProductName (DataColumn)
  SourceColumn：[空]
```

结果：刷新失败，并提示“在源查询中找不到列 'ProductName'”

### 修复后

```
表：Sales
列：ProductName (DataColumn)
  SourceColumn：ProductName
```

结果：刷新时该列会正确填充

## 兼容级别

这条规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [计算对象需要表达式](xref:kb.bpa-expression-required) — 确保计算列具有表达式
