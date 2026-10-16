---
uid: connect-databricks
title: Conectar a Databricks
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

# Conectar a Databricks

El conector de Databricks se conecta a los SQL Warehouse y clústeres en Azure Databricks y a los Workspace de Databricks en otras nubes. Solo está disponible como un Data source implícito (consulta [Data sources heredados, estructurados e implícitos](xref:connectivity#legacy-structured-and-implicit-data-sources)).

Selecciona **Modelo > Importar tablas...** y elige un origen de Databricks para abrir el cuadro de diálogo. @connecting-to-azure-databricks explica paso a paso una importación desde Azure Databricks.

![El cuadro de diálogo Conectar a Databricks, con Azure AD seleccionado como tipo de autenticación y un botón Iniciar sesión al lado](~/content/assets/images/features/connectivity/databricks-connection.png)

## Requisitos del sistema

Instala el [controlador ODBC de Databricks](https://www.databricks.com/spark/odbc-drivers-download) en tu equipo (consulta [Requisitos previos](xref:connecting-to-azure-databricks#prerequisites) en el tutorial para ver los controladores compatibles).

## Campos de conexión

| Campo                                                                                                           | Descripción                                                                                                                                                                                                                 |
| --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nombre de host del servidor**                                                                                 | El nombre de host de la pestaña **Detalles de la conexión** del recurso de cómputo en Databricks. Obligatorio                                                                                               |
| **Ruta HTTP**                                                                                                   | La ruta HTTP de la misma pestaña. Obligatorio                                                                                                                                                               |
| **Tipo**                                                                                                        | La opción de autenticación. Consulta [Autenticación](#authentication)                                                                                                                                       |
| **Nombre de usuario** y **Contraseña**, o **Iniciar sesión...** | Las credenciales de la opción de autenticación seleccionada. Los campos cambian según la opción                                                                                                             |
| **Avanzado**                                                                                                    | Configuración opcional: **Catálogo predeterminado**, **Base de datos**, **Detección automática del proxy**, **Etiquetas de consulta**, **Implementación** y **Modo de compatibilidad de BI de Metric View** |

## Autenticación

| Autenticación                       | Lo que debe proporcionar                                                                       | Inicio de sesión interactivo |
| ----------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------- |
| **Token de acceso**                 | Un token de acceso personal de Databricks. Cuando caduque, introduce uno nuevo | No                           |
| **Nombre de usuario / Contraseña**  | Nombre de usuario y contraseña                                                                 | No                           |
| **Azure AD**                        | Inicio de sesión con Microsoft Entra ID. Disponible solo para Azure Databricks | Sí                           |
| **OAuth (OIDC)** | Inicio de sesión mediante el navegador                                                         | Sí                           |
| **OAuth (M2M)**  | Un ID de cliente y un secreto de cliente del principal de servicio                             | No                           |

Para conexiones desatendidas, usa **OAuth (M2M)**, que se autentica como un principal de servicio.

Tabular Editor guarda la configuración de conexión y las credenciales en tu archivo de opciones de usuario (consulta [Dónde se almacenan las credenciales](xref:connectivity#where-credentials-are-stored)).
