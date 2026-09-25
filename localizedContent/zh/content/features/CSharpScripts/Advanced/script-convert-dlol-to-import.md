---
uid: script-convert-dlol-to-import
title: 将 OneLake 上的 Direct Lake 表转换为导入模式
author: Morten Lønskov
updated: 2025-06-25
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 将 OneLake 上的 Direct Lake 转换为导入模式

## 脚本用途

This script converts Direct Lake on OneLake (DL/OL) to Import mode tables. 如 [Direct Lake 指南文章](xref:direct-lake-guidance) 中所述，我们需要将此类表上的 [EntityPartition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.entitypartitionsource?view=analysisservices-dotnet) 替换为导入模式下相应的常规 M 分区。

## 先决条件

你需要 **SQL Endpoint**，以及 Fabric **Warehouse** 或 **Lakehouse** 的 **名称**。 Both can be found in the Fabric portal.

You will also need to know the **Schema** of the table/materialized view you wish to connect to. For Lakehouses the default is dbo.

## 脚本

### 将 OneLake 上的 Direct Lake 表转换为导入模式

```csharp
// ===================================================================================
// Convert Direct Lake on OneLake tables back to Import mode
// ----------------------------------------
// This scripts converts the selected or all tables from Direct Lake on OneLake to import
//  It adds a shared expression named SQLEndpoint and replaces the existing DatabaseQuery if it no longer needed
// ===================================================================================
using System;
using System.Linq;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Drawing;

// -------------------------------------------------------------------
// 1) Scope‐picker dialog
// -------------------------------------------------------------------
public class ScopeSelectionDialog : Form
{
    public enum ScopeOption { OnlySelected, All, Cancel }
    public ScopeOption SelectedOption { get; private set; }

    public ScopeSelectionDialog(int selectedCount, int totalCount)
    {
        Text = "Choose tables to convert";
        AutoSize = true; AutoSizeMode = AutoSizeMode.GrowAndShrink;
        StartPosition = FormStartPosition.CenterParent;
        Padding = new Padding(20);

        var layout = new TableLayoutPanel {
            ColumnCount = 1, Dock = DockStyle.Fill,
            AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink
        };
        Controls.Add(layout);

        layout.Controls.Add(new Label {
            Text = $"You have {selectedCount} table(s) selected,\nand {totalCount} Direct Lake table(s) in the model.",
            AutoSize = true, TextAlign = ContentAlignment.MiddleLeft
        });

        var panel = new FlowLayoutPanel {
            FlowDirection = FlowDirection.LeftToRight,
            Dock = DockStyle.Fill, AutoSize = true,
            Padding = new Padding(0, 20, 0, 0)
        };

        var btnOnly = new Button {
            Text = "Only selected tables", AutoSize = true,
            DialogResult = DialogResult.OK
        };
        btnOnly.Click += (s, e) => SelectedOption = ScopeOption.OnlySelected;

        var btnAll = new Button {
            Text = "All tables", AutoSize = true,
            DialogResult = DialogResult.Retry
        };
        btnAll.Click += (s, e) => SelectedOption = ScopeOption.All;

        var btnCancel = new Button {
            Text = "Cancel", AutoSize = true,
            DialogResult = DialogResult.Cancel
        };
        btnCancel.Click += (s, e) => SelectedOption = ScopeOption.Cancel;

        panel.Controls.AddRange(new Control[] { btnOnly, btnAll, btnCancel });
        layout.Controls.Add(panel);

        AcceptButton = btnOnly;
        CancelButton = btnCancel;
    }
}

// -------------------------------------------------------------------
// 2) SQL‐import dialog (schema now required)
// -------------------------------------------------------------------
public class SqlImportDialog : Form
{
    public TextBox SqlEndpoint { get; }
    public TextBox DatabaseName { get; }
    public TextBox Schema { get; }
    private Button okButton;

    public SqlImportDialog(string endpoint, string db, string schema)
    {
        Text = "Convert Direct Lake → Import";
        AutoSize = true; AutoSizeMode = AutoSizeMode.GrowAndShrink;
        StartPosition = FormStartPosition.CenterParent;
        Padding = new Padding(20);

        var layout = new TableLayoutPanel {
            ColumnCount = 1, Dock = DockStyle.Fill,
            AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink
        };
        Controls.Add(layout);

        // Endpoint
        layout.Controls.Add(new Label { Text = "SQL Analytics Endpoint:", AutoSize = true });
        SqlEndpoint = new TextBox { Width = 800, Text = endpoint };
        layout.Controls.Add(SqlEndpoint);

        // Database
        layout.Controls.Add(new Label {
            Text = "Lakehouse/Warehouse Name:", Padding = new Padding(0, 20, 0, 0),
            AutoSize = true
        });
        DatabaseName = new TextBox { Width = 800, Text = db };
        layout.Controls.Add(DatabaseName);

        // Schema (required)
        layout.Controls.Add(new Label {
            Text = "Schema:", Padding = new Padding(0, 20, 0, 0),
            AutoSize = true
        });
        Schema = new TextBox { Width = 800, Text = schema };
        layout.Controls.Add(Schema);

        // Buttons
        var panel = new FlowLayoutPanel {
            FlowDirection = FlowDirection.RightToLeft,
            Dock = DockStyle.Fill, AutoSize = true,
            Padding = new Padding(0, 20, 0, 0)
        };
        okButton = new Button {
            Text = "OK", DialogResult = DialogResult.OK,
            AutoSize = true, Enabled = false
        };
        var cancel = new Button {
            Text = "Cancel", DialogResult = DialogResult.Cancel,
            AutoSize = true
        };
        panel.Controls.AddRange(new Control[] { okButton, cancel });
        layout.Controls.Add(panel);

        AcceptButton = okButton;
        CancelButton = cancel;

        // Only enable OK when all three fields are non-empty
        SqlEndpoint.TextChanged += Validate;
        DatabaseName.TextChanged += Validate;
        Schema.TextChanged += Validate;
        Shown += (s,e) => Validate(s,e);
    }

    private void Validate(object sender, EventArgs e)
    {
        okButton.Enabled =
            !string.IsNullOrWhiteSpace(SqlEndpoint.Text) &&
            !string.IsNullOrWhiteSpace(DatabaseName.Text) &&
            !string.IsNullOrWhiteSpace(Schema.Text);
    }
}

// -------------------------------------------------------------------
// 3) Main conversion logic
// -------------------------------------------------------------------
WaitFormVisible = false;
Application.UseWaitCursor = false;

// 3.1) Find all Direct Lake tables
var allDirectLake = Model.Tables
    .Where(t => t.Partitions.Count == 1
             && t.Partitions[0].SourceType == PartitionSourceType.Entity
             && t.Partitions[0].Mode == ModeType.DirectLake)
    .ToList();

// 3.2) And those you’ve selected
var selectedDirect = Selected.Tables
    .Cast<Table>()
    .Where(t => t.Partitions.Count == 1
             && t.Partitions[0].SourceType == PartitionSourceType.Entity
             && t.Partitions[0].Mode == ModeType.DirectLake)
    .ToList();

// 3.3) Ask scope
var scopeDialog = new ScopeSelectionDialog(selectedDirect.Count, allDirectLake.Count);
var dr = scopeDialog.ShowDialog();
if (dr == DialogResult.Cancel || scopeDialog.SelectedOption == ScopeSelectionDialog.ScopeOption.Cancel)
    return;

bool isAllTables = scopeDialog.SelectedOption == ScopeSelectionDialog.ScopeOption.All;
var tablesToConvert = isAllTables
    ? allDirectLake
    : selectedDirect;

if (tablesToConvert.Count == 0)
{
    Warning("No Direct Lake tables found in the chosen scope.");
    return;
}

// 3.4) Ask for connection + schema
var sqlDialog = new SqlImportDialog("", "", "");
if (sqlDialog.ShowDialog() == DialogResult.Cancel) return;

// 3.5) Upsert shared expression "SQLEndpoint"
const string sqlTemplate = @"let
    endpoint = Sql.Database(""{0}"",""{1}"")
in
    endpoint";
var sqlexpr = Model.Expressions.FirstOrDefault(e => e.Name == "SQLEndpoint")
           ?? Model.AddExpression("SQLEndpoint");
sqlexpr.Expression = string.Format(
    sqlTemplate,
    sqlDialog.SqlEndpoint.Text,
    sqlDialog.DatabaseName.Text);

// 3.6) M‐partition template
const string mTemplate = @"let
    Source = SQLEndpoint,
    Data = Source{{[Schema=""{0}"",Item=""{1}""]}}[Data]
in
    Data";

// 3.7) Swap partitions
foreach (var table in tablesToConvert)
{
    var oldP = table.Partitions[0];
    oldP.Name += "_old";

    var newP = table.AddMPartition(
        oldP.Name.Replace("_old", ""),
        string.Format(mTemplate, sqlDialog.Schema.Text, table.Name));
    newP.Mode = ModeType.Import;

    oldP.Delete();
}

// 3.8) If converting the **entire model**, delete the old DatabaseQuery expr
if (isAllTables)
{
    var oldDbq = Model.Expressions.FirstOrDefault(e => e.Name == "DatabaseQuery");
    if (oldDbq != null)
        oldDbq.Delete();   // TE3 API: Expression.Delete() removes it from the model
}

// 3.9) Ensure default mode is Import
Model.DefaultMode = ModeType.Import;

Info("Conversion complete: Direct Lake → Import" + 
     (isAllTables ? " (DatabaseQuery removed)" : "") + ".");
```

### 说明

The script first prompts the user to determine the scope of the conversion by choosing between converting only the selected tables or all tables in the model. It then identifies which tables are currently in Direct Lake mode within the chosen scope. If no applicable tables are found, or if the user cancels the dialog, the script terminates.

The user is then prompted to enter the SQL Analytics Endpoint, the name of the Lakehouse or Warehouse, and a required Schema name. The script ensures all three fields are populated before allowing the user to proceed.

接下来，脚本会使用提供的连接详细信息创建或更新一个名为 `SQLEndpoint` 的共享表达式。 This expression uses the `Sql.Database` connector to access the Lakehouse or Warehouse.

对于每个要转换的表，脚本都会创建一个新的导入模式 M 分区，该分区引用 `SQLEndpoint` 表达式，并使用指定的 Schema 和表名。 The existing Direct Lake partition is renamed and then removed, leaving only the new Import partition.

最后，如果你选择转换模型中的所有 Direct Lake 表，脚本会检查是否存在名为 `DatabaseQuery` 的共享表达式；如果存在，就将其删除。 The model's default storage mode is then set to Import, and a confirmation message is displayed.

## AI 使用声明

此脚本在大语言模型的协助下创建。
