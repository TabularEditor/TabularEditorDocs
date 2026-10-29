---
uid: dax-debugger
title: DAX 调试器
author: Daniel Otykier
updated: 2026-10-12
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
# DAX 调试器

> [!NOTE]
> DAX 调试器在 3.2.0 版本中推出。随着我们为调试器添加更多功能，本文中的信息可能会发生变化。

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/m4g9BxcUf4U" title="YouTube 视频播放器" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

众所周知，DAX 是一种相对复杂的语言，很难掌握。大多数数据模型开发人员可能都曾遇到过 DAX 代码未返回预期结果的情况。在这种情况下，将代码逐个变量和逐个函数调用进行分解，有助于更好地了解发生了什么。

到目前为止，这种代码的“分解”是一项繁琐且耗时的任务，通常需要捕获由客户端工具执行的DAX查询，以便将其分解并在[DAX Studio](https://daxstudio.org/)或[SQL Server Management Studio](https://docs.microsoft.com/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15)中执行较小的查询片段。

Tabular Editor 3 引入了**DAX 调试器**的概念，这是一种工具，让您单步执行模型 DAX 代码的过程变得更加轻松。在概念层面上，调试器类似于传统的 IDE 调试器，例如在开发 C# 应用程序时 Visual Studio 中所用的调试器。

## 前提条件
DAX 调试器分析模型中的 DAX 代码，并生成用于评估子表达式、行上下文等的合适 DAX 查询，使您能够以交互方式单步执行代码。

为了使此功能正常工作，Tabular Editor 3 必须在**连接模式**或**工作区模式**下运行，例如直接从 Power BI Desktop 或任何其他 Analysis Services 实例加载模型元数据时。

# 开始使用

当 Tabular Editor 3 连接到 Analysis Services 实例时，可以通过以下两种方式之一启动调试器：

- 通过 Pivot Grid
- 通过 DAX 查询

启动调试器后，系统会向您显示多个新视图，这些视图提供有关正在调试的代码的上下文信息，以及突出显示当前正在调试的代码部分的 DAX 脚本视图。

> [!TIP]
> 在开始调试会话之前，请考虑格式化您的 DAX 代码，以便于阅读。

# 通过 Pivot Grid 进行调试

1. 创建新的 Pivot Grid (**文件 > 新建 > Pivot Grid**)
2. 将您要调试的度量值添加到Pivot Grid中。您可以：
  - 从 TOM Explorer 中拖动一个度量值，或
  - 在 TOM Explorer 中右键单击一个度量值，然后选择**添加到 Pivot Grid**，或者
  - 从Pivot Grid字段列表中选择度量值（**Pivot Grid > 显示字段**）
3. （可选）在筛选器区域、列区域或行区域中，向 Pivot Grid 添加一个或多个列或层次结构。
4. 右键单击Pivot Grid中的值单元格，然后选择**调试此值**。

![从数据透视表调试](~/content/assets/images/features/debug-from-pivot.png)

# 通过 DAX 查询进行调试

1. 创建新的 DAX 查询（**文件 > 新建 > DAX 查询**）。
2. 输入或粘贴 DAX 查询。这通常应是一个由 `SUMMARIZECOLUMNS` 调用组成、包含一个或多个（显式）度量值的查询，例如 Power BI 中可视化对象生成的查询。

> [!TIP]
> 您可以使用 Power BI Desktop 中的[性能分析器](https://docs.microsoft.com/power-bi/create-reports/desktop-performance-analyzer)来捕获视觉对象生成的查询。

3. 按 F5 在 Tabular Editor 3 中执行查询。找到要调试的值，右键单击单元格，然后选择**调试**。

![从查询调试](~/content/assets/images/features/debug-from-query.png)

# 调试视图

调试器提供以下视图（如果这些视图被隐藏，则可以通过**“调试”>“窗口”**菜单访问）。

- 局部变量
- 观察
- 评估语境
- 调用树

## 局部变量
此视图列出当前执行范围内的列、度量值和变量，并显示它们的值。它还显示当前正在调试的子表达式的值。当跳转到不同的子表达式时，或者当评估语境发生变化时，此列表中的值会自动更新。**局部值始终在调用树的当前所选项处进行求值**。

![局部变量](~/content/assets/images/locals.png)

您可以通过单击**值**列中的放大镜按钮来检查局部变量值。这将弹出一个对话框，更详细地显示该值。如果检查的值是表，则此功能特别有用。

![检查局部变量值](~/content/assets/images/inspect-locals.png)

如果您希望在单独的 DAX 查询窗口中检查局部变量值，可以关闭**工具 > 首选项 > DAX 调试器 > 局部变量**下的**使用弹出检查器**选项。

![DAX 调试器设置](~/content/assets/images/features/dax-debugger-settings.png)

## 观察
此视图允许您输入任何 DAX 表达式，该表达式将在当前评估上下文中进行计算。您可以输入标量和表格表达式，您可以使用所有可用的 DAX 函数，并引用当前计算范围内的变量。当单步执行到不同的子表达式时，或者当评估上下文发生变化时，监视值将自动更新。**监视值始终在评估语境栈中当前选定项的范围内进行评估**。

![监视](~/content/assets/images/watch.png)

要快速将变量、度量值或子表达式添加到“监视”视图，只需突出显示一部分代码，然后将其拖入“监视”视图即可。您还可以将光标置于要添加的表达式上，然后右键单击并选择**观察此表达式**：

![快速添加到监视](~/content/assets/images/quick-add-to-watch.png)

要添加、复制或删除观察表达式，请使用“观察”视图的右键单击上下文菜单：

![“监视”上下文菜单](~/content/assets/images/watch-context-menu.png)

**生成查询**选项与**值**列中的放大镜按钮相同，如下图所示。点击此选项后，调试器将打开一个新的 DAX 查询文档，该文档定义了计算的上下文以及计算本身，使您可以更详细地查看结果。当监视表达式是表表达式时，此功能尤为有用，如下所示：

![检查监视](~/content/assets/images/inspect-watch.png)

> [!TIP]
> **局部变量**视图和**监视**视图有何区别？
> - **局部变量**显示当前执行范围内的列、度量值、变量和其他相关子表达式的值，包括调用树中当前所选子表达式的值。
> - **监视**允许您输入任何 DAX 表达式，该表达式将在当前评估上下文中进行计算。

## 评估语境
此视图提供有关当前子表达式的 DAX 求值上下文的信息。例如，`CALCULATE` 表达式可能会执行语境转换或向求值语境添加筛选器，或者 `SUMX` 迭代器可能会添加行语境。

![评估语境](~/content/assets/images/evaluation-context.png)

您可以双击“评估上下文”堆栈中的某个项目，将焦点移至该项目。这将导致所有**监视**表达式在新上下文中重新求值（即从栈底到当前聚焦项（含）的所有上下文）。下图动画对此进行了说明。另请注意，您还可以通过在任何活动迭代中翻页浏览行，来检查活动行语境中各个列的值：

![调用树](~/content/assets/images/navigating-evaluation-context.gif)

您还可以从外部筛选语境中切换单个筛选器（例如，在生成查询的 [`SUMMARIZECOLUMNS`](https://dax.guide/summarizecolumns) 调用中对列进行分组，或在 Pivot Grid 中指定筛选器）。下面的动画对此进行了说明。以这种方式切换的筛选器将同时应用于“监视”和“局部变量”。

![调用树](~/content/assets/images/toggle-filters.gif)

最后，您可以通过点击**行**列中的“缩放”按钮，浏览任何迭代器的前 1000 行，并将当前行语境设置为这前 1000 行中的特定行。

![浏览行上下文](~/content/assets/images/browse-row-contexts.png)

## 调用树
此视图提供了整个计算的概览，并让您可以通过双击轻松在子表达式之间导航（您也可以使用快捷键进行导航）。该树还提供有关上下文转换、迭代和行上下文的信息。不会被执行的代码分支（例如在 `IF` 或 `SWITCH` 调用中，或者当迭代器为空时）会被划掉。

![调用树](~/content/assets/images/call-tree.png)

当您在调用树中的项之间导航时，DAX 调试脚本将突出显示与调用树项对应的代码，同时还会（以灰色背景）指示到达突出显示的代码所采用的路径，如下所示：

![调用树](~/content/assets/images/navigating-call-tree.gif)

请注意，在浏览树时，**局部变量**视图中的值是如何更新的。您还可以通过将光标悬停在表达式上、右键单击并选择**单步执行到选定内容**选项 (Ctrl+B) 来导航到子表达式。

![单步执行到选定内容](~/content/assets/images/debugger-step-into-selection.png)

## 标量谓词

[`CALCULATE`](https://dax.guide/calculate) 或 [`CALCULATETABLE`](https://dax.guide/calculatetable) 函数的筛选器参数中使用的标量谓词在**局部变量**视图中以特殊方式处理。

例如，以下度量值使用标量谓词，仅显示在美国或加拿大实现的销售额。

```dax
CALCULATE(
    [Total Sales],
    Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
)
```

乍一看，第 3 行的表达式似乎会返回标量值（真/假）。但是，在 DAX 中，筛选器是表格。实际上，标量谓词使用 [`FILTER`](https://dax.guide/filter) 函数转换为表表达式，如下所示：

```dax
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(Geography[Country Region Code]),
        Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
    )
)
```

`FILTER` 函数是一个迭代器，它对表 `ALL(Geography[Country Region Code])` 进行迭代，即对“Geography”表中“Country Region Code”列的所有唯一值进行迭代。迭代器为迭代中的每一行生成一个筛选语境。然后，在每个此类行语境中对标量谓词求值。对于 `FILTER` 函数，仅保留谓词计算结果为 `TRUE` 的行。在此示例中，`FILTER` 函数将输出一个包含 1 列（“Country Region Code”）和 2 行（“US”和“CA”）的表。

调试标量谓词时，**“局部变量”**视图将显示两个特殊项：**(当前表达式)**和**(筛选器表达式)**。这些项目描述如下：

![调试标量谓词](~/content/assets/images/features/debug-scalar-predicates.png)

在上面的截图中：

1. 这是当前正在调试的标量谓词。尽管这个子表达式看起来像是应该返回标量值（真/假）的表达式，但实际上它返回的是一个表。
2. **（当前表达式）**：这是谓词的*标量*值，当在如上所述由 `FILTER` 函数生成的当前*行语境*中求值时。在截图中，标量值的计算结果为 `False`，因为当前行语境中 [Country Region Code] 的值为“AU”，如 **Watch** 视图 (4) 中所示。我们可以使用**评估语境**视图 (5)，逐一行滚动浏览迭代的行。
3. **（筛选器表达式）**：这是由 `FILTER` 函数生成的*表*表达式，如上所述。在截图中，这是一个包含值“US”和“CA”的 1x2 表格。点击放大镜按钮将打开一个弹出窗口，在网格中显示表格值。
4. 我们可以使用“监视”窗口来计算当前计算上下文中的任何 DAX 表达式。在这种情况下，由于我们有活动行语境，因此可以直接引用行语境中的列，例如 `Geography[Country Region Code]`。我们可以看到，此列的当前值为“AU”，这就是标量谓词 (2) 的计算结果为 `False` 的原因。
5. 我们可以使用**评估语境**视图逐行滚动浏览迭代的行。这将更新**局部变量**视图和**监视**视图中的值,以反映当前行语境中的值。

## 键盘快捷键

使用以下键盘快捷键快速导航调用树：

- **单步执行 (F11)** - 单步执行到调用树中当前项的第一个子项。如果没有更多子项，则跳转到下一个同级项。
- **单步跳出 (Shift-F11)** - 跳出到调用树中当前项的父项。
- **单步执行 (F10)** - 跳转到下一个函数参数、算术运算的下一个子表达式，或单步进入当前函数调用（如果是非平凡函数）。
- **单步返回 (Shift-F10)** - 跳转到上一个函数参数、算术运算的上一个子表达式，或者如果当前项目之前没有参数或子表达式，则单步返回到当前项目的父级。
- **单步执行到选定内容 (Ctrl-B)** - 跳转到光标下的表达式。如果多条路径指向同一表达式（例如，当一个度量值被多个度量值和这些度量值引用时），将弹出一个对话框，提示您选择路径。
- **下一行 (F9)** - 将最内层迭代的行上下文移至迭代器的下一行。
- **上一行 (Shift-F9)** - 将最内层迭代的行上下文移至迭代器的上一行。

# 限制和已知问题

DAX 调试器目前存在以下限制：

- **UDF：**目前不支持用户定义函数 (UDF)。如果在正在调试的代码中遇到 UDF，调试器的行为可能会出乎意料。
- 调试 DAX 查询时，仅支持部分 DAX 表表达式（例如，可以调试依赖于 [SUMMARIZECOLUMNS](https://dax.guide/summarizecolumns) 的查询，但目前不支持其他表函数）。通常支持由 Power BI 生成的查询（可以通过 Power BI Desktop 性能分析器捕获）。
- 目前不支持包含隐式度量值或查询范围计算的查询。
- 浏览由筛选的表表达式产生的迭代器的前 1000 行时，浏览窗口中选定的行并不总能与评估语境栈中的当前行语境相对应（在**监视**窗口中键入 `CALCULATETABLE('<table name>')` 以检查当前行语境）。
- 调试器目前仅允许调试度量值上的DAX表达式。
- [可视化计算](https://learn.microsoft.com/power-bi/transform-model/desktop-visual-calculations-overview)无法调试，因为它们是使用查询范围列定义的。调试器目前不支持查询范围的对象。
- 如果度量值被筛选语境中的计算项修改，则调试器的“监视”/“局部变量”视图中显示的部分结果可能不正确。

如果您在使用调试器时遇到上述问题以外的问题，请将其发布到 TE3 社区支持 GitHub 网站上的[问题跟踪器](https://github.com/TabularEditor/TabularEditor3/issues)。

# 路线图

我们计划随着时间的推移，为 DAX 调试器添加许多其他功能，以解决上述问题，并使该工具具备更强大的功能。一如既往，我们非常欢迎您提供反馈。请使用[讨论区](https://github.com/TabularEditor/TabularEditor3/discussion)提出功能请求和进行一般讨论。

**祝您调试愉快！**
