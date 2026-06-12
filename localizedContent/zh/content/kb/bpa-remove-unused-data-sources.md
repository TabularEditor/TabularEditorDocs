---
uid: kb.bpa-remove-unused-data-sources
title: 删除未使用的数据源
author: Morten Lønskov
updated: 2026-01-09
description: 用于删除孤立数据源的最佳实践规则，可降低模型复杂性并提升可维护性。
---

# 删除未使用的数据源

## 概述

此最佳实践规则用于识别未被任何分区或表表达式引用的数据源。 删除未使用的数据源可以降低模型复杂性、提升可维护性，并避免混淆。 删除未使用的数据源可以降低模型复杂性、提升可维护性，并避免混淆。

- 类别：维护
- 严重性：低（1）

## 适用范围

- Provider数据源
- Structured数据源

## 为何重要

未使用的数据源会带来不必要的开销：

- **维护负担**：需要为未使用的连接维护凭据和连接字符串
- **安全隐患**：不必要的连接字符串可能暴露敏感信息
- **模型复杂性**：额外对象会让数据源列表更加杂乱
- **混淆**：开发者可能会误用已过时的数据源
- **部署问题**：未使用的数据源可能引用了已不存在的系统
- **文档负担**：额外对象需要在模型文档中加以说明

未使用的数据源通常由以下情况导致：

- 重构分区以改用其他数据源
- 将多个数据源合并为一个
- 删除表但未清理其数据源
- 测试其他连接方式

## 此规则何时触发

当数据源同时满足以下所有条件时，就会触发此规则：

```csharp
UsedByPartitions.Count() == 0
and not Model.Tables.Any(SourceExpression.Contains(OuterIt.Name))
and not Model.AllPartitions.Any(Query.Contains(OuterIt.Name))
```

换句话说：

1. 没有任何分区直接引用该数据源
2. 没有任何表的源表达式（M 查询）按名称引用该数据源
3. 任何分区查询中都不包含该数据源名称

## 如何修复

### 自动修复

此规则提供自动修复，可删除未使用的数据源：

```csharp
Delete()
```

应用步骤：

1. 在 **Best Practice Analyzer** 中选择被标记的对象
2. 点击 **Apply Fix**

### 手动修复

1. 在 **TOM Explorer** 中展开 **数据源** 节点
2. 右键点击未使用的数据源
3. 选择 **Delete**
4. 确认删除

### 删除前

确认该数据源确实未被使用：

- 检查所有表中的所有分区
- 在 M 表达式中搜索对该数据源名称的引用
- 检查自定义表达式和计算表格
- 确保文档中没有引用该连接

## 示例

### 修复前

```
数据源:
  - SQLServer_Production (Provider, 供 Sales 分区使用)
  - SQLServer_Staging (Provider, 未使用)  ← 删除
  - AzureSQL_Archive (Structured, 未使用)  ← 删除
  - PowerQuery_Web (Structured, 供 Product 分区使用)
```

### 修复后

```
数据源:
  - SQLServer_Production (Provider, 供 Sales 分区使用)
  - PowerQuery_Web (Structured, 供 Product 分区使用)
```

**结果**：模型更简洁，只保留必要的数据源

## 误报

该规则可能会标记以下类型的数据源：

- 通过使用变量的动态 M 表达式引用
- 在被注释掉的分区查询中使用
- 在批注或描述中按名称引用

**解决方案**：删除前请先人工核实；如果出于文档记录需要保留该数据源，请添加注释或批注。

## 兼容级别

这个规则适用于兼容级别为 **1200** 及以上的模型。