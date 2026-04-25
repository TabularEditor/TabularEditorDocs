---
uid: advanced-scripting
title: 高级脚本
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 高级脚本

本文将介绍 Tabular Editor 的高级脚本功能。 本文档中的信息可能会更改。 另外，也别忘了查看我们的脚本库 @csharp-script-library，里面有更多贴近实际的示例，帮助你了解如何利用 Tabular Editor 的脚本功能完成各种任务。

## 什么是高级脚本？

Tabular Editor 的界面旨在让你在构建表格模型时，轻松完成大多数常见任务。 例如，要一次性更改多个度量值的显示文件夹，只需在资源管理器树中选中这些对象，然后拖放到目标位置即可。 资源管理器树的右键快捷菜单也提供了便捷方式，可完成许多此类任务，例如将对象添加到透视或从透视中移除、批量重命名对象等。

不过，还有很多常见的工作流任务并不容易通过 UI 来完成。 因此，Tabular Editor 引入了高级脚本，让高级用户可以使用 C# 语法编写脚本，从而更直接地操作已加载的表格模型中的对象。

## 对象

[脚本 API](xref:api-index) 提供对两个顶层对象的访问：`Model` 和 `Selected`。 前者包含可用于操作表格模型中所有对象的方法和属性；后者则只公开资源管理器树中当前所选的对象。

`Model` 对象封装了 [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) 类，对外公开其部分属性，并额外提供一些方法和属性，以便更轻松地操作翻译、透视以及对象集合。 其所有后代对象同样如此，例如 Table、度量值、Column 等，都有对应的封装对象。 Tabular Editor 封装库中对象、属性和方法的完整列表，请参阅 <xref:api-index>。

通过该封装层进行操作的主要优势是：所有更改都可以在 Tabular Editor UI 中撤销。 脚本执行后只需按 CTRL+Z，你就会看到脚本所做的所有更改会立刻被撤销。 此外，该封装还提供了便捷方法，可将许多常见任务简化为一行代码。 下面我们会给出一些示例。 我们假设读者已对 C# 和 LINQ 有一定了解，因此本文不会介绍这些内容；Tabular Editor 脚本功能中与之相关的部分也不在本文范围内。 即使你不熟悉 C# 和 LINQ，也应该能看懂下面的示例。

## 设置对象属性

如果你想更改某个特定对象的属性，显然最简单的方式就是直接在 UI 中操作。 不过作为示例，我们来看一下如何通过脚本实现同样的效果。

假设你想更改 'FactInternetSales' 表中 [Sales Amount] 度量值的格式字符串。 在资源管理器树中找到该度量值后，你只需将其拖到脚本编辑器中即可。 接着，Tabular Editor 会生成下面这段代码，用来在 Tabular Object Model 中表示这个特定的度量值：

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"]
```

再输入一个点（.） 在最右侧的方括号后输入英文句点“.”，会弹出自动补全菜单，显示该度量值有哪些属性和方法。 在菜单中直接选择 "FormatString"，或者输入前几个字母后按 Tab。 然后输入等号 =，再输入 "0.0%"。 我们也把该度量值的显示文件夹一并改一下。 你的最终代码应如下所示：

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"].FormatString = "0.0%";
Model.Tables["FactInternetSales"].Measures["Sales Amount"].DisplayFolder = "New Folder";
```

**注意：** 记得在每行末尾加上分号（;）。 这是 C# 的要求。 如果忘了加，执行脚本时会出现语法错误信息。

按下 F5，或点击脚本编辑器上方的“播放”按钮来执行脚本。 你会立刻看到该度量值在资源管理器树中移动位置，以反映显示文件夹的更改。 如果你在属性网格中查看该度量值，也会看到格式字符串属性已相应更新。

### 同时处理多个对象

