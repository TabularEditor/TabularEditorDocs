---
uid: editions
title: 比较版本
author: Søren Toft Joensen
updated: 2025-02-07
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Tabular Editor 3 各版本

本文档概述并对比 Tabular Editor 3 的不同版本。

> [!NOTE]
> Tabular Editor 3 许可证为**按开发者授权**。 换句话说，只有实际使用 Tabular Editor 3 产品的人才需要许可证。

## 支持的 Data model 建模场景

Tabular Editor 3 各版本的主要区别在于它们支持哪些表格 Data model 建模场景。 要理解这一差异，可以把 Analysis Services（Tabular）看作有多种不同的“形态”：

- Power BI Desktop（请确保您了解[限制](xref:desktop-limitations)）
- 通过 XMLA 终结点使用的 Power BI Premium（Premium Per User、**Premium 容量 [A、EM 或 P SKUs]**、**Fabric 容量 [F SKUs]**）
- SQL Server（2016+）Analysis Services（版本：开发人员版、标准版、**企业版**）
- Azure Analysis Services（层级：开发者层、基本层、**标准层**）

我们将 Analysis Services 中**突出显示**的这些形态视为企业级，因此只能在 Tabular Editor 3 企业版中使用。

> [!IMPORTANT]
> Tabular Editor 只允许编辑兼容级别为 1200 或更高的 Data model。 自 SQL Server 2016 起，Analysis Services 的所有实例默认都是如此。 出于同样的原因，Tabular Editor 不支持 Excel PowerPivot，因为它使用更早的兼容级别。

支持的场景完整概览见下方矩阵：

| 场景 / 版本                                        | 桌面版                                                     | 商业版                                                       | 企业版                                                     |
| ---------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| Power BI Desktop 外部工具                          | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| 将模型元数据加载/保存到磁盘\*\*                             | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| 工作区模式\*\*\*                                    | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Power BI Premium 按用户                           | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| SQL Server 开发者版                                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| SQL Server 标准版                                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| SQL Server 企业版                                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Azure AS 开发者层                                  | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Azure AS 基础层                                   | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Azure AS 标准层                                   | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Power BI Premium 容量（P SKU）                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Power BI Embedded 容量（A/EM SKU）                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Fabric 容量（F SKU）                               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Semantic Bridge（Databricks）                    | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| [高级刷新对话框](xref:advanced-refresh)               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| [免费 DAX优化器许可证](xref:dax-optimizer-integration) | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |

\*\*\*注意：\*\*如果 Analysis Services Data model 包含透视，或表包含多个分区，则需要企业版（不适用于 Power BI Desktop 或 Power BI Premium Per User 模型）。

\*\***注意：** 支持的文件格式包括：**.pbip**（Power BI Project）、**.pbit**（Power BI 模板）、**.bim**（Analysis Services 模型元数据）、**.vpax**（VertiPaq分析器）以及**Database.json**（Tabular Editor 文件夹结构）、**TMDL**（Tabular Model Definition Language，表格模型定义语言）。

\*\*\*\*\*注意：\*\*工作区模式允许 Tabular Editor 3 将模型元数据同时保存到磁盘，并与所购买的 Tabular Editor 3 版本所支持的任意 Analysis Services 或 Power BI 版本上的数据库保持同步。

## 建模限制

我们在 Tabular Editor 3 中也会限制一些数据建模操作，以对应 Microsoft 某些服务层级（Azure Analysis Services _Basic 层级_、SQL Server Analysis Services _标准版_，以及 Power BI _Premium-Per-User_）的限制。

