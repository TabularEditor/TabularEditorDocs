---
uid: script-convert-dlol-to-import
title: 将 OneLake 上的 Direct Lake 转换为导入模式
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

此脚本将 OneLake 上的 Direct Lake（DL/OL）转换为导入模式表。 正如 [Direct Lake guidance article](xref:direct-lake-guidance) 中所述，我们需要将这类表上的 [EntityPartition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.entitypartitionsource?view=analysisservices-dotnet) 替换为导入模式下对应的常规 M 分区。

## 先决条件

你需要 **SQL Endpoint**，以及 Fabric Warehouse 或 Lakehouse 的 **名称**。 两者都可以在 Fabric 门户中找到。

你还需要知道要连接的表/物化视图的 **Schema**。 对于 Lakehouse，默认值为 dbo。

## 脚本

### 将 OneLake 上的 Direct Lake 表转换为导入模式

```csharp
// ===================================================================================
// 将 OneLake 上的 Direct Lake 表转换回导入模式
// ----------------------------------------
// 此脚本会将选中的表或所有表从 OneLake 上的 Direct Lake 转换为导入模式
//  它会添加名为 SQLEndpoint 的共享表达式，并在不再需要时删除现有的 DatabaseQuery
// ===================================================================================
using System;
using System.Linq;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Drawing;

// -------------------------------------------------------------------
// 1) 范围选择对话框
// -------------------------------------------------------------------
public class ScopeSelectionDialog : Form
{
    public enum ScopeOption { OnlySelected, All, Cancel }
    public ScopeOption SelectedOption { get; private set; }

    public ScopeSelectionDialog(int selectedCount, int totalCount)
    {
        Text = "选择要转换的表";
        AutoSize = true; AutoSizeMode = AutoSizeMode.GrowAndShrink;
        StartPosition = FormStartPosition.CenterParent;
        Padding = new Padding(20);

        var layout = new TableLayoutPanel {
            ColumnCount = 1, Dock = DockStyle.Fill,
            AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink
        };
        Controls.Add(layout);

        layout.Controls.Add(new Label {
            Text = $"你已选择 {selectedCount} 个表，\n模型中共有 {totalCount} 个 Direct Lake 表。",
            AutoSize = true, TextAlign = ContentAlignment.MiddleLeft
        });

        var panel = new FlowLayoutPanel {
            FlowDirection = FlowDirection.LeftToRight,
            Dock = DockStyle.Fill, AutoSize = true,
            Padding = new Padding(0, 20, 0, 0)
        };

        var btnOnly = new Button {
            Text = "仅转换所选表", AutoSize = true,
            DialogResult = DialogResult.OK
        };
        btnOnly.Click += (s, e) => SelectedOption = ScopeOption.OnlySelected;

        var btnAll = new Button {
            Text = "所有表", AutoSize = true,
            DialogResult = DialogResult.Retry
        };
        btnAll.Click += (s, e) => SelectedOption = ScopeOption.All;

        var btnCancel = new Button {
            Text = "取消", AutoSize = true,
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
// 2) SQL 导入对话框（现在需要 Schema）
// -------------------------------------------------------------------
public class SqlImportDialog : Form
{
    public TextBox SqlEndpoint { get; }
    public TextBox DatabaseName { get; }
    public TextBox Schema { get; }
    private Button okButton;

    public SqlImportDialog(string endpoint, string db, string schema)
    {
        Text = "转换 Direct Lake → 导入";
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
            Text = "Lakehouse/Warehouse 名称:", Padding = new Padding(0, 20, 0, 0),
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
            Text = "取消", DialogResult = DialogResult.Cancel,
            AutoSize = true
        };
        panel.Controls.AddRange(new Control[] { okButton, cancel });
        layout.Controls.Add(panel);

        AcceptButton = okButton;
        CancelButton = cancel;

        // 仅当三个字段都非空时才启用 OK
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
// 3) 主转换逻辑
// -------------------------------------------------------------------
WaitFormVisible = false;
Application.UseWaitCursor = false;

// 3.1) 查找所有 Direct Lake 表
var allDirectLake = Model.Tables
    .Where(t => t.Partitions.Count == 1
             && t.Partitions[0].SourceType == PartitionSourceType.Entity
             && t.Partitions[0].Mode == ModeType.DirectLake)
    .ToList();

// 3.2) 以及你已选择的 Direct Lake 表
var selectedDirect = Selected.Tables
    .Cast<Table>()
    .Where(t => t.Partitions.Count == 1
             && t.Partitions[0].SourceType == PartitionSourceType.Entity
             && t.Partitions[0].Mode == ModeType.DirectLake)
    .ToList();

// 3.3) 询问范围
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
    Warning("在所选范围内未找到 Direct Lake 表。");
    return;
}

// 3.4) 询问连接信息 + Schema
var sqlDialog = new SqlImportDialog("", "", "");
if (sqlDialog.ShowDialog() == DialogResult.Cancel) return;

// 3.5) 新增或更新共享表达式 "SQLEndpoint"
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

// 3.6) M 分区模板
const string mTemplate = @"let
    Source = SQLEndpoint,
    Data = Source{{[Schema=""{0}"",Item=""{1}""]}}[Data]
in
    Data";

// 3.7) 替换分区
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

// 3.8) 如果转换的是**整个模型**，删除旧的 DatabaseQuery 表达式
if (isAllTables)
{
    var oldDbq = Model.Expressions.FirstOrDefault(e => e.Name == "DatabaseQuery");
    if (oldDbq != null)
        oldDbq.Delete();   // TE3 API: Expression.Delete() removes it from the model
}

// 3.9) 确保默认模式为导入模式
Model.DefaultMode = ModeType.Import;

Info("转换完成：Direct Lake → 导入" + 
     (isAllTables ? " (已删除 DatabaseQuery)" : "") + "。");
```

### 说明

脚本会先提示你选择转换范围：只转换所选表，或转换模型中的所有表。 然后，它会识别在所选范围内当前处于 Direct Lake 模式的表。 如果没找到符合条件的表，或者你取消了对话框，脚本就会停止运行。

接着会提示你输入 SQL analytics endpoint、Lakehouse 或 Warehouse 的名称，以及必填的 Schema 名称。 脚本会确保这三个字段均已填写后，才允许你继续。

接下来，脚本会使用你提供的连接信息创建或更新名为 `SQLEndpoint` 的共享表达式。 该表达式使用 `Sql.Database` 连接器来访问 Lakehouse 或 Warehouse。

对于每个要转换的表，脚本会创建一个新的导入模式 M 分区：引用 `SQLEndpoint` 表达式，并使用指定的 Schema 和表名。 现有的 Direct Lake 分区会先被重命名，然后删除，最终仅保留新的导入分区。

最后，如果你选择转换模型中的所有 Direct Lake 表，脚本会检查是否存在名为 `DatabaseQuery` 的共享表达式；若存在则删除。 然后把模型的默认存储模式设置为导入模式，并显示一条确认信息。

## AI 使用免责声明

此脚本在 LLM 的帮助下创建。
