---
uid: connect-sql-server
title: Conectar a SQL Server
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

# Conectar a SQL Server

El conector de SQL Server permite conectarse a SQL Server, Azure SQL Database, Azure SQL Managed Instance y Azure Synapse Analytics. Ve a **Modelo > Importar tablas...** y elige un origen de SQL Server.

![El cuadro de diálogo Conectarse a SQL Server, con Azure Active Directory - Universal con MFA seleccionado en la lista de autenticación](~/content/assets/images/features/connectivity/sql-server-connection.png)

## Campos de conexión

| Campo                                                                     | Descripción                                                                                                                                                                                                           |
| ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nombre del servidor**                                                   | El servidor o la instancia a la que deseas conectarte                                                                                                                                                                 |
| **Autenticación**                                                         | La opción de autenticación. Consulta [Autenticación](#authentication)                                                                                                                                 |
| **Nombre de usuario** y **contraseña**                                    | Las credenciales de la opción de autenticación seleccionada                                                                                                                                                           |
| **Recordar contraseña**                                                   | Guarda la contraseña para la próxima conexión. Si lo desmarcas, se te pedirá la contraseña la próxima vez que importes, obtengas una vista previa o actualices el esquema de la tabla                 |
| **Database**                                                              | La base de datos desde la que importar. Selecciona **< Examinar servidor... >** para mostrar las bases de datos del servidor |
| **Cifrar la conexión**                                                    | Requiere TLS para la conexión. Consulta [Cifrado](#encryption)                                                                                                                                        |
| **Opciones avanzadas...** | Abre las propiedades completas de la cadena de conexión                                                                                                                                                               |

## Autenticación

| Autenticación                                      | Qué debes proporcionar                                                                                                               | Inicio de sesión interactivo |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------- |
| **Autenticación de SQL Server**                    | Nombre de usuario y contraseña de un inicio de sesión SQL definido en el servidor                                                    | No                           |
| **Autenticación de Windows**                       | Nada. Usa la cuenta de Windows con la que se ejecuta Tabular Editor                                                  | No                           |
| **Azure Active Directory - Universal con MFA**     | Inicio de sesión mediante el navegador                                                                                               | Sí                           |
| **Azure Active Directory - Contraseña**            | Nombre de usuario y contraseña de una cuenta de directorio. Da error si la cuenta requiere autenticación multifactor | No                           |
| **Azure Active Directory - Integrada**             | Nada. Usa la cuenta de directorio con la que has iniciado sesión en Windows, en un equipo unido al directorio        | No                           |
| **Azure Active Directory - Principal de servicio** | ID de aplicación (cliente) y secreto                                                                              | No                           |

Para uso desatendido, selecciona **Azure Active Directory - Entidad de servicio**. Cuando seleccionas **Autenticación de Windows** o **Azure Active Directory - Integrada**, **Nombre de usuario**, **Contraseña** y **Recordar contraseña** se deshabilitan, y **Nombre de usuario** muestra tu cuenta de Windows como `DOMAIN\user`.

Tabular Editor guarda la configuración de conexión y las credenciales en tu archivo de opciones de usuario (consulta [Dónde se almacenan las credenciales](xref:connectivity#where-credentials-are-stored)).

## Cifrado

**Cifrar conexión** está seleccionado de forma predeterminada y Azure SQL lo requiere.

Si tu equipo no confía en el certificado del servidor, aparece el mensaje **Certificado de SQL Server no es de confianza**. Selecciona **Aceptar** para confiar en el certificado y conectarte. El aviso no aparece si el servidor tiene un certificado en el que tu equipo confía o si desactivas **Cifrar conexión**.
