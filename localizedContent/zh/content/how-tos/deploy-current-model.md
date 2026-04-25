---
uid: deploy-current-model
title: 部署当前已加载的模型
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## 部署

如果您想将当前加载的模型部署到新数据库，或用模型更改覆盖现有数据库（例如从 Model.bim 文件加载时），请使用“模型”>“部署...”下的 Deployment Wizard。

Tabular Editor 内置 Deployment Wizard，相比从 SSDT 部署有一些优势——尤其是在部署到现有数据库时。 选择要部署到的服务器和数据库后，您可以为本次部署选择以下选项：

![Deployment Wizard](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Deployment.png)

不勾选“部署连接”复选框，就能确保目标数据库上的所有数据源保持不变。 如果模型中有一个或多个表使用了目标数据库中尚不存在的数据源，则会报错。

同样地，不勾选“部署表分区”，就能确保表上现有的分区不会被更改，从而保持分区中的数据不变。

勾选“部署角色”后，目标数据库中的角色将更新为与当前加载的模型一致；但如果未勾选“部署角色成员”，则目标数据库中各角色的成员将保持不变。