---
uid: powerbi-xmla
title: Edición a través del punto de conexión XMLA
author: Daniel Otykier
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: Solo puntos de conexión XMLA de Premium Per User
        - edition: Enterprise
          full: true
---

# Editing a Power BI semantic model through the XMLA endpoint

You can use Tabular Editor 3 to connect to a Power BI semantic model published to the Power BI service through the [XMLA endpoint](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools). The XMLA endpoint is available for workspaces assigned to a Microsoft Fabric capacity (F SKU), a Power BI Embedded capacity (A or EM SKU), a legacy Premium capacity (P SKU) or a Premium Per User (PPU) license.

> [!NOTE]
> Power BI Pro licenses are not sufficient for accessing Power BI semantic models in a shared workspace. A Fabric capacity, Embedded capacity, legacy Premium capacity or Premium Per User license is required for XMLA access.

## Requisitos previos

Tabular Editor requires the XMLA endpoint to allow both read and write access. Microsoft enabled XMLA read/write by default on all Fabric and Power BI capacity SKUs in June 2025. If you can't connect, ask [your capacity admin](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#enable-xmla-read-write) to verify the settings described in @xmla-as-connectivity.

> [!IMPORTANT]
> Si usas Tabular Editor 3, ten en cuenta las [limitaciones de licencia](xref:editions) para conectarte al punto de conexión XMLA de Power BI. Necesitas al menos Tabular Editor 3 Business o Edición Enterprise, según el tipo de Workspace de Power BI que uses.

## Limitaciones

When connecting to a semantic model through the XMLA endpoint, all data modeling operations supported by the [Tabular Object Model (TOM)](https://learn.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) are available for editing. In other words, the [Power BI Desktop Limitations](xref:desktop-limitations) do not apply when editing a semantic model through the XMLA endpoint of the Power BI Service.

## Flujo de trabajo

El punto de conexión XMLA de Power BI, en esencia, expone una instancia de Analysis Services a la que Tabular Editor puede conectarse. As such, you can treat the Power BI workspace as the Analysis Services **server** with each Power BI semantic model in the workspace corresponding to an Analysis Services **database**. Todas las funciones de modelado y administración de Tabular Editor están disponibles al conectarse al punto de conexión XMLA. If you decide to use Tabular Editor to build and maintain your Power BI semantic models, you should also consider some kind of version control system for your model metadata.

El flujo de trabajo es el siguiente:

1. Create a new data model in Tabular Editor or connect to an existing semantic model through the Power BI XMLA endpoint
2. Guarda este modelo como un archivo **Model.bim** o usa la opción [Guardar en carpeta](xref:save-to-folder) de Tabular Editor.
3. Cada vez que quieras hacer cambios en el modelo, carga el archivo o la carpeta que guardaste en el paso 2. La primera vez que lo hagas, decide si quieres usar una [base de datos de Workspace](xref:workspace-mode) o no.
4. Once you are ready to publish your changes to the Power BI service, perform a deployment through Tabular Editor (**Model > Deploy...**), thus creating a new or overwriting an existing semantic model in a Power BI workspace.

## Pasos siguientes

- @new-pbi-model
- @workspace-mode
- @importing-tables