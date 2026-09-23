---
uid: connect-onelake
title: 连接到 Fabric 和 OneLake
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

# 连接到 Fabric 和 OneLake

Tabular Editor 可连接到 Microsoft Fabric，以列出 Workspace 及其中的 Lakehouse、Warehouse 等项目，并从 OneLake 导入。

![“连接到 Lakehouse”对话框，按名称、类型、所有者和位置列出 OneLake catalog 中的项目](~/content/assets/images/features/connectivity/onelake-connection.png)

## 身份验证方式

Fabric 和 OneLake 使用 Microsoft Entra ID 进行身份验证。交互式登录是默认方式，适用于日常建模工作。如需无人值守刷新，请使用服务主体，并在 Fabric 中授予其对该 Workspace 的访问权限。

Fabric 权限在 Fabric 中授予，而不是在 Tabular Editor 中授予。如果某个帐户可以登录但看不到任何 Workspace，说明它尚未获得这些 Workspace 的访问权限。这是 Fabric 权限问题，不是连接问题。

## Direct Lake

Direct Lake 模型从 OneLake 读取数据，而不是导入数据，因此该连接是模型的一部分，而不是导入步骤。参见 @direct-lake-sql-model。

> [!NOTE]
> 如果无法确定 Lakehouse 或 Warehouse 的 SQL analytics endpoint，Tabular Editor 会改为 Report 该情况，而不会创建一个没有列的表。如果看到该错误，请检查该项目是否已在 Fabric 中完成端点预配。

## 凭据的存储位置

你在此处输入的凭据会按用户和模型分别保存到模型旁的 [用户选项](xref:user-options) 文件 (`.tmuo`) 中，并经过加密，只有你的 Windows 帐户才能读取。它们不属于模型元数据的一部分，因此不会提交到源代码管理；打开同一模型的同事需要提供自己的凭据。

生成的 M 表达式只包含服务器和对象名称。其中绝不包含密码、令牌或密钥。
