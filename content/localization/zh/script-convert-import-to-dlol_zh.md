---
uid: script-convert-import-to-dlol
title: Convert Import to Direct Lake on OneLake
author: Daniel Otykier
updated: 2025-06-20
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---

# Convert Import to Direct Lake on OneLake

## Script Purpose

This script converts Import mode tables to Direct Lake on OneLake (DL/OL). As laid out in the [Direct Lake guidance article](xref:direct-lake-guidance), we need to replace the partition(s) on such tables with a single [EntityPartition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.entitypartitionsource?view=analysisservices-dotnet), which specifies the name and schema of the table/materialized view in the Fabric Lakehouse or Warehouse, while referencing a Shared Expression that uses the [`AzureStorage.DataLake`](https://learn.microsoft.com/en-us/powerquery-m/azurestorage-datalake) (OneLake) connector.

## Prerequisites

You will need the **Workspace ID** as well as the **Resource ID** of your Fabric Warehouse or Lakehouse. Both are GUIDs that are part of the URL when navigating to the Warehouse or Lakehouse in the Fabric portal:

![Lakehouse Warehouse URL](~/content/assets/images/lakehouse-warehouse-url.png)

In the screenshot above, the **Workspace ID** of the lakehouse is highlighted in blue, while the **Resource ID** is highlighted in green.

If you are connecting to a Fabric Warehouse or a Lakehouse that supports schemas, you will also need to know the **Schema** of the table/materialized view you wish to connect to.

> [!WARNING]
> Tables in Import mode can define transformations inside their partitions (expressed using SQL or M). These transformations will be lost when converting to Direct Lake on OneLake mode, as the Direct Lake partitions must contain a 1:1 mapping of the columns in the source table/materialized view. Therefore, ensure that the source table/materialized view has the same name in the Fabric Warehouse or Lakehouse as it does in the semantic model, and that column mappings are correct before running this script.

## Script

### Convert Import mode tables to Direct Lake on OneLake

```csharp
// ==================================================================
// Convert Import to Direct Lake on OneLake
// ----------------------------------------
// 
// This script converts the selected (import) tables, or all tables
// in the model, if nothing is selected, to Direct Lake on OneLake
// tables.
//
// WARNING: The script assumes that tables have the same name in the
// Fabric Warehouse or Lakehouse, as they do in the semantic model.
// Moreover, any transformations (M or SQL based) in the import
// partitions, will be lost, as Direct Lake mode tables must contain
// 1:1 the same columns as the source table/materialized view.
//
// You will need the Workspace ID and the ID of your Fabric Warehouse
// or Lakehouse (both are GUIDs).
// ==================================================================

// Find the Shared Expression that is being used by EntityPartitions on the model:
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
    Warning("Model or selection does not contain any tables in import mode");
    return;
}
else
{
    var result = MessageBox.Show("The following tables will be converted:\r\n\r\n" + string.Join("\r\n", importTables.Select(t => "  - " + t.Name)) +
        "\r\n\r\nProceed?",
        "Confirm conversion?", MessageBoxButtons.OKCancel, MessageBoxIcon.Question);
    if (result == DialogResult.Cancel) return;
}

string workspaceId = string.Empty;
string resourceId = string.Empty;
var sharedExpression = Model.Expressions.FirstOrDefault(e => e.Expression.Contains("AzureStorage.DataLake"));
if(sharedExpression != null)
{
    // Extract existing workspace ID and resource ID
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

Info("Tables converted to Direct Lake on OneLake mode.");

public class UrlNameDialog : Form
{
    public TextBox WorkspaceId { get; private set; }
    public TextBox ResourceId { get; private set; }
    public TextBox Schema { get; private set; }
    private Button okButton;

    public UrlNameDialog(string workspaceId, string resourceId)
    {
        Text = "Convert Direct Lake on SQL to OneLake";
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

        okButton = new Button { Text = "OK", DialogResult = DialogResult.OK, AutoSize = true, Enabled = false };
        var cancelButton = new Button { Text = "Cancel", DialogResult = DialogResult.Cancel, AutoSize = true };
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

### Explanation

The script first determines whether to convert all Import mode tables in the model or only those selected by the user. It then checks if any such tables exist and prompts the user for confirmation before proceeding.

The script then attempts to locate a Shared Expression that uses the `AzureStorage.DataLake` connector. If such an expression exists, it extracts the Workspace ID and Resource ID from its expression. If no such expression is found, it creates a new one.

The user is then prompted to input the Workspace ID and Resource ID of the Fabric Warehouse or Lakehouse, as well as an optional Schema name. The script replaces the existing Shared Expression with a new one that uses the provided IDs, if they were changed.

Finally, for each Import mode table, the script creates a new EntityPartition with the specified name and schema, referencing the Shared Expression. It then deletes any existing partitions on the table that are not the newly created EntityPartition.