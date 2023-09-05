---
uid: dataset-types
title: Power BI Dataset Types
author: Morten Lønskov
updated: 2023-08-21
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---


# Dataset Types

Tabular Editor can work with several different dataset types. Bellow is an overview of which dataset types work with Tabular Editor and the capabilities that can be used with each dataset type. 


|Dataset Type|Import|Direct Lake (Standalone) | Direct Lake (Default)|PBIX|PBIP|
|---|---|---|---|---|
|Connect in Tabular Editor|✔️|✔️|❌|✔️|✔️|
|Create new dataset|✔️|❌|--|✔️|✔️|
|Write Measures|✔️|✔️|--|✔️|✔️|
|Create & Edit Tables|✔️|✔️<sup>[1](#DirectLake)</sup>|--|❌|✔️|
|Create & Edit Partitions|✔️|✔️<sup>[1](#DirectLake)</sup>|--|❌|✔️|
|Create & Edit Columns|✔️|✔️<sup>[1](#DirectLake)</sup>|--|✔️|✔️|
|Create & Edit Calculated Tables|✔️|❌|--|✔️|✔️|
|Create & Edit Calculated Columns|✔️|❌|--|✔️|✔️|
|Create & Edit Calculation Groups|✔️|❌|--|✔️|✔️|
|Create & Edit Relationships|✔️|✔️|--|✔️|✔️|
|Create & Edit Roles|✔️|❌|--|✔️|✔️|--
|Create & Edit Perspectives|✔️|✔️|--|✔️|✔️|
|Create & Edit Translations|✔️|✔️|--|✔️|✔️|
|Use Best Practice Analyzer|✔️|✔️|--|✔️|✔️|
|Create Diagrams<sup>[2](#TE3Prem)</sup>|✔️|✔️|--|✔️|✔️|
|Use Preview Data<sup>[2](#TE3Prem)</sup>|✔️|✔️|--|✔️|✔️|
|Use Pivot Grids<sup>[2](#TE3Prem)</sup>|✔️|✔️|--|✔️|✔️|
|Use DAX Queries<sup>[2](#TE3Prem)</sup>|✔️|✔️|--|✔️|✔️|
|Use DAX Debugger<sup>[2](#TE3Prem)</sup>|✔️|✔️|--|✔️|✔️|
|Use Vertipac Analyzer<sup>[2](#TE3Prem)</sup>|✔️|✔️|--|✔️|✔️|
|Process Model and Tables<sup>[2](#TE3Prem)</sup>|✔️|N/A|--|❌|❌|
|Delete Objects|✔️|✔️|--|✔️|✔️|




<a name="DirectLake">1</a> - The partition must be an Entity Partition to work correctly.

<a name="TE3Prem">2</a> - Tabular Editor 3 features only. Operations performed through the XMLA endpoint requires a Business or Enterprise license. [More information](xref:editions).

## Unsupported Dataset
The following datasets types do not support XMLA write operations and can as such not be used by Tabular Editor.

- Datasets based on a live connection to an Azure Analysis Services or SQL Server Analysis Services model.
- Datasets based on a live connection to a Power BI dataset in another workspace. Please refer to [Intro to datasets across workspaces](../connect-data/service-datasets-across-workspaces.md).
- Datasets with Push data.
- Datasets stored in My Workspace.
- Excel workbook datasets.