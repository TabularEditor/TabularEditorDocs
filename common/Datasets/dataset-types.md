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
|Create Tables|✔️|✔️^1|--|✔️|✔️|
|Create Partitions|✔️|✔️^1|--|✔️|✔️|
|Create Calculated Tables|✔️|❌|--|✔️|✔️|
|Create Calc. Columns|✔️|❌|--|✔️|✔️|
|Create Calculation Groups|✔️|❌|--|✔️|✔️|
|Create Relationships|✔️|✔️|--|✔️|✔️|
|Create Roles|✔️|❌|--|✔️|✔️|--
|Create Perspectives|✔️|✔️|--|✔️|✔️|
|Create Translations|✔️|✔️|--|✔️|✔️|
|Create Diagrams**|✔️|✔️|--|✔️|✔️|
|Use Preview Data**|✔️|✔️|--|✔️|✔️|
|Use Pivot Grids**|✔️|✔️|--|✔️|✔️|
|Use DAX Queries**|✔️|✔️|--|✔️|✔️|
|Use DAX Debugger**|✔️|✔️|--|✔️|✔️|
|Use Vertipac Analyser**|✔️|✔️|--|✔️|✔️|
|Use Best Practice Analyser|✔️|✔️|--|✔️|✔️|
|Process Model and Tables**|✔️|N/A|--|❌|❌|
|Delete Objects|✔️|✔️|--|✔️|✔️|



** Tabular Editor 3 features, some dataset such a Direct Lake requires Enterprise license. 

[^1] The partition must be an Entity Partition to work correctly.

## Unsupported Dataset

The following datasets types do not support XMLA write operations and can as such not be used by Tabular Editor.

- Datasets based on a live connection to an Azure Analysis Services or SQL Server Analysis Services model.
- Datasets based on a live connection to a Power BI dataset in another workspace. Please refer to [Intro to datasets across workspaces](../connect-data/service-datasets-across-workspaces.md).
- Datasets with Push data.
- Datasets stored in My Workspace.
- Excel workbook datasets.