---
uid: how-to-use-script-ui-helpers
title: How to Use Script UI Helpers
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# How to Use Script UI Helpers

Tabular Editor provides helper methods for user interaction in scripts: displaying output, showing messages, prompting for object selection, evaluating DAX and building custom dialogs. In the desktop UI, these show graphical dialogs. In the CLI, they write to the console.

## Quick reference

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

## Messages: Info, Warning, Error

Use these for simple communication. `Error()` does not stop script execution by itself -- follow it with `return` if you want to halt.

```csharp
if (Selected.Measures.Count() == 0)
{
    Error("Select at least one measure before running this script.");
    return;
}

// ... do work ...
Info("Updated " + Selected.Measures.Count() + " measures.");
```

## Output

`Output()` behaves differently depending on the argument type:

| Argument type                                                                   | Behavior                                      |
| ------------------------------------------------------------------------------- | --------------------------------------------- |
| TOM object (e.g., `Measure`) | Property grid allowing inspection and editing |
| `IEnumerable<TabularNamedObject>`                                               | List view with property grid                  |
| `DataTable`                                                                     | Sortable, filterable grid                     |
| String or primitive                                                             | Simple message dialog                         |

> [!NOTE]
> String output uses Windows line endings. Use `\r\n` or `Environment.NewLine` to insert line breaks. A bare `\n` renders on one line. This catches users out with M expressions, which use `\n` and print as a single line in `Output()`.

### DataTable for structured output

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
> Specify `typeof(int)` or `typeof(double)` for numeric columns to enable correct sorting in the output grid.

## Object selection dialogs

Selection helpers show a list dialog and return the user's choice. They throw an exception if the user cancels. Wrap them in try/catch.

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

### Multi-select (Tabular Editor 3 only)

> [!NOTE]
> `SelectObjects()` is only available in Tabular Editor 3. In Tabular Editor 2, use a single-select dialog in a loop or filter the selection before running the script.

`SelectObjects()` allows the user to pick multiple objects.

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

## Evaluating DAX

`EvaluateDax()` executes a DAX expression against the connected model and returns the result.

```csharp
var rowCount = Convert.ToInt64(EvaluateDax("COUNTROWS('Sales')"));
Info($"Sales table has {rowCount:N0} rows.");

// Return a table result
var result = EvaluateDax("ALL('Product'[Category])");
Output(result);
```

> [!NOTE]
> `EvaluateDax()` requires an active connection to an Analysis Services or Power BI instance. It does not work when editing a model offline.

## Guard clause patterns

Validate preconditions before the script runs.

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

## Custom WinForms dialogs

For input scenarios beyond what the built-in helpers provide, build custom WinForms dialogs directly in the script. See @how-to-build-custom-winforms-dialogs for patterns covering simple prompts, multi-field forms with validation and reusable dialog classes.

## 另见

- @脚本帮助方法
- @script-output-things
- @how-to-build-custom-winforms-dialogs
- @C# 脚本
- @script-implement-incremental-refresh
- @script-find-replace
- @script-convert-dlol-to-import

