---
uid: macros
title: 创建宏
author: Morten Lønskov
updated: 2023-12-07
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

宏是在 Tabular Editor 中保存的 C# Script，可在不同语义模型间轻松复用。
将脚本保存为宏后，你就可以在 TOM Explorer 中右键单击对象时使用该宏，从而轻松将脚本应用到你的模型中。
将脚本保存为宏后，你就可以在 TOM Explorer 中右键单击对象时使用该宏，从而轻松将脚本应用到你的模型中。

## 创建宏

创建宏的第一步是编写并测试一个 C# Script。

> [!TIP]
> 开始使用 C# 脚本编写的一个简单方法是使用内置的录制功能，它可以录制你在 TOM Explorer 中执行的操作。
> 通过这种方式，你可以了解如何与不同的模型对象交互，并创建可复用的脚本。
> 另一种方法是复用现有脚本，例如我们[脚本库](xref:csharp-script-library)中的脚本。
> 在本教程中，我们使用脚本 [Format Numeric Measures](xref:script-format-numeric-measures) 来演示宏功能。
> 通过这种方式，你可以了解如何与不同的模型对象交互，并创建可复用的脚本。
> 另一种方法是复用现有脚本，例如我们[脚本库](xref:csharp-script-library)中的脚本。
> 在本教程中，我们使用脚本 [Format Numeric Measures](xref:script-format-numeric-measures) 来演示宏功能。

当脚本按要求运行后，可以使用工具栏按钮“保存为宏”保存脚本，这会打开“保存宏”窗口。

![宏创建信息框](~/content/assets/images/features/macros/macro_tutorial_create_infobox.png)

“保存宏”窗口提供三个选项：

1. 宏名称：为宏命名，并使用反斜杠 "\" 为宏创建文件夹路径（见下文）
2. 为宏添加工具提示，方便记住其具体用途
3. 选择宏应可用的上下文。

![宏保存提示框](~/content/assets/images/features/macros/macro_tutorial_save_window.png)

在上面的示例中，宏将保存在名为 Formatting\Beginner 的文件夹中，脚本名为 "Format Numeric Measures"。 它将保存在“度量值”上下文中。 它将保存在“度量值”上下文中。

### 宏上下文

宏会保存在一个“有效上下文”中，该上下文决定脚本可以应用到模型中的哪些对象。

然后，您可以在 TOM Explorer 中右键单击度量值时使用此宏。 保存宏时指定的上下文决定了右键单击哪些对象时会显示该宏。 保存宏时指定的上下文决定了右键单击哪些对象时会显示该宏。

Tabular Editor 会根据正在保存的脚本建议一个上下文。

![宏菜单快捷方式](~/content/assets/images/features/macros/macro_tutorial_menu_shortcut.png)

## 编辑宏

在“宏”窗格中双击该宏即可打开；编辑 C# Script 后，可使用 _Ctrl + S_ 或单击“编辑宏”按钮保存。

![宏编辑信息框](~/content/assets/images/features/macros/macro_tutorial_edit_infobox.png)

## 宏 JSON 文件

宏以名为 MacroActions.json 的 JSON 文件形式存储在 %LocalAppFolder%/TabularEditor3 中。 有关 Tabular Editor 中文件类型的更多信息，请参阅 [支持的文件类型](xref:supported-files#macroactionsjson) 有关 Tabular Editor 中文件类型的更多信息，请参阅 [支持的文件类型](xref:supported-files#macroactionsjson)

## 宏文件示例

此处提供了一个 MacroActions.JSON 文件示例。 此处提供了一个 MacroActions.JSON 文件示例。 其中包含我们脚本库中的多个 C# Script：[下载示例 MacroActions 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


