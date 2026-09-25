---
uid: advanced-scripting
title: 高级脚本
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
      note: "Called C# scripts in Tabular Editor 3"
---

# 高级脚本

This is an introduction to the scripting capabilities of Tabular Editor. Everything below applies to both products, but the names differ: what Tabular Editor 2 calls **Advanced Scripting**, Tabular Editor 3 calls **C# scripts**, with a dedicated editor, IntelliSense, a script debugger and saved macros. See @csharp-scripts for the Tabular Editor 3 experience, and @csharp-script-library for real-life examples.

## 什么是高级脚本？

Tabular Editor 的界面旨在让你在构建表格模型时，轻松完成大多数常见任务。 For example, changing the Display Folder of multiple measures at once is just a matter of selecting the objects in the explorer tree and then dragging and dropping them around. The right-click context menu of the explorer tree provides a convenient way to perform many of these tasks, such as adding/removing objects from perspectives, renaming multiple objects, etc.

There may be many other common workflow tasks, which are not as easily performed through the UI however. 因此，Tabular Editor 引入了高级脚本，让高级用户可以使用 C# 语法编写脚本，从而更直接地操作已加载的表格模型中的对象。

## 对象

[脚本 API](xref:api-index) 提供对两个顶层对象的访问：`Model` 和 `Selected`。 The former contains methods and properties that allow you to manipulate all objects in the Tabular Model, whereas the latter exposes only objects that are currently selected in the explorer tree.

`Model` 对象封装了 [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) 类，对外公开其部分属性，并额外提供一些方法和属性，以便更轻松地操作翻译、透视以及对象集合。 The same applies to any descendant objects, such as Table, Measure, Column, etc. which all have corresponding wrapper objects. Please see <xref:api-index> for a complete listing of objects, properties and methods in the Tabular Editor wrapper library.

The main advantage of working through this wrapper is, that all changes will be undoable from the Tabular Editor UI. Simply press CTRL+Z after executing a script, and you will see that all changes made by the script are immediately undone. Furthermore, the wrapper provides convenient methods that turn many common tasks into simple one-liners. We will provide some examples below. It is assumed that the reader is already somewhat familiar with C# and LINQ, as these aspects of Tabular Editors scripting capabilities will not be covered here. Users unfamiliar with C# and LINQ should still be able to follow the examples given below.

## 设置对象属性

如果你想更改某个特定对象的属性，显然最简单的方式就是直接在 UI 中操作。 But as an example, let us see how we could achieve the same thing through scripting.

假设你想更改 'FactInternetSales' 表中 [Sales Amount] 度量值的格式字符串。 If you locate the measure in the explorer tree, you can simply drag it onto the script editor. Tabular Editor will then generate the following code, which represents this particular measure in the Tabular Object Model:

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"]
```

再加一个点（.） after the right-most bracket, should make the autocomplete menu pop up, showing you which properties and methods exist on this particular measure. Simply choose "FormatString" in the menu, or write the first few letters and hit Tab. Then, enter an equal sign followed by "0.0%". Let us also change the Display Folder of this measure. Your final code should look like this:

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"].FormatString = "0.0%";
Model.Tables["FactInternetSales"].Measures["Sales Amount"].DisplayFolder = "New Folder";
```

**Note:** Remember to put the semicolon (;) at the end of each line. This is a requirement of C#. If you forget it, you will get a syntax error message when trying to execute the script.

Hit F5 or the "Play" button above the script editor to execute the script. Immediately, you should see the measure moving around in the explorer tree, reflecting the changed Display Folder. If you examine the measure in the Property Grid, you should also see that the Format String property has changed accordingly.

### 同时处理多个对象

Many objects in the object model, are actually collections of multiple objects. For example, each Table object has a Measures collection. The wrapper exposes a series of convenient properties and methods on these collections, to make it easy to set the same property on multiple objects at once. This is described in detail below. Additionally, you may use all the standard LINQ extension methods to filter and browse the objects of a collection.

下面是一些最常用的 LINQ 扩展方法示例：

- `Collection.First([predicate])` 返回集合中第一个满足可选 [predicate] 条件的对象。
- `Collection.Any([predicate])` 如果集合包含任意对象（可选：满足 [predicate] 条件），则返回 true。
- `Collection.Where(predicate)` 返回按 predicate 条件筛选后的集合。
- `Collection.Select(map)` 按照指定的 map，将集合中的每个对象投影为另一个对象。
- `Collection.ForEach(action)` 对集合中的每个元素执行指定的 action。

在上面的示例中，`predicate` 是一个 lambda 表达式：它以单个对象作为输入，并返回一个布尔值作为输出。 For example, if `Collection` is a collection of measures, a typical `predicate` could look like:

