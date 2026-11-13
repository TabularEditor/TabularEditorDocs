---
uid: user-context-calculated-columns
title: 用户上下文计算列
author: Morten Lønskov
updated: 2026-10-26
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# 用户上下文计算列

*用户上下文计算列*是按用户进行评估的计算列。其表达式可以调用 [`USERPRINCIPALNAME`](https://dax.guide/userprincipalname) 或 [`USERNAME`](https://dax.guide/username) 等函数，并为每个用户返回不同的值。相比之下，标准计算列在处理表格时仅评估一次，并为所有用户返回相同的值。

计算列的 `ExpressionContext` 属性用于设置该列是评估一次还是针对每个用户进行评估：

| 表达式上下文 | 含义 |
|---|---|
| `Standard` | 默认值。表达式只能使用标准函数。对于所有用户，该列每行都有一个值。|
| `UserContext` | 表达式可以调用用户上下文函数。该列按每位用户进行评估。|

在 @tom-explorer-view 中选择一个计算列，然后在 @properties-view 的**选项**下设置**表达式上下文**。

> [!NOTE]
> `ExpressionContext` 需要兼容级别 1705 或更高，低于 1705 的计算列始终为 `Standard`。

## Direct Lake on OneLake 表

`UserContext` 是 Power BI 对 Direct Lake on OneLake 表上的计算列支持的唯一表达式上下文。当您将模型保存到 Power BI 服务时，如果 Direct Lake 表上的计算列设置为`Standard`，则保存将失败，并显示错误“默认表达式上下文不能用于 Direct Lake 表中的计算列”。Direct Lake on SQL 表不支持计算列。有关在 Direct Lake 模型上设置表达式上下文的步骤，请参阅[Direct Lake on OneLake 上的计算列](xref:direct-lake-guidance#calculated-columns-on-direct-lake-on-onelake)。

## 用户上下文列不能用于哪些情况

针对整个模型计算一次的对象无法引用用户上下文计算列。对于以下每种情况，Tabular Editor 语义分析器都会报告错误：

| 用户上下文列不能被以下项引用 | 消息 |
|---|---|
| 标准计算列 | “此表达式引用了支持用户上下文的计算列 `Table[Column]`，标准计算列中不允许引用该列。” |
| 计算表格 | “此表达式引用了支持用户上下文的计算列 `Table[Column]`，计算表格中不允许引用该列。” |
| 行级安全性筛选器 | “此表达式引用了支持用户上下文的计算列 `Table[Column]`，行级安全性筛选器中不允许引用该列。” |
| 关系，作为端点 | “关系不能将支持用户上下文的计算列 `Table[Column]` 用作端点。” |

前三条规则也适用于间接引用，例如通过度量值进行的引用。度量和其他用户上下文计算列可以引用用户上下文列。

## 错误出现的位置

| 列的引用方式 | DAX 编辑器 | @messages-view | [`te validate`](xref:te-cli-commands#validate) |
|---|---|---|---|
| 直接 | 是 | 是 | 是 |
| 间接引用，例如通过度量值引用 | 否 | 是 | 是 |
| 作为关系端点 | 否 | 是 | 是 |

DAX 编辑器不会对间接违规加下划线，因此请在部署前在 @messages-view 中检查这些违规。

关系端点违规也会显示在关系的**错误消息**属性中。系统会检查活动关系和非活动关系，并针对每个端点报告错误，因此，如果关系的两端都有用户上下文列，则会有两个错误。

> [!NOTE]
> `te validate --errors-only` 仍会报告这些违规情况，因为该选项仅隐藏警告和反模式。

## 后续步骤

- @messages-view
- @dax-editor
- @preferences
