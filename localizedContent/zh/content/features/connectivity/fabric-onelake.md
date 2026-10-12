---
uid: connect-onelake
title: 连接到 Fabric 和 OneLake
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

# 连接到 Fabric 和 OneLake

The Fabric connector lists the Lakehouse, Warehouse, SQL database and mirrored database items in the Fabric workspaces you can access, and imports tables from them. Mirrored Azure Databricks catalogs are listed as mirrored databases. Open the dialog from **Model > Import tables...** by choosing **Microsoft Fabric Lakehouse**, **Microsoft Fabric Warehouse**, **Microsoft Fabric SQL Database** or **Microsoft Fabric Mirrored Database**.

![“连接到 Lakehouse”对话框，按名称、类型、所有者和位置列出 OneLake catalog 中的项目](~/content/assets/images/features/connectivity/onelake-connection.png)

## Connection fields

| 字段                                                             | 说明                                                                                                                                                          |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sign in...** | Signs in to the Power BI service with Microsoft Entra ID                                                                                                    |
| **OneLake Catalog items**                                      | The items of the selected type in the workspaces you can access, with their **Name**, **Type**, **Owner** and **Location**. Select one item |

## 身份验证

**Sign in...** starts a Microsoft Entra ID browser sign-in. If no items appear after you sign in, your account has no access to a workspace that contains them, and a workspace admin grants that access in Fabric.

Tabular Editor saves the connection settings and credentials in your user options file (see [Where credentials are stored](xref:connectivity#where-credentials-are-stored)).

## Import and Direct Lake

On the last page of the Table Import Wizard, you choose whether the selected tables are created in Import mode or Direct Lake mode:

- Import tables read their schema through the item's SQL analytics endpoint. See [Choosing objects to import](xref:import-tables#choosing-objects-to-import).
- Direct Lake tables read directly from OneLake. 参见 @direct-lake-sql-model。
