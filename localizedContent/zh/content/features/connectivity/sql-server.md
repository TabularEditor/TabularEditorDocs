---
uid: connect-sql-server
title: 连接到 SQL Server
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

# 连接到 SQL Server

SQL Server 连接器可连接到 SQL Server、Azure SQL Database、Azure SQL Managed Instance 和 Azure Synapse Analytics。从 **模型 > 导入表...** 开始，然后选择 SQL Server 数据源。

![“连接到 SQL Server”对话框，“身份验证”列表中已选择“Azure Active Directory - Universal with MFA”](~/content/assets/images/features/connectivity/sql-server-connection.png)

## 连接字段

| 字段                                                        | 说明                                                                |
| --------------------------------------------------------- | ----------------------------------------------------------------- |
| **服务器名称**                                                 | 要连接的服务器或实例                                                        |
| **身份验证**                                                  | 身份验证选项。参见 [身份验证](#authentication)                                 |
| **用户名**和**密码**                                            | 所选身份验证选项的凭据                                                       |
| **记住密码**                                                  | 保存密码，以便下次连接时使用。如果取消选中此项，下次导入、预览或更新表架构时，系统会提示输入密码                  |
| **数据库**                                                   | 要从中导入的数据库。选择 **< 浏览服务器…… >**，以列出服务器上的数据库 |
| **加密连接**                                                  | 要求连接使用 TLS。参见 [加密](#encryption)                                   |
| **高级...** | 打开完整的连接字符串属性                                                      |

## 身份验证

| 身份验证                                   | 需要提供的内容                                | 交互式登录 |
| -------------------------------------- | -------------------------------------- | ----- |
| **SQL Server 身份验证**                    | 服务器上定义的 SQL 登录的用户名和密码                  | 否     |
| **Windows 身份验证**                       | 无。使用 Tabular Editor 运行时所使用的 Windows 帐户 | 否     |
| **Azure Active Directory - 通用，启用 MFA** | 通过浏览器登录                                | 是的    |
| **Azure Active Directory - 密码**        | 目录帐户的用户名和密码。如果该帐户需要多重身份验证，则无法使用        | 否     |
| **Azure Active Directory - 集成**        | 无。在已加入目录的计算机上，使用你用于登录 Windows 的目录帐户    | 否     |
| **Azure Active Directory - 服务主体**      | 应用程序（客户端）ID 和密钥                        | 否     |

若用于无人值守场景，请选择 **Azure Active Directory - 服务主体**。选择 **Windows 身份验证** 或 **Azure Active Directory - 集成** 后，**用户名**、**密码** 和 **记住密码** 将被禁用，且 **用户名** 会以 `DOMAIN\\user` 的格式显示你的 Windows 帐户。

Tabular Editor 会将连接设置和凭据保存在你的用户选项文件中（请参阅[凭据的存储位置](xref:connectivity#where-credentials-are-stored)）。

## 加密

**加密连接** 默认处于选中状态，Azure SQL 也要求启用它。

如果你的计算机不信任服务器证书，就会出现 **SQL Server 证书不受信任** 提示。选择 **确定** 以信任该证书并连接。如果服务器使用的是你的计算机信任的证书，或者你取消选中 **加密连接**，则不会出现该提示。
