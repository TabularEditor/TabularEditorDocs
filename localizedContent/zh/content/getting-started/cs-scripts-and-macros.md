---
uid: cs-scripts-and-macros
title: C# Script 与宏简介
author: Daniel Otykier
updated: 2021-11-03
---

# C# Script 与宏简介

任何声称能提升你生产力的软件，都应该提供某种方式来**自动化用户交互**。 在 Tabular Editor 中，你可以为此编写 C# Script。 借助 Tabular Editor 中的 C# Script，例如你可以： 在 Tabular Editor 中，你可以为此编写 C# Script。 借助 Tabular Editor 中的 C# Script，例如你可以：

- 自动创建 TOM 对象，例如度量值、表、计算项
- 与 TOM Explorer 中当前选定的对象(s)交互
- 自动为多个对象分配属性
- 以多种格式导入和导出元数据，用于审计或编写文档

如果脚本修改了你的模型元数据，你可以立即在 TOM Explorer 和属性视图中看到这些修改。 此外，你还可以**撤销脚本更改**，将模型元数据有效回滚到脚本执行之前的状态。 如果脚本执行失败，默认会自动回滚更改。 此外，你还可以**撤销脚本更改**，将模型元数据有效回滚到脚本执行之前的状态。 如果脚本执行失败，默认会自动回滚更改。

Tabular Editor 3 内置一个简单的**Script recorder**，当你对模型进行更改时，它会逐步添加脚本代码行，帮助你学习所使用的语法。

脚本可以保存为独立文件（`.csx` 扩展名），并可在 Tabular Editor 用户之间共享。 此外，脚本还可以保存为可复用的**宏**，从而让脚本与 Tabular Editor 的用户界面更紧密地集成。 此外，脚本还可以保存为可复用的**宏**，从而让脚本与 Tabular Editor 的用户界面更紧密地集成。

# 创建脚本

要创建新的 C# 脚本，请使用菜单 **文件 > 新建 > C# Script**。 注意：即使 Tabular Editor 里没有加载任何模型，也能用这个选项。 注意：即使 Tabular Editor 里没有加载任何模型，也能用这个选项。

在你的第一个脚本中，输入以下代码：

```csharp
Info("Hello world!");
```

按 F5 运行代码。

![你的第一个脚本](~/content/assets/images/first-script.png)

如果你在输入代码时出现错误，所有语法错误都会在 **信息视图** 中显示。

- 要将脚本保存为文件，只需点击 **文件 > 保存**（Ctrl+S）即可。
- 要从文件打开脚本，请使用 **文件 > 打开 > 文件...**（Ctrl+O）选项。 要从文件打开脚本，请使用 **文件 > 打开 > 文件...**（Ctrl+O）选项。 “打开文件”对话框默认会查找扩展名为 `.cs` 或 `.csx` 的文件。

# 使用 Script recorder 功能

当 C# Script 脚本视图处于焦点时，你可以在 Tabular Editor 中通过 **C# Script > 录制脚本** 菜单选项启动 Script recorder。 在录制期间，你对模型元数据所做的任何更改，都会让脚本中追加相应的代码行。 请注意，在停止录制之前，你无法手动编辑脚本。 在录制期间，你对模型元数据所做的任何更改，都会让脚本中追加相应的代码行。 请注意，在停止录制之前，你无法手动编辑脚本。

![Csharp Script Recorder](~/content/assets/images/csharp-script-recorder.png)

# 访问模型元数据

要访问当前加载的模型中的特定对象，你需要使用 C# 语法在 Tabular Object Model (TOM) 层次结构中进行导航。 该层次结构的根节点是 `Model` 对象。 该层次结构的根节点是 `Model` 对象。

下面的脚本会输出当前加载模型的名称。 如果未加载任何模型，将显示警告。 如果未加载任何模型，将显示警告。

```csharp
if(Model != null)
    Info("当前模型的名称为： " + Model.Name);
else
    Warning("当前未加载任何模型！");
```

`Model` 对象是对 [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) 类的封装，公开其中一部分属性，并额外提供了一些便捷的方法和属性。

要访问某个特定的度量值，你需要知道该度量值的名称，以及它所在表的名称：

