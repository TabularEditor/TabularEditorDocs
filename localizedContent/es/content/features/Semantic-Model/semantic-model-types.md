---
uid: semantic-model-types
title: Tipos de modelos semánticos de Power BI
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


# Tipos de modelos semánticos

Tabular Editor puede trabajar con varios tipos de modelos diferentes. A continuación, se ofrece una visión general de los tipos de modelos que funcionan con Tabular Editor y de las funciones que pueden utilizarse con cada tipo de modelo. 


|Tipo de modelo|Importación|Consulta directa|Direct Lake en OneLake|Direct Lake en SQL|.pbix|.pbip|
|---|---|---|---|---|---|---|
|Conectar en Tabular Editor|✔️|✔️|✔️|✔️|✔️| |
|Crear nuevo modelo|✔️|✔️|✔️|✔️|✔️|✔️|
|Escribir medidas|✔️|✔️|✔️|✔️|✔️|✔️|
|Crear y editar tablas|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|Crear y editar particiones|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|Crear y editar columnas|✔️|✔️|✔️<sup>[1](#DirectLake)</sup>|✔️<sup>[1](#DirectLake)</sup>|✔️|✔️|
|Crear y editar tablas calculadas|✔️|✔️|✔️<sup>[2](#DirectLakeCalculated)</sup>|✔️<sup>[4](#DirectLakeSQLCalculated)</sup>|✔️|✔️|
|Crear y editar columnas calculadas|✔️|✔️|✔️<sup>[5](#DirectLakeCalcColumn)</sup>|❌|✔️|✔️|
|Crear y editar grupos de cálculos|✔️|✔️|✔️|✔️|✔️| |
|Crear y editar relaciones|✔️|✔️|✔️|✔️|✔️| |
|Crear y editar roles|✔️|✔️|✔️|✔️|✔️|✔️|
|Crear y editar perspectivas|✔️|✔️|✔️|✔️|✔️|✔️|
|Crear y editar traducciones|✔️|✔️|✔️|✔️|✔️|✔️|
|Usar Best Practice Analyzer|✔️|✔️|✔️|✔️|✔️| |
|Editar todas las propiedades de TOM|✔️|✔️|✔️|✔️|✔️|✔️|
|Crear diagramas<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Usar datos de vista previa<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Usar tablas dinámicas<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Usar consultas DAX<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Usar el depurador de DAX<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Usar VertiPaq Analyzer<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Procesar modelo y tablas<sup>[3](#TE3Prem)</sup>|✔️|✔️|✔️|✔️|✔️|✔️|
|Eliminar objetos|✔️|✔️|✔️|✔️| | |

**Leyenda:**
- ✔️: Compatible 
- ❌: No admitido


<a name="DirectLake">1</a> - La partición de la tabla debe ser una partición de entidad para funcionar correctamente. Los modelos Direct Lake solo pueden tener una partición por tabla.
<a name="DirectLakeCalculated">2</a> - Las tablas calculadas no pueden hacer referencia a Direct Lake en tablas o columnas de OneLake. Se admiten grupos de cálculos, parámetros de simulación y parámetros de campo.

<a name="TE3Prem">3</a> - Solo funciones de Tabular Editor 3. Las operaciones realizadas a través del punto de conexión XMLA requieren una licencia Business o Enterprise. [Más información](xref:editions).
<a name="DirectLakeSQLCalculated">4</a> - Direct Lake en SQL solo admite grupos de cálculo, parámetros «what-if» y parámetros de campo, que crean implícitamente tablas calculadas. No se admiten tablas calculadas generales.
<a name="DirectLakeCalcColumn">5</a> - Función de vista previa. Las columnas calculadas de las tablas de Direct Lake en OneLake deben usar el contexto de expresión «UserContext». Se evalúan en el momento de la consulta y no se materializan, por lo que no se pueden usar como claves de relación. Consulte [Directrices de Direct Lake](xref:direct-lake-guidance#calculated-columns-on-direct-lake-on-onelake) para obtener más detalles.

>[!NOTE]
> La versión de junio de 2025 de Power BI Desktop eliminó todas las limitaciones de modelado para herramientas de terceros. Antes de eso, no se admitían varias operaciones de modelado. Consulte [Limitaciones de Power BI Desktop](xref:desktop-limitations).

>[!TIP]
> Para obtener más información sobre las restricciones de los modelos Direct Lake, consulte la [documentación de Direct Lake](https://learn.microsoft.com/fabric/fundamentals/direct-lake-overview) de Microsoft.

## Tipos de modelos semánticos no admitidos
Los siguientes tipos de modelos semánticos no son compatibles, ya que no admiten operaciones de escritura XMLA.

- Informes basados en una conexión en tiempo real a un modelo de Azure Analysis Services o de SQL Server Analysis Services.
- Informes basados en una conexión en tiempo real a un conjunto de datos de Power BI.
- Modelos con datos push.
- Modelos almacenados en Mi área de trabajo de Power BI.
- Modelos almacenados en el área de trabajo de Power BI Pro.
- Modelos semánticos predeterminados de Direct Lake. A partir de septiembre de 2025, Power BI ya no creará automáticamente modelos semánticos predeterminados cuando se cree un Warehouse, un Lakehouse o un elemento reflejado. En noviembre de 2025, todos los modelos semánticos predeterminados existentes se desconectaron de sus elementos y se convirtieron en modelos semánticos independientes. Es posible conectarse a un modelo semántico predeterminado, pero no es posible modificarlo a través del punto de conexión XMLA.
- Modelos semánticos de libros de Excel.