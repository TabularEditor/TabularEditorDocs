---
uid: kb.bpa-format-string-measures
title: 为度量值提供格式字符串
author: Morten Lønskov
updated: 2026-01-09
description: 最佳实践规则：确保可见的度量值设置了合适的格式字符串，以实现一致的显示效果。
---

# 为度量值提供格式字符串

## 概览

此最佳实践规则用于识别数据类型为数值或日期、但缺少格式字符串的可见度量值。 All measures should have explicit format strings for professional, consistent display.

- 类别：格式化

- 严重级别：中等（2）

## 适用于

- 度量值

## 为何这很重要

没有格式字符串的度量值会显示原始值，容易让用户困惑，并导致 Report 展示不一致。 Format strings ensure:

- **专业呈现**：以恰当的货币、百分比或数字格式显示数值
- **一致性**：所有 Report 都以相同格式显示数值
- **用户信心**：格式正确的数字更易阅读和理解
- **符合公司规范**：格式符合企业标准

## 此规则何时触发

```csharp
IsVisible
and string.IsNullOrWhitespace(FormatString)
and (DataType = "Int64" or DataType = "DateTime" or DataType = "Double" or DataType = "Decimal")
```

## 如何修复

### 手动修复

1. 在 **TOM Explorer** 中选择该度量值
2. 在 **属性** 窗格中，找到 **格式字符串** 字段
3. 根据该度量值的计算内容，输入合适的格式字符串
4. 保存更改

### 常见格式模式

```dax
Total Revenue = 
SUM('Sales'[Amount])
// Format String: "$#,0"

Average Price = 
AVERAGE('Sales'[UnitPrice])
// Format String: "$#,0.00"

YoY Growth = 
DIVIDE([This Year] - [Last Year], [Last Year], 0)
// Format String: "0.0%"

Order Count = 
COUNTROWS('Orders')
// Format String: "#,0"
```

## 常见原因

### 原因 1：缺少格式定义

创建新的度量值时，默认不会设置任何格式字符串。

### 原因 2：从计算列复制/粘贴

从不需要格式字符串的计算列中复制/粘贴度量值。

## 示例

### 修复前

```dax
Total Revenue = SUM('Sales'[Amount])
// No Format String
```

**显示**：1234567.89（难以阅读，没有货币符号）

### 修复后

```dax
Total Revenue = SUM('Sales'[Amount])
// Format String: "$#,0"
```

**显示**：$1,234,568（清晰、专业的格式）

## 兼容级别

该规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [列的格式字符串](xref:kb.bpa-format-string-columns)——针对列的类似验证
