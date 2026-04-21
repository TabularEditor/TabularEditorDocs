---
uid: how-to-use-script-ui-helpers
title: 如何使用脚本 UI 帮助程序
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何使用脚本 UI 帮助程序

Tabular Editor 为脚本中的用户交互提供了一些辅助方法：显示输出、显示信息、提示选择对象、对 DAX 求值，以及构建自定义对话框。 在桌面 UI 中，这些方法会弹出图形化对话框。 在 CLI 中，它们会输出到控制台。 在桌面 UI 中，这些方法会弹出图形化对话框。 在 CLI 中，它们会输出到控制台。

## 快速参考

```csharp
// Messages
Info("Operation completed.");                          // informational popup
Warning("This might take a while.");                   // warning popup
Error("No valid selection."); return;                  // error popup + stop script

Output("Hello");                                       // simple dialog

// Object selection dialogs (capture returns for reuse below)
var table = SelectTable();                             // pick a table
var column = SelectColumn(table.Columns);              // pick from filtered columns
var measure = SelectMeasure();                         // pick a measure
var ds = SelectObject<DataSource>(Model.DataSources);  // generic selection
var items = SelectObjects(Model.AllMeasures);          // multi-select (TE3 only)

// Evaluate DAX
var result = EvaluateDax("COUNTROWS('Sales')");        // run DAX on connected model

// Output (uses the variables assigned above)
Output(measure);                                       // property grid for a TOM object
Output(items);                                         // list view with property grid
Output(result);                                        // sortable/filterable grid for a DataTable
```

## 信息：信息、警告、错误

用于简单沟通。 用于简单沟通。 `Error()` 本身不会停止脚本执行——如果想中止，就在后面加上 `return`。

```csharp
if (Selected.Measures.Count() == 0)
{
    Error("Select at least one measure before running this script.");
    return;
}

// ... do work ...
Info("Updated " + Selected.Measures.Count() + " measures.");
```

## 输出

`Output()` 的行为会因参数类型而异：

| 参数类型                              | 行为            |
| --------------------------------- | ------------- |
| TOM 对象（例如 `Measure`）              | 可用于查看和编辑的属性网格 |
| `IEnumerable<TabularNamedObject>` | 带属性网格的列表视图    |
| `DataTable`                       | 可排序、可筛选的网格    |
| 字符串或基本类型                          | 简单的信息对话框      |

> [!NOTE]
> 字符串输出使用 Windows 行结束符。 使用 `\r\n` 或 `Environment.NewLine` 来插入换行符。 单独的 `\\n` 会渲染为一行。 [!NOTE]
> 字符串输出使用 Windows 行结束符。 使用 `\r\n` 或 `Environment.NewLine` 来插入换行符。 单独的 `\\n` 会渲染为一行。 这常让使用 M 表达式的用户踩坑：M 表达式使用 `\\n`，但在 `Output()` 中会被打印成单行。

### 用于结构化输出的 DataTable

```csharp
using System.Data;

var result = new DataTable();
result.Columns.Add("Measure");
result.Columns.Add("Table");
result.Columns.Add("Token Count", typeof(int));

foreach (var m in Model.AllMeasures)
{
    result.Rows.Add(m.DaxObjectName, m.Table.Name, m.Tokenize().Count);
}

Output(result);
```

> [!TIP]
> 为数值列指定 `typeof(int)` 或 `typeof(double)`，以便在输出网格中正确排序。

## 对象选择对话框

选择辅助函数会显示一个列表对话框，并返回用户的选择。 如果用户取消操作，它们会抛出异常。 请在 try/catch 中调用它们。 如果用户取消操作，它们会抛出异常。 请在 try/catch 中调用它们。

```csharp
try
{
    var table = SelectTable(Model.Tables, null, "Select a table:");
    var column = SelectColumn(
        table.Columns.Where(c => c.DataType == DataType.DateTime),
        null,
        "Select a date column:"
    );
    Info($"You selected {table.Name}.{column.Name}");
}
catch
{
    Error("Selection cancelled.");
}
```

### 多选（仅限 Tabular Editor 3）

> [!NOTE]
> `SelectObjects()` 仅在 Tabular Editor 3 中可用。 在 Tabular Editor 2 中，可以在循环中使用单选对话框，或在运行脚本前先筛选选中的对象。 在 Tabular Editor 2 中，可以在循环中使用单选对话框，或在运行脚本前先筛选选中的对象。

`SelectObjects()` 允许用户选择多个对象。

```csharp
try
{
    var measures = SelectObjects(
        Model.AllMeasures.Where(m => m.IsHidden),
        null,
        "Select measures to unhide:"
    );
    foreach (var m in measures)
        m.IsHidden = false;
}
catch
{
    Error("No selection made.");
}
```

## 评估 DAX

`EvaluateDax()` 会针对以连接模式连接的模型执行 DAX 表达式并返回结果。

```csharp
var rowCount = Convert.ToInt64(EvaluateDax("COUNTROWS('Sales')"));
Info($"Sales table has {rowCount:N0} rows.");

// Return a table result
var result = EvaluateDax("ALL('Product'[Category])");
Output(result);
```

> [!NOTE]
> `EvaluateDax()` 需要与 Analysis Services 或 Power BI 实例保持活动连接。 离线编辑模型时无法使用。 离线编辑模型时无法使用。

## 卫语句模式

在脚本运行前验证前置条件。

```csharp
// Require at least one column or measure
if (Selected.Columns.Count() == 0 && Selected.Measures.Count() == 0)
{
    Error("Select at least one column or measure.");
    return;
}

// Smart single-or-select pattern
DataSource ds;
if (Selected.DataSources.Count() == 1)
    ds = Selected.DataSource;
else
    ds = SelectObject<DataSource>(Model.DataSources, null, "Select a data source:");
```

## 自定义 WinForms 对话框

对于内置辅助函数无法覆盖的输入场景，可直接在脚本中构建自定义 WinForms 对话框。 有关简单提示、带验证的多字段表单以及可重用对话框类的实现模式，请参阅 @how-to-build-custom-winforms-dialogs。 有关简单提示、带验证的多字段表单以及可重用对话框类的实现模式，请参阅 @how-to-build-custom-winforms-dialogs。

## 另见

- @脚本帮助方法
- @script-output-things
- @how-to-build-custom-winforms-dialogs
- @C# 脚本
- @script-implement-incremental-refresh
- @script-find-replace
- @script-convert-dlol-to-import

