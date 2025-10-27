---
uid: script-convert-import-to-dlol
title: Import in Direct Lake auf OneLake konvertieren
author: Daniel Otykier
updated: 2025-06-20
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---

# Import in Direct Lake auf OneLake konvertieren

## Skriptzweck

Dieses Skript konvertiert Import-Modus-Tabellen in Direct Lake auf OneLake (DL/OL). Wie im [Direct Lake-Leitartikel](xref:direct-lake-guidance) dargelegt, müssen wir die Partition(en) in solchen Tabellen durch eine einzelne [EntityPartition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.entitypartitionsource?view=analysisservices-dotnet) ersetzen, die den Namen und das Schema der Tabelle/materialisierten Ansicht im Fabric Lakehouse oder Warehouse angibt, während auf einen freigegebenen Ausdruck verwiesen wird, der den [`AzureStorage.DataLake`](https://learn.microsoft.com/en-us/powerquery-m/azurestorage-datalake) (OneLake)-Connector verwendet.

## Voraussetzungen

Sie benötigen die **Workspace-ID** sowie die **Ressourcen-ID** Ihres Fabric Warehouse oder Lakehouse. Beide sind GUIDs, die Teil der URL sind, wenn Sie im Fabric-Portal zum Warehouse oder Lakehouse navigieren:

![Lakehouse Warehouse URL](~/content/assets/images/lakehouse-warehouse-url.png)

Im obigen Screenshot ist die **Workspace-ID** des Lakehouse blau hervorgehoben, während die **Ressourcen-ID** grün hervorgehoben ist.

Wenn Sie sich mit einem Fabric Warehouse oder einem Lakehouse verbinden, das Schemas unterstützt, müssen Sie auch das **Schema** der Tabelle/materialisierten Ansicht kennen, mit der Sie sich verbinden möchten.

> [!WARNING]
> Tabellen im Import-Modus können Transformationen in ihren Partitionen definieren (ausgedrückt mit SQL oder M). Diese Transformationen gehen bei der Konvertierung in den Direct Lake auf OneLake-Modus verloren, da die Direct Lake-Partitionen eine 1:1-Zuordnung der Spalten in der Quelltabelle/materialisierten Ansicht enthalten müssen. Stellen Sie daher sicher, dass die Quelltabelle/materialisierte Ansicht denselben Namen im Fabric Warehouse oder Lakehouse hat wie im semantischen Modell, und dass die Spaltenzuordnungen korrekt sind, bevor Sie dieses Skript ausführen.

## Skript

### Import-Modus-Tabellen in Direct Lake auf OneLake konvertieren

```csharp
// ==================================================================
// Import in Direct Lake auf OneLake konvertieren
// ----------------------------------------
// 
// Dieses Skript konvertiert die ausgewählten (Import-)Tabellen oder
// alle Tabellen im Modell, falls nichts ausgewählt ist, in Direct
// Lake auf OneLake-Tabellen.
//
// WARNUNG: Das Skript geht davon aus, dass Tabellen im Fabric
// Warehouse oder Lakehouse denselben Namen haben wie im semantischen
// Modell. Darüber hinaus gehen alle Transformationen (M- oder
// SQL-basiert) in den Import-Partitionen verloren, da Direct Lake
// Modus-Tabellen dieselben Spalten 1:1 wie die Quelltabelle/
// materialisierte Ansicht enthalten müssen.
//
// Sie benötigen die Workspace-ID und die ID Ihres Fabric Warehouse
// oder Lakehouse (beide sind GUIDs).
// ==================================================================

// Suchen Sie den freigegebenen Ausdruck, der von EntityPartitions im Modell verwendet wird:
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
    Warning("Das Modell oder die Auswahl enthält keine Tabellen im Import-Modus");
    return;
}
else
{
    var result = MessageBox.Show("Die folgenden Tabellen werden konvertiert:\r\n\r\n" + string.Join("\r\n", importTables.Select(t => "  - " + t.Name)) +
        "\r\n\r\nFortfahren?",
        "Konvertierung bestätigen?", MessageBoxButtons.OKCancel, MessageBoxIcon.Question);
    if (result == DialogResult.Cancel) return;
}

string workspaceId = string.Empty;
string resourceId = string.Empty;
var sharedExpression = Model.Expressions.FirstOrDefault(e => e.Expression.Contains("AzureStorage.DataLake"));
if(sharedExpression != null)
{
    // Extrahieren Sie vorhandene Workspace-ID und Ressourcen-ID
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

Info("Tabellen in Direct Lake auf OneLake-Modus konvertiert.");

public class UrlNameDialog : Form
{
    public TextBox WorkspaceId { get; private set; }
    public TextBox ResourceId { get; private set; }
    public TextBox Schema { get; private set; }
    private Button okButton;

    public UrlNameDialog(string workspaceId, string resourceId)
    {
        Text = "Direct Lake auf SQL in OneLake konvertieren";
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
        mainLayout.Controls.Add(new Label { Text = "Workspace-ID (GUID):", AutoSize = true });
        WorkspaceId = new TextBox { Width = 1000, Text = workspaceId };
        mainLayout.Controls.Add(WorkspaceId);

        // Resource ID
        mainLayout.Controls.Add(new Label { Text = "Fabric Warehouse / Lakehouse-ID (GUID):", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
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
        var cancelButton = new Button { Text = "Abbrechen", DialogResult = DialogResult.Cancel, AutoSize = true };
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

### Erklärung

Das Skript bestimmt zunächst, ob alle Import-Modus-Tabellen im Modell oder nur die vom Benutzer ausgewählten konvertiert werden sollen. Es prüft dann, ob solche Tabellen vorhanden sind, und fordert den Benutzer auf, die Konvertierung zu bestätigen, bevor er fortfährt.

Das Skript versucht dann, einen freigegebenen Ausdruck zu finden, der den `AzureStorage.DataLake`-Connector verwendet. Falls ein solcher Ausdruck vorhanden ist, extrahiert er die Workspace-ID und Ressourcen-ID aus dem Ausdruck. Wenn kein solcher Ausdruck gefunden wird, wird ein neuer erstellt.

Der Benutzer wird dann aufgefordert, die Workspace-ID und Ressourcen-ID des Fabric Warehouse oder Lakehouse sowie einen optionalen Schemanamen einzugeben. Das Skript ersetzt den vorhandenen freigegebenen Ausdruck durch einen neuen, der die bereitgestellten IDs verwendet, falls diese geändert wurden.

Schließlich erstellt das Skript für jede Import-Modus-Tabelle eine neue EntityPartition mit dem angegebenen Namen und Schema, die auf den freigegebenen Ausdruck verweist. Es löscht dann alle vorhandenen Partitionen in der Tabelle, die nicht die neu erstellte EntityPartition sind.