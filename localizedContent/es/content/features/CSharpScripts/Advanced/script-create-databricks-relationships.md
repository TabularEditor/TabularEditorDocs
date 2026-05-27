---
uid: script-create-databricks-relationships
title: Crear relaciones de Databricks
author: Johnny Winter
updated: 2026-04-08
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Crear relaciones de Databricks

## Propósito del script

Este script se creó como parte de la serie Tabular Editor x Databricks. En Unity Catalog es posible definir relaciones de clave primaria y foránea entre tablas. Este script puede reutilizar esta información para detectar y crear automáticamente relaciones en Tabular Editor. Al importar las relaciones, el script también ocultará las claves principales y foráneas y establecerá IsAvailableInMDX en false (excepto en el caso de las claves principales de tipo DateTime). Las claves principales también se marcan como IsKey = TRUE en el modelo semántico. <br></br>

> [!NOTE]
> Este script requiere un controlador ODBC de Databricks. Recomendamos el nuevo [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download), que sustituye al Simba Spark ODBC Driver heredado. El script detecta automáticamente qué controlador está instalado y lo usa en consecuencia.

En cada ejecución del script, se te solicitará un token de acceso personal de Databricks. Esto es necesario para autenticarse en Databricks.
El script utiliza las tablas information_schema de Unity Catalog para recuperar información sobre las relaciones, por lo que quizá deba consultarlo con su administrador de Databricks para asegurarse de que tiene permisos para consultarlas. <br></br>

## Script

### Crear relaciones de Databricks

