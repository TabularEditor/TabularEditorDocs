---
uid: how-to-build-custom-winforms-dialogs
title: Cómo crear cuadros de diálogo personalizados de WinForms en scripts
author: Morten Lønskov
updated: 2026-04-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo crear cuadros de diálogo personalizados de WinForms en scripts

Para escenarios de entrada que vayan más allá de lo que ofrecen `SelectTable()`, `SelectMeasure()` y otros asistentes integrados, crea cuadros de diálogo personalizados de WinForms directamente en un C# Script. Usa `TableLayoutPanel` y `FlowLayoutPanel` con `AutoSize` para lograr un escalado correcto en distintas configuraciones de DPI.

> [!WARNING]
> No uses el posicionamiento manual por píxeles con `Location = new Point(x, y)` en cuadros de diálogo personalizados. Este enfoque falla con configuraciones de DPI no estándar. En su lugar, usa paneles de diseño.

## Cuadro de diálogo de entrada sencillo

Un cuadro de diálogo de entrada con un solo campo y botones Aceptar/Cancelar. Usa este patrón cuando necesites un único dato del usuario.

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

## Formulario de varios campos con validación

Extiende el patrón de entrada a varios campos. Usa un evento de cambio para habilitar el botón Aceptar solo cuando todos los campos obligatorios tengan contenido.

La estructura de bloques siguiente refleja el orden que debes seguir al escribir scripts de cuadros de diálogo: configuración del formulario, campos de entrada, botones, validación y manejo del resultado.

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

## Cuadro de diálogo de selección de ámbito (clase reutilizable)

En los scripts que necesiten elegir entre operar sobre los objetos seleccionados o sobre todos los objetos, encapsula el cuadro de diálogo en una clase reutilizable.

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

## Reglas clave para cuadros de diálogo compatibles con el escalado

- Establece `AutoSize = true` y `AutoSizeMode = AutoSizeMode.GrowAndShrink` en el formulario.
- Usa `TableLayoutPanel` (apilado vertical) y `FlowLayoutPanel` (filas horizontales de botones) en lugar de coordenadas manuales.
- Establece `FormBorderStyle = FormBorderStyle.FixedDialog` y deshabilita los botones de maximizar y minimizar.
- Establece `StartPosition = FormStartPosition.CenterParent`.
- Configura siempre `AcceptButton` y `CancelButton` para que funcionen con el teclado (Enter/Esc).
- Establece `WaitFormVisible = false` antes de mostrar un cuadro de diálogo para ocultar el indicador giratorio "Ejecutando macro".
- Envuelve el formulario en una instrucción `using` para liberarlo correctamente.

## Ver también

- @how-to-use-script-ui-helpers
- @csharp-scripts
- @script-helper-methods
