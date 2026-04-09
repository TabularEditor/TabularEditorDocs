---
uid: how-to-use-script-ui-helpers
title: How to Use Script UI Helpers
author: Morten Lønskov
updated: 2026-04-09
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

// Output
Output(measure);                                       // property grid for a TOM object
Output(listOfMeasures);                                // list view with property grid
Output(dataTable);                                     // sortable/filterable grid
Output("Hello");                                       // simple dialog

// Object selection dialogs
var table = SelectTable();                             // pick a table
var column = SelectColumn(table.Columns);              // pick from filtered columns
var measure = SelectMeasure();                         // pick a measure
var obj = SelectObject<DataSource>(Model.DataSources); // generic selection
var items = SelectObjects(collection);                 // multi-select

// Evaluate DAX
var result = EvaluateDax("COUNTROWS('Sales')");        // run DAX on connected model
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

| Argument type | Behavior |
|---|---|
| TOM object (e.g., `Measure`) | Property grid allowing inspection and editing |
| `IEnumerable<TabularNamedObject>` | List view with property grid |
| `DataTable` | Sortable, filterable grid |
| String or primitive | Simple message dialog |

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

### Multi-select

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

For more complex input, build WinForms dialogs. Use `TableLayoutPanel` and `FlowLayoutPanel` with `AutoSize` for proper scaling across DPI settings.

> [!WARNING]
> Do not use manual pixel positioning with `Location = new Point(x, y)` for custom dialogs. This approach breaks at non-standard DPI settings. Use layout panels instead.

### Simple prompt dialog

```csharp
using System.Windows.Forms;
using System.Drawing;

WaitFormVisible = false;

using (var form = new Form())
{
    form.Text = "Enter a value";
    form.AutoSize = true;
    form.AutoSizeMode = AutoSizeMode.GrowAndShrink;
    form.FormBorderStyle = FormBorderStyle.FixedDialog;
    form.MaximizeBox = false;
    form.MinimizeBox = false;
    form.StartPosition = FormStartPosition.CenterParent;
    form.Padding = new Padding(20);

    var layout = new TableLayoutPanel {
        ColumnCount = 1, Dock = DockStyle.Fill,
        AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink
    };
    form.Controls.Add(layout);

    layout.Controls.Add(new Label { Text = "Display folder name:", AutoSize = true });
    var textBox = new TextBox { Width = 300, Text = "New Folder" };
    layout.Controls.Add(textBox);

    var buttons = new FlowLayoutPanel {
        FlowDirection = FlowDirection.LeftToRight,
        Dock = DockStyle.Fill, AutoSize = true,
        Padding = new Padding(0, 10, 0, 0)
    };
    var okBtn = new Button { Text = "OK", AutoSize = true, DialogResult = DialogResult.OK };
    var cancelBtn = new Button { Text = "Cancel", AutoSize = true, DialogResult = DialogResult.Cancel };
    buttons.Controls.AddRange(new Control[] { okBtn, cancelBtn });
    layout.Controls.Add(buttons);

    form.AcceptButton = okBtn;
    form.CancelButton = cancelBtn;

    if (form.ShowDialog() == DialogResult.OK)
    {
        Selected.Measures.ForEach(m => m.DisplayFolder = textBox.Text);
        Info("Updated display folder to: " + textBox.Text);
    }
}
```

### Multi-field form with validation

```csharp
using System.Windows.Forms;
using System.Drawing;

WaitFormVisible = false;

using (var form = new Form())
{
    form.Text = "Create Measure";
    form.AutoSize = true;
    form.AutoSizeMode = AutoSizeMode.GrowAndShrink;
    form.StartPosition = FormStartPosition.CenterParent;
    form.FormBorderStyle = FormBorderStyle.FixedDialog;
    form.MaximizeBox = false;
    form.MinimizeBox = false;
    form.Padding = new Padding(20);

    var layout = new TableLayoutPanel {
        ColumnCount = 1, Dock = DockStyle.Fill,
        AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink
    };
    form.Controls.Add(layout);

    // Name field
    layout.Controls.Add(new Label { Text = "Measure name:", AutoSize = true });
    var nameBox = new TextBox { Width = 400 };
    layout.Controls.Add(nameBox);

    // Expression field
    layout.Controls.Add(new Label {
        Text = "DAX expression:", AutoSize = true,
        Padding = new Padding(0, 10, 0, 0)
    });
    var exprBox = new TextBox { Width = 400, Height = 80, Multiline = true };
    layout.Controls.Add(exprBox);

    // Buttons
    var buttons = new FlowLayoutPanel {
        FlowDirection = FlowDirection.LeftToRight,
        Dock = DockStyle.Fill, AutoSize = true,
        Padding = new Padding(0, 10, 0, 0)
    };
    var okBtn = new Button {
        Text = "OK", AutoSize = true,
        DialogResult = DialogResult.OK, Enabled = false
    };
    var cancelBtn = new Button {
        Text = "Cancel", AutoSize = true,
        DialogResult = DialogResult.Cancel
    };
    buttons.Controls.AddRange(new Control[] { okBtn, cancelBtn });
    layout.Controls.Add(buttons);

    form.AcceptButton = okBtn;
    form.CancelButton = cancelBtn;

    // Enable OK only when both fields have content
    EventHandler validate = (s, e) =>
        okBtn.Enabled = !string.IsNullOrWhiteSpace(nameBox.Text)
                     && !string.IsNullOrWhiteSpace(exprBox.Text);
    nameBox.TextChanged += validate;
    exprBox.TextChanged += validate;

    if (form.ShowDialog() == DialogResult.OK)
    {
        var table = Selected.Table;
        table.AddMeasure(nameBox.Text.Trim(), exprBox.Text.Trim());
        Info("Created measure: " + nameBox.Text.Trim());
    }
}
```

