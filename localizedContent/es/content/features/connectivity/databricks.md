---
uid: connect-databricks
title: Conectar a Databricks
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

# Conectar a Databricks

Empiece por **Modelo > Importar tablas...** y elija un origen de Databricks. Todos los métodos de autenticación requieren el **Host** y el **HTTP Path** del SQL Warehouse o del clúster. Databricks muestra ambos en la página de detalles de conexión del recurso de computación.

![Cuadro de diálogo Conectar a Databricks, con Azure AD seleccionado como tipo de autenticación y un botón Iniciar sesión a su lado](~/content/assets/images/features/connectivity/databricks-connection.png)

## Métodos de autenticación

| Autenticación                       | Lo que debe proporcionar                                  | Se reconecta sin supervisión   |
| ----------------------------------- | --------------------------------------------------------- | ------------------------------ |
| **Token de acceso**                 | Un token de acceso personal de Databricks                 | Sí, hasta que caduque el token |
| **Nombre de usuario / Contraseña**  | Nombre de usuario y contraseña                            | Sí                             |
| **Azure AD**                        | Inicio de sesión con Microsoft Entra ID                   | Solo para Azure Databricks     |
| **OAuth (OIDC)** | Inicio de sesión mediante el navegador                    | No                             |
| **OAuth (M2M)**  | Un ID de cliente y un secreto de un principal de servicio | Sí                             |

> [!NOTE]
> **Azure AD** solo está disponible para Azure Databricks. En un Workspace de Databricks hospedado en cualquier otro lugar, usa cualquiera de las otras cuatro.

Para una actualización programada, **OAuth (M2M)** suele ser la opción habitual: es un principal de servicio, así que nada caduca cuando una persona deja la empresa.

## Dónde se almacenan las credenciales

Las credenciales que introduzcas aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, así que no se guardan en el control de versiones y cualquier compañero que abra el mismo modelo tendrá que introducir las suyas.

La expresión M generada solo especifica el servidor y el objeto. Nunca contiene una contraseña, un token ni una clave.
