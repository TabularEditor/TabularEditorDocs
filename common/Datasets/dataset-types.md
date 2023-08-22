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

|Capability|Import|Direct Lake (Standalone) | Direct Lake (Default)|PBIX|PBIP|
|---|---|---|---|---|
|Connect in Tabular Editor|✔️|✔️|❌|✔️|✔️|
|Create new dataset|✔️|❌|--|✔️|✔️|
|Write Measures|✔️|✔️|--|✔️|✔️|
|Create Tables|✔️|✔️^1|--|❌|✔️|
|Create Partitions|✔️|✔️^1|--|❌|✔️|
|Create Calculated Tables|✔️|❌|--|✔️|✔️|
|Create Calculated Columns|✔️|❌|--|✔️|✔️|
|Create Calculation Groups|✔️|❌|--|✔️|✔️|
|Create Relationships|✔️|✔️|--|✔️|✔️|
|Create Roles|✔️|❌|--|✔️|✔️|--
|Create Perspectives|✔️|✔️|--|✔️|✔️|
|Create Translations|✔️|✔️|--|✔️|✔️|
|Use Diagrams^2|✔️|✔️|--|✔️|✔️|
|Use Preview Data^2|✔️|✔️|--|✔️|✔️|
|Use Pivot Grids^2|✔️|✔️|--|✔️|✔️|
|Use DAX Queries^2|✔️|✔️|--|✔️|✔️|
|Use DAX Debugger^2|✔️|✔️|--|✔️|✔️|
|Use Vertipac Analyser^2|✔️|✔️|--|✔️|✔️|
|Use Best Practice Analyser|✔️|✔️|--|✔️|✔️|
|Process Model and Tables^2|✔️|N/A|--|❌|❌|
|Delete Objects|✔️|✔️|--|✔️|✔️|

[^1] The partition must be an Entity Partition to work correctly.
[^2] Tabular Editor 3 features only. Operations performed through the XMLA endpoint requires a Business or Enterprise license. [More information](xref:editions).

## Unsupported Dataset

The following datasets types do not support XMLA write operations and can as such not be used by Tabular Editor.

- Datasets based on a live connection to an Azure Analysis Services or SQL Server Analysis Services model.
- Datasets based on a live connection to a Power BI dataset in another workspace. Please refer to [Intro to datasets across workspaces](../connect-data/service-datasets-across-workspaces.md).
- Datasets with Push data.
- Datasets stored in My Workspace.
- Excel workbook datasets.
