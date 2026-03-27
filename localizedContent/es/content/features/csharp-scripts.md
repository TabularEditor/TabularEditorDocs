---
uid: csharp-scripts
title: C# Scripts
author: Daniel Otykier
updated: 2026-03-19
applies_to:
  products:
    - product: Tabular Editor 2
      true: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# C# Scripts

Esta es una introducción a las capacidades de C# Scripts de Tabular Editor 3. La información de este documento está sujeta a cambios. Además, no dejes de consultar nuestra biblioteca de scripts @csharp-script-library para ver más ejemplos reales de lo que puedes hacer con las capacidades de scripting de Tabular Editor.

## ¿Por qué scripting en C#?

El objetivo de la interfaz de usuario de Tabular Editor es facilitar la realización de la mayoría de las tareas habituales al crear modelos tabulares. Por ejemplo, cambiar la carpeta de visualización de varias medidas a la vez es tan simple como seleccionar los objetos en el árbol del explorador y arrastrar y soltar. El menú contextual del árbol del explorador, al hacer clic con el botón derecho, ofrece una forma práctica de realizar muchas de estas tareas, como agregar o quitar objetos de perspectivas, cambiar el nombre de varios objetos, etc.

Sin embargo, puede haber muchas otras tareas habituales del flujo de trabajo que no se realizan tan fácilmente desde la interfaz de usuario. Por este motivo, Tabular Editor ofrece scripting en C#, que permite a los usuarios avanzados escribir un script con sintaxis de C# para manipular de forma más directa los objetos del modelo tabular cargado.

## Code Assist

El editor de C# Scripts admite autocompletado y sugerencias de llamada basados en Roslyn y, desde Tabular Editor 3.23.0, el autocompletado admite la coincidencia por subcadenas y por acrónimos de letras mayúsculas.

## Objetos

La [API de scripting](xref:api-index) proporciona acceso a dos objetos de nivel superior, `Model` y `Selected`. El primero contiene métodos y propiedades que te permiten manipular todos los objetos del Modelo tabular, mientras que el segundo expone únicamente los objetos que están seleccionados actualmente en el árbol del explorador.

El objeto `Model` es un contenedor de la clase [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) y expone un subconjunto de sus propiedades, con algunos métodos y propiedades adicionales para facilitar las operaciones con traducciones, perspectivas y colecciones de objetos. Lo mismo se aplica a cualquier objeto descendiente, como Tabla, medida, Columna, etc., ya que todos tienen su correspondiente objeto envoltorio. Consulta <xref:api-index> para ver un listado completo de objetos, propiedades y métodos de la biblioteca de envoltorios de Tabular Editor.

La principal ventaja de trabajar a través de este envoltorio es que todos los cambios se podrán deshacer desde la interfaz de usuario de Tabular Editor. Simplemente pulsa CTRL+Z después de ejecutar un script y verás que todos los cambios realizados por el script se deshacen inmediatamente. Además, el envoltorio proporciona métodos prácticos que convierten muchas tareas habituales en simples líneas de código. A continuación, mostraremos algunos ejemplos. Se da por hecho que el lector ya está algo familiarizado con C# y LINQ, ya que aquí no se tratarán estos aspectos de las capacidades de scripting de Tabular Editor. Los usuarios que no estén familiarizados con C# y LINQ aún deberían poder seguir los ejemplos que se muestran a continuación.

## Establecer propiedades de objetos

Si quieres cambiar una propiedad de un objeto en concreto, obviamente la forma más sencilla de hacerlo es directamente desde la interfaz de usuario. Pero, a modo de ejemplo, veamos cómo podríamos lograr lo mismo mediante un script.

Supongamos que quieres cambiar la cadena de formato de tu medida [Sales Amount] en la tabla 'FactInternetSales'. Si localizas la medida en el árbol del explorador, puedes simplemente arrastrarla al editor de scripts. A continuación, Tabular Editor generará el siguiente código, que representa esa medida concreta en el Tabular Object Model:

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"]
```

Añadir un punto (.) adicional después del corchete situado más a la derecha, debería hacer que aparezca el menú de autocompletado, mostrándote qué propiedades y métodos existen en esa medida en concreto. Solo tienes que elegir "FormatString" en el menú, o escribir las primeras letras y pulsar Tab. Luego, escribe un signo igual seguido de "0.0%" (0,0%). Cambiemos también la carpeta de visualización de esta medida. El código final debería verse así:

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"].FormatString = "0.0%";
Model.Tables["FactInternetSales"].Measures["Sales Amount"].DisplayFolder = "New Folder";
```

