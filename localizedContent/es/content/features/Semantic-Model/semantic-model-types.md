---
uid: semantic-model-types
title: Tipos de modelos semánticos de Power BI
author: Morten Lønskov
updated: 2025-06-19
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Negocios
          full: true
        - edition: Empresarial
          full: true
---

# Tipos de modelos semánticos

Tabular Editor puede trabajar con varios tipos de modelos. A continuación encontrarás un resumen de qué tipos de modelo funcionan con Tabular Editor y qué capacidades se pueden usar con cada tipo de modelo.

| Tipo de modelo                                     | Importación | Direct Query | Direct Lake en OneLake                  | Direct Lake en SQL            | .pbix | .pbip |
| -------------------------------------------------- | ----------- | ------------ | --------------------------------------- | ----------------------------- | --------------------- | --------------------- |
| Conectar en Tabular Editor                         | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Crear nuevo modelo                                 | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Escribir medidas                                   | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Crear y editar tablas                              | ✔️          | ✔️           | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup> | ✔️                    | ✔️                    |
| Crear y editar particiones                         | ✔️          | ✔️           | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup> | ✔️                    | ✔️                    |
| Crear y editar columnas                            | ✔️          | ✔️           | ✔️<sup>[1](#DirectLake)</sup>           | ✔️<sup>[1](#DirectLake)</sup> | ✔️                    | ✔️                    |
| Crear y editar tablas calculadas                   | ✔️          | ✔️           | ✔️<sup>[2](#DirectLakeCalculated)</sup> | ✔️                            | ✔️                    | ✔️                    |
| Crear y editar columnas calculadas                 | ✔️          | ✔️           | ✔️<sup>[2](#DirectLakeCalculated)</sup> | ✔️                            | ✔️                    | ✔️                    |
| Crear y editar grupos de cálculo                   | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Crear y editar relaciones                          | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Crear y editar roles                               | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Crear y editar perspectivas                        | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Crear y editar traducciones                        | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Usar Best Practice Analyzer                        | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Editar todas las propiedades de TOM                | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Crear diagramas<sup>[3](#TE3Prem)</sup>            | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Usar vista previa de datos<sup>[3](#TE3Prem)</sup> | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Usar Pivot Grids<sup>[3](#TE3Prem)</sup>           | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Usar consultas DAX<sup>[3](#TE3Prem)</sup>         | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Usar el depurador de DAX<sup>[3](#TE3Prem)</sup>   | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Usar Vertipac Analyzer<sup>[3](#TE3Prem)</sup>     | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Procesar modelo y tablas<sup>[3](#TE3Prem)</sup>   | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |
| Eliminar objetos                                   | ✔️          | ✔️           | ✔️                                      | ✔️                            | ✔️                    | ✔️                    |

**Leyenda:**

- ✔️: Compatible
- ❌: No compatible

<a name="DirectLake">1</a> - La partición de la tabla debe ser una partición de entidad para funcionar correctamente, y los modelos Direct Lake solo pueden tener una partición. <a name="DirectLakeCalculated">2</a> - Las tablas y columnas calculadas no pueden hacer referencia a tablas o columnas Direct Lake en OneLake.

<a name="TE3Prem">3</a> - Solo funciones de Tabular Editor 3. Las operaciones realizadas a través del punto de conexión XMLA requieren una licencia Business o Enterprise. [Más información](xref:editions).

> [!NOTE]
> En la versión de junio de 2025 de Power BI Desktop, se eliminaron todas las limitaciones de modelado para herramientas de terceros. Antes de eso, no se admitían varias operaciones de modelado. Consulta [Limitaciones de Power BI Desktop](xref:desktop-limitations)

> [!TIP]
> Para más detalles sobre las restricciones de los modelos Direct Lake, consulta la [documentación de Direct Lake](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview) de Microsoft

## Tipos de modelos semánticos no compatibles

Los siguientes tipos de modelos semánticos no son compatibles, ya que no admiten operaciones de escritura XMLA.

- Reports basados en una conexión en vivo con un modelo de Azure Analysis Services o SQL Server Analysis Services.
- Reports basados en una conexión en directo a un dataset de Power BI.
- Modelos con datos push.
- Modelos almacenados en Mi Workspace de Power BI.
- Modelos almacenados en el Workspace Pro de Power BI.
- Modelos semánticos predeterminados de Direct Lake. (Es posible conectarse a un dataset predeterminado, pero no es posible cambiarlo a través del punto de conexión XMLA)
- Modelos semánticos de libros de Excel.