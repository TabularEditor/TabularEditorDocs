---
uid: connect-odbc
title: Conectar mediante ODBC
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

# Conectar mediante ODBC

El conector ODBC se conecta a cualquier origen que tenga un controlador ODBC y para el que Tabular Editor no tenga un cuadro de diálogo de conexión específico. Para PostgreSQL, MySQL, MariaDB e IBM Db2, Tabular Editor genera expresiones M específicas de la base de datos y el entrecomillado de identificadores. Selecciona **Modelo > Importar tablas...** y elige **ODBC** para abrir el cuadro de diálogo.

![Cuadro de diálogo para elegir un origen ODBC, con un DSN del sistema seleccionado y un nombre de usuario y una contraseña introducidos](~/content/assets/images/features/connectivity/odbc-connection.png)

## Requisitos previos

- Un controlador ODBC para el origen que coincida con la arquitectura de tu versión de Tabular Editor (x64 o ARM64). Consulta [Arquitectura del controlador](#driver-architecture).
- Un nombre de Data source (DSN) para el origen, creado en el Administrador de orígenes de datos ODBC de 64 bits.

> [!IMPORTANT]
> Un DSN solo existe en el equipo donde lo creas, y un modelo que importa a través de un DSN solo se actualiza en equipos que tengan un DSN con el mismo nombre. Si la conexión se ejecuta con una cuenta de servicio, usa un DSN del sistema.

## Campos de conexión

| Campo                                                                              | Descripción                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Nombre del Data source (DSN)**                                | Un DSN del sistema o un DSN de usuario configurado en este equipo. Obligatorio                                                                                                         |
| **Nombre de usuario** y **contraseña**                                             | Credenciales que se pasan al controlador, si el DSN las requiere                                                                                                                                       |
| **Propiedades adicionales de la cadena de conexión (opcional)** | Ajustes adicionales de la cadena de conexión, que se pasan al controlador sin modificar                                                                                                                |
| **Cláusula de reducción de filas** y **entrecomillado de identificadores**         | La sintaxis SQL que usa Tabular Editor para limitar las filas de vista previa y poner los nombres entre comillas. Selecciona **Detectar** para leer ambos valores desde el controlador |

## Autenticación

El controlador y el DSN determinan cómo inicias sesión:

| Autenticación                      | Lo que proporcionas                                                                          | Inicio de sesión interactivo |
| ---------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------- |
| **Credenciales del DSN**           | Nada. El DSN incluye autenticación Integrada o credenciales almacenadas      | No                           |
| **Nombre de usuario y contraseña** | **Nombre de usuario** y **contraseña** en el cuadro de diálogo, que se envían al controlador | No                           |

Tabular Editor guarda la configuración de conexión y las credenciales en tu archivo de opciones de usuario (consulta [dónde se almacenan las credenciales](xref:connectivity#where-credentials-are-stored)).

## Arquitectura del controlador

Tabular Editor 3 solo muestra los DSN de 64 bits, por lo que un DSN creado en el Administrador de Data source ODBC de 32 bits no aparece. Si falta un DSN, créalo en el Administrador de Data source ODBC de 64 bits (`odbcad32.exe` en `C:\Windows\System32`).

La compilación x64 solo carga controladores ODBC x64, y la compilación ARM64 solo carga controladores ODBC ARM64.
