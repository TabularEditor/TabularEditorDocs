---
uid: semantic-model-types
title: Power BI Semantic model Types
author: Morten Lønskov
updated: 2025-06-19
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

# Semantic Model Types

Tabular Editor can work with several different model types. Below is an overview of which model types work with Tabular Editor and the capabilities that can be used with each model type.

|Model Type|Import|Direct Query|Direct Lake on OneLake|Direct Lake on SQL|.pbix|.pbip|
\|---|---|---|---|---|
|Connect in Tabular Editor|✔️|✔️|✔️|✔️|✔️|
|Create new model|✔️|✔️|✔️|✔️|✔️|✔️|
|Write Measures|✔️|✔️|✔️|✔️|✔️|✔️|
|Create & Edit Tables|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|Create & Edit Partitions|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|Create & Edit Columns|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|Create & Edit Calculated Tables|✔️|✔️|✔️<sup>[2](#DirectLakeCalculated)</sup>|✔️|✔️|✔️|
|Create & Edit Calculated Columns|✔️|✔️|✔️<sup>[2](#DirectLakeCalculated)</sup>|✔️|✔️|✔️|
|Create & Edit Calculation Groups|✔️|✔️|✔️|✔️|✔️|
|Create & Edit Relationships|✔️|✔️|✔️|✔️|✔️|
|Create & Edit Roles|✔️|✔️|✔️|✔️|✔️|✔️|
|Create & Edit Perspectives|✔️|✔️|✔️|✔️|✔️|✔️|
|Create & Edit Translations|✔️|✔️|✔️|✔️|✔️|✔️|
|Use Best Practice Analyzer|✔️|✔️|✔️|✔️|✔️|
|Edit All TOM properties|✔️|✔️|✔️|✔️|✔️|✔️|
|Create Diagrams<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Use Preview Data<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Use Pivot Grids<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Use DAX Queries<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Use DAX Debugger<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Use Vertipac Analyzer<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Process Model and Tables<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Delete Objects|✔️|✔️|✔️|✔️|

**Legend:**

- ✔️: Supported
- ❌: Unsupported

<a name="DirectLake">1</a> - The table partition must be an Entity Partition to work correctly and Direct Lake models can only have one partition. <a name="DirectLakeCalculated">2</a> - Calculated Tables and Columns cannot refer to Direct Lake on OneLake tables or columns.

<a name="TE3Prem">3</a> - Tabular Editor 3 features only. Operations performed through the XMLA endpoint requires a Business or Enterprise license. [More information](xref:editions).

> [!NOTE]
> The June 2025 Release of Power BI Desktop all modeling limitations for third party tools where lifted. Prior to that various modeling operations where not supported. See [Power BI Desktop Limitations](xref:desktop-limitations)

> [!TIP]
> For further details on restrictions on Direct Lake models refer to Microsoft's [Direct Lake documentation](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview)

## Unsupported Semantic Model types

The following semantic model types are unsupported, as they don't support XMLA write operations.

- Reports based on a live connection to an Azure Analysis Services or SQL Server Analysis Services model.
- Reports based on a live connection to a Power BI dataset.
- Models with Push data.
- Models stored in Power BI My Workspace.
- Models stored in Power BI Pro Workspace.
- Direct Lake Default Semantic Models. (It is possible to connect to a default dataset, but it is not possible to change it through the XMLA endpoint)
- Excel workbook Semantic Models.