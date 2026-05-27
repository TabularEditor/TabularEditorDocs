---
uid: how-to-build-custom-winforms-dialogs
title: 如何在脚本中构建自定义 WinForms 对话框
author: Morten Lønskov
updated: 2026-04-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何在脚本中构建自定义 WinForms 对话框

对于 `SelectTable()`、`SelectMeasure()` 等内置辅助函数无法覆盖的输入场景，可直接在 C# Script 中编写自定义 WinForms 对话框。 使用 `TableLayoutPanel` 和 `FlowLayoutPanel` 并启用 `AutoSize`，以便在不同 DPI 设置下正确缩放。

> [!WARNING]
> 在自定义对话框中，不要使用 `Location = new Point(x, y)` 进行手动像素定位。 这种做法在非标准 DPI 设置下会失效。 改用布局面板。

## 简单提示对话框

包含“确定/取消”按钮的单字段输入对话框。 当你只需要用户提供一项输入时，可使用这种模式。

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

## 带验证的多字段表单

将该提示对话框模式扩展到多个字段。 使用变更事件，只有当所有必填字段都有内容时才启用“确定”按钮。

下面的代码块结构对应你编写对话框脚本时应遵循的顺序：窗体设置、输入字段、按钮、验证和结果处理。

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

## 范围选择对话框（可重用类）

如果脚本需要在对所选对象操作和对所有对象操作之间做选择，请将该对话框封装为可复用的类。

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

## 缩放安全对话框的关键规则

- 在窗体上设置 `AutoSize = true` 和 `AutoSizeMode = AutoSizeMode.GrowAndShrink`。
- 使用 `TableLayoutPanel`（垂直堆叠）和 `FlowLayoutPanel`（水平按钮行）代替手动坐标。
- 设置 `FormBorderStyle = FormBorderStyle.FixedDialog`，并禁用最大化/最小化按钮。
- 设置 `StartPosition = FormStartPosition.CenterParent`。
- 始终设置 `AcceptButton` 和 `CancelButton`，以支持键盘快捷键（Enter/Escape）。
- 在显示对话框之前，先将 `WaitFormVisible = false`，以隐藏“正在运行宏”旋转指示器。
- 用 `using` 语句包裹窗体，以确保正确释放资源。

## 另见

- @how-to-use-script-ui-helpers
- @C# 脚本
- @脚本帮助方法
