---
uid: connect-dataflows
title: 连接到 Power BI Dataflows
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

# 连接到 Power BI Dataflows

Power BI Dataflow 连接器会从你所属的 Power BI Workspaces 中的 Dataflow 导入实体，并且仅作为隐式数据源提供（参见 [传统、结构化和隐式数据源](xref:connectivity#legacy-structured-and-implicit-data-sources)）。

在 **模型 > 导入表...** 中选择 **Power BI Dataflow** 以打开此对话框。

![“连接到 Power BI Workspace”对话框，其中列出了已登录账户所属的 Workspace](~/content/assets/images/features/connectivity/dataflows-connection.png)

## 连接字段

| 字段                                                        | 说明                                   |
| --------------------------------------------------------- | ------------------------------------ |
| **登录...** | 使用 Microsoft Entra ID 登录 Power BI 服务 |
| **Workspace**                                             | 你的账户所属的 Workspace。选择一个 Workspace     |

如果某个 Workspace 没有 Dataflow，则会显示为空。

## 身份验证

**登录...** 会启动 Microsoft Entra ID 的浏览器登录流程。

Tabular Editor 会将连接设置和凭据保存到你的用户选项文件中（参见 [凭据的存储位置](xref:connectivity#where-credentials-are-stored)）。
