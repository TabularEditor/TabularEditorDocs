---
uid: connect-ssas
title: Conectar y desplegar en Analysis Services
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Conectar y desplegar en Analysis Services

Puedes abrir un modelo semántico directamente desde un servidor en lugar de desde un archivo, trabajar en él y guardar de nuevo los cambios en el servidor. Esto incluye SQL Server Analysis Services, Azure Analysis Services y el punto de conexión XMLA de Power BI / Fabric.

## Abrir un modelo desde un servidor

Selecciona **Archivo > Abrir > Modelo desde BD...** (**Ctrl+Mayús+O**) e introduce la dirección del servidor. Luego, Tabular Editor muestra las bases de datos de ese servidor para que puedas elegir cuál cargar.

- Para **SQL Server Analysis Services**, usa el nombre de la instancia; por ejemplo, `localhost` o `myserver\\tabular`.
- Para **Azure Analysis Services**, usa el nombre completo de la instancia, que empieza por `asazure://`.
- Para el **punto de conexión XMLA de Power BI / Fabric**, usa la cadena de conexión del Workspace, que empieza por `powerbi://`.
- La lista desplegable **Instancia local** muestra las instancias en ejecución de Power BI Desktop y los Workspaces Integrados de Visual Studio, de modo que puedas conectarte a una sin conocer su puerto.

@xmla-as-connectivity explica en detalle el cuadro de diálogo de conexión, incluidos los modos de autenticación, las propiedades avanzadas de la cadena de conexión, el color de la barra de estado para cada conexión y qué comprobar cuando falla una conexión. @load-save-model enumera todas las formas de abrir un modelo.

## Guardar los cambios

**Archivo > Guardar** (**Ctrl+S**) guarda los cambios en la base de datos conectada. Las herramientas cliente, como Excel, Power BI y DAX Studio, los ven de inmediato. Según lo que hayas cambiado, puede que sea necesario recalcular algunos objetos antes de volver a consultar el modelo.

Si prefieres guardar en disco una copia de un modelo en modo conectado, usa **Archivo > Guardar como...** o **Archivo > Guardar en carpeta...**.

## Desplegar en otra base de datos

Al guardar, se actualiza la base de datos a la que estás conectado. Para enviar el modelo cargado a un servidor o una base de datos diferentes, usa en su lugar el Asistente de implementación, descrito en @deployment.

## Editar un modelo de Power BI Desktop

Tabular Editor puede conectarse a una instancia en ejecución de Power BI Desktop mediante la lista desplegable **Instancia local**. A partir de la actualización de Power BI Desktop de junio de 2025, ya no hay operaciones de escritura no admitidas, por lo que las herramientas de terceros pueden modificar libremente el modelo semántico alojado en Power BI Desktop. En versiones anteriores, algunas operaciones están restringidas; consulta @desktop-limitations y @desktop-integration.
