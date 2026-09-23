---
uid: editions
title: 比较版本
author: Søren Toft Joensen
updated: 2026-09-22
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
> Tabular Editor 3 许可证为**按开发者**授权。换句话说，只有实际使用 Tabular Editor 3 产品的人才需要许可证。

The editions differ in two ways: **which data modeling scenarios** they support - that is, where the model you are editing may live - and **which features** are available once it is open. The two sections below cover each in turn. Anything not listed in either is available in every edition.

> [!TIP]
> Upgrading a license takes effect straight away. Activate the new key under **Help > About Tabular Editor**, and the features it unlocks are available without restarting Tabular Editor 3.

## 支持的 Data model 建模场景

The first difference between the editions is which types of tabular data modeling scenarios they support. 要理解这一差异，可以把 Analysis Services（Tabular）看作有多种不同的“形态”：

- Power BI Desktop（请确保您了解[限制](xref:desktop-limitations)）
- 通过 XMLA 终结点使用的 Power BI Premium（Premium Per User、**Premium 容量 [A、EM 或 P SKUs]**、**Fabric 容量 [F SKUs]**）
- SQL Server（2016+）Analysis Services（版本：开发人员版、标准版、**企业版**）
- Azure Analysis Services（层级：开发者层、基本层、**标准层**）

我们将 Analysis Services 中**突出显示**的这些形态视为企业级，因此只能在 Tabular Editor 3 企业版中使用。

我们与 Microsoft 一样，在按用户授权与按容量授权之间划定界线：

