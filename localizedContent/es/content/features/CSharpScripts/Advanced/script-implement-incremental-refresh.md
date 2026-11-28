---
uid: script-implement-incremental-refresh
title: Configurar la actualización incremental
author: Kurt Buhler
updated: 2026-11-25
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# Configurar la actualización incremental

## Objetivo del script
Este script configura una política de actualización incremental en una tabla de importación, filtrada por una columna de fecha que usted seleccione. La actualización incremental se suele usar en tablas de hechos. Para obtener más información, consulta @incremental-refresh-about.

Al ejecutar el script, se muestran las tablas que tienen una única partición de Power Query (M), una columna de fecha y hora o de enteros y ninguna política de actualización. Selecciona una tabla, selecciona una columna e introduce los valores de la política en el cuadro de diálogo. El paso de filtro depende de la columna que selecciones:

- **Columna de fecha y hora:** el paso compara la columna con los parámetros `RangeStart` y `RangeEnd`. La columna debe tener el tipo Fecha/Hora en Power Query.
- **Clave de fecha entera (aaaaMMdd):** el paso convierte los parámetros con una función `fxDateTimeToInt`, que el script añade al modelo si no existe.

El script crea los parámetros `RangeStart` y `RangeEnd` si el modelo no los tiene. Si cancelas un cuadro de diálogo, el script finaliza sin realizar cambios.

> [!NOTE]
> El script añade un paso llamado `#"Incremental Refresh"` después del último paso de la expresión M de la partición y almacena el resultado en el `SourceExpression` de la tabla. Comprueba que el paso de filtro se pliegue hasta el origen de datos. Si no lo hace, mueve el paso a un punto en el que se pliegue y actualiza las referencias del paso.

## Script

