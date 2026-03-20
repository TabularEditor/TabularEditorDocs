---
uid: kb.bpa-set-isavailableinmdx-false
title: 将 IsAvailableInMDX 设置为 False
author: Morten Lønskov
updated: 2026-01-09
description: 最佳实践规则：对未用于关系或层次结构的隐藏列禁用 MDX 访问，以优化性能。
---

# 将 IsAvailableInMDX 设置为 False

## 概览

此最佳实践规则用于识别已隐藏但 `IsAvailableInMDX` 属性仍设置为 `true`、且无需通过 MDX 查询访问的列。 对未使用的隐藏列将该属性设置为 `false`，可提升查询性能并降低内存开销。

- 类别：性能
- 严重性：中（2）

## 适用对象

- 数据列
- 计算列
- 计算表格列

## 为什么重要

当某列的 `IsAvailableInMDX` 设置为 `true` 时，Analysis Services 引擎会维护额外的元数据和结构，以支持针对该列的 MDX 查询。 对于未用于关系、层次结构、变体、日历，或未用作“按列排序”列的隐藏列，这类开销没有必要，并可能导致：

- 增加内存消耗
- 降低查询处理速度
- 增加模型元数据的复杂度

对这些列显式地将 `IsAvailableInMDX` 设置为 `false`，即可针对仅使用 DAX 的场景优化模型；而 DAX 是 Power BI 和现代 Analysis Services 模型的主要查询语言。

> [!WARNING]
> **Excel 数据透视表兼容性**：将 `IsAvailableInMDX` 设为 `false` 会导致无法将列拖到 Excel 数据透视表的“行”或“列”区域。 Excel 数据透视表在连接到 Analysis Services 表格模型时会生成 MDX 查询，并且需要属性层次结构（仅在 `IsAvailableInMDX = true` 时才会构建）才能正常工作。 如果你的用户需要使用 Excel 数据透视表或其他基于 MDX 的工具来分析数据，请**不要**将此规则应用到他们需要访问的列。 更多详细信息，请参阅 [Chris Webb 关于 IsAvailableInMDX 的文章](https://blog.crossjoin.co.uk/2018/07/02/isavailableinmdx-ssas-tabular/)。

## 何时触发此规则

当满足以下所有条件时，此规则会触发：

1. 该列的 `IsAvailableInMDX = true`
2. 该列已隐藏（或其所属表已隐藏）
3. 该列未用于任何 `SortBy` 关系
4. 该列未用于任何层次结构
5. 该列未用于任何变体
6. 该列未用于任何日历
7. 该列未作为其他列的 `SortByColumn` 使用

## 如何修复

### 自动修复

此规则包含一条自动修复表达式。 当您在 Best Practice Analyzer 中应用此修复时：

```csharp
IsAvailableInMDX = false
```

应用步骤：

1. 在 **Best Practice Analyzer** 中选择被标记的对象
2. 单击 **Apply Fix**

### 手动修复

1. 在 **TOM Explorer** 中，找到被标记的列
2. 在 **Properties** 窗格中，找到 `IsAvailableInMDX` 属性
3. 将值设置为 `false`
4. 保存更改

## 示例

考虑一个仅用于中间计算的隐藏计算列：

```dax
_TempCalculation = 
CALCULATE(
    SUM('Sales'[Amount]),
    ALLEXCEPT('Sales', 'Sales'[ProductKey])
)
```

如果该列满足以下条件：

- 在客户端工具中隐藏
- 未用于任何层次结构或关系
- 未在排序操作中引用

因此，建议将 `IsAvailableInMDX` 设为 `false`，以获得最佳性能。

## 兼容级别

此规则适用于兼容级别为 **1200** 及更高的模型。

## 相关规则

- [必要时将 IsAvailableInMDX 设为 True](xref:kb.bpa-set-isavailableinmdx-true-necessary) - 互补规则，用于确保需要通过 MDX 访问的列已启用该功能
