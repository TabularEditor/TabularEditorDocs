---
uid: user-context-calculated-columns
title: 用户上下文计算列
author: Morten Lønskov
updated: 2026-10-12
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

_用户上下文计算&#x5217;_&#x662F;指按用户分别进行计算的计算列。其表达式可以调用 [`USERPRINCIPALNAME`](https://dax.guide/userprincipalname) 或 [`USERNAME`](https://dax.guide/username) 等函数，并为每个用户返回不同的值。相比之下，标准计算列会在处理表时计算一次，并为所有用户返回相同的值。

计算列的 `ExpressionContext` 属性用于设置该列是只计算一次，还是按用户分别计算：

| 表达式上下文    | 含义                                   |
| --------- | ------------------------------------ |
| **标准**    | 默认选项。表达式只能使用标准函数。对所有用户来说，该列每一行的值都相同。 |
| **用户上下文** | 表达式可以调用用户上下文函数。该列按用户分别计算。            |

在 @tom-explorer-view 中选择一个计算列，然后在 @properties-view 的 **选项** 下设置 **表达式上下文**。

> [!NOTE]
> `ExpressionContext` 需要兼容级别 1705 或更高；在 1705 以下，计算列始终为 **Standard**。

## 用户上下文计算列不能用于哪些场景

在整个模型中只计算一次的对象不能引用用户上下文计算列。对于以下每种情况，Tabular Editor 的语义分析器都会报告错误：

| 用户上下文计算列不能被以下对象引用 | 信息                                                   |
| ----------------- | ---------------------------------------------------- |
| 标准计算列             | "此表达式引用了用户上下文计算列 `Table[Column]`，而这在标准计算列中是不允许的。"    |
| 计算表格              | "此表达式引用了用户上下文计算列 `Table[Column]`，而这在计算表格中是不允许的。"     |
| 行级安全性筛选器          | "此表达式引用了用户上下文计算列 `Table[Column]`，而这在行级安全性筛选器中是不允许的。" |
| 作为端点的关系           | "关系不能将用户上下文计算列 `Table[Column]` 作为端点。"                |

前三条规则也适用于间接引用，例如通过度量值进行引用。度量值和其他用户上下文计算列可以引用用户上下文计算列。

## 错误显示位置

| 列的引用方式       | DAX 编辑器 | @信息视图 | [`te validate`](xref:te-cli-commands#validate) |
| ------------ | ------- | ------------------ | ---------------------------------------------- |
| 直接           | 是的      | 是的                 | 是的                                             |
| 间接引用，例如通过度量值 | 否       | 是的                 | 是的                                             |
| 作为关系端点       | 否       | 是的                 | 是的                                             |

DAX 编辑器不会为间接违规加下划线，因此部署前请先在 @信息视图 中检查这些问题。

关系端点违规也会显示在该关系的 **错误信息** 属性中。无论是活动关系还是非活动关系都会被检查，错误会按端点分别进行 Report；因此如果某个关系两端都包含用户上下文列，就会报出两个错误。

> [!NOTE]
> `te validate --errors-only` 仍会 Report 这些违规，因为该选项只会隐藏警告和反模式。

## 后续步骤

- @信息视图
- @dax-editor
- @偏好
