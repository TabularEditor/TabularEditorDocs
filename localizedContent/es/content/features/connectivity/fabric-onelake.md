---
uid: connect-onelake
title: Conectar con Fabric y OneLake
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

# Conectar con Fabric y OneLake

El conector de Fabric enumera los elementos de Lakehouse, Warehouse, base de datos SQL y base de datos reflejada en los Workspaces de Fabric a los que puedes acceder, e importa tablas desde ellos. Los catálogos reflejados de Azure Databricks aparecen como bases de datos reflejadas. Abre el cuadro de diálogo desde **Modelo > Importar tablas...** y elige **Microsoft Fabric Lakehouse**, **Microsoft Fabric Warehouse**, **Microsoft Fabric SQL Database** o **Microsoft Fabric Mirrored Database**.

![El cuadro de diálogo "Conectar a un Lakehouse", que muestra elementos del catálogo de OneLake por nombre, tipo, propietario y ubicación](~/content/assets/images/features/connectivity/onelake-connection.png)

## Campos de conexión

| Campo                                                                 | Descripción                                                                                                                                                                                  |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Iniciar sesión...** | Inicia sesión en el servicio de Power BI con Microsoft Entra ID                                                                                                                              |
| **Elementos del catálogo de OneLake**                                 | Los elementos del tipo seleccionado en los Workspaces a los que puedes acceder, con sus campos **Nombre**, **Tipo**, **Propietario** y **Ubicación**. Selecciona un elemento |

## Autenticación

**Iniciar sesión...** inicia el proceso de inicio de sesión de Microsoft Entra ID en el navegador. Si no aparece ningún elemento después de iniciar sesión, tu cuenta no tiene acceso a ningún Workspace que los contenga, y un administrador del Workspace debe concederte ese acceso en Fabric.

Tabular Editor guarda la configuración de conexión y las credenciales en el archivo de opciones de usuario (consulta [Dónde se almacenan las credenciales](xref:connectivity#where-credentials-are-stored)).

## Import y Direct Lake

En la última página del Asistente para importar tablas, eliges si las tablas seleccionadas se crean en modo Import mode o en modo Direct Lake:

- Las tablas en modo Import leen su esquema a través del punto de conexión de análisis SQL del elemento. Consulta [Elegir objetos para importar](xref:import-tables#choosing-objects-to-import).
- Las tablas en modo Direct Lake leen directamente desde OneLake. Consulta @direct-lake-sql-model.
