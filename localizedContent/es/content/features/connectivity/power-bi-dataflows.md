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

The Power BI dataflows connector imports entities from dataflows in the Power BI workspaces you're a member of and is available only as an implicit data source (see [Legacy, structured and implicit data sources](xref:connectivity#legacy-structured-and-implicit-data-sources)).

Open the dialog from **Model > Import tables...** by choosing **Power BI Dataflow**.

![El cuadro de diálogo para conectarse a un Workspace de Power BI, con la lista de Workspaces a los que pertenece la cuenta con la que has iniciado sesión](~/content/assets/images/features/connectivity/dataflows-connection.png)

## Connection fields

| Campo                                                          | Descripción                                                                      |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Sign in...** | Signs in to the Power BI service with Microsoft Entra ID                         |
| **Workspaces**                                                 | The workspaces your account is a member of. Select one workspace |

If a workspace has no dataflows, it appears empty.

## Autenticación

**Sign in...** starts a Microsoft Entra ID browser sign-in.

Tabular Editor saves the connection settings and credentials in your user options file (see [Where credentials are stored](xref:connectivity#where-credentials-are-stored)).