```csharp
/*
 * Título: Crear relaciones de Databricks
 * Autor: Johnny Winter, greyskullanalytics.com
 *
 * Este script, cuando se ejecuta, recorre las tablas seleccionadas actualmente y envía una consulta a las tablas de Information Schema de Databricks para comprobar si se ha definido alguna clave foránea.
 * Cuando se identifican claves foráneas, el script crea relaciones entre las tablas del modelo semántico.
 * Excepto en las columnas de dimensión de tipo datetime, las columnas clave se ocultarán una vez creadas las relaciones; las claves primarias se marcarán como claves primarias y IsAvailableInMDX se establecerá en false.
 * Paso 1:  Selecciona una o varias tablas del modelo. Deben ser tablas que tengan definida una relación de clave foránea en Unity Catalog
            (normalmente tablas de hechos, aunque también pueden ser tablas puente o dimensiones outrigger).
 * Paso 2:  Ejecuta este script
 * Paso 3:  Introduce tu Databricks Personal Access Token cuando se te solicite
 * Paso 4:  El script se conectará a Databricks y detectará dónde existen claves foráneas en la tabla seleccionada. 
            Si la relación no existe ya en el modelo semántico, se creará.
            Si ya existe una relación entre las dos tablas, la nueva relación se creará como inactiva
            Para cada tabla procesada, un cuadro de mensaje mostrará el número de relaciones creadas.
 *          Haz clic en Aceptar para continuar con la siguiente tabla. 
 * Notas:
 *  -   Este script requiere tener instalado el Databricks ODBC Driver (recomendado) o el controlador heredado Simba Spark ODBC Driver (descarga desde https://www.databricks.com/spark/odbc-drivers-download)
 *  -   El script detecta automáticamente qué controlador está instalado
 *  -   En cada ejecución del script, se te pedirá un Databricks Personal Access Token
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

        // Etiqueta del mensaje
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
        passwordTextBox.UseSystemPasswordChar = true; // Esto oculta la entrada
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

        // Establecer los botones predeterminado y cancelar
        this.AcceptButton = okButton;
        this.CancelButton = cancelButton;

        // Dar el foco al cuadro de texto cuando se cargue el formulario
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

//Código para recuperar la información de conexión de Databricks de la consulta M en una partición de tabla
public class DatabricksConnectionInfo
{
    public string ServerHostname { get; set; }
    public string HttpPath { get; set; }
    public string DatabaseName { get; set; }
    public string SchemaName { get; set; }
    public string TableName { get; set; }

    public override string ToString()
    {
        return $"Servidor: {ServerHostname}\n"
            + $"Ruta HTTP: {HttpPath}\n"
            + $"Base de datos: {DatabaseName}\n"
            + $"Esquema: {SchemaName}\n"
            + $"Tabla: {TableName}";
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
            // Analizar la línea Source para extraer el nombre de host del servidor y la ruta HTTP
            ParseSourceLine(mQuery, connectionInfo);

            // Analizar la línea Database para extraer el nombre de la base de datos
            ParseDatabaseLine(mQuery, connectionInfo);

            // Analizar la línea Schema para extraer el nombre del esquema
            ParseSchemaLine(mQuery, connectionInfo);

            // Analizar la línea Data para extraer el nombre de la tabla
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
        // Patrón para coincidir con ambas opciones:
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
                "No se encontró una definición válida de Source en la consulta M (admite los conectores Databricks y DatabricksMultiCloud)"
            );

        connectionInfo.ServerHostname = sourceMatch.Groups[1].Value;
        connectionInfo.HttpPath = sourceMatch.Groups[2].Value;
    }

    private static void ParseDatabaseLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // Patrón para coincidir con: Database = Source{[Name="databasename",Kind="Database"]}[Data],
        var databasePattern =
            @"Database\s*=\s*Source\s*{\s*\[\s*Name\s*=\s*""([^""]+)""\s*,\s*Kind\s*=\s*""Database""\s*\]\s*}\s*\[\s*Data\s*\]";
        var databaseMatch = Regex.Match(
            mQuery,
            databasePattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!databaseMatch.Success)
            throw new FormatException("No se encontró una definición válida de Database en la consulta M");

        connectionInfo.DatabaseName = databaseMatch.Groups[1].Value;
    }

    private static void ParseSchemaLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // Patrón para coincidir con: Schema = Database{[Name="schemaname",Kind="Schema"]}[Data],
        var schemaPattern =
            @"Schema\s*=\s*Database\s*{\s*\[\s*Name\s*=\s*""([^""]+)""\s*,\s*Kind\s*=\s*""Schema""\s*\]\s*}\s*\[\s*Data\s*\]";
        var schemaMatch = Regex.Match(
            mQuery,
            schemaPattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!schemaMatch.Success)
            throw new FormatException("No se encontró una definición válida de Schema en la consulta M");

        connectionInfo.SchemaName = schemaMatch.Groups[1].Value;
    }

    private static void ParseDataLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // Patrón para coincidir con: Data = Schema{[Name="tablename",Kind="Table"]}[Data]
        var dataPattern =
            @"Data\s*=\s*Schema\s*{\s*\[\s*Name\s*=\s*""([^""]+)""\s*,\s*Kind\s*=\s*""Table""\s*\]\s*}\s*\[\s*Data\s*\]";
        var dataMatch = Regex.Match(
            mQuery,
            dataPattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!dataMatch.Success)
            throw new FormatException("No se encontró una definición válida de Data en la consulta M");

        connectionInfo.TableName = dataMatch.Groups[1].Value;
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//script principal



//comprobar que has seleccionado una tabla
if (Selected.Tables.Count == 0)
{
    // alternar el indicador giratorio "Running Macro"
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox("Selecciona una o varias tablas", MsgBoxStyle.Critical, "Se requiere una tabla");
    return;
}

//solicitar el token de acceso personal: necesario para autenticarse en Databricks
string dbxPAT;
do
{
    // alternar el indicador giratorio "Running Macro"
    ScriptHelper.WaitFormVisible = false;
    dbxPAT = MaskedInputHelper.GetMaskedInput(
        "Introduce tu Databricks Personal Access Token (necesario para conectarte al SQL Endpoint)",
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

// alternar el indicador giratorio "Running Macro"
ScriptHelper.WaitFormVisible = true;

// detectar automáticamente el controlador ODBC de Databricks
string driverPath;
string newDriverPath = @"C:\Program Files\Databricks ODBC Driver";
string legacyDriverPath = @"C:\Program Files\Simba Spark ODBC Driver";

if (System.IO.Directory.Exists(newDriverPath))
{
    driverPath = newDriverPath;
}
else if (System.IO.Directory.Exists(legacyDriverPath))
{
    driverPath = legacyDriverPath;
}
else
{
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox(
        @"No se encontró ningún controlador ODBC de Databricks.

Instala el Databricks ODBC Driver desde:
https://www.databricks.com/spark/odbc-drivers-download

Rutas de instalación esperadas:
  " + newDriverPath + @"
  " + legacyDriverPath,
        MsgBoxStyle.Critical,
        "Controlador ODBC no encontrado"
    );
    return;
}

//para cada tabla seleccionada, obtener la información de conexión de Databricks a partir de la información de la partición
foreach (var t in Selected.Tables)
{
    string mQuery = t.Partitions[t.Name].Expression;
    var connectionInfo = PowerQueryMParser.ParseMQuery(mQuery);
    var rels = 0;
    // Acceder a los componentes individuales
    string serverHostname = connectionInfo.ServerHostname;
    string httpPath = connectionInfo.HttpPath;
    string databaseName = connectionInfo.DatabaseName;
    string schemaName = connectionInfo.SchemaName;
    string tableName = connectionInfo.TableName;

    //usar esta consulta para comprobar si se ha definido alguna relación de clave primaria/foránea en Unity Catalog
    var query =
        @"
        SELECT
            fk.table_catalog AS fk_table_catalog,
            fk.table_schema AS fk_table_schema,
            fk.table_name AS fk_table_name,
            fk.column_name AS fk_column,
            pk.table_catalog AS pk_table_catalog,
            pk. table_schema AS pk_table_schema,
            pk.table_name AS pk_table_name,
            pk.column_name AS pk_column
        FROM
            "
        + databaseName
        + @".information_schema.key_column_usage fk
            INNER JOIN "
        + databaseName
        + @".information_schema.referential_constraints rc
                ON fk.constraint_catalog = rc.constraint_catalog
                AND fk.constraint_schema = rc.constraint_schema
                AND fk.constraint_name = rc.constraint_name
            INNER JOIN "
        + databaseName
        + @".information_schema.key_column_usage pk
                ON rc.unique_constraint_catalog = pk.constraint_catalog
                AND rc.unique_constraint_schema = pk.constraint_schema
            AND rc.unique_constraint_name = pk.constraint_name
        WHERE
            fk.table_schema = '"
        + schemaName
        + @"'
            AND fk.table_name = '"
        + tableName
        + @"'
        AND fk.position_in_unique_constraint = 1
";

    //establecer la cadena de conexión de DBX
    var odbcConnStr =
        @"Driver=" + driverPath + ";Host="
        + serverHostname
        + ";Port=443;HTTPPath="
        + httpPath
        + ";SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD="
        + dbxPAT;

    //probar la conexión
    OdbcConnection conn = new OdbcConnection(odbcConnStr);
    try
    {
        conn.Open();
    }
    catch
    {
        // alternar el indicador giratorio "Running Macro"
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"Error de conexión (con el controlador: " + driverPath + @")

Comprueba los siguientes requisitos previos:
    
- debes tener instalado el Databricks ODBC Driver 
(descarga desde https://www.databricks.com/spark/odbc-drivers-download)

- comprueba que el nombre del servidor de Databricks "
                + serverHostname
                + @" es correcto

- comprueba que el SQL Endpoint / HTTP Path de Databricks "
                + httpPath
                + @" es correcto

- comprueba que has usado un Personal Access Token válido",
            MsgBoxStyle.Critical,
            "Error de conexión"
        );
        return;
    }

    //enviar consulta
    OdbcDataAdapter da = new OdbcDataAdapter(query, conn);
    var dbxRelationships = new sysData.DataTable();

    try
    {
        da.Fill(dbxRelationships);
    }
    catch
    {
        // alternar el indicador giratorio "Running Macro"
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"Error de conexión

    Puede ser que: 
        - la tabla "
                + schemaName
                + "."
                + tableName
                + " no exista"
                + @"
        
        - no tengas permisos para consultar esta tabla
        
        - la conexión haya superado el tiempo de espera. Comprueba que el clúster de SQL Endpoint está en ejecución",
            MsgBoxStyle.Critical,
            "Error de conexión"
        );
        return;
    }

    //para cada tabla del modelo, comprobar si coincide con una fila de la consulta de Databricks
    foreach (var dt in Model.Tables)
    {
        //obtener la información de la tabla de origen
        string sourceMQuery = dt.Partitions[dt.Name].Expression;
        var sourceConnectionInfo = PowerQueryMParser.ParseMQuery(sourceMQuery);
        // Acceder a los componentes individuales
        string sourceSchemaName = sourceConnectionInfo.SchemaName;
        string sourceTableName = sourceConnectionInfo.TableName;

        foreach (sysData.DataRow row in dbxRelationships.Rows)
        {
            if (
                string.Equals(
                    sourceSchemaName + "." + sourceTableName,
                    row["pk_table_schema"].ToString() + "." + row["pk_table_name"].ToString(),
                    StringComparison.OrdinalIgnoreCase
                )
            )
            {
                var dimTable = dt;
                foreach (var dc in dt.DataColumns)
                    if (dc.SourceColumn == row["pk_column"].ToString())
                    {
                        var dimColumn = dc;

                        foreach (var fc in t.DataColumns)
                            if (fc.SourceColumn == row["fk_column"].ToString())
                            {
                                var factColumn = fc;

                                // Comprobar si ya existe una relación entre las dos columnas:
                                if (
                                    !Model.Relationships.Any(r =>
                                        r.FromColumn == factColumn && r.ToColumn == dimColumn
                                    )
                                )
                                {
                                    // Si ya existen relaciones entre las dos tablas, las nuevas relaciones se crearán como inactivas:
                                    var makeInactive = Model.Relationships.Any(r =>
                                        r.FromTable == t && r.ToTable == dimTable
                                    );

                                    // Agregar la nueva relación:
                                    var rel = Model.AddRelationship();
                                    rel.FromColumn = factColumn;
                                    rel.ToColumn = dimColumn;
                                    factColumn.IsHidden = true;
                                    factColumn.IsAvailableInMDX = false;
                                    dimColumn.IsKey = true;
                                    if (dc.DataType != DataType.DateTime)
                                    {
                                        dimColumn.IsHidden = true;
                                        dimColumn.IsAvailableInMDX = false;
                                    }

                                    if (makeInactive)
                                        rel.IsActive = false;
                                    rels = rels + 1;
                                }
                            }
                    }
            }
        }
    }
    // alternar el indicador giratorio "Running Macro"
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox(
        rels + " relaciones añadidas a " + t.Name,
        MsgBoxStyle.Information,
        "Agregar relaciones"
    );
    // alternar el indicador giratorio "Running Macro"
    ScriptHelper.WaitFormVisible = true;
    conn.Close();
}
```

