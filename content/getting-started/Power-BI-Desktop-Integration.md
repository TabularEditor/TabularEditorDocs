---
uid: desktop-integration
title: Power BI Desktop Integration
author: Morten Lønskov
updated: 2026-09-23
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
# Power BI Desktop Integration

Tabular Editor runs as a [Power BI Desktop external tool](https://docs.microsoft.com/en-us/power-bi/create-reports/desktop-external-tools) and performs modeling operations on Import and DirectQuery models open in Power BI Desktop.

![Tabular Editor 3 launched from the External tools ribbon in Power BI Desktop, with a measure open in the Expression Editor](~/content/assets/images/getting-started/power-bi-desktop-integration.png)

## Prerequisites

- [Power BI Desktop](https://www.microsoft.com/en-us/download/details.aspx?id=58494) (July 2020 or newer)
- [Latest version of Tabular Editor](https://tabulareditor.com/downloads)

Also, it is highly recommended that [automatic date/time](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-auto-date-time) is turned off under **Data Load** in the Power BI Desktop options.

## External Tool architecture

When a Power BI Desktop report contains a data model (one or more tables in Import or DirectQuery mode), Power BI Desktop hosts that model in a local instance of Analysis Services. External tools connect to this instance.

> [!IMPORTANT]
> Power BI Desktop reports that use a **Live Connection** to SSAS, Azure AS or a dataset in a Power BI workspace don't contain a data model, and external tools such as Tabular Editor **can't** connect to them.

> [!IMPORTANT]
> Power BI Desktop reports that directly edit a **Direct Lake** or other Fabric model don't contain a data model. Tabular Editor opens the model from the service, as Power BI Desktop does.

Power BI Desktop assigns the Analysis Services instance a port number. When you launch a tool from the **External Tools** ribbon, Power BI Desktop passes the port number to the tool as a command-line argument, and Tabular Editor loads the data model.

<img class="noscale" src="~/content/assets/images/external-tool-architecture.png" />

A connected external tool reads the model metadata, runs DAX or MDX queries against the model and changes the model metadata through the [Microsoft-provided client libraries](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions), as with any other Analysis Services instance.

## Supported Modeling Operations

From the June 2025 Power BI Desktop update, external tools can change any part of the semantic model hosted in Power BI Desktop, including adding and removing tables and columns and changing data types. For earlier versions of Power BI Desktop, see [Desktop Limitations](xref:desktop-limitations) and [the official blog post](https://powerbi.microsoft.com/en-us/blog/open-and-edit-any-semantic-model-with-power-bi-tools/).
