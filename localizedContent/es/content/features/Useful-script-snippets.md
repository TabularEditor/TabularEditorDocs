---
uid: useful-script-snippets
title: Fragmentos de script útiles
author: Daniel Otykier
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Fragmentos de script útiles

Aquí tienes una colección de pequeños fragmentos de script para empezar a usar la [funcionalidad de scripting avanzado](/Advanced-Scripting) de Tabular Editor. Muchos de estos scripts son útiles para guardarlos como [Acciones personalizadas](/Custom-Actions), de modo que puedas reutilizarlos fácilmente desde el menú contextual.

Además, asegúrate de echar un vistazo a nuestra biblioteca de scripts @csharp-script-library para ver más ejemplos reales de lo que puedes hacer con las capacidades de scripting de Tabular Editor.

***

## Crear medidas a partir de columnas

```csharp
// Creates a SUM measure for every currently selected column and hide the column.
foreach(var c in Selected.Columns)
{
    var newMeasure = c.Table.AddMeasure(
        "Sum of " + c.Name,                    // Name
        "SUM(" + c.DaxObjectFullName + ")",    // DAX expression
        c.DisplayFolder                        // Display Folder
    );
    
    // Set the format string on the new measure:
    newMeasure.FormatString = "0.00";

    // Provide some documentation:
    newMeasure.Description = "This measure is the sum of column " + c.DaxObjectFullName;

    // Hide the base column:
    c.IsHidden = true;
}
```

Este fragmento usa la función `<Table>.AddMeasure(<name>, <expression>, <displayFolder>)` para crear una nueva medida en la tabla. Usamos la propiedad `DaxObjectFullName` para obtener el nombre completo de la columna y usarlo en la expresión DAX: `'TableName'[ColumnName]`.

***

## Generar medidas de inteligencia temporal

Primero, crea acciones personalizadas para agregaciones individuales de inteligencia temporal. Por ejemplo:

```csharp
// Creates a TOTALYTD measure for every selected measure.
foreach(var m in Selected.Measures) {
    m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
}
```

Aquí usamos la propiedad `DaxObjectName` para generar una referencia sin calificar y usarla en la expresión DAX, ya que se trata de una medida: `[MeasureName]`. Guarda esto como una Acción personalizada llamada "Inteligencia temporal\Crear medida YTD" que se aplique a las medidas. Crea acciones similares para MTD, LY y lo que necesites. Después, crea lo siguiente como una nueva acción:

```csharp
// Invoca todas las Acciones personalizadas de inteligencia temporal:
CustomAction(@"Time Intelligence\Create YTD measure");
CustomAction(@"Time Intelligence\Create MTD measure");
CustomAction(@"Time Intelligence\Create LY measure");
```

Esto ilustra cómo puedes ejecutar una (o varias) acciones personalizadas desde dentro de otra acción (ten cuidado con las referencias circulares: harán que Tabular Editor se bloquee). Guarda esto como una nueva acción personalizada "Inteligencia temporal\Todo lo anterior", y tendrás una forma sencilla de generar todas tus medidas de inteligencia temporal con un solo clic:

