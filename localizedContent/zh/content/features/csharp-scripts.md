---
uid: csharp-scripts
title: C# Script
author: Daniel Otykier
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      true: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
    - product: Tabular Editor CLI
      full: true
---

# C# Script

本文将介绍 Tabular Editor 3 的 C# Script 功能。 Information in this document is subject to change. 另外，也别忘了看看我们的脚本库 @csharp-script-library，里面有更多贴近实际场景的示例，展示了你可以如何利用 Tabular Editor 的脚本功能。

## 为什么要用 C# Script？

Tabular Editor 的界面旨在让你在构建表格模型时，轻松完成大多数常见任务。 For example, changing the Display Folder of multiple measures at once is just a matter of selecting the objects in the explorer tree and then dragging and dropping them around. The right-click context menu of the explorer tree provides a convenient way to perform many of these tasks, such as adding/removing objects from perspectives, renaming multiple objects, etc.

There may be many other common workflow tasks, which are not as easily performed through the UI however. For this reason, Tabular Editor offers C# scripting, which lets advanced users write a script using C# syntax, to more directly manipulate the objects in the loaded Tabular Model.

## Code Assist

C# Script 编辑器支持基于 Roslyn 的代码补全和调用提示；从 Tabular Editor 3.23.0 起，补全还支持子字符串匹配和大写首字母缩写匹配。

## 对象

[scripting API](xref:api-index) 提供对两个顶层对象的访问：`Model` 和 `Selected`。 The former contains methods and properties that allow you to manipulate all objects in the Tabular Model, whereas the latter exposes only objects that are currently selected in the explorer tree.

`Model` 对象是 [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) 类的封装，仅公开其部分属性，并额外提供一些方法和属性，方便对翻译、透视和对象集合进行操作。 The same applies to any descendant objects, such as Table, Measure, Column, etc. which all have corresponding wrapper objects. Please see <xref:api-index> for a complete listing of objects, properties and methods in the Tabular Editor wrapper library.

The main advantage of working through this wrapper is, that all changes will be undoable from the Tabular Editor UI. Simply press CTRL+Z after executing a script, and you will see that all changes made by the script are immediately undone. Furthermore, the wrapper provides convenient methods that turn many common tasks into simple one-liners. We will provide some examples below. It is assumed that the reader is already somewhat familiar with C# and LINQ, as these aspects of Tabular Editors scripting capabilities will not be covered here. Users unfamiliar with C# and LINQ should still be able to follow the examples given below.

## 设置对象属性

如果你只想更改某一个对象的某个属性，最简单的方式当然是直接在 UI 中操作。 But as an example, let us see how we could achieve the same thing through scripting.

假设你想修改 'FactInternetSales' 表中 [Sales Amount] 度量值的格式字符串。 If you locate the measure in the explorer tree, you can simply drag it onto the script editor. Tabular Editor will then generate the following code, which represents this particular measure in the Tabular Object Model:

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
- `Collection.Any([predicate])` 如果集合包含任何对象（可选：满足 [predicate] 条件），则返回 true。
- `Collection.Where(predicate)` 返回一个集合，该集合是按 predicate 条件从原集合筛选得到的。
- `Collection.Select(map)` 根据指定的 map，将集合中的每个对象投影为另一个对象。
- `Collection.ForEach(action)` 对集合中的每个元素执行指定的 action。

在上面的示例中，`predicate` 是一个 lambda 表达式：以单个对象作为输入，并返回一个布尔值作为输出。 For example, if `Collection` is a collection of measures, a typical `predicate` could look like:

`m => m.Name.Contains("Reseller")`

该 predicate 仅在度量值的 `Name` 包含字符串“Reseller”时才会返回 true。 Wrap the expression in curly braces and use the `return` keyword, if you need more advanced logic:

```csharp
.Where(obj => {
    if(obj is Column) {
        return false;
    }
    return obj.Name.Contains("test");
})
```

回到上面的示例，`map` 是一个 lambda 表达式：以单个对象作为输入，并返回任意单个对象作为输出。 `action` is a lambda expression that takes a single object as input, but does not return any value.

## 使用 **Model** 对象

要快速引用当前已加载的表格模型中的任意对象，你可以将该对象从资源管理器树拖放到 C# Script 编辑器中：

