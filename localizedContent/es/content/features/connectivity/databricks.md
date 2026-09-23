---
uid: connect-databricks
title: Conectarse a Databricks
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

# Conectarse a Databricks

Empieza en **Modelo > Importar tablas...** y elige un origen de Databricks. Cada método de autenticación necesita el **Host** y el **HTTP Path** del SQL Warehouse o del clúster; Databricks muestra ambos en la página de detalles de conexión del recurso de cómputo.

![El cuadro de diálogo Conectarse a Databricks, con Azure AD seleccionado como tipo de autenticación y un botón Iniciar sesión al lado](~/content/assets/images/features/connectivity/databricks-connection.png)

## Métodos de autenticación

| Autenticación                       | Qué debes proporcionar                                              | Reconexión sin supervisión     |
| ----------------------------------- | ------------------------------------------------------------------- | ------------------------------ |
| **Token de acceso**                 | Un token de acceso personal de Databricks                           | Sí, hasta que caduque el token |
| **Nombre de usuario / contraseña**  | Nombre de usuario y contraseña                                      | Sí                             |
| **Azure AD**                        | Inicio de sesión con Microsoft Entra ID                             | Solo para Azure Databricks     |
| **OAuth (OIDC)** | Inicio de sesión en el navegador                                    | No                             |
| **OAuth (M2M)**  | Un identificador de cliente y un secreto de una entidad de servicio | Sí                             |

> [!NOTE]
> **Azure AD** solo está disponible para Azure Databricks. En un Workspace de Databricks alojado en cualquier otro lugar, usa una de las otras cuatro opciones.

Para una actualización programada, **OAuth (M2M)** suele ser la opción habitual: es una entidad de servicio, por lo que nada expira si una persona deja la organización.

## Dónde se almacenan las credenciales

Las credenciales que introduces aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, por lo que no se incluyen en el control de código fuente y cualquier colega que abra el mismo modelo tendrá que proporcionar las suyas.

La expresión M generada solo especifica el servidor y el objeto. Nunca contiene una contraseña, un token ni una clave.
