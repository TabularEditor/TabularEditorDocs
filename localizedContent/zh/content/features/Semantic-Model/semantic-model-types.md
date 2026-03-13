---
uid: semantic-model-types
title: Power BI 语义模型类型
author: Morten Lønskov
updated: 2025-06-19
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# 语义模型类型

Tabular Editor 可以处理多种不同的模型类型。 下面概述了哪些模型类型可与 Tabular Editor 配合使用，以及每种模型类型可用的功能。

|模型类型|导入|直接查询|OneLake 上的 Direct Lake|SQL 上的 Direct Lake|.pbix|.pbip|
\|---|---|---|---|---|
|在 Tabular Editor 中连接|✔️|✔️|✔️|✔️|✔️|
|创建新模型|✔️|✔️|✔️|✔️|✔️|✔️|
|编写度量值|✔️|✔️|✔️|✔️|✔️|✔️|
|创建和编辑表|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|创建和编辑分区|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|创建和编辑列|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|创建和编辑计算表格|✔️|✔️|✔️<sup>[2](#DirectLakeCalculated)</sup>|✔️|✔️|✔️|
|创建和编辑计算列|✔️|✔️|✔️<sup>[2](#DirectLakeCalculated)</sup>|✔️|✔️|✔️|
|创建和编辑计算组|✔️|✔️|✔️|✔️|✔️|
|创建和编辑关系|✔️|✔️|✔️|✔️|✔️|
|创建和编辑角色|✔️|✔️|✔️|✔️|✔️|✔️|
|创建和编辑透视视图|✔️|✔️|✔️|✔️|✔️|✔️|
|创建和编辑翻译|✔️|✔️|✔️|✔️|✔️|✔️|
|使用 Best Practice Analyzer|✔️|✔️|✔️|✔️|✔️|
|编辑所有 TOM 属性|✔️|✔️|✔️|✔️|✔️|✔️|
|创建图表<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用预览数据<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用 Pivot Grids<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用 DAX 查询<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用 DAX 调试器<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用 Vertipac Analyzer<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|处理模型和表格<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|删除对象|✔️|✔️|✔️|✔️|

**图例：**

- ✔️：支持
- ❌：不支持

<a name="DirectLake">1</a> - 表分区必须是 Entity Partition 才能正常工作，并且 Direct Lake 模型只能有一个分区。 <a name="DirectLakeCalculated">2</a> - 计算表格和计算列不能引用 OneLake 上的 Direct Lake 表或列。

<a name="TE3Prem">3</a> - 仅限 Tabular Editor 3 功能。 通过 XMLA endpoint 执行的操作需要 Business 或 Enterprise 许可证。 [更多信息](xref:editions)。

> [!NOTE]
> 在 2025 年 6 月发布的 Power BI Desktop 版本中，针对第三方工具的所有建模限制均已解除。 在此之前，Power BI Desktop 不支持各种建模操作。 请参阅 [Power BI Desktop 限制](xref:desktop-limitations)

> [!TIP]
> 有关 Direct Lake 模型限制的更多信息，请参阅 Microsoft 的 [Direct Lake 文档](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview)

## 不受支持的语义模型类型

以下语义模型类型不受支持，因为它们不支持 XMLA 写入操作。

- 基于与 Azure Analysis Services 或 SQL Server Analysis Services 模型的实时连接的报告。
- 基于与 Power BI 数据集的实时连接的报告。
- 具有推送数据的模型。
- 存储在 Power BI 我的工作区中的模型。
- 存储在 Power BI Pro 工作区中的模型。
- Direct Lake 默认语义模型。 (可以连接到默认数据集，但无法通过 XMLA 端点对其进行更改)
- Excel 工作簿语义模型。