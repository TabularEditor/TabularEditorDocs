---
uid: script-convert-dlsql-to-dlol
title: Convertir Direct Lake sobre SQL a OneLake
author: Daniel Otykier
updated: 2025-06-20
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Convertir Direct Lake sobre SQL a OneLake

## Objetivo del script

Este script convierte un modelo que usa Direct Lake en SQL (DL/SQL) a Direct Lake en OneLake (DL/OL). Tal como se indica en el [artículo de directrices de Direct Lake](xref:direct-lake-guidance), esto consiste simplemente en actualizar la consulta M de la Shared Expression que usan las particiones de Direct Lake del modelo para que use el conector [`AzureStorage.DataLake`](https://learn.microsoft.com/en-us/powerquery-m/azurestorage-datalake) en lugar del conector [`Sql.Database`](https://learn.microsoft.com/en-us/powerquery-m/sql-database).

## Requisitos previos

Necesitará el **Workspace ID**, así como el **Resource ID** de su Warehouse o Lakehouse de Fabric. Ambos son GUID que forman parte de la URL al navegar al Warehouse o Lakehouse en el portal de Fabric:

![URL de Lakehouse/Warehouse](~/content/assets/images/lakehouse-warehouse-url.png)

En la captura de pantalla anterior, el **Workspace ID** del Lakehouse se resalta en azul, mientras que el **Resource ID** se resalta en verde.

## Script

### Convertir Direct Lake sobre SQL a OneLake

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

### Explicación

El script primero intenta localizar un EntityPartition que esté configurado en modo Direct Lake y que tenga un Expression Source (una referencia a una Shared Expression). Si no se encuentra ninguna partición de ese tipo, muestra un mensaje de advertencia y finaliza. Además, la Shared Expression a la que se hace referencia debe especificar el conector `Sql.Database`, lo que indica que el modelo está usando actualmente Direct Lake en SQL.

Cuando el script confirma que el modelo usa Direct Lake en SQL, solicita al usuario que introduzca el **ID del Workspace** y el **ID de recurso** del Warehouse o Lakehouse de Fabric. A continuación, el script reemplaza el conector `Sql.Database` de la Shared Expression por el conector `AzureStorage.DataLake`, utilizando los ID proporcionados.

Por último, si el modelo tiene una intercalación definida, la borra, ya que este cambio requiere una nueva intercalación. A continuación, el script informa al usuario de que el modelo se ha convertido correctamente a Direct Lake en OneLake.