![imagen](https://user-images.githubusercontent.com/8976200/36632257-5565c8ca-197c-11e8-8498-82667b6e1049.png)

Por supuesto, también puedes poner todos tus cálculos de inteligencia temporal en un único script como el siguiente:

```csharp
var dateColumn = "'Date'[Date]";

// Crea medidas de inteligencia temporal para cada medida seleccionada:
foreach(var m in Selected.Measures) {
    // Acumulado del año:
    m.Table.AddMeasure(
        m.Name + " YTD",                                       // Nombre
        "TOTALYTD(" + m.DaxObjectName + ", " + dateColumn + ")",     // Expresión DAX
        m.DisplayFolder                                        // Carpeta de visualización
    );
    
    // Año anterior:
    m.Table.AddMeasure(
        m.Name + " PY",                                       // Nombre
        "CALCULATE(" + m.DaxObjectName + ", SAMEPERIODLASTYEAR(" + dateColumn + "))",     // Expresión DAX
        m.DisplayFolder                                        // Carpeta de visualización
    );    
    
    // Variación interanual
    m.Table.AddMeasure(
        m.Name + " YoY",                                       // Nombre
        m.DaxObjectName + " - [" + m.Name + " PY]",            // Expresión DAX
        m.DisplayFolder                                        // Carpeta de visualización
    );
    
    // Variación interanual %:
    m.Table.AddMeasure(
        m.Name + " YoY%",                                       // Nombre
        "DIVIDE([" + m.Name + " YoY], [" + m.Name + " PY])",    // Expresión DAX
        m.DisplayFolder                                         // Carpeta de visualización
    ).FormatString = "0.0 %";                                   // Establecer la cadena de formato como porcentaje
    
    // Acumulado del trimestre:
    m.Table.AddMeasure(
        m.Name + " QTD",                                            // Nombre
        "TOTALQTD(" + m.DaxObjectName + ", " + dateColumn + ")",    // Expresión DAX
        m.DisplayFolder                                             // Carpeta de visualización
    );
    
    // Acumulado del mes:
    m.Table.AddMeasure(
        m.Name + " MTD",                                       // Nombre
        "TOTALMTD(" + m.DaxObjectName + ", " + dateColumn + ")",     // Expresión DAX
        m.DisplayFolder                                        // Carpeta de visualización
    );
}
```

### Incluir propiedades adicionales

Si quieres establecer propiedades adicionales en la medida recién creada, el script anterior se puede modificar así:

```csharp
// Crea una medida TOTALYTD para cada medida seleccionada.
foreach(var m in Selected.Measures) {
    var newMeasure = m.Table.AddMeasure(
        m.Name + " YTD",                                       // Nombre
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // Expresión DAX
        m.DisplayFolder                                        // Carpeta de visualización
    );
    newMeasure.FormatString = m.FormatString;               // Copiar la cadena de formato de la medida original
    foreach(var c in Model.Cultures) {
        newMeasure.TranslatedNames[c] = m.TranslatedNames[c] + " YTD"; // Copiar los nombres traducidos para cada configuración regional
        newMeasure.TranslatedDisplayFolders[c] = m.TranslatedDisplayFolders[c]; // Copiar las carpetas de visualización traducidas
    }
}
```

***

## Establecer traducciones predeterminadas

A veces es útil tener traducciones predeterminadas aplicadas a todos los objetos (visibles). En este caso, una traducción predeterminada es simplemente el nombre, la descripción o la carpeta de visualización originales de un objeto. Una de las ventajas de esto es que todos los objetos de traducción se incluirán al exportar traducciones en formato JSON; es decir, para usarlas con [SSAS Tabular Translator](https://www.sqlbi.com/tools/ssas-tabular-translator/).

El script siguiente recorrerá todas las configuraciones regionales del modelo y, para cada objeto visible que aún no tenga una traducción, asignará los valores predeterminados:

```csharp
// Aplicar traducciones predeterminadas a todos los objetos traducibles (visibles) en todas las configuraciones regionales del modelo:
foreach(var culture in Model.Cultures)
{
    ApplyDefaultTranslation(Model, culture);
    foreach(var perspective in Model.Perspectives)
        ApplyDefaultTranslation(perspective, culture);
    foreach(var table in Model.Tables.Where(t => t.IsVisible))
        ApplyDefaultTranslation(table, culture);
    foreach(var measure in Model.AllMeasures.Where(m => m.IsVisible))
        ApplyDefaultTranslation(measure, culture);
    foreach(var column in Model.AllColumns.Where(c => c.IsVisible))
        ApplyDefaultTranslation(column, culture);
    foreach(var hierarchy in Model.AllHierarchies.Where(h => h.IsVisible))
        ApplyDefaultTranslation(hierarchy, culture);
    foreach(var level in Model.AllLevels.Where(l => l.Hierarchy.IsVisible))
        ApplyDefaultTranslation(level, culture);
}

void ApplyDefaultTranslation(ITranslatableObject obj, Culture culture)
{
    // Solo aplicar la traducción predeterminada cuando todavía no exista una traducción:
    if(string.IsNullOrEmpty(obj.TranslatedNames[culture]))
    {
        // Traducción predeterminada del nombre:
        obj.TranslatedNames[culture] = obj.Name;

        // Traducción predeterminada de la descripción:
        var dObj = obj as IDescriptionObject;
        if(dObj != null && string.IsNullOrEmpty(obj.TranslatedDescriptions[culture])
            && !string.IsNullOrEmpty(dObj.Description))
        {
            obj.TranslatedDescriptions[culture] = dObj.Description;
        }

        // Traducción predeterminada de la carpeta de visualización:
        var fObj = obj as IFolderObject;
        if(fObj != null && string.IsNullOrEmpty(fObj.TranslatedDisplayFolders[culture])
            && !string.IsNullOrEmpty(fObj.DisplayFolder))
        {
            fObj.TranslatedDisplayFolders[culture] = fObj.DisplayFolder;
        }
    }
}
```

***

## Gestionar perspectivas

Las medidas, columnas, jerarquías y tablas exponen la propiedad `InPerspective`, que contiene un valor True/False para cada perspectiva del modelo, e indica si el objeto en cuestión pertenece a esa perspectiva o no. Por ejemplo:

```csharp
foreach(var measure in Selected.Measures)
{
    measure.InPerspective["Inventory"] = true;
    measure.InPerspective["Reseller Operation"] = false;
}
```

El script anterior garantiza que todas las medidas seleccionadas sean visibles en la perspectiva "Inventory" y estén ocultas en la perspectiva "Reseller Operation".

Además de obtener/establecer la pertenencia a una perspectiva individual, la propiedad `InPerspective` también admite los siguientes métodos:

- `<<object>>.InPerspective.None()` - quita el objeto de todas las perspectivas.
- `<<object>>.InPerspective.All()` - incluye el objeto en todas las perspectivas.
- `<<object>>.CopyFrom(string[] perspectives)` - incluye el objeto en todas las perspectivas especificadas (matriz de cadenas que contiene los nombres de las perspectivas).
- `<<object>>.CopyFrom(perspectiveIndexer perspectives)` - copia las inclusiones en perspectivas desde otra propiedad `InPerspective`.

Este último puede usarse para copiar pertenencias a perspectivas de un objeto a otro. Por ejemplo, supongamos que tienes una medida base [Reseller Total Sales] y quieres asegurarte de que todas las medidas seleccionadas actualmente estén visibles en las mismas perspectivas que esta medida base. El siguiente script lo resuelve:

```csharp
var baseMeasure = Model.Tables["Reseller Sales"].Measures["Reseller Total Sales"];

foreach(var measure in Selected.Measures)
{
    /* Quita el comentario de la línea siguiente si quieres que 'measure' quede oculta
       en las perspectivas en las que 'baseMeasure' está oculta: */
    // measure.InPerspective.None();

    measure.InPerspective.CopyFrom(baseMeasure.InPerspective);
}
```

Esta técnica también se puede usar al generar nuevos objetos desde código. Por ejemplo, si queremos asegurarnos de que las medidas de inteligencia temporal generadas automáticamente solo sean visibles en las mismas perspectivas que su medida base, podemos ampliar el script de la sección anterior así:

```csharp
// Crea una medida TOTALYTD para cada medida seleccionada.
foreach(var m in Selected.Measures) {
    var newMeasure = m.Table.AddMeasure(
        m.Name + " YTD",                                       // Nombre
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // Expresión DAX
        m.DisplayFolder                                        // Carpeta de visualización
    );
    newMeasure.InPerspective.CopyFrom(m.InPerspective);        // Aplicar las perspectivas de la medida base
}
```

***

## Generación de particiones

Si necesitas proporcionar una partición personalizada para una tabla, un C# Script puede ayudarte a generar rápidamente muchas particiones. La idea básica es añadir una anotación a tu tabla que contenga la consulta SQL o M que se usará como plantilla para cada partición. Luego, el script sustituirá los parámetros de filtro según sea necesario. Por ejemplo, usando particiones SQL, podríamos añadir una anotación llamada `PartitionTemplateSQL` y establecer su valor en `SELECT * FROM fact_ResellerSales WHERE CalendarID BETWEEN {0} AND {1}`. Nuestro script sustituirá los marcadores `{0}` y `{1}` al generar las particiones finales. En este caso, `CalendarID` es un entero, pero por lo general te corresponde asegurarte de que la cadena resultante sea una consulta SQL (o M) válida.

![](https://user-images.githubusercontent.com/8976200/70135273-07c6fa00-168a-11ea-84f6-90f0b3498ed8.png)

Este ejemplo genera una partición por mes. Selecciona una tabla que tenga asignada la anotación `PartitionTemplateSQL` y luego ejecuta el script.

```csharp
var firstPartition = new DateTime(2018,1,1); // Fecha de la primera partición
var lastPartition = new DateTime(2020,12,1); // Fecha de la última partición

var templateSql = Selected.Table.GetAnnotation("PartitionTemplateSQL");
if(string.IsNullOrEmpty(templateSql)) throw new Exception("No partition template!");

var currentPartition = firstPartition;
while(currentPartition <= lastPartition)
{
    // Calcula los CalendarID "desde" y "hasta" (valores enteros) en función de la fecha de currentPartition:
    var calendarIdFrom = currentPartition.ToString("yyyyMMdd");
    var calendarIdTo = currentPartition.AddMonths(1).AddDays(-1).ToString("yyyyMMdd");
    
    // Determina un nombre único para la partición; como particionamos a nivel mensual, usamos yyyyMM:
    var partitionName = Selected.Table.Name + "_" + currentPartition.ToString("yyyyMM");
    
    // Sustituye los valores de los marcadores de posición en la plantilla SQL de partición:
    var partitionQuery = string.Format(templateSql, calendarIdFrom, calendarIdTo);
    
    // Crea la partición (usa .AddMPartition si usaste una plantilla de consulta M en lugar de SQL):
    Selected.Table.AddPartition(partitionName, partitionQuery);
    
    // Avanza al mes siguiente (cambia esto a .AddDays, .AddYears, etc. si necesitas más o menos particiones):
    currentPartition = currentPartition.AddMonths(1);
}
```

***

## Exportar las propiedades de los objetos a un archivo

En algunos flujos de trabajo, puede ser útil editar en bloque varias propiedades de los objetos con Excel. Usa el siguiente fragmento para exportar un conjunto estándar de propiedades a un archivo .TSV, que después se puede importar (ver más abajo).

```csharp
// Exporta propiedades de los objetos seleccionados actualmente:
var tsv = ExportProperties(Selected);
SaveFile("Exported Properties 1.tsv", tsv);
```

El archivo .TSV resultante se ve así al abrirlo en Excel:
![image](https://user-images.githubusercontent.com/8976200/36632472-e8e96ef6-197e-11e8-8285-6816b09ad036.png)
El contenido de la primera columna (Object) es una referencia al objeto. Si se cambia el contenido de esta columna, es posible que la importación posterior de las propiedades no funcione correctamente. Para cambiar el nombre de un objeto, cambia solo el valor de la segunda columna (Name).

De forma predeterminada, el archivo se guarda en la misma carpeta donde se encuentra TabularEditor.exe. De forma predeterminada, solo se exportan las siguientes propiedades (cuando corresponda, según el tipo de objeto exportado):

- Nombre
- Descripción
- Columna de origen
- Expresión
- Cadena de formato
- Tipo de datos

Para exportar propiedades diferentes, proporciona una lista de nombres de propiedades separados por comas, que se exportarán como segundo argumento de `ExportProperties`:

```csharp
// Exporta los nombres y las expresiones de filas de detalle de todas las medidas de la tabla seleccionada actualmente:
var tsv = ExportProperties(Selected.Table.Measures, "Name,DetailRowsExpression");
SaveFile("Exported Properties 2.tsv", tsv);
```

Los nombres de propiedad disponibles se encuentran en la [documentación de la API de TOM](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.aspx). En su mayoría son idénticos a los nombres que se muestran en la cuadrícula de propiedades de Tabular Editor, en CamelCase y sin espacios (con algunas excepciones; por ejemplo, la propiedad "Hidden" se llama `IsHidden` en la API de TOM).

Para importar propiedades, usa el siguiente fragmento:

```csharp
// Importa y aplica las propiedades del archivo especificado:
var tsv = ReadFile("Exported Properties 1.tsv");
ImportProperties(tsv);
```

### Exportación de propiedades indexadas

A partir de Tabular Editor 2.11.0, los métodos `ExportProperties` e `ImportProperties` admiten propiedades indexadas. Las propiedades indexadas son propiedades que aceptan una clave además del nombre de la propiedad. Un ejemplo es `myMeasure.TranslatedNames`. Esta propiedad representa la colección de todas las cadenas aplicadas como traducciones del nombre de `myMeasure`. En C#, puedes acceder al título traducido de una configuración regional concreta usando el operador de indexación: `myMeasure.TranslatedNames["da-DK"]`.

En resumen: ahora puedes exportar todas las traducciones, la información de perspectiva, las anotaciones, las propiedades extendidas y la información de seguridad a nivel de fila y de objetos en tu modelo tabular.

Por ejemplo, el siguiente script generará un archivo TSV con todas las medidas del modelo e información sobre en qué perspectivas es visible cada una:

```csharp
var tsv = ExportProperties(Model.AllMeasures, "Name,InPerspective");
SaveFile(@"c:\Project\MeasurePerspectives.tsv", tsv);
```

El archivo TSV se ve así al abrirlo en Excel:

![imagen](https://user-images.githubusercontent.com/8976200/85208532-956dec80-b331-11ea-8568-32dbd4cc5516.png)

Y tal y como se muestra arriba, puedes hacer cambios en Excel, guardar y luego cargar de nuevo los valores actualizados en Tabular Editor mediante `ImportProperties`.

Si quieres listar solo una perspectiva específica o unas pocas perspectivas concretas, puedes indicarlas en el segundo argumento de la llamada a `ExportProperties`:

```csharp
var tsv = ExportProperties(Model.AllMeasures, "Name,InPerspective[Inventory]");
SaveFile(@"c:\Project\MeasurePerspectiveInventory.tsv", tsv);
```

Del mismo modo, para traducciones, anotaciones, etc. Por ejemplo, si quisieras ver todas las traducciones al danés aplicadas a tablas, columnas, jerarquías, niveles y medidas:

```csharp
// Construct a list of objects:
var objects = new List<TabularNamedObject>();
objects.AddRange(Model.Tables);
objects.AddRange(Model.AllColumns);
objects.AddRange(Model.AllHierarchies);
objects.AddRange(Model.AllLevels);
objects.AddRange(Model.AllMeasures);

var tsv = ExportProperties(objects, "Name,TranslatedNames[da-DK],TranslatedDescriptions[da-DK],TranslatedDisplayFolders[da-DK]");
SaveFile(@"c:\Project\ObjectTranslations.tsv", tsv);
```

***

## Generación de documentación

El método `ExportProperties` mostrado arriba también se puede usar si quieres documentar todo el modelo o parte de él. El siguiente fragmento extraerá un conjunto de propiedades de todas las medidas o columnas visibles de un modelo tabular y lo guardará como un archivo TSV:

```csharp
// Construct a list of all visible columns and measures:
var objects = Model.AllMeasures.Where(m => !m.IsHidden && !m.Table.IsHidden).Cast<ITabularNamedObject>()
      .Concat(Model.AllColumns.Where(c => !c.IsHidden && !c.Table.IsHidden));

// Get their properties in TSV format (tabulator-separated):
var tsv = ExportProperties(objects,"Name,ObjectType,Parent,Description,FormatString,DataType,Expression");

// (Optional) Output to screen (can then be copy-pasted into Excel):
// tsv.Output();

// ...or save the TSV to a file:
SaveFile("documentation.tsv", tsv);
```

***

## Generación de medidas a partir de un archivo

Las técnicas anteriores para exportar/importar propiedades son útiles si quieres editar en bloque las propiedades de objetos _existentes_ en tu modelo. ¿Y si quieres importar una lista de medidas que todavía no existen?

Supongamos que tienes un archivo TSV (valores separados por tabulaciones) que contiene los nombres, las descripciones y las expresiones DAX de las medidas que quieres importar a un modelo tabular existente. Puedes usar el siguiente script para leer el archivo, dividirlo en filas y columnas, y generar las medidas. El script también asigna una anotación especial a cada medida, para poder eliminar medidas que se hayan creado previamente con el mismo script.

```csharp
var targetTable = Model.Tables["Program"];  // Name of the table that should hold the measures
var measureMetadata = ReadFile(@"c:\Test\MyMeasures.tsv");   // c:\Test\MyMeasures.tsv is a tab-separated file with a header row and 3 columns: Name, Description, Expression

// Delete all measures from the target table that have an "AUTOGEN" annotation with the value "1":
foreach(var m in targetTable.Measures.Where(m => m.GetAnnotation("AUTOGEN") == "1").ToList())
{
    m.Delete();
}

// Split the file into rows by CR and LF characters:
var tsvRows = measureMetadata.Split(new[] {'\r','\n'},StringSplitOptions.RemoveEmptyEntries);

// Loop through all rows but skip the first one:
foreach(var row in tsvRows.Skip(1))
{
    var tsvColumns = row.Split('\t');     // Assume file uses tabs as column separator
    var name = tsvColumns[0];             // 1st column contains measure name
    var description = tsvColumns[1];      // 2nd column contains measure description
    var expression = tsvColumns[2];       // 3rd column contains measure expression

    // This assumes that the model does not already contain a measure with the same name (if it does, the new measure will get a numeric suffix):
    var measure = targetTable.AddMeasure(name);
    measure.Description = description;
    measure.Expression = expression;
    measure.SetAnnotation("AUTOGEN", "1");  // Set a special annotation on the measure, so we can find it and delete it the next time the script is executed.
}
```

Si necesitas automatizar este proceso, guarda el script anterior en un archivo y usa la [Tabular Editor CLI](/Command-line-Options) de la siguiente manera:

```powershell
start /wait TabularEditor.exe "<path to bim file>" -S "<path to script file>" -B "<path to modified bim file>"
```

por ejemplo:

```powershell
start /wait TabularEditor.exe "c:\Projects\AdventureWorks\Model.bim" -S "c:\Projects\AutogenMeasures.cs" -B "c:\Projects\AdventureWorks\Build\Model.bim"
```

... o, si prefieres ejecutar el script en una base de datos ya desplegada:

```powershell
start /wait TabularEditor.exe "localhost" "AdventureWorks" -S "c:\Projects\AutogenMeasures.cs" -D "localhost" "AdventureWorks" -O
```

***

## Crear columnas de datos a partir de los metadatos del origen de la partición

> [!NOTE]
> El método `RefreshDataColumns()` descrito a continuación solo está disponible en **Tabular Editor 2**. En Tabular Editor 3, utiliza la opción **Import Table...** en su lugar.

Si una tabla usa una partición de tipo Query basada en un origen de datos del proveedor OLE DB, podemos actualizar automáticamente los metadatos de las columnas de esa tabla ejecutando el siguiente fragmento:

```csharp
Model.Tables["Reseller Sales"].RefreshDataColumns();
```

Esto resulta útil al agregar nuevas tablas a un modelo, para evitar tener que crear manualmente cada columna de datos de la tabla. El fragmento anterior asume que se puede acceder localmente al origen de la partición, utilizando la cadena de conexión existente del origen de la partición para la tabla 'Reseller Sales'. El fragmento anterior extraerá el esquema de la consulta de la partición y agregará una columna de datos a la tabla por cada columna de la consulta de origen.

Si necesitas proporcionar una cadena de conexión diferente para esta operación, también puedes hacerlo en el fragmento de código:

```csharp
var source = Model.DataSources["DWH"] as ProviderDataSource;
var oldConnectionString = source.ConnectionString;
source.ConnectionString = "...";   // Enter the connection string you want to use for metadata refresh
Model.Tables["Reseller Sales"].RefreshDataColumns();
source.ConnectionString = oldConnectionString;
```

Esto supone que las particiones de la tabla 'Reseller Sales' utilizan un origen de datos del proveedor llamado "DWH".

***

## Dar formato a expresiones DAX

Consulta [FormatDax](/FormatDax) para obtener más información.

```csharp
// Works in Tabular Editor version 2.13.0 or newer:
Selected.Measures.FormatDax();
```

Sintaxis alternativa:

```csharp
// Works in Tabular Editor version 2.13.0 or newer:
foreach(var m in Selected.Measures)
    m.FormatDax();
```

***

## Generar una lista de columnas de origen para una tabla

El siguiente script genera una lista con buen formato de las columnas de origen de la tabla actualmente seleccionada. Esto puede ser útil si quieres sustituir las consultas de particiones que usan `SELECT *` por una lista explícita de columnas.

```csharp
string.Join(",\r\n", 
    Selected.Table.DataColumns
        .OrderBy(c => c.SourceColumn)
        .Select(c => "[" + c.SourceColumn + "]")
    ).Output();
```

***

## Creación automática de relaciones

Si en tu equipo se usan de forma consistente ciertas convenciones de nomenclatura, enseguida verás que los scripts pueden ser aún más potentes.

El siguiente script, al ejecutarse en una o varias tablas de hechos, creará automáticamente relaciones con todas las tablas de dimensiones relevantes, en función de los nombres de las columnas. El script buscará columnas de la tabla de hechos cuyo nombre siga el patrón `xxxyyyKey`, donde xxx es un calificador opcional para dimensiones con roles y yyy es el nombre de la tabla de dimensiones. En la tabla de dimensiones, debe existir una columna llamada `yyyKey` y debe tener el mismo tipo de datos que la columna de la tabla de hechos. Por ejemplo, una columna llamada "ProductKey" se relacionará con la columna "ProductKey" de la tabla Product. Puedes especificar un sufijo de nombre de columna diferente para usar en lugar de "Key".

Si ya existe una relación entre la tabla de hechos y la de dimensiones, el script creará la nueva relación como inactiva.

```csharp
var keySuffix = "Key";

// Loop through all currently selected tables (assumed to be fact tables):
foreach(var fact in Selected.Tables)
{
    // Loop through all SK columns on the current table:
    foreach(var factColumn in fact.Columns.Where(c => c.Name.EndsWith(keySuffix)))
    {
        // Find the dimension table corresponding to the current SK column:
        var dim = Model.Tables.FirstOrDefault(t => factColumn.Name.EndsWith(t.Name + keySuffix));
        if(dim != null)
        {
            // Find the key column on the dimension table:
            var dimColumn = dim.Columns.FirstOrDefault(c => factColumn.Name.EndsWith(c.Name));
            if(dimColumn != null)
            {
                // Check whether a relationship already exists between the two columns:
                if(!Model.Relationships.Any(r => r.FromColumn == factColumn && r.ToColumn == dimColumn))
                {
                    // If relationships already exists between the two tables, new relationships will be created as inactive:
                    var makeInactive = Model.Relationships.Any(r => r.FromTable == fact && r.ToTable == dim);

                    // Add the new relationship:
                    var rel = Model.AddRelationship();
                    rel.FromColumn = factColumn;
                    rel.ToColumn = dimColumn;
                    factColumn.IsHidden = true;
                    if(makeInactive) rel.IsActive = false;
                }
            }
        }
    }
}
```

***

## Crear la medida DumpFilters

Inspirado en [este artículo](https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/), aquí tienes un script que creará una medida [DumpFilters] en la tabla actualmente seleccionada:

```csharp
var dax = "VAR MaxFilters = 3 RETURN ";
var dumpFilterDax = @"IF (
    ISFILTERED ( {0} ), 
    VAR ___f = FILTERS ( {0} )
    VAR ___r = COUNTROWS ( ___f )
    VAR ___t = TOPN ( MaxFilters, ___f, {0} )
    VAR ___d = CONCATENATEX ( ___t, {0}, "", "" )
    VAR ___x = ""{0} = "" & ___d 
        & IF(___r > MaxFilters, "", ... ["" & ___r & "" items selected]"") & "" ""
    RETURN ___x & UNICHAR(13) & UNICHAR(10)
)";

// Loop through all columns of the model to construct the complete DAX expression:
bool first = true;
foreach(var column in Model.AllColumns)
{
    if(!first) dax += " & ";
    dax += string.Format(dumpFilterDax, column.DaxObjectFullName);
    if(first) first = false;
}

// Add the measure to the currently selected table:
Selected.Table.AddMeasure("DumpFilters", dax);
```

***

## De CamelCase a formato de título

Un esquema de nomenclatura habitual para columnas y tablas en una base de datos relacional es CamelCase. Es decir, los nombres no contienen espacios y cada palabra empieza con una letra mayúscula. En un modelo tabular, las tablas y columnas que no están ocultas serán visibles para los usuarios de negocio, por lo que a menudo sería preferible usar un esquema de nombres más "legible". El siguiente script convertirá nombres en formato CamelCase a formato Proper Case. Las secuencias de letras en mayúsculas se mantienen tal cual (acrónimos). Por ejemplo, el script convertirá lo siguiente:

- `CustomerWorkZipcode` a `Customer Work Zipcode`
- `CustomerAccountID` a `Customer Account ID`
- `NSASecurityID` a `NSA Security ID`

Recomiendo encarecidamente guardar este script como una acción personalizada que se aplique a todos los tipos de objetos (excepto Relación, KPI, Permiso de tabla y Traducción, ya que estos no tienen una propiedad "Name" editable):

```csharp
foreach(var obj in Selected.OfType<ITabularNamedObject>()) {
    var oldName = obj.Name;
    var newName = new System.Text.StringBuilder();
    for(int i = 0; i < oldName.Length; i++) {
        // First letter should always be capitalized:
        if(i == 0) newName.Append(Char.ToUpper(oldName[i]));

        // A sequence of two uppercase letters followed by a lowercase letter should have a space inserted
        // after the first letter:
        else if(i + 2 < oldName.Length && char.IsLower(oldName[i + 2]) && char.IsUpper(oldName[i + 1]) && char.IsUpper(oldName[i]))
        {
            newName.Append(oldName[i]);
            newName.Append(" ");
        }

        // All other sequences of a lowercase letter followed by an uppercase letter, should have a space
        // inserted after the first letter:
        else if(i + 1 < oldName.Length && char.IsLower(oldName[i]) && char.IsUpper(oldName[i+1]))
        {
            newName.Append(oldName[i]);
            newName.Append(" ");
        }
        else
        {
            newName.Append(oldName[i]);
        }
    }
    obj.Name = newName.ToString();
}
```

***

## Exportar dependencias entre tablas y medidas

Supongamos que tienes un modelo grande y complejo y quieres saber qué medidas podrían verse afectadas por cambios en los datos subyacentes.

El siguiente script recorre todas las medidas de tu modelo y, para cada una, genera una lista de las tablas de las que depende, tanto directa como indirectamente. La lista se genera como un archivo separado por tabulaciones.

```csharp
string tsv = "Measure\tDependsOnTable"; // TSV file header row

// Loop through all measures:
foreach(var m in Model.AllMeasures) {

    // Get a list of ALL objects referenced by this measure (both directly and indirectly through other measures):
    var allReferences = m.DependsOn.Deep();

    // Filter the previous list of references to table references only. For column references, let's get th
    // table that each column belongs to. Finally, keep only distinct tables:
    var allTableReferences = allReferences.OfType<Table>()
        .Concat(allReferences.OfType<Column>().Select(c => c.Table)).Distinct();

    // Output TSV rows - one for each table reference:
    foreach(var t in allTableReferences)
        tsv += string.Format("\r\n{0}\t{1}", m.Name, t.Name);
}
    
tsv.Output();   
// SaveFile("c:\\MyProjects\\SSAS\\MeasureTableDependencies.tsv", tsv); // Uncomment this line to save output to a file
```

***

## Configurar agregaciones (solo para Dataset de Power BI)

A partir de [Tabular Editor 2.11.3](https://github.com/TabularEditor/TabularEditor/releases/tag/2.11.3), ya puedes establecer la propiedad `AlternateOf` en una columna, lo que te permite definir tablas de agregación en tu modelo. Esta característica está habilitada para Dataset de Power BI (nivel de compatibilidad 1460 o superior) mediante el punto de conexión XMLA del servicio Power BI.

Selecciona un rango de columnas y ejecuta el siguiente script para inicializar la propiedad `AlternateOf` en ellas:

```csharp
foreach(var col in Selected.Columns) col.AddAlternateOf();
```

Ve recorriendo las columnas una a una para asignarlas a la columna base y establecer el tipo de resumen correspondiente (Sum/Min/Max/GroupBy). Como alternativa, si quieres automatizar este proceso y las columnas de tu tabla de agregación tienen los mismos nombres que las columnas de la tabla base, puedes usar el siguiente script, que asignará las columnas por ti:

```csharp
// Select two tables in the tree (ctrl+click). The aggregation table is assumed to be the one with fewest columns.
// This script will set up the AlternateOf property on all columns on the aggregation table. Agg table columns must
// have the same name as the base table columns for this script to work.
var aggTable = Selected.Tables.OrderBy(t => t.Columns.Count).First();
var baseTable = Selected.Tables.OrderByDescending(t => t.Columns.Count).First();

foreach(var col in aggTable.Columns)
{
    // The script will set the summarization type to "Group By", unless the column uses data type decimal/double:
    var summarization = SummarizationType.GroupBy;
    if(col.DataType == DataType.Double || col.DataType == DataType.Decimal)
        summarization = SummarizationType.Sum;
    
    col.AddAlternateOf(baseTable.Columns[col.Name], summarization);
}
```

Después de ejecutar el script, deberías ver que la propiedad `AlternateOf` se ha asignado a todas las columnas de tu tabla de agregación (consulta la captura de pantalla a continuación). Ten en cuenta que la partición de la tabla base debe usar DirectQuery para que las agregaciones funcionen.

![imagen](https://user-images.githubusercontent.com/8976200/85851134-6ed70800-b7ae-11ea-82eb-37fcaa2ca9c4.png)

***

## Consultas en Analysis Services

A partir de la versión [2.12.1](https://github.com/TabularEditor/TabularEditor/releases/tag/2.12.1), Tabular Editor proporciona varios métodos auxiliares para ejecutar consultas DAX y evaluar expresiones DAX en su modelo. Estos métodos solo funcionan cuando los metadatos del modelo se han cargado directamente desde una instancia de Analysis Services, por ejemplo, cuando se usa la opción "Archivo > Abrir > Desde BD...", o cuando se usa la integración de herramientas externas de Power BI de Tabular Editor.

Están disponibles los siguientes métodos:

| Método                                                        | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void ExecuteCommand(string tmslOrXmla, bool isXmla = false)` | Este método envía el script TMSL o XMLA especificado a la instancia conectada de Analysis Services. Esto resulta útil cuando desea actualizar datos de una tabla en la instancia de AS. Tenga en cuenta que, si utiliza este método para realizar cambios de metadatos en su modelo, los metadatos del modelo local quedarán desincronizados respecto a los metadatos de la instancia de AS, y es posible que reciba una advertencia de conflicto de versiones la próxima vez que intente guardar los metadatos del modelo. Establezca el parámetro `isXmla` en `true` si envía un script XMLA. |
| `IDataReader ExecuteReader(string dax)`                       | Ejecuta la _consulta_ DAX especificada contra la base de datos de AS conectada y devuelve el objeto [AmoDataReader](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.amodatareader?view=analysisservices-dotnet) resultante. Una consulta DAX contiene una o varias instrucciones [`EVALUATE`](https://dax.guide/EVALUATE). Tenga en cuenta que no puede tener varios lectores de datos abiertos al mismo tiempo. Tabular Editor los cerrará automáticamente en caso de que olvide cerrar o liberar el lector de forma explícita.                                         |
| `Dataset ExecuteDax(string dax)`                              | Ejecuta la _consulta_ DAX especificada contra la base de datos de AS conectada y devuelve un objeto [Dataset](https://docs.microsoft.com/en-us/dotnet/api/system.data.dataset?view=netframework-4.6) que contiene los datos devueltos por la consulta. Una consulta DAX contiene una o varias instrucciones [`EVALUATE`](https://dax.guide/EVALUATE). El objeto Dataset resultante contiene una DataTable por cada instrucción `EVALUATE`. No se recomienda devolver tablas de datos muy grandes, ya que pueden provocar errores de falta de memoria u otros errores de estabilidad.            |
| `object EvaluateDax(string dax)`                              | Ejecuta la _expresión_ DAX especificada contra la base de datos de AS conectada y devuelve un objeto que representa el resultado. Si la expresión DAX es escalar, se devuelve un objeto del tipo correspondiente (string, long, decimal, double, DateTime). Si la expresión DAX es de tipo tabla, se devuelve un [DataTable](https://docs.microsoft.com/en-us/dotnet/api/system.data.datatable?view=netframework-4.6).                                                                                                                                                                       |

Los métodos están acotados al objeto `Model.Database`, pero también se pueden ejecutar directamente sin ningún prefijo.

Darren Gosbell presenta [aquí](https://darren.gosbell.com/2020/08/the-best-way-to-generate-data-driven-measures-in-power-bi-using-tabular-editor/) un caso de uso interesante: generar medidas basadas en datos mediante el método `ExecuteDax`.

Otra opción es crear un script reutilizable para actualizar una tabla. Por ejemplo, para realizar un recálculo, utilice lo siguiente:

```csharp
var type = "calculate";
var database = Model.Database.Name;
var table = Selected.Table.Name;
var tmsl = "{ \"refresh\": { \"type\": \"%type%\", \"objects\": [ { \"database\": \"%db%\", \"table\": \"%table%\" } ] } }"
    .Replace("%type%", type)
    .Replace("%db%", database)
    .Replace("%table%", table);

ExecuteCommand(tmsl);
```

### Vaciar la caché del motor de Analysis Services

A partir de Tabular Editor 2.16.6 o Tabular Editor 3.2.3, puede usar la siguiente sintaxis para enviar comandos XMLA sin procesar a Analysis Services. El siguiente ejemplo muestra cómo se puede usar para vaciar la caché del motor de AS:

```csharp
var clearCacheXmla = string.Format(@"<ClearCache xmlns=""http://schemas.microsoft.com/analysisservices/2003/engine"">  
  <Object>
    <DatabaseID>{0}</DatabaseID>
  </Object>
</ClearCache>", Model.Database.ID);

ExecuteCommand(clearCacheXmla, isXmla: true);
```

### Visualizar los resultados de la consulta

También puede usar el método auxiliar `Output` para visualizar directamente el resultado de una expresión DAX devuelta por `EvaluateDax`:

```csharp
EvaluateDax("1 + 2").Output(); // An integer
EvaluateDax("\"Hello from AS\"").Output(); // A string
EvaluateDax("{ (1, 2, 3) }").Output(); // A table
```

![imagen](https://user-images.githubusercontent.com/8976200/91638299-bbd59580-ea0e-11ea-882b-55bff73c30fb.png)

...o, si desea devolver el valor de la medida seleccionada actualmente:

```csharp
EvaluateDax(Selected.Measure.DaxObjectFullName).Output();
```

![imagen](https://user-images.githubusercontent.com/8976200/91638367-6f3e8a00-ea0f-11ea-90cd-7d2e4cff6e31.png)

Y aquí tiene un ejemplo más avanzado que permite seleccionar y evaluar varias medidas a la vez:

```csharp
var dax = "ROW(" + string.Join(",", Selected.Measures.Select(m => "\"" + m.Name + "\", " + m.DaxObjectFullName).ToArray()) + ")";
EvaluateDax(dax).Output();
```

![imagen](https://user-images.githubusercontent.com/8976200/91638356-546c1580-ea0f-11ea-8302-3e40829e00dd.png)

Si ya está en un nivel avanzado, puede usar SUMMARIZECOLUMNS u otra función DAX para visualizar la medida seleccionada desglosada por alguna columna:

```csharp
var dax = "SUMMARIZECOLUMNS('Product'[Color], " + string.Join(",", Selected.Measures.Select(m => "\"" + m.Name + "\", " + m.DaxObjectFullName).ToArray()) + ")";
EvaluateDax(dax).Output();
```

![imagen](https://user-images.githubusercontent.com/8976200/91638389-9b5a0b00-ea0f-11ea-819f-d3eee3ddfa71.png)

Recuerde que puede guardar estos scripts como Acciones personalizadas haciendo clic en el icono "+" justo encima del editor de scripts. De este modo, obtienes una colección de consultas DAX fácilmente reutilizable que puedes ejecutar y visualizar directamente desde el menú contextual de Tabular Editor:

![imagen](https://user-images.githubusercontent.com/8976200/91638790-305e0380-ea12-11ea-9d84-313f4388496f.png)

### Exportación de datos

Puedes usar el siguiente script para evaluar una consulta DAX y volcar los resultados a un archivo (el script usa un formato de archivo separado por tabulaciones):

```csharp
using System.IO;

// Este script evalúa una consulta DAX y escribe los resultados en un archivo usando un formato separado por tabulaciones:

var dax = "EVALUATE 'Customer'";
var file = @"c:\temp\file.csv";
var columnSeparator = "\t";

using(var daxReader = ExecuteReader(dax))
using(var fileWriter = new StreamWriter(file))
{
    // Escribir encabezados de columna:
    fileWriter.WriteLine(string.Join(columnSeparator, Enumerable.Range(0, daxReader.FieldCount - 1).Select(f => daxReader.GetName(f))));

    while(daxReader.Read())
    {
        var rowValues = new object[daxReader.FieldCount];
        daxReader.GetValues(rowValues);
        var row = string.Join(columnSeparator, rowValues.Select(v => v == null ? "" : v.ToString()));
        fileWriter.WriteLine(row);
    }
}
```

Si se te ocurren otros usos interesantes de estos métodos, plantéate compartirlos en el [repositorio de scripts de la comunidad](https://github.com/TabularEditor/Scripts). ¡Gracias!

***

## Sustituir los nombres del servidor y la base de datos de Power Query

Los Dataset de Power BI que importan datos desde orígenes de datos basados en SQL Server a menudo contienen expresiones M como las siguientes. Por desgracia, Tabular Editor no dispone de ningún mecanismo para "analizar" este tipo de expresión, pero si quisiéramos sustituir los nombres del servidor y la base de datos de esta expresión por otros, sin conocer los valores originales, podemos aprovechar que los valores están entre comillas dobles:

```M
let
    Source = Sql.Databases("devsql.database.windows.net"),
    AdventureWorksDW2017 = Source{[Name="AdventureWorks"]}[Data],
    dbo_DimProduct = AdventureWorksDW2017{[Schema="dbo",Item="DimProduct"]}[Data]
in
    dbo_DimProduct
```

El siguiente script sustituirá la primera aparición de un valor entre comillas dobles por un nombre de servidor y la segunda aparición de un valor entre comillas dobles por un nombre de base de datos. Ambos valores de sustitución se leen desde variables de entorno:

```csharp
// Este script se usa para sustituir los nombres del servidor y la base de datos en
// todas las particiones de Power Query, por los proporcionados mediante variables
// de entorno:
var server = "\"" + Environment.GetEnvironmentVariable("SQLServerName") + "\"";
var database = "\"" + Environment.GetEnvironmentVariable("SQLDatabaseName") + "\"";

// Esta función extraerá todos los valores entre comillas de la expresión M y devolverá una lista de cadenas
// con los valores extraídos (en orden), ignorando cualquier valor entre comillas cuando una almohadilla (#)
// preceda a la comilla:
var split = new Func<string, List<string>>(m => { 
    var result = new List<string>();
    var i = 0;
    foreach(var s in m.Split('"')) {
        if(s.EndsWith("#") && i % 2 == 0) i = -2;
        if(i >= 0 && i % 2 == 1) result.Add(s);
        i++;
    }
    return result;
});
var GetServer = new Func<string, string>(m => split(m)[0]);    // El nombre del servidor suele ser la primera cadena encontrada
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // El nombre de la base de datos suele ser la segunda cadena encontrada

// Recorre todas las particiones del modelo y sustituye los nombres del servidor y de la base de datos de las particiones
// por los especificados en las variables de entorno:
foreach(var p in Model.AllPartitions.OfType<MPartition>())
{
    if (p.Expression.Contains("Source = Sql.Database"))
        {
            var oldServer = "\"" + GetServer(p.Expression) + "\"";
            var oldDatabase = "\"" + GetDatabase(p.Expression) + "\"";
            p.Expression = p.Expression.Replace(oldServer, server).Replace(oldDatabase, database);
       }
}
```

***

## Reemplazar los Data source y las particiones de Power Query por Legacy

Si trabajas con un modelo basado en Power BI que utiliza expresiones de Power Query (M) para particiones contra un Data source basado en SQL Server, por desgracia no podrás usar el asistente Data Import de Tabular Editor 2 ni realizar una comprobación de esquema (es decir, comparar las columnas importadas con las columnas del Data source).

Para resolver este problema, puedes ejecutar el siguiente script en tu modelo para sustituir las particiones de Power Query por las correspondientes particiones de consultas SQL nativas y crear un Data source legacy (proveedor) en el modelo, que funcionará con el asistente Data Import de Tabular Editor 2:

Hay dos versiones del script: la primera usa el proveedor MSOLEDBSQL para el Data source legacy creado y credenciales codificadas de forma fija. Esto es útil para el desarrollo local. La segunda usa el proveedor SQLNCLI, que está disponible en los agentes de compilación hospedados por Microsoft en Azure DevOps, y lee las credenciales y los nombres del servidor y la base de datos desde variables de entorno, lo que hace que el script sea útil para integrarlo en Azure Pipelines.

Versión MSOLEDBSQL, que lee la información de conexión de las particiones M y solicita el nombre de usuario y la contraseña mediante Azure AD:

```csharp
#r "Microsoft.VisualBasic"

// Este script sustituye todas las particiones de Power Query de este modelo por una
// partición legacy usando la cadena de conexión proporcionada con autenticación
// AAD INTERACTIVE. El script asume que todas las particiones de Power Query
// cargan datos desde el mismo origen de datos basado en SQL Server.

// Proporciona la siguiente información:
var authMode = "ActiveDirectoryInteractive";
var userId = Microsoft.VisualBasic.Interaction.InputBox("Escribe tu nombre de usuario de AAD", "Nombre de usuario", "name@domain.com", 0, 0);
if(userId == "") return;
var password = ""; // Déjalo en blanco cuando uses la autenticación ActiveDirectoryInteractive

// Esta función extraerá todos los valores entre comillas de la expresión M y devolverá una lista de cadenas
// con los valores extraídos (en orden), ignorando cualquier valor entre comillas cuando una almohadilla (#) preceda
// a la comilla:
var split = new Func<string, List<string>>(m => { 
    var result = new List<string>();
    var i = 0;
    foreach(var s in m.Split('"')) {
        if(s.EndsWith("#") && i % 2 == 0) i = -2;
        if(i >= 0 && i % 2 == 1) result.Add(s);
        i++;
    }
    return result;
});
var GetServer = new Func<string, string>(m => split(m)[0]);    // El nombre del servidor suele ser la primera cadena encontrada
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // El nombre de la base de datos suele ser la segunda cadena encontrada
var GetSchema = new Func<string, string>(m => split(m)[2]);    // El nombre del esquema suele ser la tercera cadena encontrada
var GetTable = new Func<string, string>(m => split(m)[3]);     // El nombre de la tabla suele ser la cuarta cadena encontrada

var server = GetServer(Model.AllPartitions.OfType<MPartition>().First().Expression);
var database = GetDatabase(Model.AllPartitions.OfType<MPartition>().First().Expression);

// Agrega un origen de datos legacy al modelo:
var ds = Model.AddDataSource("AzureSQL");
ds.Provider = "System.Data.OleDb";
ds.ConnectionString = string.Format(
    "Provider=MSOLEDBSQL;Data Source={0};Initial Catalog={1};Authentication={2};User ID={3};Password={4}",
    server,
    database,
    authMode,
    userId,
    password);

// Quita las particiones de Power Query de todas las tablas y las sustituye por una única partición legacy:
foreach(var t in Model.Tables.Where(t => t.Partitions.OfType<MPartition>().Any()))
{
    var mPartitions = t.Partitions.OfType<MPartition>();
    if(!mPartitions.Any()) continue;
    var schema = GetSchema(mPartitions.First().Expression);
    var table = GetTable(mPartitions.First().Expression);
    t.AddPartition(t.Name, string.Format("SELECT * FROM [{0}].[{1}]", schema, table));
    foreach(var p in mPartitions.ToList()) p.Delete();
}
```

Versión SQLNCLI que lee la información de conexión desde variables de entorno:

```csharp
// Este script sustituye todas las particiones de Power Query de este modelo por una
// partición legacy, leyendo el nombre del servidor SQL, el nombre de la base de datos, el nombre de usuario
// y la contraseña desde las variables de entorno correspondientes. El script asume
// que todas las particiones de Power Query cargan datos desde el mismo origen de datos basado en SQL Server.

var server = Environment.GetEnvironmentVariable("SQLServerName");
var database = Environment.GetEnvironmentVariable("SQLDatabaseName");
var userId = Environment.GetEnvironmentVariable("SQLUserName");
var password = Environment.GetEnvironmentVariable("SQLUserPassword");

// Esta función extraerá todos los valores entre comillas de la expresión M y devolverá una lista de cadenas
// con los valores extraídos (en orden), ignorando cualquier valor entre comillas cuando una almohadilla (#) preceda
// a la comilla:
var split = new Func<string, List<string>>(m => { 
    var result = new List<string>();
    var i = 0;
    foreach(var s in m.Split('"')) {
        if(s.EndsWith("#") && i % 2 == 0) i = -2;
        if(i >= 0 && i % 2 == 1) result.Add(s);
        i++;
    }
    return result;
});
var GetServer = new Func<string, string>(m => split(m)[0]);    // El nombre del servidor suele ser la primera cadena encontrada
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // El nombre de la base de datos suele ser la segunda cadena encontrada
var GetSchema = new Func<string, string>(m => split(m)[2]);    // El nombre del esquema suele ser la tercera cadena encontrada
var GetTable = new Func<string, string>(m => split(m)[3]);     // El nombre de la tabla suele ser la cuarta cadena encontrada

// Agrega un origen de datos legacy al modelo:
var ds = Model.AddDataSource("AzureSQL");
ds.Provider = "System.Data.SqlClient";
ds.ConnectionString = string.Format(
    "Server={0};Initial Catalog={1};Persist Security Info=False;User ID={2};Password={3}",
    server,
    database,
    userId,
    password);

// Quita las particiones de Power Query de todas las tablas y las sustituye por una única partición legacy:
foreach(var t in Model.Tables.Where(t => t.Partitions.OfType<MPartition>().Any()))
{
    var mPartitions = t.Partitions.OfType<MPartition>();
    if(!mPartitions.Any()) continue;
    var schema = GetSchema(mPartitions.First().Expression);
    var table = GetTable(mPartitions.First().Expression);
    t.AddPartition(t.Name, string.Format("SELECT * FROM [{0}].[{1}]", schema, table));
    foreach(var p in mPartitions.ToList()) p.Delete();
}
```
