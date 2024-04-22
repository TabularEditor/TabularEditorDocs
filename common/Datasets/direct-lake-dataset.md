---
uid: direct-lake-dataset
title: Direct Lake Semantic Models
author: Morten Lønskov
updated: 2023-08-14
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
  editions:
    - edition: Desktop
      none: x
    - edition: Business
      none: x
    - edition: Enterprise
---

# Direct Lake Semantic Models
Direct Lake semantic models connect directly to data sources stored in [OneLake in Fabric](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview). 

Tabular Editor 3 can create and connect to this type of dataset. For a tutorial on this please refer to our blog article: [Direct Lake semantic models: How to use them with Tabular Editor](https://blog.tabulareditor.com/2023/09/26/fabric-direct-lake-with-tabular-editor-part-2-creation/). 
Tabular Editor 3 can create direct lake semantic models with both the Lakehouse and Datawarehouse SQL Endpoint. 

Tabular Editor 2 can connect to Direct Lake semantic models, but does not have any built in functionality to create new tables or direct lake semantic models. This needs to be done manually or with a C# script. 

<div class="NOTE">
  <h5>Direct Lake limitations</h5>
  There are  several limitations to the changes that can be made to a Direct Lake dataset: <a href="https://learn.microsoft.com/en-us/power-bi/enterprise/directlake-overview#known-issues-and-limitations">Direct Lake Known Issues and Limitations</a> We recommend <a "https://www.sqlbi.com/blog/marco/2024/04/06/direct-lake-vs-import-mode-in-power-bi/"> this article by SQLBI</a> for a initial overview of choosing between Direct Lake and Import mode.
</div>

## Creating a Direct Lake model in Tabular Editor 3

Creating a Direct Lake model in Tabular Editor 3 (3.15.0 or higher) has to be specified when the model is created in the _New Model_ dialog box, by using the Direct Lake checkbox. 

![Direct Lake New Model](~/images/common/DirectLakeNewModelDialog.png)

Using the checkbox ensures that Direct Lake specific properties and annotations are set, as well as limits the import of tables to Direct Lake supported sources. 

> [!NOTE]
> Direct Lake models currently use a collation that is different from regular Power BI import semantic models. This may lead to different results when querying the model, or when referencing object names in DAX code.
 For more information please see this blog post by Kurt Buhler: [Case-sensitive models in Power BI: consequences & considerations](https://data-goblins.com/power-bi/case-specific)

## Framing New Models and Table Imports

Tabular Editor 3 (3.15.0 or higher) automatically frames (refreshes) the model on first deployment. This is to ensure that Direct Lake mode is activated - otherwise the model would automatically fall back to DirectQuery.

Additionally, on import of new tables Tabular Editor 3 (3.15.0 or higher) frames (refreshes) the model when it is saved the next time. This preference is located under **Tools > Preferences > Model Deployment > Data Refresh**.



## Identifying a Direct Lake model
The top title bar of Tabular Editor shows which type of model is open in that instance of Tabular Editor. Additionally, the TOM Explorer displays the type and mode of every table (Import, DirectQuery, Dual or Direct Lake). If a model contains a mix of table modes, the title bar will show "Hybrid". Currently, it is not possible for a DirectLake model to contain tables in Import, DirectQuery or Dual mode.
