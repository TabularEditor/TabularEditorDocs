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

| Tipo de modelo                                          | Import | DirectQuery | Direct Lake en OneLake                  | Direct Lake en SQL                         | .pbix | .pbip |
| ------------------------------------------------------- | ------ | ----------- | --------------------------------------- | ------------------------------------------ | --------------------- | --------------------- |
| Conectar en Tabular Editor                              | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Crear un modelo nuevo                                   | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Escribir medidas                                        | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Crear y editar tablas                                   | ✔️     | ✔️          | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| Crear y editar particiones                              | ✔️     | ✔️          | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| Crear y editar columnas                                 | ✔️     | ✔️          | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup>              | ✔️                    | ✔️                    |
| Crear y editar tablas calculadas                        | ✔️     | ✔️          | ✔️<sup>[2](#DirectLakeCalculated)</sup> | ✔️<sup>[4](#DirectLakeSQLCalculated)</sup> | ✔️                    | ✔️                    |
| Crear y editar columnas calculadas                      | ✔️     | ✔️          | ❌                                       | ❌                                          | ✔️                    | ✔️                    |
| Crear y editar grupos de cálculo                        | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Crear y editar relaciones                               | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Crear y editar roles                                    | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Crear y editar perspectivas                             | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Crear y editar traducciones                             | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Usar Best Practice Analyzer                             | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    |                       |
| Editar todas las propiedades de TOM                     | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Crear diagramas<sup>[3](#TE3Prem)</sup>                 | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Usar datos de vista previa<sup>[3](#TE3Prem)</sup>      | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Usar Pivot Grid<sup>[3](#TE3Prem)</sup>                 | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Usar consultas DAX<sup>[3](#TE3Prem)</sup>              | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Usar el depurador de DAX<sup>[3](#TE3Prem)</sup>        | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Usar el Analizador VertiPaq<sup>[3](#TE3Prem)</sup>     | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Procesar el modelo y las tablas<sup>[3](#TE3Prem)</sup> | ✔️     | ✔️          | ✔️                                      | ✔️                                         | ✔️                    | ✔️                    |
| Eliminar objetos                                        | ✔️     | ✔️          | ✔️                                      | ✔️                                         |                       |                       |

**Leyenda:**

- ✔️: Compatible
- ❌: No compatible

<a name="DirectLake">1</a> - La partición de la tabla debe ser una partición de entidad para funcionar correctamente. Los modelos Direct Lake solo pueden tener una partición por tabla. <a name="DirectLakeCalculated">2</a> - Las tablas calculadas no pueden hacer referencia a Direct Lake en tablas o columnas de OneLake. Se admiten los grupos de cálculo, los parámetros de hipótesis y los parámetros de campo.

<a name="TE3Prem">3</a> - Solo funciones de Tabular Editor 3. Las operaciones realizadas a través del punto de conexión XMLA requieren una licencia Business o Enterprise. [Más información](xref:editions). <a name="DirectLakeSQLCalculated">4</a> - Direct Lake en SQL solo admite grupos de cálculo, parámetros de hipótesis y parámetros de campo, que crean implícitamente tablas calculadas. No se admiten las tablas calculadas de uso general.

> [!NOTE]
> En la versión de junio de 2025 de Power BI Desktop se eliminaron todas las limitaciones de modelado para las herramientas de terceros. Antes de eso, no se admitían varias operaciones de modelado. Consulta [Limitaciones de Power BI Desktop](xref:desktop-limitations).

> [!TIP]
> Para más detalles sobre las restricciones de los modelos Direct Lake, consulta la [documentación de Direct Lake](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview) de Microsoft

## Tipos de modelos semánticos no compatibles

Los siguientes tipos de modelos semánticos no son compatibles, ya que no admiten operaciones de escritura XMLA.

- Reports basados en una conexión en vivo con un modelo de Azure Analysis Services o SQL Server Analysis Services.
- Reports basados en una conexión en directo a un dataset de Power BI.
- Modelos con datos push.
- Modelos almacenados en Mi Workspace de Power BI.
- Modelos almacenados en el Workspace Pro de Power BI.
- Modelos semánticos predeterminados de Direct Lake. Desde septiembre de 2025, Power BI ya no crea automáticamente modelos semánticos predeterminados al crear un Warehouse, un Lakehouse o un elemento reflejado. En noviembre de 2025, todos los modelos semánticos predeterminados existentes se desvincularon de sus elementos y pasaron a ser modelos semánticos independientes. Es posible conectarse a un modelo semántico predeterminado, pero no se puede modificar a través del punto de conexión XMLA.
- Modelos semánticos de libros de Excel.