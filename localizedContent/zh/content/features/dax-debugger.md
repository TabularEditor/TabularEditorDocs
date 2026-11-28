---
uid: dax-debugger
title: DAX 调试器
author: Daniel Otykier
updated: 2026-11-25
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

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/m4g9BxcUf4U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

众所周知，DAX 是一门相对复杂、很难精通的语言。大多数数据模型开发者可能都经历过这样一种情况：DAX 代码没有返回预期结果。在这种情况下，把代码按变量逐个拆开、按函数调用逐步拆开，会有助于更好地理解到底发生了什么。

在此之前，对代码进行这种“拆解”既繁琐又耗时，往往需要捕获客户端工具执行的 DAX 查询，然后在 [DAX Studio](https://daxstudio.org/) 或 [SQL Server Management Studio](https://docs.microsoft.com/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15) 中将查询拆分并执行其中较小的部分。

Tabular Editor 3 引入了 **DAX调试器** 概念，这是一款工具，可让你更轻松地逐步深入模型中的 DAX 代码。从概念上讲，这个调试器类似于传统 IDE 的调试器，比如你在开发 C# 应用程序时 Visual Studio 自带的调试器。

## 先决条件

DAX调试器会分析你模型中的 DAX 代码，并生成适用于评估子表达式、行语境等的 DAX 查询，让你能够以交互方式逐步执行代码。

要实现这一点，Tabular Editor 3 必须在 **连接模式** 或 **工作区模式** 下运行，比如直接从 Power BI Desktop 或任何其他 Analysis Services 实例加载模型元数据时。

# 开始使用

当 Tabular Editor 3 已连接到某个 Analysis Services 实例时，可以通过以下两种方式之一启动调试器：

- 通过 Pivot Grid
- 通过 DAX 查询

启动调试器后，系统会向您显示多个新视图，提供有关正在调试的代码的上下文信息。当前正在调试的代码部分，如果属于模型，则会在调试脚本视图中突出显示；如果由查询定义，则会在DAX查询中突出显示。

> [!TIP]
> 在开始调试会话之前，建议先格式化你的 DAX 代码，让代码更易读。

# 通过 Pivot Grid 调试

1. 创建一个新的 Pivot Grid（**文件 > 新建 > Pivot Grid**）
2. 将你要调试的度量值添加到 Pivot Grid。你可以：

- 从 TOM Explorer 拖动一个度量值，或
- 在 TOM Explorer 中右键单击某个度量值，然后选择 **添加到 Pivot Grid**，或
- 从 Pivot Grid 字段列表中选择该度量值（**Pivot Grid > 显示字段**）
3. （可选）在“筛选器”区域、“列”区域或“行”区域中，向 Pivot Grid 添加一个或多个列或层次结构。
4. 在 Pivot Grid 中右键单击数值单元格，然后选择 **调试此值**。

![从 Pivot Grid 调试](~/content/assets/images/features/debug-from-pivot.png)

# 通过 DAX 查询调试

1. 创建一个新的 DAX 查询（**文件 > 新建 > DAX 查询**）。
2. 输入或粘贴DAX查询。这通常应是一个由 `SUMMARIZECOLUMNS` 调用和一个或多个（显式）度量值组成的查询，例如 Power BI 中由可视化对象生成的查询。度量值可以是模型度量值，也可以是查询使用 `DEFINE MEASURE` 定义的度量值。

> [!TIP]
> 你可以在 Power BI Desktop 中使用 [Performance Analyzer](https://docs.microsoft.com/power-bi/create-reports/desktop-performance-analyzer) 来捕获由各个 Visual 生成的查询。

3. 按 F5 在 Tabular Editor 3 中执行查询。找到要调试的值，右键单击单元格，然后选择**调试单元格**。

![DAX 查询结果单元格上的右键菜单，显示“调试单元格”](~/content/assets/images/features/debug-from-query.png)

# 调试视图

调试器提供以下视图（如果它们被隐藏，可通过 **调试 > 窗口** 菜单访问）。

- 局部变量
- 监视
- 评估语境
- 调用树

## 局部变量

此视图会列出当前执行范围内的列、度量值和变量，并显示它们的值。它还会显示当前正在调试的子表达式的值。当你单步切换到其他子表达式，或评估语境发生变化时，此列表中的值会自动更新。**局部变量值始终在调用树中当前选定的项上求值**。

![Locals](~/content/assets/images/locals.png)

你可以在 **值** 列中点击放大镜按钮来检查某个局部变量值。这会弹出一个对话框，更详细地显示该值。当被检查的值是一个表时，这尤其有用。

![Inspect locals value](~/content/assets/images/inspect-locals.png)

如果您希望在单独的 DAX 查询窗口中检查局部变量值，可以关闭 **工具 > 首选项 > Tabular Editor > DAX 调试器 > 局部变量**下的**使用弹出检查器**选项。

![包含“局部变量”、“监视”和“DAX 查询”部分的 DAX 调试器首选项页面](~/content/assets/images/features/dax-debugger-settings.png)

## 监视

此视图允许你输入任意 DAX 表达式，并在当前评估语境中进行计算。你既可以输入标量表达式，也可以输入表表达式；可以使用所有可用的 DAX 函数，并引用当前评估范围内的变量。当你单步切换到其他子表达式，或评估语境发生变化时，监视值会自动更新。**监视值始终在评估语境堆栈中当前选定项的作用域内求值**。

![Watch](~/content/assets/images/watch.png)

要快速将变量、度量值或子表达式添加到“监视”视图，只需选中一段代码并将其拖到“监视”视图中。你也可以将光标放在要添加的表达式上，然后右键并选择 **监视此表达式**：

![Quick Add To Watch](~/content/assets/images/quick-add-to-watch.png)

要添加、复制或删除观察表达式，请使用“监视”视图的右键菜单：

![Watch Context Menu](~/content/assets/images/watch-context-menu.png)

**生成查询** 选项与 **值** 列中的放大镜按钮一致，如下方截图中高亮所示。点击此项后，调试器会打开一个新的 DAX 查询文档，其中既定义了计算的语境，也定义了计算本身，让你能够更详细地检查结果。当观察表达式是表表达式时，这一点尤其有用，如下所示：

![Inspect Watch](~/content/assets/images/inspect-watch.png)

> [!TIP]
> **Locals** 视图和 **Watch** 视图有什么区别？
>
> - **Locals** 会显示当前执行范围内列、度量值、变量及其他相关子表达式的值，其中也包括调用树中当前选定子表达式的值。
> - **Watch** 允许你输入任意 DAX 表达式，并在当前评估语境中对其进行计算。

## 评估语境

此视图提供有关当前子表达式的 DAX 评估语境的信息。例如，`CALCULATE` 表达式可能会执行语境转换，或向评估语境添加筛选；`SUMX` 这类迭代器则可能会添加行语境。

![评估语境](~/content/assets/images/evaluation-context.png)

你可以在评估语境堆栈中双击某个项目，将焦点定位到该项目。这会使所有 **Watch** 表达式在新的语境下重新计算（即从堆栈底部直到并包含当前聚焦项的所有语境）。如下方动画所示。另外，你还可以在任意活动迭代中通过翻页浏览各行，从而在活动行语境中检查各列的值：

![Call Tree](~/content/assets/images/navigating-evaluation-context.gif)

你还可以从外层筛选语境中切换单个筛选条件（例如，生成查询的 [`SUMMARIZECOLUMNS`](https://dax.guide/summarizecolumns) 调用中的分组列，或 Pivot Grid 中指定的筛选条件）。如下方动画所示。以这种方式切换的筛选条件会同时对 Watch 和 Locals 生效。

![Call Tree](~/content/assets/images/toggle-filters.gif)

最后，你可以浏览任意迭代器的前 1000 行：点击 **Row** 列中的 Zoom 按钮，即可将当前行语境设置为这前 1000 行中的某一行。

![Browse Row Contexts](~/content/assets/images/browse-row-contexts.png)

## 调用树

此视图提供整个计算的结构概览，并让你通过双击轻松在各个子表达式之间导航（也可以使用快捷键进行导航）。该树还提供有关语境转换、迭代以及行语境的信息。不会执行的代码分支（例如 `IF` 或 `SWITCH` 调用中的分支，或迭代器为空时）会被加上删除线。

![Call Tree](~/content/assets/images/call-tree.png)

当你在调用树的各个项之间切换时，调试器中的 DAX 脚本会高亮显示与当前调用树项对应的代码，并标出（以灰色背景显示）到达该高亮代码所经过的路径，如下所示：

![Call Tree](~/content/assets/images/navigating-call-tree.gif)

注意，当你在树中导航时，**Locals** 视图中的值会随之更新。你也可以将光标悬停在表达式上，右键单击并选择 **Step into selection** 选项（Ctrl+B），进入某个子表达式。

![Step into selection](~/content/assets/images/debugger-step-into-selection.png)

## 函数和查询定义的代码

调试器单步执行 [DAX 用户定义函数](xref:udfs)（DAX UDF）以及 DAX 查询定义的度量值和函数。

### 单步执行函数

您单步执行 DAX UDF 的方式与单步执行 Measure 引用的方式相同。这适用于模型函数以及 DAX 查询使用 `DEFINE FUNCTION` 定义的函数。

在**调用树**中，函数调用对于传递给 `VAL` 参数的每个参数都有一个子节点，后跟一个 `Function F(params)` 节点，例如 `Function Scale(x, f)`，函数体位于其下方。传递给 `EXPR` 的参数和引用类型参数出现在主体中，具体位置为主体使用该参数的每个地方。引用参数的节点显示参数名称，其中参数按调用位置的写法显示，例如 `x: [Sales Amount]`，显示在一行中，并在 60 个字符处截断。如果调用省略了可选参数，则节点将显示参数的默认值。

![包含函数调用节点的调用树、其函数 Scale(x, f) 节点和参数节点，旁边是显示参数的“局部变量”](~/content/assets/images/features/dax-debugger-call-tree-function.png)

当当前项位于函数体中时，**局部变量**会列出函数的参数，每个参数都带有调用传递给它的实参，并隐藏调用代码的变量。`VAL` 参数显示在调用位置计算的值，而 `EXPR` 或引用类型参数显示在当前求值上下文中求值的参数。当当前项位于传递给 `EXPR` 参数的参数中时，**局部变量**会显示该参数的写入范围：调用代码的变量，以及（如果调用位于另一个函数中）封闭函数的参数。

### 在DAX查询中定义的代码

当您调试 DAX 查询中的单元格时，查询使用 `DEFINE MEASURE` 或 `DEFINE FUNCTION` 定义的度量值和函数会在 DAX 查询本身中突出显示。调试脚本视图包含模型度量值，然后是模型函数，并且仅在被调试的代码使用模型度量值或函数时才会打开。当您在查询代码和模型代码之间单步执行时，包含当前项的视图将显示在最前面。右键单击DAX查询中的代码，即可使用**单步执行到选定内容**（**Ctrl+B**）和监视命令，与在调试脚本视图中一样。

如果查询重新定义了模型度量值或函数，则重新定义仅适用于查询自己的代码。使用重新定义对象的模型度量值和函数将保留模型的定义，就像查询运行时一样。

![正在调试的 DAX 查询，其中查询中的函数体被突出显示，调试工具栏上显示“停止调试”按钮](~/content/assets/images/features/dax-debugger-query-debugging.png)

在您调试 DAX 查询时，该查询为只读，并且自动完成功能不会在查询中或在调试脚本视图中打开。如果您在查询中键入、粘贴或删除文本，则会显示 **停止调试？** 提示，并附有“正在调试 DAX 查询时无法对其进行编辑。是否要停止调试以编辑查询？”：

- **确定**将停止调试。编辑未应用，因此请在查询可编辑后重复该操作。
- **取消**将继续调试，并使查询保持不变。

在选择**确定**之前，请先选择**不再询问**，以便在以后的编辑中停止调试而不显示提示。要恢复显示提示，请在**工具 > 首选项 > Tabular Editor > DAX 调试器 > DAX 查询**下选择**编辑正在调试的 DAX 查询前询问**。

![“停止调试？”提示，其中包含“不再询问”复选框](~/content/assets/images/features/dax-debugger-stop-debugging-prompt.png)

如果您在调试时关闭DAX查询或调试脚本视图，则会显示**停止调试？**提示。选择**确定**以停止调试并关闭文档。

### 停止调试

在**调试**工具栏或**调试**菜单中选择**停止调试**，以结束会话。DAX 查询再次变为可编辑状态，调试脚本视图以及**局部变量**、**监视**、**评估语境**和**调用树**窗口关闭。关闭已调试的文档或模型也会结束会话并关闭窗口。在下一会话中，窗口将再次打开至您上次离开时的位置，并显示相同的观察表达式。**停止调试**没有默认的键盘快捷键；请在**工具 > 首选项 > Tabular Editor > 键盘**下分配一个快捷键。

## 标量谓词

在 [`CALCULATE`](https://dax.guide/calculate) 或 [`CALCULATETABLE`](https://dax.guide/calculatetable) 函数的筛选参数中使用的标量谓词，会在 **Locals** 视图中以一种特殊方式处理。

例如，下面的度量值使用了一个标量谓词，仅显示在美国或加拿大产生的销售额。

```dax
CALCULATE(
    [Total Sales],
    Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
)
```

乍一看，第 3 行的表达式似乎会返回一个标量值（true/false）。不过，在 DAX 中，筛选条件本质上是表。实际上，标量谓词会使用 [`FILTER`](https://dax.guide/filter) 函数转换为一个表表达式，如下所示：

```dax
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(Geography[Country Region Code]),
        Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
    )
)
```

`FILTER` 函数是一个迭代器，会遍历表 `ALL(Geography[Country Region Code])`，即 Geography 表中“Country Region Code”列的所有唯一值。迭代器会为迭代中的每一行生成一个筛选语境。然后会在每个这样的行语境中计算该标量谓词。对于 `FILTER` 函数，只会保留谓词计算结果为 `TRUE` 的行。在此示例中，`FILTER` 函数会输出一个包含 1 列（“Country Region Code”）且有 2 行（“US”和“CA”）的表。

在调试标量谓词时，**Locals** 视图会显示两个特殊项：**(Current expression)** 和 **(Filter expression)**。具体如下：

![调试标量谓词](~/content/assets/images/features/debug-scalar-predicates.png)

在上面的屏幕截图中：

1. 这是当前正在调试的标量谓词。尽管这个子表达式看起来像是应返回标量值（true/false），但实际上它返回的是一张表。
2. **（当前表达式）**：这是谓词在上文所述、由 `FILTER` 函数生成的当前行语境中求值后得到的标量值。在截图中，标量值的计算结果为 `False`，因为当前行语境中 [Country Region Code] 的值是 "AU"，如在 **Watch** 视图中所示 (4)。我们可以使用 **Evaluation Context** 视图 (5) 逐行浏览迭代过程。
3. **（筛选表达式）**：这是由 `FILTER` 函数生成的表表达式，如上所述。在截图中，这是一个 1x2 表，包含值 "US" 和 "CA"。点击放大镜按钮会打开一个弹出窗口，以网格形式显示表中的值。
4. 我们可以使用 **Watch** 窗口，在当前评估语境中对任意 DAX 表达式求值。在这种情况下，由于我们有一个活动的行语境，因此可以直接引用行语境中的列，例如 `Geography[Country Region Code]`。我们可以看到此列的当前值是“AU”，因此标量谓词 (2) 的求值结果为 `False`。
5. 我们可以使用 **Evaluation Context** 视图逐行浏览迭代过程。这会更新 **Locals** 视图以及 **Watch** 视图中的值，以反映当前行语境中的值。

## 键盘快捷键

使用以下键盘快捷键可快速在调用树中导航：

- **单步进入 (F11)** - 进入调用树中当前项的第一个子项。如果没有更多子项，则跳转到下一个同级项。
- **单步跳出 (Shift-F11)** - 跳出到调用树中当前项的父项。
- **单步跳过 (F10)** - 跳转到下一个函数参数、算术运算的下一个子表达式，或进入当前函数调用（如果它不是一个简单的函数）。
- **回退一步 (Shift-F10)** - 跳转到上一个函数参数、算术运算的上一个子表达式；如果当前项之前没有参数或子表达式，则跳出到当前项的父项。
- **进入所选内容 (Ctrl-B)** - 跳转到光标下的表达式。如果有多条路径通向同一表达式（例如，当某个度量值被多个度量值引用，而这些度量值又被其他度量值引用时），系统会弹出对话框提示你选择路径。
- **下一行 (F9)** - 将最内层迭代的行语境移动到迭代器的下一行。
- **上一行 (Shift-F9)** - 将最内层迭代的行语境移动到迭代器的上一行。

**停止调试**没有默认快捷键。请参阅[停止调试](#stop-debugging)。

# 限制与已知问题

DAX 调试器存在以下限制：

- 调试 DAX 查询时，仅支持 DAX 表表达式的子集（例如，可以调试依赖于 [SUMMARIZECOLUMNS](https://dax.guide/summarizecolumns) 的查询，但不支持其他表函数）。通常支持由 Power BI 生成的查询（可以通过 Power BI Desktop 性能分析器捕获）。
- 只能调试返回度量值的单元格，该度量值可以是模型度量值，也可以是查询使用 `DEFINE MEASURE` 定义的度量值。内联表达式列的单元格（例如 `SUMMARIZECOLUMNS` 调用中的 `"Twice", Twice([Sales Amount])`）以及隐式度量值无法调试。
- 不支持引用查询范围 Measure 或函数参数的**监视**表达式。
- 在浏览由筛选后的表表达式产生的迭代器的前 1000 行时，浏览窗口中选中的行并不总是与评估语境堆栈中的当前行语境相对应（在 **监视** 窗口中输入 `CALCULATETABLE('<table name>')` 以检查当前行语境）。
- 调试器仅允许调试度量值上的DAX表达式。
- 无法调试依赖于查询范围列的单元格。这包括使用查询范围列定义的[视觉计算](https://learn.microsoft.com/power-bi/transform-model/desktop-visual-calculations-overview)。
- 如果某个度量值在筛选语境中被计算项修改，那么调试器的“监视/本地变量”视图里显示的部分结果可能不正确。

如果你遇到的调试器问题不在上面的列表中，请将其提交到 TE3 社区支持 GitHub 站点的 [问题跟踪器](https://github.com/TabularEditor/TabularEditor3/issues)。

# 路线图

我们计划在未来持续为 DAX调试器添加更多功能，以解决上述问题，并让这个工具更加强大。一如既往，我们非常欢迎反馈。功能需求和一般讨论请使用 [Discussions 区](https://github.com/TabularEditor/TabularEditor3/discussion)。

**调试愉快！**
