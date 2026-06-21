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

# 通过 XMLA endpoint 编辑 Power BI 语义模型

你可以使用 Tabular Editor 3，通过 [XMLA endpoint](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools) 连接到已发布到 Power BI 服务的 Power BI 语义模型。 分配到 Fabric capacity（F SKU）、Power BI Embedded capacity（A 或 EM SKU）或旧版 Premium capacity（P SKU）的 Workspace，或使用 Premium Per User（PPU）许可证时，均可使用 XMLA endpoint。

> [!NOTE]
> 仅有 Power BI Pro 许可证不足以在共享 Workspace 中访问 Power BI 语义模型。 XMLA 访问需要 Fabric capacity、Embedded capacity、旧版 Premium capacity 或 Premium Per User 许可证。

## 先决条件

Tabular Editor 要求 XMLA endpoint 同时允许读取和写入访问。 Microsoft 已于 2025 年六月在所有 Fabric 和 Power BI 容量 SKU 上默认启用 XMLA 读取/写入。 如果无法连接，请让 [你的容量管理员](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#enable-xmla-read-write) 验证 @xmla-as-connectivity 中描述的设置。

> [!IMPORTANT]
> 如果你使用 Tabular Editor 3，请注意连接到 Power BI XMLA endpoint 的[许可证限制](xref:editions)。 根据你使用的 Power BI Workspace 类型，你至少需要 Tabular Editor 3 商业版或企业版。

## 限制

通过 XMLA endpoint 连接到语义模型时，可以编辑 [Tabular Object Model (TOM)](https://learn.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 支持的所有数据建模操作。 换句话说，通过 Power BI 服务的 XMLA endpoint 编辑语义模型时，[Power BI Desktop Limitations](xref:desktop-limitations) 不适用。

## 工作流

Power BI XMLA endpoint 本质上相当于公开了一个 Analysis Services 实例，Tabular Editor 可以连接到该实例。 因此，你可以将 Power BI Workspace 视为 Analysis Services **服务器**，而 Workspace 中的每个 Power BI 语义模型都对应一个 Analysis Services **数据库**。 连接到 XMLA endpoint 后，Tabular Editor 的所有建模和管理功能都可用。 如果你决定使用 Tabular Editor 来构建和维护 Power BI 语义模型，也应考虑为模型元数据使用某种版本控制系统。

工作流如下：

1. 在 Tabular Editor 中创建新的 Data model，或通过 Power BI 的 XMLA endpoint 连接到现有的语义模型
2. 将此模型保存为 **Model.bim** 文件，或使用 Tabular Editor 的 [保存到文件夹](xref:save-to-folder) 选项。
3. 每当你要更改模型时，加载你在步骤 2 中保存的文件/文件夹。 第一次这样做时，决定是否要使用 [Workspace 数据库](xref:workspace-mode)。
4. 当你准备将更改发布到 Power BI 服务时，通过 Tabular Editor 进行部署（**Model > Deploy...**），从而在 Power BI Workspace 中创建新的语义模型，或覆盖现有语义模型。

## 后续步骤

- @new-pbi-model
- @workspace-mode
- @importing-tables