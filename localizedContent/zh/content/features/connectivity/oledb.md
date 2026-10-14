---
uid: connect-oledb
title: 通过 OLE DB 连接
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

# 通过 OLE DB 连接

OLE DB 连接器可连接到具有 OLE DB 提供程序但没有可用 ODBC 驱动程序的数据源。选择 **模型 > 导入表...**，然后选择 **OLE DB**，即可打开 Windows **数据链接属性** 对话框。

![“数据链接属性”对话框的“提供程序”选项卡，其中列出了此计算机上安装的 OLE DB 提供程序](~/content/assets/images/features/connectivity/oledb-connection.png)

## 先决条件

为该数据源安装与 Tabular Editor 构建架构匹配的 OLE DB 提供程序。

> [!WARNING]
> Analysis Services 支持的 OLE DB 提供程序少于 Windows。如果 Analysis Services 不支持该提供程序，则可以在 Tabular Editor 中导入该数据源，但在服务器上刷新会失败。如果有专用连接对话框，就使用它；如果没有，就使用 [ODBC](xref:connect-odbc)。

## 连接字段

**数据链接属性** 对话框包含以下选项卡：

| 字段                  | 说明                                |
| ------------------- | --------------------------------- |
| **提供程序** 选项卡        | 此计算机上安装的 OLE DB 提供程序。选择数据源对应的提供程序 |
| **连接** 选项卡          | 所选提供程序需要的数据源、凭据和其他设置              |
| **高级** 和 **全部** 选项卡 | 更多提供程序特定的连接字符串属性                  |

如果已保存的连接字符串指定了未安装的提供程序，则会显示警告。安装该提供程序，或选择其他提供程序。

## 身份验证

提供程序决定你的登录方式，因此请在 **连接** 选项卡中输入其登录设置，例如用户名和密码或集成安全性。

Tabular Editor 会将连接设置和凭据保存到你的用户选项文件中（请参阅[凭据的存储位置](xref:connectivity#where-credentials-are-stored)）。
