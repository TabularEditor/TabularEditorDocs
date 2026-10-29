---
uid: semantic-model-types
title: Power BI 语义模型类型
author: Morten Lønskov
updated: 2026-10-26
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

Tabular Editor 可以与多种不同类型的模型配合使用。以下概述了哪些模型类型可与 Tabular Editor 一起使用，以及每种模型类型可使用的功能。 


|模型类型|导入|Direct Query|Direct Lake on OneLake|Direct Lake on SQL|.pbix|.pbip|
|---|---|---|---|---|---|---|
|在 Tabular Editor 中连接|✔️|✔️|✔️|✔️|✔️| |
|创建新模型|✔️|✔️|✔️|✔️|✔️|✔️|
|编写度量值|✔️|✔️|✔️|✔️|✔️|✔️|
|创建和编辑表|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|创建和编辑分区|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|创建和编辑列|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|创建和编辑计算表|✔️|✔️|✔️<sup>[2](#DirectLakeCalculated)</sup>|✔️<sup>[4](#DirectLakeSQLCalculated)</sup>|✔️|✔️|
|创建和编辑计算列|✔️|✔️|✔️<sup>[5](#DirectLakeCalcColumn)</sup>|❌|✔️|✔️|
|创建和编辑计算组|✔️|✔️|✔️|✔️|✔️| |
|创建和编辑关系|✔️|✔️|✔️|✔️|✔️| |
|创建和编辑角色|✔️|✔️|✔️|✔️|✔️|✔️|
|创建和编辑透视|✔️|✔️|✔️|✔️|✔️|✔️|
|创建和编辑翻译|✔️|✔️|✔️|✔️|✔️|✔️|
|使用最佳实践分析器|✔️|✔️|✔️|✔️|✔️| |
|编辑所有 TOM 属性|✔️|✔️|✔️|✔️|✔️|✔️|
|创建图表<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用预览数据<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用数据透视表<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用 DAX 查询<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用 DAX 调试器<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|使用 VertiPaq Analyzer<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|处理模型和表<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|删除对象|✔️|✔️|✔️|✔️| | |

**图例：**
- ✔️：支持 
- ❌：不支持


<a name="DirectLake">1</a> - 表分区必须是实体分区才能正常工作。Direct Lake 模型每个表只能有一个分区。
<a name="DirectLakeCalculated">2</a> - 计算表不能引用 OneLake 表或列上的 Direct Lake。支持计算组、模拟分析参数和字段参数。

<a name="TE3Prem">3</a> - 仅限 Tabular Editor 3 功能。通过 XMLA endpoint 执行的操作需要 Business 或 Enterprise 许可证。[更多信息](xref:editions)。
<a name="DirectLakeSQLCalculated">4</a> - Direct Lake on SQL 仅支持计算组、假设分析参数和字段参数，这些参数会隐式创建计算表。不支持常规计算表。
<a name="DirectLakeCalcColumn">5</a> - 预览功能。Direct Lake on OneLake 表上的计算列必须使用 `UserContext` 表达式上下文。它们在查询时进行评估，且不会物化，因此不能用作关系键。有关详细信息，请参阅[Direct Lake 指南](xref:direct-lake-guidance#calculated-columns-on-direct-lake-on-onelake)。

>[!NOTE]
> Power BI Desktop 2025 年 6 月版本取消了对第三方工具的所有建模限制。在此之前，不支持各种建模操作。请参阅[Power BI Desktop 限制](xref:desktop-limitations)。

>[!TIP]
> 有关 Direct Lake 模型限制的更多详细信息，请参阅 Microsoft 的[Direct Lake 文档](https://learn.microsoft.com/fabric/fundamentals/direct-lake-overview)

## 不支持的语义模型类型
以下语义模型类型不受支持，因为它们不支持 XMLA 写入操作。

- 基于与 Azure Analysis Services 或 SQL Server Analysis Services 模型的实时连接的报表。
- 基于与 Power BI 数据集的实时连接的报告。
- 具有推送数据的模型。
- 存储在 Power BI“我的工作区”中的模型。
- 存储在 Power BI Pro 工作区中的模型。
- Direct Lake 默认语义模型。截至 2025 年 9 月，在创建仓库、湖仓或镜像项时，Power BI 不再自动创建默认语义模型。到 2025 年 11 月，所有现有的默认语义模型都已与其项目断开连接，成为独立的语义模型。可以连接到默认语义模型，但无法通过 XMLA 端点对其进行更改。
- Excel 工作簿语义模型。