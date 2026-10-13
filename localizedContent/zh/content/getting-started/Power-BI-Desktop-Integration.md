---
uid: desktop-integration
title: Power BI Desktop 集成
author: Morten Lønskov
updated: 2026-09-23
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

Tabular Editor 以 [Power BI Desktop 外部工具](https://docs.microsoft.com/en-us/power-bi/create-reports/desktop-external-tools)的形式运行，并对在 Power BI Desktop 中打开的导入模式和 DirectQuery 模式模型执行建模操作。

![从 Power BI Desktop 的“外部工具”功能区启动的 Tabular Editor 3，表达式编辑器中打开了一个度量值](~/content/assets/images/getting-started/power-bi-desktop-integration.png)

## 先决条件

- [Power BI Desktop](https://www.microsoft.com/en-us/download/details.aspx?id=58494)（2020 年七月或更高版本）
- [最新版 Tabular Editor](https://tabulareditor.com/downloads)

此外，强烈建议在 Power BI Desktop 选项的 **数据加载** 下关闭 [自动日期/时间](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-auto-date-time)。

## 外部工具架构

当 Power BI Desktop Report 包含 Data model（即包含一张或多张处于导入模式或 DirectQuery 模式的表）时，Power BI Desktop 会将该 Data model 托管在本地的 Analysis Services 实例中。外部工具会连接到此实例。

> [!IMPORTANT]
> 使用 **Live Connection** 连接到 SSAS、Azure AS 或 Power BI Workspace 中的 Dataset 的 Power BI Desktop Report 不包含 Data model，因此 Tabular Editor 等外部工具**无法**连接到这些 Report。

> [!IMPORTANT]
> 在 Power BI Desktop 中直接编辑 **Direct Lake** 或其他 Fabric 模型的 Report 不包含 Data model。 Tabular Editor 会像 Power BI Desktop 一样，从服务中打开该模型。

Power BI Desktop 会为该 Analysis Services 实例分配一个端口号。当你从 **外部工具** 功能区启动工具时，Power BI Desktop 会将端口号作为命令行参数传递给该工具，随后 Tabular Editor 会加载 Data model。

<img class="noscale" src="~/content/assets/images/external-tool-architecture.png" />

外部工具连接后，会读取模型元数据，对模型运行 DAX 或 MDX 查询，并与连接到任何其他 Analysis Services 实例时一样，通过 [Microsoft 提供的客户端库](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions) 更改模型元数据。

## 支持的建模操作

从 2025 年六月的 Power BI Desktop 更新开始，外部工具可以更改托管在 Power BI Desktop 中的语义模型的任何部分，包括添加和删除表与列，以及更改数据类型。对于更早版本的 Power BI Desktop，请参阅 [桌面版限制](xref:desktop-limitations) 和 [官方博客文章](https://powerbi.microsoft.com/en-us/blog/open-and-edit-any-semantic-model-with-power-bi-tools/)。
