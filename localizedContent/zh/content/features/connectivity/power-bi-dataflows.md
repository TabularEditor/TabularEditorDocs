---
uid: connect-dataflows
title: Connect to Power BI dataflows
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

# Connect to Power BI dataflows

Tabular Editor can import entities from a Power BI dataflow, so a model can reuse transformations that already exist in a workspace rather than repeating them.

![The Connect to a Power BI workspace dialog, listing the workspaces the signed-in account belongs to](~/content/assets/images/features/connectivity/dataflows-connection.png)

## Authenticators

Dataflows authenticate with Microsoft Entra ID, against the Power BI service.

| What you supply                           | When                            |
| ----------------------------------------- | ------------------------------- |
| An interactive Microsoft Entra ID sign-in | Normal interactive use          |
| A service principal                       | Scheduled or unattended refresh |

You see the workspaces your account is a member of. A dataflow in a workspace you have not been added to does not appear, and a workspace with no dataflows in it is listed empty rather than hidden.

> [!NOTE]
> Service principal access to the Power BI REST API has to be enabled by a Power BI administrator in the tenant settings before a service principal can list workspaces at all. Until it is, a service principal signs in successfully and sees nothing.

## Where the credentials are stored

Credentials you enter here are saved per user and per model in the [user options](xref:user-options) file (`.tmuo`) beside the model, encrypted so that only your Windows account can read them. They are not part of the model metadata, so they are not committed to source control and a colleague opening the same model supplies their own.

The generated M expression names the server and the object only. It never contains a password, a token or a key.
