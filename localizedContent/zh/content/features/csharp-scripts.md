---
uid: csharp-scripts
title: C# Script
author: Daniel Otykier
updated: 2026-03-19
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
---

# C# Script

本文将介绍 Tabular Editor 3 的 C# Script 功能。 本文档中的信息可能会发生变更。 另外，别忘了查看我们的脚本库 @csharp-script-library，里面有更多贴近实际的示例，展示如何使用 Tabular Editor 的脚本功能。 本文档中的信息可能会发生变更。 另外，别忘了查看我们的脚本库 @csharp-script-library，里面有更多贴近实际的示例，展示如何使用 Tabular Editor 的脚本功能。

## 为什么要用 C# Script？

Tabular Editor 的 UI 旨在让你在构建表格模型时轻松完成大多数常见任务。 例如，要一次性更改多个度量值的显示文件夹，只需在资源管理器树中选中这些对象，然后拖放到相应位置即可。 资源管理器树的右键菜单提供了更便捷的入口来完成许多任务，例如将对象添加到透视中或从透视中移除、批量重命名对象等。 例如，要一次性更改多个度量值的显示文件夹，只需在资源管理器树中选中这些对象，然后拖放到相应位置即可。 资源管理器树的右键菜单提供了更便捷的入口来完成许多任务，例如将对象添加到透视中或从透视中移除、批量重命名对象等。

不过，还有不少常见的工作流任务并不容易通过 UI 完成。 因此，Tabular Editor 提供 C# Script，让高级用户可以用 C# 语法编写脚本，更直接地操作已加载的表格模型中的对象。

## Code Assist

C# Script 编辑器支持基于 Roslyn 的代码补全和调用提示；从 Tabular Editor 3.23.0 起，补全还支持子字符串匹配和大写首字母缩写匹配。

## 对象

[scripting API](xref:api-index) 提供对两个顶层对象的访问：`Model` 和 `Selected`。 前者包含用于操作表格模型中所有对象的方法和属性；后者只公开当前在资源管理器树中选中的对象。 前者包含用于操作表格模型中所有对象的方法和属性；后者只公开当前在资源管理器树中选中的对象。

`Model` 对象是 [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) 类的封装，仅公开其部分属性，并额外提供一些方法和属性，方便对翻译、透视和对象集合进行操作。 同样也适用于任何派生对象，例如表、度量值、列等，它们都各自有对应的包装器对象。 请参阅 <xref:api-index>，查看 Tabular Editor 包装器库中对象、属性和方法的完整列表。 同样也适用于任何派生对象，例如表、度量值、列等，它们都各自有对应的包装器对象。 请参阅 <xref:api-index>，查看 Tabular Editor 包装器库中对象、属性和方法的完整列表。

通过此包装器进行操作的主要优势在于：所有更改都可以在 Tabular Editor UI 中撤销。 执行脚本后直接按 CTRL+Z，你会看到脚本所做的所有更改会立即被撤销。 此外，包装器还提供了一些便捷方法，让许多常见任务都能用一行代码完成。 下面我们会提供一些示例。 我们假设你已经对 C# 和 LINQ 有一定了解，因为这里不会讲解 Tabular Editor 脚本功能中的这些内容。 即使你不熟悉 C# 和 LINQ，也应该能跟上下面的示例。

## 设置对象属性

如果你只想更改某一个对象的某个属性，最简单的方式当然是直接在 UI 中操作。 不过作为示例，我们来看如何通过脚本实现同样的效果。 不过作为示例，我们来看如何通过脚本实现同样的效果。

