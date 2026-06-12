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

当 Power BI Desktop Report 包含 Data model（即以导入或 DirectQuery 模式添加了一张或多张表）时，该 Data model 会托管在由 Power BI Desktop 管理的 Analysis Services 实例中。 外部工具可以出于不同目的连接到该 Analysis Services 实例。 外部工具可以出于不同目的连接到该 Analysis Services 实例。

> [!IMPORTANT]
> 通过 **Live Connection** 连接到 SSAS、Azure AS 或 Power BI Workspace 中的 Dataset 的 Power BI Desktop Report 不包含 Data model。 因此，这些 Report **无法**与 Tabular Editor 等外部工具一起使用。 因此，这些 Report **无法**与 Tabular Editor 等外部工具一起使用。

> [!IMPORTANT]
> 直接编辑 Fabric 中的 **Direct Lake** 或其他模型的 Power BI Desktop Report 不包含 Data model。 相反，Tabular Editor 将直接从服务中打开模型——这基本上也是 Power BI Desktop 的做法。 相反，Tabular Editor 将直接从服务中打开模型——这基本上也是 Power BI Desktop 的做法。

外部工具可以通过 Power BI Desktop 分配的特定端口号，连接到由 Power BI Desktop 管理的 Analysis Services 实例。 当你从 Power BI Desktop 的“外部工具”功能区直接启动某个工具时，该端口号会作为命令行参数传递给外部工具。 对于 Tabular Editor 而言，这会使其加载该 Data model。 当你从 Power BI Desktop 的“外部工具”功能区直接启动某个工具时，该端口号会作为命令行参数传递给外部工具。 对于 Tabular Editor 而言，这会使其加载该 Data model。

<img class="noscale" src="~/content/assets/images/external-tool-architecture.png" />

一旦连接到 Analysis Services 实例，外部工具就可以获取模型元数据信息，针对 Data model 执行 DAX 或 MDX 查询，甚至还能通过 [Microsoft 提供的客户端库](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions) 来更改模型元数据。 从这一点来看，由 Power BI Desktop 管理的 Analysis Services 实例与任何其他类型的 Analysis Services 实例并无不同。 从这一点来看，由 Power BI Desktop 管理的 Analysis Services 实例与任何其他类型的 Analysis Services 实例并无不同。

## 支持的建模操作

从 2025 年六月的 Power BI Desktop 更新开始，已不再存在任何不受支持的写入操作。 换句话说，第三方工具现在可以自由修改托管在 Power BI Desktop 中的语义模型的任何方面，包括添加和删除表与列、更改数据类型等。 不过，如果您使用的是 2025 年六月更新之前版本的 Power BI Desktop，请参阅[桌面版限制](xref:desktop-limitations)一文了解相关限制。 换句话说，第三方工具现在可以自由修改托管在 Power BI Desktop 中的语义模型的任何方面，包括添加和删除表与列、更改数据类型等。 不过，如果您使用的是 2025 年六月更新之前版本的 Power BI Desktop，请参阅[桌面版限制](xref:desktop-limitations)一文了解相关限制。

更多信息请参阅[官方博客文章](https://powerbi.microsoft.com/en-us/blog/open-and-edit-any-semantic-model-with-power-bi-tools/)。
