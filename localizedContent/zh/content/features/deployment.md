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

## 模型部署

Tabular Editor 3（商业版和企业版）可以复制当前加载的语义模型元数据，并将其部署到 Analysis Services 实例或 Power BI / Fabric 的 XMLA endpoint。

要执行部署，请通过 **Model > Deploy...** 菜单启动 **Deployment Wizard**。

> [!NOTE]
> Tabular Editor 3 商业版在支持哪些 Analysis Services 实例类型或 Power BI / Fabric Workspace 进行 XMLA 连接方面存在一些[限制](xref:editions)。 这一点同样适用于部署。

## 部署选项

选择要部署到的目标服务器和数据库后，你会看到一组 **部署选项**，如下方截图所示。

![部署选项](~/content/assets/images/deployment-options.png)

包括：

- **部署模型结构**：表示将部署模型元数据。 取消选中会导致无法执行部署（该选项出于历史原因保留）。
- **部署数据源**：对于使用 _显式_ 数据源的模型，此选项用于指定部署时是否包含这些数据源。 如果你修改了一个或多个数据源属性，但不打算部署这些修改，取消选中此选项会很有用。 例如，将模型元数据从开发环境部署到测试环境时，你可能希望目标环境上的连接字符串等保持原样。 注意：对于 Power BI / Fabric 语义模型，此选项通常不会启用，因为此类模型使用 _隐式_ 数据源：凭据由 Power BI 服务管理，连接详细信息存储在分区的 M 查询中，或存储在模型的共享表达式中。
- **部署表分区**：此选项表示是否应部署表分区。 在某些情况下，目标数据库可能包含模型元数据中不存在的分区。 取消选中此选项将阻止部署修改目标服务器上的任何现有分区。 如果勾选这个选项，Tabular Editor 将把目标服务器上的分区与模型元数据同步。 如果目标服务器上存在分区，但模型元数据中没有这些分区，它们将被删除（包括其中包含的数据）。
  - **部署受增量刷新刷新策略管控的分区**：启用 **部署表分区** 选项后，你可以选择避免部署受增量刷新刷新策略管控的分区。 当模型中包含由 [增量刷新刷新策略](xref:incremental-refresh-about) 自动创建的分区，而你希望部署除该刷新策略管控的分区之外的所有分区时，这个选项就很有用。
- **部署模型角色**：这个选项用来决定是否部署模型中定义的角色。 取消勾选这个选项将按原样保留模型中现有的角色。 如果你正在部署对模型中的表或列所做的更改，可能需要重新检查 [RLS 或 OLS 设置](xref:data-security-about)，以确保它们仍然有效。
  - **部署模型角色成员**：这个选项用来决定是否部署角色成员。 通常会直接在服务器上管理角色成员，而不是在模型元数据中管理。 取消勾选这个选项将阻止部署修改目标服务器上的任何现有角色成员。

## 部署脚本

在部署过程中，Tabular Editor 会生成一个 [CreateOrReplace TMSL 脚本](https://learn.microsoft.com/en-us/analysis-services/tmsl/createorreplace-command-tmsl?view=asallproducts-allversions)，并在 Analysis Services 引擎上执行该脚本。 CreateOrReplace 脚本包含重新创建模型所需的全部元数据，包括表、列、度量值、关系、透视、翻译等。 如果目标服务器上尚不存在该模型，将创建该模型。 如果模型已存在，则现有对象将被脚本中指定的新元数据替换。

如果在 **部署选项** 页面取消选择了某些选项，Tabular Editor 将在生成的 TMSL 脚本中使用这些对象的原始元数据定义，从而在服务器上按原样保留其定义。

Deployment Wizard 的最后一页允许你导出生成的脚本，这样你就能在执行前先审查这些更改。

## 部署影响

> [!WARNING]
> 这种部署属于 **仅元数据部署**。 根据对模型所做更改的类型，部署期间可能会丢失已导入的数据。 在这种情况下，你可能需要在部署完成后执行一次刷新操作。

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
> 鉴于以这种方式部署语义模型可能带来的影响，我们建议不要使用此选项将其部署到生产环境。 更好的做法是设置一条用于将模型部署到生产环境的 [CI/CD 流水线](https://blog.tabulareditor.com/category/ci-cd/)。