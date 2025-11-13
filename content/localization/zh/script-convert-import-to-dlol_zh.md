---
uid: script-convert-import-to-dlol
title: 将导入转换为 OneLake 上的直接湖
author: Daniel Otykier
updated: 2025-06-20
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---

# 将导入转换为 OneLake 上的直接湖

## 脚本用途

此脚本将导入模式表转换为 OneLake 上的直接湖 (DL/OL)。 如 [Direct Lake 指南文章](xref:direct-lake-guidance) 中所述，我们需要用单个 [EntityPartition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.entitypartitionsource?view=analysisservices-dotnet) 替换此类表上的分区，该分区指定 Fabric Lakehouse 或 Warehouse 中表/物化视图的名称和架构，同时引用使用 [`AzureStorage.DataLake`](https://learn.microsoft.com/en-us/powerquery-m/azurestorage-datalake) (OneLake) 连接器的共享表达式。

## 先决条件

您将需要 **工作区 ID** 以及 Fabric Warehouse 或 Lakehouse 的 **资源 ID**。 两者都是 GUID，是在 Fabric 门户中导航到 Warehouse 或 Lakehouse 时 URL 的一部分：

![Lakehouse Warehouse URL](~/content/assets/images/lakehouse-warehouse-url.png)

在上面的屏幕截图中，lakehouse 的 **工作区 ID** 以蓝色突出显示，而 **资源 ID** 以绿色突出显示。

如果您连接到支持架构的 Fabric Warehouse 或 Lakehouse，您还需要了解要连接的表/物化视图的 **架构**。

> [!WARNING]
> 导入模式下的表可以在其分区内定义转换（使用 SQL 或 M 表达）。 转换为 OneLake 直接湖模式时，这些转换将丢失，因为直接湖分区必须包含源表/物化视图中列的 1:1 映射。 因此，在运行此脚本之前，请确保源表/物化视图在 Fabric Warehouse 或 Lakehouse 中的名称与在语义模型中的名称相同，并且列映射正确。

## 脚本

### 将导入模式表转换为 OneLake 上的直接湖

```csharp
// ==================================================================
// 将导入转换为 OneLake 上的直接湖
// ----------------------------------------
// 
// 此脚本将选定的（导入）表或模型中的所有表
// 转换为 OneLake 上的直接湖表（如果未选择任何内容）。
//
// 警告：脚本假设表在 Fabric Warehouse 或 Lakehouse
// 中的名称与在语义模型中的名称相同。
// 此外，导入分区中的任何转换（基于 M 或 SQL）都将丢失，
// 因为直接湖模式表必须包含与源表/物化视图完全相同的列。
//
// 您将需要工作区 ID 和 Fabric Warehouse
// 或 Lakehouse 的 ID（两者都是 GUID）。
// ==================================================================

// 查找模型上的 EntityPartitions 使用的共享表达式：
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
    Warning("模型或选择不包含任何导入模式的表");
    return;
}
else
{
    var result = MessageBox.Show("以下表将被转换：\r\n\r\n" + string.Join("\r\n", importTables.Select(t => "  - " + t.Name)) +
        "\r\n\r\n继续？",
        "确认转换？", MessageBoxButtons.OKCancel, MessageBoxIcon.Question);
    if (result == DialogResult.Cancel) return;
}

string workspaceId = string.Empty;
string resourceId = string.Empty;
var sharedExpression = Model.Expressions.FirstOrDefault(e => e.Expression.Contains("AzureStorage.DataLake"));
if(sharedExpression != null)
{
    // 提取现有的工作区 ID 和资源 ID
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

Info("表已转换为 OneLake 上的直接湖模式。");

public class UrlNameDialog : Form
{
    public TextBox WorkspaceId { get; private set; }
    public TextBox ResourceId { get; private set; }
    public TextBox Schema { get; private set; }
    private Button okButton;

    public UrlNameDialog(string workspaceId, string resourceId)
    {
        Text = "将直接湖从 SQL 转换为 OneLake";
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

        // 工作区 ID
        mainLayout.Controls.Add(new Label { Text = "工作区 ID (GUID):", AutoSize = true });
        WorkspaceId = new TextBox { Width = 1000, Text = workspaceId };
        mainLayout.Controls.Add(WorkspaceId);

        // 资源 ID
        mainLayout.Controls.Add(new Label { Text = "Fabric Warehouse / Lakehouse ID (GUID):", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
        ResourceId = new TextBox { Width = 1000, Text = resourceId };
        mainLayout.Controls.Add(ResourceId);

        // 架构
        mainLayout.Controls.Add(new Label { Text = "架构（可选）:", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
        Schema = new TextBox { Width = 1000 };
        mainLayout.Controls.Add(Schema);


        // 按钮
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

脚本首先确定是转换模型中的所有导入模式表还是仅转换用户选择的表。 然后检查是否存在任何此类表，并在继续之前提示用户确认。

脚本然后尝试定位使用 `AzureStorage.DataLake` 连接器的共享表达式。 如果存在这样的表达式，它从其表达式中提取工作区 ID 和资源 ID。 如果找不到这样的表达式，它会创建一个新的。

然后提示用户输入 Fabric Warehouse 或 Lakehouse 的工作区 ID 和资源 ID，以及可选的架构名称。 如果更改了现有的共享表达式，脚本会用使用提供的 ID 的新表达式替换它。

最后，对于每个导入模式表，脚本创建一个具有指定名称和架构的新 EntityPartition，引用共享表达式。 然后它删除该表上不是新创建的 EntityPartition 的任何现有分区。