对象模型中的许多对象，其实都是由多个对象组成的集合。 例如，每个 Table 对象都有一个度量值集合。 该包装器为这些集合提供了一系列便捷的属性和方法，方便你一次性为多个对象设置同一个属性。 下面会详细说明。 此外，你还可以使用所有标准的 LINQ 扩展方法来筛选和浏览集合中的对象。

下面是一些最常用的 LINQ 扩展方法示例：

- `Collection.First([predicate])` 返回集合中第一个满足可选 [predicate] 条件的对象。
- `Collection.Any([predicate])` 如果集合包含任意对象（可选：满足 [predicate] 条件），则返回 true。
- `Collection.Where(predicate)` 返回按 predicate 条件筛选后的集合。
- `Collection.Select(map)` 按照指定的 map，将集合中的每个对象投影为另一个对象。
- `Collection.ForEach(action)` 对集合中的每个元素执行指定的 action。

在上面的示例中，`predicate` 是一个 lambda 表达式：它以单个对象作为输入，并返回一个布尔值作为输出。 例如，如果 `Collection` 是一个度量值的集合，一个典型的 `predicate` 可能如下所示：

`m => m.Name.Contains("Reseller")`

仅当该度量值的 Name 属性包含字符串 "Reseller" 时，此 predicate 才会返回 true。 如果你需要更复杂的逻辑，可以用大括号将表达式括起来，并使用 `return` 关键字：

```csharp
.Where(obj => {
    if(obj is Column) {
        return false;
    }
    return obj.Name.Contains("test");
})
```

回到上面的示例，`map` 是一个 lambda 表达式：它以单个对象作为输入，并返回一个对象作为输出。 `action` 是一个 lambda 表达式：它以单个对象作为输入，但不返回任何值。

