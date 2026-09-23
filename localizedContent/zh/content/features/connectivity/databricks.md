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

从 **模型 > 导入表...** 开始，并选择 Databricks 数据源。所有身份验证方式都需要 SQL Warehouse 或集群的 **Host** 和 **HTTP Path**，Databricks 会在该计算资源的连接详细信息页面中显示这两项信息。

![“连接到 Databricks”对话框，其中身份验证类型选为 Azure AD，旁边有一个“登录”按钮](~/content/assets/images/features/connectivity/databricks-connection.png)

## 身份验证方式

| 身份验证                                | 你需要提供的内容                 | 可无人值守重新连接             |
| ----------------------------------- | ------------------------ | --------------------- |
| **访问令牌**                            | Databricks 个人访问令牌        | 是，直到令牌过期              |
| **用户名 / 密码**                        | 用户名和密码                   | 是的                    |
| **Azure AD**                        | 使用 Microsoft Entra ID 登录 | 仅适用于 Azure Databricks |
| **OAuth (OIDC)** | 通过浏览器登录                  | 否                     |
| **OAuth (M2M)**  | 服务主体的客户端 ID 和客户端机密       | 是的                    |

> [!NOTE]
> **Azure AD** 仅适用于 Azure Databricks。如果你的 Databricks Workspace 托管在其他位置，请使用另外四种方法中的一种。

对于计划刷新，**OAuth (M2M)** 通常是首选：它使用服务主体，因此不会因为某个人离职而到期。

## 凭据存储位置

你在此处输入的凭据会按用户和模型分别保存到模型旁的[用户选项](xref:user-options)文件（`.tmuo`）中，并经过加密，因此只有你的 Windows 帐户可以读取。它们不是模型元数据的一部分，因此不会提交到源代码管理；同事打开同一模型时会使用他们自己的凭据。

生成的 M 表达式仅包含服务器和对象名称。其中绝不会包含密码、令牌或密钥。