### Scope selection dialog (reusable class)

For scripts that need a choice between operating on selected objects or all objects, create a reusable dialog class.

```csharp
using System.Windows.Forms;
using System.Drawing;

public class ScopeDialog : Form
{
    public enum ScopeOption { OnlySelected, All, Cancel }
    public ScopeOption SelectedOption { get; private set; }

    public ScopeDialog(int selectedCount, int totalCount)
    {
        Text = "Choose scope";
        AutoSize = true;
        AutoSizeMode = AutoSizeMode.GrowAndShrink;
        StartPosition = FormStartPosition.CenterParent;
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        MinimizeBox = false;
        Padding = new Padding(20);

        var layout = new TableLayoutPanel {
            ColumnCount = 1, Dock = DockStyle.Fill,
            AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink
        };
        Controls.Add(layout);

        layout.Controls.Add(new Label {
            Text = $"{selectedCount} object(s) selected out of {totalCount} total.",
            AutoSize = true
        });

        var buttons = new FlowLayoutPanel {
            FlowDirection = FlowDirection.LeftToRight,
            Dock = DockStyle.Fill, AutoSize = true,
            Padding = new Padding(0, 15, 0, 0)
        };

        var btnSelected = new Button {
            Text = "Only selected", AutoSize = true,
            DialogResult = DialogResult.OK
        };
        btnSelected.Click += (s, e) => SelectedOption = ScopeOption.OnlySelected;

        var btnAll = new Button {
            Text = "All objects", AutoSize = true,
            DialogResult = DialogResult.Yes
        };
        btnAll.Click += (s, e) => SelectedOption = ScopeOption.All;

        var btnCancel = new Button {
            Text = "Cancel", AutoSize = true,
            DialogResult = DialogResult.Cancel
        };
        btnCancel.Click += (s, e) => SelectedOption = ScopeOption.Cancel;

        buttons.Controls.AddRange(new Control[] { btnSelected, btnAll, btnCancel });
        layout.Controls.Add(buttons);

        AcceptButton = btnSelected;
        CancelButton = btnCancel;
    }
}

// Usage:
WaitFormVisible = false;
using (var dialog = new ScopeDialog(Selected.Measures.Count(), Model.AllMeasures.Count()))
{
    dialog.ShowDialog();
    switch (dialog.SelectedOption)
    {
        case ScopeDialog.ScopeOption.OnlySelected:
            Selected.Measures.ForEach(m => m.FormatString = "#,##0.00");
            break;
        case ScopeDialog.ScopeOption.All:
            Model.AllMeasures.ForEach(m => m.FormatString = "#,##0.00");
            break;
        case ScopeDialog.ScopeOption.Cancel:
            break;
    }
}
```

### Key rules for scaling-safe dialogs

- Set `AutoSize = true` and `AutoSizeMode = AutoSizeMode.GrowAndShrink` on the form.
- Use `TableLayoutPanel` (vertical stacking) and `FlowLayoutPanel` (horizontal button rows) instead of manual coordinates.
- Set `FormBorderStyle = FormBorderStyle.FixedDialog` and disable maximize/minimize.
- Set `StartPosition = FormStartPosition.CenterParent`.
- Always set `AcceptButton` and `CancelButton` for keyboard support (Enter/Escape).
- Call `WaitFormVisible = false` before showing a dialog to hide the "Running Macro" spinner.
- Wrap the form in a `using` statement for proper disposal.

## See also

- @script-helper-methods
- @script-output-things
- @csharp-scripts
- @script-implement-incremental-refresh
- @script-find-replace
- @script-convert-dlol-to-import
