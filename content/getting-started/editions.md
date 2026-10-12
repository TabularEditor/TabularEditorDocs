---
uid: editions
title: Compare editions
author: Søren Toft Joensen
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---
# Tabular Editor 3 Editions

This document provides an overview and comparison of the different editions of Tabular Editor 3.

> [!NOTE]
> Tabular Editor 3 licenses are **per developer**. In other words, only the persons who use the Tabular Editor 3 product will need a license.

The editions differ in two ways: **which data modeling scenarios** they support - that is, where the model you are editing may live - and **which features** are available once it is open. The two sections below cover each in turn. Anything not listed in either is available in every edition.

> [!TIP]
> Upgrading a license takes effect straight away. Activate the new key under **Help > About Tabular Editor**, and the features it unlocks are available without restarting Tabular Editor 3.

## Supported Data Modeling Scenarios

The first difference between the editions is which types of tabular data modeling scenarios they support. To understand this difference, consider that Analysis Services (Tabular) exists in a number of different "flavors":

- Power BI Desktop (make sure you understand the [limitations](xref:desktop-limitations))
- Power BI Premium through the XMLA Endpoint (Premium Per User, **Premium Capacity [A, EM or P SKUs]**, **Fabric Capacity [F SKUs]**)
- SQL Server (2016+) Analysis Services (Editions: Developer, Standard, **Enterprise**)
- Azure Analysis Services (Tiers: Developer, Basic, **Standard**)

We consider the **highlighted** flavors of Analysis Services to be Enterprise-Tier, and as such, these may only be used with Tabular Editor 3 Enterprise Edition.

We draw that line where Microsoft draws its own, between per-user and capacity-based licensing:

