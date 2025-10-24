---
uid: script-convert-dlsql-to-dlol
title: Convert Direct Lake on SQL to OneLake
author: Daniel Otykier
updated: 2025-06-20
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---

# Convert Direct Lake on SQL to OneLake

## Script Purpose

This script converts a model that uses Direct Lake on SQL (DL/SQL) to Direct Lake on OneLake (DL/OL). As laid out in the [Direct Lake guidance article](xref:direct-lake-guidance), this is a simple matter of updating the M query on the Shared Expression used by the Direct Lake partitions on the model, to use the [`AzureStorage.DataLake`](https://learn.microsoft.com/en-us/powerquery-m/azurestorage-datalake) connector instead of the [`Sql.Database`](https://learn.microsoft.com/en-us/powerquery-m/sql-database) connector.

## Prerequisites

You will need the **Workspace ID** as well as the **Resource ID** of your Fabric Warehouse or Lakehouse. Both are GUIDs that are part of the URL when navigating to the Warehouse or Lakehouse in the Fabric portal:

![Lakehouse Warehouse URL](~/content/assets/images/lakehouse-warehouse-url.png)

In the screenshot above, the **Workspace ID** of the lakehouse is highlighted in blue, while the **Resource ID** is highlighted in green.

## Script

### Convert Direct Lake on SQL to OneLake

```csharp
// ==================================================================
// Convert Direct Lake on SQL to OneLake
// -------------------------------------
// 
// This script detects if the current model uses Direct Lake on SQL
// and suggests to upgrade the model to Direct Lake on OneLake.
//
// You will need the Workspace ID and the ID of your Fabric Warehouse
// or Lakehouse (both are GUIDs).
// ==================================================================

// Find the Shared Expression that is being used by EntityPartitions on the model:
using System.Windows.Forms;
using System.Drawing;

var partition = Model.AllPartitions.OfType<EntityPartition>()
    .FirstOrDefault(e => e.Mode == ModeType.DirectLake && e.ExpressionSource != null);
var expressionSource = partition == null ? null : partition.ExpressionSource;

if (expressionSource == null)
{
    Warning("Your model does not seem to contain any tables in Direct Lake mode.");
    return;
}

if (!expressionSource.Expression.Contains("Sql.Database"))
{
    Warning("This model is not configured for Direct Lake over SQL.");
    return;
}

WaitFormVisible = false;
Application.UseWaitCursor = false;
var promptDialog = new UrlNameDialog();
if(promptDialog.ShowDialog() == DialogResult.Cancel) return;

const string mTemplate = @"let
    Source = AzureStorage.DataLake(""https://onelake.dfs.fabric.microsoft.com/%workspaceId%/%resourceId%"", [HierarchicalNavigation=true])
in
    Source";

expressionSource.Expression = mTemplate.Replace("%workspaceId%", promptDialog.WorkspaceId.Text).Replace("%resourceId%", promptDialog.ResourceId.Text);

if(!string.IsNullOrEmpty(Model.Collation))
{
    Model.Collation = null;
    Info("Model successfully converted to Direct Lake on OneLake. You may need to deploy it as a new semantic model, since the model collation was modified.");
}
else
    Info("Model successfully converted to Direct Lake on OneLake.");

// UI code below this line:
public class UrlNameDialog : Form
{
    public TextBox WorkspaceId { get; private set; }
    public TextBox ResourceId { get; private set; }
    private Button okButton;

    public UrlNameDialog()
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
        WorkspaceId = new TextBox { Width = 1000 };
        mainLayout.Controls.Add(WorkspaceId);

        // Resource ID
        mainLayout.Controls.Add(new Label { Text = "Fabric Warehouse / Lakehouse ID (GUID):", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
        ResourceId = new TextBox { Width = 1000 };
        mainLayout.Controls.Add(ResourceId);

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
    }
    
    private void Validate(object sender, EventArgs e)
    {
        Guid g;
        okButton.Enabled = Guid.TryParse(WorkspaceId.Text, out g) && Guid.TryParse(ResourceId.Text, out g);
    }
}
```

### Explanation

The script first attempts to locate an EntityPartition that is configured for Direct Lake mode and has an Expression Source (a reference to a Shared Expression). If no such partition is found, it displays a warning message and exits. Moreover, the referenced Shared Expression must specify the `Sql.Database` connector, which indicates that the model is currently using Direct Lake on SQL.

Once the script confirms that the model is using Direct Lake on SQL, it prompts the user to input the **Workspace ID** and **Resource ID** of the Fabric Warehouse or Lakehouse. The script then replaces the `Sql.Database` connector in the Shared Expression with the `AzureStorage.DataLake` connector, using the provided IDs.

Finally, if the model has a collation set, it clears it, as this change requires a new collation. The script then informs the user that the model has been successfully converted to Direct Lake on OneLake.