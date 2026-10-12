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

The SQL Server connector connects to SQL Server, Azure SQL Database, Azure SQL Managed Instance and Azure Synapse Analytics. Ve a **Modelo > Importar tablas...** y elige un origen de SQL Server.

![The Connect to SQL Server dialog, with Azure Active Directory - Universal with MFA selected in the Authentication list](~/content/assets/images/features/connectivity/sql-server-connection.png)

## Connection fields

| Campo                                                           | Descripción                                                                                                                                                                               |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Server name**                                                 | The server or instance to connect to                                                                                                                                                      |
| **Authentication**                                              | The authentication option. See [Authentication](#authentication)                                                                                                          |
| **User name** and **Password**                                  | The credentials for the selected authentication option                                                                                                                                    |
| **Remember password**                                           | Saves the password for the next connection. If you clear it, you're prompted for the password the next time you import, preview or update the table schema                |
| **Database**                                                    | The database to import from. Select **< Browse server... >** to list the databases on the server |
| **Encrypt connection**                                          | Requires TLS for the connection. See [Encryption](#encryption)                                                                                                            |
| **Advanced...** | Opens the full connection string properties                                                                                                                                               |

## Autenticación

| Autenticación                                      | Qué debes proporcionar                                                                                                  | Interactive sign-in |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------- |
| **Autenticación de SQL Server**                    | User name and password of a SQL login defined on the server                                                             | No                  |
| **Autenticación de Windows**                       | Nada. Uses the Windows account Tabular Editor runs as                                                   | No                  |
| **Azure Active Directory - Universal con MFA**     | Inicio de sesión mediante el navegador                                                                                  | Sí                  |
| **Azure Active Directory - Contraseña**            | User name and password of a directory account. Fails if the account requires multifactor authentication | No                  |
| **Azure Active Directory - Integrada**             | Nada. Uses the directory account you're signed in to Windows with, on a directory-joined machine        | No                  |
| **Azure Active Directory - Principal de servicio** | ID de aplicación (cliente) y secreto                                                                 | No                  |

For unattended use, select **Azure Active Directory - Service Principal**. When you select **Windows Authentication** or **Azure Active Directory - Integrated**, **User name**, **Password** and **Remember password** are disabled and **User name** shows your Windows account as `DOMAIN\user`.

Tabular Editor saves the connection settings and credentials in your user options file (see [Where credentials are stored](xref:connectivity#where-credentials-are-stored)).

## Cifrado

**Encrypt connection** is selected by default, and Azure SQL requires it.

If your machine doesn't trust the server's certificate, a **SQL Server certificate not trusted** prompt appears. Select **OK** to trust the certificate and connect. The prompt doesn't appear if the server has a certificate your machine trusts or if you clear **Encrypt connection**.