假设你想修改 'FactInternetSales' 表中 [Sales Amount] 度量值的格式字符串。 如果你在资源管理器树中找到该度量值，直接将其拖到脚本编辑器即可。 随后 Tabular Editor 会生成如下代码，用于在 Tabular Object Model 中表示这个特定的度量值： 如果你在资源管理器树中找到该度量值，直接将其拖到脚本编辑器即可。 随后 Tabular Editor 会生成如下代码，用于在 Tabular Object Model 中表示这个特定的度量值：

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"]
```

再加一个点（.） 在最右侧括号后加上英文句点.，就会弹出自动补全菜单，显示这个度量值有哪些属性和方法。 在菜单中直接选择 "FormatString"，或者输入前几个字母后按 Tab。 然后输入等号，后面接 "0.0%"。 我们也来修改此度量值的显示文件夹。 最终代码应如下所示：

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"].FormatString = "0.0%";
Model.Tables["FactInternetSales"].Measures["Sales Amount"].DisplayFolder = "New Folder";
```

**注意：** 记得在每行末尾加上分号（;）。 这是 C# 的要求。 如果忘了加，尝试执行脚本时会收到语法错误信息。

按 F5 或点击脚本编辑器上方的“播放”按钮来执行脚本。 你会立刻看到该度量值在资源管理器树中移动位置，反映出“显示文件夹”已更改。 如果你在属性网格中查看该度量值，也会看到“格式字符串”属性已相应更改。

### 同时处理多个对象

对象模型中的许多对象实际上都是由多个对象组成的集合。 例如，每个表对象都有一个度量值集合。 该封装器在这些集合上提供了一系列便捷的属性和方法，便于你一次性为多个对象设置相同的属性。 下文将对此进行详细说明。 此外，你还可以使用所有标准的 LINQ 扩展方法来筛选和浏览集合中的对象。

下面是一些最常用的 LINQ 扩展方法示例：

- `Collection.First([predicate])` 返回集合中第一个满足可选 [predicate] 条件的对象。
- `Collection.Any([predicate])` 如果集合包含任何对象（可选：满足 [predicate] 条件），则返回 true。
- `Collection.Where(predicate)` 返回一个集合，该集合是按 predicate 条件从原集合筛选得到的。
- `Collection.Select(map)` 根据指定的 map，将集合中的每个对象投影为另一个对象。
- `Collection.ForEach(action)` 对集合中的每个元素执行指定的 action。

在上面的示例中，`predicate` 是一个 lambda 表达式：以单个对象作为输入，并返回一个布尔值作为输出。 例如，如果 `Collection` 是一个度量值集合，一个典型的 `predicate` 可能是： 例如，如果 `Collection` 是一个度量值集合，一个典型的 `predicate` 可能是：

`m => m.Name.Contains("Reseller")`

该 predicate 仅在度量值的 `Name` 包含字符串“Reseller”时才会返回 true。 如果需要更复杂的逻辑，可以用花括号包裹表达式并使用 `return` 关键字： 如果需要更复杂的逻辑，可以用花括号包裹表达式并使用 `return` 关键字：

```csharp
.Where(obj => {
    if(obj is Column) {
        return false;
    }
    return obj.Name.Contains("test");
})
```

回到上面的示例，`map` 是一个 lambda 表达式：以单个对象作为输入，并返回任意单个对象作为输出。 `action` 是一个 lambda 表达式：以单个对象作为输入，但不返回任何值。 `action` 是一个 lambda 表达式：以单个对象作为输入，但不返回任何值。

## 使用 **Model** 对象

要快速引用当前已加载的表格模型中的任意对象，你可以将该对象从资源管理器树拖放到 C# Script 编辑器中：

