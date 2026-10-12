---
uid: connect-dataflows
title: 连接到 Power BI Dataflows
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

# 连接到 Power BI Dataflows

The Power BI dataflows connector imports entities from dataflows in the Power BI workspaces you're a member of and is available only as an implicit data source (see [Legacy, structured and implicit data sources](xref:connectivity#legacy-structured-and-implicit-data-sources)).

Open the dialog from **Model > Import tables...** by choosing **Power BI Dataflow**.

![“连接到 Power BI Workspace”对话框，其中列出了已登录账户所属的 Workspace](~/content/assets/images/features/connectivity/dataflows-connection.png)

## Connection fields

| 字段                                                             | 说明                                                                               |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Sign in...** | Signs in to the Power BI service with Microsoft Entra ID                         |
| **Workspaces**                                                 | The workspaces your account is a member of. Select one workspace |

If a workspace has no dataflows, it appears empty.

## 身份验证

**Sign in...** starts a Microsoft Entra ID browser sign-in.

Tabular Editor saves the connection settings and credentials in your user options file (see [Where credentials are stored](xref:connectivity#where-credentials-are-stored)).
