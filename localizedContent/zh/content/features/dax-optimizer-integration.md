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
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# DAX优化器集成

> [!NOTE]
> Tabular Editor 3 **企业版** 用户可免费使用 DAX优化器。 [Learn more](https://blog.tabulareditor.com/2024/10/31/free-dax-optimizer-access-in-tabular-editor-3/)

Tabular Editor 3.18.0 introduces **DAX Optimizer** as an integrated experience. [DAX优化器](https://daxoptimizer.com) 是一项服务，可帮助你优化 SSAS/Azure AS 表格模型以及 Power BI/Fabric 语义模型。 The tool combines [VertiPaq Analyzer statistics](https://www.sqlbi.com/tools/vertipaq-analyzer/) with a static analysis of your DAX code, thus providing a prioritized list of recommendations, to help you quickly identify potential performance bottlenecks.

> [!IMPORTANT]
> DAX Optimizer is a paid third-party service. 要在 Tabular Editor 3 中使用 **DAX优化器** 功能，你需要拥有一个 [DAX优化器账户](https://www.daxoptimizer.com/free-tour/)。

## 视频简介

观看来自 [SQLBI](https://www.sqlbi.com) 的 Marco Russo 介绍 Tabular Editor 3 中的 DAX优化器集成：

<iframe width="640" height="360" src="https://www.youtube-nocookie.com/embed/Z5lZdI79tF8" title="Detect and Fix Issues with Tabular Editor 3 and DAX Optimizer Integration" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## 开始使用

要访问此功能，请在 **视图** 菜单中选择 **DAX优化器**。

![Dax 优化器](~/content/assets/images/features/dax-optimizer-view-menu.png)

你会看到一个新视图，类似下图：

![Dax 优化器视图](~/content/assets/images/features/dax-optimizer-view.png)

要将 Tabular Editor 3 连接到 DAX优化器服务，请在 **选项** 菜单中点击 **Connect...**。 You will be prompted to enter your Tabular Tools (DAX Optimizer) credentials.

如果你想要**断开连接**或**使用其他帐户连接**，请再次打开 **Options** 菜单，然后选择 **Reconnect...** 选项。 Cancelling the dialog will disconnect the current session.

If you want Tabular Editor 3 to automatically connect the next time the application is launched, you can check the **Connect automatically** option within the **Options** menu. 如果你的 DAX优化器帐户在多个区域都有 Workspace，也可以通过 **Options** 菜单选择要连接的区域。

最后，**Options** 菜单还支持你在[组场景](https://docs.daxoptimizer.com/how-to-guides/managing-groups)中切换到其他帐户。

## 浏览 Workspace 和模型

连接后，视图顶部的下拉列表会自动列出你现有的 Workspace、模型和模型版本。 Make your selections from left to right (i.e. choose the **Workspace** first, then the **Model**, then the **Version**). The view will display a summary of the currently selected model version, with information such as model size, number of tables, number of measures, etc.

![Model Overview](~/content/assets/images/model-overview.png)

> [!NOTE]
> Tabular Editor 3 支持上传 VPAX 文件，以便在 DAX优化器服务中创建新模型或新模型版本。 If, however, you need to create or manage workspaces, move or share models, etc. you will need to do this through the [DAX Optimizer web interface](https://app.daxoptimizer.com).

如果某个模型版本尚未分析，你会看到一个用于启动分析的选项。 Note that, depending on your account plan, you may have a limited number of "runs" available.

Once the analysis is complete, you will be presented with a summary showing the number of issues detected. The information shown is similar to what you would see in the DAX Optimizer web interface.

Go to the **Issues** or **Measures** tab to view detailed results. Use the column headers to sort and filter the results.

![Dax 优化器问题](~/content/assets/images/features/dax-optimizer-issues.png)

## 导航问题和度量值

在上述详细视图中双击某个问题或度量值后，你会跳转到 **DAX优化器结果** 视图；在那里会显示该度量值的原始 DAX 表达式，并将有问题的部分高亮标出。 The list on the left side of the screen lets you toggle which issues to highlight. Moreover, you can mark issues as **Fixed** or **Ignored** using the checkboxes within the list.

![Dax 优化器结果](~/content/assets/images/features/dax-optimizer-results.png)

在视图右上角点击 **Find in TOM Explorer...** 按钮，即可跳转到当前加载模型中对应的度量值。

勾选 **Track TOM Explorer** 复选框，使 TOM Explorer 与 **DAX优化器结果** 视图中当前选中的度量值保持同步。

当你在 **DAX优化器结果** 视图的 DAX 代码面板中点击某个度量值引用时，视图会跳转到该度量值。 You can then use the **Back** (Alt+Left) and **Forward** (Alt+Right) buttons to navigate back and forth between the measures you have visited.

## 上传模型和模型版本

要将 VPAX 统计信息上传到 DAX优化器，请确保 Tabular Editor 当前已连接到某个 Analysis Services 实例（SSAS、Azure AS、Power BI Desktop 或 Power BI/Fabric 的 XMLA endpoint）。 Then, select the workspace in the top-left dropdown on the **DAX Optimizer** view. Click on **Upload...** within the **Options** menu.

你将看到一个与下图类似的对话框：

![Upload Vpax](~/content/assets/images/upload-vpax.png)

在此，你可以选择将 VPAX 作为 Workspace 中的新模型上传，或将其作为现有模型的统计信息更新上传。

- 对于 **新模型**，你必须提供名称，并选择是否对 VPAX 进行[混淆](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/)（关于混淆的更多信息请参见下文）。 You must also choose which [contract](https://docs.daxoptimizer.com/glossary/contract) the model should be uploaded under. This impacts the number and frequency of DAX Optimizer [_runs_](https://docs.daxoptimizer.com/glossary/run) you can subsequently perform on the model.
- 对于 **新模型版本**，你必须选择要更新的现有模型。

点击 **OK** 按钮后，VPAX 文件将上传到 DAX优化器，你就可以开始分析该模型。

> [!NOTE]
> 如果在 Tabular Editor 3 中没有可用的 VertiPaq分析器统计信息，我们会在上传 VPAX 文件之前先为当前模型收集这些统计信息。 We will also automatically re-collect statistics if the last statistics collection is older than or equal to the statistics of the last VPAX file upload, for the specific model.

### Obfuscation

By default, VPAX files uploaded using Tabular Editor 3 will be obfuscated. In the **Upload Model** you may toggle obfuscation on/off for new model uploads. Subsequent model version uploads will be obfuscated or not depending on the first version upload. You can also export an obfuscated VPAX file locally without uploading to DAX Optimizer through the **VertiPaq Analyzer** view. In this case, a dictionary file is generated and stored on your local machine, next to the exported .ovpax file. This dictionary file is used to deobfuscate the contents of the .ovpax file.

当通过 **DAX优化器** 视图将已混淆的 VPAX 数据上传到 DAX优化器服务时，Tabular Editor 会自动跟踪混淆字典，并将其存储在本机的 `%LocalAppData%\TabularEditor3\DaxOptimizer` 文件夹中。 As such, when browsing models using the **DAX Optimizer** feature in Tabular Editor 3, models are automatically deobfuscated if a suitable dictionary is found in this folder, providing a more seamless experience when using obfuscation.

如果未找到字典，你可以选择手动指定一个字典文件。

![Obfuscated Model](~/content/assets/images/obfuscated-model.png)

如果未提供字典文件，你只能浏览已混淆的模型和 DAX优化器结果，这意味着你无法查看原始 DAX 表达式，也无法在 TOM Explorer 中导航到对应的度量值。

[了解有关 DAX优化器 混淆的更多信息](https://docs.daxoptimizer.com/how-to-guides/obfuscating-files)。

> [!TIP]
> 如果你想通过 DAX优化器 Web 界面浏览已混淆的模型，可以从 `%LocalAppData%\TabularEditor3\DaxOptimizer` 位置选择一个字典。 The DAX Optimizer web interface performs the deobfuscation on the client side, so your dictionary is never uploaded to the DAX Optimizer service.

### 分析模型

Once a VPAX file has been uploaded, please allow a few seconds for the file to be "verified" by the DAX Optimizer service. 验证完成后，勾选“你同意**消耗 1 次运行**来分析此模型。”复选框，然后在 **DAX优化器** 视图中点击 **分析** 按钮，即可执行一次 DAX优化器“运行”：

![Dax Optimizer 分析](~/content/assets/images/features/dax-optimizer-analyze.png)

分析所需时间取决于模型大小和度量值数量，通常需要几分钟。 Once the analysis is complete, you will be presented with a summary of the issues detected.

## 已知问题和限制

以下是 **DAX优化器** 功能的已知问题和限制，我们预计会在未来版本中解决：

- **DAX优化器** 视图不会显示任何合同剩余的“运行”次数。 As a workaround, sign in to https://app.daxoptimizer.com and click the "lightning" icon in the top-right corner, to view how many "runs" you have left per contract.