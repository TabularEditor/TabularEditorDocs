---
uid: desktop-integration
title: Power BI Desktop 集成
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Power BI Desktop 集成

[Power BI Desktop 支持外部工具](https://docs.microsoft.com/en-us/power-bi/create-reports/desktop-external-tools)，这使 Tabular Editor 在桌面版中处理导入或 DirectQuery 数据时能够执行建模操作。

![image](~/content/assets/images/getting-started/power-bi-desktop-integration.png)

## 先决条件

- [Power BI Desktop](https://www.microsoft.com/en-us/download/details.aspx?id=58494)（2020 年七月或更高版本）
- [最新版 Tabular Editor](https://tabulareditor.com/downloads)

此外，强烈建议**禁用**[自动日期/时间](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-auto-date-time)（Power BI Desktop 中“数据加载”下的设置）。

## 外部工具架构

当 Power BI Desktop Report 包含 Data model（即以导入或 DirectQuery 模式添加了一张或多张表）时，该 Data model 会托管在由 Power BI Desktop 管理的 Analysis Services 实例中。 External Tools may connect to this instance of Analysis Services for different purposes.

> [!IMPORTANT]
> 通过 **Live Connection** 连接到 SSAS、Azure AS 或 Power BI Workspace 中的 Dataset 的 Power BI Desktop Report 不包含 Data model。 As such, these reports **cannot** be used with external tools such as Tabular Editor.

> [!IMPORTANT]
> Power BI Desktop reports that directly edits a **Direct Lake** or other Fabric model do not contain a data model. Instead, Tabular Editor will open the model directly from the service which is essentially what Power BI Desktop also does.

外部工具可以通过 Power BI Desktop 分配的特定端口号，连接到由 Power BI Desktop 管理的 Analysis Services 实例。 When a tool is launched directly from the "External Tools" ribbon in Power BI Desktop, this port number is passed to the external tool as a command line argument. In Tabular Editor's case, this causes the data model to be loaded in Tabular Editor.

<img class="noscale" src="~/content/assets/images/external-tool-architecture.png" />

一旦连接到 Analysis Services 实例，外部工具就可以获取模型元数据信息，针对 Data model 执行 DAX 或 MDX 查询，甚至还能通过 [Microsoft 提供的客户端库](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions) 来更改模型元数据。 In this regard, the Analysis Services instance managed by Power BI Desktop is no different from any other type of Analysis Services instance.

## 支持的建模操作

从 2025 年六月的 Power BI Desktop 更新开始，已不再存在任何不受支持的写入操作。 In other words, third party tools can now freely modify any aspect of the semantic model hosted in Power BI Desktop, including adding and removing tables and columns, changing data types, etc. However, if you're using a version of Power BI Desktop prior to the June 2025 update, please view the limitations in the [Desktop Limitations](xref:desktop-limitations) article.

更多信息请参阅[官方博客文章](https://powerbi.microsoft.com/en-us/blog/open-and-edit-any-semantic-model-with-power-bi-tools/)。