- **Premium Per User is a per-seat license.** The person editing the model is the person who paid for the seat. That matches how Business Edition is licensed: a personal, non-transferable key tied to a single user. See [Personal vs. Transferable licenses](#personal-vs-transferable-licenses).
- **Premium Capacity (P SKUs), Embedded Capacity (A/EM SKUs) and Fabric Capacity (F SKUs) are shared, organization-scale deployments.** Models hosted there are team-owned and serve many consumers, which is the scenario Enterprise Edition is built and priced for.

The same logic applies outside Power BI. Business Edition covers the SQL Server Analysis Services Developer and Standard editions along with the Azure Analysis Services Developer and Basic tiers. Those tiers serve a single developer or a small-scale deployment. SQL Server Analysis Services Enterprise Edition and Azure Analysis Services Standard tier host organization-scale models, so they require Enterprise Edition.

> [!IMPORTANT]
> Tabular Editor only allows editing data models using Compatibility Level 1200 or higher. This is the default on any instance of Analysis Services starting from SQL Server 2016. For the same reason, Tabular Editor does not support Excel PowerPivot, as this uses an earlier Compatibility Level.

Please refer to the matrix below for the full overview of supported scenarios:

|Scenario / Edition|Desktop|Business|Enterprise|
|---|---|---|---|
|External Tool for Power BI Desktop|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Load/save model metadata to disk\*\*|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>\*|<span class="emoji">&#10004;</span>|
|Workspace Mode\*\*\*|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>\*|<span class="emoji">&#10004;</span>|
|Power BI Premium Per User|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|SQL Server Developer Edition|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>\*|<span class="emoji">&#10004;</span>|
|SQL Server Standard Edition|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|SQL Server Enterprise Edition|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Azure AS Developer Tier|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>\*|<span class="emoji">&#10004;</span>|
|Azure AS Basic Tier|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Azure AS Standard Tier|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Power BI Premium Capacity (P SKUs)|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Power BI Embedded Capacity (A/EM SKUs)|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Fabric Capacity (F SKUs)|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|

\***Note:** Enterprise Edition is required if the Analysis Services data model contains perspectives or tables with multiple partitions (does not apply to Power BI Desktop or Power BI Premium Per User models).

\*\***Note:** Supported file formats are: **.pbip** (Power BI Project) **.pbit** (Power BI Template), **.bim** (Analysis Services model metadata), **.vpax** (VertiPaq Analyzer) and **database.json** (Tabular Editor folder structure), **TMDL** (Tabular Model Definition Language).

\*\*\***Note:** Workspace Mode allows Tabular Editor 3 to simultaneously save model metadata to disk and synchronize a database on any of the editions of Analysis Services or Power BI supported by the Tabular Editor 3 edition purchased.

## Feature availability

Beyond the scenarios above, these are the features whose availability depends on the edition. Trial and Consultancy licenses carry the Enterprise Edition feature set.

### Editing and refreshing

|Feature|Desktop|Business|Enterprise|
|---|---|---|---|
|[Save with supporting files](xref:save-with-supporting-files) for Fabric|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|[Advanced Refresh dialog](xref:advanced-refresh) and [refresh override profiles](xref:refresh-overrides)|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Automatic metadata backups on save and deploy|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|

Ordinary refresh commands, and everything else in the refresh menu, are available in every edition. The three rows above are unavailable in Desktop Edition because that edition works only against a live Power BI Desktop model, with no model files of its own.

### Modeling features

|Feature|Desktop|Business|Enterprise|
|---|---|---|---|
|Perspectives in an Analysis Services model\*|N/A|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Tables with multiple partitions in an Analysis Services model\*|N/A|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Perspectives and multiple partitions in a Power BI model|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Direct Lake tables|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|[Semantic Bridge](xref:semantic-bridge) for Databricks Metric Views|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|

\***Note:** Desktop Edition cannot open Analysis Services models at all, which is why these two rows do not apply to it. See [Modeling Restrictions](#modeling-restrictions) below for what happens when a model uses one of these features on an edition that does not allow it.

The Semantic Bridge row covers the **Import from Metric View YAML...** command and the `SemanticBridge` object in [C# scripts](xref:csharp-scripts); on a lower edition the menu item is not shown, and a script that reaches for the service reports that it is unavailable at your license level.

### AI Assistant, MCP server and administrator policies

The [AI Assistant](xref:ai-assistant) and the [MCP server](xref:mcp-server) themselves are available in every edition. What Enterprise Edition adds is the ability to govern them centrally, and a record of what they did.

|Feature|Desktop|Business|Enterprise|
|---|---|---|---|
|AI Assistant and MCP server|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|General administrator [policies](xref:policies), such as turning off updates, telemetry, scripts, macros or AI entirely|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Capping what the AI Assistant and the MCP server may reach, per resource|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Locking the AI provider, endpoint, model, organization and project, or restricting them to an allowlist|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Publishing Custom Instructions for the organization, and ruling out the ones a user keeps|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Withholding individual MCP tools, and fixing the MCP server port|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Allowing only C# scripts and macros that stay within the model (`BlockUnsafeScripts`)|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|A local audit record of AI Assistant and MCP server activity|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|

> [!IMPORTANT]
> The Enterprise policies are never quietly ignored on an edition that is not licensed for them. If any of their values is set on a machine running Desktop or Business Edition, the AI Assistant and the MCP server refuse to start and name the values that require Enterprise Edition, and a `BlockUnsafeScripts` value stops every script and macro from running until an Enterprise license is activated. Roll them out against the licenses you actually have. See @policies.

### Licensing and support

|Feature|Desktop|Business|Enterprise|
|---|---|---|---|
|[Free DAX Optimizer access](xref:dax-optimizer-integration)|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|**Help > Dedicated Support** for contacting our support team directly|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Simultaneous installations per user|1|2|3|

The DAX Optimizer *integration* itself is in every edition; what Enterprise Edition adds is eligibility for a redemption code that gives you DAX Optimizer access at no extra cost.

### Available in every edition

Everything else is the same whichever edition you hold, including the DAX editor and IntelliSense-like [code assist](xref:code-actions), [DAX queries](xref:dax-query) and the [DAX debugger](xref:dax-debugger), [DAX scripts](xref:dax-scripts) and [user-defined functions](xref:udfs), [C# scripts](xref:csharp-scripts) and [macros](xref:macros), the [Best Practice Analyzer](xref:using-bpa) with its [built-in rules](xref:built-in-bpa-rules), the [Perspective Editor](xref:perspective-editor), the [Metadata Translation Editor](xref:metadata-translation-editor), the [Calendar Editor](xref:calendars), [table groups](xref:table-groups), [diagrams](xref:diagram-view), [data preview](xref:table-preview) and [pivot grids](xref:pivot-grid), the VertiPaq Analyzer integration, the [DAX Package Manager](xref:dax-package-manager), the [Table Import Wizard](xref:import-tables) and [unsaved change indicators](xref:unsaved-changes).

## Modeling Restrictions

We restrict a few data modeling operations inside Tabular Editor 3 as well, corresponding to the restrictions on certain Microsoft service tiers (Azure Analysis Services *Basic Tier*, SQL Server Analysis Services *Standard Edition*, and Power BI *Premium-Per-User*).

Specifically, [Azure AS Basic Tier and SQL Server Standard Edition do not support perspectives or multiple partitions](https://azure.microsoft.com/en-us/pricing/details/analysis-services/), and as such, SSAS/Azure AS models using these features require TE3 Enterprise Edition. DirectQuery is not restricted by your Tabular Editor 3 edition at all: whether you can use it depends on the server the model is hosted on.

Similarly, [Power BI Premium-Per-User workspaces do not support Direct Lake datasets](https://learn.microsoft.com/en-us/power-bi/enterprise/directlake-overview#prerequisites), which is why Power BI models using this feature also requires TE3 Enterprise Edition.

|Model type|Feature|Desktop|Business|Enterprise|
|---|---|---|---|---|
|Azure AS / SSAS|Perspectives|N/A|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Azure AS / SSAS|Multiple partitions|N/A|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Azure AS / SSAS|DirectQuery*|N/A|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Azure AS / SSAS|Direct Lake|N/A|N/A|N/A|
|Power BI|Perspectives**|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Power BI|Multiple partitions**|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Power BI|DirectQuery|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Power BI|Direct Lake|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|

\***Note:** Analysis Services on SQL Server Standard Edition pre-2019 does not support DirectQuery. Nor does Azure AS Basic Tier. [Learn more](https://learn.microsoft.com/en-us/analysis-services/analysis-services-features-by-edition?view=asallproducts-allversions#tabular-models).

\*\***Note:** Perspectives and multiple partitions are available in Business Edition for Power BI models, but the model's `CompatibilityMode` must be set to `PowerBI`. See [Change compatibility mode](xref:change-compatibility-mode) for instructions.

Desktop Edition works only against a live Power BI Desktop model, which is why the Analysis Services rows do not apply to it.

If you attempt to open a model that uses one or more of the modeling restrictions listed above, while on a TE3 Business Edition license, you will see the error message below:

![This edition of Tabular Editor 3 does not support Enterprise-tier semantic models](~/content/assets/images/editions-01.png)

A model that acquires one of these while you are editing it is not silently mangled either: the save is refused, and the message names the feature and, for multiple partitions, the tables in question. Adding a perspective to an Analysis Services model is prevented up front - the **Perspectives** folder is not shown in the TOM Explorer and the command to create one is unavailable.

> [!IMPORTANT]
> Tabular Editor can only be used as an external tool for Power BI Desktop when the Power BI report (.pbix, .pbip or .pbit) file contains a data model (Import, DirectQuery or Composite). **Reports using Live connection are not supported** since these reports do not contain a data model. [More information](xref:desktop-limitations).

## Personal vs. Transferable licenses

Our Desktop Edition and Business Edition uses a **personal** licensing model. This means, that a user receives their own personal License Key, which can not be shared or transferred to other users. When a user no longer requires the product, their subscription should be cancelled to avoid recurring payments.

Our Enterprise Edition uses a **transferable** licensing model. The license administrator receives a single License Key, which is then valid for a number of named users up to the quantity purchased. Users are identified by their e-mail address, which is entered the first time a user activates an installation of Tabular Editor 3. The first time a user activates a Tabular Editor 3 installation using the license key, they are "locked-in" to that license for 30 days. After the 30 day lock-in period, a user can be removed from the license at any time, freeing up the license slot for another user. License administrators can view and manage users through our [self-service portal](https://tabulareditor.com/my-account). You may also <a href="mailto:support@tabulareditor.com?subject=Transferable%20License%20Rotation">contact support</a> for assistance.

## Multiple installations

Each Tabular Editor 3 user is allowed to install the tool on multiple machines depending on the type of license held:

| |Desktop|Business|Enterprise|
|---|---|---|---|
|Simultaneous installations|1|2|3|

> [!NOTE]
> Sharing a single license among multiple users is against our [licensing terms](https://tabulareditor.com/eula-te3).

You can deactivate an existing installation at any time from within the tool itself, by choosing the "Change license key..." option under "Help > About Tabular Editor". You can also deactivate an installation through our [self-service portal](https://tabulareditor.com/sign-in) by navigating to the "Licenses" tab.

If you need more simultaneous installations of Tabular Editor 3 than listed above, please contact [licensing@tabulareditor.com](mailto:licensing@tabulareditor.com).

## Enterprise Edition Volume Discounts

If you require more than 25 seats, please <a href="mailto:sales@tabulareditor.com">contact sales</a> for a quote.


## Command-line and CI/CD licensing

Tabular Editor 3 is a desktop application. It has no command-line interface of its own. For automated deployments and CI/CD pipelines, use either `TabularEditor.exe` (the [Tabular Editor 2 command line](xref:command-line-options)) or the cross-platform [Tabular Editor CLI](xref:te-cli) (`te`). Both are separate from the Tabular Editor 3 desktop application.

> **Do I need a license to run CI/CD pipelines?**
> No. `TabularEditor.exe` (TE2 CLI) and the Tabular Editor CLI (`te`, during preview) do not require a Tabular Editor 3 license. Only developers using the Tabular Editor 3 desktop application need a license.

At General Availability the Tabular Editor CLI will require a license; pricing is still being finalized and will be announced ahead of GA.