### Explicación

El script usa WinForms para solicitar un token de acceso personal de Databricks, que se utiliza para autenticarse en Databricks. Detecta automáticamente si está instalado el nuevo Databricks ODBC Driver o el controlador heredado Simba Spark ODBC Driver. Para cada tabla seleccionada, el script recupera la información de la cadena de conexión de Databricks y el esquema y el nombre de la tabla a partir de la consulta M de la partición de la tabla seleccionada. A continuación, con el controlador ODBC detectado, envía a Databricks una consulta SQL que consulta las tablas information_schema para encontrar cualquier relación de clave foránea definida en Unity Catalog para esa tabla. Para cada fila devuelta en la consulta SQL, el script busca en el modelo nombres de tablas y columnas coincidentes y, si aún no existe una relación, crea una nueva. En las dimensiones con roles, donde la misma tabla puede tener varias claves externas relacionadas con una sola tabla, la primera relación detectada será la activa y todas las demás relaciones posteriores se crearán como inactivas. El script también ocultará las claves primarias y foráneas, y establecerá IsAvailableInMDX en false (con la excepción de las claves primarias de tipo DateTime). Las claves primarias también se marcan como IsKey = TRUE en el modelo semántico. Después de ejecutar el script para cada tabla seleccionada, aparecerá un cuadro de diálogo que mostrará cuántas relaciones nuevas se han creado.

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-before.png" alt="Table relationships before running the script" style="width: 1000px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Antes de ejecutar el script, no hay relaciones definidas.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-pat.png" alt="Prompt for Databricks personal access token" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> El script le solicitará un token de acceso personal de Databricks para poder autenticarse en Databricks.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-done.png" alt="The number of new relationships created" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 3:</strong> Después de ejecutar el script para cada tabla seleccionada, se muestra el número de relaciones nuevas creadas.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-after.png" alt="Table relationships after running the script" style="width: 750px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 4:</strong> Relaciones entre tablas después de ejecutar el script.</figcaption>
</figure>

