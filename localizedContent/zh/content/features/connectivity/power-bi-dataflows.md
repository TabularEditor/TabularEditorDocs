---
uid: connect-dataflows
title: 连接到 Power BI Dataflows
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

# 连接到 Power BI Dataflows

Tabular Editor 可以从 Power BI Dataflow 导入实体，使模型能够复用 Workspace 中已有的转换，而无需重复执行。

![“连接到 Power BI Workspace”对话框，其中列出了已登录账户所属的 Workspace](~/content/assets/images/features/connectivity/dataflows-connection.png)

## 身份验证方式

Dataflows 通过 Microsoft Entra ID 向 Power BI 服务进行身份验证。

| 你需要提供的内容                  | 适用场景        |
| ------------------------- | ----------- |
| 交互式 Microsoft Entra ID 登录 | 常规交互式使用     |
| 服务主体                      | 计划刷新或无人值守刷新 |

你会看到你的账户所属的 Workspace。你未被添加到的 Workspace 中的 Dataflow 不会显示；没有任何 Dataflow 的 Workspace 会显示为空，而不会被隐藏。

> [!NOTE]
> 在服务主体能够列出任何 Workspace 之前，Power BI 管理员必须先在租户设置中启用对 Power BI REST API 的服务主体访问。在启用之前，服务主体即使登录成功，也看不到任何内容。

## 凭据的存储位置

你在这里输入的凭据会按用户、按模型保存到模型旁边的 [用户选项](xref:user-options) 文件（`.tmuo`）中，并经过加密，只有你的 Windows 账户才能读取。它们不属于模型元数据，因此不会提交到源代码管理；打开同一模型的同事需要提供自己的凭据。

生成的 M 表达式只包含服务器和对象的名称。其中绝不会包含密码、令牌或密钥。
