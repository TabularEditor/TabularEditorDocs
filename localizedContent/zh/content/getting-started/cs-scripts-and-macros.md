---
uid: cs-scripts-and-macros
title: C# Script 与宏简介
author: Daniel Otykier
updated: 2021-11-03
---

# C# Script 与宏简介

任何声称能提升你生产力的软件，都应该提供某种方式来**自动化用户交互**。 In Tabular Editor, you can write C# scripts for exactly this purpose. With C# scripts in Tabular Editor, you can, for example:

- 自动创建 TOM 对象，例如度量值、表、计算项
- 与 TOM Explorer 中当前选定的对象(s)交互
- 自动为多个对象分配属性
- 以多种格式导入和导出元数据，用于审计或编写文档

如果脚本修改了你的模型元数据，你可以立即在 TOM Explorer 和属性视图中看到这些修改。 Moreover, you can **undo script changes**, effectively rolling back the model metadata to the point before the script was executed. If a script fails execution, the changes are automatically rolled back by default.

Tabular Editor 3 内置一个简单的**Script recorder**，当你对模型进行更改时，它会逐步添加脚本代码行，帮助你学习所使用的语法。

脚本可以保存为独立文件（`.csx` 扩展名），并可在 Tabular Editor 用户之间共享。 In addition, a script can be stored as a reusable **macro**, which integrates the script more closely with Tabular Editors user interface.

# 创建脚本

要创建新的 C# 脚本，请使用菜单 **文件 > 新建 > C# Script**。 Note that this option is available even when no model is loaded in Tabular Editor.

在你的第一个脚本中，输入以下代码：

```csharp
Info("Hello world!");
```

按 F5 运行代码。

![你的第一个脚本](~/content/assets/images/first-script.png)

如果你在输入代码时出现错误，所有语法错误都会在 **信息视图** 中显示。

- 要将脚本保存为文件，只需点击 **文件 > 保存**（Ctrl+S）即可。
- To open a script from a file, use the **File > Open > File...** (Ctrl+O) option. “打开文件”对话框默认会查找扩展名为 `.cs` 或 `.csx` 的文件。

# 使用 Script recorder 功能

当 C# Script 脚本视图处于焦点时，你可以在 Tabular Editor 中通过 **C# Script > 录制脚本** 菜单选项启动 Script recorder。 While the script is recording, any change you make to your model metadata will cause additional lines of code to be added to the script. Note that you cannot edit the script manually until you stop the recording.

![Csharp Script Recorder](~/content/assets/images/csharp-script-recorder.png)

# 访问模型元数据

要访问当前加载的模型中的特定对象，你需要使用 C# 语法在 Tabular Object Model (TOM) 层次结构中进行导航。 The root of this hierarchy is the `Model` object.

下面的脚本会输出当前加载模型的名称。 If no model is loaded, a warning is displayed.

```csharp
if(Model != null)
    Info("The name of the current model is: " + Model.Name);
else
    Warning("No model is currently loaded!");
```

`Model` 对象是对 [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) 类的封装，公开其中一部分属性，并额外提供了一些便捷的方法和属性。

要访问某个特定的度量值，你需要知道该度量值的名称，以及它所在表的名称：

```csharp
var myMeasure = Model.Tables["Internet Sales"].Measures["Internet Total Sales"];
myMeasure.Description = "The formula for this measure is: " + myMeasure.Expression;
```

上述脚本的第 1 行在“Internet Sales”表上定位到“Internet Total Sales”度量值，然后将该度量值的引用存入 `myMeasure` 变量。

脚本的第 2 行根据一段硬编码字符串以及该度量值的（DAX）表达式来设置度量值的说明。

Tabular Editor 可以自动生成引用特定对象的代码：将对象从 TOM Explorer 拖放到 C# Script 视图即可。

![通过拖放生成对象引用](~/content/assets/images/generate-csharp-code.gif)

