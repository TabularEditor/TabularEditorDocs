---
uid: script-implement-incremental-refresh
title: 设置增量刷新
author: Kurt Buhler
updated: 2026-11-25
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# 配置增量刷新

## 脚本用途
此脚本会在导入表上配置增量刷新策略，并按你选择的日期列进行筛选。增量刷新通常用于事实表。有关背景信息，请参阅 @incremental-refresh-about。

运行脚本时，它会列出具有单个 Power Query (M) 分区、datetime 或整数列且没有刷新策略的表。选择一个表，选择一列，然后在对话框中输入策略值。筛选步骤取决于您选择的列：

- **datetime 列：**该步骤将该列与 `RangeStart` 和 `RangeEnd` 参数进行比较。该列在 Power Query 中必须为日期/时间类型。
- **整数日期键 (yyyyMMdd)：**此步骤使用 `fxDateTimeToInt` 函数转换参数，如果该函数不存在，则脚本会将其添加到模型中。

如果模型中没有 `RangeStart` 和 `RangeEnd` 参数，脚本会创建这两个参数。如果你取消了对话框，脚本就会在不进行任何更改的情况下结束。

> [!NOTE]
> 该脚本在分区 M 表达式的最后一个步骤之后添加一个名为 `#"Incremental Refresh"` 的步骤，并将结果存储在表的 `SourceExpression` 中。检查筛选步骤是否折叠到数据源。如果未折叠，请将此步骤移动到可以折叠的位置，并更新步骤引用。

## 脚本

### 为所选列实现增量刷新
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
### 说明
脚本运行后，在 **TOM Explorer** 中右键单击该表，然后选择 **Apply refresh policy**，即可创建策略分区。然后对新分区执行完全刷新。有关步骤，请参阅 @incremental-refresh-setup。

## 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-configure-incremental-refresh.png" alt="帮助您根据所选列配置增量刷新的提示" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong>选择表和列后，此对话框将设置数据存储时长、要刷新的数据量以及是否仅刷新完整期间。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-configure-incremental-refresh-success.png" alt="列出在“预算”表中配置的刷新策略值和后续步骤的脚本信息对话框" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong>确认对话框列出了已配置的值和后续步骤。</figcaption>
</figure>