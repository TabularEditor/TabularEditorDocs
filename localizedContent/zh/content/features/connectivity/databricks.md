---
uid: connect-databricks
title: 连接到 Databricks
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

# 连接到 Databricks

The Databricks connector connects to SQL warehouses and clusters in Azure Databricks and in Databricks workspaces on other clouds. It's available only as an implicit data source (see [Legacy, structured and implicit data sources](xref:connectivity#legacy-structured-and-implicit-data-sources)).

Select **Model > Import tables...** and choose a Databricks source to open the dialog. @connecting-to-azure-databricks walks through an Azure Databricks import step by step.

![The Connect to Databricks dialog, with Azure AD selected as the authentication type and a Sign in button beside it](~/content/assets/images/features/connectivity/databricks-connection.png)

## 前提条件

Install the [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download) on your machine (see [Prerequisites](xref:connecting-to-azure-databricks#prerequisites) in the tutorial for the supported drivers).

## Connection fields

| 字段                                                                                               | 说明                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Server Hostname**                                                                              | The host name from the **Connection details** tab of the compute resource in Databricks. 必需                                                                       |
| **HTTP Path**                                                                                    | The HTTP path from the same tab. 必需                                                                                                                               |
| **Type**                                                                                         | The authentication option. See [Authentication](#authentication)                                                                                                  |
| **Username** and **Password**, or **Sign in...** | The credentials for the selected authentication option. The fields change with the option                                                                         |
| **Advanced**                                                                                     | Optional settings: **Default catalog**, **Database**, **Automatic Proxy Discovery**, **Query tags**, **Implementation** and **Metric View BI Compatibility Mode** |

## 身份验证

| 身份验证                                | 需要提供的内容                                                                              | Interactive sign-in |
| ----------------------------------- | ------------------------------------------------------------------------------------ | ------------------- |
| **访问令牌**                            | A Databricks personal access token. When it expires, enter a new one | 否                   |
| **用户名 / 密码**                        | 用户名和密码                                                                               | 否                   |
| **Azure AD**                        | A Microsoft Entra ID sign-in. Available only for Azure Databricks    | 是的                  |
| **OAuth (OIDC)** | 通过浏览器登录                                                                              | 是的                  |
| **OAuth (M2M)**  | A service principal client ID and client secret                                      | 否                   |

For unattended connections, use **OAuth (M2M)**, which authenticates as a service principal.

Tabular Editor saves the connection settings and credentials in your user options file (see [Where credentials are stored](xref:connectivity#where-credentials-are-stored)).