![将对象拖放到 C# Script 脚本编辑器中](~/content/assets/images/drag-object-to-script.gif)

可以参考 [TOM 文档](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx)，了解 Model 及其派生对象上有哪些属性。 另外，也可以查看 <xref:api-index>，获取包装对象公开的属性和方法的完整列表。 另外，也可以查看 <xref:api-index>，获取包装对象公开的属性和方法的完整列表。

## 使用 **Selected** 对象

在某些工作流中，能够显式引用表格模型中的任何对象非常有用；但有时你希望从资源管理器树中挑选对象，然后只对所选对象执行脚本。 这时 `Selected` 对象就派上用场了。 这时 `Selected` 对象就派上用场了。

`Selected` 对象提供了一组属性，便于识别当前选中的内容，同时也可以将选择范围限定为特定类型的对象。 在使用显示文件夹浏览时，如果在资源管理器树中选中了一个或多个文件夹，则其所有子项也会被视为已选中。
对于单项选择，请使用要访问的对象类型的单数名称。 例如，

`Selected.Hierarchy`

它指向树中当前选中的层次结构，前提是只选中了一个层次结构。 如果要处理多选，请使用该类型的复数名称： 如果要处理多选，请使用该类型的复数名称：

`Selected.Hierarchies`

单数对象上存在的所有属性，在其复数形式上也同样存在，只有少数例外。 这意味着你可以用一行代码一次性为多个对象设置这些属性，而无需使用上面提到的 LINQ 扩展方法。 例如，假设你想把当前选中的所有度量值移动到名为 "Test" 的新显示文件夹中：

`Selected.Measures.DisplayFolder = "Test";`

如果树中当前没有选中任何度量值，上面的代码不会执行任何操作，也不会抛出错误。 否则，所有选中的度量值的 DisplayFolder 属性都会被设置为 "Test"（即使这些度量值位于文件夹中也是如此，因为 `Selected` 对象也会包含所选文件夹内的对象）。 如果你使用单数形式 `Measure` 而不是 `Measures`，除非当前选择恰好包含一个度量值，否则会报错。

虽然没法一次性设置多个对象的 Name 属性，但还是有一些办法。 虽然没法一次性设置多个对象的 Name 属性，但还是有一些办法。 如果只是想将某个字符串的所有匹配项替换为另一个字符串，可以使用提供的 "Rename" 方法，例如：

```csharp
Selected.Measures
        .Rename("Amount", "Value");
```

这会将当前所选所有度量值的名称中出现的“Amount”替换为“Value”。
或者，也可以按上文所述使用 LINQ 的 ForEach() 方法，以实现更复杂的逻辑：
或者，也可以按上文所述使用 LINQ 的 ForEach() 方法，以实现更复杂的逻辑：

```csharp
Selected.Measures
        .ForEach(m => if(m.Name.Contains("Reseller")) m.Name += " DEPRECATED");
```

此示例会在所有已选且名称包含“Reseller”的度量值名称后追加文本“ DEPRECATED”。 此示例会在所有已选且名称包含“Reseller”的度量值名称后追加文本“ DEPRECATED”。 或者，我们也可以先使用 LINQ 扩展方法 `Where()` 过滤集合，再应用 `ForEach()` 操作，得到的结果完全相同：

```csharp
Selected.Measures
        .Where(m => m.Name.Contains("Reseller"))
        .ForEach(m => m.Name += " DEPRECATED");
```

### Selected 访问器完整列表

下表列出了 `Selected` 对象上所有可用的单数和复数访问器。 如果当前选择中不恰好包含一个该类型的对象，单数访问器会抛出 `SelectionException`。 如果未选择该类型的任何对象，复数访问器会返回空集合。

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
| `Selected.分区`                       | `Selected.Partitions`                | 分区      |
| `Selected.角色`                       | `Selected.Roles`                     | 模型角色    |
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

## 辅助方法

Tabular Editor 提供了一组专用的辅助方法，便于完成某些脚本任务。 注意，其中一些方法也可以以扩展方法的形式调用。 例如，`object.Output();` 与 `Output(object);` 是等价的。 注意，其中一些方法也可以以扩展方法的形式调用。 例如，`object.Output();` 与 `Output(object);` 是等价的。

- `void Output(object value)` - 停止脚本执行，并显示所提供对象的信息。 当脚本作为命令行执行的一部分运行时，该方法会将该对象的字符串表示形式写入控制台。 当脚本作为命令行执行的一部分运行时，该方法会将该对象的字符串表示形式写入控制台。
- `void SaveFile(string filePath, string content)` - 便捷地将文本数据保存到文件。
- `string ReadFile(string filePath)` - 便捷地从文件加载文本数据。
- `string ExportProperties(IEnumerable<ITabularNamedObject> objects, string properties)` - 便捷地将多个对象的一组属性导出为 TSV 字符串。
- `void ImportProperties(string tsvData)` - 便捷地将 TSV 字符串中的属性加载到多个对象中。
- `void CustomAction(string name)` - 按名称调用宏。
- `void CustomAction(this IEnumerable<ITabularNamedObject> objects, string name)` - 对指定对象调用宏。
- `string ConvertDax(string dax, bool useSemicolons)` - 在美/英区域设置与非美/英区域设置之间相互转换 DAX 表达式。 如果 `useSemicolons` 为 true（默认），则会将 `dax` 字符串从默认的美/英格式转换为非美/英格式。 也就是说，逗号（列表分隔符）会转换为分号，句点（小数分隔符）会转换为逗号。 如果将 `useSemicolons` 设为 false，则反向转换。 如果 `useSemicolons` 为 true（默认），则会将 `dax` 字符串从默认的美/英格式转换为非美/英格式。 也就是说，逗号（列表分隔符）会转换为分号，句点（小数分隔符）会转换为逗号。 如果将 `useSemicolons` 设为 false，则反向转换。
- `void FormatDax(this IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - 为所提供集合中的所有对象格式化 DAX 表达式
- `void FormatDax(this IDaxDependantObject obj)` - 将对象加入队列，在脚本执行完成时，或调用 `CallDaxFormatter` 方法时，对其 DAX 表达式进行格式化。
- `void CallDaxFormatter(bool shortFormat, bool? skipSpace)` - 格式化截至目前已加入队列的对象上的所有 DAX 表达式
- `void Info(string)` - 将一条提示信息输出到控制台（仅当脚本在命令行执行过程中运行时）。
- `void Warning(string)` - 将一条警告信息输出到控制台（仅当脚本在命令行执行过程中运行时）。
- `void Error(string)` - 将一条错误信息输出到控制台（仅当脚本在命令行执行过程中运行时）。
- `T SelectObject(this IEnumerable<T> objects, T preselect = null, string label = "Select object") where T: TabularNamedObject` - 向用户显示一个对话框，提示其从指定对象中选择一个。 如果用户取消对话框，此方法将返回 null。 如果用户取消对话框，此方法将返回 null。
- `void CollectVertiPaqAnalyzerStats()` - 如果 Tabular Editor 已连接到 Analysis Services 实例，则会运行 VertiPaq分析器统计信息收集器。
- `long GetCardinality(this Column column)` - 如果当前模型有可用的 VertiPaq分析器统计信息，此方法将返回指定列的基数。

有关可用帮助方法及其语法的完整列表，请参阅 @script-helper-methods。

### 调试脚本

如上所述，你可以使用 `Output(object);` 方法暂停脚本执行，并打开一个对话框来显示所传入对象的信息。 你也可以将此方法作为扩展方法使用，通过 `object.Output();` 来调用。 关闭对话框后，脚本将继续执行。 你也可以将此方法作为扩展方法使用，通过 `object.Output();` 来调用。 关闭对话框后，脚本将继续执行。

对话框会根据输出对象的类型，以以下四种方式之一呈现：

- 单个对象（如 string、int 和 DateTime，但不包括任何派生自 TabularNamedObject 的对象）将以简单的信息对话框显示，方法是对该对象调用 `.ToString()`：

![C-sharp Output](~/content/assets/images/c-sharp-script-output-function.png)

- 单个 TabularNamedObject（例如表、度量值，或 Tabular Editor 中提供的任何其他 TOM NamedMetadataObject）将显示在“属性网格”中，类似于在 Tree Explorer 树形资源管理器中选中某个对象时的效果。 你可以在网格中编辑该对象的属性。但请注意：如果脚本在后续执行过程中遇到错误，并且启用了“自动回滚”——"Auto-Rollback"——这些编辑将自动撤销：

![C-sharp Output](~/content/assets/images/c-sharp-script-auto-rollback.png)

- 任何对象的 IEnumerable（TabularNamedObject 除外）都会以列表形式显示，其中每个列表项都会显示 IEnumerable 中各对象的 `.ToString()` 值及其类型：

![C-sharp Output](~/content/assets/images/c-sharp-script-output-to-string-function.png)

- 任何 TabularNamedObject 的 IEnumerable 都会让对话框左侧显示对象列表，右侧显示属性网格。 属性网格会根据列表中当前选中的对象进行填充，并且属性可编辑方式与输出单个 TabularNamedObject 时相同： 属性网格会根据列表中当前选中的对象进行填充，并且属性可编辑方式与输出单个 TabularNamedObject 时相同：

![C-sharp Output](~/content/assets/images/c-sharp-script-output-function-enumerated.png)

你可以勾选左下角的“不要再显示后续输出”复选框，以避免脚本在之后任何 `.Output()` 调用时暂停。

## 以预览方式运行 C# Script

**带预览运行**操作允许你在提交之前，预览 C# Script 对模型元数据所做的所有更改。 在运行不熟悉的脚本或执行批量修改时，这会很有用。 在运行不熟悉的脚本或执行批量修改时，这会很有用。

要使用此功能，在工具栏或菜单中点击 **脚本 > 带预览运行**。 流程如下： 流程如下：

1. Tabular Editor 会在执行前为模型元数据创建快照
2. 脚本将运行直至完成
3. Tabular Editor 会将当前模型的元数据状态与执行前创建的快照进行比较
4. 如果检测到更改，将弹出预览对话框，以并排的分层差异视图显示模型（执行前与执行后）
5. 更改采用颜色区分：绿色表示新增对象，红色表示已删除对象，橙色表示已修改的属性
6. 使用 **仅显示更改** 复选框隐藏未更改的项目，将注意力集中在脚本更改的内容上
7. 单击 **确定** 以接受更改，或单击 **还原** 以撤销所有更改

![脚本预览 - 模型更改](~/content/assets/images/c-sharp-script-preview-changes.png)

如果脚本失败（编译或运行时错误），所有模型元数据更改都会自动回滚，并且不会显示预览对话框。 如果脚本成功但未检测到任何元数据更改，则会改为显示一条信息。 如果脚本成功但未检测到任何元数据更改，则会改为显示一条信息。

脚本执行产生的所有模型元数据更改都会封装在一次撤销事务中。 即使在预览对话框中接受了更改，也仍可通过 **Ctrl+Z** 撤销整个操作。

> [!IMPORTANT]
> 预览与撤销功能仅适用于模型元数据更改。 如果脚本执行写入文件、数据库或发起 Web 请求等外部操作，这些操作会立即执行，且无法撤销。 预览对话框不会尝试分析脚本代码——其原理是比较执行前后的模型元数据状态。

> [!TIP]
> 当你在聊天中执行 C# Script 时，[AI 助手](xref:ai-assistant)会自动显示更改预览对话框，因此在应用前始终有机会查看 AI 生成的模型更改。

## .NET 引用

你可以像在普通的 C# 源代码中一样，使用 `using` 关键字来简化类名等写法。 你可以像在普通的 C# 源代码中一样，使用 `using` 关键字来简化类名等写法。 此外，你还可以使用语法 `#r "<assembly name or DLL path>"` 来包含外部程序集，方式与 Azure Functions 中使用的 .csx 脚本类似。

例如，下面这段脚本现在会按预期工作：

```csharp
// 程序集引用必须放在文件最顶部：
#r "System.IO.Compression"

// using 关键字必须位于其他任何语句之前：
using System.IO.Compression;
using System.IO;

var xyz = 123;

// using 语句仍会按预期方式工作：
using(var data = new MemoryStream())
using(var zip = new ZipArchive(data, ZipArchiveMode.Create)) 
{
   // ...
}
```

默认情况下，Tabular Editor 会自动引入以下 `using` 指令（即使脚本中未显式声明），以便更方便地完成常见任务：

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

<a name="accessing-environment-variables"></a>

## 访问环境变量

通过 Tabular Editor CLI 运行 C# Script 时（尤其是在 CI/CD 流水线中），可以使用环境变量向脚本传递参数。 这是推荐的做法，因为 Tabular Editor CLI 执行的 C# Script 不支持传统的命令行参数。 这是推荐的做法，因为 Tabular Editor CLI 执行的 C# Script 不支持传统的命令行参数。

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

// 应用与环境相关的设置
foreach(var table in Model.Tables)
{
    if(environment == "Production" && !refreshPolicy)
    {
        // 如有需要，在生产环境中禁用增量刷新的刷新策略
        table.EnableRefreshPolicy = false;
    }
}

Info($"已为 {environment} 环境配置模型");
```

<a name="compatibility"></a>

## 兼容性

Tabular Editor 2 和 Tabular Editor 3 的脚本 API 大多兼容，但在某些情况下，你可能希望根据所使用的版本对代码进行条件编译。 为此，你可以使用预处理器指令，这些指令是在 Tabular Editor 3.10.0 中引入的。 为此，你可以使用预处理器指令，这些指令是在 Tabular Editor 3.10.0 中引入的。

```csharp
#if TE3
    // 仅当脚本在 TE3（版本 3.10.0 或更高）中运行时才会编译此代码。
    Info("Hello from TE3!");
#else
    // 在其他所有情况下都会编译此代码。
    Info("Hello from TE2!");
#endif
```

如果你想在脚本运行时知道 Tabular Editor 的具体版本，可以查看程序集版本：

```csharp
var currentVersion = typeof(Model).Assembly.GetName().Version;
Info(currentVersion.ToString());
```

公开的产品版本号（例如 "2.20.2" 或 "3.10.1"）可以通过以下代码获取：

```csharp
using System.Diagnostics;

var productVersion = FileVersionInfo.GetVersionInfo(Selected.GetType().Assembly.Location).ProductVersion;
productVersion.Output(); // productVersion 是一个字符串（例如 "2.20.2" 或 "3.10.1"）
```

如果你只想要主版本号（整数），可以用：

```csharp
var majorVersion = Selected.GetType().Assembly.GetName().Version.Major;
majorVersion.Output(); // majorVersion is an integer (2 or 3)
```

## 已知问题与限制

- 由于脚本的执行方式，某些脚本操作可能导致 Tabular Editor 3 应用程序崩溃或无响应。 例如，包含无限循环（`while(true) {}`）的脚本会导致应用程序卡死。 如果出现这种情况，你需要通过 Windows 任务管理器结束 Tabular Editor 进程。 例如，包含无限循环（`while(true) {}`）的脚本会导致应用程序卡死。 如果出现这种情况，你需要通过 Windows 任务管理器结束 Tabular Editor 进程。

如果你打算将脚本保存为[宏](xref:creating-macros)，请注意以下限制：

- 如果脚本主体包含带访问修饰符（`public`、`static` 等）的本地方法，则无法将该脚本保存为宏。 删除这些访问修饰符，或改为将该方法移到一个类中。 删除这些访问修饰符，或改为将该方法移到一个类中。
- 目前宏不支持在脚本主体中使用 `await` 关键字。 目前宏不支持在脚本主体中使用 `await` 关键字。 如果脚本主体调用了异步方法，应使用 `MyAsyncMethod.Wait()` 或 `MyAsyncMethod.Result`，而不是 `await MyAsyncMethod()`。 在脚本中其他位置定义的 `async` 方法里使用 `await` 是可以的。 在脚本中其他位置定义的 `async` 方法里使用 `await` 是可以的。