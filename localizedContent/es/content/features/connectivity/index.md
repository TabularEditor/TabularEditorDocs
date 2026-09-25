---
uid: conectividad
title: Conectividad
author: Morten Lønskov
updated: 2026-09-21
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Conectividad

Tabular Editor 3 connects to two different kinds of thing, and they authenticate differently.

- **The model you are editing**, on Analysis Services, Azure Analysis Services or a Power BI or Fabric workspace, reached over XMLA. See @xmla-as-connectivity.
- **The data sources your model imports from**, reached through the [Table Import Wizard](xref:import-tables). That is what the pages below cover.

## Where credentials live

Credentials are stored per user and per model in the [user options](xref:user-options) file (`.tmuo`), encrypted with your Windows account key. They are not part of the model metadata and they never reach source control. See @supported-files.

This has one consequence worth knowing up front: a colleague who opens the same model supplies their own credentials, and so does the same person on a different machine.

## Legacy, structured and implicit data sources

Which authenticators you are offered also depends on how the model stores the data source, and the model decides that rather than you.

- **Legacy (provider)** data sources are available to every model, whatever its compatibility level. Credentials are stored server-side in the Tabular Object Model.
- **Structured (Power Query)** data sources are available at compatibility level 1400 and above. Credentials have to be supplied again on every deployment to Analysis Services.
- **Implicit** data sources are what Power BI and Fabric models use, and a Direct Lake model can use nothing else. There is no data source object in the metadata at all: the M expression on the partition names the source, and credentials are held by Power BI Desktop or the Power BI service rather than by the model.

Where more than one kind is available, the wizard prefers implicit, then structured, then legacy.

This is also why the source list is shorter outside Power BI. Snowflake, Databricks and Power BI dataflows are only reachable as implicit data sources, so the wizard leaves them out when the model is on Analysis Services. See [Types of TOM data sources](xref:import-tables#types-of-tom-data-sources).

Whichever kind the model ends up with, the credentials _Tabular Editor_ uses to browse the source and read its schema are the ones you type into the connection dialog, and they go in the `.tmuo` file described above. They are separate from the credentials Analysis Services or Power BI uses at refresh time.
