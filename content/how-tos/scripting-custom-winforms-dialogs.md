---
uid: how-to-build-custom-winforms-dialogs
title: How to Build Custom WinForms Dialogs in Scripts
author: Morten Lønskov
updated: 2026-04-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# How to Build Custom WinForms Dialogs in Scripts

For input scenarios beyond what `SelectTable()`, `SelectMeasure()` and the other built-in helpers provide, build custom WinForms dialogs directly in a C# script. Use `TableLayoutPanel` and `FlowLayoutPanel` with `AutoSize` for proper scaling across DPI settings.

> [!WARNING]
> Do not use manual pixel positioning with `Location = new Point(x, y)` for custom dialogs. This approach breaks at non-standard DPI settings. Use layout panels instead.

## Simple prompt dialog

A single-field prompt with OK/Cancel buttons. Use this pattern when you need one piece of user input.

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

## Multi-field form with validation

Extend the prompt pattern to multiple fields. Use a change event to enable the OK button only when all required fields have content.

The block structure below mirrors the order you should follow when writing dialog scripts: form setup, input fields, buttons, validation and result handling.

```csharp
using System.Windows.Forms;
using System.Drawing;

WaitFormVisible = false;

using (var form = new Form())
{
    // --- Form setup: AutoSize + layout panel for DPI-safe scaling ---
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

    // --- Input fields: name and expression ---
    layout.Controls.Add(new Label { Text = "Measure name:", AutoSize = true });
    var nameBox = new TextBox { Width = 400 };
    layout.Controls.Add(nameBox);

    layout.Controls.Add(new Label {
        Text = "DAX expression:", AutoSize = true,
        Padding = new Padding(0, 10, 0, 0)
    });
    var exprBox = new TextBox { Width = 400, Height = 80, Multiline = true };
    layout.Controls.Add(exprBox);

    // --- Buttons: OK/Cancel with keyboard support ---
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

    // --- Validation: enable OK only when both fields have content ---
    EventHandler validate = (s, e) =>
        okBtn.Enabled = !string.IsNullOrWhiteSpace(nameBox.Text)
                     && !string.IsNullOrWhiteSpace(exprBox.Text);
    nameBox.TextChanged += validate;
    exprBox.TextChanged += validate;

    // --- Process result ---
    if (form.ShowDialog() == DialogResult.OK)
    {
        var table = Selected.Table;
        table.AddMeasure(nameBox.Text.Trim(), exprBox.Text.Trim());
        Info("Created measure: " + nameBox.Text.Trim());
    }
}
```

## Scope selection dialog (reusable class)

For scripts that need a choice between operating on selected objects or all objects, encapsulate the dialog in a reusable class.

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

## Key rules for scaling-safe dialogs

- Set `AutoSize = true` and `AutoSizeMode = AutoSizeMode.GrowAndShrink` on the form.
- Use `TableLayoutPanel` (vertical stacking) and `FlowLayoutPanel` (horizontal button rows) instead of manual coordinates.
- Set `FormBorderStyle = FormBorderStyle.FixedDialog` and disable maximize/minimize.
- Set `StartPosition = FormStartPosition.CenterParent`.
- Always set `AcceptButton` and `CancelButton` for keyboard support (Enter/Escape).
- Call `WaitFormVisible = false` before showing a dialog to hide the "Running Macro" spinner.
- Wrap the form in a `using` statement for proper disposal.

## See also

- @how-to-use-script-ui-helpers
- @csharp-scripts
- @script-helper-methods
