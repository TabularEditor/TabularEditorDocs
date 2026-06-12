---
uid: kb.bpa-udf-use-compound-names
title: 为用户定义函数使用复合名称
author: Morten Lønskov
updated: 2026-03-19
description: 最佳实践规则：确保 DEFINE 中的用户定义函数使用分隔符字符，避免将来与新增的内置 DAX 函数发生命名冲突。
---

# 为用户定义函数使用复合名称

## 概述

此最佳实践规则会识别在 DEFINE 中定义且名称中不包含分隔符字符（`.` 或 `_`）的用户定义函数（UDF）。 此最佳实践规则会识别在 DEFINE 中定义且名称中不包含分隔符字符（`.` 或 `_`）的用户定义函数（UDF）。 复合名称可以避免命名冲突：如果 Microsoft 引入了同名的内置 DAX 函数，也不会受到影响。

- 类别：预防错误

- 严重性：低（1）

## 适用范围

- 用户定义函数

## 为什么这很重要

名称中不含分隔符字符的 UDF 将来可能会失效，风险包括：

- **命名冲突**：如果 Microsoft 添加了与你的 UDF 同名的新内置 DAX 函数，内置函数将优先生效，你的 UDF 将无法继续工作
- **歧义**：如果没有命名空间或前缀，就难以判断一次函数调用指向的是内置 DAX 函数还是自定义 UDF
- **维护成本**：一旦发生冲突后才重命名 UDF，就需要在整个模型中更新所有引用

使用复合名称（例如 `Finance.CalcProfit` 或 `My_CalcProfit`）可以让你的 UDF 与内置 DAX 函数明显区分开来。

## 此规则何时触发

当 UDF 名称既不包含句点也不包含下划线时，将触发此规则：

```csharp
not Name.Contains(".") and not Name.Contains("_")
```

## 如何修复

### 手动修复

1. 在 **TOM Explorer** 中找到该用户定义函数
2. 将其重命名，使名称包含命名空间分隔符（`.`）或下划线（`_`）
3. Tabular Editor 会在整个模型中自动更新所有引用

## 常见原因

### 原因 1：命名过于简单

该函数使用了一个普通名称，未考虑未来可能发生的冲突。

### 原因 2：从查询导入

该 UDF 应用于 DAX 查询的 DEFINE 部分，但未遵循命名空间约定。

## 示例

### 修复前

```dax
// 未使用命名空间分隔符命名的函数
FUNCTION CalcProfit =
    (
        revenue: DOUBLE,
        cost: DOUBLE
    )
    => revenue - cost
```

### 修复后

```dax
// 使用命名空间分隔符命名的函数
FUNCTION Finance.CalcProfit =
    (
        revenue: DOUBLE,
        cost: DOUBLE
    )
    => revenue - cost
```

## 兼容级别

这个规则适用于兼容级别为 **1702** 及以上的模型。

## 相关规则

- [DAX 用户自定义函数](xref:udfs)
- [内置 BPA 规则](xref:built-in-bpa-rules)
