---
uid: advanced-scripting
title: Scripting avanzado
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Scripting avanzado

Esta es una introducción a las capacidades de scripting avanzado de Tabular Editor. La información de este documento está sujeta a cambios. Además, no dejes de echar un vistazo a nuestra biblioteca de scripts @csharp-script-library para ver más ejemplos reales de lo que puedes hacer con las capacidades de scripting de Tabular Editor.

## ¿Qué es el scripting avanzado?

El objetivo de la interfaz de usuario de Tabular Editor es facilitar la ejecución de la mayoría de las tareas habituales al crear modelos tabulares. Por ejemplo, cambiar la carpeta de visualización de varias medidas a la vez es tan sencillo como seleccionar los objetos en el árbol del explorador y arrastrarlos y soltarlos para reorganizarlos. El menú contextual al hacer clic con el botón derecho del árbol del explorador ofrece una forma práctica de realizar muchas de estas tareas, como agregar o quitar objetos de las perspectivas, cambiar el nombre de varios objetos, etc.

Aun así, hay muchas otras tareas habituales del flujo de trabajo que no se realizan con la misma facilidad desde la interfaz de usuario. Por este motivo, Tabular Editor incorpora el scripting avanzado, que permite a los usuarios avanzados escribir un script con sintaxis de C# para manipular de forma más directa los objetos del modelo tabular cargado.

## Objetos

La [API de scripting](xref:api-index) proporciona acceso a dos objetos de nivel superior: `Model` y `Selected`. El primero contiene métodos y propiedades que te permiten manipular todos los objetos del modelo tabular, mientras que el segundo expone solo los objetos seleccionados actualmente en el árbol del explorador.

El objeto `Model` es un envoltorio de la clase [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx), que expone un subconjunto de sus propiedades, con algunos métodos y propiedades adicionales para facilitar las operaciones con traducciones, perspectivas y colecciones de objetos. Lo mismo se aplica a cualquier objeto derivado, como tabla, medida, columna, etc., que cuentan con su correspondiente objeto envoltorio. Consulta <xref:api-index> para ver una lista completa de objetos, propiedades y métodos de la biblioteca de envoltorios de Tabular Editor.

La principal ventaja de trabajar a través de este envoltorio es que todos los cambios se pueden deshacer desde la interfaz de usuario de Tabular Editor. Basta con pulsar CTRL+Z después de ejecutar un script y verás que todos los cambios realizados por el script se deshacen de inmediato. Además, este envoltorio ofrece métodos prácticos que convierten muchas tareas habituales en sencillas instrucciones de una sola línea. A continuación veremos algunos ejemplos. Damos por hecho que ya tienes cierta familiaridad con C# y LINQ, ya que estos aspectos de las capacidades de scripting de Tabular Editor no se tratarán aquí. Los usuarios que no estén familiarizados con C# y LINQ deberían poder seguir los ejemplos que se muestran a continuación.

## Configurar las propiedades de los objetos

Si quieres cambiar la propiedad de un objeto en concreto, obviamente la forma más sencilla es hacerlo directamente desde la interfaz de usuario. Pero, a modo de ejemplo, veamos cómo podríamos conseguir lo mismo mediante un script.

Supongamos que quieres cambiar la cadena de formato de tu medida [Sales Amount] en la tabla 'FactInternetSales'. Si localizas la medida en el árbol del explorador, puedes arrastrarla directamente al editor de scripts. Tabular Editor generará entonces el siguiente código, que representa esta medida concreta en el Tabular Object Model:

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"]
```

Añadir un punto (.) adicional después del corchete situado más a la derecha, debería aparecer el menú de autocompletado, mostrándote qué propiedades y métodos existen en esta medida concreta. Simplemente elige "FormatString" en el menú, o escribe las primeras letras y pulsa Tab. Luego, escribe un signo igual seguido de "0.0%". Cambiemos también la carpeta de visualización de esta medida. El código final debería quedar así:

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"].FormatString = "0.0%";
Model.Tables["FactInternetSales"].Measures["Sales Amount"].DisplayFolder = "New Folder";
```

