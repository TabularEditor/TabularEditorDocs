---
uid: kb.bpa-set-isavailableinmdx-true-necessary
title: 必要时将 IsAvailableInMDX 设置为 True
author: Morten Lønskov
updated: 2026-01-09
description: 一条最佳实践规则：通过确保用于层次结构和关系的列启用 MDX 可用性，防止查询错误。
---

# 必要时将 IsAvailableInMDX 设置为 True

## 概述

此最佳实践规则会识别那些将 `IsAvailableInMDX` 设为 `false`，但实际用于需要 MDX 访问场景的列。 这些列必须启用 MDX 可用性，才能在层次结构、关系和排序操作中正常工作。

- 类别：错误预防
- 严重性：高（3）

## 适用对象

- 数据列
- 计算列
- 计算表格列

## 为什么这很重要

当某列用于特定的模型结构时，Analysis Services 引擎需要通过 MDX 访问该列。 对需要 MDX 的列禁用 MDX 访问会导致：

- **查询失败**：层次结构和排序操作会失败并报错
- **可视化出错**：使用受影响层次结构的图表和表格会显示错误
- **关系问题**：针对关系的 MDX 查询可能失败
- **日历/变体错误**：时间智能功能会失效
- **行为不可预测**：某些查询能运行，另一些会失败，取决于客户端工具

当列满足以下情况时，需要 `IsAvailableInMDX = true`：

- 在层次结构中用作级别
- 作为“按此列排序”列被引用
- 用于变体（替代层级）
- 是日历定义的一部分
- 作为其他列的“按此列排序”目标列

## 该规则何时触发

当某列的 `IsAvailableInMDX = false` 且满足以下任一条件时，规则会触发：

```csharp
IsAvailableInMDX = false
and
(
    UsedInSortBy.Any()
    or
    UsedInHierarchies.Any()
    or
    UsedInVariations.Any()
    or
    UsedInCalendars.Any()
    or
    SortByColumn != null
)
```

这个规则会检查以下依赖集合：

| 属性                  | 说明             | 使用示例           |
| ------------------- | -------------- | -------------- |
| `UsedInHierarchies` | 该列作为层级级别时所属的层级 | 产品层级级别         |
| `UsedInSortBy`      | 使用该列作为排序键的列    | 按月份编号对月份名称进行排序 |
| `UsedInVariations`  | 使用该列的备用层级      | 产品变体           |
| `UsedInCalendars`   | 对日历元数据的引用      | 日期表的日历定义       |
| `SortByColumn`      | 该列按另一列排序       | 此列包含“按列排序”的引用  |

## 如何修复

### 自动修复

此规则包含一个自动修复：

```csharp
IsAvailableInMDX = true
```

应用步骤：

1. 在 **Best Practice Analyzer** 中选择被标记的对象
2. 点击 **Apply Fix**

### 手动修复

1. 在 **TOM Explorer** 中找到被标记的列
2. 在 **属性** 窗格中找到 `IsAvailableInMDX`
3. 将值设置为 `true`
4. 保存并测试受影响的层次结构和排序

## 常见场景

### 场景 1：层次结构级别列

**问题**：用作层次结构级别的列禁用了 MDX

```dax
Hierarchy: Geography
  Levels:
    - Country
    - State (IsAvailableInMDX = false)  ← 问题
    - City
```

**错误**："由于其中一个级别在 MDX 中不可用，无法使用层次结构 'Geography'。"

**解决方案**：将 `State[IsAvailableInMDX]` 设为 `true`

### 场景 2：排序依据列

**问题**：作为按列排序目标的列禁用了 MDX

```
Month Name column:
  - SortByColumn = MonthNumber
  - MonthNumber.IsAvailableInMDX = false  ← 问题
```

**错误**：月份按字母顺序显示，而不是按日历顺序

**解决方案**：将 `MonthNumber[IsAvailableInMDX]` 设为 `true`

### 场景 3：日历定义

**问题**：日历元数据中使用的日期列禁用了 MDX

```
DateTable:
  - Calendar 使用 DateKey 列
  - DateKey.IsAvailableInMDX = false  ← 问题
```

**错误**：时间智能函数失败

**解决方案**：将 `DateKey[IsAvailableInMDX] = true`

## 兼容级别

本规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [将 IsAvailableInMDX 设为 False](xref:kb.bpa-set-isavailableinmdx-false) — 配套的优化规则
