---
uid: incremental-refresh-workspace-mode
title: Using Workspace Mode on a Model with Incremental Refresh
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.4.2 and earlier
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Workspace mode and incremental refresh

> [!IMPORTANT]
> This article only applies to versions 3.4.2 and earlier of Tabular Editor.
> Since the 3.5.0 update, _Workspace Mode_ will not overwrite deployed Refresh Policy partitions from scheduled refreshes. 
> Refresh policy partitions will also not be serialized in source control. You can change this setting in _'Tools > Preferences... > Save-to-Folder'_.

---

![Incremental Refresh Workspace Mode Visual Abstract](~/content/assets/images/tutorials/incremental-refresh-workspace-mode.png)

---

Incremental Refresh creates new partitions upon the first scheduled refresh in a day. As a result, any local metadata (i.e. `.bim` or `database.json`) will be out-of-sync with the remote model metadata after the refresh. As a result, __when working with a model that has tables configured with Incremental Refresh, _Workspace Mode_ is not recommended__. 


> [!IMPORTANT]
> Setting up Incremental Refresh with Tabular Editor 3 is limited to dataset hosted in the Power BI Datasets service. For Analysis Services, custom [partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) is required.

---

### Workspace Mode is not Recommended
The reason is because _Workspace Mode_ will overwrite the remote model metadata with local metadata files; any out-of-sync changes (like to Policy Range partitions) will be lost. When working with _Workspace Mode_ on these models, you would need to _Apply refresh policy_ for tables using incremental refresh before saving changes every day.

  ![Workspace mode can get out of sync with local metadata.](~/content/assets/images/tutorials/incremental-refresh-workspace-mode-out-of-sync.png)

### Recommendation: Develop & Deploy from Local Metadata
__Instead, it is recommended to develop the model from the local metadata files.__ Changes can be deployed excluding partitions governed by a Refresh Policy, so there is no risk of overwriting the policies created by Power BI. A second read/refresh instance of Tabular Editor can be connected to the remote model for testing purposes.

To deploy the model, go _Model > Deploy..._ which opens the Deployment Wizard. Here you can select whether you want to include partitions governed by Incremental Refresh policies:

  ![Deploy partitions, avoiding partitions with refresh policies.](~/content/assets/images/tutorials/incremental-refresh-deploy-partitions.png)
  

By deploying the model without these Policy Range partitions, you are mitigating any potential impact due to out-of-sync incremental refresh partitions between the metadata and remote model.