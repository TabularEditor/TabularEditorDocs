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

OLE DB es la otra opción de propósito general y la que conviene usar cuando un origen ofrece un proveedor OLE DB, pero no un controlador ODBC utilizable.

![Cuadro de diálogo Propiedades de vínculo de datos en la pestaña Proveedor, con la lista de proveedores OLE DB instalados en el equipo](~/content/assets/images/features/connectivity/oledb-connection.png)

## Métodos de autenticación

Al igual que con ODBC, el proveedor —y no Tabular Editor— decide cómo debes iniciar sesión.

| Campo                                  | Qué es                                                                         |
| -------------------------------------- | ------------------------------------------------------------------------------ |
| **Proveedor**                          | Un proveedor OLE DB instalado en este equipo                                   |
| **Servidor**                           | Lo que el proveedor requiera para identificar el origen                        |
| **Nombre de usuario** y **Contraseña** | Se proporcionan al proveedor cuando los necesita                               |
| **Opciones adicionales**               | Configuración adicional de la cadena de conexión, que se transmite sin cambios |

La lista de proveedores se lee del equipo, por lo que muestra lo que está instalado, no todo lo que existe. Si un proveedor no aparece en la lista, primero debe instalarse con la misma arquitectura que Tabular Editor.

> [!TIP]
> Siempre que exista, utiliza un cuadro de diálogo específico y, en caso contrario, prefiere ODBC a OLE DB. Analysis Services admite una gama más limitada de proveedores OLE DB que Windows, por lo que un origen que se conecta en el asistente puede aun así fallar al actualizarse en el servidor.

## Dónde se guardan las credenciales

Las credenciales que introduzcas aquí se guardan, por usuario y por modelo, en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, por lo que no se incluyen en el control de versiones, y un compañero que abra el mismo modelo deberá proporcionar las suyas.

La expresión M generada solo especifica el servidor y el objeto. Nunca contiene una contraseña, un token ni una clave.