**Nota:** Recuerda poner el punto y coma (;) al final de cada línea. Esto es un requisito de C#. Si lo olvidas, recibirás un mensaje de error de sintaxis al intentar ejecutar el script.

Pulsa F5 o el botón "Play" en la parte superior del editor de scripts para ejecutar el script. Inmediatamente deberías ver que la medida se desplaza por el árbol del explorador, reflejando el cambio en la carpeta de visualización. Si examinas la medida en la cuadrícula de propiedades, también verás que la propiedad Format String ha cambiado en consecuencia.

### Trabajar con varios objetos a la vez

Muchos objetos del modelo de objetos son, en realidad, colecciones de varios objetos. Por ejemplo, cada objeto Table tiene una colección de medidas. El wrapper expone una serie de propiedades y métodos prácticos en estas colecciones, lo que facilita establecer la misma propiedad en varios objetos a la vez. Esto se describe en detalle a continuación. Además, puedes usar todos los métodos de extensión estándar de LINQ para filtrar y explorar los objetos de una colección.

A continuación hay unos pocos ejemplos de los métodos de extensión LINQ más utilizados:

- `Collection.First([predicate])` Devuelve el primer objeto de la colección que cumple la condición opcional [predicate].
- `Collection.Any([predicate])` Devuelve `true` si la colección contiene algún objeto (opcionalmente, que cumpla la condición [predicate]).
- `Collection.Where(predicate)` Devuelve una colección que corresponde a la colección original filtrada según la condición del predicado.
- `Collection.Select(map)` Proyecta cada objeto de la colección en otro objeto según el mapeo especificado.
- `Collection.ForEach(action)` Ejecuta la acción especificada en cada elemento de la colección.

En los ejemplos anteriores, `predicate` es una expresión lambda que toma un único objeto como entrada y devuelve un valor booleano como salida. Por ejemplo, si `Collection` es una colección de medidas, un `predicate` típico podría ser:

`m => m.Name.Contains("Reseller")`

Este predicado devolvería true solo si el Nombre de la medida contiene la cadena de caracteres "Reseller". Envuelve la expresión entre llaves y usa la palabra clave `return` si necesitas una lógica más avanzada:

```csharp
.Where(obj => {
    if(obj is Column) {
        return false;
    }
    return obj.Name.Contains("test");
})
```

Volviendo a los ejemplos anteriores, `map` es una expresión lambda que toma un único objeto como entrada y devuelve un único objeto como salida. `action` es una expresión lambda que toma un único objeto como entrada, pero no devuelve ningún valor.

## Trabajar con el objeto **Model**

Para hacer referencia rápidamente a cualquier objeto en el modelo tabular cargado actualmente, se puede arrastrar y soltar el objeto desde el árbol del explorador al editor de C# Script:

