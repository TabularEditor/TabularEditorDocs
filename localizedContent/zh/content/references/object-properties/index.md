---
uid: object-properties
title: 对象属性参考
author: Jeroen ter Heerdt
updated: 2026-10-05
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 对象属性参考

<!--
SUMMARY: Reference for every property that Tabular Editor shows in the Properties view, grouped by object type.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

语义模型中的每个对象，例如表、列或度量值，都有一组属性。这些属性来自 Tabular Object Model (TOM)，也就是 Analysis Services、Power BI 和 Fabric 用来定义语义模型的对象模型。这些属性会显示在 @properties-view 中；C# Script 可通过 @api-index 读取和写入这些属性。

这份参考介绍属性视图中显示的每项属性。如果 Tabular Editor 为某个属性提供了相关功能，例如编辑器、Best Practice Analyzer (BPA) 规则或 C# Script，对应条目会链接到该功能。

要更改属性，在 @tom-explorer-view 中选择一个或多个对象，然后在属性视图中编辑其值。当你选择多个对象时，新值将应用于它们全部。参见 @editing-properties。

## 这份参考的组织方式

@object-properties-common 介绍大多数对象共有的属性，例如 `Name`、`Description` 和 `Annotations`。其他每个页面各自介绍一类相关对象：

| 页面                                                    | 对象                                              |
| ----------------------------------------------------- | ----------------------------------------------- |
| @object-properties-common                | 大多数对象共有的属性                                      |
| @object-properties-model                 | 模型                                              |
| @object-properties-tables                | 表、计算表格、计算组表                                     |
| @object-properties-columns               | 数据列、计算列、计算表格列、替代对象、变体                           |
| @object-properties-measures              | 度量值、KPI                                         |
| @object-properties-calculation-groups    | 计算组、计算项                                         |
| @object-properties-hierarchies           | 层次结构、级别                                         |
| @object-properties-relationships         | 关系                                              |
| @object-properties-partitions            | 分区、M 分区、实体分区、策略范围分区、刷新策略、数据覆盖范围定义               |
| @object-properties-data-sources          | 提供程序数据源与 Structured数据源、共享表达式、Query Group、数据绑定提示 |
| @object-properties-security              | 角色、表格权限、角色成员                                    |
| @object-properties-perspectives-cultures | 透视、区域设置                                         |
| @object-properties-calendars             | 日历、时间相关列组、时间单位列关联                               |
| @object-properties-functions             | 用户自定义函数、集合                                      |

每个页面都会为每个对象设置一个部分。章节开头会列出指向该对象常见属性的链接，随后是每个属性对应的条目。对于每种对象，属性都会按类别列出，其顺序与在属性视图中选择 **分类** 时显示的顺序一致。类别包括：

- **基本**：最常修改的属性，例如名称、说明和格式字符串。
- **元数据**：对象的相关信息，例如对象类型或错误信息。这些属性大多为只读。
- **选项**：更改对象行为方式的属性，例如表达式、汇总方式或排序顺序。
- **翻译、透视、安全性**：按区域设置的翻译、透视成员关系以及按角色的安全设置。

某些对象还有其他类别，例如模型上的 **数据访问选项**。

每个条目的标题都是该属性在属性视图中显示的名称。标题下方一行显示该属性的 TOM 名称、类型和类别：

> **显示名称**
> `TomName` · 类型 · 类别

TOM 名称是在 C# Script 中使用的名称。对于少数属性，表格式模型定义语言 (TMDL) 会使用另一个名称，例如，TMDL 会将度量值的 `FormatStringExpression` 保存为 `formatStringDefinition`。

如果适用，这些部分会按以下顺序显示在类别后面：

- **只读**：你不能更改该值。
- **兼容级别 NNNN+**：模型所需的最低兼容级别，例如 `compatibility level 1540+`。
- 用于标识该属性是由 Tabular Editor 添加的。参见 [Tabular Editor 添加的属性](#properties-that-tabular-editor-adds)。

例如，Lineage tag 的条目开头如下：

> **Lineage tag**
> `LineageTag` · 字符串 · 选项 · 兼容级别 1540+

## 依赖于模型的属性

属性视图会隐藏不适用于当前模型的属性。显示哪些属性取决于：

- 模型的兼容级别。许多属性都要求最低兼容级别，例如 `LineageTag` 需要 1540 或更高的兼容级别。要查看或更改兼容级别，请选择模型，然后在属性视图中展开 `Database`。
- 模型的兼容模式。某些属性仅适用于 Power BI 和 Fabric 模型，或仅适用于 Analysis Services 模型。
- 对象的状态。某些属性仅在另一个属性具有特定值时才会显示。例如，只有当表具有刷新策略时，才会显示该刷新策略的属性。

## Tabular Editor 添加的属性

属性视图中的几乎每个属性都是 TOM 属性，会保存在模型中，并且对读取该模型的所有工具可见。 Tabular Editor 还会添加一些它自己的属性。元数据行会按以下方式标记它们：

| 标记          | 含义                                                                  | 是否保存在模型中？                      |
| ----------- | ------------------------------------------------------------------- | ------------------------------ |
| _计算得出_      | Tabular Editor 会计算该值以供显示，例如 `DaxObjectFullName` 或 `ObjectTypeName`。 | 否                              |
| _指向……的快捷方式_ | 显示或编辑另一个对象的 TOM 属性。例如，表上的 `SourceType` 会显示该表第一个分区的源类型。              | 是，会作为它所指向的 TOM 属性保存在模型中        |
| _存储为注释_     | Tabular Editor 会将该值作为对象上的注释保存，例如 `TableGroup`。                      | 是，保存为只有 Tabular Editor 才会读取的注释 |

## 另见

- @属性视图
- @tom-explorer-view
- @editing-properties
- @best-practice-analyzer
- @C# 脚本
- @api-index
