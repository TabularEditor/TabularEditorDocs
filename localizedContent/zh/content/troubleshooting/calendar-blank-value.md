---
uid: calendar-blank-value
title: Calendar 函数日期为空的错误
author: Morten Lønskov
updated: 2025-10-20
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# Calendar 函数日期为空的错误

## 概述

在 **Tabular Editor 3 (TE3)** 中刷新模型时可能会出现这个错误，即使受影响的表并未直接引用 `CALENDAR()` 函数。 这通常表示某个依赖的日期表或日历表依赖其他表中的值，而这些表在刷新过程中会暂时为空，导致开始日期或结束日期的值为空白。

## 症状

- 在 Tabular Editor 3 中刷新模型失败，错误为：

  ```
  Calendar 函数中的开始日期或结束日期不能为“空白”值。
  ```

- 同一模型或表在 Power BI Desktop 或 Power BI Service 中可以成功刷新。

- 使用新名称重新导入该表（例如 _TableName 1_）可暂时成功。

- 受影响表的 M 表达式看起来很简单且有效：

  ```m
  let
    Source = <DataSource>,
    Data = Source{[Schema=SchemaVar,Item="TableX"]}[Data]
  in
    Data
  ```

## 原因

虽然这个错误看起来与正在刷新的表无关，但通常源自模型中的下游依赖项。

例如，日期表或日历表可能会基于多个事务表中的最小日期和最大日期，动态定义其范围：

```dax
CALENDAR(
  MINX(UNION(TableA, TableB, TableC), [Date]),
  MAXX(UNION(TableA, TableB, TableC), [Date])
)
```

如果其中一个或多个源表为空，`MINX` 或 `MAXX` 表达式会返回空白值，从而导致 `CALENDAR()` 函数失败。

## 解决步骤

1. **识别依赖表**
   - 在 Tabular Editor 3 中使用 **Dependencies** 视图，找出引用其他表日期字段的 Date 或 Calendar 表。
2. **检查空表**
   - 确认所有被引用的表都包含数据。 如果源表为空，请刷新数据源或调整架构变量配置。
3. **添加默认兜底值**
   - 为避免边界为空，请用 `COALESCE()` 包裹表达式，或指定默认日期值：

     ```dax
     CALENDAR(
       COALESCE(MINX(...), DATE(2000,1,1)),
       COALESCE(MAXX(...), TODAY())
     )
     ```
4. **重新处理模型**
   - 在应用修复或更新数据后，在 Tabular Editor 3 中重新处理受影响的表。

## 补充说明

> [!NOTE]
> 此问题可能在 M 脚本中引入架构变量时出现，例如使用变量来定义架构名称（如 `SchemaVar`）。