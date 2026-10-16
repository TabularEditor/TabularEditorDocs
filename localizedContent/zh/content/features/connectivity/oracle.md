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

Oracle 连接器通过 Oracle OLE DB 提供程序连接到 Oracle 数据库。选择 **模型 > 导入表...**，然后选择 Oracle 数据源，即可打开对话框。

<!-- IMAGE NEEDED: connectivity/oracle-connect-dialog.png
     The Connect to Oracle dialog with Server, Username, Password and
     Additional connection string properties (optional) visible.
     House border, 100% DPI.
     Alt text: "The Connect to Oracle dialog with the server, user name and password fields" -->

## 先决条件

在本机上安装 Oracle OLE DB 提供程序 (`OraOLEDB.Oracle`)，它是 Oracle Data Access Components (ODAC) 的一部分。如果缺少该提供程序，Tabular Editor 会显示以下警告：

![未安装 ODAC 驱动程序的警告，提示 Tabular Editor 3 需要 Oracle Data Access Components 中的 OraOLEDB.Oracle 提供程序](~/content/assets/images/features/connectivity/oracle-connection.png)

## 连接字段

| 字段                | 说明                                 |
| ----------------- | ---------------------------------- |
| **服务器**           | TNS 名称、Easy Connect 字符串或完整连接描述符。必需 |
| **用户名** 和 **密码**  | Oracle 数据库账户。**用户名** 为必填项          |
| **附加连接字符串属性（可选）** | 附加的连接字符串设置                         |

## 身份验证

请使用 Oracle 数据库账户的用户名和密码进行身份验证。该对话框不提供集成身份验证或基于目录的身份验证选项。

Tabular Editor 会将连接设置和凭据保存在你的用户选项文件中（请参阅[凭据存储位置](xref:connectivity#where-credentials-are-stored)）。

## 标识符

在其生成的 SQL 中，Tabular Editor 会用双引号括起 Oracle 架构名和表名。 Oracle 会以大写形式存储未加引号的名称，因此，不带引号创建的表 `sales` 会显示为 `SALES`。原生查询中带引号的名称必须与存储时的大小写完全一致。如果向导没有列出你预期的表，请先检查它在 Oracle 中名称的大小写，再检查权限。
