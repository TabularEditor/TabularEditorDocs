---
uid: connect-ssas
title: 连接并部署到 Analysis Services
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 连接并部署到 Analysis Services

你可以直接从服务器而不是从文件打开语义模型，对其进行操作，并将更改写回服务器。这涵盖 SQL Server Analysis Services、Azure Analysis Services，以及 Power BI / Fabric 的 XMLA endpoint。

## 从服务器打开模型

选择 **文件 > 打开 > 从数据库打开模型...**（**Ctrl+Shift+O**），然后输入服务器地址。随后，Tabular Editor 会列出该服务器上的数据库，供你选择要加载的数据库。

- 对于 **SQL Server Analysis Services**，使用实例名称，例如 `localhost` 或 `myserver\\tabular`。
- 对于 **Azure Analysis Services**，使用以 `asazure://` 开头的完整实例名称。
- 对于 **Power BI / Fabric XMLA endpoint**，请使用以 `powerbi://` 开头的 Workspace 连接字符串。
- **本地实例**下拉列表会列出正在运行的 Power BI Desktop 实例以及 Visual Studio 集成 Workspace，这样你就可以在不知道端口的情况下附加到其中一个。

@xmla-as-connectivity 完整介绍了连接对话框，包括身份验证模式、高级连接字符串属性、每个连接的状态栏颜色，以及连接失败时要检查的内容。 @load-save-model 列出了打开模型的所有方式。

## 将更改写回

**文件 > 保存**（**Ctrl+S**）会将你的更改写入已连接的数据库。 Excel、Power BI 和 DAX Studio 等客户端工具会立即反映这些更改。根据你所做的更改，模型再次可供查询之前，可能需要先重新计算相关对象。

如果你想改为将连接模式下的模型复制到磁盘，可以使用 **文件 > 另存为...** 或 **文件 > 保存到文件夹...**。

## 部署到其他数据库

保存会更新你当前连接的数据库。如果要将已加载的模型推送到 _其他_ 服务器或数据库，请改用 @deployment 中介绍的 Deployment Wizard 部署向导。

## 编辑 Power BI Desktop 模型

Tabular Editor 可以通过 **本地实例** 下拉列表附加到正在运行的 Power BI Desktop 实例。自 2025 年六月的 Power BI Desktop 更新起，已不再存在任何不受支持的写入操作，因此第三方工具可以自由修改托管在 Desktop 中的语义模型。在较早版本中，部分操作受限；请参阅 @desktop-limitations 和 @desktop-integration。
