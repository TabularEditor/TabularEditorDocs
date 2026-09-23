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

Tabular Editor puede importar entidades de un Dataflow de Power BI, de modo que un modelo pueda reutilizar las transformaciones que ya existen en un Workspace en lugar de repetirlas.

![El cuadro de diálogo Conectarse a un Workspace de Power BI, en el que se enumeran los Workspaces a los que pertenece la cuenta con la que has iniciado sesión](~/content/assets/images/features/connectivity/dataflows-connection.png)

## Métodos de autenticación

Los Dataflows se autentican con Microsoft Entra ID frente al servicio de Power BI.

| Lo que proporcionas                                    | Cuándo                                 |
| ------------------------------------------------------ | -------------------------------------- |
| Un inicio de sesión interactivo con Microsoft Entra ID | Uso interactivo normal                 |
| Una entidad de servicio                                | Actualización programada o desatendida |

Puedes ver los Workspaces de los que forma parte tu cuenta. Un Dataflow de un Workspace al que no te hayan agregado no aparece, y un Workspace sin Dataflows se muestra vacío en lugar de ocultarse.

> [!NOTE]
> Un administrador de Power BI debe habilitar el acceso de la entidad de servicio a la API REST de Power BI en la configuración del inquilino antes de que una entidad de servicio pueda siquiera enumerar Workspaces. Hasta que se habilite, una entidad de servicio inicia sesión correctamente y no ve nada.

## Dónde se almacenan las credenciales

Las credenciales que introduces aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas de modo que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, por lo que no se incluyen en el control de código fuente y un compañero que abra el mismo modelo tendrá que proporcionar las suyas.

La expresión M generada solo incluye el nombre del servidor y del objeto. Nunca contiene una contraseña, un token ni una clave.
