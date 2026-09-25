---
uid: script-convert-dlol-to-import
title: Convertir Direct Lake en OneLake a modo Import
author: Morten Lønskov
updated: 2025-06-25
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Convertir Direct Lake en OneLake al modo Import

## Objetivo del script

Este script convierte las tablas de Direct Lake en OneLake (DL/OL) al modo Import mode. Tal como se indica en el [artículo de orientación de Direct Lake](xref:direct-lake-guidance), necesitamos reemplazar el [EntityPartition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.entitypartitionsource?view=analysisservices-dotnet) de este tipo de tablas por la partición M normal correspondiente en el modo Import mode.

## Requisitos previos

Necesitarás el **punto de conexión de análisis SQL** y el **nombre** de tu Warehouse o Lakehouse de Fabric. Ambos pueden encontrarse en el portal de Fabric.

También tendrás que conocer el **esquema** de la tabla o vista materializada a la que quieres conectarte. En los Lakehouse, el valor predeterminado es dbo.

## Script

### Convertir tablas Direct Lake en OneLake al modo Import mode

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

### Explicación

El script primero te pide que determines el alcance de la conversión, eligiendo entre convertir solo las tablas seleccionadas o todas las tablas del modelo. A continuación, identifica qué tablas están actualmente en modo Direct Lake dentro del ámbito elegido. Si no se encuentran tablas aplicables o si cancelas el cuadro de diálogo, el script finaliza.

Después, el script te pide que introduzcas el punto de conexión de análisis SQL, el nombre del Lakehouse o Warehouse y un nombre de esquema obligatorio. El script se asegura de que los tres campos estén rellenados antes de dejarte continuar.

A continuación, el script crea o actualiza una expresión compartida llamada `SQLEndpoint` con los detalles de conexión proporcionados. Esta expresión usa el conector `Sql.Database` para acceder al Lakehouse o Warehouse.

Para cada tabla que se convierte, el script crea una nueva partición M en modo Import mode que hace referencia a la expresión `SQLEndpoint` y usa el esquema indicado y el nombre de la tabla. La partición Direct Lake existente se renombra y luego se elimina, dejando únicamente la nueva partición en modo Import.

Por último, si elegiste convertir todas las tablas Direct Lake del modelo, el script busca una expresión compartida existente llamada `DatabaseQuery` y la elimina si la encuentra. Luego, el modo de almacenamiento predeterminado del modelo se establece en Import y se muestra un mensaje de confirmación.

## Descargo de responsabilidad sobre el uso de IA

Este script se creó con la ayuda de un LLM.
