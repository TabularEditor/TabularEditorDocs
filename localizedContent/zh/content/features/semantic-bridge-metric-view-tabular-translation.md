---
uid: semantic-bridge-metric-view-tabular-translation
title: Metric View to Tabular translation
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

# Metric View to Tabular translation

<!--
SUMMARY: Describes the process and specifics of translating a Metric View to a TOM model.
-->

> [!NOTE]
> The Semantic Bridge is in public preview.
> The 3.25.0 release supports Metric View v0.1 metadata, and the 3.26.2 release supports Metric View v1.1 metadata.
> Limitations are described below.

This page describes how translation works when importing a Metric View definition into a Tabular model.

## 翻译过程

将 Metric View 翻译为 Tabular 模型分为几个步骤：

1. 从磁盘读取 YAML 文件
2. 对 YAML 进行反序列化
3. 验证反序列化后的 YAML 是否为有效的 Metric View
4. If it is a valid Metric View, store it as the currently loaded Metric View, similar to how there is a loaded Tabular model that you interact with.
   If it is not a valid Metric View, the process stops here and diagnostic messages are available.
5. 分析 Metric View，并尝试将其转换为一种中间表示
6. 尝试将中间表示转换为 Tabular 模型

The import GUI handles all of this for you, but you can also use C# scripts to customize different steps of the process and operate on the Metric View programmatically, similarly to how you are used to doing with a Tabular model.
Specifically, you can

- load a Metric View from disk with [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A): loading makes it available in C# scripts as [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model), but does not import the structure into the Tabular model
- deserialize a Metric View from a string with [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A): similar to loading, the model is available as [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model), but is not imported
- save a Metric View to disk with [`SemanticBridge.MetricView.Save`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Save%2A)
- serialize a Metric View to a string with [`SemanticBridge.MetricView.Serialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Serialize%2A).
- validate a Metric View using a system that is similar to the [Best Practice Analyzer](xref:best-practice-analyzer) with [`SemanticBridge.MetricView.Validate`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate%2A)
  - you can create your own custom validation rules with [`SemanticBridge.MetricView.MakeValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRule%2A) and its simpler versions
- import a Metric View to Tabular with [`SemanticBridge.MetricView.ImportToTabularFromFile`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.ImportToTabularFromFile%2A), which does the exact same as the import GUI, or [`SemanticBridge.MetricView.ImportToTabular`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.ImportToTabular%2A), which is similar, but operates on the currently loaded Metric View, rather than reading one from disk.

### Per object translation notes

The four items below, `View`, `Join`, `Field`, and `Measure`, are the core objects of a Metric View definition that become TOM objects.
Other metadata in the Metric View definition are either ignored or modify exactly how these objects are translated.

> [!NOTE]
> The translation is performed upon the Metric View object model, so we discuss everything in these terms.
> See [the Metric View object model docs](xref:semantic-bridge-metric-view-object-model) for specifics of the object model and how it aligns to the YAML spec.

#### `View` translation

- translate
  - `Source`: becomes the single fact table, named 'Fact' in the TOM model
  - `Comment`: becomes TOM `Model.Description`
  - `Joins`: see `Join`
  - `Fields`: see `Field`
  - `Measures`: see `Measure`
- do not translate
  - `Filter`
  - `Materialization`

If the `Source` is a 3-part table or view reference, it is translated to an M partition that accesses the SQL object by name.
If the `Source` is not a 3-part table or view reference, it is translated to an M partition with an embedded SQL query, with the entirety of the `Source` string as the SQL query.

The `Filter` property is ignored for purposes of translation;
if you need the logic included in `Filter`, you will have to manually add this.
The `Filter` expression applies to all queries against the Metric View, and so a full automated translation would require joining all tables named in `Joins` in generated M code in TOM.

Any defined `Materialization` is ignored for the purposes of translation;
these are query optimization metadata for executing queries on Databricks and not relevant to a TOM model.

#### `Join` translation

- translated
  - `Name`: becomes TOM table name
  - `Source`: becomes M partition on table
  - `On`: becomes a TOM relationship
  - `Joins`: become additional TOM tables
  - `Cardinality`
- untranslated
  - `Using`
  - `Rely`

`Join`s each become a TOM table, with an M partition defined according to the same rules as for the `View.Source` property.