**Nota:** Recuerda poner el punto y coma (;) al final de cada línea. Es un requisito de C#. Si lo olvidas, recibirás un mensaje de error de sintaxis al intentar ejecutar el script.

Pulsa F5 o el botón "Play" situado encima del editor de scripts para ejecutar el script. Al instante, deberías ver cómo la medida se mueve por el árbol del explorador, reflejando el cambio en la carpeta de visualización. Si examinas la medida en la cuadrícula de propiedades, también deberías ver que la propiedad de la cadena de formato ha cambiado en consecuencia.

### Trabajar con varios objetos a la vez

Muchos objetos del modelo de objetos son, en realidad, colecciones de varios objetos. Por ejemplo, cada objeto Table tiene una colección de medidas llamada "Measures". El wrapper expone una serie de propiedades y métodos prácticos de estas colecciones, lo que facilita establecer la misma propiedad en varios objetos a la vez. Esto se describe en detalle más abajo. Además, puedes usar todos los métodos de extensión estándar de LINQ para filtrar y recorrer los objetos de una colección.

A continuación se muestran algunos ejemplos de los métodos de extensión de LINQ más usados:

- `Collection.First([predicate])` Devuelve el primer objeto de la colección que cumpla la condición opcional [predicate].
- `Collection.Any([predicate])` Devuelve `true` si la colección contiene algún objeto (opcionalmente, que cumpla la condición [predicate]).
- `Collection.Where(predicate)` Devuelve una colección que corresponde a la colección original filtrada por la condición del predicado.
- `Collection.Select(map)` Proyecta cada objeto de la colección en otro objeto según el `map` especificado.
- `Collection.ForEach(action)` Ejecuta la acción especificada sobre cada elemento de la colección.

En los ejemplos anteriores, `predicate` es una expresión lambda que toma un único objeto como entrada y devuelve un valor booleano como salida. Por ejemplo, si `Collection` es una colección de medidas, un `predicate` típico podría ser:

`m => m.Name.Contains("Reseller")`

Este `predicate` solo devolvería `true` si la propiedad `Name` de la medida contiene la cadena de caracteres "Reseller". Si necesitas una lógica más avanzada, envuelve la expresión entre llaves y usa la palabra clave `return`:

```csharp
.Where(obj => {
    if(obj is Column) {
        return false;
    }
    return obj.Name.Contains("test");
})
```

Volviendo a los ejemplos anteriores, `map` es una expresión lambda que toma un único objeto como entrada y devuelve un único objeto como salida. `action` es una expresión lambda que toma un único objeto como entrada, pero no devuelve ningún valor.

