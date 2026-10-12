---
uid: connect-onelake
title: 连接到 Fabric 和 OneLake
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

# 连接到 Fabric 和 OneLake

Fabric 连接器会列出你可访问的 Fabric Workspace 中的 Lakehouse、Warehouse、SQL 数据库和镜像数据库项目，并从这些项目中导入表。已镜像的 Azure Databricks 目录会显示为镜像数据库。在 **模型 > 导入表...** 中选择 **Microsoft Fabric Lakehouse**、**Microsoft Fabric Warehouse**、**Microsoft Fabric SQL Database** 或 **Microsoft Fabric Mirrored Database**，即可打开此对话框。

![“连接到 Lakehouse”对话框，按名称、类型、所有者和位置列出 OneLake catalog 中的项目](~/content/assets/images/features/connectivity/onelake-connection.png)

## 连接字段

| 字段                                                        | 说明                                                                  |
| --------------------------------------------------------- | ------------------------------------------------------------------- |
| **登录...** | 使用 Microsoft Entra ID 登录 Power BI 服务                                |
| **OneLake 目录项**                                           | 列出你可访问的 Workspace 中所选类型的项目，并显示其 **名称**、**类型**、**所有者** 和 **位置**。选择一项 |

## 身份验证

**登录...** 会启动 Microsoft Entra ID 浏览器登录流程。如果你登录后仍未看到任何项目，说明你的帐户无权访问包含这些项目的 Workspace。Workspace 管理员需要在 Fabric 中授予你相应的访问权限。

Tabular Editor 会将连接设置和凭据保存到你的用户选项文件中（请参阅[凭据的存储位置](xref:connectivity#where-credentials-are-stored)）。

## 导入与 Direct Lake

在表导入向导的最后一页，你可以选择将所选表创建为导入模式还是 Direct Lake 模式：

- 导入表会通过该项的 SQL analytics endpoint 读取其架构。请参阅[选择要导入的对象](xref:import-tables#choosing-objects-to-import)。
- Direct Lake 表直接从 OneLake 读取。参见 @direct-lake-sql-model。
