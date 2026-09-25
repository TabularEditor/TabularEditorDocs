---
uid: dax-editor
title: DAX编辑器
author: Daniel Otykier
updated: 2026-09-14
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

它提供三种不同的模式：

- **表达式编辑器** 用于在 TOM Explorer 中对对象上的单个 DAX 表达式进行快速修改。
- **DAX 查询**（连接功能）用于编写 DAX 查询，从已连接的 Analysis Services / Power BI 实例中获取数据。
- **DAX脚本**：用于在单个文档中查看并编辑多个对象的 DAX 表达式及其基本属性。

这三种模式在[键盘快捷键](xref:shortcuts3#dax-code)、语法高亮、Code Assist 等方面支持的操作完全一致。

## Code Assist 功能

Tabular Editor 3 的 DAX编辑器提升效率的关键在于其**参数信息**和**自动补全**功能。 Collectively, these are known as **Code Assist** features (other vendors use the term "IntelliSense").

**参数信息**会在光标所在位置显示该 DAX 函数及其参数的详细信息。 The information is displayed in a tooltip above the cursor. Hit [Esc] to close the tooltip and [Ctrl+Shift+Space] to display it.

**Auto-Complete** provides context-sensitive suggestions as you type, in a dropdown box. You can use the keyboard to navigate the items in the dropdown and hitting [Enter] or [Tab] will insert the selected item into your code. You can hit [Esc] to close the dropdown and [Ctrl+Space] to open it.

也可以通过编辑器的上下文菜单调用这些功能。

DAX calltips update as you cycle syntax alternatives using the Up/Down arrows.

![Dax Code Assist](~/content/assets/images/dax-code-assist.png)

Code Assist 的大多数选项可在 [**工具 > 偏好 > 文本编辑器 > DAX编辑器 > Code Assist**](xref:preferences#dax-editor--code-assist) 中进行配置。

## 窥视定义

While the cursor is over an object reference such as a variable or a measure reference, hit [Alt+F12] to display an inline editor with the definition of that object, below the cursor. This is useful when you want to see the DAX code of a referenced object without leaving the current position in the document.

![窥视定义](~/content/assets/images/peek-definition.png)

Use the Esc key to close the Peek Definition panel again.

## 转到定义

Instead of peeking, we can also jump straight to the location where the referenced object is defined. To do this, hit [F12]. If the referenced object is not defined within the current document, this operation will jump over to that object in the TOM Explorer. If needed, you can navigate back using [Alt+Left Arrow].

## 定义度量值

For DAX scripts and DAX queries, it is sometimes useful to include the definition of a measure that is referenced elsewhere in the code. The **Define Measure** feature lets you do that when the cursor is over a measure reference. You may also choose the **Define Measure with Dependencies** option if you want to include all downstream measure references as well.

![定义度量值及其依赖项](~/content/assets/images/define-measure-with-deps.png)

## Inline Measure

If you want to bring the definition of a measure into the current document, the **Inline Measure** feature lets you do just that. Right-click a measure reference in the DAX editor and choose **Inline Measure**.

A measure reference implicitly turns the current row into a filter before the measure's expression is evaluated. Pasting the expression in as-is would therefore change the result, so when the reference sits inside a row context, for example as the second argument of an iterator such as [`SUMX`](https://dax.guide/sumx) or [`FILTER`](https://dax.guide/filter), Tabular Editor wraps the inlined expression in [`CALCULATE`](https://dax.guide/calculate) to preserve that behavior:

```dax
// Before using inline measure on the [Margin] measure
SUMX ( 'Sales', [Margin] )

// After using inline measure on the [Margin] measure
SUMX ( 'Sales', CALCULATE ( 'Sales'[Amount] - 'Sales'[Cost] ) )
```

The wrap is only added where it can make a difference. The expression is inserted unwrapped when:

- the reference is **not inside a row context**, including when it already sits inside a `CALCULATE( ... )` of its own
- the measure's expression **reads nothing from the model** (a constant, a reference to another measure or a call to a function such as `TODAY()`). A reference to a table, a column, a calendar or a [user-defined function](xref:udfs) does count as reading from the model, and does get the wrap
- the expression **already performs the transition itself**, through a `CALCULATE( ... )` or `CALCULATETABLE( ... )` with no filter arguments. With a filter argument the wrap is still added, because filter arguments are evaluated before the transition

If the measure's expression cannot be analyzed, the wrap is added, on the principle that a wrap that was not needed is harmless where a missing one is not.

## 格式化 DAX

Tabular Editor 3 中的 DAX编辑器会在你输入时自动格式化代码，比如修正函数和对象引用的大小写、添加合适的缩进，以及在括号内外加上适当的空格等。 All of this can be configured under [**Tools > Preferences > Text Editors > DAX Editor > Auto Formatting**](xref:preferences#dax-editor--auto-formatting).

However, sometimes it is necessary to format the entire document. This can be done by hitting [F6] or [Shift+F6] if you prefer more frequent line breaks. 对于 DAX 查询，你还可以使用 [Alt+F6] 重新格式化代码，让逗号始终放在行首，这在调试时很有用。

## 重构

如果你想更改变量或扩展列的名称，可以在光标位于该变量或扩展列引用处时，使用 **重构** 选项 (Ctrl+R)。 This will select all instances of that object, allowing you to rename it everywhere at once.

## 可配置的键盘快捷键

DAX编辑器以及一般的代码编辑器都具有很强的可配置性，并支持许多额外命令，帮助你快速、高效地编辑代码。 You can view all of these commands, as well as modify and assign keyboard shortcuts under **Tools > Preferences > Tabular Editor > Keyboard**.
