---
uid: using-bpa
title: 使用 Best Practice Analyzer
author: Morten Lønskov
updated: 2023-02-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Best Practice Analyzer

Best Practice Analyzer (BPA) 允许你针对模型元数据定义规则，以便在开发 Power BI 或 Analysis Services 模型时推动遵循特定约定和最佳实践。

> [!NOTE]
> Tabular Editor 3 包含一套全面的 [内置 Best Practice Analyzer 规则](xref:built-in-bpa-rules)，对新用户默认启用。

## BPA 概览

BPA 概览会显示模型中当前被违反的所有已定义规则：

![BPA Overview](~/content/assets/images/common/BPAOverview.png)

你也始终可以在主界面看到当前有多少条规则被违反。

![BPA Overview Line](~/content/assets/images/common/PBAOverviewMenuLine.png)

单击该链接（或按 F10）会打开完整的 BPA 窗口。

> [!NOTE]
> 如果你更偏好视频导览，PowerBI.tips 上有我们团队的 Daniel Otykier 讲解 Best Practice Analyzer 的详细视频：

<iframe width="640" height="360" src="https://www.youtube-nocookie.com/embed/5WnN0NG2nBk" title="PowerBI.Tips - Tutorial - Best Practice Analyzer in Tabular Editor" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### 功能

每当模型发生更改时，Best Practice Analyzer 都会在后台扫描你的模型以发现问题。 你可以在 **工具 > 偏好设置 > Best Practice Analyzer** 中禁用此功能。

在 TE2 和 TE3 中，BPA 窗口都支持将窗口停靠到桌面一侧，同时把主窗口放在另一侧，让你在处理模型时也能随时看到 BPA 问题。

Best Practice Analyzer 窗口会持续列出模型中所有 **有效规则**，以及各规则对应的违规对象。 在列表内任意位置右键单击，或使用窗口顶部的工具栏按钮，即可执行以下操作：

- **管理规则...**：这将打开“管理规则”界面，我们将在下文介绍。 你也可以通过主界面中的“工具 > 管理 BPA 规则...”菜单打开此界面。
- **转到对象...**：选择此选项，或在列表中双击某个对象，会在主界面中定位到同一对象。
- **忽略项/多项**：在列表中选择一个或多个对象并选择此选项，会向所选对象应用注释，指示 Best Practice Analyzer 之后忽略这些对象。 如果你误将某个对象设为忽略，请在屏幕顶部切换“显示已忽略”按钮。 这样你就能取消忽略之前忽略的对象。
- **忽略规则**：如果你在列表中选择了一个或多个规则，此选项会在模型级别添加注释，指示始终忽略所选规则。 同样，切换“显示已忽略”按钮也能取消忽略这些规则。
- **生成修复脚本**：对于有简易修复的规则（即只需在对象上设置单个属性即可解决问题），将启用此选项。 点击后，会把一段 C# Script 复制到你的剪贴板中。 然后，你可以将该脚本粘贴到 Tabular Editor 的 [高级脚本编写](/Advanced-Scripting) 区域中，在执行以应用修复之前先进行查看。
- **应用修复**：如上所述，这个选项同样适用于有简易修复的规则。 它不会将脚本复制到剪贴板，而是会立即执行它。

## 管理最佳实践规则

如果你需要添加、删除或修改应用于模型的规则，可以使用一个专门的界面来完成。 你可以点击 Best Practice Analyzer 窗口左上角的按钮打开它，也可以在主窗口使用菜单项“工具 > 管理 BPA 规则...”。

![BPA Manage Rules](~/content/assets/images/common/BPAOverviewManageRules.png)

“管理 BPA 规则”窗口包含两个列表：上方列表表示当前已加载的规则**集合**。 在该列表中选择一个集合后，下方列表会显示此集合中定义的所有规则。

![BPA Manage Rules UI](~/content/assets/images/common/PBAOverviewManageRulesPopUp.png)