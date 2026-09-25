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
> Tabular Editor 3 许可证为**按开发者**授权。 In other words, only the persons who use the Tabular Editor 3 product will need a license.

The editions differ in two ways: **which data modeling scenarios** they support - that is, where the model you are editing may live - and **which features** are available once it is open. The two sections below cover each in turn. Anything not listed in either is available in every edition.

> [!TIP]
> Upgrading a license takes effect straight away. Activate the new key under **Help > About Tabular Editor**, and the features it unlocks are available without restarting Tabular Editor 3.

## 支持的 Data model 建模场景

The first difference between the editions is which types of tabular data modeling scenarios they support. To understand this difference, consider that Analysis Services (Tabular) exists in a number of different "flavors":

- Power BI Desktop（请确保您了解[限制](xref:desktop-limitations)）
- 通过 XMLA 终结点使用的 Power BI Premium（Premium Per User、**Premium 容量 [A、EM 或 P SKUs]**、**Fabric 容量 [F SKUs]**）
- SQL Server（2016+）Analysis Services（版本：开发人员版、标准版、**企业版**）
- Azure Analysis Services（层级：开发者层、基本层、**标准层**）

我们将 Analysis Services 中**突出显示**的这些形态视为企业级，因此只能在 Tabular Editor 3 企业版中使用。

We draw that line where Microsoft draws its own, between per-user and capacity-based licensing:

