---
uid: script-convert-dlsql-to-dlol
title: Direct Lake auf SQL zu OneLake konvertieren
author: Daniel Otykier
updated: 2025-06-20
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---

# Direct Lake auf SQL zu OneLake konvertieren

## Skriptzweck

Dieses Skript konvertiert ein Modell, das Direct Lake auf SQL (DL/SQL) verwendet, zu Direct Lake auf OneLake (DL/OL). Wie im [Artikel zur Direct Lake-Anleitung](xref:direct-lake-guidance) dargelegt, geht es einfach darum, die M-Abfrage für den freigegebenen Ausdruck, der von den Direct Lake-Partitionen im Modell verwendet wird, zu aktualisieren, um den Connector [`AzureStorage.DataLake`](https://learn.microsoft.com/en-us/powerquery-m/azurestorage-datalake) statt des Connectors [`Sql.Database`](https://learn.microsoft.com/en-us/powerquery-m/sql-database) zu verwenden.

## Voraussetzungen

Sie benötigen die **Workspace-ID** sowie die **Ressourcen-ID** Ihres Fabric Warehouse oder Lakehouse. Beide sind GUIDs, die Teil der URL sind, wenn Sie im Fabric-Portal zum Warehouse oder Lakehouse navigieren:

![Lakehouse Warehouse URL](~/content/assets/images/lakehouse-warehouse-url.png)

Im obigen Screenshot ist die **Workspace-ID** des Lakehouse blau hervorgehoben, während die **Ressourcen-ID** grün hervorgehoben ist.

## Skript

### Direct Lake auf SQL zu OneLake konvertieren

```csharp
// ==================================================================
// Direct Lake auf SQL zu OneLake konvertieren
// -------------------------------------
// 
// Dieses Skript erkennt, ob das aktuelle Modell Direct Lake auf SQL
// verwendet, und empfiehlt ein Upgrade des Modells auf Direct Lake
// auf OneLake.
//
// Sie benötigen die Workspace-ID und die ID Ihres Fabric Warehouse
// oder Lakehouse (beide sind GUIDs).
// ==================================================================

// Finden Sie den freigegebenen Ausdruck, der von EntityPartitions im Modell verwendet wird:
using System.Windows.Forms;
using System.Drawing;

var partition = Model.AllPartitions.OfType<EntityPartition>()
    .FirstOrDefault(e => e.Mode == ModeType.DirectLake && e.ExpressionSource != null);
var expressionSource = partition == null ? null : partition.ExpressionSource;

if (expressionSource == null)
{
    Warning("Ihr Modell scheint keine Tabellen im Direct Lake-Modus zu enthalten.");
    return;
}

if (!expressionSource.Expression.Contains("Sql.Database"))
{
    Warning("Dieses Modell ist nicht für Direct Lake über SQL konfiguriert.");
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
    Info("Modell erfolgreich zu Direct Lake auf OneLake konvertiert. Sie müssen es möglicherweise als neues semantisches Modell bereitstellen, da die Modellsortierung geändert wurde.");
}
else
    Info("Modell erfolgreich zu Direct Lake auf OneLake konvertiert.");

// UI-Code unter dieser Zeile:
public class UrlNameDialog : Form
{
    public TextBox WorkspaceId { get; private set; }
    public TextBox ResourceId { get; private set; }
    private Button okButton;

    public UrlNameDialog()
    {
        Text = "Direct Lake auf SQL zu OneLake konvertieren";
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
        WorkspaceId = new TextBox { Width = 1000 };
        mainLayout.Controls.Add(WorkspaceId);

        // Resource ID
        mainLayout.Controls.Add(new Label { Text = "Fabric Warehouse / Lakehouse-ID (GUID):", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
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
        var cancelButton = new Button { Text = "Abbrechen", DialogResult = DialogResult.Cancel, AutoSize = true };
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

### Erklärung

Das Skript versucht zunächst, eine EntityPartition zu finden, die für den Direct Lake-Modus konfiguriert ist und eine Expression Source (einen Verweis auf einen freigegebenen Ausdruck) aufweist. Wenn keine solche Partition gefunden wird, zeigt es eine Warnmeldung an und wird beendet. Darüber hinaus muss der referenzierte freigegebene Ausdruck den Connector `Sql.Database` angeben, was darauf hinweist, dass das Modell derzeit Direct Lake auf SQL verwendet.

Sobald das Skript bestätigt, dass das Modell Direct Lake auf SQL verwendet, fordert es den Benutzer auf, die **Workspace-ID** und **Ressourcen-ID** des Fabric Warehouse oder Lakehouse einzugeben. Das Skript ersetzt dann den Connector `Sql.Database` im freigegebenen Ausdruck durch den Connector `AzureStorage.DataLake` unter Verwendung der bereitgestellten IDs.

Abschließend löscht das Skript die Sortierung des Modells, falls diese gesetzt ist, da diese Änderung eine neue Sortierung erfordert. Das Skript informiert den Benutzer dann, dass das Modell erfolgreich zu Direct Lake auf OneLake konvertiert wurde.