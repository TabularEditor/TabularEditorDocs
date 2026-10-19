---
uid: dax-optimizer-integration
title: DAX 优化器集成
author: Daniel Otykier
updated: 2026-10-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# DAX优化器集成

> [!NOTE]
> Tabular Editor 3 **企业版**用户可免费使用 DAX Optimizer。[了解详细信息](https://blog.tabulareditor.com/2024/10/31/free-dax-optimizer-access-in-tabular-editor-3/)

Tabular Editor 3.18.0 将**DAX Optimizer** 作为集成体验推出。[DAX Optimizer](https://daxoptimizer.com) 是一项帮助您优化 SSAS/Azure AS 表格模型和 Power BI/Fabric 语义模型 的服务。该工具将[VertiPaq 分析器统计数据](https://www.sqlbi.com/tools/vertipaq-analyzer/)与 DAX 代码的静态分析相结合，从而提供按优先级排序的建议列表，帮助您快速识别潜在的性能瓶颈。

> [!IMPORTANT]
> DAX 优化器是一项付费的第三方服务。要使用 Tabular Editor 3 中的**DAX Optimizer**功能，您需要一个[DAX Optimizer 账户](https://www.daxoptimizer.com/free-tour/)。

## 视频简介

观看来自 [SQLBI](https://www.sqlbi.com) 的 Marco Russo 介绍 Tabular Editor 3 中的 DAX Optimizer 集成：

<iframe width="640" height="360" src="https://www.youtube-nocookie.com/embed/Z5lZdI79tF8" title="使用 Tabular Editor 3 和 DAX Optimizer 集成检测并修复问题" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## 开始使用

要访问此功能，请转到**“视图”**菜单，然后选择**“DAX Optimizer”**。

![DAX Optimizer](~/content/assets/images/features/dax-optimizer-view-menu.png)

您将看到一个类似于下图的新视图：

![DAX Optimizer 视图](~/content/assets/images/features/dax-optimizer-view.png)

要将 Tabular Editor 3 连接到 DAX 优化器服务，请通过“选项”菜单单击“连接…”。系统将提示您输入 Tabular Tools（DAX 优化器）凭据。

如果您希望**断开连接**或**使用其他账户连接**，请再次转到**“选项”**菜单，然后选择**“重新连接…”**选项。取消对话框将断开当前会话。

如果你希望 Tabular Editor 3 在下次启动应用程序时自动连接，则可以在“选项”菜单中选中“自动连接”选项。如果您拥有一个在多个区域都设有工作区的 DAX Optimizer 账户，您也可以通过**选项**菜单选择要连接的区域。

最后，**“选项”**菜单还允许您在[群组场景](https://docs.daxoptimizer.com/how-to-guides/managing-groups)中切换到其他账户。

## 浏览工作区和模型

连接后，视图顶部的下拉菜单将填充您的现有工作区、模型和模型版本。请从左到右进行选择（即先选择**工作区**，然后选择**模型**，最后选择**版本**）。视图将显示当前所选模型版本的摘要，其中包含模型大小、表数、度量值数等信息。

![模型概览](~/content/assets/images/model-overview.png)

> [!NOTE]
> Tabular Editor 3 允许您上传 VPAX 文件，以便在 DAX 优化器服务中创建新模型或模型版本。但是，如果您需要创建或管理工作区、移动或共享模型等，则需要通过 [DAX优化器 Web 界面](https://app.daxoptimizer.com)进行此操作。

如果模型版本尚未分析，您将可以选择开始分析。请注意，根据您的账户套餐，您可用的“运行”次数可能有限。

分析完成后，系统将向您显示一个摘要，其中列出检测到的问题数量。显示的信息与您在 DAX 优化器 Web 界面中看到的信息类似。

转到**问题**或**度量值**选项卡，查看详细结果。使用列标题对结果进行排序和筛选。

![DAX Optimizer 问题](~/content/assets/images/features/dax-optimizer-issues.png)

## 浏览问题和度量值

当您在上图所示的详细视图中双击某个问题或度量值时，系统将带您进入**DAX 优化器结果**视图，其中显示了度量值的原始 DAX 表达式，并突出显示了有问题的地方。通过屏幕左侧的列表，您可以切换要突出显示的问题。此外，您还可以使用列表中的复选框将问题标记为**已修复**或**已忽略**。

![DAX优化器结果](~/content/assets/images/features/dax-optimizer-results.png)

点击视图右上角的**在 TOM Explorer 中查找…**按钮，导航到当前加载模型中的相应度量值。

勾选**跟踪 TOM Explorer**复选框，使 TOM Explorer 与 DAX 优化器结果视图中当前选定的度量值保持同步。

当您在**DAX优化器结果**视图中的DAX代码面板中单击Measure引用时，视图将导航到该Measure。然后，您可以使用**后退**（Alt+向左键）和**前进**（Alt+向右键）按钮在您已访问的度量值之间来回导航。

## 上传模型和模型版本

要将 VPAX 统计信息上传到 DAX优化器，请确保 Tabular Editor 当前已连接到 Analysis Services 实例（SSAS、Azure AS、Power BI Desktop 或 Power BI/Fabric XMLA endpoint）。然后，在**DAX优化器**视图的左上角下拉菜单中选择工作区。在**选项**菜单中单击**上传……**。

您将看到一个类似于下方所示的对话框：

![上传 Vpax](~/content/assets/images/upload-vpax.png)

在这里，您可以选择是将 VPAX 作为工作区中的新模型上传，还是 VPAX 包含现有模型的更新统计信息。

- 对于**新模型**，您必须提供一个名称，并选择是否应[混淆](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/) VPAX（有关混淆的更多详细信息，请参阅下文）。您还必须选择应在哪个[合同](https://docs.daxoptimizer.com/glossary/contract)下上传模型。这将影响您随后可以对模型执行的 DAX 优化器[*运行*](https://docs.daxoptimizer.com/glossary/run)的次数和频率。
- 对于**新模型版本**，你必须选择要更新的现有模型。

点击**确定**按钮后，VPAX 文件将被上传到 DAX优化器，您将能够开始分析模型。

> [!NOTE]
> 如果 Tabular Editor 3 中没有 VertiPaq 分析器统计数据，则会在上传 VPAX 文件之前收集当前模型的统计数据。如果上次收集的时间晚于或等于模型的上次 VPAX 上传时间，也会重新收集统计数据。上传的统计数据始终从模型的数据中读取。如果无法读取统计数据，则不会开始上传。

### 混淆

默认情况下，使用 Tabular Editor 3 上传的 VPAX 文件将被混淆。在**上传模型**中，您可以为新模型上传切换混淆的开/关。后续模型版本的上传将根据第一个版本的上传情况进行混淆或不进行混淆。您还可以通过**VertiPaq Analyzer**视图将混淆的 VPAX 文件导出到本地，而无需上传到 DAX 优化器。在这种情况下，系统会生成一个字典文件，并将其存储在您的本地计算机上，位于导出的 .ovpax 文件旁边。此字典文件用于对 .ovpax 文件的内容进行反混淆。

当通过**DAX优化器**视图将混淆的 VPAX 数据上传到 DAX优化器服务时，Tabular Editor 会将混淆字典存储在本地计算机的“%LocalAppData%\TabularEditor3\DaxOptimizer”文件夹中，从而自动跟踪混淆字典。因此，在使用 Tabular Editor 3 中的**DAX Optimizer**功能浏览模型时，如果在此文件夹中找到合适的字典，则会自动对模型进行反混淆处理，从而在使用混淆功能时提供更顺畅的体验。

如果未找到字典，您将可以选择手动指定字典文件。

![混淆模型](~/content/assets/images/obfuscated-model.png)

如果未提供字典文件，您将只能浏览混淆的模型和 DAX Optimizer 结果，这意味着您将无法查看原始 DAX 表达式或在 TOM Explorer 中导航到相应的度量值。

[了解有关DAX优化器混淆的更多信息](https://docs.daxoptimizer.com/how-to-guides/obfuscating-files)。

> [!TIP]
> 如果您想通过 DAX 优化器 Web 界面浏览混淆模型，可以从“%LocalAppData%\TabularEditor3\DaxOptimizer”位置指定字典。DAX优化器 Web 界面在客户端执行反混淆操作，因此您的字典绝不会上传到 DAX优化器服务。

### 分析模型

上传 VPAX 文件后，请等待几秒钟，让 DAX优化器服务“验证”该文件。验证完成后，您可以勾选“您同意**使用 1 次运行**来分析此模型。”复选框，然后点击**DAX Optimizer**视图中的**分析**按钮，执行 DAX Optimizer“运行”：

![DAX Optimizer 分析](~/content/assets/images/features/dax-optimizer-analyze.png)

分析将需要几分钟才能完成，具体取决于模型的大小和度量值的数量。分析完成后，系统将向您显示所检测到的问题的汇总。

## 已知问题和限制

以下是**DAX 优化器**功能的已知问题和限制，我们预计将在未来版本中解决这些问题：

- **DAX Optimizer** 视图不会显示任何给定合约的剩余“运行”次数。作为一种变通方法，请登录 https://app.daxoptimizer.com ，然后单击右上角的“闪电”图标，以查看每个合同的剩余“运行”次数。