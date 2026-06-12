---
uid: dax-debugger
title: DAX调试器
author: Daniel Otykier
updated: 2022-01-19
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

# DAX调试器

> [!NOTE]
> DAX调试器在 3.2.0 版本中推出。 随着我们为调试器添加更多功能，本文信息可能会有所变化。 随着我们为调试器添加更多功能，本文信息可能会有所变化。

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/m4g9BxcUf4U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

众所周知，DAX 是一门相对复杂、很难精通的语言。 大多数数据模型开发者可能都经历过这样一种情况：DAX 代码没有返回预期结果。 在这种情况下，把代码按变量逐个拆开、按函数调用逐步拆开，会有助于更好地理解到底发生了什么。

在此之前，这种对代码进行“拆解”的工作既繁琐又耗时，往往需要捕获客户端工具执行的 DAX 查询，然后在 [DAX Studio](https://daxstudio.org/) 或 [SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15) 中将查询拆开并执行其中较小的片段。

Tabular Editor 3 引入了 **DAX调试器** 概念，这是一款工具，可让你更轻松地逐步深入模型中的 DAX 代码。 从概念上讲，这个调试器类似于传统 IDE 的调试器，比如你在开发 C# 应用程序时 Visual Studio 自带的调试器。 从概念上讲，这个调试器类似于传统 IDE 的调试器，比如你在开发 C# 应用程序时 Visual Studio 自带的调试器。

## 先决条件

DAX调试器会分析你模型中的 DAX 代码，并生成适用于评估子表达式、行语境等的 DAX 查询，让你能够以交互方式逐步执行代码。

要实现这一点，Tabular Editor 3 必须在 **连接模式** 或 **工作区模式** 下运行，比如直接从 Power BI Desktop 或任何其他 Analysis Services 实例加载模型元数据时。

# 开始使用

当 Tabular Editor 3 已连接到某个 Analysis Services 实例时，可以通过以下两种方式之一启动调试器：

- 通过 Pivot Grid
- 通过 DAX 查询

启动调试器后，你会看到多个新视图，它们为正在调试的代码提供上下文信息；同时还会有一个 DAX 脚本视图，用于突出显示当前正在调试的那部分代码。

> [!TIP]
> 在开始调试会话之前，建议先格式化你的 DAX 代码，让代码更易读。

# 通过 Pivot Grid 调试

1. 创建一个新的 Pivot Grid（**文件 > 新建 > Pivot Grid**）
2. 将你要调试的度量值添加到 Pivot Grid。 你可以： 你可以：

- 从 TOM Explorer 拖动一个度量值，或
- 在 TOM Explorer 中右键单击某个度量值，然后选择 **添加到 Pivot Grid**，或
- 从 Pivot Grid 字段列表中选择该度量值（**Pivot Grid > 显示字段**）

3. （可选）在 Pivot Grid 的筛选区域、列区域或行区域中添加一列或多列。
4. 在 Pivot Grid 中右键单击数值单元格，然后选择 **调试此值**。

![从 Pivot Grid 调试](~/content/assets/images/features/debug-from-pivot.png)

# 通过 DAX 查询调试

1. 创建一个新的 DAX 查询（**文件 > 新建 > DAX 查询**）。
2. 输入或粘贴 DAX 查询。 通常，这应是一条由 `SUMMARIZECOLUMNS` 调用构成的查询，并包含一个或多个（显式）度量值，例如 Power BI 中的 Visual 所生成的查询。

> [!TIP]
> 你可以在 Power BI Desktop 中使用 [Performance Analyzer](https://docs.microsoft.com/en-us/power-bi/create-reports/desktop-performance-analyzer) 来捕获由 Visual 生成的查询。

3. 按 F5 在 Tabular Editor 3 中执行查询。 找到你要调试的值，右键单击该单元格并选择 **调试**。

![从查询中调试](~/content/assets/images/features/debug-from-query.png)

# 调试视图

调试器提供以下视图（如果它们被隐藏，可通过 **调试 > 窗口** 菜单访问）。

- 局部变量
- 监视
- 评估语境
- 调用树

<a name="locals"></a>

## 局部变量

此视图会列出当前执行范围内的列、度量值和变量，并显示它们的值。 它还会显示当前正在调试的子表达式的值。 当你单步切换到其他子表达式，或评估语境发生变化时，此列表中的值会自动更新。 **局部变量值始终在调用树中当前选定的项上求值**。

![Locals](~/content/assets/images/locals.png)

你可以在 **值** 列中点击放大镜按钮来检查某个局部变量值。 这会弹出一个对话框，更详细地显示该值。 当被检查的值是一个表时，这尤其有用。 这会弹出一个对话框，更详细地显示该值。 当被检查的值是一个表时，这尤其有用。

![Inspect locals value](~/content/assets/images/inspect-locals.png)

如果你更想在单独的 DAX 查询窗口中检查局部变量值，可以在 **工具 > 偏好 > DAX调试器 > 局部变量** 中关闭 **使用弹出式检查器** 选项。

![Dax 调试器设置](~/content/assets/images/features/dax-debugger-settings.png)

## 监视

此视图允许你输入任意 DAX 表达式，并在当前评估语境中进行计算。 你既可以输入标量表达式，也可以输入表表达式；可以使用所有可用的 DAX 函数，并引用当前评估范围内的变量。 当你单步切换到其他子表达式，或评估语境发生变化时，监视值会自动更新。 **监视值始终在评估语境堆栈中当前选定项的作用域内求值**。 你既可以输入标量表达式，也可以输入表表达式；可以使用所有可用的 DAX 函数，并引用当前评估范围内的变量。 当你单步切换到其他子表达式，或评估语境发生变化时，监视值会自动更新。 **监视值始终在评估语境堆栈中当前选定项的作用域内求值**。

![Watch](~/content/assets/images/watch.png)

要快速将变量、度量值或子表达式添加到“监视”视图，只需选中一段代码并将其拖到“监视”视图中。 你也可以将光标放在要添加的表达式上，然后右键并选择 **监视此表达式**： 你也可以将光标放在要添加的表达式上，然后右键并选择 **监视此表达式**：

![Quick Add To Watch](~/content/assets/images/quick-add-to-watch.png)

要添加、复制或删除观察表达式，请使用“监视”视图的右键菜单：

![Watch Context Menu](~/content/assets/images/watch-context-menu.png)

**生成查询** 选项与 **值** 列中的放大镜按钮一致，如下方截图中高亮所示。 点击此项后，调试器会打开一个新的 DAX 查询文档，其中既定义了计算的语境，也定义了计算本身，让你能够更详细地检查结果。 当观察表达式是表表达式时，这一点尤其有用，如下所示：

![Inspect Watch](~/content/assets/images/inspect-watch.png)

> [!TIP]
> **Locals** 视图和 **Watch** 视图有什么区别？
>
> - **Locals** 会显示当前执行范围内列、度量值、变量及其他相关子表达式的值，其中也包括调用树中当前选定子表达式的值。
> - **Watch** 允许你输入任意 DAX 表达式，并在当前评估语境中对其进行计算。

## 评估语境

此视图提供有关当前子表达式的 DAX 评估语境的信息。 例如，`CALCULATE` 表达式可能会执行语境转换，或向评估语境添加筛选；`SUMX` 这类迭代器则可能会添加行语境。 例如，`CALCULATE` 表达式可能会执行语境转换，或向评估语境添加筛选；`SUMX` 这类迭代器则可能会添加行语境。

![评估语境](~/content/assets/images/evaluation-context.png)

你可以在评估语境堆栈中双击某个项目，将焦点定位到该项目。 这会使所有 **Watch** 表达式在新的语境下重新计算（即从堆栈底部直到并包含当前聚焦项的所有语境）。 如下方动画所示。 另外，你还可以在任意活动迭代中通过翻页浏览各行，从而在活动行语境中检查各列的值：

![Call Tree](~/content/assets/images/navigating-evaluation-context.gif)

你还可以从外层筛选语境中切换单个筛选条件（例如，生成查询的 [`SUMMARIZECOLUMNS`](https://dax.guide/summarizecolumns) 调用中的分组列，或 Pivot Grid 中指定的筛选条件）。 如下方动画所示。 以这种方式切换的筛选条件会同时对 Watch 和 Locals 生效。

![Call Tree](~/content/assets/images/toggle-filters.gif)

最后，你可以浏览任意迭代器的前 1000 行：点击 **Row** 列中的 Zoom 按钮，即可将当前行语境设置为这前 1000 行中的某一行。

![Browse Row Contexts](~/content/assets/images/browse-row-contexts.png)

## 调用树

此视图提供整个计算的结构概览，并让你通过双击轻松在各个子表达式之间导航（也可以使用快捷键进行导航）。 该树还提供有关语境转换、迭代以及行语境的信息。 不会执行的代码分支（例如 `IF` 或 `SWITCH` 调用中的分支，或迭代器为空时）会被加上删除线。

![Call Tree](~/content/assets/images/call-tree.png)

当你在调用树的各个项之间切换时，调试器中的 DAX 脚本会高亮显示与当前调用树项对应的代码，并标出（以灰色背景显示）到达该高亮代码所经过的路径，如下所示：

![Call Tree](~/content/assets/images/navigating-call-tree.gif)

注意，当你在树中导航时，**Locals** 视图中的值会随之更新。 你也可以将光标悬停在表达式上，右键单击并选择 **Step into selection** 选项（Ctrl+B），进入某个子表达式。 你也可以将光标悬停在表达式上，右键单击并选择 **Step into selection** 选项（Ctrl+B），进入某个子表达式。

![Step into selection](~/content/assets/images/debugger-step-into-selection.png)

<a name="scalar-predicates"></a>

## 标量谓词

在 [`CALCULATE`](https://dax.guide/calculate) 或 [`CALCULATETABLE`](https://dax.guide/calculatetable) 函数的筛选参数中使用的标量谓词，会在 **Locals** 视图中以一种特殊方式处理。

例如，下面的度量值使用了一个标量谓词，仅显示在美国或加拿大产生的销售额。

```dax
CALCULATE(
    [Total Sales],
    Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
)
```

乍一看，第 3 行的表达式似乎会返回一个标量值（true/false）。 不过，在 DAX 中，筛选条件本质上是表。 乍一看，第 3 行的表达式似乎会返回一个标量值（true/false）。 不过，在 DAX 中，筛选条件本质上是表。 实际上，标量谓词会使用 [`FILTER`](https://dax.guide/filter) 函数转换为一个表表达式，如下所示：

```dax
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(Geography[Country Region Code]),
        Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
    )
)
```

`FILTER` 函数是一个迭代器，会遍历表 `ALL(Geography[Country Region Code])`，即 Geography 表中“Country Region Code”列的所有唯一值。 迭代器会为迭代中的每一行生成一个筛选语境。 然后会在每个这样的行语境中计算该标量谓词。 对于 `FILTER` 函数，只会保留谓词计算结果为 `TRUE` 的行。 在此示例中，`FILTER` 函数会输出一个包含 1 列（“Country Region Code”）且有 2 行（“US”和“CA”）的表。 迭代器会为迭代中的每一行生成一个筛选语境。 然后会在每个这样的行语境中计算该标量谓词。 对于 `FILTER` 函数，只会保留谓词计算结果为 `TRUE` 的行。 在此示例中，`FILTER` 函数会输出一个包含 1 列（“Country Region Code”）且有 2 行（“US”和“CA”）的表。

在调试标量谓词时，**Locals** 视图会显示两个特殊项：**(Current expression)** 和 **(Filter expression)**。 具体如下： 具体如下：

![调试标量谓词](~/content/assets/images/features/debug-scalar-predicates.png)

在上面的屏幕截图中：

1. 这是当前正在调试的标量谓词。 这是当前正在调试的标量谓词。 尽管这个子表达式看起来像是应返回标量值（true/false），但实际上它返回的是一张表。
2. **（当前表达式）**：这是谓词在上文所述、由 `FILTER` 函数生成的当前_行语境_中求值后得到的_标量_值。 **（当前表达式）**：这是谓词在上文所述、由 `FILTER` 函数生成的当前_行语境_中求值后得到的_标量_值。 在截图中，标量值的计算结果为 `False`，因为当前行语境中 [Country Region Code] 的值是 "AU"，如在 **Watch** 视图中所示 (4)。 我们可以使用 **Evaluation Context** 视图 (5) 逐行浏览迭代过程。 我们可以使用 **Evaluation Context** 视图 (5) 逐行浏览迭代过程。
3. **（筛选表达式）**：这是由 `FILTER` 函数生成的_表_表达式，如上所述。 在截图中，这是一个 1x2 表，包含值 "US" 和 "CA"。 点击放大镜按钮会打开一个弹出窗口，以网格形式显示表中的值。
4. 我们可以使用 **Watch** 窗口，在当前评估语境中对任意 DAX 表达式求值。 在这种情况下，由于我们有一个活动的行语境，因此可以直接引用行语境中的列，例如 `Geography[Country Region Code]`。 我们可以看到此列的当前值是“AU”，因此标量谓词 (2) 的求值结果为 `False`。 在这种情况下，由于我们有一个活动的行语境，因此可以直接引用行语境中的列，例如 `Geography[Country Region Code]`。 我们可以看到此列的当前值是“AU”，因此标量谓词 (2) 的求值结果为 `False`。
5. 我们可以使用 **Evaluation Context** 视图逐行浏览迭代过程。 我们可以使用 **Evaluation Context** 视图逐行浏览迭代过程。 这会更新 **Locals** 视图以及 **Watch** 视图中的值，以反映当前行语境中的值。

## 键盘快捷键

使用以下键盘快捷键可快速在调用树中导航：

- **单步进入 (F11)** - 进入调用树中当前项的第一个子项。 如果没有更多子项，则跳转到下一个同级项。 如果没有更多子项，则跳转到下一个同级项。
- **单步跳出 (Shift-F11)** - 跳出到调用树中当前项的父项。
- **单步跳过 (F10)** - 跳转到下一个函数参数、算术运算的下一个子表达式，或进入当前函数调用（如果它不是一个简单的函数）。
- **回退一步 (Shift-F10)** - 跳转到上一个函数参数、算术运算的上一个子表达式；如果当前项之前没有参数或子表达式，则跳出到当前项的父项。
- **进入所选内容 (Ctrl-B)** - 跳转到光标下的表达式。 如果有多条路径通向同一表达式（例如，当某个度量值被多个度量值引用，而这些度量值又被其他度量值引用时），系统会弹出对话框提示你选择路径。
- **下一行 (F9)** - 将最内层迭代的行语境移动到迭代器的下一行。
- **上一行 (Shift-F9)** - 将最内层迭代的行语境移动到迭代器的上一行。

# 限制和已知问题

DAX调试器当前有以下限制：

- **UDFs：** 当前不支持用户定义函数 (UDF)。 如果在正在调试的代码中遇到 UDF，调试器可能会出现异常行为。 如果在正在调试的代码中遇到 UDF，调试器可能会出现异常行为。
- 调试 DAX 查询时，仅支持部分 DAX 表表达式（例如，可以调试依赖 [SUMMARIZECOLUMNS](https://dax.guide/summarizecolumns) 的查询，但其他表格函数目前不支持）。 通常支持由 Power BI 生成的查询（可通过 Power BI Desktop 性能分析器捕获）。 通常支持由 Power BI 生成的查询（可通过 Power BI Desktop 性能分析器捕获）。
- 目前不支持包含隐式度量值或查询范围内计算的查询。
- 在浏览由筛选后的表表达式产生的迭代器的前 1000 行时，浏览窗口中选中的行并不总是与评估语境堆栈中的当前行语境相对应（在 **监视** 窗口中输入 `CALCULATETABLE('<table name>')` 以检查当前行语境）。
- 调试器目前仅允许在度量值上调试 DAX 表达式。
- 无法调试 [Visual 计算](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-visual-calculations-overview)，因为它们是使用查询范围内的列定义的。 调试器目前不支持查询范围内的对象。 调试器目前不支持查询范围内的对象。
- 如果某个度量值在筛选语境中被计算项修改，那么调试器的“监视/本地变量”视图里显示的部分结果可能不正确。

如果你遇到的调试器问题不在上面的列表中，请将其提交到 TE3 社区支持 GitHub 站点的 [问题跟踪器](https://github.com/TabularEditor/TabularEditor3/issues)。

# 路线图

我们计划在未来持续为 DAX调试器添加更多功能，以解决上述问题，并让这个工具更加强大。 一如既往，我们非常欢迎反馈。 功能需求和一般讨论请使用 [Discussions 区](https://github.com/TabularEditor/TabularEditor3/discussion)。

**调试愉快！**