- **Premium Per User is a per-seat license.** The person editing the model is the person who paid for the seat. That matches how Business Edition is licensed: a personal, non-transferable key tied to a single user. See [Personal vs. Transferable licenses](#personal-vs-transferable-licenses).
- **Premium Capacity (P SKUs), Embedded Capacity (A/EM SKUs) and Fabric Capacity (F SKUs) are shared, organization-scale deployments.** Models hosted there are team-owned and serve many consumers, which is the scenario Enterprise Edition is built and priced for.

The same logic applies outside Power BI. Business Edition covers the SQL Server Analysis Services Developer and Standard editions along with the Azure Analysis Services Developer and Basic tiers. Those tiers serve a single developer or a small-scale deployment. SQL Server Analysis Services Enterprise Edition and Azure Analysis Services Standard tier host organization-scale models, so they require Enterprise Edition.

> [!IMPORTANT]
> Tabular Editor 仅允许编辑兼容级别为 1200 或更高的数据模型。 This is the default on any instance of Analysis Services starting from SQL Server 2016. For the same reason, Tabular Editor does not support Excel PowerPivot, as this uses an earlier Compatibility Level.

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

| 功能                                                                                                       | 桌面版                                                     | 商业版                                                     | 企业版                                                     |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| [Save with supporting files](xref:save-with-supporting-files) for Fabric                                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| [Advanced Refresh dialog](xref:advanced-refresh) and [refresh override profiles](xref:refresh-overrides) | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Automatic metadata backups on save and deploy                                                            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |

Ordinary refresh commands, and everything else in the refresh menu, are available in every edition. The three rows above are unavailable in Desktop Edition because that edition works only against a live Power BI Desktop model, with no model files of its own.

### Modeling features

| 功能                                                                  | 桌面版                                                     | 商业版                                                     | 企业版                                                     |
| ------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Perspectives in an Analysis Services model\*                        | N/A                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Tables with multiple partitions in an Analysis Services model\*     | N/A                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
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

\***注：** SQL Server 标准版 2019 之前的 Analysis Services 不支持 DirectQuery。 Nor does Azure AS Basic Tier. [Learn more](https://learn.microsoft.com/en-us/analysis-services/analysis-services-features-by-edition?view=asallproducts-allversions#tabular-models).

\*\***注意：** 在商业版中，Power BI 模型支持透视和多个分区，但模型的 `CompatibilityMode` 必须设置为 `PowerBI`。 See [Change compatibility mode](xref:change-compatibility-mode) for instructions.

Desktop Edition works only against a live Power BI Desktop model, which is why the Analysis Services rows do not apply to it.

如果您在使用 TE3 商业版许可证时尝试打开一个应用了上述一项或多项建模限制的模型，将会看到以下错误信息：

![This edition of Tabular Editor 3 does not support Enterprise-tier semantic models](~/content/assets/images/editions-01.png)

A model that acquires one of these while you are editing it is not silently mangled either: the save is refused, and the message names the feature and, for multiple partitions, the tables in question. Adding a perspective to an Analysis Services model is prevented up front - the **Perspectives** folder is not shown in the TOM Explorer and the command to create one is unavailable.

> [!IMPORTANT]
> 只有当 Power BI Report（.pbix、.pbip 或 .pbit）文件包含 Data model（Import、DirectQuery 或 Composite）时，Tabular Editor 才能在 Power BI Desktop 中作为外部工具使用。 **Reports using Live connection are not supported** since these reports do not contain a data model. [More information](xref:desktop-limitations).

## 个人许可证与可转让许可证

Our Desktop Edition and Business Edition uses a **personal** licensing model. This means, that a user receives their own personal License Key, which can not be shared or transferred to other users. When a user no longer requires the product, their subscription should be cancelled to avoid recurring payments.

Our Enterprise Edition uses a **transferable** licensing model. The license administrator receives a single License Key, which is then valid for a number of named users up to the quantity purchased. Users are identified by their e-mail address, which is entered the first time a user activates an installation of Tabular Editor 3. The first time a user activates a Tabular Editor 3 installation using the license key, they are "locked-in" to that license for 30 days. After the 30 day lock-in period, a user can be removed from the license at any time, freeing up the license slot for another user. License administrators can view and manage users through our [self-service portal](https://tabulareditor.com/my-account). You may also <a href="mailto:support@tabulareditor.com?subject=Transferable%20License%20Rotation">contact support</a> for assistance.

## 多台设备安装

每位 Tabular Editor 3 用户可根据所持许可证类型，在多台设备上安装该工具：

|                            | 桌面版 | 商业版 | 企业版 |
| -------------------------- | --- | --- | --- |
| Simultaneous installations | 1   | 2   | 3   |

> [!NOTE]
> Sharing a single license among multiple users is against our [licensing terms](https://tabulareditor.com/eula-te3).

你可以随时在工具内停用现有安装：在“帮助 > 关于 Tabular Editor”下选择“更改许可证密钥...”选项。 You can also deactivate an installation through our [self-service portal](https://tabulareditor.com/sign-in) by navigating to the "Licenses" tab.

如果您需要的 Tabular Editor 3 并发安装数量超过上述范围，请联系 [licensing@tabulareditor.com](mailto:licensing@tabulareditor.com)。

## 企业版批量折扣

我们的企业版采用分级定价，具体如下表所示（按月承诺也适用类似的折扣率）：

| Tier           | 每席年度价格                      |
| -------------- | --------------------------- |
| 前 5 个席位        | $950.00 USD |
| 接下来的 6-10 个席位  | $900.00 USD |
| 接下来的 11-20 个席位 | $850.00 USD |
| 接下来的 21-50 个席位 | $800.00 USD |
| 51 个席位及以上      | $750.00 USD |

例如，如果您需要 12 个席位，价格构成如下：

```text
Seats 1-5:    5 x 950.00 = $  4,750.00
Seats 6-10:   5 x 900.00 = $  4,500.00
Seats 11-12:  2 x 850.00 = $  1,700.00
--------------------------------------
Total                      $ 10,950.00
======================================
```

如果您需要超过 100 个席位，请 <a href="mailto:sales@tabulareditor.com">联系销售</a> 获取报价。

## Command-line and CI/CD licensing

Tabular Editor 3 is a desktop application. It has no command-line interface of its own. For automated deployments and CI/CD pipelines, use either `TabularEditor.exe` (the [Tabular Editor 2 command line](xref:command-line-options)) or the cross-platform [Tabular Editor CLI](xref:te-cli) (`te`). Both are separate from the Tabular Editor 3 desktop application.

> **Do I need a license to run CI/CD pipelines?**
> No. `TabularEditor.exe` (TE2 CLI) and the Tabular Editor CLI (`te`, during preview) do not require a Tabular Editor 3 license. Only developers using the Tabular Editor 3 desktop application need a license.

At General Availability the Tabular Editor CLI will require a license; pricing is still being finalized and will be announced ahead of GA.