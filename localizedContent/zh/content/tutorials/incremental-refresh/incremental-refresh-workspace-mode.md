---
uid: incremental-refresh-workspace-mode
title: 在启用了增量刷新的模型中使用工作区模式
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.4.2 及更早版本
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 工作区模式与增量刷新

> [!IMPORTANT]
> This article only applies to versions 3.4.2 and earlier of Tabular Editor.
> Since the 3.5.0 update, _Workspace Mode_ will not overwrite deployed Refresh Policy partitions from scheduled refreshes.
> Refresh policy partitions will also not be serialized in source control. You can change this setting in _'Tools > Preferences... > Save-to-Folder'_.

---

![增量刷新工作区模式 Visual 摘要](~/content/assets/images/tutorials/incremental-refresh-workspace-mode.png)

---

Incremental Refresh creates new partitions upon the first scheduled refresh in a day. As a result, any local metadata (i.e. `.bim` or `database.json`) will be out-of-sync with the remote model metadata after the refresh. As a result, **when working with a model that has tables configured with Incremental Refresh, _Workspace Mode_ is not recommended**.

> [!IMPORTANT]
> 在 Tabular Editor 3 中设置增量刷新仅限于托管在 Power BI Dataset 服务中的数据集。 For Analysis Services, custom [partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) is required.

---

### 不建议使用工作区模式

原因在于：_工作区模式_ 会用本地元数据文件覆盖远程模型元数据；任何不同步的更改（例如对策略范围分区的更改）都会丢失。 When working with _Workspace Mode_ on these models, you would need to _Apply refresh policy_ for tables using incremental refresh before saving changes every day.

![工作区模式可能会与本地元数据不同步。](~/content/assets/images/tutorials/incremental-refresh-workspace-mode-out-of-sync.png)

### 建议：基于本地元数据进行开发和部署

**相反，建议基于本地元数据文件来开发模型。** 部署更改时可以排除受刷新策略管控的分区，因此不会有覆盖 Power BI 所创建策略的风险。 A second read/refresh instance of Tabular Editor can be connected to the remote model for testing purposes.

要部署模型，请转到 _Model > Deploy..._，这将打开 Deployment Wizard。 Here you can select whether you want to include partitions governed by Incremental Refresh policies:

![部署分区，同时避开带有刷新策略的分区。](~/content/assets/images/tutorials/incremental-refresh-deploy-partitions.png)

部署模型时不包含这些 Policy Range 分区，可降低因元数据与远程模型之间的增量刷新分区不同步而带来的潜在影响。