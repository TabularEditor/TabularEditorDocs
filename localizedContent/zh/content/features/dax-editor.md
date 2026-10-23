---
uid: dax-editor
title: DAX编辑器
author: Daniel Otykier
updated: 2026-10-11
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

**DAX 编辑器**是 Tabular Editor 3 的核心。

它有三种不同的*版本*：

- **表达式编辑器**用于对 TOM Explorer 中对象的单个 DAX 表达式进行快速更改。
- **DAX 查询**（已连接功能）用于编写 DAX 查询，以便从连接的 Analysis Services/Power BI 实例检索数据。
- **DAX脚本**用于在单个文档中查看和编辑多个对象的DAX表达式和基本属性。

所有三种版本在[键盘快捷键](xref:shortcuts3#dax-code)、语法高亮、代码辅助等方面都支持相同的操作。

## Code Assist 功能

Tabular Editor 3 的 DAX 编辑器中提高工作效率的主要推动因素是其**参数信息**和**自动补全**功能。统称为**Code Assist**功能（其他供应商使用“IntelliSense”一词）。

**参数信息**提供有关光标所在位置的 DAX 函数及其参数的详细信息。该信息显示在光标上方的工具提示中。按 [Esc] 关闭工具提示，按 [Ctrl+Shift+空格键] 显示工具提示。

**自动补全**在您输入时，在下拉框中提供与上下文相关的建议。您可以使用键盘导航下拉菜单中的项，按 [Enter] 或 [Tab] 将所选项插入到您的代码中。您可以按 [Esc] 关闭下拉菜单，按 [Ctrl+空格键] 打开下拉菜单。

这些功能也可以通过编辑器的上下文菜单调用。

当您使用向上/向下箭头切换语法备选方案时，DAX 参数提示会随之更新。

![DAX 代码助手](~/content/assets/images/dax-code-assist.png)

代码辅助的大多数方面都可以在 [**工具 > 首选项 > 文本编辑器 > DAX 编辑器 > 代码辅助**](xref:preferences#text-editors--dax-editor--code-assist) 下进行配置。

## 窥视定义

当光标位于变量或度量值引用等对象引用上方时，按 [Alt+F12] 将在光标下方显示包含该对象定义的内联编辑器。当您想要查看引用对象的 DAX 代码，而又不想离开文档中的当前位置时，这非常有用。

![窥视定义](~/content/assets/images/peek-definition.png)

使用 Esc 键再次关闭“窥视定义”面板。

## 转到定义

除了“快速查看”之外，我们还可以直接跳转到被引用对象被定义的位置。要执行此操作，请按 [F12]。如果被引用对象未在当前文档中定义，此操作将跳转到 TOM Explorer 中的该对象。如果需要，您可以使用 [Alt+向左箭头] 导航返回。

## 定义度量值

对于 DAX 脚本和 DAX 查询，有时包含代码中其他位置引用的 Measure 的定义会很有用。当光标位于 Measure 引用上方时，**定义 Measure** 功能可让您执行此操作。如果您还希望包含所有下游度量值引用，也可以选择**定义具有依赖项的度量值**选项。

![定义带依赖项的度量值](~/content/assets/images/define-measure-with-deps.png)

## 内联度量值

如果您想将度量值的定义引入当前文档，**内联度量值**功能可以让您做到这一点。在 DAX 编辑器中右键单击 Measure 引用，然后选择**内联 Measure**。

在计算 Measure 的表达式之前，Measure 引用会隐式地将当前行转换为筛选器。因此，原样粘贴表达式将改变结果。所以，当引用位于行语境中时（例如，作为 [`SUMX`](https://dax.guide/sumx) 或 [`FILTER`](https://dax.guide/filter) 等迭代器的第二个参数），Tabular Editor 会将内联表达式封装在 [`CALCULATE`](https://dax.guide/calculate) 中，以保留该行为：

```dax
// Before using inline measure on the [Margin] measure
SUMX ( 'Sales', [Margin] )

// After using inline measure on the [Margin] measure
SUMX ( 'Sales', CALCULATE ( 'Sales'[Amount] - 'Sales'[Cost] ) )
```

仅在能够产生影响的地方添加包装。在以下情况下，插入的表达式不带包装：

- 引用**不在行语境中**，包括当它已经位于其自身的 `CALCULATE( ... )` 中时
- 度量的表达式**不从模型中读取任何内容**（常量、对另一个度量的引用或对 `TODAY()` 等函数的调用）。对表、列、日历或[用户定义函数](xref:udfs)的引用确实算作从模型中读取，并且确实会得到包裹
- 该表达式**已通过没有筛选器参数的 `CALCULATE( ... )` 或 `CALCULATETABLE( ... )` **自行执行转换**。如果有筛选器参数，仍会添加包裹，因为筛选器参数在转换之前进行计算。

如果无法分析该度量的表达式，则会添加包装，其原则是，不需要的包装是无害的，而缺少包装则不然。

## 格式化DAX

Tabular Editor 3 中的 DAX 编辑器会在您键入时自动设置代码格式，即修正函数和对象引用的大小写，在括号之间添加适当的缩进和空格等。所有这些都可以在[**工具 > 首选项 > 文本编辑器 > DAX 编辑器 > 自动格式化**](xref:preferences#text-editors--dax-editor--auto-formatting)下进行配置。

但是，有时有必要格式化整个文档。如果您希望更频繁地换行，可以通过按 [F6] 或 [Shift+F6] 来完成此操作。对于 DAX 查询，您还可以使用 [Alt+F6] 重新格式化代码，以便始终在行首添加逗号，这在调试时非常有用。 

## 重构

如果您想更改变量或扩展列的名称，可以在光标位于变量或扩展列引用上时使用**重构**选项 (Ctrl+R)。这将选择该对象的所有实例，使您能够一次性在所有位置对其重命名。

## 可配置的键盘快捷键

DAX 编辑器和代码编辑器通常具有高度可配置性，并支持许多其他命令，用于快速、高效地编辑代码。您可以在**工具 > 首选项 > Tabular Editor > 键盘**下查看所有这些命令，以及修改和分配键盘快捷键。
