---
uid: conectividad
title: Conectividad
author: Morten Lønskov
updated: 2026-09-21
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

Tabular Editor 3 se conecta a dos tipos distintos de elementos, y la autenticación es diferente en cada caso.

- **El modelo que estás editando**, en Analysis Services, Azure Analysis Services o en un Workspace de Power BI o Fabric, al que accedes mediante XMLA. Consulta @xmla-as-connectivity.
- **Los Data sources desde los que importa tu modelo**, a los que accedes mediante el [Asistente para importar tablas](xref:import-tables). Eso es lo que cubren las páginas siguientes.

## Dónde se almacenan las credenciales

Las credenciales se almacenan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`), cifradas con la clave de tu cuenta de Windows. No forman parte de los metadatos del modelo y nunca se incluyen en el control de código fuente. Consulta @supported-files.

Esto tiene una consecuencia que conviene conocer desde el principio: un compañero que abra el mismo modelo tendrá que proporcionar sus propias credenciales, y lo mismo ocurrirá si esa misma persona lo abre en otro equipo.

## Data sources heredados, estructurados e implícitos

Los métodos de autenticación disponibles también dependen de cómo el modelo almacene el Data source, y eso lo decide el modelo, no tú.

- Los Data sources **heredados (provider)** están disponibles para cualquier modelo, sea cual sea su nivel de compatibilidad. Las credenciales se almacenan en el servidor, dentro del Tabular Object Model.
- Los Data sources **estructurados (Power Query)** están disponibles a partir del nivel de compatibilidad 1400. Las credenciales deben volver a proporcionarse en cada implementación en Analysis Services.
- **Los Data sources implícitos** son los que usan los modelos de Power BI y Fabric, y un modelo Direct Lake no puede usar ningún otro. No hay ningún objeto Data source en los metadatos: la expresión M de la partición indica el origen, y las credenciales las guardan Power BI Desktop o el servicio de Power BI, no el modelo.

Cuando hay más de un tipo disponible, el asistente prefiere primero el implícito, luego el estructurado y, por último, el heredado.

Esta es también la razón por la que la lista de orígenes es más corta fuera de Power BI. Snowflake, Databricks y los Dataflow de Power BI solo son accesibles como Data sources implícitos, por lo que el asistente los omite cuando el modelo está en Analysis Services. Consulta [Tipos de Data sources de TOM](xref:import-tables#types-of-tom-data-sources).

Sea cual sea el tipo con el que acabe el modelo, las credenciales que _Tabular Editor_ usa para explorar el origen y leer su esquema son las que introduces en el cuadro de diálogo de conexión, y se guardan en el archivo `.tmuo` descrito anteriormente. Son independientes de las credenciales que Analysis Services o Power BI usan durante la actualización.
