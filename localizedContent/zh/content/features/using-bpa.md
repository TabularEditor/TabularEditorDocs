---
uid: using-bpa
title: 使用 Best Practice Analyzer
author: Morten Lønskov
updated: 2026-09-14
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

# 最佳实践分析器

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

每当模型发生更改时，Best Practice Analyzer 都会在后台扫描你的模型以发现问题。 You can disable this feature under **Tools > Preferences > Best Practice Analyzer**.

在 TE2 和 TE3 中，BPA 窗口都支持将窗口停靠到桌面一侧，同时把主窗口放在另一侧，让你在处理模型时也能随时看到 BPA 问题。

Best Practice Analyzer 窗口会持续列出模型中所有 **有效规则**，以及各规则对应的违规对象。 Right-clicking anywhere inside the list or using the toolbar buttons at the top of the window, let's you perform the following actions:

- **Manage rules...**: This opens the Manage Rules UI, which we will cover below. 你也可以通过主界面中的“工具 > 管理 BPA 规则...”菜单打开此界面。
- **转到对象...**：选择此选项，或在列表中双击某个对象，会在主界面中定位到同一对象。
- **忽略项/多项**：在列表中选择一个或多个对象并选择此选项，会向所选对象应用注释，指示 Best Practice Analyzer 之后忽略这些对象。 If you ignored an object by mistake, toggle the "Show ignored" button at the top of the screen. This will let you unignore an object that was previously ignored.
- **忽略规则**：如果你在列表中选择了一个或多个规则，此选项会在模型级别添加注释，指示始终忽略所选规则。 Again, by toggling the "Show ignored" button, you can unignore rules as well.
- **Generate fix script**: Rules that have an easy fix (meaning the issue can be resolved simply by setting a single property on the object), will have this option enabled. By clicking, you will get a C# script copied into your clipboard. This script can then be subsequently pasted into the [Advanced Scripting](xref:advanced-scripting) area of Tabular Editor, where you can review it before executing it to apply the fix.
- **Apply fix**: This option is also available for rules than have an easy fix, as mentioned above. Instead of copying the script to the clipboard, it will be executed immediately.

## 管理最佳实践规则

If you need to add, remove or modify the rules applying to your model, there's a specific UI for that. 你可以通过点击 Best Practice Analyzer 窗口左上角的按钮打开它，也可以在主窗口中使用“Tools > Manage BPA Rules...”菜单项。

![BPA Manage Rules](~/content/assets/images/common/BPAOverviewManageRules.png)

“管理 BPA 规则”窗口包含两个列表：上方列表表示当前已加载的规则**集合**。 Selecting a collection in this list, will display all the rules that are defined within this collection in the bottom list.

The collections are:

| Collection                                  | Where its rules live                                                                                                                     | Editable                                 |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **(Effective rules)**    | Not a store of its own; the merged, deduplicated set of every rule below, which is what actually runs against your model                 | 否                                        |
| **Built-in Best Practices**                 | Shipped with Tabular Editor 3; a curated set maintained by the Tabular Editor team. See @built-in-bpa-rules | No, but individual rules can be disabled |
| One entry per **external rule file or URL** | Wherever the file or URL points                                                                                                          | Depends on the source                    |
| **Rules within the current model**          | An annotation on the model itself, so they travel with it                                                                                | 是的                                       |
| **Rules for the local user**                | `%LocalAppData%\TabularEditor3\BPARules.json`; only you see them                                                                       | 是的                                       |
| **Rules on the local machine**              | `%ProgramData%`; every user of this machine sees them                                                                                    | 是的                                       |

The built-in collection is only listed while _Enable built-in best practice rules_ is on under @preferences. Its rule IDs are reserved: defining your own rule with one of them is refused.

Use **Enable All** and **Disable All** to switch a whole collection on or off without deleting anything.

![BPA Manage Rules UI](~/content/assets/images/common/PBAOverviewManageRulesPopUp.png)