---
uid: semantic-model-types
title: Power BI 语义模型类型
author: Morten Lønskov
updated: 2026-03-27
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

# 语义模型类型

Tabular Editor 可与多种不同的模型类型配合使用。 Tabular Editor 可与多种不同的模型类型配合使用。 下面概述了哪些模型类型可与 Tabular Editor 配合使用，以及每种模型类型可用的功能。

| 模型类型                                   | 导入 | DirectQuery | OneLake 上的 Direct Lake                  | SQL 上的 Direct Lake                         | .pbix | .pbip |
| -------------------------------------- | -- | ----------- | --------------------------------------- | ------------------------------------------ | --------------------- | --------------------- |
| 在 Tabular Editor 中连接                   | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    |                       |
| 创建新模型                                  | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 编写度量值                                  | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 创建和编辑表格                                | ✔️ | ✔️          | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| 创建和编辑分区                                | ✔️ | ✔️          | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| 创建和编辑列                                 | ✔️ | ✔️          | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| 创建和编辑计算表格                              | ✔️ | ✔️          | ✔️<sup>[2](#DirectLakeCalculated)</sup> | ✔️<sup>[4](#DirectLakeSQLCalculated)</sup> | ✔️                    | ✔️                    |
| 创建和编辑计算列                               | ✔️ | ✔️          | ❌                                       | ❌                                          | ✔️                    | ✔️                    |
| 创建和编辑计算组                               | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    |                       |
| 创建和编辑关系                                | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    |                       |
| 创建和编辑角色                                | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 创建/编辑透视                                | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 创建/编辑翻译                                | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 使用 Best Practice Analyzer              | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    |                       |
| 编辑所有 TOM 属性                            | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 创建图表<sup>[3](#TE3Prem)</sup>           | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 使用预览数据<sup>[3](#TE3Prem)</sup>         | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 使用Pivot Grid<sup>[3](#TE3Prem)</sup>   | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 使用 DAX 查询<sup>[3](#TE3Prem)</sup>      | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 使用 DAX 调试器<sup>[3](#TE3Prem)</sup>     | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 使用 VertiPaq分析器<sup>[3](#TE3Prem)</sup> | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 处理模型和表格<sup>[3](#TE3Prem)</sup>        | ✔️ | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| 删除对象                                   | ✔️ | ✔️          | ✔️                                      | ✔️                                         |                       |                       |

**图例：**

- ✔️：支持
- ❌：不支持

<a name="DirectLake">1</a> - 表分区必须是 Entity Partition，才能正常工作。 Direct Lake 模型的每个表只能有一个分区。 <a name="DirectLake">1</a> - 表分区必须是 Entity Partition，才能正常工作。 Direct Lake 模型的每个表只能有一个分区。 <a name="DirectLakeCalculated">2</a> - 计算表格不能引用 OneLake 上的 Direct Lake 表或列。 支持计算组、假设分析参数和字段参数。 支持计算组、假设分析参数和字段参数。

<a name="TE3Prem">3</a> - 仅限 Tabular Editor 3 功能。 通过 XMLA endpoint 执行的操作需要 Business 或 Enterprise 许可证。 [更多信息](xref:editions)。 <a name="DirectLakeSQLCalculated">4</a> - SQL 上的 Direct Lake 仅支持计算组、假设分析参数和字段参数，它们会隐式创建计算表格。 不支持常规计算表格。

> [!NOTE]
> 2025 年六月发布的 Power BI Desktop 版本已解除对第三方工具的所有建模限制。 在此之前，许多建模操作都不受支持。 见 [Power BI Desktop 限制](xref:desktop-limitations)。 在此之前，许多建模操作都不受支持。 见 [Power BI Desktop 限制](xref:desktop-limitations)。

> [!TIP]
> 有关 Direct Lake 模型限制的更多详细信息，请参阅 Microsoft 的 [Direct Lake 文档](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview)

## 不受支持的语义模型类型

以下语义模型类型不受支持，因为它们不支持 XMLA 写入操作。

- 基于与 Azure Analysis Services 或 SQL Server Analysis Services 模型的实时连接的报告。
- 基于与 Power BI 数据集的实时连接的报告。
- 具有推送数据的模型。
- 存储在 Power BI 我的工作区中的模型。
- 存储在 Power BI Pro 工作区中的模型。
- Direct Lake 默认语义模型。 自 2025 年九月起，创建 Warehouse、Lakehouse 或镜像项时，Power BI 不再自动创建默认语义模型。 到 2025 年十一月，所有现有默认语义模型都已与其对应项断开连接，并成为独立的语义模型。 可以连接到默认语义模型，但无法通过 XMLA endpoint 对其进行更改。
- Excel 工作簿语义模型。