Most TOM objects (tables, columns, measures, etc.) in Tabular Editor, exposes the same set of properties that are available when using the AMO/TOM client libraries directly. For this reason, you can refer to [Microsoft's AMO/TOM documentation](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet), to learn which properties are available. For example, [here](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure?view=analysisservices-dotnet#properties) is the documentation for available measure properties.

# 访问当前 TOM Explorer 的选中项

为了让脚本可复用，仅仅像上面那样通过名称直接引用模型中的对象通常远远不够。 Instead, it is useful to refer to whichever object(s) is currently selected in Tabular Editor's **TOM Explorer view**. This is possible through the use of the `Selected` object.

```csharp
Info("You have currently selected: " + Selected.Measures.Count + " measure(s).");
```

The `Selected` object by itself is a collection of all objects currently selected, including objects within selected display folders. In addition, the `Selected` object contains multiple properties that makes it easy to refer to specific object types, such as the `.Measures` property shown in the example above. In general, these properties exist in both a plural (`.Measures`) and a singular (`.Measure`) form. The former is a collection that you can iterate through, and which will be empty if the current selection does not contain any objects of that type, whereas the latter is a reference to the currently selected object, if and only if exactly one of that type of object is selected.

@useful-script-snippets 文章包含了许多示例脚本，展示如何使用 `Selected` 对象来完成各种任务。

# 与用户交互

In the examples above, we used the `Info(...)` and `Warning(...)` global methods to show a message to the user in various flavors. Tabular Editor provides a number of these global methods as well as extension methods for showing and collecting information, and for various other common tasks. The most commonly used are listed below:

- `void Output(object value)` - 暂停脚本执行，并显示所提供对象的详细信息。 When the provided object is a TOM object or a collection of TOM objects, a detailed view of all properties are shown.
- `void SaveFile(string filePath, string content)` - 将文本数据保存到文件的便捷方式。
- `string ReadFile(string filePath)` - 从文件加载文本数据的便捷方式。
- `string ExportProperties(IEnumerable<ITabularNamedObject> objects, string properties = "...")` - 将多个对象的一组属性导出为 TSV 字符串的便捷方式。
- `void ImportProperties(string tsvData)` - 将 TSV 字符串中的属性导入多个对象的便捷方式。
- `string ConvertDax(dax, useSemicolons)` - 在 US/UK 与非 US/UK 区域设置之间相互转换 DAX 表达式。 If `useSemicolons` is true (default) the `dax` string is converted from the native US/UK format to non-US/UK. That is, commas (list separators) will be converted to semicolons and periods (decimal separators) will be converted to commas. Vice versa if `useSemicolons` is set to false.
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

你经常使用的脚本可以保存为可重复使用的宏，每次启动 Tabular Editor 时都能使用。 Moreover, macros are automatically integrated in the context menu of the **TOM Explorer view** and you can even use the **Tools > Customize...** option to add macros to existing or custom menus and toolbars.

要将脚本保存为宏，请使用 **C# Script > 保存为宏...** 选项。

![保存新宏](~/content/assets/images/save-new-macro.png)

Provide a name for your macro. 你可以使用反斜杠将宏组织到文件夹中。例如，名称 "My Macros\Test" 会在 TOM Explorer 的上下文菜单中创建一个 "My Macros" 子菜单，并在该子菜单中提供一个 "Test" 菜单选项，用于调用该脚本。

你还可以提供一个可选的工具提示，当鼠标悬停在宏创建的菜单选项上时会显示该提示。

你还需要指定宏上下文，用来规定需要选中哪些类型(一种或多种)的对象，宏才会在上下文菜单中可用。

最后，你可以在 **宏启用条件（高级）** 下指定一个应计算为 true/false 的 C# 表达式（通常基于 `Selected` 或 `Model` 对象）。 This lets you control more granularly whether the macro should be enabled or not, based on the current selection. For example, you could use the following expression:

```csharp
Selected.Measures.Count == 1
```

仅当恰好选中 1 个度量值时才启用宏。

# 管理宏

你可以在**宏视图**中查看之前保存的所有宏。 To bring this view into focus, use the **View > Macros** menu option. This view allows you to:

- **重命名宏**（只需将光标放到 **Name** 列中，然后输入新名称）
- **删除宏。** 选中它，然后单击宏列表上方的红色“X”按钮。
- **Edit a macro.** Double-click the macro in the list (double-click on the "Id" column of the list). This will open the macro in a new C# script view, where you can make code changes. Hit Ctrl+S to save the code changes. 如果你需要编辑其他宏属性（工具提示、宏上下文等），请使用 **C# Script > Edit Macro...** 菜单项。

# 后续步骤

- @personalizing-te3
- @boosting-productivity-te3

# 延伸阅读

- @C# 脚本
- @useful-script-snippets