### Implementar la actualización incremental para la columna seleccionada
```csharp
#r "System.Drawing"
// Configures an incremental refresh policy on the table you select.
// The policy filters on a datetime column or an integer date key (yyyyMMdd) column.
using System.Drawing;
using System.Text.RegularExpressions;
using System.Windows.Forms;

// Hide the 'Running Macro' spinbox
ScriptHelper.WaitFormVisible = false;

Func<Column, bool> isDateColumn = c =>
    c is DataColumn &&
    (c.DataType == DataType.DateTime || c.DataType == DataType.Int64);

// Candidate tables: no refresh policy yet, a single Power Query (M) partition and at least one date column
var candidateTables = Model.Tables.Where(t =>
    !t.EnableRefreshPolicy &&
    t.Partitions.Count == 1 &&
    t.Partitions[0].SourceType == PartitionSourceType.M &&
    t.Columns.Any(isDateColumn)
).ToList();

if (candidateTables.Count == 0)
{
    Error("No table qualifies for incremental refresh. A table needs a single Power Query (M) partition, a datetime or integer column and no existing refresh policy.");
    return;
}

var _Table = candidateTables.SelectTable(null, "Select a table (normally a fact table)");
if (_Table == null)
{
    Error("No table selected. Ending script without changes.");
    return;
}

var _Column = (DataColumn)_Table.Columns.Where(isDateColumn).SelectColumn(null, "Select a datetime or integer date key (yyyyMMdd) column.");
if (_Column == null)
{
    Error("No column selected. Ending script without changes.");
    return;
}

// Split the M expression at its final 'in' keyword
var _MExpression = _Table.Partitions[0].Expression;
var inKeywords = Regex.Matches(_MExpression, @"^[ \t]*in\b", RegexOptions.Multiline);
if (inKeywords.Count == 0)
{
    Error("The M expression of '" + _Table.Name + "' has no 'let ... in' structure. Add the filter step manually.");
    return;
}
var lastIn = inKeywords[inKeywords.Count - 1];
var stepsBeforeIn = _MExpression.Substring(0, lastIn.Index).TrimEnd();
var lastStep = _MExpression.Substring(lastIn.Index + lastIn.Length).Trim();

// Incremental Refresh Configuration
// Input box config
Font _fontConfig = new Font("Segoe UI", 11);

// Label for how long data should be stored
var storeDataLabel = new Label();
storeDataLabel.Text = "Store data in the last:";
storeDataLabel.Location = new Point(20, 20);
storeDataLabel.AutoSize = true;
storeDataLabel.Font = _fontConfig;

// User input for how long data should be stored
var storeDataTextBox = new TextBox();
storeDataTextBox.Location = new Point(storeDataLabel.Location.X + TextRenderer.MeasureText(storeDataLabel.Text, storeDataLabel.Font).Width + 20, storeDataLabel.Location.Y);
storeDataTextBox.Size = new Size(100, 20);
storeDataTextBox.Text = "3";
storeDataTextBox.Font = _fontConfig;

// User selection for how long data should be stored (granularity)
var storeDataComboBox = new ComboBox();
storeDataComboBox.Location = new Point(storeDataTextBox.Location.X + storeDataTextBox.Width + 20, storeDataLabel.Location.Y);
storeDataComboBox.Size = new Size(100, 20);
storeDataComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
storeDataComboBox.Items.AddRange(new object[] { "days", "months", "quarters", "years" });
storeDataComboBox.SelectedIndex = 3;
storeDataComboBox.Font = _fontConfig;

// Label for how much data should be refreshed
var refreshDataLabel = new Label();
refreshDataLabel.Text = "Refresh data in the last:";
refreshDataLabel.Location = new Point(20, storeDataLabel.Location.Y + storeDataLabel.Height + 15);
refreshDataLabel.AutoSize = true;
refreshDataLabel.Font = _fontConfig;

// User input for how much data should be refreshed
var refreshDataTextBox = new TextBox();
refreshDataTextBox.Location = new Point(storeDataTextBox.Location.X, refreshDataLabel.Location.Y);
refreshDataTextBox.Size = new Size(100, 20);
refreshDataTextBox.Text = "30";
refreshDataTextBox.Font = _fontConfig;

// User selection for how much data should be refreshed (Period)
var refreshDataComboBox = new ComboBox();
refreshDataComboBox.Location = new Point(storeDataComboBox.Location.X, refreshDataLabel.Location.Y);
refreshDataComboBox.Size = new Size(100, 20);
refreshDataComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
refreshDataComboBox.Items.AddRange(new object[] { "days", "months", "quarters", "years" });
refreshDataComboBox.SelectedIndex = 0;
refreshDataComboBox.Font = _fontConfig;

// User input to refresh full periods or not
var fullPeriodsCheckBox = new CheckBox();
fullPeriodsCheckBox.Text = "Refresh only full periods";
fullPeriodsCheckBox.Location = new Point(storeDataLabel.Location.X + 3, refreshDataLabel.Location.Y + refreshDataLabel.Height + 15);
fullPeriodsCheckBox.AutoSize = true;
fullPeriodsCheckBox.Font = _fontConfig;

// Form OK button
var okButton = new Button();
okButton.Text = "OK";
okButton.Location = new Point(storeDataLabel.Location.X, fullPeriodsCheckBox.Location.Y + fullPeriodsCheckBox.Height + 15);
okButton.MinimumSize = new Size(80, 25);
okButton.AutoSize = true;
okButton.DialogResult = DialogResult.OK;
okButton.Font = _fontConfig;

// Form cancel button
var cancelButton = new Button();
cancelButton.Text = "Cancel";
cancelButton.Location = new Point(okButton.Location.X + okButton.Width + 10, okButton.Location.Y);
cancelButton.MinimumSize = new Size(80, 25);
cancelButton.AutoSize = true;
cancelButton.DialogResult = DialogResult.Cancel;
cancelButton.Font = _fontConfig;

// Adjust the Location of the labels to align with the text boxes
storeDataLabel.Location = new Point(storeDataLabel.Location.X, storeDataLabel.Location.Y + 4);
refreshDataLabel.Location = new Point(refreshDataLabel.Location.X, refreshDataLabel.Location.Y + 4);

// Form config
var form = new Form();
form.Text = "Incremental Refresh configuration:";
form.AutoSize = true;
form.MinimumSize = new Size(450, 0);
form.FormBorderStyle = FormBorderStyle.FixedDialog;
form.MaximizeBox = false;
form.MinimizeBox = false;
form.StartPosition = FormStartPosition.CenterScreen;
form.AutoScaleMode = AutoScaleMode.Dpi;
form.AcceptButton = okButton;
form.CancelButton = cancelButton;

form.Controls.Add(storeDataLabel);
form.Controls.Add(storeDataTextBox);
form.Controls.Add(storeDataComboBox);
form.Controls.Add(refreshDataLabel);
form.Controls.Add(refreshDataTextBox);
form.Controls.Add(refreshDataComboBox);
form.Controls.Add(fullPeriodsCheckBox);
form.Controls.Add(okButton);
form.Controls.Add(cancelButton);

var result = form.ShowDialog();
form.Dispose();

if (result != DialogResult.OK)
{
    Error("Cancelled configuration! Ending script without changes.");
    return;
}

int storeDataPeriods, refreshDataPeriods;
if (!int.TryParse(storeDataTextBox.Text, out storeDataPeriods) || storeDataPeriods < 1 ||
    !int.TryParse(refreshDataTextBox.Text, out refreshDataPeriods) || refreshDataPeriods < 1)
{
    Error("Enter whole numbers greater than 0 for both periods. Ending script without changes.");
    return;
}

// Index order matches the combo box items: days, months, quarters, years
var granularities = new[] {
    RefreshGranularityType.Day,
    RefreshGranularityType.Month,
    RefreshGranularityType.Quarter,
    RefreshGranularityType.Year
};

// Add the RangeStart and RangeEnd parameters if they don't exist
if (!Model.Expressions.Contains("RangeStart"))
{
    Model.AddExpression(
        "RangeStart",
        @"#datetime(2023, 1, 1, 0, 0, 0) meta
[
    IsParameterQuery = true,
    IsParameterQueryRequired = true,
    Type = type datetime
]");
}

if (!Model.Expressions.Contains("RangeEnd"))
{
    Model.AddExpression(
        "RangeEnd",
        @"#datetime(2024, 1, 1, 0, 0, 0) meta
[
    IsParameterQuery = true,
    IsParameterQueryRequired = true,
    Type = type datetime
]");
}

// Configure the refresh policy
_Table.EnableRefreshPolicy = true;
_Table.RollingWindowGranularity = granularities[storeDataComboBox.SelectedIndex];
_Table.RollingWindowPeriods = storeDataPeriods;
_Table.IncrementalGranularity = granularities[refreshDataComboBox.SelectedIndex];
_Table.IncrementalPeriods = refreshDataPeriods;
// -1 refreshes complete periods only
_Table.IncrementalPeriodsOffset = fullPeriodsCheckBox.Checked ? -1 : 0;

// Power Query column reference, e.g. [#"Order Date"]
var mColumn = "[#\"" + _Column.SourceColumn.Replace("\"", "\"\"") + "\"]";

string rangeStart, rangeEnd;
if (_Column.DataType == DataType.Int64)
{
    // Integer date key (yyyyMMdd): convert the parameters with a helper function
    if (!Model.Expressions.Contains("fxDateTimeToInt"))
    {
        var dateTimeToInt = Model.AddExpression(
            "fxDateTimeToInt",
            @"(x as datetime) => Date.Year(x) * 10000 + Date.Month(x) * 100 + Date.Day(x)");
        dateTimeToInt.SetAnnotation("PBI_ResultType", "Function");
        dateTimeToInt.Kind = ExpressionKind.M;
    }
    rangeStart = @"fxDateTimeToInt(#""RangeStart"")";
    rangeEnd = @"fxDateTimeToInt(#""RangeEnd"")";
}
else
{
    // The column must have the Date/Time type in Power Query
    rangeStart = @"#""RangeStart""";
    rangeEnd = @"#""RangeEnd""";
}

// Add a filter step after the last step of the M expression
_Table.SourceExpression =
    stepsBeforeIn + ",\n" +
    @"    #""Incremental Refresh"" = Table.SelectRows(" + lastStep + ", each " +
    mColumn + " >= " + rangeStart + " and " + mColumn + " < " + rangeEnd + ")" +
    "\nin\n" +
    @"    #""Incremental Refresh""";

Info(
    "Configured the incremental refresh policy on '" + _Table.Name + "'.\n" +
    "\nStore data in the last: " + storeDataPeriods + " " + storeDataComboBox.SelectedItem +
    "\nRefresh data in the last: " + refreshDataPeriods + " " + refreshDataComboBox.SelectedItem +
    "\nRefresh only full periods: " + fullPeriodsCheckBox.Checked +
    "\n\nRight-click the table and select 'Apply refresh policy'." +
    "\nThen run a full refresh of the new policy partitions."
);
```
### Explicación
Después de que se ejecute el script, haz clic con el botón derecho en la tabla del **Explorador TOM** y selecciona **Aplicar política de actualización** para crear las particiones de la política. A continuación, ejecute una actualización completa de las nuevas particiones. Para consultar los pasos, ve a @incremental-refresh-setup.

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-configure-incremental-refresh.png" alt="El cuadro de diálogo que le ayuda a configurar la actualización incremental en función de las columnas seleccionadas" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Después de seleccionar la tabla y la columna, este cuadro de diálogo establece durante cuánto tiempo se almacenarán los datos, cuántos datos se actualizarán y si se actualizarán solo los periodos completos.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-configure-incremental-refresh-success.png" alt="Cuadro de diálogo de información del script que muestra los valores de la política de actualización configurados en la tabla Budget y los pasos siguientes" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> El cuadro de diálogo de confirmación enumera los valores configurados y los siguientes pasos.</figcaption>
</figure>