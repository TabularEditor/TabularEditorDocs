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

ODBC es la vía general para conectarse a un origen que no tiene un cuadro de diálogo específico en Tabular Editor. Así se accede a PostgreSQL, MySQL, MariaDB e IBM Db2, y Tabular Editor reconoce cada uno de ellos lo suficiente como para generar la expresión M correcta y poner los identificadores entre comillas tal como lo espera esa base de datos.

![El cuadro de diálogo "Elegir origen ODBC", con un DSN del sistema seleccionado y el nombre de usuario y la contraseña completados](~/content/assets/images/features/connectivity/odbc-connection.png)

## Métodos de autenticación

ODBC no tiene su propia lista de métodos de autenticación. La forma de iniciar sesión la determinan el controlador y el DSN que selecciones.

| Campo                                              | Qué es                                                                                  |
| -------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **Nombre de Data source (DSN)** | Un DSN configurado en el Administrador ODBC de Data source de Windows                   |
| **Nombre de usuario** y **contraseña**             | Se proporcionan al controlador cuando el DSN no incluye ya las credenciales             |
| **Opciones adicionales**                           | Parámetros adicionales de la cadena de conexión que se pasan al controlador sin cambios |

Por tanto, que la conexión pueda volver a establecerse sin que haya una persona presente depende del controlador, no de Tabular Editor. Un DSN con autenticación Integrada o con una cuenta de servicio almacenada se vuelve a conectar por sí solo; uno que solicita credenciales no.

> [!NOTE]
> Un DSN es específico de cada equipo. Un modelo que importa a través de un DSN solo se actualiza en un equipo donde exista un DSN con el mismo nombre, algo que conviene prever antes de incorporar un agente de compilación. Use un DSN del sistema en lugar de un DSN de usuario cuando una cuenta de servicio vaya a ejecutar la actualización.

## Los controladores deben coincidir con la arquitectura

Tabular Editor 3 es una aplicación de 64 bits en x64 y ARM64, por lo que solo reconoce controladores ODBC de 64 bits y DSN de 64 bits. Un DSN creado en el administrador de ODBC de 32 bits no aparece en la lista. Windows incluye ambos administradores, así que comprueba cuál usaste si no aparece un DSN que acabas de crear.

## Dónde se almacenan las credenciales

Las credenciales que introduzca aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo su cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, así que no se incluyen en el control de código fuente y un compañero que abra el mismo modelo tendrá que proporcionar las suyas.

La expresión M generada solo incluye el nombre del servidor y del objeto. Nunca contiene una contraseña, un token ni una clave.
