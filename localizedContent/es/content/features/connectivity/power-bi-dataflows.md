---
uid: connect-dataflows
title: Conectarse a los Dataflows de Power BI
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

# Conectarse a los Dataflows de Power BI

Tabular Editor puede importar entidades desde un Dataflow de Power BI, de modo que un modelo pueda reutilizar las transformaciones que ya existen en un Workspace en lugar de repetirlas.

![El cuadro de diálogo para conectarse a un Workspace de Power BI, con la lista de Workspaces a los que pertenece la cuenta con la que has iniciado sesión](~/content/assets/images/features/connectivity/dataflows-connection.png)

## Autenticadores

Los Dataflows se autentican con Microsoft Entra ID en el servicio de Power BI.

| Lo que debes proporcionar                             | Cuándo                                 |
| ----------------------------------------------------- | -------------------------------------- |
| Un inicio de sesión interactivo de Microsoft Entra ID | Uso interactivo normal                 |
| Una entidad de servicio                               | Actualización programada o desatendida |

Verás los Workspaces de los que es miembro tu cuenta. Un Dataflow de un Workspace al que no se te haya agregado no aparece, y un Workspace sin Dataflows se muestra vacío en lugar de ocultarse.

> [!NOTE]
> Un administrador de Power BI debe habilitar el acceso de la entidad de servicio a la API REST de Power BI en la configuración del inquilino antes de que una entidad de servicio pueda enumerar Workspaces. Hasta entonces, una entidad de servicio iniciará sesión correctamente, pero no verá nada.

## Dónde se almacenan las credenciales

Las credenciales que introduzcas aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`), junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, por lo que no se incluyen en el control de código fuente, y un compañero que abra el mismo modelo deberá proporcionar las suyas.

La expresión M generada solo incluye el nombre del servidor y del objeto. Nunca contiene una contraseña, un token ni una clave.
