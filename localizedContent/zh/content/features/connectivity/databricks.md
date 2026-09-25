---
uid: connect-databricks
title: 连接到 Databricks
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

# 连接到 Databricks

在 **模型 > 导入表...** 中开始，然后选择 Databricks 数据源。每种身份验证方式都需要 SQL Warehouse 或群集的 **Host** 和 **HTTP Path**，Databricks 会在该计算资源的连接详细信息页面上显示这两项。

![“连接到 Databricks”对话框，其中选择了 Azure AD 作为身份验证类型，旁边有一个“登录”按钮](~/content/assets/images/features/connectivity/databricks-connection.png)

## 身份验证方式

| 身份验证                                | 需要提供的内容                  | 可自动重新连接             |
| ----------------------------------- | ------------------------ | ------------------- |
| **访问令牌**                            | Databricks 个人访问令牌        | 是，直到令牌过期为止          |
| **用户名 / 密码**                        | 用户名和密码                   | 是的                  |
| **Azure AD**                        | 使用 Microsoft Entra ID 登录 | 仅限 Azure Databricks |
| **OAuth (OIDC)** | 通过浏览器登录                  | 否                   |
| **OAuth (M2M)**  | 服务主体的客户端 ID 和客户端密钥       | 是的                  |

> [!NOTE]
> **Azure AD** 仅适用于 Azure Databricks。如果 Databricks Workspace 托管在其他位置，请使用其余四种方式之一。

对于定时刷新，**OAuth (M2M)** 通常是首选：它使用服务主体，因此不会因人员离职而到期。

## 凭据存储位置

你在此输入的凭据会按用户、按模型分别保存到模型旁的 [用户选项](xref:user-options) 文件（`.tmuo`）中，并已加密，只有你的 Windows 帐户才能读取。它们不属于模型元数据，因此不会提交到源代码管理中；同事打开同一模型时需要提供自己的凭据。

生成的 M 表达式只会指定服务器和对象的名称。其中绝不会包含密码、令牌或密钥。
