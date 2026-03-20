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
        - edition: 桌面版
          none: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# 工作区模式与增量刷新

> [!IMPORTANT]
> 这篇文章只适用于 Tabular Editor 3.4.2 及更早版本。
> 自 3.5.0 更新起，_工作区模式_ 不会覆盖通过计划刷新部署的刷新策略分区。
> 刷新策略分区也不会被序列化并纳入源代码管理。 你可以在 _'Tools > 偏好设置…… > Save-to-Folder'_. 中更改此设置。

---

![增量刷新工作区模式 Visual 摘要](~/content/assets/images/tutorials/incremental-refresh-workspace-mode.png)

---

增量刷新会在一天中的第一次计划刷新时创建新的分区。 因此，刷新后，任何本地元数据（即 `.bim` 或 `Database.json`）都会与远程模型元数据不同步。 因此，**在处理表已配置增量刷新的模型时，不建议使用 _工作区模式_**。

> [!IMPORTANT]
> 在 Tabular Editor 3 中设置增量刷新仅限于托管在 Power BI Dataset 服务中的数据集。 对于 Analysis Services，需要自定义[分区](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions)。

---

### 不建议使用工作区模式

原因在于：_工作区模式_ 会用本地元数据文件覆盖远程模型元数据；任何不同步的更改（例如对策略范围分区的更改）都会丢失。 在这些模型上使用 _工作区模式_ 时，你每天在保存更改之前，都需要对使用增量刷新的表执行 _应用刷新策略_。

![工作区模式可能会与本地元数据不同步。](~/content/assets/images/tutorials/incremental-refresh-workspace-mode-out-of-sync.png)

### 建议：基于本地元数据进行开发和部署

**相反，建议基于本地元数据文件来开发模型。** 部署更改时可以排除受刷新策略管控的分区，因此不会有覆盖 Power BI 所创建策略的风险。 可启动第二个 Tabular Editor 读取/刷新实例，并连接到远程模型用于测试。

要部署模型，请转到 _Model > Deploy..._，这将打开 Deployment Wizard。 在这里，你可以选择是否包含受增量刷新刷新策略控制的分区：

![部署分区，同时避开带有刷新策略的分区。](~/content/assets/images/tutorials/incremental-refresh-deploy-partitions.png)

部署模型时不包含这些 Policy Range 分区，可降低因元数据与远程模型之间的增量刷新分区不同步而带来的潜在影响。