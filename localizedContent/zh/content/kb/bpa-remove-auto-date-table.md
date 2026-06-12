---
uid: kb.bpa-remove-auto-date-table
title: 移除自动日期表
author: Morten Lønskov
updated: 2026-01-09
description: 用于识别并移除会增大模型体积、降低性能的自动生成日期表的最佳实践规则。
---

# 移除自动日期表

## 概述

此最佳实践规则用于识别由 Power BI Desktop 自动生成的日期表。 应移除这些自动生成的表（`DateTableTemplate_` 和 `LocalDateTable_`），改用一个明确、统一的日期表，以优化模型大小和性能。 应移除这些自动生成的表（`DateTableTemplate_` 和 `LocalDateTable_`），改用一个明确、统一的日期表，以优化模型大小和性能。

- 类别：性能

- 严重性：中（2）

## 适用范围

- 表
- 计算表格

## 为什么这很重要

当启用“自动日期/时间”时，Power BI 会为每个日期/日期时间列自动创建隐藏的日期表。 这会带来以下问题： 这会带来以下问题：

- **模型大小增加**：每个自动生成的表都会添加不必要的数据
- **内存开销增加**：多个日期表比共享同一个日期表占用更多内存
- **刷新更慢**：额外的表会增加刷新耗时

使用一个设计良好的日期表会更高效，也更易于维护。

## 此规则何时触发

当规则发现名称符合以下条件的计算表格时会触发：

- 以 `"DateTableTemplate_"` 开头，或
- 以 `"LocalDateTable_"` 开头

这些前缀表示这些日期表是由 Power BI 自动生成的。

## 如何修复

### 手动修复

1. 在 Power BI Desktop 中禁用 **自动日期/时间**（**文件** > **选项** > **数据加载**）
2. 创建一个专用的日期表。
3. 将其标记为日期表，并与事实表建立关系
4. 在 **TOM Explorer** 中删除以 `DateTableTemplate_` 或 `LocalDateTable_` 开头的表
5. 验证自定义日期表关系是否正常工作

## 常见原因

### 原因 1：启用了自动日期/时间功能

Power BI Desktop 的“自动日期/时间”功能会自动创建这些表格。

### 原因 2：迁移过来的模型

这些模型是在启用自动日期表的情况下创建的，之后从未清理过。

### 原因 3：默认设置

新模型会使用默认设置，从而启用自动日期表。

## 示例

### 修复前

```
表格：
  - Sales
  - LocalDateTable_OrderDate（隐藏，自动生成）
  - LocalDateTable_ShipDate（隐藏，自动生成）
  - Products
  - LocalDateTable_ReleaseDate（隐藏，自动生成）
```

**结果**：多个隐藏表会导致模型体积膨胀

### 修复后

```
表格：
  - Sales
  - Products
  - DateTable（显式创建，标记为日期表格）
    -> 与 Sales[OrderDate]、Sales[ShipDate]、Products[ReleaseDate] 建立关系
```

**结果**：一个高效的日期表即可支撑所有日期关系

## 兼容级别

这个规则适用于兼容级别 **1200** 及更高的模型。

## 相关规则

- [应存在日期表](xref:kb.bpa-date-table-exists) - 确保存在合适的日期表

## 了解更多

- [在 Power BI 中禁用自动日期/时间](https://learn.microsoft.com/power-bi/guidance/auto-date-time)
- [创建日期表](https://learn.microsoft.com/power-bi/guidance/model-date-tables)
- [日期表最佳实践](https://www.sqlbi.com/articles/creating-a-simple-date-table-in-dax/)