![Arrastrando y soltando un objeto en el editor de scripts de C#](~/content/assets/images/drag-object-to-script.gif)

Consulta la [documentación de TOM](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) para obtener una visión general de las propiedades disponibles en el Modelo y en sus objetos descendientes. Además, consulta <xref:api-index> para obtener un listado completo de las propiedades y los métodos expuestos por el objeto envoltorio.

## Trabajando con el objeto **Selected**

Poder hacer referencia de forma explícita a cualquier objeto del Modelo tabular viene muy bien para algunos flujos de trabajo, pero a veces quieres elegir objetos concretos del árbol del explorador y luego ejecutar un script solo sobre los objetos seleccionados. Aquí es donde el objeto `Selected` resulta útil.

El objeto `Selected` ofrece una serie de propiedades que facilitan identificar qué hay seleccionado en este momento, además de limitar la selección a objetos de un tipo concreto. Al explorar con carpetas de visualización, si se seleccionan una o varias carpetas en el árbol del explorador, todos sus elementos secundarios también se consideran seleccionados.
Para selecciones únicas, usa el nombre en singular del tipo de objeto al que quieres acceder. Por ejemplo,

`Selected.Hierarchy`

hace referencia a la jerarquía seleccionada actualmente en el árbol, siempre que se haya seleccionado una y solo una jerarquía. Usa el nombre del tipo en plural si quieres trabajar con selecciones múltiples:

`Selected.Hierarchies`

Todas las propiedades que existen en el objeto en singular también existen en su forma plural, con algunas excepciones. Esto significa que puedes establecer el valor de estas propiedades para varios objetos a la vez, con una sola línea de código y sin usar los métodos de extensión LINQ mencionados anteriormente. Por ejemplo, imagina que quieres mover todas las medidas seleccionadas actualmente a una nueva carpeta de visualización llamada "Test":

`Selected.Measures.DisplayFolder = "Test";`

Si no hay medidas seleccionadas actualmente en el árbol, el código anterior no hace nada y no se genera ningún error. De lo contrario, la propiedad DisplayFolder se establecerá en "Test" en todas las medidas seleccionadas (incluso en las medidas que se encuentren dentro de carpetas, ya que el objeto `Selected` también incluye los objetos de las carpetas seleccionadas). Si usas la forma singular `Measure` en lugar de `Measures`, obtendrás un error a menos que la selección actual contenga exactamente una medida.

Aunque no podemos establecer la propiedad `Name` de varios objetos a la vez, seguimos teniendo algunas opciones disponibles. Si solo queremos reemplazar todas las apariciones de una cadena de caracteres por otra, podemos usar el método "Rename" incluido, así:

```csharp
Selected.Measures
        .Rename("Amount", "Value");
```

Esto reemplazaría cualquier aparición de la palabra "Amount" por la palabra "Value" en los nombres de todas las medidas seleccionadas actualmente.
Como alternativa, podemos usar el método LINQ ForEach(), tal como se describió antes, para incluir lógica más avanzada:

```csharp
Selected.Measures
        .ForEach(m => if(m.Name.Contains("Reseller")) m.Name += " DEPRECATED");
```

Este ejemplo añadirá el texto " DEPRECATED" al final de los nombres de todas las medidas seleccionadas que contengan la palabra "Reseller". Como alternativa, podríamos usar el método de extensión LINQ `Where()` para filtrar la colección antes de aplicar la operación `ForEach()`, lo que daría exactamente el mismo resultado:

```csharp
Selected.Measures
        .Where(m => m.Name.Contains("Reseller"))
        .ForEach(m => m.Name += " DEPRECATED");
```

### Lista completa de los accesores de `Selected`

La siguiente tabla enumera todos los accesores singulares y plurales disponibles en el objeto `Selected`. Los accesores singulares lanzan una `SelectionException` si la selección actual no contiene exactamente un objeto de ese tipo. Los accesores plurales devuelven una colección vacía si no se selecciona ningún objeto de ese tipo.

| Singular                              | Plural                               | Tipo de objeto                     |
| ------------------------------------- | ------------------------------------ | ---------------------------------- |
| `Selected.Medida`                     | `Selected.Measures`                  | Medidas                            |
| `Selected.Column`                     | `Selected.Columns`                   | Todos los tipos de columna         |
| `Selected.DataColumn`                 | `Selected.DataColumns`               | Columnas de datos                  |
| `Selected.CalculatedColumn`           | `Selected.CalculatedColumns`         | Columnas calculadas                |
| `Selected.CalculatedTableColumn`      | `Selected.CalculatedTableColumns`    | Columnas de tablas calculadas      |
| `Selected.Hierarchy`                  | `Selected.Hierarchies`               | Jerarquías                         |
| `Selected.Level`                      | `Selected.Levels`                    | Niveles de jerarquía               |
| `Selected.Table`                      | `Selected.Tables`                    | Tablas                             |
| `Selected.CalculatedTable`            | `Selected.CalculatedTables`          | Tablas calculadas                  |
| `Selected.Partición`                  | `Selected.Particiones`               | Particiones                        |
| `Selected.rol`                        | `Selected.Roles`                     | Roles del modelo                   |
| `Selected.TablePermission`            | `Selected.TablePermissions`          | Permisos de tabla                  |
| `Selected.KPI`                        | `Selected.KPIs`                      | KPI                                |
| `Selected.Calendar`                   | `Selected.Calendars`                 | Calendarios                        |
| `Selected.CalculationItem`            | `Selected.CalculationItems`          | Elementos de cálculo               |
| `Selected.Function`                   | `Selected.Functions`                 | Funciones definidas por el usuario |
| `Selected.DataSource`                 | `Selected.DataSources`               | Fuentes de datos                   |
| `Selected.SingleColumnRelationship`   | `Selected.SingleColumnRelationships` | Relaciones                         |
| `Perspectiva seleccionada`            | `Selected.Perspectives`              | Perspectivas                       |
| `Configuración regional seleccionada` | `Selected.Cultures`                  | Traducciones                       |

> [!NOTE]
> Los accesores de Rol, KPI, Calendar, CalculationItem, TablePermission, Function, DataSource, SingleColumnRelationship, CalculatedColumn, CalculatedTableColumn, DataColumn, CalculatedTable y Partición se agregaron en Tabular Editor 3.26.0.

## Métodos auxiliares

Tabular Editor proporciona un conjunto de métodos auxiliares especiales para facilitar la realización de determinadas tareas de scripting. Ten en cuenta que algunos de ellos pueden invocarse como métodos de extensión. Por ejemplo, `object.Output();` y `Output(object);` son equivalentes.

- `void Output(object value)` - detiene la ejecución del script y muestra información sobre el objeto proporcionado. Cuando el script se ejecuta como parte de una ejecución desde la línea de comandos, se escribirá en la consola una representación en cadena del objeto.
- `void SaveFile(string filePath, string content)` - forma práctica de guardar datos de texto en un archivo.
- `string ReadFile(string filePath)` - forma práctica de cargar datos de texto desde un archivo.
- `string ExportProperties(IEnumerable<ITabularNamedObject> objects, string properties)` - forma práctica de exportar un conjunto de propiedades de varios objetos como una cadena TSV.
- `void ImportProperties(string tsvData)` - forma práctica de cargar propiedades en varios objetos desde una cadena TSV.
- `void CustomAction(string name)` - invoca una macro por su nombre.
- `void CustomAction(this IEnumerable<ITabularNamedObject> objects, string name)` - invoca una macro en los objetos especificados.
- `string ConvertDax(string dax, bool useSemicolons)` - convierte una expresión DAX entre configuraciones regionales de EE. UU./Reino Unido y configuraciones regionales distintas de EE. UU./Reino Unido. Si `useSemicolons` es true (valor predeterminado), la cadena `dax` se convierte del formato nativo de EE. UU./Reino Unido al formato no EE. Es decir, las comas (separadores de lista) se convertirán en punto y coma, y los puntos (separadores decimales) se convertirán en comas. Y viceversa si `useSemicolons` se establece en false.
- `void FormatDax(this IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - da formato a las expresiones DAX en todos los objetos de la colección proporcionada
- `void FormatDax(this IDaxDependantObject obj)` - pone un objeto en cola para dar formato a la expresión DAX cuando finalice la ejecución del script, o cuando se llame al método `CallDaxFormatter`.
- `void CallDaxFormatter(bool shortFormat, bool? skipSpace)` - da formato a todas las expresiones DAX de los objetos puestos en cola hasta el momento
- `void Info(string)` - Escribe un mensaje informativo en la consola (solo cuando el script se ejecuta como parte de una ejecución en la línea de comandos).
- `void Warning(string)` - Escribe un mensaje de advertencia en la consola (solo cuando el script se ejecuta como parte de una ejecución en la línea de comandos).
- `void Error(string)` - Escribe un mensaje de error en la consola (solo cuando el script se ejecuta como parte de una ejecución en la línea de comandos).
- `T SelectObject(this IEnumerable<T> objects, T preselect = null, string label = "Select object") where T: TabularNamedObject` - Muestra un cuadro de diálogo para que el usuario seleccione uno de los objetos especificados. Si el usuario cancela el cuadro de diálogo, este método devuelve `null`.
- `void CollectVertiPaqAnalyzerStats()` - Si Tabular Editor está conectado a una instancia de Analysis Services, ejecuta el recopilador de estadísticas del Analizador VertiPaq.
- `long GetCardinality(this Column column)` - Si las estadísticas del Analizador VertiPaq están disponibles para el modelo actual, este método devuelve la cardinalidad de la columna especificada.

Para ver la lista completa de métodos auxiliares disponibles y su sintaxis, consulte @script-helper-methods.

### Depuración de scripts

Como se mencionó anteriormente, puede usar el método `Output(object);` para pausar la ejecución del script y abrir un cuadro de diálogo con información sobre el objeto que se ha pasado. También puede usar este método como método de extensión, invocándolo como `object.Output();`. El script se reanuda cuando se cierra el cuadro de diálogo.

El cuadro de diálogo aparecerá de una de estas cuatro maneras, según el tipo de objeto que se esté enviando a la salida:

- Los objetos singulares (como strings, ints y DateTimes, excepto cualquier objeto que derive de TabularNamedObject) se mostrarán como un cuadro de diálogo de mensaje simple, invocando el método `.ToString()` sobre el objeto:

![C-sharp Output](~/content/assets/images/c-sharp-script-output-function.png)

- Los TabularNamedObjects singulares (como Tablas, Medidas o cualquier otro TOM NamedMetadataObject disponible en Tabular Editor) se mostrarán en una cuadrícula de propiedades, de forma similar a cuando se ha seleccionado un objeto en el Explorador de árboles. Las propiedades del objeto se pueden editar en la cuadrícula, pero tenga en cuenta que, si se encuentra un error más adelante durante la ejecución del script, la edición se deshará automáticamente si "Auto-Rollback" está habilitado:

![C-sharp Output](~/content/assets/images/c-sharp-script-auto-rollback.png)

- Cualquier IEnumerable de objetos (excepto TabularNamedObjects) se mostrará en una lista, donde cada elemento de la lista muestra el valor `.ToString()` y el tipo del objeto dentro del IEnumerable:

![C-sharp Output](~/content/assets/images/c-sharp-script-output-to-string-function.png)

- Cualquier IEnumerable de TabularNamedObjects hará que el cuadro de diálogo muestre una lista de objetos a la izquierda y una cuadrícula de propiedades a la derecha. La cuadrícula de propiedades se rellenará a partir del objeto seleccionado en la lista, y las propiedades se podrán editar igual que cuando se envía a la salida un único TabularNamedObject:

![C-sharp Output](~/content/assets/images/c-sharp-script-output-function-enumerated.png)

Puede marcar la casilla "No mostrar más salidas" en la esquina inferior izquierda para evitar que el script se detenga en futuras invocaciones de `.Output()`.

## Ejecutar C# Scripts con vista previa

La acción **Ejecutar con vista previa** te permite revisar todos los cambios de metadatos del modelo realizados por un C# Script antes de confirmarlos. Esto resulta útil al ejecutar scripts desconocidos o al realizar modificaciones masivas.

Para usar esta función, haz clic en **Script > Ejecutar con vista previa** en la barra de herramientas o en el menú. El flujo de trabajo es el siguiente:

1. Tabular Editor toma una instantánea de los metadatos del modelo antes de la ejecución
2. El script se ejecuta hasta completarse
3. Tabular Editor compara el estado actual de los metadatos del modelo con la instantánea tomada antes de la ejecución
4. Si se detectan cambios, aparecerá un cuadro de diálogo de vista previa que muestra, lado a lado, una comparación jerárquica de las diferencias del modelo (antes y después)
5. Los cambios se codifican por colores: verde para los objetos agregados, rojo para los eliminados y naranja para las propiedades modificadas
6. Usa la casilla **Mostrar solo cambios** para ocultar los elementos sin cambios y centrarte en lo que modificó el script
7. Haz clic en **OK** para aceptar los cambios, o en **Revert** para deshacer todos los cambios

![Vista previa del script: cambios en el modelo](~/content/assets/images/c-sharp-script-preview-changes.png)

Si el script falla (error de compilación o en tiempo de ejecución), todos los cambios de metadatos del modelo se revierten automáticamente y no se muestra ningún cuadro de diálogo de vista previa. Si el script se ejecuta correctamente pero no realiza ningún cambio detectable en los metadatos, se muestran mensajes informativos en su lugar.

Todos los cambios de metadatos del modelo derivados de la ejecución de un script se agrupan en una única transacción de deshacer. Incluso después de aceptar los cambios en el cuadro de diálogo de vista previa, aún puede deshacer toda la operación con **Ctrl+Z**.

> [!IMPORTANT]
> Las funciones de vista previa y deshacer solo se aplican a los cambios de metadatos del modelo. Si un script realiza operaciones externas, como escribir en archivos, bases de datos o realizar solicitudes web, esas operaciones se ejecutan de inmediato y no se pueden revertir. El cuadro de diálogo de vista previa no intenta analizar el código del script; funciona comparando el estado de los metadatos del modelo antes y después de la ejecución.

> [!TIP]
> El [Asistente de IA](xref:ai-assistant) muestra automáticamente el cuadro de diálogo de vista previa de cambios cuando ejecuta C# Script desde el chat, de modo que siempre puede revisar los cambios del modelo generados por la IA antes de que se apliquen.

## Referencias de .NET

Puede usar la palabra clave `using` para acortar nombres de clases, etc., igual que en el código fuente normal de C#. Además, puede incluir ensamblados externos utilizando la sintaxis `#r "<assembly name or DLL path>"`, similar a los scripts .csx usados en Azure Functions.

Por ejemplo, el siguiente script ahora funcionará como se espera:

```csharp
// Las referencias de ensamblados deben estar al principio del archivo:
#r "System.IO.Compression"

// Las palabras clave using deben ir antes que cualquier otra instrucción:
using System.IO.Compression;
using System.IO;

var xyz = 123;

// Las instrucciones using siguen funcionando como deben:
using(var data = new MemoryStream())
using(var zip = new ZipArchive(data, ZipArchiveMode.Create)) 
{
   // ...
}
```

De forma predeterminada, Tabular Editor aplica las siguientes directivas `using` (aunque no se especifiquen en el script) para facilitar las tareas habituales:

```csharp
using System;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json;
using TabularEditor.TOMWrapper;
using TabularEditor.TOMWrapper.Utils;
using TabularEditor.UI;
```

Además, los siguientes ensamblados de .NET Framework se cargan de forma predeterminada:

- System.Dll
- System.Core.Dll
- System.Data.Dll
- System.Windows.Forms.Dll
- Microsoft.Csharp.Dll
- Newtonsoft.Json.Dll
- TomWrapper.Dll
- TabularEditor.Exe
- Microsoft.AnalysisServices.Tabular.Dll

<a name="accessing-environment-variables"></a>

## Acceso a variables de entorno

Al ejecutar scripts de C# mediante la CLI de Tabular Editor (especialmente en canalizaciones de CI/CD), puedes pasar parámetros a tus scripts usando variables de entorno. Este es el enfoque recomendado, ya que los C# Scripts ejecutados por Tabular Editor CLI no admiten argumentos tradicionales de línea de comandos.

### Lectura de variables de entorno

Usa el método `Environment.GetEnvironmentVariable()` para leer variables de entorno en tu script:

```csharp
// Read environment variables
var serverName = Environment.GetEnvironmentVariable("SERVER_NAME");
var environment = Environment.GetEnvironmentVariable("ENVIRONMENT");

// Use them in your script
foreach(var dataSource in Model.DataSources.OfType<ProviderDataSource>())
{
    if(dataSource.Name == "SQLDW")
    {
        dataSource.ConnectionString = dataSource.ConnectionString
            .Replace("{SERVER}", serverName)
            .Replace("{ENV}", environment);
    }
}

Info($"Updated connection strings for {environment} environment");
```

### Integración con Azure DevOps

Las variables de entorno se integran sin problemas con las canalizaciones de Azure DevOps, ya que todas las variables de canalización están disponibles automáticamente como variables de entorno de forma predeterminada.

**Ejemplo de canalización YAML de Azure DevOps:**

```yaml
variables:
  targetServer: 'Production'
  targetDatabase: 'AdventureWorks'

steps:
- task: PowerShell@2
  displayName: 'Deploy Model with Parameters'
  env:
    SERVER_NAME: $(targetServer)
    DATABASE_NAME: $(targetDatabase)
  inputs:
    targetType: 'inline'
    script: |
      TabularEditor.exe "Model.bim" -S "DeploymentScript.csx" -D "$(targetServer)" "$(targetDatabase)" -O -V -E -W
```

En este ejemplo, el script `DeploymentScript.csx` puede acceder a `SERVER_NAME` y `DATABASE_NAME` mediante `Environment.GetEnvironmentVariable()`.

### Casos de uso comunes

Las variables de entorno son especialmente útiles para:

- **Cadenas de conexión dinámicas**: Actualiza las conexiones a los orígenes de datos según el entorno de implementación (Dev, UAT, Producción)
- **Lógica condicional**: Aplica transformaciones distintas según el entorno de destino
- **Configuración de implementación**: Controla qué objetos se implementan o se modifican según los parámetros
- **Compatibilidad con varios entornos**: Usa el mismo script en distintos entornos con valores diferentes

**Ejemplo: modificaciones específicas por entorno:**

```csharp
var environment = Environment.GetEnvironmentVariable("DEPLOY_ENV") ?? "Development";
var refreshPolicy = Environment.GetEnvironmentVariable("ENABLE_REFRESH_POLICY") == "true";

// Aplica configuración específica por entorno
foreach(var table in Model.Tables)
{
    if(environment == "Production" && !refreshPolicy)
    {
        // Deshabilita las políticas de actualización incremental en producción si se especifica
        table.EnableRefreshPolicy = false;
    }
}

Info($"Modelo configurado para el entorno {environment}");
```

<a name="compatibility"></a>

## Compatibilidad

Las API de scripting de Tabular Editor 2 y Tabular Editor 3 son en gran medida compatibles. Sin embargo, en algunos casos conviene compilar el código condicionalmente en función de la versión que estés usando. Para ello, puedes usar directivas de preprocesador, que se introdujeron en Tabular Editor 3.10.0.

```csharp
#if TE3
    // This code will only be compiled when the script is running in TE3 (version 3.10.0 or newer).
    Info("Hello from TE3!");
#else
    // This code will be compiled in all other cases.
    Info("Hello from TE2!");
#endif
```

Si necesitas conocer la versión exacta de Tabular Editor en tiempo de ejecución del script, puedes inspeccionar la versión del ensamblado:

```csharp
var currentVersion = typeof(Model).Assembly.GetName().Version;
Info(currentVersion.ToString());
```

La versión pública del producto (por ejemplo, "2.20.2" o "3.10.1") se puede obtener con este código:

```csharp
using System.Diagnostics;

var productVersion = FileVersionInfo.GetVersionInfo(Selected.GetType().Assembly.Location).ProductVersion;
productVersion.Output(); // productVersion is a string ("2.20.2" or "3.10.1", for example)
```

Si solo quieres el número de versión principal (como entero), usa:

```csharp
var majorVersion = Selected.GetType().Assembly.GetName().Version.Major;
majorVersion.Output(); // majorVersion is an integer (2 or 3)
```

## Problemas y limitaciones conocidos

- Algunas operaciones en los scripts pueden hacer que la aplicación Tabular Editor 3 se bloquee o deje de responder, debido a la forma en que se ejecutan los scripts. Por ejemplo, un script con un bucle infinito (`while(true) {}`) hará que la aplicación se quede colgada. Si esto ocurre, tendrás que finalizar el proceso de Tabular Editor desde el Administrador de tareas de Windows.

Si tienes pensado guardar el script como una [macro](xref:creating-macros), ten en cuenta las siguientes limitaciones:

- Si el cuerpo del script contiene métodos locales con modificadores de acceso (`public`, `static`, etc.), el script no se puede guardar como una macro. Elimina los modificadores de acceso o, en su lugar, mueve el método a una clase.
- Actualmente, las macros no admiten la palabra clave `await` si se usa en el cuerpo del script. Si el cuerpo del script llama a métodos asíncronos, debes usar `MyAsyncMethod.Wait()` o `MyAsyncMethod.Result` en lugar de `await MyAsyncMethod()`. No hay problema en usar `await` en métodos `async` definidos en otra parte del script.