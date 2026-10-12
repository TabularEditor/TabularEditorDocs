---
uid: connect-oracle
title: 连接到 Oracle
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

# 连接到 Oracle

The Oracle connector connects to Oracle databases through the Oracle OLE DB provider. Select **Model > Import tables...** and choose an Oracle source to open the dialog.

<!-- IMAGE NEEDED: connectivity/oracle-connect-dialog.png
     The Connect to Oracle dialog with Server, Username, Password and
     Additional connection string properties (optional) visible.
     House border, 100% DPI.
     Alt text: "The Connect to Oracle dialog with the server, user name and password fields" -->

## 先决条件

Install the Oracle OLE DB provider (`OraOLEDB.Oracle`), part of Oracle Data Access Components (ODAC), on your machine. If the provider is missing, Tabular Editor shows this warning:

![未安装 ODAC 驱动程序的警告，提示 Tabular Editor 3 需要 Oracle Data Access Components 中的 OraOLEDB.Oracle 提供程序](~/content/assets/images/features/connectivity/oracle-connection.png)

## Connection fields

| 字段                                                                        | 说明                                                                               |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **服务器**                                                                   | The TNS name, Easy Connect string or full connect descriptor. 必需 |
| **Username** and **Password**                                             | An Oracle database account. **Username** is required             |
| **Additional connection string properties (optional)** | Extra connection string settings                                                 |

## 身份验证

You authenticate with the user name and password of an Oracle database account. The dialog has no integrated or directory-based authentication option.

Tabular Editor saves the connection settings and credentials in your user options file (see [Where credentials are stored](xref:connectivity#where-credentials-are-stored)).

## 标识符

In the SQL it generates, Tabular Editor quotes Oracle schema and table names with double quotes. Oracle stores unquoted names in upper case, so a table created as `sales` without quotes appears as `SALES`. Quoted names in a native query must match the stored case. If the wizard doesn't list a table you expect, check the case of its name in Oracle before you check permissions.
