---
uid: script-convert-import-to-dlol
title: 在 OneLake 上将导入模式表转换为 Direct Lake
author: Daniel Otykier
updated: 2025-06-20
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 在 OneLake 上将导入模式表转换为 Direct Lake

## 脚本用途

此脚本将导入模式表转换为 OneLake 上的 Direct Lake（DL/OL）。 正如 [Direct Lake 指南文章](xref:direct-lake-guidance) 中所述，我们需要将这类表的分区替换为单个 [EntityPartition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.entitypartitionsource?view=analysisservices-dotnet)。该分区会指定 Fabric Lakehouse 或 Warehouse 中表/物化视图的名称和架构，并引用一个使用 [`AzureStorage.DataLake`](https://learn.microsoft.com/en-us/powerquery-m/azurestorage-datalake)（OneLake）连接器的共享表达式（Shared Expression）。

## 先决条件

你需要 **Workspace ID**，以及 Fabric Warehouse 或 Lakehouse 的 **Resource ID**。 这两者都是 GUID，当你在 Fabric 门户中导航到 Warehouse 或 Lakehouse 时，它们会出现在 URL 中：

![Lakehouse Warehouse URL](~/content/assets/images/lakehouse-warehouse-url.png)

在上面的截图中，Lakehouse 的 **Workspace ID** 用蓝色标注，**Resource ID** 用绿色标注。

如果你要连接到支持架构的 Fabric Warehouse 或 Lakehouse，还需要知道你要连接的表/物化视图的 **Schema**。

> [!WARNING]
> 导入模式表可以在其分区中定义转换（使用 SQL 或 M 表达）。 当转换为 OneLake 上的 Direct Lake 模式时，这些转换将会丢失，因为 Direct Lake 分区必须与源表/物化视图中的列保持 1:1 映射。 因此，在运行此脚本之前，请确保源表/物化视图在 Fabric Warehouse 或 Lakehouse 中的名称与语义模型中的名称一致，并且列映射正确。

## 脚本

### 将导入模式表转换为 OneLake 上的 Direct Lake

```csharp
// ==================================================================
// 将导入模式转换为 OneLake 上的 Direct Lake
// ----------------------------------------
// 
// 此脚本会将所选的 (导入) 表；如果未选择任何内容，则会将模型中的所有表
// 转换为 OneLake 上的 Direct Lake 表。
//
// 警告：脚本假设这些表在 Fabric Warehouse 或 Lakehouse 中的名称
// 与其在语义模型中的名称一致。
// 另外，导入分区中的任何转换 (基于 M 或 SQL) 都会丢失，
// 因为 Direct Lake 模式表必须与源表/物化视图保持 1:1 相同的列。
//
// 你需要 Workspace ID，以及 Fabric Warehouse
// 或 Lakehouse 的 ID (两者都是 GUID)。
// ==================================================================

// 查找模型中 EntityPartition 正在使用的共享表达式：
using System.Windows.Forms;
using System.Drawing;
using System.Data;

IEnumerable<Table> tableSource = Selected.Context.HasFlag(Context.Tables) ? (IEnumerable<Table>)Selected.Tables : Model.Tables;
var importTables = tableSource.Where(t => t.Partitions.All(p => 
            (p.SourceType == PartitionSourceType.Query || p.SourceType == PartitionSourceType.M) && 
            (p.Mode == ModeType.Import || (p.Mode == ModeType.Default && Model.DefaultMode == ModeType.Import))))
    .ToList();

WaitFormVisible = false;
Application.UseWaitCursor = false;

if(importTables.Count == 0)
{
    Warning("模型或所选内容不包含任何导入模式表");
    return;
}
else
{
    var result = MessageBox.Show("将转换以下表：\r\n\r\n" + string.Join("\r\n", importTables.Select(t => "  - " + t.Name)) +
        "\r\n\r\n继续？",
        "确认转换？", MessageBoxButtons.OKCancel, MessageBoxIcon.Question);
    if (result == DialogResult.Cancel) return;
}

string workspaceId = string.Empty;
string resourceId = string.Empty;
var sharedExpression = Model.Expressions.FirstOrDefault(e => e.Expression.Contains("AzureStorage.DataLake"));
if(sharedExpression != null)
{
    // 提取现有的 Workspace ID 和 Resource ID
    var ix = sharedExpression.Expression.IndexOf("onelake.dfs.fabric.microsoft.com");
    var url = sharedExpression.Expression.Substring(ix + 33, 73);
    var guids = url.Split('/');
    Guid g;
    if(Guid.TryParse(guids[0], out g) && Guid.TryParse(guids[1], out g))
    {
        workspaceId = guids[0];
        resourceId = guids[1];
    }
}

var promptDialog = new UrlNameDialog(workspaceId, resourceId);
if(promptDialog.ShowDialog() == DialogResult.Cancel) return;

const string mTemplate = @"let
    Source = AzureStorage.DataLake(""https://onelake.dfs.fabric.microsoft.com/%workspaceId%/%resourceId%"", [HierarchicalNavigation=true])
in
    Source";

if(promptDialog.WorkspaceId.Text != workspaceId || promptDialog.ResourceId.Text != resourceId)
{
    if (sharedExpression == null) sharedExpression = Model.AddExpression("DatabaseQuery");
    sharedExpression.Expression = mTemplate.Replace("%workspaceId%", promptDialog.WorkspaceId.Text).Replace("%resourceId%", promptDialog.ResourceId.Text);
}

foreach(var table in importTables)
{
    var ep = table.AddEntityPartition();
    ep.EntityName = table.Name;
    ep.ExpressionSource = sharedExpression;
    ep.SchemaName = promptDialog.Schema.Text;
    ep.Mode = ModeType.DirectLake;
    foreach(var p in table.Partitions.ToList()) if(p != ep) p.Delete();
    ep.Name = table.Name;
}

Info("表已转换为 OneLake 上的 Direct Lake 模式。");

public class UrlNameDialog : Form
{
    public TextBox WorkspaceId { get; private set; }
    public TextBox ResourceId { get; private set; }
    public TextBox Schema { get; private set; }
    private Button okButton;

    public UrlNameDialog(string workspaceId, string resourceId)
    {
        Text = "将 SQL 上的 Direct Lake 转换到 OneLake";
        AutoSize = true;
        AutoSizeMode = AutoSizeMode.GrowAndShrink;
        StartPosition = FormStartPosition.CenterParent;
        Padding = new Padding(20);

        var mainLayout = new TableLayoutPanel
        {
            ColumnCount = 1,
            RowCount = 3,
            Dock = DockStyle.Fill,
            AutoSize = true,
            AutoSizeMode = AutoSizeMode.GrowAndShrink
        };
        Controls.Add(mainLayout);

        // Workspace ID
        mainLayout.Controls.Add(new Label { Text = "Workspace ID (GUID):", AutoSize = true });
        WorkspaceId = new TextBox { Width = 1000, Text = workspaceId };
        mainLayout.Controls.Add(WorkspaceId);

        // Resource ID
        mainLayout.Controls.Add(new Label { Text = "Fabric Warehouse / Lakehouse ID (GUID):", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
        ResourceId = new TextBox { Width = 1000, Text = resourceId };
        mainLayout.Controls.Add(ResourceId);

        // Schema
        mainLayout.Controls.Add(new Label { Text = "Schema (optional):", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
        Schema = new TextBox { Width = 1000 };
        mainLayout.Controls.Add(Schema);


        // Buttons
        var buttonPanel = new FlowLayoutPanel
        {
            Padding = new Padding(0, 20, 0, 0),
            FlowDirection = FlowDirection.RightToLeft,
            Dock = DockStyle.Fill,
            AutoSize = true
        };

        okButton = new Button { Text = "确定", DialogResult = DialogResult.OK, AutoSize = true, Enabled = false };
        var cancelButton = new Button { Text = "取消", DialogResult = DialogResult.Cancel, AutoSize = true };
        buttonPanel.Controls.Add(okButton);
        buttonPanel.Controls.Add(cancelButton);

        AcceptButton = okButton;
        CancelButton = cancelButton;
        mainLayout.Controls.Add(buttonPanel);

        WorkspaceId.TextChanged += Validate;
        ResourceId.TextChanged += Validate;
        this.Shown += Validate;
    }
    
    private void Validate(object sender, EventArgs e)
    {
        Guid g;
        okButton.Enabled = Guid.TryParse(WorkspaceId.Text, out g) && Guid.TryParse(ResourceId.Text, out g);
    }
}
```

### 说明

脚本首先判断：是转换模型中所有导入模式表，还是仅转换用户选中的表。 接着，脚本会检查是否存在此类表，并在继续之前提示用户确认。

脚本随后会尝试查找一个使用 `AzureStorage.DataLake` 连接器的共享表达式。 如果存在这样的表达式，它会从该表达式中提取 Workspace ID 和 Resource ID。 如果未找到这样的表达式，它会创建一个新的表达式。

随后会提示用户输入 Fabric Warehouse 或 Lakehouse 的 Workspace ID 和 Resource ID，以及一个可选的 Schema 名称。 如果这些 ID 有所更改，脚本会用一个使用所提供 ID 的新共享表达式替换现有共享表达式。

最后，对于每个导入模式表，脚本都会创建一个新的 EntityPartition，并使用指定的名称和架构，同时引用共享表达式。 随后，它会删除表上除新创建的 EntityPartition 之外的所有现有分区。