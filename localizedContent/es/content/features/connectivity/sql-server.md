---
uid: connect-sql-server
title: Conectar a SQL Server
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

# Conectar a SQL Server

Abarca SQL Server, Azure SQL Database, Azure SQL Managed Instance y Azure Synapse. Ve a **Modelo > Importar tablas...** y elige un origen de SQL Server.

![El cuadro de diálogo Conectar a SQL Server, con Azure Active Directory - Universal con MFA seleccionado en la lista de Autenticación](~/content/assets/images/features/connectivity/sql-server-connection.png)

## Métodos de autenticación

| Autenticación                                    | Qué debes proporcionar                                             | Notas                                                                                                                                   |
| ------------------------------------------------ | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Autenticación de SQL Server**                  | Nombre de usuario y contraseña                                     | Un inicio de sesión definido en el propio servidor, no en tu directorio                                                                 |
| **Autenticación de Windows**                     | Nada                                                               | Usa la cuenta de Windows con la que se está ejecutando Tabular Editor                                                                   |
| **Azure Active Directory - Universal con MFA**   | Inicio de sesión en el navegador                                   | Es el único modo que solicita intervención del usuario. Úsalo para un trabajo interactivo, no para una tarea programada |
| **Azure Active Directory - Contraseña**          | Nombre de usuario y contraseña                                     | Una cuenta de directorio. Falla cuando la cuenta requiere autenticación multifactor                                     |
| **Azure Active Directory - Integrada**           | Nada                                                               | Usa la cuenta del directorio con la que has iniciado sesión en Windows, siempre que el equipo esté unido al directorio                  |
| **Azure Active Directory - Entidad de servicio** | ID de aplicación (cliente) y secreto de cliente | La opción habitual para la actualización desatendida                                                                                    |

Los dos modos de autenticación integrada no requieren nombre de usuario ni contraseña, y Tabular Editor borra ambos campos al seleccionar uno de ellos.

## Cifrado

**Cifrar conexión** controla si la conexión requiere TLS. Azure SQL lo requiere. Déjalo activado, salvo que te estés conectando a un servidor local sin certificado; en ese caso, la conexión fallará con un error de certificado hasta que instales uno o desactives esta opción.

## Guardar la contraseña

**Guardar contraseña** almacena la contraseña para la próxima vez. Si la desmarcas, se te volverá a pedir la próxima vez que el modelo necesite el origen de datos.

## Dónde se almacenan las credenciales

Las credenciales que introduzcas aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas de modo que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, así que no se incluyen en el control de código fuente y, si un compañero abre el mismo modelo, tendrá que proporcionar las suyas.

La expresión M generada solo incluye el servidor y el objeto. Nunca contiene una contraseña, un token ni una clave.
