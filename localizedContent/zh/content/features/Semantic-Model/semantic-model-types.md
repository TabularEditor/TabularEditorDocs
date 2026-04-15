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

Tabular Editor 可以处理多种不同的模型类型。 下面概述了哪些模型类型可与 Tabular Editor 配合使用，以及每种模型类型可用的功能。

| Model Type                                           | 导入 | Direct Query | OneLake 上的 Direct Lake                  | SQL 上的 Direct Lake                         | .pbix | .pbip |
| ---------------------------------------------------- | -- | ------------ | --------------------------------------- | ------------------------------------------ | --------------------- | --------------------- |
| Connect in Tabular Editor                            | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Create new model                                     | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Write Measures                                       | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Create & Edit Tables             | ✔️ | ✔️           | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| Create & Edit Partitions         | ✔️ | ✔️           | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| Create & Edit Columns            | ✔️ | ✔️           | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| Create & Edit Calculated Tables  | ✔️ | ✔️           | ✔️<sup>[2](#DirectLakeCalculated)</sup> | ✔️<sup>[4](#DirectLakeSQLCalculated)</sup> | ✔️                    | ✔️                    |
| Create & Edit Calculated Columns | ✔️ | ✔️           | ❌                                       | ❌                                          | ✔️                    | ✔️                    |
| Create & Edit Calculation Groups | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Create & Edit Relationships      | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Create & Edit Roles              | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Create & Edit Perspectives       | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Create & Edit Translations       | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use Best Practice Analyzer                           | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Edit All TOM properties                              | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Create Diagrams<sup>[3](#TE3Prem)</sup>              | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use Preview Data<sup>[3](#TE3Prem)</sup>             | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use Pivot Grids<sup>[3](#TE3Prem)</sup>              | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use DAX Queries<sup>[3](#TE3Prem)</sup>              | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use DAX Debugger<sup>[3](#TE3Prem)</sup>             | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use VertiPaq Analyzer<sup>[3](#TE3Prem)</sup>        | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Process Model and Tables<sup>[3](#TE3Prem)</sup>     | ✔️ | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Delete Objects                                       | ✔️ | ✔️           | ✔️                                      | ✔️                                         |                       |                       |

**图例：**

- ✔️：支持
- ❌：不支持

<a name="DirectLake">1</a> - The table partition must be an Entity Partition to work correctly. Direct Lake models can only have one partition per table. <a name="DirectLakeCalculated">2</a> - Calculated Tables cannot refer to Direct Lake on OneLake tables or columns. Calculation groups, what-if parameters and field parameters are supported.

<a name="TE3Prem">3</a> - 仅限 Tabular Editor 3 功能。 通过 XMLA endpoint 执行的操作需要 Business 或 Enterprise 许可证。 [更多信息](xref:editions)。 <a name="DirectLakeSQLCalculated">4</a> - Direct Lake on SQL only supports calculation groups, what-if parameters and field parameters, which implicitly create calculated tables. General calculated tables are not supported.

> [!NOTE]
> The June 2025 release of Power BI Desktop lifted all modeling limitations for third-party tools. Prior to that, various modeling operations were not supported. See [Power BI Desktop Limitations](xref:desktop-limitations).

> [!TIP]
> 有关 Direct Lake 模型限制的更多信息，请参阅 Microsoft 的 [Direct Lake 文档](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview)

## 不受支持的语义模型类型

The following semantic model types are unsupported, as they do not support XMLA write operations.

- 基于与 Azure Analysis Services 或 SQL Server Analysis Services 模型的实时连接的报告。
- 基于与 Power BI 数据集的实时连接的报告。
- 具有推送数据的模型。
- 存储在 Power BI 我的工作区中的模型。
- 存储在 Power BI Pro 工作区中的模型。
- Direct Lake 默认语义模型。 As of September 2025, Power BI no longer automatically creates default semantic models when a warehouse, lakehouse or mirrored item is created. By November 2025, all existing default semantic models were disconnected from their items and became independent semantic models. It is possible to connect to a default semantic model, but it is not possible to change it through the XMLA endpoint.
- Excel 工作簿语义模型。