---
uid: connectivity
title: Connectivity
author: Morten Lønskov
updated: 2026-09-23
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

# Connectivity

Tabular Editor 3 authenticates each of these connections separately:

- **The semantic model you edit**, on SQL Server Analysis Services, Azure Analysis Services or a Power BI or Fabric workspace, over XMLA. See @xmla-as-connectivity and @connect-ssas.
- **The data sources the model imports from**, through the [Table Import Wizard](xref:import-tables). The pages in this section cover these connections.

## Data sources

Each source has its own connection dialog:

- @connect-sql-server: SQL Server, Azure SQL Database, Azure SQL Managed Instance and Azure Synapse Analytics
- @connect-snowflake: Snowflake, including key pair authentication
- @connect-databricks: Azure Databricks and Databricks on other clouds
- @connect-oracle: Oracle databases through the Oracle OLE DB provider
- @connect-odbc: any source with an ODBC driver, including PostgreSQL, MySQL, MariaDB and IBM Db2
- @connect-oledb: any source with an OLE DB provider
- @connect-onelake: Fabric Lakehouse, Warehouse, SQL database and mirrored database items
- @connect-dataflows: Power BI dataflows

## Where credentials are stored

Tabular Editor saves the connection settings and credentials you enter in a connection dialog in the [user options](xref:user-options) file (`.tmuo`). This file is per user and per model, and the credentials in it are encrypted with the Windows Data Protection API under your Windows user account. See @supported-files.

- The credentials aren't part of the model metadata and aren't committed to source control.
- Each user supplies their own credentials, on each machine.
- Generated M expressions contain no credentials.

## What the credentials are used for

Tabular Editor uses the credentials from the connection dialog to connect to the source when you import tables, preview data and update table schema. If the authentication option has no interactive sign-in, Tabular Editor connects with the saved credentials without prompting.

Data refreshes in Analysis Services and Power BI use the credentials configured for the data source in the model, on the server or in the Power BI service. You set the credentials Analysis Services uses in the data source properties after you import the tables (see [Creating a new data source](xref:import-tables#creating-a-new-data-source)).

## Legacy, structured and implicit data sources

The data source types available in the wizard depend on the model:

- **Legacy (provider)** data sources are available to every model except Direct Lake models. Credentials are managed in the provider data source object in the Tabular Object Model (TOM) and are stored and encrypted server-side.
- **Structured (Power Query)** data sources are available at compatibility level 1400 and above. You supply credentials again each time you deploy to Analysis Services.
- **Implicit** data sources are available to Power BI and Fabric models. Direct Lake models use only implicit data sources. With an implicit data source, the model has no data source object: import partitions carry an M expression that names the source, Direct Lake partitions reference a shared expression, and Power BI Desktop or the Power BI service holds the credentials.

When the model has no data sources, the wizard preselects implicit if it's available, then structured, then legacy.

Snowflake, Databricks and Power BI dataflows are available only as implicit data sources. The wizard hides them for models that don't support implicit data sources, such as Analysis Services models (see [Types of TOM data sources](xref:import-tables#types-of-tom-data-sources)).
