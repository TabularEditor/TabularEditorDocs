---
uid: powerbi-xmla
title: Power BI XMLA endpoint
author: Daniel Otykier
updated: 2021-09-10
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
      partial: Tabular Editor 3 Business Edition only allows connecting to the XMLA endpoint of Premium-Per-User (PPU) workspaces.
    - edition: Enterprise
---
# Editing a Power BI dataset through the XMLA endpoint

You can use Tabular Editor 3 to connect to a Power BI dataset published to the Power BI service through the [XMLA endpoint](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools). The XMLA endpoint is available for Power BI Premium Capacity workspaces (i.e. workspaces assigned to a Px, Ax or EMx SKU), or Power BI Premium-Per-User (PPU) workspaces.

> [!NOTE]
> Power BI Pro licenses are not sufficient for accessing Power BI datasets in a shared workspace. Premium/Embedded capacity or Premium-Per-User Power BI licensing is required for XMLA access.

## Prerequisites

Tabular Editor requires the XMLA endpoint to allow both read/write access. This setting is controlled by [your capacity admin](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#enable-xmla-read-write).

> [!IMPORTANT]
> If using Tabular Editor 3 be aware of the [license limitations](xref:editions) for connecting to the Power BI XMLA endpoint. You need at least Tabular Editor 3 Business or Enterprise Edition depending on the type of Power BI Workspace used.

## Limitations

When connecting to a dataset through the XMLA endpoint, all data modeling operations supported by the [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) are available for editing. In other words, the [Power BI Desktop Limitations](xref:desktop-limitations) do not apply when editing a dataset through the XMLA endpoint of the Power BI Service.

> [!WARNING]
> Once a change is made to a Power BI dataset through the XMLA endpoint, it will not be possible to download the dataset as a .pbix file. [More information](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#power-bi-desktop-authored-datasets).