![将对象拖放到 C# Script 脚本编辑器中](~/content/assets/images/drag-object-to-script.gif)

可以参考 [TOM 文档](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx)，了解 Model 及其派生对象上有哪些属性。 Additionally, refer to <xref:api-index> for a complete listing of the properties and methods exposed by the wrapper object.

## 使用 **Selected** 对象

在某些工作流中，能够显式引用表格模型中的任何对象非常有用；但有时你希望从资源管理器树中挑选对象，然后只对所选对象执行脚本。 This is where the `Selected` object comes in handy.

The `Selected` object provides a range of properties that make it easy to identify what is currently selected, as well as limiting the selection to objects of a particular type. When browsing with Display Folders, and one or more folders are selected in the explorer tree, all their child items are considered to be selected as well.
For single selections, use the singular name for the type of object you want to access. For example,

`Selected.Hierarchy`

它指向树中当前选中的层次结构，前提是只选中了一个层次结构。 Use the plural type name, in case you want to work with multiselections:

`Selected.Hierarchies`

All properties that exist on the singular object, also exist on its plural form, with a few exceptions. This means that you can set the value of these properties for multiple objects at once, with just one line of code and without using the LINQ extension methods mentioned above. For example, say you wanted to move all currently selected measures into a new Display Folder called "Test":

`Selected.Measures.DisplayFolder = "Test";`

If no measures are currently selected in the tree, the above code does nothing, and no error is raised. Otherwise, the DisplayFolder property will be set to "Test" on all selected measures (even measures residing within folders, as the `Selected` object also includes objects in selected folders). If you use the singular form `Measure` instead of `Measures`, you will get an error unless the current selection contains exactly one measure.

Although we cannot set the Name property of multiple objects at once, we still have some options available. 如果只是想将某个字符串的所有匹配项替换为另一个字符串，可以使用提供的 "Rename" 方法，例如：

```csharp
Selected.Measures
        .Rename("Amount", "Value");
```

这会将当前所选所有度量值的名称中出现的“Amount”替换为“Value”。
Alternatively, we may use the LINQ ForEach()-method, as described above, to include more advanced logic:

```csharp
Selected.Measures
        .ForEach(m => if(m.Name.Contains("Reseller")) m.Name += " DEPRECATED");
```

This example will append the text " DEPRECATED" to the names of all selected measures where the names contain the word "Reseller". 或者，我们也可以先使用 LINQ 扩展方法 `Where()` 过滤集合，再应用 `ForEach()` 操作，得到的结果完全相同：

```csharp
Selected.Measures
        .Where(m => m.Name.Contains("Reseller"))
        .ForEach(m => m.Name += " DEPRECATED");
```

### Selected 访问器完整列表

The following table lists all available singular and plural accessors on the `Selected` object. Singular accessors throw a `SelectionException` if the current selection does not contain exactly one object of that type. Plural accessors return an empty collection if no objects of that type are selected.

| 单数                                  | 复数                                   | 对象类型    |
| ----------------------------------- | ------------------------------------ | ------- |
| `Selected.Measure`                  | `Selected.Measures`                  | 度量值     |
| `Selected.Column`                   | `Selected.Columns`                   | 所有列类型   |
| `Selected.DataColumn`               | `Selected.DataColumns`               | 数据列     |
| `Selected.CalculatedColumn`         | `Selected.CalculatedColumns`         | 计算列     |
| `Selected.CalculatedTableColumn`    | `Selected.CalculatedTableColumns`    | 计算表格列   |
| `Selected.Hierarchy`                | `Selected.Hierarchies`               | 层次结构    |
| `Selected.Level`                    | `Selected.Levels`                    | 层级      |
| `Selected.Table`                    | `Selected.Tables`                    | 表格      |
| `Selected.CalculatedTable`          | `Selected.CalculatedTables`          | 计算表格    |
| `Selected.Partition`                | `Selected.Partitions`                | 分区      |
| `Selected.Role`                     | `Selected.Roles`                     | 模型角色    |
| `Selected.TablePermission`          | `Selected.TablePermissions`          | 表格权限    |
| `Selected.KPI`                      | `Selected.KPIs`                      | KPI     |
| `Selected.Calendar`                 | `Selected.Calendars`                 | 日历      |
| `Selected.CalculationItem`          | `Selected.CalculationItems`          | 计算项     |
| `Selected.Function`                 | `Selected.Functions`                 | 用户自定义函数 |
| `Selected.DataSource`               | `Selected.DataSources`               | 数据源     |
| `Selected.SingleColumnRelationship` | `Selected.SingleColumnRelationships` | 关系      |
| `Selected.Perspective`              | `Selected.Perspectives`              | 透视      |
| `Selected.Culture`                  | `Selected.Cultures`                  | 翻译      |

> [!NOTE]
> 在 Tabular Editor 3.26.0 中，新增了 角色、KPI、日历、计算项、表权限、函数、数据源、单列关系、计算列、计算表列、数据列、计算表和分区的访问器。

Starting with Tabular Editor 3.27.0, objects that were deleted since the model was last saved remain visible in the TOM Explorer, and can be selected. Such objects are not part of the model, so they never appear in the accessors above. Instead, `Selected.Deleted` lists the selected deleted objects, each with a `Name`, `ObjectType`, `Parent` and a `Restore()` method. `Selected.Deleted.Restore()` restores all of them at once. Model objects also expose `HasUnsavedChanges` and `Revert()`, which let a script roll back part of a model. See @unsaved-changes for details.

## 辅助方法

Tabular Editor 提供了一组专用的辅助方法，便于完成某些脚本任务。 Note that some of these may be invoked as extension methods. For example, `object.Output();` and `Output(object);` are equivalent.

- `void Output(object value)` - 停止脚本执行，并显示所提供对象的信息。 When the script is running as part of a command line execution, this will write a string representation of the object to the console.
- `void SaveFile(string filePath, string content)` - 将文本数据保存到文件的便捷方式。
- `string ReadFile(string filePath)` - 从文件加载文本数据的便捷方式。
- `string ExportProperties(IEnumerable<ITabularNamedObject> objects, string properties)` - 便捷地将多个对象的一组属性导出为 TSV 字符串。
- `void ImportProperties(string tsvData)` - 将 TSV 字符串中的属性导入多个对象的便捷方式。
- `void CustomAction(string name)` - 按名称调用宏。
- `void CustomAction(this IEnumerable<ITabularNamedObject> objects, string name)` - 对指定对象调用宏。
- `string ConvertDax(string dax, bool useSemicolons)` - 在美/英区域设置与非美/英区域设置之间相互转换 DAX 表达式。 If `useSemicolons` is true (default) the `dax` string is converted from the native US/UK format to non-US/UK. That is, commas (list separators) will be converted to semicolons and periods (decimal separators) will be converted to commas. Vice versa if `useSemicolons` is set to false.
- `void FormatDax(this IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - 格式化所提供集合中所有对象上的 DAX 表达式
- `void FormatDax(this IDaxDependantObject obj)` - 将对象加入队列，在脚本执行完成时，或调用 `CallDaxFormatter` 方法时，对其 DAX 表达式进行格式化。
- `void CallDaxFormatter(bool shortFormat, bool? skipSpace)` - 格式化截至目前已入队的对象上的所有 DAX 表达式
- `void Info(string)` - 将一条提示信息输出到控制台（仅当脚本在命令行执行过程中运行时）。
- `void Warning(string)` - 将一条警告信息输出到控制台（仅当脚本在命令行执行过程中运行时）。
- `void Error(string)` - 将一条错误信息输出到控制台（仅当脚本在命令行执行过程中运行时）。
- `T SelectObject(this IEnumerable<T> objects, T preselect = null, string label = "Select object") where T: TabularNamedObject` - 向用户显示一个对话框，提示其从指定对象中选择一个。 If the user cancels the dialog, this method returns null.
- `void CollectVertiPaqAnalyzerStats()` - 如果 Tabular Editor 已连接到 Analysis Services 实例，则会运行 VertiPaq分析器统计信息收集器。
- `long GetCardinality(this Column column)` - 如果当前模型有可用的 VertiPaq分析器统计信息，此方法将返回指定列的基数。

有关可用帮助方法及其语法的完整列表，请参阅 @script-helper-methods。

### 调试脚本

如上所述，你可以使用 `Output(object);` 方法来暂停脚本执行，并打开一个对话框来显示传入对象的信息。 You can also use this method as an extension method, invoking it as `object.Output();`. The script is resumed when the dialog is closed.

根据输出对象的类型，对话框会以下面四种方式之一显示：

- 单个对象（例如 string、int 和 DateTime，但不包括派生自 TabularNamedObject 的任何对象）会通过对该对象调用 `.ToString()` 方法，以简单的信息对话框形式显示：

![C-sharp Output](~/content/assets/images/c-sharp-script-output-function.png)

- 单个 TabularNamedObject（例如表、度量值，或 Tabular Editor 中提供的任何其他 TOM NamedMetadataObject）会显示在属性网格中，类似于在 Tree Explorer 中选中对象时的效果。 Properties on the object may be edited in the grid, but note that if an error is encountered at a later point in the script execution, the edit will be automatically undone, if "Auto-Rollback" is enabled:

![C-sharp Output](~/content/assets/images/c-sharp-script-auto-rollback.png)

- 任何对象的 IEnumerable（不包括 TabularNamedObject）都会以列表形式显示；列表中的每一项都会显示该 IEnumerable 中对象的 `.ToString()` 值及其类型：

![C-sharp Output](~/content/assets/images/c-sharp-script-output-to-string-function.png)

- 任何 TabularNamedObject 的 IEnumerable 都会使对话框左侧显示对象列表，右侧显示属性网格。 The Property Grid will be populated from whatever object is selected in the list, and properties may be edited just as when a single TabularNamedObject is being output:

![C-sharp Output](~/content/assets/images/c-sharp-script-output-function-enumerated.png)

你可以勾选左下角的“不再显示更多输出”复选框，以防脚本在后续任何 `.Output()` 调用时暂停。

## 以预览方式运行 C# Script

**带预览运行**操作允许你在提交之前，预览 C# Script 对模型元数据所做的所有更改。 This is useful when running unfamiliar scripts or performing bulk modifications.

要使用此功能，在工具栏或菜单中点击 **脚本 > 带预览运行**。 The workflow is:

1. Tabular Editor 会在执行前为模型元数据创建快照
2. 脚本将运行直至完成
3. Tabular Editor 会将当前模型的元数据状态与执行前创建的快照进行比较
4. 如果检测到更改，将弹出预览对话框，以并排的分层差异视图显示模型（执行前与执行后）
5. 更改采用颜色区分：绿色表示新增对象，红色表示已删除对象，橙色表示已修改的属性
6. 使用 **仅显示更改** 复选框隐藏未更改的项目，将注意力集中在脚本更改的内容上
7. 单击 **确定** 以接受更改，或单击 **还原** 以撤销所有更改

![脚本预览 - 模型更改](~/content/assets/images/c-sharp-script-preview-changes.png)

如果脚本失败（编译或运行时错误），所有模型元数据更改都会自动回滚，并且不会显示预览对话框。 If the script succeeds but makes no detectable metadata changes, an informational message is displayed instead.

All model metadata changes from a script execution are wrapped in a single undo transaction. Even after accepting changes through the preview dialog, you can still undo the entire operation with **Ctrl+Z**.

> [!IMPORTANT]
> The preview and undo features only apply to model metadata changes. If a script performs external operations such as writing to files, databases or making web requests, those operations are executed immediately and cannot be reverted. The preview dialog does not attempt to analyze the script code — it works by comparing the model metadata state before and after execution.

> [!TIP]
> The [AI Assistant](xref:ai-assistant) shows this dialog when it runs a script itself, as long as **Preview changes** is on under **Tools > Preferences > AI Features > AI Assistant**. It is on by default, so you always get a chance to review AI-generated model changes before they are applied.

> [!NOTE]
> The preview dialog does not apply to a script run by an agent over the [MCP server](xref:mcp-server). Those scripts are compiled, checked by the safety analysis and run against the model atomically. The agent gets back a structured summary of what changed, and the changes are marked in the [TOM Explorer and the Properties view](xref:unsaved-changes) for you to review or revert afterwards.

## .NET 引用

You can use the `using` keyword to shorten class names, etc. just like in regular C# source code. 此外，你还可以使用语法 `#r "<assembly name or DLL path>"` 来包含外部程序集，方式与 Azure Functions 中使用的 .csx 脚本类似。

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

## 访问环境变量

通过 Tabular Editor CLI 运行 C# Script 时（尤其是在 CI/CD 流水线中），可以使用环境变量向脚本传递参数。 This is the recommended approach, as C# scripts executed by Tabular Editor CLI don't support traditional command-line arguments.

> [!NOTE]
> `Environment` is one of the types refused when an administrator has set the `BlockUnsafeScripts` policy. See [Administrator policies](#administrator-policies).

### 读取环境变量

在脚本中使用 `Environment.GetEnvironmentVariable()` 方法读取环境变量：

```csharp
// Read environment variables
var serverName = Environment.GetEnvironmentVariable("SERVER_NAME");
var environment = Environment.GetEnvironmentVariable("ENVIRONMENT");

// Use them in your script
foreach(var dataSource in Model.DataSources.OfType<ProviderDataSource>())
{
    if(dataSource.Name == "SQLDW")
    {
        dataSource.ConnectionString = dataSource.ConnectionString
            .Replace("{SERVER}", serverName)
            .Replace("{ENV}", environment);
    }
}

Info($"Updated connection strings for {environment} environment");
```

### Azure DevOps 集成

环境变量可与 Azure DevOps 流水线无缝集成，因为默认情况下，所有流水线变量都会自动作为环境变量提供。

**Azure DevOps YAML 流水线示例：**

```yaml
variables:
  targetServer: 'Production'
  targetDatabase: 'AdventureWorks'

steps:
- task: PowerShell@2
  displayName: 'Deploy Model with Parameters'
  env:
    SERVER_NAME: $(targetServer)
    DATABASE_NAME: $(targetDatabase)
  inputs:
    targetType: 'inline'
    script: |
      TabularEditor.exe "Model.bim" -S "DeploymentScript.csx" -D "$(targetServer)" "$(targetDatabase)" -O -V -E -W
```

在此示例中，脚本 `DeploymentScript.csx` 可以通过 `Environment.GetEnvironmentVariable()` 访问 `SERVER_NAME` 和 `DATABASE_NAME`。

### 常见使用场景

环境变量尤其适用于：

- **动态连接字符串**：根据部署环境（Dev、UAT、Production）更新数据源连接
- **条件逻辑**：根据目标环境应用不同的转换
- **部署配置**：基于参数控制要部署或修改的对象
- **多环境支持**：在不同环境中复用同一脚本，只需使用不同的值

**示例——按环境修改：**

```csharp
var environment = Environment.GetEnvironmentVariable("DEPLOY_ENV") ?? "Development";
var refreshPolicy = Environment.GetEnvironmentVariable("ENABLE_REFRESH_POLICY") == "true";

// Apply environment-specific settings
foreach(var table in Model.Tables)
{
    if(environment == "Production" && !refreshPolicy)
    {
        // Disable incremental refresh policies in production if specified
        table.EnableRefreshPolicy = false;
    }
}

Info($"Configured model for {environment} environment");
```

## Administrator policies

Scripting can be governed centrally, so what a script may do on your own machine is not always what it may do on a machine your IT department manages. Two [policies](xref:policies) decide that.

`DisableCSharpScripts` turns scripting off outright: scripts cannot be created or executed, and the same goes for macros under `DisableMacros`.

`BlockUnsafeScripts` is the middle ground, and the one worth understanding as a script author. Scripts and macros keep working, but only where they stay within the semantic model. A script that reads or writes a file, makes a web request, starts another program, references an outside assembly with `#r`, or sends a command straight to the server is refused before any of it runs.

### What counts as staying within the model

The decision is made by analyzing the compiled script, not by searching its text, so an indirect route to the same place is refused too: reflection through `Type.GetType` or `InvokeMember`, expression trees and delegate invocation, `Activator`, `AppDomain`, `Environment`, XML readers and writers that take a path or a URL, and type-name-based deserialization.

Among the [helper methods](xref:script-helper-methods), the three that write outside the model count as unsafe:

| Refused                                       | Still available                                                              |
| --------------------------------------------- | ---------------------------------------------------------------------------- |
| `SaveFile`, `ExecuteCommand`, `Bpa.ExportCsv` | `ReadFile`, `ExecuteDax`, `EvaluateDax`, `ExecuteReader`, `ExportProperties` |

Everything in the TOM object model is fine, as are `System`, `System.Linq`, `System.Collections.Generic` and `Newtonsoft.Json`. In practice a script that builds and changes model objects is unaffected, and a script that exports something to disk is not.

### What you see when a script is refused

A **Script not run** dialog names the policy and what the script used, and the status bar reads _Script blocked by your organization's policy_. The error list stays empty, because this is not a compile error: the script is valid, it is just not allowed to run here. **Run with preview** behaves the same way and shows no preview dialog.

A macro is analyzed when it is saved. Saving succeeds, and a dialog tells you the macro is saved but will not run. A blocked macro is left out of every menu, so it cannot be run by accident, and appears under **View > Macros** with its **Blocked** column filled in. Edit it back inside the line and its menu item returns, without restarting Tabular Editor.

On the command line, `te script`, `te macro run` and `te bpa run --fix` refuse in the same way, exit with a non-zero code and report `blockedByPolicy` in JSON output.

> [!NOTE]
> `BlockUnsafeScripts` requires Tabular Editor 3 Enterprise Edition. If the value is set on a copy that is not licensed for it, no script or macro runs at all, safe or not, until an Enterprise license is activated. The Tabular Editor CLI has no editions and simply applies the policy.

## 兼容性

Tabular Editor 2、Tabular Editor 3（Desktop）和 Tabular Editor CLI 的脚本 API 基本兼容，但在某些情况下，你可能需要根据当前运行的宿主环境来有条件地编译代码。 The CLI host defines a `TECLI` preprocessor symbol; TE3 Desktop defines `TE3` (and version-bracketed symbols like `TE3_3_15_OR_GREATER` for the active minor); TE2 defines neither. Preprocessor directives were introduced in Tabular Editor 3.10.0. Use them to write portable scripts:

```csharp
#if TECLI
    // CLI host - no UI APIs available
    Info($"Running under the CLI on {Environment.OSVersion.Platform}");
#elif TE3
    // TE3 Desktop - UI APIs are available
    ShowMessage("Hello from TE3");
#else
    // TE2 (legacy) - neither TECLI nor TE3 is defined
    Info("Hello from TE2");
#endif

#if TE3_3_15_OR_GREATER
    // Gated on a specific TE3 minor version
#endif
```

One CLI-specific caveat: the TE3-Desktop UI helpers `SelectMeasure()`, `SelectTable()`, `SelectColumn()`, `SelectObject()`, and `SelectObjects()` throw `NotSupportedException` under `te script` since the CLI has no UI to pop up. Wrap such calls in `#if TE3` (or `try/catch`) when sharing scripts across hosts.

如果你想在脚本运行时知道 Tabular Editor 的具体版本，可以查看程序集版本：

```csharp
var currentVersion = typeof(Model).Assembly.GetName().Version;
Info(currentVersion.ToString());
```

公开的产品版本号（例如 "2.20.2" 或 "3.10.1"）可以通过以下代码获取：

```csharp
using System.Diagnostics;

var productVersion = FileVersionInfo.GetVersionInfo(Selected.GetType().Assembly.Location).ProductVersion;
productVersion.Output(); // productVersion is a string ("2.20.2" or "3.10.1", for example)
```

如果你只想要主版本号（整数），可以用：

```csharp
var majorVersion = Selected.GetType().Assembly.GetName().Version.Major;
majorVersion.Output(); // majorVersion is an integer (2 or 3)
```

## 已知问题和限制

- 由于脚本的执行方式，某些脚本操作可能导致 Tabular Editor 3 应用程序崩溃或无响应。 For example, a script with an infinite loop (`while(true) {}`) will cause the application to hang. If this happens, you will have to end the Tabular Editor process through the Windows Task Manager.

如果你打算将脚本保存为[宏](xref:creating-macros)，请注意以下限制：

- 如果脚本主体包含带访问修饰符（`public`、`static` 等）的本地方法，则无法将该脚本保存为宏。 Remove the access modifiers, or move the method into a class instead.
- Macros currently do not support the `await` keyword, if used in the script body. 如果脚本主体调用了异步方法，应使用 `MyAsyncMethod.Wait()` 或 `MyAsyncMethod.Result`，而不是 `await MyAsyncMethod()`。 It is fine to use `await` in `async` methods that are defined elsewhere in the script.