---
uid: connect-dataflows
title: Conectarse a los Dataflows de Power BI
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

# Conectarse a los Dataflows de Power BI

El conector de Dataflow de Power BI importa entidades de los Dataflows en los Workspaces de Power BI de los que eres miembro y solo está disponible como un Data source implícito (consulta [Orígenes de datos heredados, estructurados e implícitos](xref:connectivity#legacy-structured-and-implicit-data-sources)).

Abre el cuadro de diálogo desde **Modelo > Importar tablas...** eligiendo **Power BI Dataflow**.

![El cuadro de diálogo para conectarse a un Workspace de Power BI, con la lista de Workspaces a los que pertenece la cuenta con la que has iniciado sesión](~/content/assets/images/features/connectivity/dataflows-connection.png)

## Campos de conexión

| Campo                                                                 | Descripción                                                                           |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Iniciar sesión...** | Inicia sesión en el servicio Power BI con Microsoft Entra ID                          |
| **Workspaces**                                                        | Los Workspaces a los que pertenece tu cuenta. Selecciona un Workspace |

Si un Workspace no tiene Dataflows, aparecerá vacío.

## Autenticación

**Iniciar sesión...** inicia el proceso de inicio de sesión en el navegador con Microsoft Entra ID.

Tabular Editor guarda la configuración de conexión y las credenciales en tu archivo de opciones de usuario (consulta [Dónde se almacenan las credenciales](xref:connectivity#where-credentials-are-stored)).
