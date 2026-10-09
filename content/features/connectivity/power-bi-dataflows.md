---
uid: connect-dataflows
title: Connect to Power BI dataflows
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

# Connect to Power BI dataflows

The Power BI dataflows connector imports entities from dataflows in the Power BI workspaces you're a member of and is available only as an implicit data source (see [Legacy, structured and implicit data sources](xref:connectivity#legacy-structured-and-implicit-data-sources)).

Open the dialog from **Model > Import tables...** by choosing **Power BI Dataflow**.

![The Connect to a Power BI workspace dialog, listing the workspaces the signed-in account belongs to](~/content/assets/images/features/connectivity/dataflows-connection.png)

## Connection fields

| Field | Description |
| -- | -- |
| **Sign in...** | Signs in to the Power BI service with Microsoft Entra ID |
| **Workspaces** | The workspaces your account is a member of. Select one workspace |

If a workspace has no dataflows, it appears empty.

## Authentication

**Sign in...** starts a Microsoft Entra ID browser sign-in.

Tabular Editor saves the connection settings and credentials in your user options file (see [Where credentials are stored](xref:connectivity#where-credentials-are-stored)).
