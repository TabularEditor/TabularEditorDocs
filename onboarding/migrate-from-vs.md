---
uid: migrate-from-vs
title: Migrating from Visual Studio
author: Daniel Otykier
updated: 2021-09-30
---

# Migrating from Visual Studio / SQL Server Data Tools

This article assumes that you are familiar with Tabular model development using [Analysis Services Projects for Visual Studio](https://marketplace.visualstudio.com/items?itemName=ProBITools.MicrosoftAnalysisServicesModelingProjects) (formerly known as SQL Server Data Tools). This is common among developers using SQL Server Analysis Services (Tabular) or Azure Analysis Services.

- If you have never used Visual Studio for Tabular model development, you can safely skip this topic.
- If you previously used Tabular Editor 2.x for Tabular model development, we recommend you skip directly to the @migrate-from-te2 article.

## Partial migration

Tabular Editor 3 contains features that allow you to completely migrate away from Visual Studio for tabular model development. This is in contrast to Tabular Editor 2.x, where some users still preferred using Visual Studio for things like table import, visualization of relationships and preview of data.

However, as you familiarize yourself with Tabular Editor 3, you might still find it useful to open your tabular models in Visual Studio from time to time. This is possible at any time, since Tabular Editor 3 does not modify the **Model.bim** file format (aka. the [TOM JSON](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)) used by Visual Studio, thus ensuring compatibility with Visual Studio.

The only exception is, if you decide to use Tabular Editor's [Save-to-folder](xref:parallel-development#what-is-save-to-folder) feature, as this file format is not supported by Visual Studio. However, you can easily recreate a Model.bim file for use with Visual Studio, using the **File > Save as...** option in Tabular Editor.

> [!NOTE]
> If you often face the need to convert back and forth between Tabular Editor's folder structure file format and Visual Studio's model.bim file format, consider writing a small Windows command script using [Tabular Editor 2.x CLI](xref:command-line-options) to automate the conversion process.