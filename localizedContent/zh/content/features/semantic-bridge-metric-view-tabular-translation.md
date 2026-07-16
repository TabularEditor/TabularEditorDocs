---
uid: semantic-bridge-metric-view-tabular-翻译
title: 从 Metric View 到 Tabular 的翻译
author: Greg Baldini
updated: 2026-06-30
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# 从 Metric View 到 Tabular 的翻译

<!--
SUMMARY: Describes the process and specifics of translating a Metric View to a TOM model.
-->

> [!NOTE]
> Semantic Bridge 目前处于公共预览阶段。
> 3.25.0 版本支持 Metric View v0.1 元数据，3.26.2 版本支持 Metric View v1.1 元数据。
> 相关限制如下。

本页介绍在将 Metric View 定义导入 Tabular 模型时，翻译机制如何运作。

## 翻译过程

将 Metric View 翻译为 Tabular 模型分为几个步骤：

1. 从磁盘读取 YAML 文件
2. 对 YAML 进行反序列化
3. 验证反序列化后的 YAML 是否为有效的 Metric View
4. 如果它是有效的 Metric View，就将其保存为当前加载的 Metric View，就像你与已加载的 Tabular 模型交互一样。
   如果它不是有效的 Metric View，流程会在此停止，并提供诊断信息。
5. 分析 Metric View，并尝试将其转换为一种中间表示
6. 尝试将中间表示转换为 Tabular 模型

导入 GUI 会替你处理这一切。不过，你也可以使用 C# Script 来自定义流程中的不同步骤，并以编程方式操作 Metric View，就像你平时操作 Tabular 模型一样。
具体来说，你可以

- 使用 [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) 从磁盘加载 Metric View：加载后可在 C# Script 中通过 [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model) 访问，但不会将结构导入 Tabular 模型
- 使用 [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A) 从字符串反序列化 Metric View：与加载类似，模型可通过 [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model) 访问，但不会导入到 Tabular 模型中
- 使用 [`SemanticBridge.MetricView.Save`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Save%2A) 将 Metric View 保存到磁盘
- 使用 [`SemanticBridge.MetricView.Serialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Serialize%2A) 将 Metric View 序列化为字符串。
- 使用与 [Best Practice Analyzer](xref:best-practice-analyzer) 类似的系统，通过 [`SemanticBridge.MetricView.Validate`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate%2A) 验证 Metric View
  - 你可以使用 [`SemanticBridge.MetricView.MakeValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRule%2A) 及其更简化的版本创建你自己的验证规则
- 使用 [`SemanticBridge.MetricView.ImportToTabularFromFile`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.ImportToTabularFromFile%2A) 将 Metric View 导入 Tabular，它执行的操作与导入 GUI 完全相同；或者使用 [`SemanticBridge.MetricView.ImportToTabular`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.ImportToTabular%2A)，其方式类似，但它作用于当前已加载的 Metric View，而不是从磁盘读取。

### 按对象的翻译说明

下面这四项：`View`、`Join`、`Field` 和 `Measure`，是 Metric View 定义中的核心对象，最终会成为 TOM 对象。
Metric View 定义中的其他元数据要么会被忽略，要么会影响这些对象的具体翻译方式。

> [!NOTE]
> 本文的翻译以 Metric View 对象模型为基础，因此下文将一律以该术语体系进行说明。
> 有关对象模型的详细信息，以及它与 YAML 规范的对应关系，请参阅 [Metric View 对象模型文档](xref:semantic-bridge-metric-view-object-model)。

#### `View` 翻译

- 将被翻译
  - `Source`：变为单个事实表，在 TOM 模型中名为“Fact”
  - `Comment`：变为 TOM `Model.Description`
  - `Joins`：请参阅 `Join`
  - `Fields`：请参阅 `Field`
  - `Measures`: 请参阅 `Measure`
- 不翻译
  - `Filter`
  - `Materialization`

如果 `Source` 是由 3 个部分组成的表或视图引用，它会被转换为一个按名称访问 SQL 对象的 M 分区。
如果 `Source` 不是由 3 个部分组成的表或视图引用，它会被转换为一个嵌入 SQL 查询的 M 分区，其中整个 `Source` 字符串都会作为 SQL 查询。

出于翻译目的，`Filter` 属性将被忽略；
如果需要包含 `Filter` 中的逻辑，则需手动添加。
`Filter` 表达式会应用于针对 Metric View 的所有查询，因此，要实现完全自动的翻译，需要在 TOM 中生成的 M 代码里联接 `Joins` 中列出的所有表。

出于翻译目的，任何已定义的 `Materialization` 都会被忽略；
这些是用于在 Databricks 上执行查询的查询优化元数据，与 TOM 模型无关。

#### `Join` 翻译

- 将被翻译
  - `Name`：变为 TOM 表名
  - `Source`：变为该表的 M 分区
  - `On`：变为 TOM 关系
  - `Joins`：变为额外的 TOM 表
  - `Cardinality`
