---
uid: script-add-databricks-metadata-descriptions
title: Agregar descripciones de metadatos de Databricks
author: Johnny Winter
updated: 2025-09-04
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Agregar descripciones de metadatos de Databricks

## Propósito del script

Este script se creó como parte de la serie Tabular Editor x Databricks. En Unity Catalog es posible proporcionar comentarios descriptivos para tablas y columnas. Este script puede reutilizar esta información para rellenar automáticamente las descripciones de tablas y columnas en su modelo semántico. <br></br>

> [!NOTE]
> Este script requiere tener instalado el Simba Spark ODBC Driver (descarga desde https://www.databricks.com/spark/odbc-drivers-download)
> Cada ejecución del script solicitará al usuario un token de acceso personal de Databricks. Esto es necesario para autenticarse en Databricks.
> El script utiliza las tablas information_schema de Unity Catalog para obtener información sobre las relaciones, así que quizá deba consultarlo con su administrador de Databricks para asegurarse de que tiene permisos para consultar estas tablas. <br></br>

## Script

### Agregar descripciones de metadatos de Databricks

```csharp
/*
 * Título: Agregar descripciones de metadatos de Databricks
 * Autor: Johnny Winter, greyskullanalytics.com
 *
 * Este script, al ejecutarse, recorrerá las tablas seleccionadas actualmente y enviará una consulta a Databricks para comprobar si cada tabla tiene descripciones de metadatos definidas en Unity Catalog.
 * Cuando exista una descripción, se agregará a la descripción del modelo semántico.
 * Paso 1:  Seleccione una o varias tablas en el modelo
 * Paso 2:  Ejecute este script
 * Paso 3:  Introduzca su token de acceso personal de Databricks cuando se le solicite
 * Paso 4:  El script se conectará a Databricks y actualizará las descripciones de tablas y columnas cuando existan. 
 *          Para cada tabla procesada, un cuadro de mensaje mostrará el número de descripciones actualizadas.
 *          Haga clic en OK para continuar con la siguiente tabla.
 * Notas:
 *  -   Este script requiere tener instalado el Simba Spark ODBC Driver (descarga desde https://www.databricks.com/spark/odbc-drivers-download)
 *  -   Cada ejecución del script solicitará al usuario un token de acceso personal de Databricks
 */
#r "Microsoft.VisualBasic"
using System;
using System.Data.Odbc;
using System.Drawing;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using sysData = System.Data;

//código para crear un cuadro de entrada enmascarada para el token PAT de Databricks
public partial class PasswordInputForm : Form
{
    public string Password { get; private set; }

    private TextBox passwordTextBox;
    private Button okButton;
    private Button cancelButton;
    private Label promptLabel;

    public PasswordInputForm(string prompt, string title)
    {
        InitializeComponent(prompt, title);
    }

    private void InitializeComponent(string prompt, string title)
    {
        this.Text = title;
        this.Size = new System.Drawing.Size(4000, 1500);
        this.StartPosition = FormStartPosition.WindowsDefaultLocation;
        this.FormBorderStyle = FormBorderStyle.FixedDialog;
        this.MaximizeBox = false;
        this.MinimizeBox = false;

        // Etiqueta del aviso
        promptLabel = new Label();
        promptLabel.Text = prompt;
        promptLabel.Location = new System.Drawing.Point(12, 15);
        promptLabel.Size = new System.Drawing.Size(360, 40);
        promptLabel.AutoSize = false;
        this.Controls.Add(promptLabel);

        // Cuadro de texto de contraseña
        passwordTextBox = new TextBox();
        passwordTextBox.Location = new System.Drawing.Point(12, 55);
        passwordTextBox.Size = new System.Drawing.Size(360, 20);
        passwordTextBox.UseSystemPasswordChar = true; // Esto enmascara la entrada
        passwordTextBox.KeyPress += (s, e) =>
        {
            if (e.KeyChar == (char)Keys.Return)
            {
                OkButton_Click(null, null);
                e.Handled = true;
            }
        };
        this.Controls.Add(passwordTextBox);

        // Botón Aceptar
        okButton = new Button();
        okButton.Text = "Aceptar";
        okButton.Location = new System.Drawing.Point(216, 85);
        okButton.Size = new System.Drawing.Size(150, 50);
        okButton.Click += OkButton_Click;
        this.Controls.Add(okButton);

        // Botón Cancelar
        cancelButton = new Button();
        cancelButton.Text = "Cancelar";
        cancelButton.Location = new System.Drawing.Point(297, 85);
        cancelButton.Size = new System.Drawing.Size(150, 50);
        cancelButton.Click += CancelButton_Click;
        this.Controls.Add(cancelButton);

        // Establecer botones predeterminado y de cancelación
        this.AcceptButton = okButton;
        this.CancelButton = cancelButton;

        // Enfocar el cuadro de texto cuando se carga el formulario
        this.Load += (s, e) => passwordTextBox.Focus();
    }

    private void OkButton_Click(object sender, EventArgs e)
    {
        Password = passwordTextBox.Text;
        this.DialogResult = DialogResult.OK;
        this.Close();
    }

    private void CancelButton_Click(object sender, EventArgs e)
    {
        Password = string.Empty;
        this.DialogResult = DialogResult.Cancel;
        this.Close();
    }

    public static string ShowDialog(string prompt, string title)
    {
        using (var form = new PasswordInputForm(prompt, title))
        {
            if (form.ShowDialog() == DialogResult.OK)
                return form.Password;
            return string.Empty;
        }
    }
}

public static class MaskedInputHelper
{
    public static string GetMaskedInput(string prompt, string title, string defaultValue = "")
    {
        using (var form = new Form())
        {
            form.Text = title;
            form.Size = new System.Drawing.Size(1000, 500);
            form.StartPosition = FormStartPosition.CenterScreen;
            form.FormBorderStyle = FormBorderStyle.FixedDialog;
            form.MaximizeBox = false;
            form.MinimizeBox = false;

            var label = new Label()
            {
                Left = 12,
                Top = 15,
                Size = new System.Drawing.Size(900, 100),
                Text = prompt,
            };
            var textBox = new TextBox()
            {
                Left = 12,
                Top = 150,
                Size = new System.Drawing.Size(900, 100),
                UseSystemPasswordChar = true,
                Text = defaultValue,
            };
            var buttonOk = new Button()
            {
                Text = "Aceptar",
                Size = new System.Drawing.Size(150, 50),
                Left = 12,
                Width = 150,
                Top = 200,
                DialogResult = DialogResult.OK,
            };
            var buttonCancel = new Button()
            {
                Text = "Cancelar",
                Size = new System.Drawing.Size(150, 50),
                Left = 175,
                Width = 150,
                Top = 200,
                DialogResult = DialogResult.Cancel,
            };

            buttonOk.Click += (sender, e) =>
            {
                form.Close();
            };
            form.Controls.Add(label);
            form.Controls.Add(textBox);
            form.Controls.Add(buttonOk);
            form.Controls.Add(buttonCancel);
            form.AcceptButton = buttonOk;
            form.CancelButton = buttonCancel;

            return form.ShowDialog() == DialogResult.OK ? textBox.Text : string.Empty;
        }
    }
}

//Código para recuperar la información de conexión a Databricks desde la consulta M en una partición de tabla
public class DatabricksConnectionInfo
{
    public string ServerHostname { get; set; }
    public string HttpPath { get; set; }
    public string DatabaseName { get; set; }
    public string SchemaName { get; set; }
    public string TableName { get; set; }

    public override string ToString()
    {
        return $"Server: {ServerHostname}\n"
            + $"HTTP Path: {HttpPath}\n"
            + $"Database: {DatabaseName}\n"
            + $"Schema: {SchemaName}\n"
            + $"Table: {TableName}";
    }
}

public class PowerQueryMParser
{
    public static DatabricksConnectionInfo ParseMQuery(string mQuery)
    {
        if (string.IsNullOrWhiteSpace(mQuery))
            throw new ArgumentException("La consulta M no puede ser nula ni estar vacía");

        var connectionInfo = new DatabricksConnectionInfo();

        try
        {
            // Analiza la línea Source para extraer el nombre de host del servidor y el HTTP Path
            ParseSourceLine(mQuery, connectionInfo);

            // Analiza la línea Database para extraer el nombre de la base de datos
            ParseDatabaseLine(mQuery, connectionInfo);

            // Analiza la línea Schema para extraer el nombre del esquema
            ParseSchemaLine(mQuery, connectionInfo);

            // Analiza la línea Data para extraer el nombre de la tabla
            ParseDataLine(mQuery, connectionInfo);

            return connectionInfo;
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"Error al analizar la consulta M: {ex.Message}", ex);
        }
    }

    private static void ParseSourceLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // Patrón para hacer coincidir ambos casos:
        // Source = DatabricksMultiCloud.Catalogs("hostname", "httppath", null),
        // Source = Databricks.Catalogs("hostname", "httppath", null),
        var sourcePattern =
            @"Source\s*=\s*Databricks(?:MultiCloud)?\.Catalogs\s*\(\s*""([^""]+)""\s*,\s*""([^""]+)""\s*,\s*null\s*\)";
        var sourceMatch = Regex.Match(
            mQuery,
            sourcePattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!sourceMatch.Success)
            throw new FormatException(
                "No se pudo encontrar una definición Source válida en la consulta M (admite los conectores Databricks y DatabricksMultiCloud)"
            );

        connectionInfo.ServerHostname = sourceMatch.Groups[1].Value;
        connectionInfo.HttpPath = sourceMatch.Groups[2].Value;
    }

    private static void ParseDatabaseLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // Patrón para hacer coincidir: Database = Source{[Name="databasename",Kind="Database"]}[Data],
        var databasePattern =
            @"Database\s*=\s*Source\s*{\s*\[\s*Name\s*=\s*""([^""]+)""\s*,\s*Kind\s*=\s*""Database""\s*\]\s*}\s*\[\s*Data\s*\]";
        var databaseMatch = Regex.Match(
            mQuery,
            databasePattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!databaseMatch.Success)
            throw new FormatException("No se pudo encontrar una definición Database válida en la consulta M");

        connectionInfo.DatabaseName = databaseMatch.Groups[1].Value;
    }

    private static void ParseSchemaLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // Patrón para hacer coincidir: Schema = Database{[Name="schemaname",Kind="Schema"]}[Data],
        var schemaPattern =
            @"Schema\s*=\s*Database\s*{\s*\[\s*Name\s*=\s*""([^""]+)""\s*,\s*Kind\s*=\s*""Schema""\s*\]\s*}\s*\[\s*Data\s*\]";
        var schemaMatch = Regex.Match(
            mQuery,
            schemaPattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!schemaMatch.Success)
            throw new FormatException("No se pudo encontrar una definición Schema válida en la consulta M");

        connectionInfo.SchemaName = schemaMatch.Groups[1].Value;
    }

    private static void ParseDataLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // Patrón para hacer coincidir: Data = Schema{[Name="tablename",Kind="Table"]}[Data]
        var dataPattern =
            @"Data\s*=\s*Schema\s*{\s*\[\s*Name\s*=\s*""([^""]+)""\s*,\s*Kind\s*=\s*""Table""\s*\]\s*}\s*\[\s*Data\s*\]";
        var dataMatch = Regex.Match(
            mQuery,
            dataPattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!dataMatch.Success)
            throw new FormatException("No se pudo encontrar una definición Data válida en la consulta M");

        connectionInfo.TableName = dataMatch.Groups[1].Value;
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//script principal



//comprueba que el usuario tenga una tabla seleccionada
if (Selected.Tables.Count == 0)
{
    // alterna el indicador giratorio de 'Running Macro'
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox("Seleccione una o varias tablas", MsgBoxStyle.Critical, "Se requiere una tabla");
    return;
}

//solicita el token de acceso personal: se requiere para autenticarse en Databricks
string dbxPAT;
do
{
    // alterna el indicador giratorio de 'Running Macro'
    ScriptHelper.WaitFormVisible = false;
    dbxPAT = MaskedInputHelper.GetMaskedInput(
        "Introduzca su token de acceso personal de Databricks (necesario para conectarse al SQL Endpoint)",
        "Token de acceso personal"
    );

    if (string.IsNullOrEmpty(dbxPAT))
    {
        return; // El usuario canceló
    }

    if (string.IsNullOrWhiteSpace(dbxPAT))
    {
        MessageBox.Show(
            "Se requiere un token de acceso personal",
            "Se requiere un token de acceso personal",
            MessageBoxButtons.OK,
            MessageBoxIcon.Warning
        );
    }
} while (string.IsNullOrWhiteSpace(dbxPAT));

// alterna el indicador giratorio de 'Running Macro'
ScriptHelper.WaitFormVisible = true;

//para cada tabla seleccionada, obtiene la información de conexión a Databricks desde la información de la partición
foreach (var t in Selected.Tables)
{
    string mQuery = t.Partitions[t.Name].Expression;
    var connectionInfo = PowerQueryMParser.ParseMQuery(mQuery);
    var columnDescriptions = 0;
    var tableDescriptions = 0;
    // Accede a componentes individuales
    string serverHostname = connectionInfo.ServerHostname;
    string httpPath = connectionInfo.HttpPath;
    string databaseName = connectionInfo.DatabaseName;
    string schemaName = connectionInfo.SchemaName;
    string tableName = connectionInfo.TableName;
    //establece la cadena de conexión a DBX
    var odbcConnStr =
        @"DSN=Simba Spark;driver=C:\Program Files\Simba Spark ODBC Driver;host="
        + serverHostname
        + ";port=443;httppath="
        + httpPath
        + ";thrifttransport=2;ssl=1;authmech=3;uid=token;pwd="
        + dbxPAT;

    //prueba la conexión
    OdbcConnection conn = new OdbcConnection(odbcConnStr);
    try
    {
        conn.Open();
    }
    catch
    {
        // alterna el indicador giratorio de 'Running Macro'
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"Conexión fallida

Compruebe los siguientes requisitos previos:
    
- debe tener instalado el Simba Spark ODBC Driver 
(descarga desde https://www.databricks.com/spark/odbc-drivers-download)

- el controlador ODBC debe estar instalado en la ruta C:\Program Files\Simba Spark ODBC Driver

- compruebe que el nombre del servidor de Databricks "
                + serverHostname
                + @" es correcto

- compruebe que el SQL endpoint / HTTP Path de Databricks "
                + httpPath
                + @" es correcto

- compruebe que ha utilizado un token de acceso personal válido",
            MsgBoxStyle.Critical,
            "Error de conexión"
        );
        return;
    }

    //obtiene metadatos de la tabla
    var tableQuery =
        "SELECT comment FROM "
        + databaseName
        + ".information_schema.tables WHERE table_schema = '"
        + schemaName
        + "' AND table_name = '"
        + tableName
        + "'";
    OdbcDataAdapter td = new OdbcDataAdapter(tableQuery, conn);
    var dbxTable = new sysData.DataTable();

    try
    {
        td.Fill(dbxTable);
    }
    catch
    {
        // alterna el indicador giratorio de 'Running Macro'
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"Conexión fallida

O bien: 
    - la tabla "
                + schemaName
                + "."
                + tableName
                + " no existe"
                + @"
    
    - no tiene permisos para consultar esta tabla
    
    - la conexión agotó el tiempo de espera. Compruebe que el clúster del SQL Endpoint esté en ejecución",
            MsgBoxStyle.Critical,
            "Error de conexión: metadatos de tabla"
        );
        return;
    }
    string tableUpdate = "";
    foreach (sysData.DataRow row in dbxTable.Rows)
    {
        if (t.Description != row["comment"].ToString())
        {
            t.Description = row["comment"].ToString();
            tableUpdate = t.Name + " descripción de la tabla actualizada.";
        }
    }

    //obtiene metadatos de las columnas
    var columnsQuery = @"DESCRIBE " + databaseName + "." + schemaName + "." + tableName;
    OdbcDataAdapter da = new OdbcDataAdapter(columnsQuery, conn);
    var dbxColumns = new sysData.DataTable();

    try
    {
        da.Fill(dbxColumns);
    }
    catch
    {
        // alterna el indicador giratorio de 'Running Macro'
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"Conexión fallida

O bien: 
    - la tabla "
                + schemaName
                + "."
                + tableName
                + " no existe"
                + @"
    
    - no tiene permisos para consultar esta tabla
    
    - la conexión agotó el tiempo de espera. Compruebe que el clúster del SQL Endpoint esté en ejecución",
            MsgBoxStyle.Critical,
            "Error de conexión: metadatos de columnas"
        );
        return;
    }

    //actualiza las descripciones de columnas
    int counter = 0;
    foreach (sysData.DataRow row in dbxColumns.Rows)
    {
        string sourceColumn = row["col_name"].ToString();
        if (sourceColumn.Length != 0)
        {
            foreach (var c in t.DataColumns)
            {
                if (c.SourceColumn == sourceColumn && c.Description != row["comment"].ToString())
                {
                    c.Description = row["comment"].ToString();
                    counter = counter + 1;
                }
            }
        }
    }
    string msg;
    if (tableUpdate.Length > 0)
    {
        msg =
            tableUpdate
            + @"

"
            + counter
            + " descripciones actualizadas en "
            + t.Name;
    }
    else
    {
        msg = counter + " descripciones actualizadas en " + t.Name;
    }
    // alterna el indicador giratorio de 'Running Macro'
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox(msg, MsgBoxStyle.Information, "Actualizar descripciones de metadatos");
    // alterna el indicador giratorio de 'Running Macro'
    ScriptHelper.WaitFormVisible = true;
    conn.Close();
}
```

### Explicación

El script usa WinForms para solicitar un token de acceso personal de Databricks, que se utiliza para autenticarse en Databricks. Para cada tabla seleccionada, el script recupera la información de la cadena de conexión de Databricks, así como el nombre del esquema y de la tabla, a partir de la consulta M en la partición de la tabla seleccionada. A continuación, mediante el controlador Spark ODBC, envía a Databricks una consulta SQL que consulta las tablas information_schema para devolver la descripción de la tabla definida en Unity Catalog. A continuación, se actualiza la descripción de la tabla en el modelo semántico. También se envía a la tabla seleccionada una segunda consulta SQL con el comando DESCRIBE para obtener las descripciones de las columnas. Los resultados se recorren en un bucle y se añaden descripciones al modelo. Una vez que el script se ha ejecutado en cada tabla seleccionada, se muestra un cuadro de diálogo con el número de descripciones actualizadas.

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-pat.png" alt="Prompt for Databricks personal access token" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> El script le solicitará un token de acceso personal de Databricks para que pueda autenticarse en Databricks.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-add-databricks-metadata-descriptions-done.png" alt="The number of descriptions updated" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> Después de que el script se haya ejecutado para cada tabla seleccionada, se muestra el número de descripciones actualizadas.</figcaption>
</figure>



