---
uid: connect-odbc
title: 通过 ODBC 连接
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

# 通过 ODBC 连接

ODBC 连接器可连接到任何具有 ODBC 驱动程序、且在 Tabular Editor 中没有专用连接对话框的数据源。对于 PostgreSQL、MySQL、MariaDB 和 IBM Db2，Tabular Editor 会生成特定于数据库的 M 表达式，并使用相应的标识符加引号规则。选择 **模型 > 导入表...**，然后选择 **ODBC** 以打开该对话框。

![选择 ODBC 数据源对话框，其中已选择系统 DSN，并已填写用户名和密码](~/content/assets/images/features/connectivity/odbc-connection.png)

## 先决条件

- 适用于该数据源且与 Tabular Editor 版本架构（x64 或 ARM64）匹配的 ODBC 驱动程序。请参阅 [驱动程序架构](#driver-architecture)。
- 在 64 位 ODBC 数据源管理器中为该数据源创建的数据源名称（DSN）。

> [!IMPORTANT]
> DSN 仅存在于创建它的计算机上，而通过 DSN 导入的模型只能在具有同名 DSN 的计算机上刷新。如果连接由服务帐户运行，请使用系统 DSN。

## 连接字段

| 字段                    | 说明                                                           |
| --------------------- | ------------------------------------------------------------ |
| **数据源名称（DSN）**        | 此计算机上配置的系统 DSN 或用户 DSN。必需                                    |
| **用户名** 和 **密码**      | 如果 DSN 需要，则会将这些凭据传递给驱动程序                                     |
| **附加连接字符串属性（可选）**     | 额外的连接字符串设置，原样传递给驱动程序                                         |
| **行限制子句**和**标识符引用方式** | Tabular Editor 用于限制预览行数并对名称加引号的 SQL 语法。选择 **检测** 以从驱动程序读取这两项 |

## 身份验证

驱动程序和 DSN 会决定登录方式：

| 身份验证       | 需要提供的内容                            | 交互式登录 |
| ---------- | ---------------------------------- | ----- |
| **DSN 凭据** | 无。 DSN 使用集成身份验证或存储的凭据              | 否     |
| **用户名和密码** | 在对话框中输入的 **用户名** 和 **密码** 将传递给驱动程序 | 否     |

Tabular Editor 会将连接设置和凭据保存在你的用户选项文件中（请参阅[凭据的存储位置](xref:connectivity#where-credentials-are-stored)）。

## 驱动程序架构

Tabular Editor 3 只会列出 64 位 DSN，因此在 32 位 ODBC 数据源管理器中创建的 DSN 不会显示。如果缺少某个 DSN，就在 64 位 ODBC 数据源管理器中创建它（`C:\Windows\System32` 中的 `odbcad32.exe`）。

对于 x64 版本，只能加载 x64 ODBC 驱动程序；对于 ARM64 版本，只能加载 ARM64 ODBC 驱动程序。
