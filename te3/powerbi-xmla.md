---
uid: powerbi-xmla
title: Power BI XMLA endpoint
author: Daniel Otykier
updated: 2021-10-01
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

## Workflow

The Power BI XMLA endpoint essentially exposes an instance of Analysis Services that Tabular Editor can connect to. As such, you can treat the Power BI workspace as the Analysis Services **server** with each Power BI dataset in the workspace corresponding to an Analysis Services **database**. All of Tabular Editor's modeling and management features are available when connecting to the XMLA endpoint. If you decide to use Tabular Editor to build and maintain your Power BI datasets, you should also consider some kind of version control software for your model metadata.

The workflow is then:

1. Create a new data model in Tabular Editor or connect to an existing dataset through the Power BI XMLA endpoint
2. Save this model as a **Model.bim** file or use Tabular Editor's [Save to folder](xref:save-to-folder) option.
3. Whenever you want to make changes to the model, load the file/folder you saved in step 2. The first time you do this, decide whether you want to use a [workspace database](@workspace-mode) or not.
4. Once you are ready to publish your changes to the Power BI service, perform a deployment through Tabular Editor (**Model > Deploy...**), thus creating a new or overwriting an existing dataset in a Power BI workspace.

## Next steps

- @new-pbi-model
- @workspace-mode
- @importing-tables