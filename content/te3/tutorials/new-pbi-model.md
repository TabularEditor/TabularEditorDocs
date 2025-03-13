---
uid: new-pbi-model
title: Create a Power BI Dataset
author: Daniel Otykier
updated: 2021-09-06
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
    - edition: Enterprise
---
# (Tutorial) Creating your first Power BI dataset

This page walks you through the process of creating a new Power BI dataset from scratch using Tabular Editor 3.

> [!IMPORTANT]
> Tabular Editor 3 Business Edition is limited to [Power BI Premium Per User](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-per-user-faq). For Power BI Premium or Embedded capacity, you must upgrade to Tabular Editor 3 Enterprise Edition. In either case, the Power BI workspace in which the dataset is to be deployed, must have its [XMLA read/write endpoint enabled](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#enable-xmla-read-write).
>
> Tabular Editor 3 Desktop Edition does not have any support for Power BI datasets.
> 
> [More information](xref:editions).

##### Creating a new dataset

1. From the File menu, choose New > Model... or hit `CTRL+N`

![New model](https://user-images.githubusercontent.com/8976200/116813604-c83d5f80-ab54-11eb-8a6f-4347f26aa626.png)

- Provide a name for your model or use the default value. Then, set the compatibility level to "1560 (Power BI Dataset)".
- For the best development experience, check the "Use workspace database" option. This requires that you have a development workspace available in Power BI, with XMLA read/write enabled. When you click OK, you will be prompted to enter the connection string for the Power BI workspace in which you want the workspace database created.

> [!NOTE]
> With a workspace database, you can validate Power Query (M expressions) and import table schema from Power Query expressions. You can also refresh and query data in the workspace database, making it easier to debug and test your DAX expressions.
