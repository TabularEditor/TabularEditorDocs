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

Tabular Editor se conecta a Microsoft Fabric para listar los Workspaces y los Lakehouse, Warehouse y otros elementos que contienen, e importar desde OneLake.

![El cuadro de diálogo "Conectar a un Lakehouse", que muestra elementos del catálogo de OneLake por nombre, tipo, propietario y ubicación](~/content/assets/images/features/connectivity/onelake-connection.png)

## Métodos de autenticación

Fabric y OneLake se autentican con Microsoft Entra ID. El inicio de sesión interactivo es la opción predeterminada y cubre el trabajo de modelado habitual. Para una actualización desatendida, usa un principal de servicio y concédele acceso al Workspace en Fabric.

Los permisos de Fabric se conceden en Fabric, no en Tabular Editor. Una cuenta que puede iniciar sesión pero no ve Workspaces no ha recibido acceso a ellos; es un tema de permisos de Fabric, no un problema de conexión.

## Direct Lake

Un modelo Direct Lake lee desde OneLake en lugar de importar, por lo que la conexión forma parte del modelo y no de un paso de importación. Consulta @direct-lake-sql-model.

> [!NOTE]
> Cuando no se puede determinar el punto de conexión de análisis SQL de un Lakehouse o Warehouse, Tabular Editor lo indica en lugar de crear una tabla sin columnas. Si ves ese error, comprueba que el elemento haya terminado de aprovisionar su punto de conexión en Fabric.

## Dónde se almacenan las credenciales

Las credenciales que introduzcas aquí se guardan por usuario y por modelo en el archivo [opciones de usuario](xref:user-options) (`.tmuo`) situado junto al modelo, cifradas de modo que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, por lo que no se registran en el control de código fuente, y un colega que abra el mismo modelo deberá proporcionar sus propias credenciales.

La expresión M generada solo especifica el servidor y el objeto. Nunca contiene contraseñas, tokens ni claves.