`m => m.Name.Contains("Reseller")`

仅当该度量值的 Name 属性包含字符串 "Reseller" 时，此 predicate 才会返回 true。 Wrap the expression in curly braces and use the `return` keyword, if you need more advanced logic:

```csharp
.Where(obj => {
    if(obj is Column) {
        return false;
    }
    return obj.Name.Contains("test");
})
```

回到上面的示例，`map` 是一个 lambda 表达式：它以单个对象作为输入，并返回一个对象作为输出。 `action` is a lambda expression that takes a single object as input, but does not return any value.

使用高级脚本编辑器的 IntelliSense 功能查看还有哪些 LINQ 方法，或参考 [LINQ-to-Objects 文档](https://msdn.microsoft.com/en-us/library/9eekhta0.aspx)。

## 使用 **Model** 对象

要快速引用当前加载的表格模型中的任意对象，可以将该对象从资源管理器树状视图拖放到高级脚本编辑器中：

![Dragging and dropping an object into the Advanced Scripting editor](~/content/assets/images/advanced-scripting-01.gif)

如需了解 Model 及其后代对象包含哪些属性，请参阅 [TOM 文档](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx)。 Additionally, refer to <xref:api-index> for a complete listing of the properties and methods exposed by the wrapper object.

## 使用 **Selected** 对象

在某些工作流中，能够显式引用表格模型中的任意对象非常方便；但有时你希望从资源管理器树中挑选一批对象，然后仅对所选对象执行脚本。 This is where the `Selected` object comes in handy.

The `Selected` object provides a range of properties that make it easy to identify what is currently selected, as well as limiting the selection to objects of a particular type. When browsing with Display Folders, and one or more folders are selected in the explorer tree, all their child items are considered to be selected as well.
For single selections, use the singular name for the type of object you want to access. For example,

`Selected.Hierarchy`

它指的是树中当前选中的层次结构，但前提是必须且只能选中一个层次结构。 Use the plural type name, in case you want to work with multiselections:

`Selected.Hierarchies`

All properties that exist on the singular object, also exist on its plural form, with a few exceptions. This means that you can set the value of these properties for multiple objects at once, with just one line of code and without using the LINQ extension methods mentioned above. For example, say you wanted to move all currently selected measures into a new Display Folder called "Test":

`Selected.Measures.DisplayFolder = "Test";`

If no measures are currently selected in the tree, the above code does nothing, and no error is raised. Otherwise, the DisplayFolder property will be set to "Test" on all selected measures (even measures residing within folders, as the `Selected` object also includes objects in selected folders). If you use the singular form `Measure` instead of `Measures`, you will get an error unless the current selection contains exactly one measure.

Although we cannot set the Name property of multiple objects at once, we still have some options available. 如果你只是想把某个字符串的所有出现位置替换成另一个字符串，可以使用提供的“Rename”方法，如下所示：

```csharp
Selected.Measures
        .Rename("Amount", "Value");
```

这会将当前选中的所有度量值名称中的“Amount”全部替换为“Value”。
Alternatively, we may use the LINQ ForEach()-method, as described above, to include more advanced logic:

```csharp
Selected.Measures
        .ForEach(m => { if(m.Name.Contains("Reseller")) m.Name += " DEPRECATED"; });
```

This example will append the text " DEPRECATED" to the names of all selected measures where the names contain the word "Reseller". 另外，你也可以在应用 `ForEach()` 操作之前，先用 LINQ 扩展方法 `Where()` 过滤集合，这将得到完全相同的结果：

```csharp
Selected.Measures
        .Where(m => m.Name.Contains("Reseller"))
        .ForEach(m => m.Name += " DEPRECATED");
```

## 辅助方法

To make debugging scripts easier, Tabular Editor provides a set of special helper methods. Internally, these are static methods decorated with the `[ScriptMethod]`-attribute. This attribute allows scripts to call the methods directly, without the need to specify a namespace or class name. Plugins may also use the `[ScriptMethod]` attribute to expose public static methods for scripting in a similar way.

Some of them may be invoked as extension methods, so `object.Output();` and `Output(object);` are equivalent.

The ones you will reach for most often are `Output()` for inspecting an object mid-script, `Info()`, `Warning()` and `Error()` for messages, `SaveFile()` and `ReadFile()` for text data, and `ExportProperties()` / `ImportProperties()` for moving property values in and out as TSV.

@script-helper-methods is the maintained list of every helper method with its full signature. Use it rather than the summary here.

### 调试脚本

如上所述，你可以使用 `Output(object);` 方法来暂停脚本执行，并打开一个对话框来显示传入对象的信息。 You can also use this method as an extension method, invoking it as `object.Output();`. The script is resumed when the dialog is closed.

根据输出对象的类型，对话框会以下面四种方式之一显示：

- 单个对象（例如 string、int 和 DateTime，但不包括派生自 TabularNamedObject 的任何对象）会通过对该对象调用 `.ToString()` 方法，以简单的信息对话框形式显示：

![image](~/content/assets/images/advanced-scripting-02.png)

- 单个 TabularNamedObject（例如表、度量值，或 Tabular Editor 中提供的任何其他 TOM NamedMetadataObject）会显示在属性网格中，类似于在 Tree Explorer 中选中对象时的效果。 Properties on the object may be edited in the grid, but note that if an error is encountered at a later point in the script execution, the edit will be automatically undone, if "Rollback on error" is enabled:

![image](~/content/assets/images/advanced-scripting-03.png)

- 任何对象的 IEnumerable（不包括 TabularNamedObject）都会以列表形式显示；列表中的每一项都会显示该 IEnumerable 中对象的 `.ToString()` 值及其类型：

![image](~/content/assets/images/advanced-scripting-04.png)

- 任何 TabularNamedObject 的 IEnumerable 都会使对话框左侧显示对象列表，右侧显示属性网格。 The Property Grid will be populated from whatever object is selected in the list, and properties may be edited just as when a single TabularNamedObject is being output:

![image](~/content/assets/images/advanced-scripting-05.png)

你可以勾选左下角的“不再显示更多输出”复选框，以防脚本在后续任何 `.Output()` 调用时暂停。

## .NET 引用

Scripts support the `using` keyword to shorten class names, just as regular C# source does, and can pull in external assemblies with `#r "<assembly name or DLL path>"`, the same syntax `.csx` scripts use.

例如，下面的脚本现在将按预期工作：

```csharp
// Assembly references must be at the very top of the file:
#r "System.IO.Compression"

// Using keywords must come before any other statements:
using System.IO.Compression;
using System.IO;

var xyz = 123;

// Using statements still work the way they're supposed to:
using(var data = new MemoryStream())
using(var zip = new ZipArchive(data, ZipArchiveMode.Create)) 
{
   // ...
}
```

默认情况下，为了便于完成常见任务，Tabular Editor 会自动添加以下 `using` 指令（即使脚本中未显式声明）：

```csharp
using System;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json;
using TabularEditor.TOMWrapper;
using TabularEditor.TOMWrapper.Utils;
using TabularEditor.UI;
```

此外，默认还会加载以下 .NET Framework 程序集：

- System.Dll
- System.Core.Dll
- System.Data.Dll
- System.Windows.Forms.Dll
- Microsoft.Csharp.Dll
- Newtonsoft.Json.Dll
- TomWrapper.Dll
- TabularEditor.Exe
- Microsoft.AnalysisServices.Tabular.Dll

## 使用 Roslyn 进行编译

> [!NOTE]
> This section applies to **Tabular Editor 2 only**. Tabular Editor 3 compiles scripts with Roslyn natively, so newer C# language features are available with no setup and there is no compiler path to configure.

Tabular Editor 2 compiles scripts with the C# compiler that ships with .NET Framework, which supports C# 5. To use later language features such as string interpolation, point it at a Roslyn compiler instead, under **File > Preferences > General**. Specify the directory holding the compiler executable (`csc.exe`) and the language version to pass to it:

![image](~/content/assets/images/advanced-scripting-06.png)

### Visual Studio 2017

对于典型的 Visual Studio 2017 Enterprise 安装，Roslyn 编译器位于此处：

```
c:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\MSBuild\15.0\Bin\Roslyn
```

默认包含 C# 6.0 的语言特性。

![image](~/content/assets/images/advanced-scripting-07.png)

### Visual Studio 2019

对于典型的 Visual Studio 2019 Community 安装，Roslyn 编译器位于：

```
c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\Roslyn
```

VS2019 随附的编译器支持 C# 8.0 语言特性，可通过在编译器选项中指定以下内容来启用：

```
-langversion:8.0
```

### Visual Studio 2022

对于典型的 Visual Studio 2022 **Community Edition** 安装，Roslyn 编译器位于：

```
C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\Roslyn\csc.exe
```

如果你使用的是 Visual Studio 2022 的其他版本，路径可能会略有不同。 For example, for the **Enterprise Edition**, it is located here:

```
C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\Roslyn
```

VS2022 最新更新随附的编译器支持 [C# 12.0 语言特性](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-12)，可通过在编译器选项中指定以下内容来启用：

```
-langversion:12.0
```
