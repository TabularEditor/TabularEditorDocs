---
uid: connect-sql-server
title: 连接到 SQL Server
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

# 连接到 SQL Server

涵盖 SQL Server、Azure SQL Database、Azure SQL Managed Instance 和 Azure Synapse。从 **模型 > 导入表...** 开始，然后选择 SQL Server 数据源。

![“连接到 SQL Server”对话框，其中已在“身份验证”列表中选择“Azure Active Directory - 通用，启用 MFA”](~/content/assets/images/features/connectivity/sql-server-connection.png)

## 身份验证方式

| 身份验证                                   | 需要提供的内容         | 说明                                   |
| -------------------------------------- | --------------- | ------------------------------------ |
| **SQL Server 身份验证**                    | 用户名和密码          | 由服务器本身定义的登录名，而非目录中的账户                |
| **Windows 身份验证**                       | 无需提供            | 使用 Tabular Editor 当前运行所用的 Windows 账户 |
| **Azure Active Directory - 通用，启用 MFA** | 通过浏览器登录         | 这是唯一会弹出交互提示的方式。用于交互式操作，不适用于计划任务      |
| **Azure Active Directory - 密码**        | 用户名和密码          | 目录账户。如果该账户需要多重身份验证，此方式将无法使用          |
| **Azure Active Directory - 集成**        | 无               | 使用你用于登录 Windows 的目录帐户，前提是该计算机已加入该目录  |
| **Azure Active Directory - 服务主体**      | 应用程序（客户端）ID 和密钥 | 通常用于无人值守刷新                           |

两种集成模式都不需要用户名或密码，选择其中一种时，Tabular Editor 会清空这两个字段。

## 加密

**加密连接**用于控制连接是否必须使用 TLS。 Azure SQL 要求启用此项。除非你要连接到没有证书的本地服务器，否则请保持开启。若连接到无证书服务器，连接会因证书错误而失败，直到你安装证书或将其关闭。

## 保存密码

**保存密码**会保存该密码，供下次使用。如果取消勾选，下次模型需要该数据源时会再次提示你输入。

## 凭据的存储位置

你在此处输入的凭据会按用户、按模型保存在模型旁的 [用户选项](xref:user-options) 文件（`.tmuo`）中，并经过加密，只有你的 Windows 账户可以读取。它们不是模型元数据的一部分，因此不会提交到源代码管理；同事打开同一模型时需要输入自己的凭据。

生成的 M 表达式只会包含服务器和对象的名称。其中绝不会包含密码、令牌或密钥。
