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
// Convertir tablas Direct Lake en OneLake de vuelta a Import mode
// ----------------------------------------
// Este script convierte las tablas seleccionadas o todas de Direct Lake en OneLake a Import mode
//  Agrega una expresión compartida llamada SQLEndpoint y reemplaza la DatabaseQuery existente si ya no se necesita
// ===================================================================================
using System;
using System.Linq;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Drawing;

// -------------------------------------------------------------------
// 1) Diálogo para elegir el ámbito
// -------------------------------------------------------------------
public class ScopeSelectionDialog : Form
{
    public enum ScopeOption { OnlySelected, All, Cancel }
    public ScopeOption SelectedOption { get; private set; }

    public ScopeSelectionDialog(int selectedCount, int totalCount)
    {
        Text = "Elige las tablas que quieres convertir";
        AutoSize = true; AutoSizeMode = AutoSizeMode.GrowAndShrink;
        StartPosition = FormStartPosition.CenterParent;
        Padding = new Padding(20);

        var layout = new TableLayoutPanel {
            ColumnCount = 1, Dock = DockStyle.Fill,
            AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink
        };
        Controls.Add(layout);

        layout.Controls.Add(new Label {
            Text = $"Tienes {selectedCount} tabla(s) seleccionadas,\ny {totalCount} tabla(s) Direct Lake en el modelo.",
            AutoSize = true, TextAlign = ContentAlignment.MiddleLeft
        });

        var panel = new FlowLayoutPanel {
            FlowDirection = FlowDirection.LeftToRight,
            Dock = DockStyle.Fill, AutoSize = true,
            Padding = new Padding(0, 20, 0, 0)
        };

        var btnOnly = new Button {
            Text = "Solo las tablas seleccionadas", AutoSize = true,
            DialogResult = DialogResult.OK
        };
        btnOnly.Click += (s, e) => SelectedOption = ScopeOption.OnlySelected;

        var btnAll = new Button {
            Text = "Todas las tablas", AutoSize = true,
            DialogResult = DialogResult.Retry
        };
        btnAll.Click += (s, e) => SelectedOption = ScopeOption.All;

        var btnCancel = new Button {
            Text = "Cancelar", AutoSize = true,
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
// 2) Diálogo de importación SQL (ahora el esquema es obligatorio)
// -------------------------------------------------------------------
public class SqlImportDialog : Form
{
    public TextBox SqlEndpoint { get; }
    public TextBox DatabaseName { get; }
    public TextBox Schema { get; }
    private Button okButton;

    public SqlImportDialog(string endpoint, string db, string schema)
    {
        Text = "Convertir Direct Lake → Import mode";
        AutoSize = true; AutoSizeMode = AutoSizeMode.GrowAndShrink;
        StartPosition = FormStartPosition.CenterParent;
        Padding = new Padding(20);

        var layout = new TableLayoutPanel {
            ColumnCount = 1, Dock = DockStyle.Fill,
            AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink
        };
        Controls.Add(layout);

        // Endpoint
        layout.Controls.Add(new Label { Text = "Punto de conexión de análisis SQL:", AutoSize = true });
        SqlEndpoint = new TextBox { Width = 800, Text = endpoint };
        layout.Controls.Add(SqlEndpoint);

        // Base de datos
        layout.Controls.Add(new Label {
            Text = "Nombre del Lakehouse/Warehouse:", Padding = new Padding(0, 20, 0, 0),
            AutoSize = true
        });
        DatabaseName = new TextBox { Width = 800, Text = db };
        layout.Controls.Add(DatabaseName);

        // Esquema (obligatorio)
        layout.Controls.Add(new Label {
            Text = "Esquema:", Padding = new Padding(0, 20, 0, 0),
            AutoSize = true
        });
        Schema = new TextBox { Width = 800, Text = schema };
        layout.Controls.Add(Schema);

        // Botones
        var panel = new FlowLayoutPanel {
            FlowDirection = FlowDirection.RightToLeft,
            Dock = DockStyle.Fill, AutoSize = true,
            Padding = new Padding(0, 20, 0, 0)
        };
        okButton = new Button {
            Text = "Aceptar", DialogResult = DialogResult.OK,
            AutoSize = true, Enabled = false
        };
        var cancel = new Button {
            Text = "Cancelar", DialogResult = DialogResult.Cancel,
            AutoSize = true
        };
        panel.Controls.AddRange(new Control[] { okButton, cancel });
        layout.Controls.Add(panel);

        AcceptButton = okButton;
        CancelButton = cancel;

        // Solo habilitar Aceptar cuando los tres campos no estén vacíos
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
// 3) Lógica principal de conversión
// -------------------------------------------------------------------
WaitFormVisible = false;
Application.UseWaitCursor = false;

// 3,1) Encontrar todas las tablas Direct Lake
var allDirectLake = Model.Tables
    .Where(t => t.Partitions.Count == 1
             && t.Partitions[0].SourceType == PartitionSourceType.Entity
             && t.Partitions[0].Mode == ModeType.DirectLake)
    .ToList();

// 3,2) Y las que has seleccionado
var selectedDirect = Selected.Tables
    .Cast<Table>()
    .Where(t => t.Partitions.Count == 1
             && t.Partitions[0].SourceType == PartitionSourceType.Entity
             && t.Partitions[0].Mode == ModeType.DirectLake)
    .ToList();

// 3,3) Preguntar el ámbito
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
    Warning("No se encontraron tablas Direct Lake en el ámbito seleccionado.");
    return;
}

// 3,4) Pedir conexión + esquema
var sqlDialog = new SqlImportDialog("", "", "");
if (sqlDialog.ShowDialog() == DialogResult.Cancel) return;

// 3,5) Insertar o actualizar la expresión compartida "SQLEndpoint"
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

// 3,6) Plantilla de partición M
const string mTemplate = @"let
    Source = SQLEndpoint,
    Data = Source{{[Schema=""{0}"",Item=""{1}""]}}[Data]
in
    Data";

// 3,7) Cambiar particiones
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

// 3,8) Si se convierte **todo el modelo**, eliminar la expresión DatabaseQuery anterior
if (isAllTables)
{
    var oldDbq = Model.Expressions.FirstOrDefault(e => e.Name == "DatabaseQuery");
    if (oldDbq != null)
        oldDbq.Delete();   // API de TE3: Expression.Delete() la elimina del modelo
}

// 3,9) Asegurar que el modo predeterminado sea Import mode
Model.DefaultMode = ModeType.Import;

Info("Conversión completada: Direct Lake → Import mode" + 
     (isAllTables ? " (DatabaseQuery eliminado)" : "") + ".");
```

### Explicación

El script primero te pide que determines el alcance de la conversión, eligiendo entre convertir solo las tablas seleccionadas o todas las tablas del modelo. A continuación, identifica qué tablas están actualmente en modo Direct Lake dentro del ámbito elegido. Si no se encuentran tablas aplicables o si cancelas el cuadro de diálogo, el script finaliza.

Después, el script te pide que introduzcas el punto de conexión de análisis SQL, el nombre del Lakehouse o Warehouse y un nombre de esquema obligatorio. El script se asegura de que los tres campos estén rellenados antes de dejarte continuar.

A continuación, el script crea o actualiza una expresión compartida llamada `SQLEndpoint` con los detalles de conexión proporcionados. Esta expresión usa el conector `Sql.Database` para acceder al Lakehouse o Warehouse.

Para cada tabla que se convierte, el script crea una nueva partición M en modo Import mode que hace referencia a la expresión `SQLEndpoint` y usa el esquema indicado y el nombre de la tabla. La partición Direct Lake existente se renombra y luego se elimina, dejando únicamente la nueva partición en modo Import.

Por último, si elegiste convertir todas las tablas Direct Lake del modelo, el script busca una expresión compartida existente llamada `DatabaseQuery` y la elimina si la encuentra. Luego, el modo de almacenamiento predeterminado del modelo se establece en Import y se muestra un mensaje de confirmación.

## Descargo de responsabilidad sobre el uso de IA

Este script se creó con la ayuda de un LLM.
