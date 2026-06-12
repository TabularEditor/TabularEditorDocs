---
uid: kb.bpa-date-table-exists
title: 应包含日期表
author: Morten Lønskov
updated: 2026-01-09
description: 最佳做法规则：确保你的模型包含专用日期表，以便时间智能功能正常运行。
---

# 应包含日期表

## 概述

此最佳做法规则会验证你的表格模型是否包含至少一个已正确配置的日期表。 日期表对于时间智能计算至关重要，并确保整个模型中基于日期的筛选一致性。 日期表对于时间智能计算至关重要，并确保整个模型中基于日期的筛选一致性。

- 类别：性能

- 严重性：中（2）

## 适用于

- 模型

## 为什么这很重要

专用日期表至关重要，因为它可以：

- **启用时间智能**：`DATESYTD`、`SAMEPERIODLASTYEAR` 和 `TOTALYTD` 等函数需要日期表
- **确保筛选一致**：为日期属性提供单一可信来源
- **提升性能**：建立正确的日历关系
- **支持自定义日历**：支持财年计算和自定义层次结构

如果没有正确标记的日期表，许多 DAX 时间智能函数会失效或产生不正确的结果。

## 此规则何时触发

当模型中的**所有**表都满足以下条件时，将触发此规则：

1. 没有任何表定义日历（`Calendars.Count = 0`）
2. 没有任何表包含标记为键且 `DataType = DateTime` 的列
3. 没有任何表的 `DataCategory = "Time"`

这表示模型缺少合适的日期维度。

## 如何修复

### 选项 1：使用 DAX 创建日期表

添加一个涵盖完整日期范围的计算表格：

```dax
DateTable = 
ADDCOLUMNS (
    CALENDAR (DATE(2020, 1, 1), DATE(2030, 12, 31)),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "Month", FORMAT([Date], "MMMM"),
    "MonthNumber", MONTH([Date]),
    "Day", DAY([Date]),
    "WeekDay", FORMAT([Date], "dddd")
)
```

### 选项 2：从数据源导入

在数据仓库或数据源中创建日期维度表，并将其导入模型。

### 标记为日期表格

创建该表后：

1. 在 **TOM Explorer** 中选择日期表
2. 右键单击，然后选择 **标记为日期表格**
3. 选择日期列作为键列
4. 在日期表和事实表之间创建关系

### 设置日历元数据

或者，配置日历元数据：

1. 选择日期表
2. 在 **属性** 窗格中，展开 **日历**
3. 添加一个新日历，并配置日期列引用

## 示例

典型的日期表结构：

| 日期         | 年份   | 季度 | 月份 | 月份编号 | 日  |
| ---------- | ---- | -- | -- | ---- | -- |
| 2025-01-01 | 2025 | Q1 | 一月 | 1    | 1  |
| 2025-01-02 | 2025 | Q1 | 一月 | 1    | 2  |
| ……         | ……   | …… | …… | ……   | …… |

创建完成后，建立以下关系：

```
'DateTable'[Date] (1) -> (*) 'Sales'[OrderDate]
'DateTable'[Date] (1) -> (*) 'Orders'[ShipDate]
```

## 兼容级别

这个规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [删除自动日期表](xref:kb.bpa-remove-auto-date-table) - 删除与现有功能重复的自动日期表

## 了解更多

- [在 Power BI 中创建日期表](https://learn.microsoft.com/power-bi/guidance/model-date-tables)
- [DAX 中的时间智能函数](https://learn.microsoft.com/dax/time-intelligence-functions-dax)
- [标记为日期表格](https://learn.microsoft.com/power-bi/transform-model/desktop-date-tables)