- 不翻译
  - `Using`
  - `Rely`

每个 `Join` 都会转换为一个 TOM 表，并按照与 `View.Source` 属性相同的规则定义一个 M 分区。

`On` 等值连接（例如 `source.fk = dimTable.pk`）会转换为 TOM 关系。
`On` 属性中的其他任何谓词都不会被转换为关系。

Metric View 中的 `Join` 树会转换为 TOM 表，并形成一条 N:1 关系链（前提是相应的基数受支持；请参阅下文关于基数的说明）。
这表示一个雪花模型架构。

`Cardinality` 为 `ManyToOne` 时，会转换为 TOM 的 N:1 关系。
未填充的 `Cardinality`，或未设置此属性的 `Join`，默认按 `ManyToOne` 处理，这与 [Metric View 文档](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#joins) 一致。
`Cardinality` 的其他值目前还不支持翻译为关系。

`Using` 连接不支持翻译；因此不会生成 TOM 关系。

`Rely` 不会以任何方式传递到 TOM 模型中。

在未创建 TOM 关系的情况下，我们仍会创建 TOM 表，并按其他部分所述将所有 Metric View `Fields` 转换为 TOM 列。

> [!NOTE]
> Databricks 最近引入了一种新模式，在多个 `Join` 子树上使用 `OneToMany` 基数来实现多事实模型。
> 我们尚未完全支持这种模式的转换：会带入所有表、字段和度量值，但不会创建全部关系。
> 导入遵循此模式的模型时，会显示一条诊断警告。

#### `Field` 翻译

- 已翻译
  - `Name`
  - `DisplayName`
  - `Expr`
  - `Comment`：将映射为 TOM 列的 `Description` 属性
  - `Format`：将映射为 TOM 列的 `FormatString` 属性；有关 `Format` 的翻译，请参阅下文相应部分
- 未翻译
  - `Synonyms`

每个 `Field` 都会成为 Tabular 模型中的一列。

如果 `Field.DisplayName` 有值，
则 TOM 列的 `Name` 为 `Field.DisplayName`；否则为 `Field.Name`。

如果 `Expr` 是不带限定符的字段引用，则将其添加到事实表中。
如果 `Expr` 是带限定符的引用（例如 `table.field`），
则将其添加到为 `Join` 创建的表中，该表的名称与该限定引用的表名部分相同；
如果表名部分为 `source`，则将其添加到事实表中。
无论是带限定符还是不带限定符的字段引用，
该字段都会作为 [`TOMWrapper.DataColumn`](xref:TabularEditor.TOMWrapper.DataColumn) 添加。
如果 `Expr` 是 SQL 表达式，
则会将其作为 [`TOMWrapper.CalculatedColumn`](xref:TabularEditor.TOMWrapper.CalculatedColumn) 添加。
当 `Expr` 是 SQL 表达式时，我们会提取其中所有字段引用；
如果所有字段引用的表名部分都相同，
则会将其添加到为该 `Join` 创建的表中；
否则会将其添加到事实表。
我们会识别 SQL 表达式中的所有字段引用；如果这些引用尚未在 Metric View 中作为 `Field` 存在，则将其作为 `DataColumn` 添加到 Tabular 模型中。
我们不会转换 `Field.Expr` 属性中的 SQL 表达式；
该 SQL 表达式会作为注释包含在 `CalculatedColumn` 的 DAX 表达式中。
这些表达式需由用户自行翻译。

一些示例：

| `Expr`                                                | 翻译后的类型             | 添加到的表           | 注意                                       |
| ----------------------------------------------------- | ------------------ | --------------- | ---------------------------------------- |
| `field1`                                              | `DataColumn`       | `'Fact'`        | 未限定字段引用等同于用 `source` 进行限定的字段引用           |
| `source.field2`                                       | `DataColumn`       | `'Fact'`        | `source` 是对 `View.Source` 属性的引用，即事实表     |
| `dimCustomer.key`                                     | `DataColumn`       | `'dimCustomer'` | 必须存在一个 `Join`，其 `Name` 属性为 `dimCustomer` |
| `CONCAT(dimCustomer.FirstName, dimCustomer.LastName)` | `CalculatedColumn` | `'dimCustomer'` | 限定名称中的所有表部分都指向同一个名称                      |
| `CONCAT(dimGeo.Country, dimCustomer.Address)`         | `CalculatedColumn` | `'Fact'`        | 存在多个彼此不同的表部分                             |

#### `度量值` 的翻译

- 已翻译
  - `Name`
  - `DisplayName`
  - `Expr`：将成为 TOM 度量值的 `Expression` 属性；请参阅下文关于 SQL -> DAX 翻译的部分
  - `Comment`：会成为 TOM 度量值的 `Description` 属性
  - `Format`：将成为 TOM 度量值的 `FormatString` 属性；请参阅下文关于 `Format` 翻译的部分
- 未翻译
  - `Synonyms`
  - `Window`

所有度量值都会添加到事实表中。

如果 Metric View 中存在 `Measure.DisplayName`，那么 TOM 度量值的 `Name` 就是 Metric View 的 `Measure.DisplayName`；
否则就是 Metric View 的 `Measure.Name`。

`Expr` 会被翻译为 DAX；如果我们无法自动翻译该度量值，则会以注释形式原样传递。
我们会识别 SQL 表达式中的所有字段引用；如果这些字段尚未作为 Metric View 的 `Field` 存在，则会将它们作为 `DataColumn` 添加到 Tabular 模型中。

窗口规范不会被翻译；无论 `Expr` 中的 SQL 如何，都会回退为 DAX 注释。

### `Format` 翻译

Metric View 的 `Format` 会被翻译为其所在对象上的 TOM `FormatString`。
目标格式是 TOM 模型中使用的 VBA 风格格式字符串。
该翻译尽力而为：
如果我们能创建与 `Format` 配置完全匹配的格式字符串，就会这样做；
如果无法创建完全等效的格式字符串，则会回退为近似等效格式，并发出一条警告，供你在导入后查看。

货币、百分比和数字格式都能顺利翻译：
货币会转换为带分组的数字格式，并以货币符号作为前缀；
百分比会转换为遵循所声明小数位数的百分比格式；
数字会遵循所声明的小数位数和分组分隔符，而科学计数法缩写会转换为指数格式。

年-月-日日期可以顺利翻译为 ISO 日期格式；
本地化的长月份日期和本地化的数字月份日期可以顺利翻译为 `Long Date` 和 `Short Date` 命名格式；
时:分和时:分:秒时间可以顺利翻译为 `Short Time` 和 `Long Time` 命名格式。

其余格式无法精确翻译，并会发出警告：
紧凑数字缩写形式和字节格式会回退为普通数字格式；
本地化的短月份日期会回退为 `Long Date`；
年-周日期会回退为 ISO 日期；
组合日期时间格式会回退为 ISO 组合格式。

### SQL -> DAX 翻译

Metric View 在 SQL 表达式之上提供了一个结构化层，因此翻译 Metric View 的一部分工作是在 Tabular 模型中将 SQL 转换为 DAX 和 M。
支持的聚合包括求和、计数、非重复计数、最大值、最小值和平均值。
SQL->DAX 翻译支持基本算术运算、常见计数模式、度量值引用以及括号优先级。

> [!WARNING]
> 注意，SQL 和 DAX 是不同的语言，语义也不同。
> 我们无法保证转换后的度量值在 Metric View SQL 与我们生成的 Tabular DAX 中的行为完全一致。
> 定义在事实表字段上的基本聚合通常表现相同，而定义在维度表字段上的聚合则更可能产生非预期结果。

## Metric Views 与 Tabular 模型中的常见通用术语

为可能不熟悉 Metric Views 或表格模型的用户，我们在下方提供了一份不完整的对照速查表。
我们对 Metric View 对象的称呼基于它们在 YAML 中的表示；对 Tabular 对象的称呼则基于该对象类型在 TMDL/TMSL 中的名称。

| 通用术语  | Tabular 中的名称 | Metric View 中的名称                                     | 说明                             | 注意                                                                                                  |
| ----- | ------------ | ---------------------------------------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------- |
| 事实表   | 表            | `source`                                             | 用于存放维度外键以及可聚合的数值字段的表           | 一个 Metric View 只有一个未命名的事实表，并在 YAML 中表示为根级 `source` 属性。 表格模型不区分表的类型：某个表是否为事实表只能推断出来                  |
| 维度    | 表            | `join`                                               | 用于存放描述性属性以及一个主键的表，事实表通过该主键与其关联 | Tabular 模型同样不会区分，因此“维度”的角色也只能像事实表一样通过推断得出。                                                          |
| 分区    | 分区           | `source`（仅用于 `join`）                                 | 用于数据管理的对象，保存表中的一部分数据           | 表格模型中的表可以有多个分区，并且必须至少有一个。 如上所述，Metric View 的事实仅被定义为一个源，但 Metric View 的联接也有一个 `source` 属性，其作用大致类似于分区 |
| 字段    | 列            | 字段                                                   | 表格中的一列                         |                                                                                                     |
| 度量值   | 度量值          | 度量值                                                  | 在模型中按业务逻辑进行汇总的定量值              | 表格模型中的度量值使用 DAX 编写，而在 Metric View 中使用 SQL 编写                                                        |
| 联接或关系 | 关系           | join.on 或 join.using | 一个表中的外键与另一个表中的主键之间的对应关系        | 在表格模型中，关系是显式对象；而在 Metric View YAML 中，它被隐式定义为 `join` 对象的一个属性                                         |

## 其他参考资料

- @semantic-bridge
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- @semantic-bridge-how-tos
- [Metric View API 文档](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
