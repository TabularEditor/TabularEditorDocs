---
uid: new-pbi-model
title: 创建 Power BI 语义模型
author: Daniel Otykier
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "仅限高级每用户 XMLA 终结点"
        - edition: Enterprise
          full: true
---

# （教程）创建第一个 Power BI 语义模型

本页将带你从零开始，使用 Tabular Editor 3 创建一个全新的 Power BI 语义模型。

> [!IMPORTANT]
> Tabular Editor 3 Business Edition is limited to [Power BI Premium Per User](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-per-user-faq). For Fabric, Power BI Premium or Embedded capacity, you must upgrade to Tabular Editor 3 Enterprise Edition. In either case, the target workspace must allow [XMLA read/write access](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#enable-xmla-read-write) - the default on all capacity SKUs since June 2025.
>
> Tabular Editor 3 桌面版不支持 Power BI 语义模型。
>
> [更多信息](xref:editions)。

##### 创建新的语义模型

1. 在“文件”菜单中，选择“新建” > “模型……” 或按 `CTRL+N`

![新建模型](~/content/assets/images/tutorials/new-pbi-model.png)

- 为模型指定名称，或使用默认值。 为模型指定名称，或使用默认值。 然后，将兼容级别设置为“1609（Power BI / Fabric）”。
- 为了获得最佳开发体验，请勾选“使用 Workspace 数据库”选项。 这要求你在 Power BI 中有一个可用的开发 Workspace，并已启用 XMLA 读/写。 为了获得最佳开发体验，请勾选“使用 Workspace 数据库”选项。 这要求你在 Power BI 中有一个可用的开发 Workspace，并已启用 XMLA 读/写。 单击“确定”后，系统会提示你输入 Power BI Workspace 的连接字符串，以便在该 Power BI Workspace 中创建 Workspace 数据库。

> [!NOTE]
> 使用 Workspace 数据库，你可以验证 Power Query（M 表达式），并从 Power Query 表达式中导入表架构。 你还可以在 Workspace 数据库中刷新和查询数据，便于调试和测试 DAX 表达式。 你还可以在 Workspace 数据库中刷新和查询数据，便于调试和测试 DAX 表达式。