使用高级脚本编辑器的 IntelliSense 功能查看还有哪些 LINQ 方法，或参考 [LINQ-to-Objects 文档](https://msdn.microsoft.com/en-us/library/9eekhta0.aspx)。

## 使用 **Model** 对象

要快速引用当前加载的表格模型中的任意对象，可以将该对象从资源管理器树状视图拖放到高级脚本编辑器中：

![将对象拖放到高级脚本编辑器中](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/DragDropTOM.gif)

如需了解 Model 及其后代对象包含哪些属性，请参阅 [TOM 文档](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx)。 另外，你也可以查看 <xref:api-index>，获取这个包装对象公开的属性和方法的完整列表。

## 使用 **Selected** 对象

在某些工作流中，能够显式引用表格模型中的任意对象非常方便；但有时你希望从资源管理器树中挑选一批对象，然后仅对所选对象执行脚本。 这时 `Selected` 对象就派上用场了。

`Selected` 对象提供了一系列属性，便于你识别当前选中了什么，同时还能将选择范围限定为某一特定类型的对象。 在使用显示文件夹浏览时，如果在资源管理器树中选中了一个或多个文件夹，这些文件夹下的所有子项也会被视为已选中。
对于单个对象的选择，请使用要访问的对象类型的单数名称。 例如，

`Selected.Hierarchy`

它指的是树中当前选中的层次结构，但前提是必须且只能选中一个层次结构。 如果你想处理多选，请使用该类型名称的复数形式：

`Selected.Hierarchies`

单数形式对象具备的属性，复数形式也同样具备，只有少数例外。 这意味着你可以用一行代码一次性为多个对象设置这些属性值，而无需使用上面提到的 LINQ 扩展方法。 例如，假设你想把当前选中的所有度量值移动到一个名为 "Test" 的新显示文件夹中：

`Selected.Measures.DisplayFolder = "Test";`

如果树中当前没选中任何度量值，上面的代码什么也不做，也不会引发错误。 否则，所有选中度量值的 DisplayFolder 属性都会被设置为 "Test"（即使这些度量值位于显示文件夹内也一样，因为 `Selected` 对象也会包含所选显示文件夹中的对象）。 如果你使用单数形式的 `Measure` 而不是 `Measures`，除非当前选择中恰好只有一个度量值，否则会报错。

虽然我们无法一次性设置多个对象的 Name 属性，但仍然有一些可选方案。 如果你只是想把某个字符串的所有出现位置替换成另一个字符串，可以使用提供的“Rename”方法，如下所示：

```csharp
Selected.Measures
        .Rename("Amount", "Value");
```

这会将当前选中的所有度量值名称中的“Amount”全部替换为“Value”。
或者，我们也可以使用上面介绍的 LINQ ForEach() 方法，以便加入更复杂的逻辑：

```csharp
Selected.Measures
        .ForEach(m => if(m.Name.Contains("Reseller")) m.Name += " DEPRECATED");
```

此示例会在所有选中且名称包含 "Reseller" 的度量值名称后追加文本 " DEPRECATED"。 另外，你也可以在应用 `ForEach()` 操作之前，先用 LINQ 扩展方法 `Where()` 过滤集合，这将得到完全相同的结果：

```csharp
Selected.Measures
        .Where(m => m.Name.Contains("Reseller"))
        .ForEach(m => m.Name += " DEPRECATED");
```

<a name="helper-methods"></a>

## 辅助方法

为了让脚本调试更容易，Tabular Editor 提供了一组特殊的辅助方法。 从内部实现来看，这些是用 `[ScriptMethod]` 特性修饰的静态方法。 该特性允许脚本直接调用这些方法，无需指定命名空间或类名。 插件也可以使用 `[ScriptMethod]` 特性，以类似方式将公共静态方法公开给脚本调用。

从 2.7.4 起，Tabular Editor 提供以下脚本方法。 注意，其中一些方法也可以作为扩展方法来调用。 例如，`object.Output();` 与 `Output(object);` 是等价的。

- `Output(object);` - 在弹出对话框中显示指定对象或对象集合的详细信息。 通过 UI 执行时，用户可以选择忽略后续弹窗。 通过 CLI 执行时，信息会输出到控制台。
- `SaveFile(filePath, content);` - 将文本数据保存到文件的便捷方式。
- `ReadFile(filePath);` - 从文件加载文本数据的便捷方式。
- `ExportProperties(objects, properties);` - 将多个对象的一组属性导出为 TSV 字符串的便捷方式。
- `ImportProperties(tsvData);` - 从 TSV 字符串将属性导入到多个对象中的便捷方式。
- `CustomAction(name);` - 按名称调用自定义操作。
- `CustomAction(objects, name);` - 在指定对象上调用自定义操作。
- `ConvertDax(dax, useSemicolons);` - 在 US/UK 与非 US/UK 区域设置之间转换 DAX 表达式。 如果 `useSemicolons` 为 true（默认值），则会将 `dax` 字符串从 US/UK 的本地格式转换为非 US/UK 格式。 也就是说，逗号（列表分隔符）会转换为分号，句点（小数分隔符）会转换为逗号。 如果将 `useSemicolons` 设为 false，则相反。
- `FormatDax(IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - 格式化所提供集合中所有对象上的 DAX 表达式
- `FormatDax(IDaxDependantObject obj)` - 将对象加入 DAX 表达式格式化队列；在脚本执行完成后，或调用 `CallDaxFormatter` 方法时执行格式化。
- `CallDaxFormatter(bool shortFormat, bool? skipSpace)` - 格式化截至目前已入队的对象上的所有 DAX 表达式
- `Info(string);` - 在弹出对话框中显示一条信息。 当脚本在 CLI 中运行时，控制台会输出一条信息。
- `Warning(string);` - 在弹出对话框中显示一条警告信息。 当脚本在 CLI 中运行时，控制台会输出一条警告信息。
- `Error(string);` - 在弹出对话框中显示一条错误信息。 当脚本在 CLI 中运行时，控制台会输出一条错误信息。

你可以在[这里](xref:script-helper-methods)查看所有辅助方法的最新列表。

### 调试脚本

如上所述，你可以使用 `Output(object);` 方法来暂停脚本执行，并打开一个对话框来显示传入对象的信息。 你也可以将此方法作为扩展方法使用，通过 `object.Output();` 来调用。 关闭对话框后，脚本会继续执行。

根据输出对象的类型，对话框会以下面四种方式之一显示：

- 单个对象（例如 string、int 和 DateTime，但不包括派生自 TabularNamedObject 的任何对象）会通过对该对象调用 `.ToString()` 方法，以简单的信息对话框形式显示：

![image](https://user-images.githubusercontent.com/8976200/29941982-9917d0cc-8e94-11e7-9e78-24aaf11fd311.png)

- 单个 TabularNamedObject（例如表、度量值，或 Tabular Editor 中提供的任何其他 TOM NamedMetadataObject）会显示在属性网格中，类似于在 Tree Explorer 中选中对象时的效果。 你可以在网格中编辑对象的属性。但请注意：如果在脚本后续执行过程中遇到错误，且启用了“出错时回滚”，这些更改会自动撤销：

![image](https://user-images.githubusercontent.com/8976200/29941852-2acc9846-8e94-11e7-9380-f84fef26a78c.png)

- 任何对象的 IEnumerable（不包括 TabularNamedObject）都会以列表形式显示；列表中的每一项都会显示该 IEnumerable 中对象的 `.ToString()` 值及其类型：

![image](https://user-images.githubusercontent.com/8976200/29942113-02dad928-8e95-11e7-9c04-5bb87b396f3f.png)

- 任何 TabularNamedObject 的 IEnumerable 都会使对话框左侧显示对象列表，右侧显示属性网格。 属性网格会根据列表中当前选中的对象进行填充；你也可以像输出单个 TabularNamedObject 时一样编辑其属性：

![image](https://user-images.githubusercontent.com/8976200/29942190-498cbb5c-8e95-11e7-8455-32750767cf13.png)

你可以勾选左下角的“不再显示更多输出”复选框，以防脚本在后续任何 `.Output()` 调用时暂停。

## .NET 引用

[Tabular Editor 2.8.6 版本](https://github.com/TabularEditor/TabularEditor/tree/2.8.6)会让编写复杂脚本变得容易多了。 得益于新的预处理器，你现在可以像在常规 C# 源代码中一样使用 `using` 关键字来缩短类名等。 此外，你还可以像在 Azure Functions 使用的 .csx 脚本那样，使用语法 `#r "<assembly name or DLL path>"` 引用外部程序集。

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

如果你更喜欢使用 Visual Studio 2017 引入的新 Roslyn 编译器来编译脚本，那么从 Tabular Editor 2.12.2 版本开始，你可以在“文件 > 偏好设置 > 常规”中进行配置。 这样你就可以使用更新的 C# 语言特性，比如字符串插值。 只需指定包含编译器可执行文件（`csc.exe`）的目录路径，并在编译器选项中指定语言版本：

![image](https://user-images.githubusercontent.com/8976200/92464140-0902f580-f1cd-11ea-998a-b6ecce57b399.png)

### Visual Studio 2017

对于典型的 Visual Studio 2017 Enterprise 安装，Roslyn 编译器位于此处：

```
c:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\MSBuild\15.0\Bin\Roslyn
```

默认包含 C# 6.0 的语言特性。

![image](https://user-images.githubusercontent.com/8976200/92464584-a52cfc80-f1cd-11ea-9b66-3b47ac36f6c6.png)

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

如果你使用的是 Visual Studio 2022 的其他版本，路径可能会略有不同。 例如，对于 **企业版**，路径位于：

```
C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\Roslyn
```

VS2022 最新更新随附的编译器支持 [C# 12.0 语言特性](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-12)，可通过在编译器选项中指定以下内容来启用：

```
-langversion:12.0
```