具体来说，[Azure AS Basic 层级和 SQL Server Analysis Services 标准版不支持透视、多个分区或 DirectQuery](https://azure.microsoft.com/en-us/pricing/details/analysis-services/)。因此，使用这些功能的 SSAS/Azure AS 模型需要 TE3 企业版。

同样地，[Power BI Premium-Per-User Workspace 不支持 Direct Lake Dataset](https://learn.microsoft.com/en-us/power-bi/enterprise/directlake-overview#prerequisites)，所以使用该功能的 Power BI 模型也需要 TE3 企业版。

| 模型类型            | 功能                      | 商务版                                                     | 企业版                                                     |
| --------------- | ----------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Azure AS / SSAS | 透视                      | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | 多个分区                    | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | DirectQuery\*           | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | Direct Lake             | 不适用                                                     | 不适用                                                     |
| Power BI        | Perspectives\*\*        | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | Multiple partitions\*\* | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | DirectQuery             | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | Direct Lake             | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

\***注意：** SQL Server 标准版 2019 年之前的 Analysis Services 不支持 DirectQuery。 Azure AS 基本层也同样不支持 DirectQuery。 [了解更多](https://learn.microsoft.com/en-us/analysis-services/analysis-services-features-by-edition?view=asallproducts-allversions#tabular-models)。

\*\***Note:** Perspectives and multiple partitions are available in Business Edition for Power BI models, but the model's `CompatibilityMode` must be set to `PowerBI`. See [Change compatibility mode](xref:change-compatibility-mode) for instructions.

如果您在使用 TE3 商业版许可证时尝试打开一个应用了上述一项或多项建模限制的模型，将会看到以下错误信息：

![此版本的 Tabular Editor 3 不支持企业级语义模型](https://github.com/TabularEditor/TabularEditorDocs/assets/8976200/7ef69593-ea4b-4a16-a8df-543f5c31ac65)

除了上面列出的内容之外，Tabular Editor 3 各版本之间没有其他功能差异。

> [!NOTE]
> 注意，Power BI Desktop [目前并不支持所有 Data model 建模操作](xref:desktop-limitations)。 因此，Tabular Editor 3 默认会阻止 Power BI Desktop 不支持的操作。 不过，你可以在“工具 > 偏好 > Power BI”中解除该限制。

> [!IMPORTANT]
> 仅当 Power BI Report（.pbix、.pbip 或 .pbit）文件包含 Data model（导入、DirectQuery 或复合模式）时，Tabular Editor 才能作为 Power BI Desktop 的外部工具使用。 **不支持使用 Live connection 的 Report**，因为这些 Report 不包含 Data model。 [更多信息](xref:desktop-limitations)。

## 个人许可证与可转让许可证

我们的桌面版和商业版采用**个人**许可模式。 这意味着每位用户都会获得自己的个人许可证密钥，该密钥无法与其他用户共享或转让。 当用户不再需要该产品时，应取消订阅，以避免产生续费。

我们的企业版采用**可转让**许可模式。 许可证管理员会收到一个许可证密钥，该密钥对一定数量的具名用户有效，数量上限为购买的席位数。 用户通过其电子邮件地址进行识别；该地址需要在用户首次激活 Tabular Editor 3 安装时输入。 用户首次使用许可证密钥激活 Tabular Editor 3 安装时，会在该许可证下被“锁定”30 天。 30 天锁定期结束后，可随时将用户从许可证中移除，从而释放许可证名额供其他用户使用。 许可证管理员可通过我们的[自助门户](https://tabulareditor.com/my-account)查看和管理用户。 你也可以<a href="mailto:support@tabulareditor.com?subject=Transferable%20License%20Rotation">联系支持团队</a>获取帮助。

## 多台设备安装

每位 Tabular Editor 3 用户可根据所持许可证类型，在多台设备上安装该工具：

|           | 桌面版 | 商业版 | 企业版 |
| --------- | --- | --- | --- |
| 可同时激活的安装数 | 1   | 2   | 3   |

> [!NOTE]
> 在多位用户之间共享同一个许可证违反我们的[许可条款](https://tabulareditor.com/license-terms)。

你可以随时在工具内停用现有安装：在“Help > About Tabular Editor”下选择“Change license key...”。 你也可以通过我们的[自助门户](https://tabulareditor.com/sign-in)停用安装：进入“Licenses”选项卡。

如果您需要的 Tabular Editor 3 并发安装数量超过上述范围，请联系 [licensing@tabulareditor.com](mailto:licensing@tabulareditor.com)。

## 企业版批量折扣

我们的企业版采用分级定价，具体如下表所示（按月承诺也适用类似的折扣率）：

| 档位             | 每席年度价格                      |
| -------------- | --------------------------- |
| 前 5 个席位        | $950.00 USD |
| 接下来的 6-10 个席位  | $900.00 USD |
| 接下来的 11-20 个席位 | $850.00 USD |
| 接下来的 21-50 个席位 | $800.00 USD |
| 51 个席位及以上      | $750.00 USD |

例如，如果您需要 12 个席位，价格构成如下：

```text
席位 1-5：    5 x 950.00 = $  4,750.00
席位 6-10：   5 x 900.00 = $  4,500.00
席位 11-12：  2 x 850.00 = $  1,700.00
--------------------------------------
总计                      $ 10,950.00
======================================
```

如果您需要超过 100 个席位，请 <a href="mailto:sales@tabulareditor.com">联系销售</a> 获取报价。
