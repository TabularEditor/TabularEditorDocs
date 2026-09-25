---
uid: connect-odbc
title: Conectar mediante ODBC
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

# Conectar mediante ODBC

ODBC es la opción general para conectarse a un origen que no tiene un cuadro de diálogo específico en Tabular Editor. Así se accede a PostgreSQL, MySQL, MariaDB e IBM Db2, y Tabular Editor reconoce cada uno de ellos lo bastante bien como para generar la expresión M correcta y entrecomillar los identificadores de la forma que espera cada base de datos.

![El cuadro de diálogo "Elegir origen ODBC", con un DSN del sistema seleccionado y el nombre de usuario y la contraseña rellenados](~/content/assets/images/features/connectivity/odbc-connection.png)

## Métodos de autenticación

ODBC no tiene una lista propia de métodos de autenticación. La forma de iniciar sesión la decide el controlador y el DSN que selecciones.

| Campo                                               | Qué es                                                                                   |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Nombre del Data source (DSN)** | Un DSN configurado en el Administrador de orígenes de datos ODBC de Windows              |
| **Nombre de usuario** y **contraseña**              | Se proporcionan al controlador cuando el DSN no incluye ya las credenciales              |
| **Opciones adicionales**                            | Configuración adicional de la cadena de conexión, que se pasa al controlador sin cambios |

Por lo tanto, que la conexión pueda restablecerse sin que haya una persona presente depende del controlador, no de Tabular Editor. Un DSN con autenticación Integrada o con una cuenta de servicio almacenada se reconecta por sí solo; uno que solicita credenciales, no.

> [!NOTE]
> Un DSN es específico de cada equipo. Un modelo que importa a través de un DSN solo se actualiza en un equipo donde exista un DSN con el mismo nombre, algo que conviene planificar antes de involucrar a un agente de compilación. Usa un DSN de sistema en lugar de un DSN de usuario cuando una cuenta de servicio vaya a ejecutar la actualización.

## Los controladores deben coincidir con la arquitectura

Tabular Editor 3 es una aplicación de 64 bits en x64 y ARM64, por lo que solo ve controladores ODBC de 64 bits y DSN de 64 bits. Un DSN creado en el administrador ODBC de 32 bits no aparece en la lista. Windows incluye ambos administradores, así que comprueba cuál utilizaste si no aparece un DSN que acabas de crear.

## Dónde se almacenan las credenciales

Las credenciales que introduzcas aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, por lo que no se incluyen en el control de versiones, y un compañero que abra el mismo modelo proporcionará sus propias credenciales.

La expresión M generada solo nombra el servidor y el objeto. Nunca contiene una contraseña, un token ni una clave.
