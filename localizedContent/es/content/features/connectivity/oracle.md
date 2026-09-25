---
uid: connect-oracle
title: Conectar a Oracle
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

# Conectar a Oracle

Ve a **Modelo > Importar tablas...** y selecciona un origen de Oracle.

El conector de Oracle requiere que el proveedor OLE DB de Oracle esté instalado en tu equipo. Si no está instalado, verás esta advertencia:

![Advertencia de que el controlador ODAC no está instalado; indica que Tabular Editor 3 requiere el proveedor OraOLEDB.Oracle de Oracle Data Access Components](~/content/assets/images/features/connectivity/oracle-connection.png)

## Métodos de autenticación

Las conexiones de Oracle usan un nombre de usuario y una contraseña de base de datos. En el cuadro de diálogo de conexión no existe ningún modo de autenticación integrada ni basado en directorios.

| Campo                                  | Qué es                                                                      |
| -------------------------------------- | --------------------------------------------------------------------------- |
| **Servidor**                           | El nombre TNS, una cadena Easy Connect o el descriptor de conexión completo |
| **Nombre de usuario** y **Contraseña** | Una cuenta de base de datos de Oracle                                       |
| **Opciones adicionales**               | Configuración adicional de la cadena de conexión, que se pasa sin cambios   |

## Identificadores

Los nombres de los objetos de Oracle siempre van entre comillas dobles, y Oracle interpreta un nombre sin comillas como si estuviera en mayúsculas. Por lo tanto, una tabla creada como `sales` será `\"SALES\"` a menos que se haya creado entre comillas. Si el asistente no enumera una tabla que esperabas, comprueba el uso de mayúsculas y minúsculas en su nombre en Oracle antes de dar por hecho que se trata de un problema de permisos.

## Dónde se almacenan las credenciales

Las credenciales que introduces aquí se guardan, por usuario y por modelo, en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, así que no se registran en el control de versiones, y cualquier compañero que abra el mismo modelo deberá proporcionar sus propias credenciales.

La expresión M generada solo nombra el servidor y el objeto. Nunca contiene una contraseña, un token ni una clave.