```csharp
var myMeasure = Model.Tables["Internet Sales"].Measures["Internet Total Sales"];
myMeasure.Description = "此度量值的公式为： " + myMeasure.Expression;
```

上述脚本的第 1 行在“Internet Sales”表上定位到“Internet Total Sales”度量值，然后将该度量值的引用存入 `myMeasure` 变量。

脚本的第 2 行根据一段硬编码字符串以及该度量值的（DAX）表达式来设置度量值的说明。

Tabular Editor 可以自动生成引用特定对象的代码：将对象从 TOM Explorer 拖放到 C# Script 视图即可。

![通过拖放生成对象引用](~/content/assets/images/generate-csharp-code.gif)

Tabular Editor 中的大多数 TOM 对象（表、列、度量值等） 公开的属性集与直接使用 AMO/TOM 客户端库时可用的属性集相同。 因此，你可以参考 [Microsoft 的 AMO/TOM 文档](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet)，了解有哪些可用属性。 例如，[此处](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure?view=analysisservices-dotnet#properties) 提供了可用度量值属性的文档。

# 访问当前 TOM Explorer 的选中项

为了让脚本可复用，仅仅像上面那样通过名称直接引用模型中的对象通常远远不够。 相反，引用 Tabular Editor 的 **TOM Explorer 视图** 中当前选中的对象(一个或多个)会更有用。 这可以通过使用 `Selected` 对象来实现。 相反，引用 Tabular Editor 的 **TOM Explorer 视图** 中当前选中的对象(一个或多个)会更有用。 这可以通过使用 `Selected` 对象来实现。

```csharp
Info("你当前已选择： " + Selected.Measures.Count + " 个度量值(s)。");
```

`Selected` 对象本身是一个集合，包含当前选中的所有对象，包括所选显示文件夹中的对象。 此外，`Selected` 对象还包含多个属性，便于引用特定对象类型，例如上例中的 `.Measures` 属性，即度量值集合。 一般来说，这些属性同时提供复数形式（`.Measures`，度量值集合）和单数形式（`.Measure`，度量值）。 前者是一个可供你迭代的集合；如果当前选择不包含该类型的任何对象，它将为空。后者则是对当前所选对象的引用，只有在且仅在恰好选中了一个该类型对象时才会有值。

@useful-script-snippets 文章包含了许多示例脚本，展示如何使用 `Selected` 对象来完成各种任务。

# 与用户交互

在上面的示例中，我们使用 `Info(...)` 和 `Warning(...)` 全局方法，以不同方式向用户显示信息。 Tabular Editor 提供了不少这类全局方法以及扩展方法，用于显示与收集信息，以及处理其他常见任务。 最常用的如下：

- `void Output(object value)` - 暂停脚本执行，并显示所提供对象的详细信息。 如果提供的对象是 TOM 对象或 TOM 对象集合，将显示其所有属性的详细视图。 如果提供的对象是 TOM 对象或 TOM 对象集合，将显示其所有属性的详细视图。
- `void SaveFile(string filePath, string content)` - 将文本数据保存到文件的便捷方式。
- `string ReadFile(string filePath)` - 从文件加载文本数据的便捷方式。
- `string ExportProperties(IEnumerable<ITabularNamedObject> objects, string properties = "...")` - 将多个对象的一组属性导出为 TSV 字符串的便捷方式。
- `void ImportProperties(string tsvData)` - 将 TSV 字符串中的属性导入多个对象的便捷方式。
- `string ConvertDax(dax, useSemicolons)` - 在 US/UK 与非 US/UK 区域设置之间相互转换 DAX 表达式。 如果 `useSemicolons` 为 true（默认），`dax` 字符串会从 US/UK 本地格式转换为非 US/UK 格式。 也就是说，逗号（列表分隔符）会转换为分号，句点（小数分隔符）会转换为逗号。 如果将 `useSemicolons` 设为 false，则反之亦然。 如果 `useSemicolons` 为 true（默认），`dax` 字符串会从 US/UK 本地格式转换为非 US/UK 格式。 也就是说，逗号（列表分隔符）会转换为分号，句点（小数分隔符）会转换为逗号。 如果将 `useSemicolons` 设为 false，则反之亦然。
- `void FormatDax(IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - 对所提供集合中的所有对象的 DAX 表达式进行格式化
- `void FormatDax(IDaxDependantObject obj)` - 将对象加入队列，以便在脚本执行完成后，或调用 `CallDaxFormatter` 方法时，对其 DAX 表达式进行格式化。
- `void CallDaxFormatter(bool shortFormat, bool? skipSpace)` - 对截至目前已入队对象的所有 DAX 表达式进行格式化
- `void Info(string message)` - 显示一条信息。
- `void Warning(string message)` - 显示一条警告信息。
- `void Error(string message)` - 显示一条错误信息。
- `measure SelectMeasure(Measure preselect = null, string label = "...")` - 显示所有度量值的列表，并提示你选择一个。
- `T SelectObject<T>(this IEnumerable<T> objects, T preselect = null, string label = "...") where T: TabularNamedObject` - 显示提供的对象列表，提示你选择一个，并返回该对象（如果按下“取消”按钮，则返回 null）。
- `IList<T> SelectObjects<T>(this IEnumerable<T> objects, IEnumerable<T> preselect = null, string label = "...") where T: TabularNamedObject` - 显示提供的对象列表，提示你选择任意数量的对象，并返回所选对象的列表（如果按下“取消”按钮，则返回 null）。

# 将脚本保存为宏

你经常使用的脚本可以保存为可重复使用的宏，每次启动 Tabular Editor 时都能使用。 此外，宏会自动集成到 **TOM Explorer 视图** 的上下文菜单中；你甚至可以使用 **工具 > 自定义...** 选项，将宏添加到现有或自定义的菜单和工具栏。 此外，宏会自动集成到 **TOM Explorer 视图** 的上下文菜单中；你甚至可以使用 **工具 > 自定义...** 选项，将宏添加到现有或自定义的菜单和工具栏。

要将脚本保存为宏，请使用 **C# Script > 保存为宏...** 选项。

![保存新宏](~/content/assets/images/save-new-macro.png)

给你的宏起个名字。 给你的宏起个名字。 你可以使用反斜杠将宏组织到文件夹中。例如，名称 "My Macros\Test" 会在 TOM Explorer 的上下文菜单中创建一个 "My Macros" 子菜单，并在该子菜单中提供一个 "Test" 菜单选项，用于调用该脚本。

你还可以提供一个可选的工具提示，当鼠标悬停在宏创建的菜单选项上时会显示该提示。

你还需要指定宏上下文，用来规定需要选中哪些类型(一种或多种)的对象，宏才会在上下文菜单中可用。

最后，你可以在 **宏启用条件（高级）** 下指定一个应计算为 true/false 的 C# 表达式（通常基于 `Selected` 或 `Model` 对象）。 这样你就可以根据当前选择，更细粒度地控制宏是否应启用。 例如，你可以使用以下表达式： 这样你就可以根据当前选择，更细粒度地控制宏是否应启用。 例如，你可以使用以下表达式：

```csharp
Selected.Measures.Count == 1
```

仅当恰好选中 1 个度量值时才启用宏。

# 管理宏

你可以在**宏视图**中查看之前保存的所有宏。 要将此视图置于前台，请使用 **视图 > 宏** 菜单项。 该视图可让你： 要将此视图置于前台，请使用 **视图 > 宏** 菜单项。 该视图可让你：

- **重命名宏**（只需将光标放到 **Name** 列中，然后输入新名称）
- **删除宏。** 选中它，然后单击宏列表上方的红色“X”按钮。
- **编辑宏。** 在列表中双击该宏（双击列表的“Id”列）。 这会在新的 C# Script 视图中打开该宏，你可以在那里修改代码。 按 Ctrl+S 保存代码更改。 **编辑宏。** 在列表中双击该宏（双击列表的“Id”列）。 这会在新的 C# Script 视图中打开该宏，你可以在那里修改代码。 按 Ctrl+S 保存代码更改。 如果你需要编辑其他宏属性（工具提示、宏上下文等），请使用 **C# Script > Edit Macro...** 菜单项。

# 后续步骤

- @personalizing-te3
- @boosting-productivity-te3

# 延伸阅读

- @csharp-scripts
- @useful-script-snippets