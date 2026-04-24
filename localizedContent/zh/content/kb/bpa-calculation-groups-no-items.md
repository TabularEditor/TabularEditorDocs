---
uid: kb.bpa-calculation-groups-no-items
title: 计算组应包含计算项
author: Morten Lønskov
updated: 2026-01-09
description: 此最佳做法规则用于识别未包含任何计算项的计算组，这类计算组应补充内容或移除。
---

# 计算组应包含计算项

## 概览

此最佳做法规则会识别不包含任何计算项的计算组。 空的计算组没有实际作用，应补充计算项或直接移除。 空的计算组没有实际作用，应补充计算项或直接移除。

- 类别：维护
- 严重性：中等（2）

## 适用对象

- 计算组

## 为什么重要

- **部署错误**：空计算组可能无法通过 Power BI Service 的验证
- **模型错误**：可能导致 DAX 计算出现非预期行为
- **开发人员困惑**：团队成员会浪费时间排查不完整的结构
- **性能开销**：引擎会处理不必要的元数据

## 此规则何时触发

当计算组中的计算项数量为零时，此规则会触发：

```csharp
CalculationItems.Count == 0
```

## 如何修复

### 选项 1：添加计算项

如果该计算组确有业务用途：

1. 在 **TOM Explorer** 中展开计算组表
2. 展开 **计算组** 列
3. 右键单击并选择 **添加计算项**
4. 定义计算项表达式

### 选项 2：删除计算组

如果不再需要，请执行以下操作：

1. 在 **TOM Explorer** 中，定位到计算组表
2. 右键单击该表
3. 选择 **删除**

## 常见原因

### 原因 1：开发未完成

计算组在规划阶段创建，但尚未实现。

### 原因 2：从其他模型迁移

仅复制了计算组结构，但未包含任何计算项。

### 原因 3：重构

所有计算项已移动到另一个计算组。

## 示例

### 修复前

```
计算组：时间智能
  计算项：(无)  ← 问题
```

### 修复后

```
计算组：时间智能
  计算项：
    - 当前期间：SELECTEDMEASURE()
    - 年初至今：CALCULATE(SELECTEDMEASURE(), DATESYTD('Date'[Date]))
    - 去年同期：CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
```

## 兼容级别

此规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [透视应包含对象](xref:kb.bpa-perspectives-no-objects) —— 针对空透视的类似规则
- [必须提供表达式](xref:kb.bpa-expression-required) —— 确保计算项包含表达式

## 了解更多

- [表格模型中的计算组](https://learn.microsoft.com/analysis-services/tabular-models/calculation-groups)
- [创建计算组](https://www.sqlbi.com/articles/introducing-calculation-groups/)
- [计算组模式](https://www.sqlbi.com/calculation-groups/)