- **Premium Per User 是按席位许可。** 编辑模型的人必须就是购买该席位的那位用户。这与商业版的授权方式一致：个人、不可转让的密钥，绑定到单一用户。请参阅 [个人许可证与可转让许可证](#personal-vs-transferable-licenses)。
- **Premium Capacity（P SKU）、Embedded Capacity（A/EM SKU）和 Fabric Capacity（F SKU）属于共享的组织级部署。** 托管在这些容量上的模型归团队所有，并服务于众多使用者——这正是企业版的设计与定价所针对的场景。

同样的逻辑也适用于 Power BI 之外的场景。商业版涵盖 SQL Server Analysis Services 的 Developer 和 Standard 版本，以及 Azure Analysis Services 的 Developer 和 Basic 层级。这些版本和层级通常面向单个开发者或小规模部署。 SQL Server Analysis Services Enterprise Edition 和 Azure Analysis Services Standard 层用于托管组织级模型，因此需要企业版。

> [!IMPORTANT]
> Tabular Editor 仅允许编辑兼容级别为 1200 或更高的数据模型。自 SQL Server 2016 起，Analysis Services 的所有实例默认都是如此。出于同样的原因，Tabular Editor 不支持 Excel PowerPivot，因为它使用更早的兼容级别。

支持的场景完整概览见下方矩阵：

| 场景 / 版本                        | 桌面版                                                     | 商业版                                                       | 企业版                                                     |
| ------------------------------ | ------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| Power BI Desktop 外部工具          | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| 将模型元数据加载/保存到磁盘\*\*             | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| 工作区模式\*\*\*                    | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Power BI Premium 按用户           | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| SQL Server 开发者版                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| SQL Server 标准版                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| SQL Server 企业版                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Azure AS 开发者层                  | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Azure AS 基础层                   | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Azure AS 标准层                   | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Power BI Premium 容量（P SKU）     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Power BI Embedded 容量（A/EM SKU） | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Fabric 容量（F SKU）               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |

\***注：** 如果 Analysis Services Data model 包含透视或包含多个分区的表，则需要企业版（不适用于 Power BI Desktop 或 Power BI Premium Per User 模型）。

\*\***注意：** 支持的文件格式包括：**.pbip**（Power BI Project）、**.pbit**（Power BI 模板）、**.bim**（Analysis Services 模型元数据）、**.vpax**（VertiPaq分析器）以及**Database.json**（Tabular Editor 文件夹结构）、**TMDL**（Tabular Model Definition Language，表格模型定义语言）。

\*\*\***注：** 工作区模式允许 Tabular Editor 3 同时将模型元数据保存到磁盘，并同步所购买的 Tabular Editor 3 版本支持的任意 Analysis Services 或 Power BI 版本上的数据库。

## Feature availability

Beyond the scenarios above, these are the features whose availability depends on the edition. Trial and Consultancy licenses carry the Enterprise Edition feature set.

### Editing and refreshing

| 功能                                                                                                       | 桌面版                                                     | 商务版                                                     | 企业版                                                     |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| [Save with supporting files](xref:save-with-supporting-files) for Fabric                                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| [Advanced Refresh dialog](xref:advanced-refresh) and [refresh override profiles](xref:refresh-overrides) | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Automatic metadata backups on save and deploy                                                            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |

Ordinary refresh commands, and everything else in the refresh menu, are available in every edition. The three rows above are unavailable in Desktop Edition because that edition works only against a live Power BI Desktop model, with no model files of its own.

### Modeling features

| 功能                                                                  | 桌面版                                                     | 商业版                                                     | 企业版                                                     |
| ------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Perspectives in an Analysis Services model\*                        | 不适用                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Tables with multiple partitions in an Analysis Services model\*     | 不适用                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Perspectives and multiple partitions in a Power BI model            | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Direct Lake tables                                                  | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| [Semantic Bridge](xref:semantic-bridge) for Databricks Metric Views | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

\***Note:** Desktop Edition cannot open Analysis Services models at all, which is why these two rows do not apply to it. See [Modeling Restrictions](#modeling-restrictions) below for what happens when a model uses one of these features on an edition that does not allow it.

The Semantic Bridge row covers the **Import from Metric View YAML...** command and the `SemanticBridge` object in [C# scripts](xref:csharp-scripts); on a lower edition the menu item is not shown, and a script that reaches for the service reports that it is unavailable at your license level.

### AI Assistant, MCP server and administrator policies

The [AI Assistant](xref:ai-assistant) and the [MCP server](xref:mcp-server) themselves are available in every edition. What Enterprise Edition adds is the ability to govern them centrally, and a record of what they did.

| 功能                                                                                                                      | 桌面版                                                     | 商业版                                                     | 企业版                                                     |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| AI Assistant and MCP server                                                                                             | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| General administrator [policies](xref:policies), such as turning off updates, telemetry, scripts, macros or AI entirely | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Capping what the AI Assistant and the MCP server may reach, per resource                                                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Locking the AI provider, endpoint, model, organization and project, or restricting them to an allowlist                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Publishing Custom Instructions for the organization, and ruling out the ones a user keeps                               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Withholding individual MCP tools, and fixing the MCP server port                                                        | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Allowing only C# scripts and macros that stay within the model (`BlockUnsafeScripts`)                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| A local audit record of AI Assistant and MCP server activity                                                            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

> [!IMPORTANT]
> The Enterprise policies are never quietly ignored on an edition that is not licensed for them. If any of their values is set on a machine running Desktop or Business Edition, the AI Assistant and the MCP server refuse to start and name the values that require Enterprise Edition, and a `BlockUnsafeScripts` value stops every script and macro from running until an Enterprise license is activated. Roll them out against the licenses you actually have. See @policies.

### Licensing and support

| 功能                                                                    | 桌面版                                                     | 商业版                                                     | 企业版                                                     |
| --------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| [Free DAX Optimizer access](xref:dax-optimizer-integration)           | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| **Help > Dedicated Support** for contacting our support team directly | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Simultaneous installations per user                                   | 1                                                       | 2                                                       | 3                                                       |

The DAX Optimizer _integration_ itself is in every edition; what Enterprise Edition adds is eligibility for a redemption code that gives you DAX Optimizer access at no extra cost.

### Available in every edition

Everything else is the same whichever edition you hold, including the DAX editor and IntelliSense-like [code assist](xref:code-actions), [DAX queries](xref:dax-query) and the [DAX debugger](xref:dax-debugger), [DAX scripts](xref:dax-scripts) and [user-defined functions](xref:udfs), [C# scripts](xref:csharp-scripts) and [macros](xref:macros), the [Best Practice Analyzer](xref:using-bpa) with its [built-in rules](xref:built-in-bpa-rules), the [Perspective Editor](xref:perspective-editor), the [Metadata Translation Editor](xref:metadata-translation-editor), the [Calendar Editor](xref:calendars), [table groups](xref:table-groups), [diagrams](xref:diagram-view), [data preview](xref:table-preview) and [pivot grids](xref:pivot-grid), the VertiPaq Analyzer integration, the [DAX Package Manager](xref:dax-package-manager), the [Table Import Wizard](xref:import-tables) and [unsaved change indicators](xref:unsaved-changes).

## 建模限制

我们也会在 Tabular Editor 3 中限制部分 Data model 建模操作，以与 Microsoft 某些服务层级（Azure Analysis Services _Basic Tier_、SQL Server Analysis Services _Standard Edition_，以及 Power BI _Premium-Per-User_）的限制保持一致。

Specifically, [Azure AS Basic Tier and SQL Server Standard Edition do not support perspectives or multiple partitions](https://azure.microsoft.com/en-us/pricing/details/analysis-services/), and as such, SSAS/Azure AS models using these features require TE3 Enterprise Edition. DirectQuery is not restricted by your Tabular Editor 3 edition at all: whether you can use it depends on the server the model is hosted on.

同样地，[Power BI Premium-Per-User Workspace 不支持 Direct Lake Dataset](https://learn.microsoft.com/en-us/power-bi/enterprise/directlake-overview#prerequisites)，所以使用该功能的 Power BI 模型也需要 TE3 企业版。

| 模型类型            | 功能            | 桌面版                                                     | 商业版                                                     | 企业版                                                     |
| --------------- | ------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Azure AS / SSAS | 透视            | N/A                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | 多个分区          | N/A                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | DirectQuery\* | N/A                                                     | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | Direct Lake   | N/A                                                     | N/A                                                     | N/A                                                     |
| Power BI        | 透视\*\*        | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | 多个分区\*\*      | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | DirectQuery   | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | Direct Lake   | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

\***注：** SQL Server 标准版 2019 之前的 Analysis Services 不支持 DirectQuery。 Azure AS 基本层也同样不支持 DirectQuery。[了解更多](https://learn.microsoft.com/en-us/analysis-services/analysis-services-features-by-edition?view=asallproducts-allversions#tabular-models)。

\*\***注意：** 在商业版中，Power BI 模型支持透视和多个分区，但模型的 `CompatibilityMode` 必须设置为 `PowerBI`。有关操作说明，请参阅 [更改兼容模式](xref:change-compatibility-mode)。

Desktop Edition works only against a live Power BI Desktop model, which is why the Analysis Services rows do not apply to it.

如果您在使用 TE3 商业版许可证时尝试打开一个应用了上述一项或多项建模限制的模型，将会看到以下错误信息：

![此版本的 Tabular Editor 3 不支持企业级语义模型](~/content/assets/images/editions-01.png)

A model that acquires one of these while you are editing it is not silently mangled either: the save is refused, and the message names the feature and, for multiple partitions, the tables in question. Adding a perspective to an Analysis Services model is prevented up front - the **Perspectives** folder is not shown in the TOM Explorer and the command to create one is unavailable.

> [!IMPORTANT]
> 只有当 Power BI Report（.pbix、.pbip 或 .pbit）文件包含 Data model（Import、DirectQuery 或 Composite）时，Tabular Editor 才能在 Power BI Desktop 中作为外部工具使用。**不支持使用 Live connection 的 Report**，因为这些 Report 不包含 Data model。[更多信息](xref:desktop-limitations)。

## 个人许可证与可转让许可证

我们的桌面版和商业版采用**个人**许可模式。这意味着每位用户都会获得自己的个人许可证密钥，该密钥无法与其他用户共享或转让。当用户不再需要该产品时，应取消订阅，以避免产生续费。

我们的企业版采用**可转让**许可模式。许可证管理员会收到一个许可证密钥，该密钥对一定数量的具名用户有效，数量上限为购买的席位数。用户通过其电子邮件地址进行识别；该地址需要在用户首次激活 Tabular Editor 3 安装时输入。用户首次使用许可证密钥激活 Tabular Editor 3 安装时，会在该许可证下被“锁定”30 天。 30 天锁定期结束后，可随时将用户从许可证中移除，从而释放许可证名额供其他用户使用。许可证管理员可通过我们的[自助门户](https://tabulareditor.com/my-account)查看和管理用户。你也可以<a href="mailto:support@tabulareditor.com?subject=Transferable%20License%20Rotation">联系支持团队</a>获取帮助。

## 多台设备安装

每位 Tabular Editor 3 用户可根据所持许可证类型，在多台设备上安装该工具：

|           | 桌面版 | 商业版 | 企业版 |
| --------- | --- | --- | --- |
| 可同时激活的安装数 | 1   | 2   | 3   |

> [!NOTE]
> 在多个用户之间共享同一许可证违反我们的[许可条款](https://tabulareditor.com/eula-te3)。

你可以随时在工具内停用现有安装：在“帮助 > 关于 Tabular Editor”下选择“更改许可证密钥...”选项。你也可以通过我们的[自助门户](https://tabulareditor.com/sign-in)停用安装：进入“Licenses”选项卡。

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

## 命令行与 CI/CD 授权许可

Tabular Editor 3 是一款桌面应用程序。它本身没有命令行界面。对于自动化部署和 CI/CD 流水线，可使用 `TabularEditor.exe`（[Tabular Editor 2 命令行](xref:command-line-options)）或跨平台的 [Tabular Editor CLI](xref:te-cli)（`te`）。两者都独立于 Tabular Editor 3 桌面应用程序。

> **运行 CI/CD 管道需要许可证吗？**
> 不需要。 `TabularEditor.exe`（TE2 CLI）和 Tabular Editor CLI（`te`，处于预览阶段）不需要 Tabular Editor 3 许可证。只有使用 Tabular Editor 3 桌面应用程序的开发人员才需要许可证。

Tabular Editor CLI 在正式发布（GA）时将需要许可证；定价仍在最终确定中，并会在 GA 之前公布。