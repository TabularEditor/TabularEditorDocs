---
uid: csharp-scripts
title: C# Scripts
author: Daniel Otykier
updated: 2026-05-27
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

# C# Scripts

This is an introduction to the C# Scripting capabilities of Tabular Editor 3. Information in this document is subject to change. Also, make sure to check out our script library @csharp-script-library, for some more real-life examples of what you can do with the scripting capabilities of Tabular Editor.

## Why C# scripting?

Tabular Editor 的界面旨在让你在构建表格模型时，轻松完成大多数常见任务。 For example, changing the Display Folder of multiple measures at once is just a matter of selecting the objects in the explorer tree and then dragging and dropping them around. The right-click context menu of the explorer tree provides a convenient way to perform many of these tasks, such as adding/removing objects from perspectives, renaming multiple objects, etc.

There may be many other common workflow tasks, which are not as easily performed through the UI however. For this reason, Tabular Editor offers C# scripting, which lets advanced users write a script using C# syntax, to more directly manipulate the objects in the loaded Tabular Model.

## Code Assist

The C# script editor supports Roslyn-powered completion and call tips and from Tabular Editor 3.23.0, completion supports substring and capital-letters acronym matching.

## Objects

[脚本 API](xref:api-index) 提供对两个顶层对象的访问：`Model` 和 `Selected`。 The former contains methods and properties that allow you to manipulate all objects in the Tabular Model, whereas the latter exposes only objects that are currently selected in the explorer tree.

The `Model` object is a wrapper of the [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) class, exposing a subset of it’s properties, with some additional methods and properties for easier operations on translations, perspectives and object collections. The same applies to any descendant objects, such as Table, Measure, Column, etc. which all have corresponding wrapper objects. Please see <xref:api-index> for a complete listing of objects, properties and methods in the Tabular Editor wrapper library.

The main advantage of working through this wrapper is, that all changes will be undoable from the Tabular Editor UI. Simply press CTRL+Z after executing a script, and you will see that all changes made by the script are immediately undone. Furthermore, the wrapper provides convenient methods that turn many common tasks into simple one-liners. We will provide some examples below. It is assumed that the reader is already somewhat familiar with C# and LINQ, as these aspects of Tabular Editors scripting capabilities will not be covered here. Users unfamiliar with C# and LINQ should still be able to follow the examples given below.

## Setting object properties

如果你想更改某个特定对象的属性，显然最简单的方式就是直接在 UI 中操作。 But as an example, let us see how we could achieve the same thing through scripting.

假设你想更改 'FactInternetSales' 表中 [Sales Amount] 度量值的格式字符串。 If you locate the measure in the explorer tree, you can simply drag it onto the script editor. Tabular Editor will then generate the following code, which represents this particular measure in the Tabular Object Model:

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"]
```

Adding an extra dot (.) after the right-most bracket, should make the autocomplete menu pop up, showing you which properties and methods exist on this particular measure. Simply choose "FormatString" in the menu, or write the first few letters and hit Tab. Then, enter an equal sign followed by "0.0%". Let us also change the Display Folder of this measure. Your final code should look like this:

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"].FormatString = "0.0%";
Model.Tables["FactInternetSales"].Measures["Sales Amount"].DisplayFolder = "New Folder";
```

**Note:** Remember to put the semicolon (;) at the end of each line. This is a requirement of C#. If you forget it, you will get a syntax error message when trying to execute the script.

Hit F5 or the "Play" button above the script editor to execute the script. Immediately, you should see the measure moving around in the explorer tree, reflecting the changed Display Folder. If you examine the measure in the Property Grid, you should also see that the Format String property has changed accordingly.

### Working with multiple objects at once

Many objects in the object model, are actually collections of multiple objects. For example, each Table object has a Measures collection. The wrapper exposes a series of convenient properties and methods on these collections, to make it easy to set the same property on multiple objects at once. This is described in detail below. Additionally, you may use all the standard LINQ extension methods to filter and browse the objects of a collection.

Below is a few examples of the most commonly used LINQ extension methods:

- `Collection.First([predicate])` Returns the first object in the collection satisfying the optional [predicate] condition.
- `Collection.Any([predicate])` Returns true if the collection contains any objects (optionally satisfying the [predicate] condition).
- `Collection.Where(predicate)` Returns a collection that is the original collection filtered by the predicate condition.
- `Collection.Select(map)` Projects each object in the collection into another object according to the specified map.
- `Collection.ForEach(action)` Performs the specified action on each element in the collection.

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

## Working with the **Model** object

