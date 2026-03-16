---
uid: dax-optimizer-integration
title: DAX优化器集成
author: Daniel Otykier
updated: 2024-10-30
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# DAX优化器集成

> [!NOTE]
> Tabular Editor 3 **企业版** 用户可免费使用 DAX优化器。 [了解更多](https://blog.tabulareditor.com/2024/10/31/free-dax-optimizer-access-in-tabular-editor-3/)

Tabular Editor 3.18.0 将 **DAX优化器** 作为集成式体验引入其中。 [DAX优化器](https://daxoptimizer.com) 是一项服务，可帮助你优化 SSAS/Azure AS 表格模型以及 Power BI/Fabric 语义模型。 该工具将 [VertiPaq分析器统计信息](https://www.sqlbi.com/tools/vertipaq-analyzer/) 与对你的 DAX 代码进行的静态分析相结合，从而提供一份按优先级排序的建议列表，帮助你快速定位潜在的性能瓶颈。

> [!IMPORTANT]
> DAX优化器是一项付费的第三方服务。 要在 Tabular Editor 3 中使用 **DAX优化器** 功能，你需要拥有一个 [DAX优化器账户](https://www.daxoptimizer.com/free-tour/)。

## 视频简介

观看来自 [SQLBI](https://www.sqlbi.com) 的 Marco Russo 介绍 Tabular Editor 3 中的 DAX优化器集成：

<iframe width="640" height="360" src="https://www.youtube-nocookie.com/embed/Z5lZdI79tF8" title="Detect and Fix Issues with Tabular Editor 3 and DAX Optimizer Integration" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## 开始使用

要访问此功能，请在 **视图** 菜单中选择 **DAX优化器**。

![Dax 优化器](~/content/assets/images/features/dax-optimizer-view-menu.png)

你会看到一个新视图，类似下图：

![Dax 优化器视图](~/content/assets/images/features/dax-optimizer-view.png)

要将 Tabular Editor 3 连接到 DAX优化器服务，请在 **选项** 菜单中点击 **Connect...**。 系统将提示你输入 Tabular Tools（DAX优化器）的登录凭据。

如果你想要**断开连接**或**使用其他帐户连接**，请再次打开 **Options** 菜单，然后选择 **Reconnect...** 选项。 取消该对话框将断开当前会话。

如果你希望 Tabular Editor 3 在下次启动应用时自动连接，可以在 **Options** 菜单中勾选 **Connect automatically** 选项。 如果你的 DAX优化器帐户在多个区域都有 Workspace，也可以通过 **Options** 菜单选择要连接的区域。

最后，**Options** 菜单还支持你在[组场景](https://docs.daxoptimizer.com/how-to-guides/managing-groups)中切换到其他帐户。

## 浏览 Workspace 和模型

连接后，视图顶部的下拉列表会自动列出你现有的 Workspace、模型和模型版本。 从左到右依次选择（即先选 **Workspace**，再选 **Model**，最后选 **Version**）。 该视图会显示当前所选模型版本的摘要信息，例如模型大小、表数量、度量值数量等。

![Model Overview](~/content/assets/images/model-overview.png)

> [!NOTE]
> Tabular Editor 3 支持上传 VPAX 文件，以便在 DAX优化器服务中创建新模型或新模型版本。 但如果你需要创建或管理 Workspace、移动或共享模型等，则需要通过 [DAX优化器 Web 界面](https://app.daxoptimizer.com) 来完成。

如果某个模型版本尚未分析，你会看到一个用于启动分析的选项。 注意，根据你的帐户计划，可用的“运行”次数可能有限。

分析完成后，你将看到一个摘要，其中显示检测到的问题数量。 这里显示的信息和你在 DAX优化器网页版里看到的内容类似。

转到 **Issues** 或 **度量值** 选项卡查看详细结果。 使用列标题对结果进行排序和筛选。

![Dax 优化器问题](~/content/assets/images/features/dax-optimizer-issues.png)

## 导航问题和度量值

在上述详细视图中双击某个问题或度量值后，你会跳转到 **DAX优化器结果** 视图；在那里会显示该度量值的原始 DAX 表达式，并将有问题的部分高亮标出。 屏幕左侧的列表可让你切换需要高亮显示的具体问题。 此外，你还可以使用列表中的复选框将问题标记为 **Fixed** 或 **Ignored**。

![Dax 优化器结果](~/content/assets/images/features/dax-optimizer-results.png)

在视图右上角点击 **Find in TOM Explorer...** 按钮，即可跳转到当前加载模型中对应的度量值。

勾选 **Track TOM Explorer** 复选框，使 TOM Explorer 与 **DAX优化器结果** 视图中当前选中的度量值保持同步。

当你在 **DAX优化器结果** 视图的 DAX 代码面板中点击某个度量值引用时，视图会跳转到该度量值。 然后，你可以使用 **Back** (Alt+Left) 和 **Forward** (Alt+Right) 按钮，在你访问过的度量值之间来回切换。

## 上传模型和模型版本

要将 VPAX 统计信息上传到 DAX优化器，请确保 Tabular Editor 当前已连接到某个 Analysis Services 实例（SSAS、Azure AS、Power BI Desktop 或 Power BI/Fabric 的 XMLA endpoint）。 然后，在 **DAX优化器** 视图左上角的下拉列表中选择 Workspace。 在 **Options** 菜单中点击 **Upload...**。

你将看到一个与下图类似的对话框：

![Upload Vpax](~/content/assets/images/upload-vpax.png)

在此，你可以选择将 VPAX 作为 Workspace 中的新模型上传，或将其作为现有模型的统计信息更新上传。

- 对于 **新模型**，你必须提供名称，并选择是否对 VPAX 进行[混淆](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/)（关于混淆的更多信息请参见下文）。 你还必须选择要把该模型上传到哪个[合约](https://docs.daxoptimizer.com/glossary/contract)下。 这会影响你后续在该模型上可执行的 DAX优化器 [_runs_](https://docs.daxoptimizer.com/glossary/run) 的次数和频率。
- 对于 **新模型版本**，你必须选择要更新的现有模型。

点击 **OK** 按钮后，VPAX 文件将上传到 DAX优化器，你就可以开始分析该模型。

> [!NOTE]
> 如果在 Tabular Editor 3 中没有可用的 VertiPaq分析器统计信息，我们会在上传 VPAX 文件之前先为当前模型收集这些统计信息。 对于该模型，如果上一次统计信息收集的时间早于或等于最近一次 VPAX 文件上传时所使用的统计信息时间，我们也会自动重新收集统计信息。

### 混淆

默认情况下，使用 Tabular Editor 3 上传的 VPAX 文件会进行混淆处理。 在 **Upload Model** 中，你可以在上传新模型时开启或关闭混淆。 后续的模型版本上传是否混淆，将取决于第一个版本上传时的设置。 你也可以在 **VertiPaq分析器** 视图中，将混淆后的 VPAX 文件导出到本地，而无需上传到 DAX优化器。 在这种情况下，会生成一个字典文件，并保存在本地，与导出的 .ovpax 文件位于同一目录下。 该字典文件用于对 .ovpax 文件的内容进行去混淆。

当通过 **DAX优化器** 视图将已混淆的 VPAX 数据上传到 DAX优化器服务时，Tabular Editor 会自动跟踪混淆字典，并将其存储在本机的 `%LocalAppData%\TabularEditor3\DaxOptimizer` 文件夹中。 因此，在 Tabular Editor 3 中使用 **DAX优化器** 功能浏览模型时，如果在该文件夹中找到合适的字典，模型会自动去混淆，从而在使用混淆功能时获得更顺畅的体验。

如果未找到字典，你可以选择手动指定一个字典文件。

![Obfuscated Model](~/content/assets/images/obfuscated-model.png)

如果未提供字典文件，你只能浏览已混淆的模型和 DAX优化器结果，这意味着你无法查看原始 DAX 表达式，也无法在 TOM Explorer 中导航到对应的度量值。

[了解有关 DAX优化器 混淆的更多信息](https://docs.daxoptimizer.com/how-to-guides/obfuscating-files)。

> [!TIP]
> 如果你想通过 DAX优化器 Web 界面浏览已混淆的模型，可以从 `%LocalAppData%\TabularEditor3\DaxOptimizer` 位置选择一个字典。 DAX优化器 Web 界面会在客户端执行去混淆，因此你的字典不会上传到 DAX优化器服务。

### 分析模型

VPAX 文件上传后，请稍等几秒钟，等待 DAX优化器服务对文件进行“验证”。 验证完成后，勾选“你同意**消耗 1 次运行**来分析此模型。”复选框，然后在 **DAX优化器** 视图中点击 **分析** 按钮，即可执行一次 DAX优化器“运行”：

![Dax Optimizer 分析](~/content/assets/images/features/dax-optimizer-analyze.png)

分析所需时间取决于模型大小和度量值数量，通常需要几分钟。 分析完成后，你将看到检测到的问题摘要。

## 已知问题和限制

以下是 **DAX优化器** 功能的已知问题和限制，我们预计会在未来版本中解决：

- **DAX优化器** 视图不会显示任何合同剩余的“运行”次数。 变通方法：登录 https://app.daxoptimizer.com，点击右上角的“闪电”图标，查看各合同剩余的“运行”次数。