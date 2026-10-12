---
uid: connect-ssas
title: Connect and deploy to Analysis Services
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Connect and deploy to Analysis Services

You can open a semantic model straight from a server rather than from a file, work on it, and write your changes back. This covers SQL Server Analysis Services, Azure Analysis Services, and the Power BI / Fabric XMLA endpoint.

## Opening a model from a server

Choose **File > Open > Model from DB...** (**Ctrl+Shift+O**) and enter the server address. Tabular Editor then lists the databases on that server so you can pick the one to load.

- For **SQL Server Analysis Services**, use the instance name, for example `localhost` or `myserver\tabular`.
- For **Azure Analysis Services**, use the full instance name beginning with `asazure://`.
- For the **Power BI / Fabric XMLA endpoint**, use the workspace connection string beginning with `powerbi://`.
- The **Local Instance** dropdown lists running instances of Power BI Desktop and Visual Studio integrated workspaces, so you can attach to one without knowing its port.

@xmla-as-connectivity covers the connection dialog in full, including authentication modes, advanced connection string properties, the per-connection status bar colour, and what to check when a connection fails. @load-save-model lists every way a model can be opened.

## Saving changes back

**File > Save** (**Ctrl+S**) writes your changes to the connected database. Client tools such as Excel, Power BI and DAX Studio see them immediately. Depending on what you changed, objects may need recalculating before the model can be queried again.

To take a copy of a connected model onto disk instead, use **File > Save As...** or **File > Save to Folder...**.

## Deploying to a different database

Saving updates the database you're connected to. To push the loaded model to a *different* server or database, use the deployment wizard instead, described in @deployment.

## Editing a Power BI Desktop model

Tabular Editor can attach to a running instance of Power BI Desktop through the **Local Instance** dropdown. As of the June 2025 Power BI Desktop update there are no longer any unsupported write operations, so third-party tools may freely modify the semantic model hosted in Desktop. On earlier versions some operations are restricted; see @desktop-limitations and @desktop-integration.
