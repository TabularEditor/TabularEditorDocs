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

> [!NOTE]
> 在 Tabular Editor 2 中，用于复用 C# Script 的功能叫做 @custom-actions。

## 创建宏

创建宏的第一步是编写并测试一个 C# Script。

> [!TIP]
> 开始进行 C# Script 编写的一个简单方法是使用内置的录制功能，它会记录你在 TOM Explorer 中执行的操作。
> his way you can see how to interact with the different model objects and create reusable scripts.
> nother way is to reuse existing scripts such as those in our [script library](xref:csharp-script-library).
> n this tutorial we use the script [Format Numeric Measures](xref:script-format-numeric-measures) to showcase the Macro functionality.

当脚本满足要求并正常运行后，可点击工具栏中的“另存为宏”按钮保存脚本，这将打开“保存宏”窗口。

![宏 创建信息框](~/content/assets/images/features/macros/macro_tutorial_create_infobox.png)

“保存宏”窗口提供三个选项：

1. 宏名称：为宏命名，并使用反斜杠 "\" 为该宏创建文件夹路径（见下文）
2. 为宏提供工具提示，方便你记住它的具体作用
3. 选择宏应在哪个上下文中可用。

![宏保存信息框](~/content/assets/images/features/macros/macro_tutorial_save_window.png)

在上面的示例中，宏将保存到名为 Formatting\Beginner 的文件夹中，脚本名为“格式化数字度量值”。 It will be saved in the context of measures.

### 宏上下文

宏会保存在一个“有效上下文”中，该上下文决定脚本可以应用到模型中的哪些对象。

之后，在 TOM Explorer 中右键单击某个度量值时即可使用该宏。 The context given while saving the Macro determines which objects will show the Macro when right clicking on that object.

Tabular Editor 会根据正在保存的脚本建议一个上下文。

![宏菜单快捷方式](~/content/assets/images/features/macros/macro_tutorial_menu_shortcut.png)

## 编辑宏

在“宏”窗格中双击即可打开宏。编辑 C# Script 后，可按 _Ctrl + S_ 或单击“Edit Macro”按钮保存。

![宏编辑信息框](~/content/assets/images/features/macros/macro_tutorial_edit_infobox.png)

## 宏 JSON 文件

宏以名为 MacroActions.json 的 JSON 文件形式存储在 %LocalAppFolder%/TabularEditor3 中。 For more information on file types in Tabular Editor please see [Supported File Types](xref:supported-files#macroactionsjson)

## 宏文件示例

An example of a MacroActions.JSON file can be found here. 其中包含我们脚本库中的多个 C# Script: [下载示例 MacroActions 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


