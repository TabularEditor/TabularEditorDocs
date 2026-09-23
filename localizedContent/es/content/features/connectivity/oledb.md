---
uid: connect-oledb
title: Conectar mediante OLE DB
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

# Conectar mediante OLE DB

OLE DB es la otra vía de propósito general y la opción adecuada cuando un origen ofrece un proveedor OLE DB, pero no un controlador ODBC que funcione.

![El cuadro de diálogo Propiedades del vínculo de datos en su pestaña Proveedor, con la lista de proveedores OLE DB instalados en el equipo](~/content/assets/images/features/connectivity/oledb-connection.png)

## Autenticadores

Al igual que con ODBC, es el proveedor quien decide cómo inicias sesión, no Tabular Editor.

| Campo                                  | Qué es                                                                      |
| -------------------------------------- | --------------------------------------------------------------------------- |
| **Proveedor**                          | Un proveedor OLE DB instalado en este equipo                                |
| **Servidor**                           | Lo que el proveedor necesite para identificar el origen                     |
| **Nombre de usuario** y **contraseña** | Se facilitan al proveedor cuando las necesita                               |
| **Opciones adicionales**               | Configuración adicional de la cadena de conexión, que se transmite tal cual |

La lista de proveedores se lee del equipo, por lo que muestra lo que está instalado y no todo lo que existe. Si falta un proveedor en la lista, primero hay que instalarlo con la misma arquitectura que Tabular Editor.

> [!TIP]
> Prefiere un cuadro de diálogo específico cuando exista; si no, ODBC antes que OLE DB. Analysis Services admite una gama más limitada de proveedores OLE DB que Windows, por lo que un origen que se conecta en el asistente puede, aun así, fallar al actualizarse en el servidor.

## Dónde se almacenan las credenciales

Las credenciales que introduzcas aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, por lo que no se confirman en el control de versiones, y un compañero que abra el mismo modelo proporcionará las suyas.

La expresión M generada solo incluye el nombre del servidor y del objeto. Nunca contiene una contraseña, un token ni una clave.
