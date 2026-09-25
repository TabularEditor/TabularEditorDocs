---
uid: macros
title: 创建宏
author: Morten Lønskov
updated: 2026-09-22
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

# （教程）创建宏

宏是保存在 Tabular Editor 中的 C# Script，可以在不同语义模型之间轻松复用。
Saving a script as a  Macro will allow that macro to be used when right clicking on the objects in the TOM Explorer making it simple to apply the script to your model.

## 创建宏

创建宏的第一步是编写并测试一个 C# Script。

> [!TIP]
> 开始使用 C# 脚本编写的一个简单方法是使用内置的录制功能，它可以录制你在 TOM Explorer 中执行的操作。
> his way you can see how to interact with the different model objects and create reusable scripts.
> nother way is to reuse existing scripts such as those in our [script library](xref:csharp-script-library).
> n this tutorial we use the script [Format Numeric Measures](xref:script-format-numeric-measures) to showcase the Macro functionality.

当脚本按要求运行后，可以使用工具栏按钮“保存为宏”保存脚本，这会打开“保存宏”窗口。

![宏创建信息框](~/content/assets/images/features/macros/macro_tutorial_create_infobox.png)

“保存宏”窗口提供三个选项：

1. 宏名称：为宏命名，并使用反斜杠 "\" 为宏创建文件夹路径（见下文）
2. 为宏添加工具提示，方便记住其具体用途
3. 选择宏应可用的上下文。

![宏保存提示框](~/content/assets/images/features/macros/macro_tutorial_save_window.png)

在上面的示例中，宏将保存在名为 Formatting\Beginner 的文件夹中，脚本名为 "Format Numeric Measures"。 It will be saved in the context of measures.

### 宏上下文

宏会保存在一个“有效上下文”中，该上下文决定脚本可以应用到模型中的哪些对象。

然后，您可以在 TOM Explorer 中右键单击度量值时使用此宏。 The context given while saving the Macro determines which objects will show the Macro when right clicking on that object.

Tabular Editor 会根据正在保存的脚本建议一个上下文。

![宏菜单快捷方式](~/content/assets/images/features/macros/macro_tutorial_menu_shortcut.png)

## 编辑宏

在“宏”窗格中双击该宏即可打开；编辑 C# Script 后，可使用 _Ctrl + S_ 或单击“编辑宏”按钮保存。

![宏编辑信息框](~/content/assets/images/features/macros/macro_tutorial_edit_infobox.png)

## Administrator policies

Macros can be governed centrally, through the registry policies an IT department deploys. `DisableMacros` stops them being saved or run at all, and macros stored in `%LocalAppData%` are not loaded when Tabular Editor starts.

In Tabular Editor 3, `BlockUnsafeScripts` allows macros only where they stay within the semantic model. A macro that reads or writes a file, reaches the network, starts another program or references an outside assembly is saved, but left out of every menu so it cannot be run by accident. You will find it under **View > Macros** with its **Blocked** column filled in, where it can still be opened and edited; bring it back inside the line and its menu item returns without restarting Tabular Editor. Saving such a macro tells you it is saved but will not run.

See [C# Scripts](xref:csharp-scripts#administrator-policies) for what counts as staying within the model, and @policies for the registry values themselves.

## 宏 JSON 文件

宏以名为 MacroActions.json 的 JSON 文件形式存储在 %LocalAppFolder%/TabularEditor3 中。 For more information on file types in Tabular Editor please see [Supported File Types](xref:supported-files#macroactionsjson)

## 宏文件示例

An example of a MacroActions.JSON file can be found here. 其中包含我们脚本库中的多个 C# Script: [下载示例 MacroActions 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


