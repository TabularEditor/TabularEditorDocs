---
uid: connect-onelake
title: Conectar con Fabric y OneLake
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

# Conectar con Fabric y OneLake

Tabular Editor se conecta a Microsoft Fabric para listar los Workspaces y los elementos de Lakehouse, Warehouse y otros que hay en ellos, y para importar desde OneLake.

![El cuadro de diálogo Conectar a un Lakehouse, que enumera elementos del catálogo de OneLake por nombre, tipo, propietario y ubicación](~/content/assets/images/features/connectivity/onelake-connection.png)

## Métodos de autenticación

Fabric y OneLake usan Microsoft Entra ID para autenticarse. El inicio de sesión interactivo es la opción predeterminada y cubre el trabajo habitual de modelado. Para una actualización sin supervisión, usa una entidad de servicio y concédele acceso al Workspace en Fabric.

Los permisos de Fabric se conceden en Fabric, no en Tabular Editor. Una cuenta que puede iniciar sesión pero no ve ningún Workspace no tiene acceso a ellos, por lo que es una cuestión de permisos de Fabric y no un problema de conexión.

## Direct Lake

Un modelo Direct Lake lee desde OneLake en lugar de importar datos, por lo que la conexión forma parte del modelo y no de un paso de importación. Consulta @direct-lake-sql-model.

> [!NOTE]
> Cuando no se puede determinar el punto de conexión de análisis SQL de un Lakehouse o Warehouse, Tabular Editor lo indica en lugar de crear una tabla sin columnas. Si ves ese error, comprueba que el elemento haya terminado de aprovisionar su punto de conexión en Fabric.

## Dónde se almacenan las credenciales

Las credenciales que introduzcas aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, por lo que no se incluyen en el control de código fuente, y un compañero que abra el mismo modelo tendrá que proporcionar las suyas.

La expresión M generada solo incluye el nombre del servidor y del objeto. Nunca contiene una contraseña, un token o una clave.
