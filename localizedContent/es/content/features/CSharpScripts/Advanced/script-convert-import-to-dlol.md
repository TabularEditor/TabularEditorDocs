---
uid: script-convert-import-to-dlol
title: Convertir de modo Import a Direct Lake en OneLake
author: Daniel Otykier
updated: 2025-06-20
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Convertir de modo Import a Direct Lake en OneLake

## Propósito del script

Este script convierte tablas en modo Import a Direct Lake en OneLake (DL/OL). Tal y como se indica en el [artículo de guía de Direct Lake](xref:direct-lake-guidance), debemos reemplazar la partición (o particiones) de estas tablas por una única [EntityPartition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.entitypartitionsource?view=analysisservices-dotnet), que especifica el nombre y el esquema de la tabla/vista materializada en el Lakehouse o Warehouse de Fabric, a la vez que hace referencia a una expresión compartida que usa el conector [`AzureStorage.DataLake`](https://learn.microsoft.com/en-us/powerquery-m/azurestorage-datalake) (OneLake).

## Requisitos previos

Necesitará el **Workspace ID**, así como el **Resource ID** de su Warehouse o Lakehouse de Fabric. Ambos son GUID que forman parte de la URL al navegar al Warehouse o Lakehouse en el portal de Fabric:

![URL de Lakehouse/Warehouse](~/content/assets/images/lakehouse-warehouse-url.png)

En la captura de pantalla anterior, el **Workspace ID** del Lakehouse se resalta en azul, mientras que el **Resource ID** se resalta en verde.

Si se conecta a un Warehouse de Fabric o a un Lakehouse que admita esquemas, también deberá conocer el **Schema** de la tabla/vista materializada a la que desea conectarse.

> [!WARNING]
> Las tablas en modo Import pueden definir transformaciones dentro de sus particiones (expresadas mediante SQL o M). Estas transformaciones se perderán al convertir a Direct Lake en OneLake, ya que las particiones de Direct Lake deben contener una asignación 1:1 de las columnas de la tabla/vista materializada de origen. Por lo tanto, asegúrese de que la tabla/vista materializada de origen tenga el mismo nombre en el Warehouse o Lakehouse de Fabric que en el modelo semántico, y de que las asignaciones de columnas sean correctas antes de ejecutar este script.

## Script

### Convertir tablas en modo Import a Direct Lake en OneLake

```csharp
// ==================================================================
// Convertir Import a Direct Lake en OneLake
// ----------------------------------------
// 
// Este script convierte las tablas seleccionadas (Import) o, si no hay
// ninguna seleccionada, todas las tablas del modelo, a tablas
// Direct Lake en OneLake.
//
// ADVERTENCIA: El script asume que las tablas tienen el mismo nombre
// en el Warehouse o Lakehouse de Fabric que en el modelo semántico.
// Además, cualquier transformación (basada en M o SQL) en las
// particiones en modo Import se perderá, ya que las tablas en modo Direct Lake
// deben contener 1:1 las mismas columnas que la tabla/vista
// materializada de origen.
//
// Necesitará el Workspace ID y el ID de su Warehouse o Lakehouse de
// Fabric (ambos son GUID).
// ==================================================================

// Buscar la expresión compartida que usan las EntityPartitions en el modelo:
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
    Warning("El modelo o la selección no contiene ninguna tabla en modo Import");
    return;
}
else
{
    var result = MessageBox.Show("Se convertirán las siguientes tablas:\r\n\r\n" + string.Join("\r\n", importTables.Select(t => "  - " + t.Name)) +
        "\r\n\r\n¿Continuar?",
        "¿Confirmar conversión?", MessageBoxButtons.OKCancel, MessageBoxIcon.Question);
    if (result == DialogResult.Cancel) return;
}

string workspaceId = string.Empty;
string resourceId = string.Empty;
var sharedExpression = Model.Expressions.FirstOrDefault(e => e.Expression.Contains("AzureStorage.DataLake"));
if(sharedExpression != null)
{
    // Extraer el Workspace ID y el Resource ID existentes
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

Info("Tablas convertidas a Direct Lake en OneLake.");

public class UrlNameDialog : Form
{
    public TextBox WorkspaceId { get; private set; }
    public TextBox ResourceId { get; private set; }
    public TextBox Schema { get; private set; }
    private Button okButton;

    public UrlNameDialog(string workspaceId, string resourceId)
    {
        Text = "Convertir Direct Lake sobre SQL a OneLake";
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
        mainLayout.Controls.Add(new Label { Text = "ID de Fabric Warehouse / Lakehouse (GUID):", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
        ResourceId = new TextBox { Width = 1000, Text = resourceId };
        mainLayout.Controls.Add(ResourceId);

        // Schema
        mainLayout.Controls.Add(new Label { Text = "Esquema (opcional):", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
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

        okButton = new Button { Text = "Aceptar", DialogResult = DialogResult.OK, AutoSize = true, Enabled = false };
        var cancelButton = new Button { Text = "Cancelar", DialogResult = DialogResult.Cancel, AutoSize = true };
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

### Explicación

El script determina primero si debe convertir todas las tablas en modo Import del modelo o solo las que el usuario haya seleccionado. A continuación, comprueba si existe alguna tabla de este tipo y solicita confirmación al usuario antes de continuar.

A continuación, el script intenta localizar una expresión compartida que use el conector `AzureStorage.DataLake`. Si existe una expresión de este tipo, extrae el ID del Workspace y el ID del recurso de su expresión. Si no se encuentra ninguna expresión de ese tipo, crea una nueva.

A continuación, se pide al usuario que introduzca el ID del Workspace y el ID del recurso del Warehouse o Lakehouse de Fabric, así como un nombre de esquema opcional. El script reemplaza la expresión compartida existente por una nueva que use los ID proporcionados, si se han modificado.

Por último, para cada tabla de Import mode, el script crea una nueva EntityPartition con el nombre y el esquema especificados, haciendo referencia a la Shared Expression. Luego elimina cualquier partición existente en la tabla que no sea la EntityPartition recién creada.