To quickly reference any object in the currently loaded Tabular Model, you can drag and drop the object from the explorer tree and into the C# script editor:

![Dragging and dropping an object into the C# script editor](~/content/assets/images/drag-object-to-script.gif)

如需了解 Model 及其后代对象包含哪些属性，请参阅 [TOM 文档](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx)。 Additionally, refer to <xref:api-index> for a complete listing of the properties and methods exposed by the wrapper object.

## Working with the **Selected** object

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
        .ForEach(m => if(m.Name.Contains("Reseller")) m.Name += " DEPRECATED");
```

This example will append the text " DEPRECATED" to the names of all selected measures where the names contain the word "Reseller". 另外，你也可以在应用 `ForEach()` 操作之前，先用 LINQ 扩展方法 `Where()` 过滤集合，这将得到完全相同的结果：

```csharp
Selected.Measures
        .Where(m => m.Name.Contains("Reseller"))
        .ForEach(m => m.Name += " DEPRECATED");
```

### Complete list of Selected accessors

The following table lists all available singular and plural accessors on the `Selected` object. Singular accessors throw a `SelectionException` if the current selection does not contain exactly one object of that type. Plural accessors return an empty collection if no objects of that type are selected.

| Singular                            | Plural                               | Object Type              |
| ----------------------------------- | ------------------------------------ | ------------------------ |
| `Selected.Measure`                  | `Selected.Measures`                  | Measures                 |
| `Selected.Column`                   | `Selected.Columns`                   | All column types         |
| `Selected.DataColumn`               | `Selected.DataColumns`               | Data columns             |
| `Selected.CalculatedColumn`         | `Selected.CalculatedColumns`         | Calculated columns       |
| `Selected.CalculatedTableColumn`    | `Selected.CalculatedTableColumns`    | Calculated table columns |
| `Selected.Hierarchy`                | `Selected.Hierarchies`               | Hierarchies              |
| `Selected.Level`                    | `Selected.Levels`                    | Hierarchy levels         |
| `Selected.Table`                    | `Selected.Tables`                    | Tables                   |
| `Selected.CalculatedTable`          | `Selected.CalculatedTables`          | Calculated tables        |
| `Selected.Partition`                | `Selected.Partitions`                | Partitions               |
| `Selected.Role`                     | `Selected.Roles`                     | Model roles              |
| `Selected.TablePermission`          | `Selected.TablePermissions`          | Table permissions        |
| `Selected.KPI`                      | `Selected.KPIs`                      | KPIs                     |
| `Selected.Calendar`                 | `Selected.Calendars`                 | Calendars                |
| `Selected.CalculationItem`          | `Selected.CalculationItems`          | Calculation items        |
| `Selected.Function`                 | `Selected.Functions`                 | User-defined functions   |
| `Selected.DataSource`               | `Selected.DataSources`               | Data sources             |
| `Selected.SingleColumnRelationship` | `Selected.SingleColumnRelationships` | Relationships            |
| `Selected.Perspective`              | `Selected.Perspectives`              | Perspectives             |
| `Selected.Culture`                  | `Selected.Cultures`                  | Translations             |

> [!NOTE]
> The accessors for Role, KPI, Calendar, CalculationItem, TablePermission, Function, DataSource, SingleColumnRelationship, CalculatedColumn, CalculatedTableColumn, DataColumn, CalculatedTable and Partition were added in Tabular Editor 3.26.0.

## Helper methods

Tabular Editor provides a set of special helper methods to make certain script tasks easier to achieve. Note that some of these may be invoked as extension methods. For example, `object.Output();` and `Output(object);` are equivalent.

- `void Output(object value)` - halts script execution and displays information about the provided object. When the script is running as part of a command line execution, this will write a string representation of the object to the console.
- `void SaveFile(string filePath, string content)` - convenient way to save text data to a file.
- `string ReadFile(string filePath)` - convenient way to load text data from a file.
- `string ExportProperties(IEnumerable<ITabularNamedObject> objects, string properties)` - convenient way to export a set of properties from multiple objects as a TSV string.
- `void ImportProperties(string tsvData)` - convenient way to load properties into multiple objects from a TSV string.
- `void CustomAction(string name)` - invoke a macro by name.
- `void CustomAction(this IEnumerable<ITabularNamedObject> objects, string name)` - invoke a macro on the specified objects.
- `string ConvertDax(string dax, bool useSemicolons)` - converts a DAX expression between US/UK and non-US/UK locales. If `useSemicolons` is true (default) the `dax` string is converted from the native US/UK format to non-US/UK. That is, commas (list separators) will be converted to semicolons and periods (decimal separators) will be converted to commas. Vice versa if `useSemicolons` is set to false.
- `void FormatDax(this IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - formats DAX expressions on all objects in the provided collection
- `void FormatDax(this IDaxDependantObject obj)` - queues an object for DAX expression formatting when script execution is complete, or when the `CallDaxFormatter` method is called.
- `void CallDaxFormatter(bool shortFormat, bool? skipSpace)` - formats all DAX expressions on objects enqueued so far
- `void Info(string)` - Writes an informational message to the console (only when the script is executed as part of a command line execution).
- `void Warning(string)` - Writes a warning message to the console (only when the script is executed as part of a command line execution).
- `void Error(string)` - Writes an error message to the console (only when the script is executed as part of a command line execution).
- `T SelectObject(this IEnumerable<T> objects, T preselect = null, string label = "Select object") where T: TabularNamedObject` - Displays a dialog to the user prompting to select one of the objects specified. If the user cancels the dialog, this method returns null.
- `void CollectVertiPaqAnalyzerStats()` - If Tabular Editor is connected to an instance of Analysis Services, this runs the VertiPaq Analyzer statistics collector.
- `long GetCardinality(this Column column)` - If VertiPaq Analyzer statistics are available for the current model, this method returns the cardinality of the specified column.

For a full list of available helper methods and their syntax, view @script-helper-methods.

### Debugging scripts

如上所述，你可以使用 `Output(object);` 方法来暂停脚本执行，并打开一个对话框来显示传入对象的信息。 You can also use this method as an extension method, invoking it as `object.Output();`. The script is resumed when the dialog is closed.

The dialog will appear in one of four different ways, depending on the kind of object being output:

- Singular objects (such as strings, ints and DateTimes, except any object that derives from TabularNamedObject) will be displayed as a simple message dialog, by invoking the `.ToString()` method on the object:

![C-sharp Output](~/content/assets/images/c-sharp-script-output-function.png)

- 单个 TabularNamedObject（例如表、度量值，或 Tabular Editor 中提供的任何其他 TOM NamedMetadataObject）会显示在属性网格中，类似于在 Tree Explorer 中选中对象时的效果。 Properties on the object may be edited in the grid, but note that if an error is encountered at a later point in the script execution, the edit will be automatically undone, if "Auto-Rollback" is enabled:

![C-sharp Output](~/content/assets/images/c-sharp-script-auto-rollback.png)

- Any IEnumerable of objects (except TabularNamedObjects) will be displayed in a list, where each list item shows the `.ToString()` value and type of the object in the IEnumerable:

![C-sharp Output](~/content/assets/images/c-sharp-script-output-to-string-function.png)

- 任何 TabularNamedObject 的 IEnumerable 都会使对话框左侧显示对象列表，右侧显示属性网格。 The Property Grid will be populated from whatever object is selected in the list, and properties may be edited just as when a single TabularNamedObject is being output:

![C-sharp Output](~/content/assets/images/c-sharp-script-output-function-enumerated.png)

You can tick the "Don't show more outputs" checkbox at the lower left-hand corner, to prevent the script from halting on any further `.Output()` invocations.

## Run C# Scripts with Preview

**带预览运行**操作允许你在提交之前，预览 C# Script 对模型元数据所做的所有更改。 This is useful when running unfamiliar scripts or performing bulk modifications.

要使用此功能，在工具栏或菜单中点击 **脚本 > 带预览运行**。 The workflow is:

1. Tabular Editor takes a snapshot of the model metadata before execution
2. The script runs to completion
3. Tabular Editor compares the current model metadata state to the snapshot taken before execution
4. If changes are detected, a preview dialog appears showing a side-by-side hierarchical diff of the model (before and after)
5. Changes are color-coded: green for added objects, red for deleted and orange for modified properties
6. Use the **Show changes only** checkbox to hide unchanged items and focus on what the script changed
7. Click **OK** to accept the changes, or **Revert** to undo all changes

![Script Preview - Model Changes](~/content/assets/images/c-sharp-script-preview-changes.png)

如果脚本失败（编译或运行时错误），所有模型元数据更改都会自动回滚，并且不会显示预览对话框。 If the script succeeds but makes no detectable metadata changes, an informational message is displayed instead.

All model metadata changes from a script execution are wrapped in a single undo transaction. Even after accepting changes through the preview dialog, you can still undo the entire operation with **Ctrl+Z**.

> [!IMPORTANT]
> The preview and undo features only apply to model metadata changes. If a script performs external operations such as writing to files, databases or making web requests, those operations are executed immediately and cannot be reverted. The preview dialog does not attempt to analyze the script code — it works by comparing the model metadata state before and after execution.

> [!TIP]
> The [AI Assistant](xref:ai-assistant) shows the preview changes dialog automatically when you execute C# scripts from the chat, so you always get a chance to review AI-generated model changes before they are applied.

## .NET references

You can use the `using` keyword to shorten class names, etc. just like in regular C# source code. In addition, you can include external assemblies by using the syntax `#r "<assembly name or DLL path>"` similar to .csx scripts used in Azure Functions.

For example, the following script will now work as expected:

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

By default, Tabular Editor applies the following `using` keyword (even though they are not specified in the script), to make common tasks easier:

```csharp
using System;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json;
using TabularEditor.TOMWrapper;
using TabularEditor.TOMWrapper.Utils;
using TabularEditor.UI;
```

In addition, the following .NET Framework assemblies are loaded by default:

- System.Dll
- System.Core.Dll
- System.Data.Dll
- System.Windows.Forms.Dll
- Microsoft.Csharp.Dll
- Newtonsoft.Json.Dll
- TomWrapper.Dll
- TabularEditor.Exe
- Microsoft.AnalysisServices.Tabular.Dll

<a name="accessing-environment-variables"></a>

## Accessing Environment Variables

通过 Tabular Editor CLI 运行 C# Script 时（尤其是在 CI/CD 流水线中），可以使用环境变量向脚本传递参数。 This is the recommended approach, as C# scripts executed by Tabular Editor CLI don't support traditional command-line arguments.

### Reading Environment Variables

Use the `Environment.GetEnvironmentVariable()` method to read environment variables in your script:

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

### Azure DevOps Integration

Environment variables integrate seamlessly with Azure DevOps pipelines, as all pipeline variables are automatically available as environment variables by default.

**Example Azure DevOps YAML Pipeline:**

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

In this example, the script `DeploymentScript.csx` can access `SERVER_NAME` and `DATABASE_NAME` using `Environment.GetEnvironmentVariable()`.

### Common Use Cases

Environment variables are particularly useful for:

- **Dynamic connection strings**: Update data source connections based on deployment environment (Dev, UAT, Production)
- **Conditional logic**: Apply different transformations based on target environment
- **Deployment configuration**: Control which objects to deploy or modify based on parameters
- **Multi-environment support**: Use the same script across different environments with different values

**Example - Environment-specific modifications:**

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

<a name="compatibility"></a>

## Compatibility

The scripting APIs for Tabular Editor 2, Tabular Editor 3 (Desktop), and the Tabular Editor CLI are mostly compatible, but there are cases where you want to conditionally compile code depending on which host is running. The CLI host defines a `TECLI` preprocessor symbol; TE3 Desktop defines `TE3` (and version-bracketed symbols like `TE3_3_15_OR_GREATER` for the active minor); TE2 defines neither. Preprocessor directives were introduced in Tabular Editor 3.10.0. Use them to write portable scripts:

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

If you need to know the exact version of Tabular Editor at script runtime, you can inspect the assembly version:

```csharp
var currentVersion = typeof(Model).Assembly.GetName().Version;
Info(currentVersion.ToString());
```

The public product version (for example, "2.20.2" or "3.10.1") can be found using this code:

```csharp
using System.Diagnostics;

var productVersion = FileVersionInfo.GetVersionInfo(Selected.GetType().Assembly.Location).ProductVersion;
productVersion.Output(); // productVersion is a string ("2.20.2" or "3.10.1", for example)
```

If you just want the major version number (as an integer), use:

```csharp
var majorVersion = Selected.GetType().Assembly.GetName().Version.Major;
majorVersion.Output(); // majorVersion is an integer (2 or 3)
```

## Known issues and limitations

- Certain script operations may cause the Tabular Editor 3 application to crash or become unresponsive, due to the way scripts are executed. For example, a script with an infinite loop (`while(true) {}`) will cause the application to hang. If this happens, you will have to end the Tabular Editor process through the Windows Task Manager.

If you intend to save the script as a [macro](xref:creating-macros), please be aware of the following limitations:

- If the script body contains local methods with access modifiers (`public`, `static`, etc.), the script cannot be saved as a macro. Remove the access modifiers, or move the method into a class instead.
- Macros currently do not support the `await` keyword, if used in the script body. If your script body calls into asynchronous methods, you should use `MyAsyncMethod.Wait()` or `MyAsyncMethod.Result` instead of `await MyAsyncMethod()`. It is fine to use `await` in `async` methods that are defined elsewhere in the script.