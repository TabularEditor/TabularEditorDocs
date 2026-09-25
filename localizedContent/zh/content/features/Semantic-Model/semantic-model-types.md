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

Tabular Editor can work with several different model types. 下面概述了哪些模型类型可与 Tabular Editor 一起使用，以及每种模型类型可使用哪些功能。

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

**Legend:**

- ✔️：支持
- ❌：不支持

<a name="DirectLake">1</a> - The table partition must be an Entity Partition to work correctly. Direct Lake models can only have one partition per table. <a name="DirectLakeCalculated">2</a> - 计算表格不能引用 OneLake 上的 Direct Lake 表或列。 Calculation groups, what-if parameters and field parameters are supported.

<a name="TE3Prem">3</a> - Tabular Editor 3 features only. Operations performed through the XMLA endpoint requires a Business or Enterprise license. [更多信息](xref:editions)。 <a name="DirectLakeSQLCalculated">4</a> - Direct Lake on SQL only supports calculation groups, what-if parameters and field parameters, which implicitly create calculated tables. General calculated tables are not supported.

> [!NOTE]
> 2025 年六月发布的 Power BI Desktop 版本已解除对第三方工具的所有建模限制。 Prior to that, various modeling operations were not supported. See [Power BI Desktop Limitations](xref:desktop-limitations).

> [!TIP]
> 如需了解 Direct Lake 模型限制的更多详细信息，请参阅 Microsoft 的 [Direct Lake 文档](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview)

## 不受支持的语义模型类型

以下语义模型类型不受支持，因为它们不支持 XMLA 写入操作。

- 基于与 Azure Analysis Services 或 SQL Server Analysis Services 模型的实时连接的报告。
- 基于与 Power BI 数据集的实时连接的报告。
- 具有推送数据的模型。
- 存储在 Power BI 我的工作区中的模型。
- 存储在 Power BI Pro 工作区中的模型。
- Direct Lake Default Semantic Models. As of September 2025, Power BI no longer automatically creates default semantic models when a warehouse, lakehouse or mirrored item is created. By November 2025, all existing default semantic models were disconnected from their items and became independent semantic models. It is possible to connect to a default semantic model, but it is not possible to change it through the XMLA endpoint.
- Excel 工作簿语义模型。