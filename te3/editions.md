---
uid: editions
title: Compare editions
author: Søren Toft Joensen
updated: 2021-09-09
---
# Tabular Editor 3 Editions

This document provides an overview and comparison of the different editions of Tabular Editor 3.

## Supported Data Modeling Scenarios

The main difference between the various editions of Tabular Editor 3, is which types of tabular data modeling scenarios they support. To understand this difference, consider that Analysis Services (Tabular) exists in a number of different "flavors":

- Power BI Desktop (make sure you you understand the [limitations](xref:desktop-limitations))
- Power BI Premium through the XMLA Endpoint (Premium Per User or **Premium Capacity [A, EM or P SKUs]**)
- SQL Server (2016+) Analysis Services (Editions: Developer, Standard, **Enterprise**)
- Azure Analysis Services (Tiers: Developer, Basic, **Standard**)

> [!IMPORTANT]
> Tabular Editor only allows editing data models using Compatibility Level 1200 or higher. This is the default on any instance of Analysis Services starting from SQL Server 2016.

We consider the **highlighted** flavors of Analysis Services to be Enterprise-Tier, and as such, these may only be used with Tabular Editor 3 Enterprise Edition. Please refer to the matrix below for the full overview of supported scenarios:

|Scenario / Edition|Desktop|Business|Enterprise
|---|---|---|---|
|External Tool for Power BI Desktop|<span class="emoji"><span class="emoji">&#10004;</span></span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Load/save model metadata to disk**|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>*|<span class="emoji">&#10004;</span>|
|Workspace Mode***|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>*|<span class="emoji">&#10004;</span>|
|Power BI Premium Per User|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|SQL Server Developer Edition|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>*|<span class="emoji">&#10004;</span>|
|SQL Server Standard Edition|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|SQL Server Enterprise Edition|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Azure AS Developer Tier|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>*|<span class="emoji">&#10004;</span>|
|Azure AS Basic Tier|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Azure AS Standard Tier|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Power BI Premium Capacity (P SKUs)|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Power BI Embedded Capacity (A/EM SKUs)|<span class="emoji">&#10060;</span>|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|

\***Note:** Enterprise Edition is required if the Analysis Services data model contains perspectives or tables with multiple partitions (does not apply to Power BI Desktop or Power BI Premium Per User models).

\*\***Note:** Supported file formats are: **.pbit** (Power BI Template), **.bim** (Analysis Services model metadata), **.vpax** (VertiPaq Analyzer) and **database.json** (Tabular Editor folder structure).

\*\*\***Note:** Workspace Mode allows Tabular Editor 3 to simultaneously save model metadata to disk and synchronize a database on any of the editions of Analysis Services or Power BI supported by the Tabular Editor 3 edition purchased.

## Modeling Restrictions for non-Power BI models

Specifically for Analysis Services (not Power BI) data models, we restrict a few data modeling operations inside Tabular Editor 3 as well, corresponding to the restrictions on Azure Analysis Services Basic Tier and SQL Server Analysis Services Standard Edition:

|modeling Feature / Edition|Business|Enterprise
|---|---|---|
|Perspectives|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|
|Multiple partitions|<span class="emoji">&#10060;</span>|<span class="emoji">&#10004;</span>|

There are no other feature differences between the Tabular Editor 3 editions, than the ones listed above. 

## Modeling Restrictions for Power BI models

There are no feature differences across the Tabular Editor 3 editions for Power BI data models.

> [!NOTE]
> Please keep in mind that Power BI Desktop [currently does not support all Data modeling operations](xref:desktop-limitations). For this reason, Tabular Editor 3 by default blocks operations that are not supported by Power BI Desktop. However, this restriction can be removed under Tools > Preferences > Power BI.

> [!IMPORTANT]
> Tabular Editor can only be used as an external tool for Power BI Desktop when the Power BI report (.pbix or .pbit) file contains a data model (Import, DirectQuery or Composite). **Reports using Live connection are not supported** since these reports do not contain a data model. [More information](xref:desktop-limitations).

## Personal vs. Transferable licenses

Our Desktop Edition and Business Edition uses a personal licensing model. This means, that a user receives their own personal License Key, which can not be shared or transferred to other users. When a user no longer requires the product, their subscription should be cancelled to avoid recurring payments.

Our Enterprise Edition uses a transferable licensing model. The license administrator receives a single License Key, which is then valid for a number of named users up to the quantity purchased. Users are identified by their e-mail address, which is entered the first time a user activates an installation of Tabular Editor 3. The license administrator may <a href="mailto:support@tabulareditor.com?subject=Transferable%20License%20Rotation">contact support</a> in case a user should be removed from the license, such as when an employee leaves the team.

## Number of installations per user

The table below lists the number of installations that can be active at a time, for any given user, using the specified type of license:

| |Desktop|Business|Enterprise|
|---|---|---|---|
|Installations|1|1|3|

You can deactivate an existing installation at any time from within the tool itself, by choosing the "Change license key..." option under "Help > About Tabular Editor". You may also <a href="mailto:support@tabulareditor.com?subject=Deactivation">contact support</a> if you need our assistance in deactivating an installation.

## Enterprise Edition Volume Discounts

Our Enterprise Edition is priced in tiers, according to the following table (similar discount rates apply to monthly commitment):

|Tier|Yearly price per seat|
|---|---|
|First 5 seats|$950.00 USD|
|Next 6-10 seats|$900.00 USD|
|Next 11-20 seats|$850.00 USD|
|Next 21-50 seats|$800.00 USD|
|Seats 51 and above|$750.00 USD|

As an example, if you need 12 seats, the price breaks down as follow:

```text
Seats 1-5:    5 x 950.00 = $  4,750.00
Seats 6-10:   5 x 900.00 = $  4,500.00
Seats 11-12:  2 x 850.00 = $  1,700.00
--------------------------------------
Total                      $ 10,950.00
======================================
```

If you require more than 100 seats, please <a href="mailto:sales@tabulareditor.com">contact sales</a> for a quote.
