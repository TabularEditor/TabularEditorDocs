---
uid: desktop-limitations
title: Power BI Desktop limitations
author: Daniel Otykier
updated: 2021-09-10
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Power BI Desktop limitations

When using Tabular Editor (any edition) as an [external tool for Power BI Desktop](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools), there are a number of limitations to be aware about. This article provides more details on these limitations.

The limitations mentioned in this article apply to Tabular Editor 2.x as well.

## External Tool architecture

When a Power BI Desktop report (.pbix or .pbit file) contains a data model (that is, one or more tables have been added in Import or DirectQuery mode), that data model is hosted inside an instance of Analysis Services managed by Power BI Desktop. External Tools may connect to this instance of Analysis Services for different purposes.

> [!IMPORTANT]
> Power BI Desktop reports that use a **Live Connection** to SSAS, Azure AS or a dataset in a Power BI workspace do not contain a data model. As such, these reports **can not** be used with external tools such as Tabular Editor.

External tools may connect to the instance of Analysis Services managed by Power BI Desktop through a specific port number assigned by Power BI Desktop. When a tool is launched directly from the "External Tools" ribbon in Power BI Desktop, this port number is passed to the external tool as a command line argument. In Tabular Editor's case, this causes the data model to be loaded in Tabular Editor.

<img class="noscale" src="../images/external-tool-architecture.png" />

Once connected to the instance of Analysis Services, an external tool can obtain information about the model metadata, execute DAX or MDX queries against the data model, an even apply changes to the model metadata through [Microsoft-provided client libraries](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions). In this regard, the Analysis Services instance managed by Power BI Desktop is no different from any other type of Analysis Services instance.

## Data modeling operations

However, due to the way Power BI Desktop interoperates with Analysis Services, there are a few important limitations to the type of changes external tools may apply to the model metadata. These are listed [in the official documentation for External Tools](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations) and repeated here for convenience:

### Supported write operations
- Define and edit measures for calculations, including format string, KPI, and detail rows settings.
- Add calculation groups for calculation reusability in complex models.
- Create perspectives to define focused, business-domain specific views of dataset metadata.
- Apply metadata translations to support multi-language versions within a single dataset.
- Add dataset roles for row-level security (RLS) and object-level security (OLS) rules to restrict data access.

### Data modeling limitations
All Tabular Object Model (TOM) metadata can be accessed for read-only. Write operations are limited because Power BI Desktop must remain in-sync with the external modifications, therefore the following operations are not supported:

- Any TOM object types not covered in Supported write operations, such as tables and columns.
- Editing a Power BI Desktop template (PBIT) file.
- Report-level or data-level translations.
- Renaming tables and columns is not yet supported
- Sending processing commands to a dataset loaded in Power BI Desktop

> [!NOTE]
> The Analysis Services instance managed by Power BI Desktop does not enforce the allowed data modeling operations. It is up to the External Tool to ensure that no unsupported changes are made. Ignoring this may lead to unpredictable results, corrupt .pbix/.pbit report files or Power BI Desktop becoming unstable.

# Tabular Editor and Power BI Desktop

When using Tabular Editor (any edition) as an external tool for Power BI Desktop, all unsupported operations according to the list above, are disabled by default. In other words, Tabular Editor will not allow you to add or rename tables, columns, etc. on a Power BI Desktop model.

Though unsupported, it turns out that a number of operations can still be applied without causing issues. For example, setting properties such as Display Folder, Description, Summarization, etc. on individual columns using an external tool seems to work just fine at the time of writing. For this reason, Tabular Editor has an option that allows advanced users to experiment, by allowing all data modeling operations even when connected to a Power BI Desktop model. You can enable this option under **Tools > Preferences > Power BI > Allow *unsupported* modeling operations**, but make sure you understand the risks involved before doing so.

> [!NOTE]
> In Tabular Editor 2.x, this setting is available under **File > Preferences > Allow unsupported Power BI features (experimental)**

Once this feature is enabled, Tabular Editor will no longer block any modeling operation, but instead provide you full read/write access to all TOM objects and properties. While the feature is enabled, you will see a warning prompt whenever you open a Power BI Desktop model in Tabular Editor:

<img class="noscale" src="https://user-images.githubusercontent.com/8976200/133221565-6ecb7022-f69d-4964-a0bc-e068f8ed118d.png" />

> [!WARNING]
> Microsoft Support will not be able to assist you, if unsupported changes are made your .pbix file through External Tools. Our recommendation is to always keep a backup of the .pbix or .pbit file before launching any external tool that allows making changes to your data model.
