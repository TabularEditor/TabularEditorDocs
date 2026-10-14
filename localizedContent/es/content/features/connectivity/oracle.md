---
uid: connect-oracle
title: Conectar a Oracle
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

# Conectar a Oracle

El conector de Oracle se conecta a bases de datos Oracle a través del proveedor OLE DB de Oracle. Selecciona **Modelo > Importar tablas...** y elige un origen de Oracle para abrir el cuadro de diálogo.

<!-- IMAGE NEEDED: connectivity/oracle-connect-dialog.png
     The Connect to Oracle dialog with Server, Username, Password and
     Additional connection string properties (optional) visible.
     House border, 100% DPI.
     Alt text: "The Connect to Oracle dialog with the server, user name and password fields" -->

## Requisitos previos

Instala el proveedor Oracle OLE DB (`OraOLEDB.Oracle`), que forma parte de Oracle Data Access Components (ODAC), en tu equipo. Si falta el proveedor, Tabular Editor muestra esta advertencia:

![Advertencia de que el controlador ODAC no está instalado; indica que Tabular Editor 3 requiere el proveedor OraOLEDB.Oracle de Oracle Data Access Components](~/content/assets/images/features/connectivity/oracle-connection.png)

## Campos de conexión

| Campo                                                                              | Descripción                                                                                                |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Servidor**                                                                       | El nombre TNS, la cadena de Easy Connect o el descriptor de conexión completo. Obligatorio |
| **Nombre de usuario** y **Contraseña**                                             | Una cuenta de base de datos de Oracle. **Nombre de usuario** es obligatorio                |
| **Propiedades adicionales de la cadena de conexión (opcional)** | Configuración adicional de la cadena de conexión                                                           |

## Autenticación

Te autenticas con el nombre de usuario y la contraseña de una cuenta de base de datos de Oracle. El cuadro de diálogo no tiene ninguna opción de autenticación integrada ni basada en directorio.

Tabular Editor guarda la configuración de conexión y las credenciales en tu archivo de opciones de usuario (consulta [Dónde se almacenan las credenciales](xref:connectivity#where-credentials-are-stored)).

## Identificadores

En el SQL que genera, Tabular Editor encierra entre comillas dobles los nombres de esquema y de tabla de Oracle. Oracle almacena los nombres sin comillas en mayúsculas, por lo que una tabla creada como `sales` sin comillas aparece como `SALES`. Los nombres entre comillas en una consulta nativa deben respetar exactamente las mayúsculas y minúsculas con las que se almacenaron. Si el asistente no muestra una tabla que esperas, comprueba las mayúsculas y minúsculas de su nombre en Oracle antes de revisar los permisos.
