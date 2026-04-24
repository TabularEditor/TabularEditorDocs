---
uid: dax-editor
title: DAX编辑器
author: Daniel Otykier
updated: 2023-02-03
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

# DAX编辑器

**DAX编辑器**是 Tabular Editor 3 的核心功能。

它提供三种不同的_模式_：

- **表达式编辑器** 用于在 TOM Explorer 中对对象上的单个 DAX 表达式进行快速修改。
- **DAX 查询**（连接功能）用于编写 DAX 查询，从已连接的 Analysis Services / Power BI 实例中获取数据。
- **DAX脚本**：用于在单个文档中查看并编辑多个对象的 DAX 表达式及其基本属性。

这三种模式在[键盘快捷键](xref:shortcuts3#dax-code)、语法高亮、Code Assist 等方面支持的操作完全一致。

<a name="code-assist-features"></a>

## Code Assist 功能

Tabular Editor 3 的 DAX编辑器提升效率的关键在于其**参数信息**和**自动补全**功能。 这些功能统称为 **Code Assist**（其他厂商通常称之为“IntelliSense”）。

**参数信息**会在光标所在位置显示该 DAX 函数及其参数的详细信息。 这些信息会以工具提示的形式显示在光标上方。 按 [Esc] 关闭工具提示，按 [Ctrl+Shift+Space] 显示工具提示。

**自动补全**会在你输入时在下拉框中提供与上下文相关的建议。 你可以使用键盘在下拉列表中选择条目，按下 [Enter] 或 [Tab] 即可将所选条目插入代码中。 按 [Esc] 关闭下拉框，按 [Ctrl+Space] 打开下拉框。

也可以通过编辑器的上下文菜单调用这些功能。

使用上/下箭头在不同语法选项之间切换时，DAX 调用提示会随之更新。

![Dax Code Assist](~/content/assets/images/dax-code-assist.png)

Code Assist 的大多数选项可在 [**工具 > 偏好 > 文本编辑器 > DAX编辑器 > Code Assist**](xref:preferences#dax-editor--code-assist) 中进行配置。

## 窥视定义

当光标停留在变量或度量值引用等对象引用上时，按下 [Alt+F12]，即可在光标下方显示包含该对象定义的内联编辑器。 当你想查看被引用对象的 DAX 代码，同时又不想离开文档中的当前位置时，这会很有用。

![窥视定义](~/content/assets/images/peek-definition.png)

按 Esc 键就能关闭“窥视定义”面板。

## 转到定义

除了用“窥视定义”，你也可以直接跳转到被引用对象的定义位置。 要这么做，按下 [F12]。 如果被引用对象不在当前文档中定义，此操作会跳转到 TOM Explorer 中的该对象。 如有需要，你可以按 [Alt+左箭头] 返回。

# 定义度量值

对于 DAX脚本和 DAX 查询，有时需要将代码中其他位置引用的度量值定义一并包含进来。 当光标位于度量值引用上时，**定义度量值** 功能可让你做到这一点。 如果你还想把所有下游的度量值引用也一并包含进来，也可以选择 **定义度量值及依赖项** 选项。

![定义度量值及依赖项](~/content/assets/images/define-measure-with-deps.png)

# 内联度量值

如果你想将某个度量值的定义带入当前文档，**内联度量值** 功能正好可以做到这一点。 当原始度量值引用处于行语境中时，Tabular Editor 会自动在度量值表达式外包裹 [`CALCULATE`](https://dax.guide/calculate)（度量值引用本就隐式包含该函数）。

# 格式化 DAX

Tabular Editor 3 中的 DAX编辑器会在你输入时自动格式化代码，比如修正函数和对象引用的大小写、添加合适的缩进，以及在括号内外加上适当的空格等。 这些都可以在 [**工具 > 偏好 > 文本编辑器 > DAX编辑器 > 自动格式化**](xref:preferences#dax-editor--auto-formatting) 中进行配置。

不过，有时也需要对整个文档进行格式化。 按 [F6] 即可；如果你希望换行更频繁，可按 [Shift+F6]。 对于 DAX 查询，你还可以使用 [Alt+F6] 重新格式化代码，让逗号始终放在行首，这在调试时很有用。

# 重构

如果你想更改变量或扩展列的名称，可以在光标位于该变量或扩展列引用处时，使用 **重构** 选项 (Ctrl+R)。 这会选中该对象的所有引用，让你一次性在所有位置完成重命名。

# 可配置的键盘快捷键

DAX编辑器以及一般的代码编辑器都具有很强的可配置性，并支持许多额外命令，帮助你快速、高效地编辑代码。 你可以在 **工具 > 偏好 > Tabular Editor > 键盘** 中查看所有这些命令，并修改和分配键盘快捷键。