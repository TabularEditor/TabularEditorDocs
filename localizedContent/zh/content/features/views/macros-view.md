---
uid: macros-view
title: 宏视图
author: Morten Lønskov
updated: 2023-03-22
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

# 宏视图

宏是 Tabular Editor 的一项强大功能，可让你自动化重复任务，或为你的模型创建自定义操作。 宏是用 C# 编写的脚本，可访问并操作 Tabular Object Model (TOM)。

你可以在 Tabular Editor 的“宏”菜单中创建、编辑、运行和管理宏。

> [!TIP]
> 你可以按以下模式在宏名称前加上前缀，将宏归类到文件夹中：`FolderName\MacroName`

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/macros-view.png" alt="Macro Window" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> Tabular Editor 中的宏窗口。 概述所有已保存的宏 </figcaption>
</figure>

> [!NOTE]
> 宏视图会列出当前保存在你的 `%localappdata%\TabularEditor3\MacroActions.json` 文件中的所有宏。

- 你可以点击视图左上角的“X”按钮删除宏。
- 你可以双击列表项来编辑宏。 这将打开一个 [C# Script 文档](xref:csharp-scripts)，其中包含宏被调用时将执行的代码。 要保存对宏的更改，点击工具栏按钮“编辑宏...”（见下方截图），或使用菜单项 **C# Script > 编辑宏...**。
- 要创建新宏，先创建一个新的 [C# Script](xref:csharp-scripts)，然后使用菜单项 **C# Script > 另存为宏...** 把它保存为宏。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/edit-macro.png" alt="Edit Macro Button" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2:</strong> 当你打开一个宏时，可以将其保存回去，方法是选择 "编辑宏……" </figcaption>
</figure>

## 后续步骤

- @creating-macros
