---
uid: semantic-bridge-metric-view-fields-and-dimensions
title: Metric View 中的字段与维度
author: Greg Baldini
updated: 2026-06-25
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.26.2
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Metric View 中的字段与维度

<!--
SUMMARY: Explains the Databricks Metric View `dimensions` -> `fields` keyword rename and the
matching Semantic Bridge C# API rename (Dimension -> Field): what changed, that the old names
still work, migration guidance, and what Tabular Editor emits on round-trip.
-->

在 2026 年春季，Metric View 规范将 Metric View YAML 规范中的一个规范顶层键从 `dimensions`（现已弃用）改为 `fields`。
两者都指 Metric View 中可供查询的列集合——这些列既可以是对源列的直接引用，也可以由 SQL 表达式定义。
[文档指出，应优先使用 `fields`，但这两个术语都仍然有效](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#dimensions)。
我们已更新 Semantic Bridge 中的 Metric View 对象模型，以与之保持一致。
根据 Metric View 规范，序列化和反序列化仍支持使用任一键。
我们在对象模型中为旧版与“dimension”关联的名称提供向后兼容的适配层。
在 C# Script 中使用该对象模型的用户，应在条件允许时迁移到与“field”关联的名称。

**影响范围**：手动编写 Metric View YAML 的任何人，以及在 Tabular Editor 中通过 C# Script 使用 Metric View 对象模型的任何人。

## 版本管理

此更改是在 v1.1 规范发布后发生的，而且没有新的规范版本。
因此，我们在 Semantic Bridge 中采取了较为保守的处理方式。
对于 v0.1 和 v1.1 的 Metric View，我们默认使用 `dimensions`。
未来，对于任何更新版本的 Metric View，我们都将默认使用 `fields`。
这样做是出于谨慎考虑，也为了尽可能与其他可能尚未跟上最新已发布 Metric View 规范的工具保持互操作性。

## 序列化与反序列化

根据 [Metric View 文档](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#dimensions)，这两个键在序列化时仍然有效。

| YAML 源中使用的键  | 版本                                            | 反序列化是否成功 | 反序列化时是否发出警告  | 重新序列化时使用的键 |
| ------------ | --------------------------------------------- | -------- | ------------ | ---------- |
| `fields`     | <1.1 | 是        | 是            | `fields`   |
| `dimensions` | <1.1 | 是        | 否            | `维度`       |
| 两者都不是        | <1.1 | 是        | 否            | `维度`       |
| `字段`         | 1.1                           | 是        | 否            | `字段`       |
| `维度`         | 1.1                           | 是        | 是            | `维度`       |
| 两者都不是        | 1.1                           | 是        | 否            | `维度`       |
| `字段`         | > 1.1                         | 是        | 否            | `字段`       |
| `维度`         | > 1.1                         | 是        | 是            | `维度`       |
| 两者都没有        | > 1.1                         | 是        | 否            | `字段`       |
| 两者都有         | 任意                                            | 否        | 是（错误，反序列化失败） | 不适用，反序列化失败 |

我们将继续在所有 Metric View 版本中支持这两个关键字，除非未来的规范更新另有说明。
你可以继续按自己的偏好自由使用任意一个，但请注意上文中关于序列化和反序列化的警告及默认行为。

你可能会注意到：在 v1.1 的 Metric View 中，我们会对 `dimensions` 发出警告；同时，如果同一 v1.1 中两者都未提供，我们会默认选择 `dimensions`。
这是我们较为保守的默认选择，因为在 1.1 版本中期才将 `fields` 引入为首选项。
该警告与 Metric View 文档一致，文档指出应将 `fields` 视为默认项。
将 `dimensions` 设为默认值，是为了与其他可能仅面向最初发布时 v1.1 规范的工具保持互操作性。

如果一个定义中同时包含这两个键，我们会将其视为错误，并且会导致此类 Metric View 反序列化失败。
据我们所知，除了手动编辑 YAML 之外，没有其他方式会产生这种情况；你当然也不可能通过 Semantic Bridge 或我们提供的任何操作无意间造成这种情况。
这种同时使用 `dimensions` 和 `fields` 的 Metric View 定义需要手动处理。

关于 Metric View YAML 定义中的 `materialization` 块，有一个重要说明：无论顶层使用哪个键，这一 YAML 部分仍然只使用 `dimensions`。
[查看有关 materialization 的文档，获取权威指导](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#materialization)。

最后，使用 `dimensions` 或 `fields` 在行为或语义上都没有区别。
这些关键字只是同义词，不过建议优先使用 `fields`。

## Metric View 对象模型 API 变更：`Dimension` 改为 `Field`

鉴于建议优先使用 `fields`，我们已在整个 Semantic Bridge 中统一采用这一用法。
我们提供了一个[Metric View 对象模型，用于以编程方式与 Metric View 交互](xref:semantic-bridge-metric-view-object-model)，这是在 Semantic Bridge 中实现这些翻译所必需的。
我们已弃用 `Dimension` 对象，以及所有名称中使用了“dimension”或“dimensions”的相关方法和属性。
我们创建了新的 `Field` 对象，以及新的以“field”命名的方法和属性。
`Dimension` 对象及其相关方法和属性现在会发出已过时的警告。
所有基于 `Dimension` 的代码仍可正常运行，但在经过一段适当的时间后，我们可能会将其移除。
与 Databricks 一样，我们建议你在所有新开发中使用 `Field` 及其相关方法。

在实现层面，所有基于 `Dimension` 的代码都会转发到基于 `Field` 的实现，或与其实现保持一致。
虽然我们建议使用 `Field`，但两者可以互换使用。
总体而言，从 `Dimension` 迁移到 `Field` 应当是透明的。

技术说明：[`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) 是 `Field` 的子类。
因此，你可能会观察到 `Field` 和 `Dimension` 代码之间存在一些差异，不过也有合理的变通方法。
如果希望代码在 `Dimension` 被移除后仍能继续运行，请针对 `Field` 进行分支并声明；切勿直接命名或测试具体的 `Dimension` 类型。 给定一个字段 `f`：

| 避免使用                                                             | 改用                                                     | 为什么在移除 `Dimension` 后会失效                              |
| ---------------------------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------- |
| `f is Dimension`                                                 | `f is Field`                                           | `Dimension` 将无法通过编译；而 `is Field` 在移除前后都为 true        |
| `f is Dimension x`                                               | `f is Field x`                                         | 相同                                                   |
| `case Dimension x:`                                              | `case Field x:`                                        | 相同                                                   |
| `(Dimension)f`, `f as Dimension`                                 | 直接将 `f` 当作 `Field` 使用（无需强制转换）                          | 强制转换的目标类型消失了；`f` 已经是 `Field`                         |
| `f.GetType() == typeof(Dimension)`                               | `f is Field`                                           | `typeof(Dimension)` 将无法通过编译                          |
| `f.GetType() == typeof(Field)`                                   | `f is Field`                                           | 现在为 false（运行时类型是 `Dimension`），之后为 true，因此会在不知不觉中发生翻转 |
| `f.GetType().Name == "Dimension"`（或 `== "Field"`）                | `f is Field`；如需标签，使用 `f.ToString()` 或 `f.Name`         | 类型名字符串现在是 `"Dimension"`，之后是 `"Field"`                |
| `Dimension x = ...`, `List<Dimension>`, `IEnumerable<Dimension>` | `Field x = ...`, `view.Fields`, `IReadOnlyList<Field>` | `Dimension` 类型名不再存在                                  |
| `typeof(Dimension)`, `nameof(Dimension)`                         | `typeof(Field)`, `nameof(Field)`                       | `Dimension` 符号已被移除                                   |
| `MakeValidationRule<MetricView.Dimension>(...)`                  | `MakeValidationRule<MetricView.Field>(...)`            | 该类型参数引用了已移除的类型                                       |

> [!NOTE]
> 对象模型中 `Dimension` 类型的弃用，以及未来可能移除该类型及其相关方法，都不会影响使用任一 YAML 关键字进行序列化或反序列化。

## 名称对照：从 `Dimension` 到 `Field`

下表列出了每个已弃用的 `Dimension` 名称，以及对应的规范 `Field` 替代名称。 旧名称仍可编译（但会出现过时警告），且行为完全一致；新脚本中优先使用规范名称。

| 旧名称（已弃用）                                                        | 规范名称                                                        | 适用范围                                 |
| --------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------ |
| `MetricView.Dimension`（类型）                                      | `MetricView.Field`（类型）                                      | 对象模型                                 |
| `view.Dimensions`                                               | `view.Fields`                                               | `View` 集合                            |
| `view.Dimensions["name"]`                                       | `view.Fields["name"]`                                       | 在集合中按名称索引                            |
| `view.AddDimension(name, expr)`                                 | `view.AddField(name, expr)`                                 | `View` 方法                            |
| `SemanticBridge.MetricView.MakeValidationRuleForDimension(...)` | `SemanticBridge.MetricView.MakeValidationRuleForField(...)` | 验证规则辅助方法（两个重载版本，分别带和不带 `minVersion`） |
| `context.DimensionNames`                                        | `context.FieldNames`                                        | 传递给验证规则的上下文                          |

## 相关内容

- @semantic-bridge
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- [Metric View API](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
