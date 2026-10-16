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

Databricks 连接器可连接到 Azure Databricks 中的 SQL Warehouse 和群集，以及其他云端 Databricks Workspace 中的 SQL Warehouse 和群集。它仅以隐式数据源形式提供（参阅 [旧版、结构化和隐式数据源](xref:connectivity#legacy-structured-and-implicit-data-sources)）。

选择 **模型 > 导入表...**，然后选择 Databricks 数据源以打开对话框。 @connecting-to-azure-databricks 会逐步演示 Azure Databricks 导入过程。

![“连接到 Databricks”对话框，其中身份验证类型选择为 Azure AD，旁边有一个“登录”按钮](~/content/assets/images/features/connectivity/databricks-connection.png)

## 前提条件

在你的计算机上安装 [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download)（支持的驱动程序请参阅教程中的[先决条件](xref:connecting-to-azure-databricks#prerequisites)）。

## 连接字段

| 字段                                                                           | 说明                                                                 |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **服务器主机名**                                                                   | Databricks 中计算资源的 **连接详细信息** 选项卡中的主机名。必需                           |
| **HTTP 路径**                                                                  | 同一选项卡中的 HTTP 路径。必需                                                 |
| **类型**                                                                       | 身份验证选项。参阅 [身份验证](#authentication)                                  |
| **用户名** 和 **密码**，或 **登录...** | 所选身份验证选项的凭据。这些字段会随所选选项而变化                                          |
| **高级**                                                                       | 可选设置：**默认目录**、**数据库**、**自动代理发现**、**查询标记**、**实现**以及**指标视图 BI 兼容模式** |

## 身份验证

| 身份验证                                | 需要提供的内容                                     | 交互式登录 |
| ----------------------------------- | ------------------------------------------- | ----- |
| **访问令牌**                            | Databricks 个人访问令牌。过期后，请输入新的令牌               | 否     |
| **用户名 / 密码**                        | 用户名和密码                                      | 否     |
| **Azure AD**                        | Microsoft Entra ID 登录。仅适用于 Azure Databricks | 是的    |
| **OAuth (OIDC)** | 通过浏览器登录                                     | 是的    |
| **OAuth (M2M)**  | 服务主体的客户端 ID 和客户端密钥                          | 否     |

对于无人值守连接，请使用 **OAuth (M2M)**，它会以服务主体的身份进行身份验证。

Tabular Editor 会将连接设置和凭据保存到您的用户选项文件中（请参阅[凭据的存储位置](xref:connectivity#where-credentials-are-stored)）。