`On` equijoins (e.g., `source.fk = dimTable.pk`) become TOM relationships.
Any other predicate in an `On` property is not translated as a relationship.

Trees of `Join`s in a Metric View are translated as TOM tables in a chain of N:1 relationships, where the cardinalities are supported (see note on cardinality below).
This represents a snowflake model schema.

`Cardinality` of `ManyToOne` is translated as a TOM N:1 relationship.
An unpopulated `Cardinality` or a `Join` without this property set is treated as `ManyToOne` by default, in accordance with [Metric View docs](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#joins).
Other values for `Cardinality` are not yet supported for translation as a relationship.

`Using` joins are not supported for translation; these do not yield a TOM relationship.

`Rely` is not propagated into the TOM model in any way.

In cases where a TOM relationship is not created, we still create a TOM table and translate all Metric View `Fields` to TOM columns as described elsewhere.

> [!NOTE]
> Databricks has recently introduced a new pattern using `OneToMany` cardinality against multiple `Join` sub-trees to implement a multi-fact model.
> We do not yet translate this pattern fully: we bring over all tables, fields, and measures, but do not create all relationships.
> A diagnostic warning is shown when importing a model following this pattern.

#### `Field` translation

- translated
  - `Name`
  - `DisplayName`
  - `Expr`
  - `Comment`: becomes TOM column's `Description` property
  - `Format`: becomes TOM column's `FormatString` property; see section below on `Format` translation
- untranslated
  - `Synonyms`

Each `Field` becomes a column in the Tabular model.

The TOM column's `Name` is `Field.DisplayName` if it is populated,
otherwise it is `Field.Name`.

If the `Expr` is an unqualified field reference, it is added to the fact table.
If the `Expr` is a qualified reference (e.g., `table.field`),
then it is added to the table created for the `Join` with the same name as the table-part of the qualified reference;
if the table-part is `source`, it is added to the fact table.
In both the qualified and unqualified field reference cases,
the field is added as a [`TOMWrapper.DataColumn`](xref:TabularEditor.TOMWrapper.DataColumn).
If the `Expr` is a SQL expression,
then it is added as [`TOMWrapper.CalculatedColumn`](xref:TabularEditor.TOMWrapper.CalculatedColumn).
When the `Expr` is a SQL expression, we extract all field references;
if all field references share the same table-part,
then we add it to the table created for that `Join`,
otherwise we add it to the fact table.
We identify all field references in the SQL expression and add those to the Tabular model as `DataColumn`s if they do not already exist as a Metric View `Field`.
We do not translate SQL expressions for `Field.Expr` properties;
the SQL expression is included as a comment in the DAX expression for the `CalculatedColumn`.
It is up to the user to translate these expressions.

一些示例：

| `Expr`                                                | 翻译后的类型             | 添加到的表           | 注意                                       |
| ----------------------------------------------------- | ------------------ | --------------- | ---------------------------------------- |
| `field1`                                              | `DataColumn`       | `'Fact'`        | 未限定字段引用等同于用 `source` 进行限定的字段引用           |
| `source.field2`                                       | `DataColumn`       | `'Fact'`        | `source` 是对 `View.Source` 属性的引用，即事实表     |
| `dimCustomer.key`                                     | `DataColumn`       | `'dimCustomer'` | 必须存在一个 `Join`，其 `Name` 属性为 `dimCustomer` |
| `CONCAT(dimCustomer.FirstName, dimCustomer.LastName)` | `CalculatedColumn` | `'dimCustomer'` | 限定名称中的所有表部分都指向同一个名称                      |
| `CONCAT(dimGeo.Country, dimCustomer.Address)`         | `CalculatedColumn` | `'Fact'`        | 存在多个彼此不同的表部分                             |

#### `Measure` translation

- translated
  - `Name`
  - `DisplayName`
  - `Expr`: becomes TOM measure's `Expression` property; see section below on SQL -> DAX translation
  - `Comment`: becomes TOM measure's `Description` property
  - `Format`: becomes TOM measure's `FormatString` property; see section below on `Format` translation
- untranslated
  - `Synonyms`
  - `Window`

All measures are added to the fact table.

The TOM measure's `Name` is the Metric View's `Measure.DisplayName` if it exists,
otherwise it is the Metric View's `Measure.Name`.

`Expr` is translated to DAX or passed through as a comment in cases where we cannot automatically translate the measure.
We identify all field references in the SQL expression and add those to the Tabular model as `DataColumn`s if they do not already exist as a Metric View `Field`.

Window specifications are not translated and cause fallback to a DAX comment, regardless of the SQL in `Expr`.

### `Format` translation

A Metric View `Format` is translated to a TOM `FormatString` on the object that carries it.
The target is a VBA-style format string, as used in TOM models.
The translation is best-effort:
if we can create a format string that exactly matches the configuration of the `Format`, then we do so;
if we cannot create an exact equivalent, then we fall back to an approximate equivalent and emit a warning you can review after import.

Currency, percentage, and number formats translate cleanly:
currency becomes a currency-symbol prefix on a grouped numeric format,
percentage becomes a percent format that honors the declared decimal places,
and number honors the declared decimal places and group separator, with the scientific abbreviation becoming an exponential format.

Year-month-day dates translate cleanly to an ISO date format;
locale long-month and locale numeric-month dates translate cleanly to the `Long Date` and `Short Date` named formats;
and hour-minute and hour-minute-second times translate cleanly to the `Short Time` and `Long Time` named formats.

The remaining formats cannot be precisely translated and emit a warning:
the compact number abbreviation and the byte format fall back to a plain numeric format;
the locale short-month date falls back to `Long Date`;
the year-week date falls back to an ISO date;
and a combined date-and-time format falls back to an ISO composite.

### SQL -> DAX translation

Metric View 在 SQL 表达式之上提供了一个结构化层，因此翻译 Metric View 的一部分工作是在 Tabular 模型中将 SQL 转换为 DAX 和 M。
Supported aggregations are sum, count, distinct count, max, min, and average.
Basic arithmetic, common counting patterns, measure references, and parenthesis precedence are all supported for SQL->DAX translation.

> [!WARNING]
> Note that SQL and DAX are different languages with different semantics.
> 我们无法保证转换后的度量值在 Metric View SQL 与我们生成的 Tabular DAX 中的行为完全一致。
> Basic aggregates defined on fact table fields should behave the same, whereas aggregates defined on fields in dimension tables are more likely to produce undesired results.

## Metric Views 与 Tabular 模型中的常见通用术语

For those of our users who may be unfamiliar with either Metric Views or Tabular models, we provide an incomplete rosetta stone below.
我们对 Metric View 对象的称呼基于它们在 YAML 中的表示；对 Tabular 对象的称呼则基于该对象类型在 TMDL/TMSL 中的名称。

| 通用术语  | Tabular 中的名称 | Metric View 中的名称                                     | 说明                             | 注意                                                                                                                                                                                                                                                         |
| ----- | ------------ | ---------------------------------------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 事实表   | 表            | `source`                                             | 用于存放维度外键以及可聚合的数值字段的表           | 一个 Metric View 只有一个未命名的事实表，并在 YAML 中表示为根级 `source` 属性。 Tabular models do not differentiate between types of tables: whether a table is a fact can only be inferred                                                                         |
| 维度    | 表            | `join`                                               | 用于存放描述性属性以及一个主键的表，事实表通过该主键与其关联 | Tabular 模型同样不会区分，因此“维度”的角色也只能像事实表一样通过推断得出。                                                                                                                                                                                                                 |
| 分区    | 分区           | `source`（仅用于 `join`）                                 | 用于数据管理的对象，保存表中的一部分数据           | Tabular model tables can have many partitions and must have at least one. The Metric View fact, as mentioned above is defined purely as a source, but Metric View joins also have a `source` property, which acts roughly like a partition |
| 字段    | 列            | 字段                                                   | 表格中的一列                         |                                                                                                                                                                                                                                                            |
| 度量值   | 度量值          | 度量值                                                  | 在模型中按业务逻辑进行汇总的定量值              | 表格模型中的度量值使用 DAX 编写，而在 Metric View 中使用 SQL 编写                                                                                                                                                                                                               |
| 联接或关系 | 关系           | join.on 或 join.using | 一个表中的外键与另一个表中的主键之间的对应关系        | 在表格模型中，关系是显式对象；而在 Metric View YAML 中，它被隐式定义为 `join` 对象的一个属性                                                                                                                                                                                                |

## Additional references

- @semantic-bridge
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- @semantic-bridge-how-tos
- [Metric View API docs](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
