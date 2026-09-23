---
uid: connect-odbc
title: 通过 ODBC 连接
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

# 通过 ODBC 连接

对于在 Tabular Editor 中没有专用对话框的数据源，ODBC 是通用连接方式。 PostgreSQL、MySQL、MariaDB 和 IBM Db2 都通过这种方式连接，而 Tabular Editor 对它们的识别也足够准确，能够生成正确的 M 表达式，并按各数据库要求的方式为标识符加引号。

![选择 ODBC 数据源对话框，其中已选择系统 DSN，并已填写用户名和密码](~/content/assets/images/features/connectivity/odbc-connection.png)

## 身份验证方式

ODBC 本身没有自己的身份验证方式列表。身份验证方式由驱动程序以及所指向的 DSN 决定。

| 字段               | 说明                            |
| ---------------- | ----------------------------- |
| **数据源名称（DSN）**   | 在 Windows ODBC 数据源管理器中配置的 DSN |
| **用户名** 和 **密码** | 当 DSN 本身未包含凭据时，提供给驱动程序        |
| **其他选项**         | 额外的连接字符串设置，原样传递给驱动程序          |

因此，连接能否在无人值守的情况下重新建立，取决于驱动程序，而不是 Tabular Editor。使用集成身份验证或已存储服务帐户的 DSN 可以自动重新连接；需要弹出提示的则不能。

> [!NOTE]
> DSN 是按计算机配置的。通过 DSN 导入的模型只能在存在同名 DSN 的计算机上刷新；在引入构建代理之前就应提前规划这一点。如果刷新将由服务帐户运行，请使用系统 DSN，而不是用户 DSN。

## 驱动程序必须与体系结构匹配

Tabular Editor 3 在 x64 和 ARM64 上是 64 位应用程序，因此它会识别 64 位 ODBC 驱动程序和 64 位 DSN。在 32 位 ODBC 管理程序中创建的 DSN 不会显示在列表中。 Windows 同时提供这两个版本的管理程序，因此如果你刚创建的 DSN 没有显示，请检查你使用的是哪一个。

## 凭据存储位置

你在此输入的凭据会按用户和模型分别保存到模型旁边的 [用户选项](xref:user-options) 文件（`.tmuo`）中，并已加密，只有你的 Windows 帐户才能读取。它们不是模型元数据的一部分，因此不会提交到版本控制中，打开同一模型的同事需要自行提供凭据。

生成的 M 表达式只包含服务器和对象的名称。其中绝不会包含密码、令牌或密钥。
