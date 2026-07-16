---
uid: new-pbi-model
title: Create a Power BI Semantic Model
author: Daniel Otykier
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "Premium Per User XMLA Endpoints Only"
        - edition: Enterprise
          full: true
---
# (Tutorial) Creating your first Power BI semantic model

This page walks you through the process of creating a new Power BI semantic model from scratch using Tabular Editor 3.

> [!IMPORTANT]
> Tabular Editor 3 Business Edition is limited to [Power BI Premium Per User](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-per-user-faq). For Fabric, Power BI Premium or Embedded capacity, you must upgrade to Tabular Editor 3 Enterprise Edition. In either case, the target workspace must allow [XMLA read/write access](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#enable-xmla-read-write) - the default on all capacity SKUs since June 2025.
>
> Tabular Editor 3 Desktop Edition does not have any support for Power BI semantic models.
> 
> [More information](xref:editions).

##### Creating a new semantic model

1. From the File menu, choose New > Model... or hit `CTRL+N`

![New model](~/content/assets/images/tutorials/new-pbi-model.png)

- Provide a name for your model or use the default value. Then, set the compatibility level to "1705 (Power BI / Fabric)" (the latest Power BI / Fabric level). "1702 (Power BI / Fabric)" also remains available if you need it.
- For the best development experience, check the "Use workspace database" option. This requires that you have a development workspace available in Power BI, with XMLA read/write enabled. When you click OK, you will be prompted to enter the connection string for the Power BI workspace in which you want the workspace database created.

> [!NOTE]
> With a workspace database, you can validate Power Query (M expressions) and import table schema from Power Query expressions. You can also refresh and query data in the workspace database, making it easier to debug and test your DAX expressions.
