---
uid: connect-oracle
title: 连接到 Oracle
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

# 连接到 Oracle

从 **模型 > 导入表...** 开始，选择 Oracle 作为数据源。

Oracle 连接器要求在本机安装 Oracle OLE DB 提供程序。如果未安装，就会出现以下警告：

![未安装 ODAC 驱动程序的警告，提示 Tabular Editor 3 需要 Oracle Data Access Components 中的 OraOLEDB.Oracle 提供程序](~/content/assets/images/features/connectivity/oracle-connection.png)

## 身份验证方式

Oracle 连接使用数据库用户名和密码。连接对话框不支持集成身份验证或基于目录的模式。

| 字段             | 说明                              |
| -------------- | ------------------------------- |
| **服务器**        | TNS 名称、Easy Connect 字符串或完整连接描述符 |
| **用户名**和**密码** | Oracle 数据库帐户                    |
| **其他选项**       | 额外的连接字符串设置，将不做更改地原样传递           |

## 标识符

Oracle 对象名称始终用双引号括起来，而 Oracle 会将未加引号的名称视为大写。因此，以 `sales` 创建的表默认是 `"SALES"`，除非它是用引号创建的。如果向导没有列出你预期的表，先检查它在 Oracle 中名称的大小写，再假定是权限问题。

## 凭据的存储位置

你在此处输入的凭据会按用户和模型分别保存到模型旁的 [用户选项](xref:user-options) 文件 (`.tmuo`) 中，并以加密方式存储，因此只有你的 Windows 帐户才能读取。它们不属于模型元数据，因此不会提交到源代码管理中；同事打开同一模型时需要提供自己的凭据。

生成的 M 表达式只会包含服务器和对象名称。其中绝不会包含密码、令牌或密钥。
