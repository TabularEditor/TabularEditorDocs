---
uid: creating-macros
title: 创建宏
author: Morten Lønskov
updated: 2023-12-07
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
      note: "称为“自定义操作”"
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# （教程）创建宏

宏是保存在 Tabular Editor 中的 C# Script，可以在不同语义模型之间轻松复用。
将脚本保存为宏后，在 TOM Explorer 中右键单击对象即可使用该宏，从而轻松将脚本应用到模型中。

> [!NOTE]
> 在 Tabular Editor 2 中，用于复用 C# Script 的功能叫做 @custom-actions。

## 创建宏

创建宏的第一步是编写并测试一个 C# Script。

> [!TIP]
> 开始进行 C# Script 编写的一个简单方法是使用内置的录制功能，它会记录你在 TOM Explorer 中执行的操作。
> 这样你就能看到如何与不同的模型对象交互，并创建可复用的脚本。
> 另一种方法是复用现有脚本，例如我们的[脚本库](xref:csharp-script-library)中的脚本。
> 在本教程中，我们使用脚本 [Format Numeric Measures](xref:script-format-numeric-measures) 来演示宏功能。

当脚本满足要求并正常运行后，可点击工具栏中的“另存为宏”按钮保存脚本，这将打开“保存宏”窗口。

![宏 创建信息框](~/content/assets/images/features/macros/macro_tutorial_create_infobox.png)

“保存宏”窗口提供三个选项：

1. 宏名称：为宏命名，并使用反斜杠 "\" 为该宏创建文件夹路径（见下文）
2. 为宏提供工具提示，方便你记住它的具体作用
3. 选择宏应在哪个上下文中可用。

![宏保存信息框](~/content/assets/images/features/macros/macro_tutorial_save_window.png)

在上面的示例中，宏将保存到名为 Formatting\Beginner 的文件夹中，脚本名为“格式化数字度量值”。 它会保存在“度量值”上下文中。

### 宏上下文

宏会保存在一个“有效上下文”中，该上下文决定脚本可以应用到模型中的哪些对象。

之后，在 TOM Explorer 中右键单击某个度量值时即可使用该宏。 保存宏时所选择的上下文决定：在哪些对象上右键单击时会显示该宏。

Tabular Editor 会根据正在保存的脚本建议一个上下文。

![宏菜单快捷方式](~/content/assets/images/features/macros/macro_tutorial_menu_shortcut.png)

## 编辑宏

在“宏”窗格中双击即可打开宏。编辑 C# Script 后，可按 _Ctrl + S_ 或单击“Edit Macro”按钮保存。

![宏编辑信息框](~/content/assets/images/features/macros/macro_tutorial_edit_infobox.png)

## 宏 JSON 文件

宏以名为 MacroActions.json 的 JSON 文件形式存储在 %LocalAppFolder%/TabularEditor3 中。 有关 Tabular Editor 中包括宏在内的文件类型的更多信息，请参阅 [支持的文件类型](xref:supported-files#macroactionsjson)

## 宏文件示例

你可以在此处找到一个宏文件 MacroActions.json 示例。 其中包含我们脚本库中的多个 C# Script: [下载示例 MacroActions 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


