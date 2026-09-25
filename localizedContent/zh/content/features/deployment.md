---
uid: deployment
title: 模型部署
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 模型部署

Tabular Editor 3（商业版和企业版）可以复制当前加载的语义模型元数据，并将其部署到 Analysis Services 实例或 Power BI / Fabric 的 XMLA endpoint。

要执行部署，请通过 **Model > Deploy...** 菜单启动 **Deployment Wizard**。

> [!NOTE]
> Tabular Editor 3 商业版在支持哪些 Analysis Services 实例类型或 Power BI / Fabric Workspace 进行 XMLA 连接方面存在一些[限制](xref:editions)。 This applies to deployment as well.

## 部署选项

选择要部署到的目标服务器和数据库后，你会看到一组 **部署选项**，如下方截图所示。

![部署选项](~/content/assets/images/deployment-options.png)

These are:

- **部署模型结构**：表示将部署模型元数据。 Unchecking this prevents you from performing the deployment (the option exists for historic reasons).
- **Deploy Data Sources**: For models that use _explicit_ data sources, this option indicates whether any such data sources will be included in the deployment. Unchecking this option may be useful, if one or more properties on a data source has been modified, and you do not intend to deploy these modifications. For example, if you are deploying model metadata from a Development environment to a Test environment, you may want to retain any connection strings, etc. on the destination environment as-is. 注意：对于 Power BI / Fabric 语义模型，此选项通常不会启用，因为此类模型使用 _隐式_ 数据源：凭据由 Power BI 服务管理，连接详细信息存储在分区的 M 查询中，或存储在模型的共享表达式中。
- **Deploy Table Partitions**: This option indicates whether table partitions should be deployed. In some cases, the destination database may contain partitions that are not present in the model metadata. Unchecking this option will prevent the deployment from modifying any existing partitions on the destination server. If this option is checked, Tabular Editor will synchronize the partitions on the destination server with the model metadata. If any partitions are present on the destination server, but not in the model metadata, they will be removed (including the data contained in them).
  - **Deploy partitions governed by Incremental Refresh Policies**: When the **Deploy Table Partitions** option is enabled, you will have an option to avoid deploying partitions that are governed by Incremental Refresh Policies. This is useful when you have a model with partitions that created automatically by the [Incremental Refresh Policy](xref:incremental-refresh-about), and you want to deploy all partitions except those governed by the policy.
- **Deploy Model Roles**: This option indicates whether roles defined in the model should be deployed. Unchecking this option will retain existing roles on the model as-is. 如果你正在部署对模型中的表或列所做的更改，可能需要重新检查 [RLS 或 OLS 设置](xref:data-security-about)，以确保它们仍然有效。
  - **Deploy Model Role Members**: This option indicates whether role members should be deployed. It is common to manage role members directly on the server, rather than in the model metadata. Unchecking this option will prevent the deployment from modifying any existing role members on the destination server.

## 部署脚本

在部署过程中，Tabular Editor 会生成一个 [CreateOrReplace TMSL 脚本](https://learn.microsoft.com/en-us/analysis-services/tmsl/createorreplace-command-tmsl?view=asallproducts-allversions)，并在 Analysis Services 引擎上执行该脚本。 The CreateOrReplace script contains all the metadata required to recreate the model, including tables, columns, measures, relationships, perspectives, translations, etc. If the model does not already exist on the target server, it will be created. If the model already exists, existing objects will be replaced with the new metadata specified in the script.

如果在 **部署选项** 页面取消选择了某些选项，Tabular Editor 将在生成的 TMSL 脚本中使用这些对象的原始元数据定义，从而在服务器上按原样保留其定义。

Deployment Wizard 的最后一页允许你导出生成的脚本，这样你就能在执行前先审查这些更改。

## 部署影响

> [!WARNING]
> This type of deployment is a **metadata-only deployment**. Depending on the types of changes made to the model, imported data could be lost during deployment. In this case, you may need to execute a refresh operation once the deployment is complete.

一般来说，以下对模型的更改无需后续数据刷新：

- 添加/编辑/删除度量值和 KPI，包括它们的 DAX 表达式。
- 编辑 FormatString、Description、DisplayFolder 等属性。
- 添加/编辑/删除元数据翻译、透视、OLS 和 RLS 角色。

以下更改可能需要先执行一次 **Calculate refresh**，然后才能查询这些对象：

- 添加/编辑计算列、计算表格和计算组
- 添加/编辑关系
- 添加/编辑层次结构
- 删除列/表格

以下更改可能需要执行一次 **Full refresh**：

- 添加/编辑分区、表格和列

> [!WARNING]
> Because of the potential impact of deploying a semantic model this way, we recommend not using this option to perform a deployment against a production environment. 更好的做法是设置一条用于将模型部署到生产环境的 [CI/CD 流水线](https://blog.tabulareditor.com/category/ci-cd/)。