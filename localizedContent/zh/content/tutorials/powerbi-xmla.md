---
uid: powerbi-xmla
title: 通过 XMLA endpoint 编辑
author: Daniel Otykier
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: 仅适用于 Premium Per User XMLA 终结点
        - edition: Enterprise
          full: true
---

# Editing a Power BI semantic model through the XMLA endpoint

You can use Tabular Editor 3 to connect to a Power BI semantic model published to the Power BI service through the [XMLA endpoint](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools). The XMLA endpoint is available for workspaces assigned to a Microsoft Fabric capacity (F SKU), a Power BI Embedded capacity (A or EM SKU), a legacy Premium capacity (P SKU) or a Premium Per User (PPU) license.

> [!NOTE]
> Power BI Pro licenses are not sufficient for accessing Power BI semantic models in a shared workspace. A Fabric capacity, Embedded capacity, legacy Premium capacity or Premium Per User license is required for XMLA access.

## 先决条件

Tabular Editor requires the XMLA endpoint to allow both read and write access. Microsoft enabled XMLA read/write by default on all Fabric and Power BI capacity SKUs in June 2025. If you can't connect, ask [your capacity admin](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#enable-xmla-read-write) to verify the settings described in @xmla-as-connectivity.

> [!IMPORTANT]
> 如果你使用 Tabular Editor 3，请注意连接到 Power BI XMLA endpoint 的[许可证限制](xref:editions)。 根据你使用的 Power BI Workspace 类型，你至少需要 Tabular Editor 3 商业版或企业版。 根据你使用的 Power BI Workspace 类型，你至少需要 Tabular Editor 3 商业版或企业版。

## 限制

When connecting to a semantic model through the XMLA endpoint, all data modeling operations supported by the [Tabular Object Model (TOM)](https://learn.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) are available for editing. In other words, the [Power BI Desktop Limitations](xref:desktop-limitations) do not apply when editing a semantic model through the XMLA endpoint of the Power BI Service.

## 工作流

Power BI XMLA endpoint 本质上相当于公开了一个 Analysis Services 实例，Tabular Editor 可以连接到该实例。 因此，你可以将 Power BI Workspace 视为 Analysis Services 的**服务器**，而 Workspace 中的每个 Power BI Dataset 则对应 Analysis Services 的**数据库**。 连接到 XMLA endpoint 后，Tabular Editor 的所有建模和管理功能都可用。 如果你决定使用 Tabular Editor 来构建并维护你的 Power BI Dataset，也应考虑为模型元数据使用某种版本控制系统。 As such, you can treat the Power BI workspace as the Analysis Services **server** with each Power BI semantic model in the workspace corresponding to an Analysis Services **database**. 连接到 XMLA endpoint 后，Tabular Editor 的所有建模和管理功能都可用。 If you decide to use Tabular Editor to build and maintain your Power BI semantic models, you should also consider some kind of version control system for your model metadata.

工作流如下：

1. Create a new data model in Tabular Editor or connect to an existing semantic model through the Power BI XMLA endpoint
2. 将此模型保存为 **Model.bim** 文件，或使用 Tabular Editor 的 [保存到文件夹](xref:save-to-folder) 选项。
3. 每当你要更改模型时，加载你在步骤 2 中保存的文件/文件夹。 第一次这样做时，决定是否要使用 [Workspace 数据库](xref:workspace-mode)。
4. Once you are ready to publish your changes to the Power BI service, perform a deployment through Tabular Editor (**Model > Deploy...**), thus creating a new or overwriting an existing semantic model in a Power BI workspace.

## 后续步骤

- @new-pbi-model
- @workspace-mode
- @importing-tables