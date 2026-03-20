---
uid: powerbi-xmla
title: 通过 XMLA endpoint 编辑
author: Daniel Otykier
updated: 2021-10-01
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
          note: Premium Per User XMLA Endpoints Only
        - edition: Enterprise
          full: true
---

# 通过 XMLA endpoint 编辑 Power BI Dataset

你可以使用 Tabular Editor 3，通过 [XMLA endpoint](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools) 连接到发布到 Power BI 服务的 Power BI Dataset。 XMLA endpoint 可用于 Power BI Premium 容量 Workspace（即分配到 Px、Ax 或 EMx SKU 的 Workspace），或 Power BI Premium Per User（PPU）Workspace。

> [!NOTE]
> 仅有 Power BI Pro 许可证不足以在共享 Workspace 中访问 Power BI Dataset。 进行 XMLA 访问需要 Premium/Embedded 容量或 Power BI Premium Per User 许可。

## 先决条件

Tabular Editor 要求 XMLA endpoint 同时允许读取和写入访问。 该设置由容量管理员控制，详见[这里](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#enable-xmla-read-write)。

> [!IMPORTANT]
> 如果你使用 Tabular Editor 3，请注意连接到 Power BI XMLA endpoint 的[许可证限制](xref:editions)。 根据你使用的 Power BI Workspace 类型，你至少需要 Tabular Editor 3 商业版或企业版。

## 限制

通过 XMLA endpoint 连接到 Dataset 时，可以编辑 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 支持的所有 Data model 建模操作。 换句话说，通过 Power BI 服务的 XMLA endpoint 编辑 Dataset 时，[Power BI Desktop 限制](xref:desktop-limitations) 不适用。

## 工作流

Power BI XMLA endpoint 本质上相当于公开了一个 Analysis Services 实例，Tabular Editor 可以连接到该实例。 因此，你可以将 Power BI Workspace 视为 Analysis Services 的**服务器**，而 Workspace 中的每个 Power BI Dataset 则对应 Analysis Services 的**数据库**。 连接到 XMLA endpoint 后，Tabular Editor 的所有建模和管理功能都可用。 如果你决定使用 Tabular Editor 来构建并维护你的 Power BI Dataset，也应考虑为模型元数据使用某种版本控制系统。

工作流如下：

1. 在 Tabular Editor 中创建新的 Data model，或通过 Power BI 的 XMLA endpoint 连接到现有的 Dataset
2. 将此模型保存为 **Model.bim** 文件，或使用 Tabular Editor 的 [保存到文件夹](xref:save-to-folder) 选项。
3. 每当你要更改模型时，加载你在步骤 2 中保存的文件/文件夹。 第一次这样做时，决定是否要使用 [Workspace 数据库](xref:workspace-mode)。
4. 当你准备将更改发布到 Power BI 服务时，通过 Tabular Editor 进行部署（**Model > Deploy...**），从而在 Power BI Workspace 中创建新的 Dataset，或覆盖现有 Dataset。

## 后续步骤

- @new-pbi-model
- @workspace-mode
- @importing-tables