---
uid: new-pbi-model
title: 创建 Power BI 语义模型
author: Daniel Otykier
updated: 2021-09-06
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
> Tabular Editor 3 商业版仅适用于 [Power BI Premium Per User](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-per-user-faq)。 如果你使用 Fabric/Power BI Premium 或 Embedded 容量，则必须升级到 Tabular Editor 3 企业版。 无论哪种情况，要部署语义模型的 Power BI Workspace 都必须启用 [XMLA 读/写端点](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#enable-xmla-read-write)。
>
> Tabular Editor 3 桌面版不支持 Power BI 语义模型。
>
> [更多信息](xref:editions)。

##### 创建新的语义模型

1. 在“文件”菜单中，选择“新建” > “模型……” 或按 `CTRL+N`

![新建模型](~/content/assets/images/tutorials/new-pbi-model.png)

- 为模型指定名称，或使用默认值。 然后，将兼容级别设置为“1609（Power BI / Fabric）”。
- 为了获得最佳开发体验，请勾选“使用 Workspace 数据库”选项。 这要求你在 Power BI 中有一个可用的开发 Workspace，并已启用 XMLA 读/写。 单击“确定”后，系统会提示你输入 Power BI Workspace 的连接字符串，以便在该 Power BI Workspace 中创建 Workspace 数据库。

> [!NOTE]
> 使用 Workspace 数据库，你可以验证 Power Query（M 表达式），并从 Power Query 表达式中导入表架构。 你还可以在 Workspace 数据库中刷新和查询数据，便于调试和测试 DAX 表达式。
