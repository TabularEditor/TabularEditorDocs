---
uid: change-compatibility-mode
title: 更改兼容模式
author: Morten Lønskov
updated: 2026-04-08
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

# 更改兼容模式

模型的 **兼容模式** 决定模型面向的平台。 该属性决定： 该属性决定：

- 可用的 Tabular Object Model (TOM) 对象和属性
- Tabular Editor 将应用哪些版本限制

兼容模式与 [兼容级别](xref:update-compatibility-level) 是两个不同的概念，兼容级别会通过版本号来限定可用功能。

## 兼容模式的取值

`Database.CompatibilityMode` 属性可取以下值，这些值由 [Microsoft.AnalysisServices.CompatibilityMode](https://learn.microsoft.com/dotnet/api/microsoft.analysisservices.compatibilitymode?view=analysisservices-dotnet) 枚举定义：

| 值                  | 含义                                                                                                                                                                                                                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Unknown`          | 未指定具体模式。 当未显式设置模式时的默认值。 未指定具体模式。 当未显式设置模式时的默认值。 AS 客户端库会根据所使用的 TOM 功能自动检测实际模式（例如，是否包含任何 Power BI 特有功能）。                                                                                                                                                                                           |
| `AnalysisServices` | 模型以 SQL Server Analysis Services 或 Azure Analysis Services 为目标。                                                                                                                                                                                                                                   |
| `PowerBI`          | 模型以 Power BI（Desktop、Premium Per User、Premium Capacity、Fabric）为目标。 某些 TOM 属性仅在此模式下可用。 有关详细信息，请参阅 [Microsoft.AnalysisServices.Tabular 命名空间参考](https://learn.microsoft.com/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet) 中各属性的“备注”部分。 |
| `Excel`            | 该模型源自 Excel Power Pivot Data model。 该模型源自 Excel Power Pivot Data model。 Tabular Editor 不支持 Power Pivot 模型。                                                                                                                                                                                        |

Azure Analysis Services 和 SQL Server Analysis Services 仅支持 `AnalysisServices` 模式。 Power BI 和 Fabric 同时支持 `AnalysisServices` 和 `PowerBI` 模式。 Power BI 和 Fabric 同时支持 `AnalysisServices` 和 `PowerBI` 模式。

> [!IMPORTANT]
> Tabular Editor 使用兼容模式来确定版本限制。 [!IMPORTANT]
> Tabular Editor 使用兼容模式来确定版本限制。 即使将模型部署到 Power BI，只要模型设置为 `AnalysisServices` 模式，透视和多个分区等功能仍会触发“仅企业版可用”的限制。

## 何时更改兼容模式

当以下条件全部满足时，将兼容模式更改为 `PowerBI`：

- 模型部署到 Power BI（Premium Per User、Premium Capacity 或 Fabric）
- 该模型**不会**部署到 SSAS 或 Azure Analysis Services
- 该 `.bim` 文件最初是在 Visual Studio、SSDT 或其他默认使用 `AnalysisServices` 模式的工具中创建的
- 你收到关于企业版功能（如透视）的版本错误提示，但对于 Power BI 模型而言，这些功能在你当前版本中本应可用

## 更改兼容模式

1. 在 Tabular Editor 中打开模型。
2. 在 **TOM Explorer** 中，选择顶级 **Model** 节点。
3. 在 **Properties** 面板中，展开 **Database**。
4. 找到 `CompatibilityMode`。
5. 将该值从 `AnalysisServices` 更改为 `PowerBI`。
6. 保存模型（**Ctrl+S**）。

![更改兼容模式](~/content/assets/images/how-to/change-compatibility-mode.png)

> [!NOTE]
> 更改兼容模式会影响哪些 TOM 属性可用，以及模型的验证方式。 保存前，先确认部署目标与所选模式一致。 保存前，先确认部署目标与所选模式一致。