Usa la funcionalidad de IntelliSense del editor de scripts avanzado para ver qué otros métodos de LINQ existen, o consulta la [documentación de LINQ-to-Objects](https://msdn.microsoft.com/en-us/library/9eekhta0.aspx).

## Trabajar con el objeto **Model**

Para hacer referencia rápidamente a cualquier objeto del modelo tabular cargado actualmente, puedes arrastrar y soltar el objeto desde el árbol del explorador hasta el editor de scripts avanzado:

![Arrastrar y soltar un objeto en el editor de scripts avanzado](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/DragDropTOM.gif)

Consulta la [documentación de TOM](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) para ver un resumen de las propiedades disponibles en `Model` y en sus objetos descendientes. Además, consulta <xref:api-index> para ver un listado completo de las propiedades y métodos expuestos por el objeto contenedor.

## Trabajar con el objeto **Selected**

Poder referirte explícitamente a cualquier objeto del Modelo tabular es ideal para algunos flujos de trabajo, pero a veces quieres seleccionar objetos concretos del árbol del explorador y luego ejecutar un script solo sobre los objetos seleccionados. Aquí es donde el objeto `Selected` resulta muy útil.

El objeto `Selected` proporciona una serie de propiedades que facilitan identificar la selección actual, así como limitarla a objetos de un tipo determinado. Al navegar con las carpetas de visualización, si hay una o varias carpetas seleccionadas en el árbol del explorador, todos sus elementos secundarios también se consideran seleccionados.
Para selecciones únicas, usa el nombre en singular del tipo de objeto al que quieres acceder. Por ejemplo,

`Selected.Hierarchy`

hace referencia a la jerarquía seleccionada actualmente en el árbol, siempre que haya seleccionada una única jerarquía. Usa el nombre del tipo en plural si quieres trabajar con selecciones múltiples:

`Selected.Hierarchies`

Todas las propiedades que existen en el objeto singular también existen en su forma plural, con algunas excepciones. Esto significa que puedes establecer el valor de estas propiedades para varios objetos a la vez, con una sola línea de código y sin usar los métodos de extensión LINQ mencionados anteriormente. Por ejemplo, supongamos que quieres mover todas las medidas seleccionadas actualmente a una nueva carpeta de visualización llamada "Test":

`Selected.Measures.DisplayFolder = "Test";`

Si actualmente no hay medidas seleccionadas en el árbol, el código anterior no hace nada y no se produce ningún error. De lo contrario, la propiedad DisplayFolder se establecerá en "Test" para todas las medidas seleccionadas (incluso para las medidas que estén dentro de carpetas, ya que el objeto `Selected` también incluye los objetos de las carpetas seleccionadas). Si usas la forma singular `Measure` en lugar de `Measures`, obtendrás un error, salvo que la selección actual contenga exactamente una medida.

Aunque no se puede establecer la propiedad Name de varios objetos a la vez, aún tienes algunas opciones. Si solo quieres reemplazar todas las apariciones de una cadena de caracteres por otra, puedes usar el método "Rename" incluido, de esta forma:

```csharp
Selected.Measures
        .Rename("Amount", "Value");
```

Esto reemplazaría cualquier aparición de la palabra "Amount" por "Value" en los nombres de todas las medidas seleccionadas actualmente.
Como alternativa, puedes usar el método ForEach() de LINQ, tal y como se describe arriba, para incluir una lógica más avanzada:

```csharp
Selected.Measures
        .ForEach(m => if(m.Name.Contains("Reseller")) m.Name += " DEPRECATED");
```

Este ejemplo añadirá el texto " DEPRECATED" al final de los nombres de todas las medidas seleccionadas cuyos nombres contengan la palabra "Reseller". Como alternativa, puedes usar el método de extensión `Where()` de LINQ para filtrar la colección antes de aplicar la operación `ForEach()`, lo que daría exactamente el mismo resultado:

```csharp
Selected.Measures
        .Where(m => m.Name.Contains("Reseller"))
        .ForEach(m => m.Name += " DEPRECATED");
```

## Métodos auxiliares

Para facilitar la depuración de scripts, Tabular Editor ofrece un conjunto de métodos auxiliares especiales. Internamente, se trata de métodos estáticos decorados con el atributo `[ScriptMethod]`. Este atributo permite que los scripts llamen a los métodos directamente, sin necesidad de especificar un espacio de nombres o un nombre de clase. Los complementos también pueden usar el atributo `[ScriptMethod]` para exponer métodos estáticos públicos para su uso en scripts, de forma similar.

A partir de la versión 2.7.4, Tabular Editor proporciona los siguientes métodos de script. Ten en cuenta que algunos de estos pueden invocarse como métodos de extensión. Por ejemplo, `object.Output();` y `Output(object);` son equivalentes.

- `Output(object);` - muestra información detallada sobre el objeto especificado o la colección de objetos en un cuadro de diálogo emergente. Cuando se ejecuta a través de la interfaz de usuario, el usuario tiene la opción de ignorar los cuadros de diálogo emergentes adicionales. Cuando se ejecuta desde la CLI, la información se envía a la consola.
- `SaveFile(filePath, content);` - forma práctica de guardar datos de texto en un archivo.
- `ReadFile(filePath);` - forma práctica de cargar datos de texto desde un archivo.
- `ExportProperties(objects, properties);` - forma práctica de exportar un conjunto de propiedades de varios objetos como una cadena TSV.
- `ImportProperties(tsvData);` - forma práctica de cargar propiedades en varios objetos a partir de una cadena TSV.
- `CustomAction(name);` - invoca una acción personalizada por su nombre.
- `CustomAction(objects, name);` - invoca una acción personalizada en los objetos especificados.
- `ConvertDax(dax, useSemicolons);` - convierte una expresión DAX entre configuraciones regionales de EE. UU./Reino Unido y otras configuraciones regionales. Si `useSemicolons` es `true` (valor predeterminado), la cadena `dax` se convierte del formato nativo de EE. UU./Reino Unido al formato no EE. UU./Reino Unido. Es decir, las comas (separadores de lista) se convierten en punto y coma, y los puntos (separadores decimales) se convierten en comas. Y viceversa si `useSemicolons` se establece en `false`.
- ¿`FormatDax(IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - da formato a las expresiones DAX de todos los objetos de la colección proporcionada
- `FormatDax(IDaxDependantObject obj)` - pone un objeto en cola para dar formato a la expresión DAX cuando finalice la ejecución del script, o cuando se llame al método `CallDaxFormatter`.
- ¿`CallDaxFormatter(bool shortFormat, bool? skipSpace)` - da formato a todas las expresiones DAX de los objetos puestos en cola hasta el momento
- `Info(string);` - muestra un mensaje informativo en un cuadro de diálogo emergente de mensajes. Cuando el script se ejecuta en la CLI, se escribe un mensaje informativo en la consola.
- `Warning(string);` - Muestra un mensaje de advertencia en un cuadro de diálogo emergente. Cuando el script se ejecuta en la CLI, se escribe un mensaje de advertencia en la consola.
- `Error(string);` - Muestra un mensaje de error en un cuadro de diálogo emergente. Cuando el script se ejecuta en la CLI, se escribe un mensaje de error en la consola.

Puedes encontrar una lista actualizada de todos los métodos auxiliares [aquí](xref:script-helper-methods).

### Depuración de scripts

Como se mencionó anteriormente, puedes usar el método `Output(object);` para pausar la ejecución del script y abrir un cuadro de diálogo con información sobre el objeto pasado como argumento. También puedes usar este método como método de extensión, invocándolo como `object.Output();`. El script se reanuda cuando se cierra el cuadro de diálogo.

El cuadro de diálogo aparecerá de una de estas cuatro formas, según el tipo de objeto que se envíe como salida:

- Los objetos individuales (como string, int y DateTime, excepto cualquier objeto que derive de TabularNamedObject) se mostrarán como un cuadro de diálogo de mensaje sencillo, invocando el método `.ToString()` del objeto:

![image](https://user-images.githubusercontent.com/8976200/29941982-9917d0cc-8e94-11e7-9e78-24aaf11fd311.png)

- Los TabularNamedObjects individuales (como tablas, medidas o cualquier otro NamedMetadataObject de TOM disponible en Tabular Editor) se mostrarán en una cuadrícula de propiedades, similar a cuando se ha seleccionado un objeto en el Tree Explorer. Las propiedades del objeto se pueden editar en la cuadrícula, pero ten en cuenta que, si se produce un error más adelante durante la ejecución del script, la edición se deshará automáticamente si "Rollback on error" está habilitado:

![image](https://user-images.githubusercontent.com/8976200/29941852-2acc9846-8e94-11e7-9380-f84fef26a78c.png)

- Cualquier IEnumerable de objetos (excepto TabularNamedObjects) se mostrará en una lista, donde cada elemento de la lista muestra el valor de `.ToString()` y el tipo del objeto en el IEnumerable:

![image](https://user-images.githubusercontent.com/8976200/29942113-02dad928-8e95-11e7-9c04-5bb87b396f3f.png)

- Cualquier IEnumerable de TabularNamedObjects hará que el cuadro de diálogo muestre una lista de los objetos a la izquierda y una cuadrícula de propiedades a la derecha. La cuadrícula de propiedades se rellenará con el objeto seleccionado en la lista, y las propiedades se pueden editar igual que cuando se envía a la salida un único TabularNamedObject:

![image](https://user-images.githubusercontent.com/8976200/29942190-498cbb5c-8e95-11e7-8455-32750767cf13.png)

Puedes marcar la casilla "Don't show more outputs" en la esquina inferior izquierda para evitar que el script se detenga en futuras invocaciones de `.Output()`.

## Referencias de «.NET»

[Tabular Editor versión 2.8.6](https://github.com/TabularEditor/TabularEditor/tree/2.8.6) facilita mucho la escritura de scripts complejos. Gracias al nuevo preprocesador, ahora puedes usar la palabra clave `using` para acortar nombres de clases, etc., igual que en el código fuente normal de C#. Además, puedes incluir ensamblados externos mediante la sintaxis `#r "<assembly name or DLL path>"`, similar a los scripts .csx que se usan en Azure Functions.

Por ejemplo, el siguiente script ahora funcionará como se espera:

```csharp
// Assembly references must be at the very top of the file:
#r "System.IO.Compression"

// Using keywords must come before any other statements:
using System.IO.Compression;
using System.IO;

var xyz = 123;

// Using statements still work the way they're supposed to:
using(var data = new MemoryStream())
using(var zip = new ZipArchive(data, ZipArchiveMode.Create)) 
{
   // ...
}
```

De forma predeterminada, Tabular Editor incluye automáticamente las siguientes directivas `using` (aunque no estén especificadas en el script) para facilitar las tareas más comunes:

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

## Compilar con Roslyn

Si prefieres compilar tus scripts con el nuevo compilador Roslyn introducido con Visual Studio 2017, puedes configurarlo en File > Preferencias > General a partir de la versión 2.12.2 de Tabular Editor. Esto te permite usar características más recientes del lenguaje C#, como la interpolación de cadenas. Solo tienes que especificar la ruta al directorio que contiene el ejecutable del compilador (`csc.exe`) e indicar la versión del lenguaje como una opción del compilador:

![image](https://user-images.githubusercontent.com/8976200/92464140-0902f580-f1cd-11ea-998a-b6ecce57b399.png)

### Visual Studio 2017

En una instalación típica de Visual Studio 2017 Enterprise, el compilador Roslyn se encuentra aquí:

```
c:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\MSBuild\15.0\Bin\Roslyn
```

Esto incluye las características del lenguaje C# 6.0 de forma predeterminada.

![image](https://user-images.githubusercontent.com/8976200/92464584-a52cfc80-f1cd-11ea-9b66-3b47ac36f6c6.png)

### Visual Studio 2019

Para una instalación típica de Visual Studio 2019 Community, el compilador de Roslyn se encuentra aquí:

```
c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\Roslyn
```

El compilador que se incluye con VS2019 admite las características del lenguaje C# 8,0, que se pueden habilitar especificando lo siguiente como opciones del compilador:

```
-langversion:8.0
```

### Visual Studio 2022

Para una instalación típica de Visual Studio 2022 **Community Edition**, el compilador de Roslyn se encuentra aquí:

```
C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\Roslyn\csc.exe
```

Si usa otra edición de Visual Studio 2022, la ruta puede variar ligeramente. Por ejemplo, para la **Edición Enterprise**, se encuentra en:

```
C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\Roslyn
```

El compilador incluido en la actualización más reciente de VS2022 admite las [características del lenguaje C# 12,0](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-12), que se pueden habilitar indicando las siguientes opciones del compilador:

```
-langversion:12.0
```
