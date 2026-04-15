---
uid: semantic-model-types
title: Tipos de modelos semánticos de Power BI
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

# Tipos de modelos semánticos

Tabular Editor puede trabajar con varios tipos de modelos. A continuación encontrarás un resumen de qué tipos de modelo funcionan con Tabular Editor y qué capacidades se pueden usar con cada tipo de modelo.

| Model Type                                           | Import | Direct Query | Direct Lake en OneLake                  | Direct Lake en SQL                         | .pbix | .pbip |
| ---------------------------------------------------- | ------ | ------------ | --------------------------------------- | ------------------------------------------ | --------------------- | --------------------- |
| Connect in Tabular Editor                            | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Create new model                                     | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Write Measures                                       | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Create & Edit Tables             | ✔️     | ✔️           | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| Create & Edit Partitions         | ✔️     | ✔️           | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| Create & Edit Columns            | ✔️     | ✔️           | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| Create & Edit Calculated Tables  | ✔️     | ✔️           | ✔️<sup>[2](#DirectLakeCalculated)</sup> | ✔️<sup>[4](#DirectLakeSQLCalculated)</sup> | ✔️                    | ✔️                    |
| Create & Edit Calculated Columns | ✔️     | ✔️           | ❌                                       | ❌                                          | ✔️                    | ✔️                    |
| Create & Edit Calculation Groups | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Create & Edit Relationships      | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Create & Edit Roles              | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Create & Edit Perspectives       | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Create & Edit Translations       | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use Best Practice Analyzer                           | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Edit All TOM properties                              | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Create Diagrams<sup>[3](#TE3Prem)</sup>              | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use Preview Data<sup>[3](#TE3Prem)</sup>             | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use Pivot Grids<sup>[3](#TE3Prem)</sup>              | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use DAX Queries<sup>[3](#TE3Prem)</sup>              | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use DAX Debugger<sup>[3](#TE3Prem)</sup>             | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Use VertiPaq Analyzer<sup>[3](#TE3Prem)</sup>        | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Process Model and Tables<sup>[3](#TE3Prem)</sup>     | ✔️     | ✔️           | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Delete Objects                                       | ✔️     | ✔️           | ✔️                                      | ✔️                                         |                       |                       |

**Leyenda:**

- ✔️: Compatible
- ❌: No compatible

<a name="DirectLake">1</a> - The table partition must be an Entity Partition to work correctly. Direct Lake models can only have one partition per table. <a name="DirectLakeCalculated">2</a> - Calculated Tables cannot refer to Direct Lake on OneLake tables or columns. Calculation groups, what-if parameters and field parameters are supported.

<a name="TE3Prem">3</a> - Solo funciones de Tabular Editor 3. Las operaciones realizadas a través del punto de conexión XMLA requieren una licencia Business o Enterprise. [Más información](xref:editions). <a name="DirectLakeSQLCalculated">4</a> - Direct Lake on SQL only supports calculation groups, what-if parameters and field parameters, which implicitly create calculated tables. General calculated tables are not supported.

> [!NOTE]
> The June 2025 release of Power BI Desktop lifted all modeling limitations for third-party tools. Prior to that, various modeling operations were not supported. See [Power BI Desktop Limitations](xref:desktop-limitations).

> [!TIP]
> Para más detalles sobre las restricciones de los modelos Direct Lake, consulta la [documentación de Direct Lake](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview) de Microsoft

## Tipos de modelos semánticos no compatibles

The following semantic model types are unsupported, as they do not support XMLA write operations.

- Reports basados en una conexión en vivo con un modelo de Azure Analysis Services o SQL Server Analysis Services.
- Reports basados en una conexión en directo a un dataset de Power BI.
- Modelos con datos push.
- Modelos almacenados en Mi Workspace de Power BI.
- Modelos almacenados en el Workspace Pro de Power BI.
- Modelos semánticos predeterminados de Direct Lake. As of September 2025, Power BI no longer automatically creates default semantic models when a warehouse, lakehouse or mirrored item is created. By November 2025, all existing default semantic models were disconnected from their items and became independent semantic models. It is possible to connect to a default semantic model, but it is not possible to change it through the XMLA endpoint.
- Modelos semánticos de libros de Excel.