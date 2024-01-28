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
Direct Lake semantic models connect directly to data sources stored in [Fabric One Lake](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview). 

Tabular Editor 3 can create and connect to this type of dataset. For a tutorial on this please refer to our blog article: [Direct Lake semantic models: How to use them with Tabular Editor](https://blog.tabulareditor.com/2023/09/26/fabric-direct-lake-with-tabular-editor-part-2-creation/). 
Tabular Editor 3 can create direct lake semantic models with both the Lakehouse and Datawarehouse SQL Endpoint. 

Tabular Editor 2 can connect to Direct Lake semantic models, but does not have any built in functionality to create new tables or direct lake semantic models. This needs to be done manually or with a C# script. 

> [!NOTE]
> DirectLake models currently use a collation that is different from regular Power BI import semantic models. This may lead to different results when querying the model, or when referencing object names in DAX code.
 For more information please see this blog post by Kurt Buhler: [Case-sensitive models in Power BI: consequences & considerations](https://data-goblins.com/power-bi/case-specific)


<div class="NOTE">
  <h5>FABRIC IN PREVIEW</h5>
  Fabric is currently in preview and there are therefore several limitations to the changes that can be made to a Direct Lake dataset: <a href="https://learn.microsoft.com/en-us/power-bi/enterprise/directlake-overview#known-issues-and-limitations">Direct Lake Known Issues and Limitations</a>
</div>

## Identifying a Direct Lake model
The top title bar of Tabular Editor shows which type of model is open in that instance of Tabular Editor. Additionally, the TOM Explorer displays the type and mode of every table (Import, DirectQuery, Dual or Direct Lake). If a model contains a mix of table modes, the title bar will show "Hybrid". Currenctly, it is not possible for a DirectLake model to contain tables in Import, DirectQuery or Dual mode.
