---
uid: conectividad
title: Conectividad
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Conectividad

Tabular Editor 3 autentica cada una de estas conexiones de forma independiente:

- **El modelo semántico que editas**, en SQL Server Analysis Services, Azure Analysis Services o un Workspace de Power BI o Fabric, a través de XMLA. Consulta @xmla-as-connectivity y @connect-ssas.
- **Los Data sources desde los que el modelo importa datos**, mediante el [Asistente para importar tablas](xref:import-tables). En las páginas de esta sección se describen estas conexiones.

## Fuentes de datos

Cada origen tiene su propio cuadro de diálogo de conexión:

- @connect-sql-server: SQL Server, Azure SQL Database, Azure SQL Managed Instance y Azure Synapse Analytics
- @connect-snowflake: Snowflake, incluida la autenticación mediante par de claves
- @connect-databricks: Azure Databricks y Databricks en otras nubes
- @connect-oracle: bases de datos Oracle mediante el proveedor OLE DB de Oracle
- @connect-odbc: cualquier origen con un controlador ODBC, incluidos PostgreSQL, MySQL, MariaDB e IBM Db2
- @connect-oledb: cualquier origen con un proveedor OLE DB
- @connect-onelake: elementos de Fabric: Lakehouse, Warehouse, base de datos SQL y base de datos reflejada
- @connect-dataflows: Dataflow de Power BI

## Dónde se almacenan las credenciales

Tabular Editor guarda la configuración de conexión y las credenciales que introduces en un cuadro de diálogo de conexión en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`). Este archivo es específico de cada usuario y de cada modelo, y las credenciales que contiene se cifran con la API de protección de datos de Windows en el contexto de tu cuenta de usuario de Windows. Consulta @supported-files.

- Las credenciales no forman parte de los metadatos del modelo ni se incluyen en el control de versiones.
- Cada usuario proporciona sus propias credenciales en cada equipo.
- Las expresiones M generadas no contienen credenciales.

## Para qué se usan las credenciales

Tabular Editor usa las credenciales del cuadro de diálogo de conexión para conectarse al origen cuando importas tablas, obtienes una vista previa de los datos y actualizas el esquema de la tabla. Si la opción de autenticación no tiene inicio de sesión interactivo, Tabular Editor se conecta con las credenciales guardadas sin que se te solicite nada.

Las actualizaciones de datos en Analysis Services y Power BI usan las credenciales configuradas para el Data source en el modelo, en el servidor o en el servicio de Power BI. Establezca las credenciales que utiliza Analysis Services en las propiedades del Data source después de importar las tablas (consulte [Crear un nuevo Data source](xref:import-tables#creating-a-new-data-source)).

## Data sources heredados, estructurados e implícitos

Los tipos de Data sources disponibles en el asistente dependen del modelo:

- Los Data sources **heredados (proveedor)** están disponibles para todos los modelos, excepto para los modelos Direct Lake. Las credenciales se administran en el objeto de origen de datos del proveedor del Tabular Object Model (TOM) y se almacenan y cifran en el lado del servidor.
- **Los Data sources estructurados (Power Query)** están disponibles a partir del nivel de compatibilidad 1400 en adelante. Debe proporcionar de nuevo las credenciales cada vez que implemente en Analysis Services.
- Los Data sources **implícitos** están disponibles para los modelos de Power BI y Fabric. Los modelos Direct Lake solo usan Data sources implícitos. Con un Data source implícito, el modelo no tiene ningún objeto de Data source: las particiones de importación incluyen una expresión M que nombra el origen, las particiones Direct Lake hacen referencia a una expresión compartida y Power BI Desktop o el servicio de Power BI almacenan las credenciales.

Cuando el modelo no tiene ningún Data source, el asistente preselecciona el Data source implícito si está disponible; después, el Data source estructurado; y, por último, el Data source heredado.

Snowflake, Databricks y los Dataflows de Power BI solo están disponibles como Data sources implícitos. El asistente los oculta para los modelos que no admiten Data sources implícitos, como los modelos de Analysis Services (consulta [Tipos de Data sources de TOM](xref:import-tables#types-of-tom-data-sources)).
