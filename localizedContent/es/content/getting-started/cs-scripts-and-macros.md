---
uid: cs-scripts-and-macros
title: Introducción a los C# Scripts y macros
author: Daniel Otykier
updated: 2021-11-03
---

# Introducción a los C# Scripts y macros

Cualquier software que afirme mejorar tu productividad debería ofrecer algún medio para **automatizar las interacciones del usuario**. En Tabular Editor, puedes escribir C# Scripts precisamente con ese objetivo. Con los C# Scripts en Tabular Editor, por ejemplo, puedes:

- Automatizar la creación de objetos TOM como medidas, tablas y elementos de cálculo
- Interactuar con el/los objeto(s) seleccionados actualmente en el Explorador TOM
- Asignar propiedades automáticamente a varios objetos
- Importar y exportar metadatos en varios formatos, con fines de auditoría o documentación

Si un script modifica los metadatos de tu modelo, podrás ver los cambios de inmediato en el Explorador TOM y en la vista de propiedades. Además, puedes **deshacer los cambios del script**, revirtiendo en la práctica los metadatos del modelo al punto anterior a la ejecución del script. Si falla la ejecución de un script, los cambios se revierten automáticamente de forma predeterminada.

Tabular Editor 3 incluye un **Grabador de scripts** sencillo que te ayuda a aprender la sintaxis, añadiendo líneas de código de script de forma incremental a medida que haces cambios en tu modelo.

Un script se puede guardar como un archivo independiente (con extensión `.csx`), que puedes compartir con otros usuarios de Tabular Editor. Además, un script se puede guardar como una **macro** reutilizable, que integra el script de forma más estrecha con la interfaz de usuario de Tabular Editor.

# Crear un script

Para crear un nuevo script de C#, usa la opción de menú **Archivo > Nuevo > C# Script**. Ten en cuenta que esta opción está disponible incluso cuando no hay ningún modelo cargado en Tabular Editor.

Para tu primer script, escribe el siguiente código:

```csharp
Info("Hello world!");
```

Pulsa F5 para ejecutar el código.

![Tu primer script](~/content/assets/images/first-script.png)

Si cometiste un error al escribir el código, se mostrará cualquier error de sintaxis en la **vista de mensajes**.

- Para guardar el script como archivo, solo pulsa **Archivo > Guardar** (Ctrl+S).
- Para abrir un script desde un archivo, usa la opción **Archivo > Abrir > Archivo...** (Ctrl+O). De forma predeterminada, el cuadro de diálogo "Abrir archivo" buscará archivos con las extensiones `.cs` o `.csx`.

# Uso del Grabador de scripts

Mientras el foco esté en un script de C#, puedes iniciar el Grabador de scripts en Tabular Editor mediante la opción de menú **C# Script > Record script**. Mientras se graba el script, cualquier cambio que hagas en los metadatos del modelo hará que se agreguen líneas de código adicionales al script. Ten en cuenta que no puedes editar el script manualmente hasta que detengas la grabación.

![Grabador de scripts de C#](~/content/assets/images/csharp-script-recorder.png)

# Acceso a los metadatos del modelo

Para acceder a objetos específicos del modelo cargado actualmente, debes usar la sintaxis de C# para navegar por la jerarquía del Tabular Object Model (TOM). La raíz de esta jerarquía es el objeto `Model`.

El siguiente script muestra el nombre del modelo cargado actualmente. Si no hay ningún modelo cargado, se muestra una advertencia.

```csharp
if(Model != null)
    Info("El nombre del modelo actual es: " + Model.Name);
else
    Warning("No hay ningún modelo cargado actualmente!");
```

El objeto `Model` es un contenedor de la clase [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx), que expone un subconjunto de sus propiedades, con algunos métodos y propiedades adicionales para mayor comodidad.

Para acceder a una medida específica, necesitarás conocer el nombre de esa medida y el nombre de la tabla en la que se encuentra:

```csharp
var myMeasure = Model.Tables["Internet Sales"].Measures["Internet Total Sales"];
myMeasure.Description = "La fórmula de esta medida es: " + myMeasure.Expression;
```

La línea 1 del script anterior localiza la medida "Internet Total Sales" en la tabla "Internet Sales" y, a continuación, guarda una referencia a esa medida en la variable `myMeasure`.

La línea 2 del script establece la descripción de la medida a partir de una cadena literal y de la expresión (DAX) de la medida.

En Tabular Editor, puedes generar automáticamente el código que hace referencia a un objeto específico arrastrándolo y soltándolo desde el Explorador TOM a la vista de C# Script.

![Generate an object reference by dragging](~/content/assets/images/generate-csharp-code.gif)

La mayoría de los objetos TOM (tablas, columnas, medidas, etc.) en Tabular Editor exponen el mismo conjunto de propiedades que están disponibles al usar directamente las bibliotecas de cliente AMO/TOM. Por este motivo, puedes consultar la [documentación de AMO/TOM de Microsoft](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet) para saber qué propiedades están disponibles. Por ejemplo, [aquí](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure?view=analysisservices-dotnet#properties) está la documentación sobre las propiedades disponibles de una medida.

# Acceder a la selección actual del Explorador TOM

Para que los scripts sean reutilizables, rara vez basta con poder hacer referencia a los objetos del modelo directamente por su nombre, como se muestra arriba. En su lugar, es útil hacer referencia al/los objeto(s) seleccionados actualmente en la **vista del Explorador TOM** de Tabular Editor. Esto es posible mediante el uso del objeto `Selected`.

```csharp
Info("Actualmente has seleccionado: " + Selected.Measures.Count + " medida(s).");
```

El objeto `Selected` por sí solo es una colección de todos los objetos seleccionados actualmente, incluidos los objetos que hay dentro de las carpetas de visualización seleccionadas. Además, el objeto `Selected` contiene varias propiedades que facilitan hacer referencia a tipos de objeto específicos, como la propiedad `.Measures` mostrada en el ejemplo anterior. En general, estas propiedades existen tanto en plural (`.Measures`, medidas) como en singular (`.Measure`, medida). El primero es una colección que puedes recorrer y que estará vacía si la selección actual no contiene ningún objeto de ese tipo, mientras que el segundo es una referencia al objeto seleccionado actualmente, si y solo si se ha seleccionado exactamente un objeto de ese tipo.

El artículo @useful-script-snippets incluye muchos ejemplos de scripts que usan el objeto `Selected` para realizar varias tareas.

# Interacción con el usuario

En los ejemplos anteriores, usamos los métodos globales `Info(...)` y `Warning(...)` para mostrar mensajes al usuario de distintas formas. Tabular Editor ofrece varios de estos métodos globales, así como métodos de extensión para mostrar y recopilar información, y para otras tareas habituales. Los más utilizados se enumeran a continuación:

- `void Output(object value)` - detiene la ejecución del script y muestra información detallada sobre el objeto proporcionado. Cuando el objeto proporcionado es un objeto TOM o una colección de objetos TOM, se muestra una vista detallada de todas las propiedades.
- `void SaveFile(string filePath, string content)` - forma práctica de guardar datos de texto en un archivo.
- `string ReadFile(string filePath)` - forma práctica de cargar datos de texto desde un archivo.
- `string ExportProperties(IEnumerable<ITabularNamedObject> objects, string properties = "...")` - forma práctica de exportar un conjunto de propiedades de varios objetos como una cadena TSV.
- `void ImportProperties(string tsvData)` - forma práctica de cargar propiedades en varios objetos a partir de una cadena TSV.
- `string ConvertDax(dax, useSemicolons)` - convierte una expresión DAX entre configuraciones regionales de EE. UU./Reino Unido y las que no son de EE. Si `useSemicolons` es `true` (valor predeterminado), la cadena `dax` se convierte del formato nativo de EE. UU./Reino Unido a un formato no EE. Es decir, las comas (separadores de lista) se convierten en punto y coma y los puntos (separadores decimales) se convierten en comas. Y viceversa si `useSemicolons` se establece en `false`.
- `void FormatDax(IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - da formato a las expresiones DAX en todos los objetos de la colección proporcionada
- `void FormatDax(IDaxDependantObject obj)` - pone un objeto en cola para el formateo de expresiones DAX cuando finalice la ejecución del script, o cuando se llame al método `CallDaxFormatter`.
- `void CallDaxFormatter(bool shortFormat, bool? skipSpace)` - da formato a todas las expresiones DAX de los objetos que se hayan puesto en cola hasta el momento
- `void Info(string message)` - Muestra mensajes informativos.
- `void Warning(string message)` - Muestra mensajes de advertencia.
- `void Error(string message)` - Muestra mensajes de error.
- `measure SelectMeasure(Measure preselect = null, string label = "...")` - Muestra una lista de todas las medidas y solicita al usuario que seleccione una.
- `T SelectObject<T>(this IEnumerable<T> objects, T preselect = null, string label = "...") where T: TabularNamedObject` - Muestra una lista de los objetos proporcionados, solicita al usuario que seleccione uno y devuelve ese objeto (o null si se pulsó el botón Cancelar).
- `IList<T> SelectObjects<T>(this IEnumerable<T> objects, IEnumerable<T> preselect = null, string label = "...") where T: TabularNamedObject` - Muestra una lista de los objetos proporcionados, solicita al usuario que seleccione uno o varios y devuelve la lista de objetos seleccionados (o null si se pulsó el botón Cancelar).

# Guardar un script como macro

Los scripts que usas a menudo se pueden guardar como macros reutilizables, que siempre estarán disponibles cuando inicies Tabular Editor. Además, las macros quedan integradas automáticamente en el menú contextual de la **vista del Explorador TOM** y también puedes usar la opción **Herramientas > Personalizar...** para añadir macros a menús y barras de herramientas existentes o personalizados.

Para guardar un script como macro, usa la opción **C# Script > Guardar como macro...**.

![Guardar nueva macro](~/content/assets/images/save-new-macro.png)

Indica un nombre para tu macro. Puedes usar barras invertidas para organizar las macros en carpetas; por ejemplo, un nombre como "My Macros\Test" creará un submenú "My Macros" en el menú contextual del Explorador TOM y, dentro de ese submenú, habrá una opción de menú "Test" que ejecuta el script.

También puedes proporcionar una descripción emergente opcional, que se mostrará al pasar el cursor sobre la opción de menú creada por la macro.

También debes especificar el contexto de la macro, que indica el/los tipo(s) de objetos que deben estar seleccionados para que la macro esté disponible en el menú contextual.

Por último, en **Condición de habilitación de la macro (avanzado)** puedes especificar una expresión C# que se evalúe como true/false (normalmente en función de los objetos `Selected` o `Model`). Esto te permite controlar con más detalle si la macro debe estar habilitada o no, según la selección actual. Por ejemplo, podrías usar la siguiente expresión:

```csharp
Selected.Measures.Count == 1
```

para habilitar tu macro solo cuando se seleccione exactamente 1 medida.

# Administración de macros

Puedes ver todas las macros guardadas anteriormente en la **Vista de macros**. Para traer esta vista al primer plano, usa la opción de menú **Ver > Macros**. Esta vista te permite:

- **Cambiar el nombre de una macro** (simplemente coloca el cursor en la columna **Nombre** y escribe el nuevo nombre)
- **Eliminar una macro.** Selecciónala y haz clic en el botón rojo "X" encima de la lista de macros.
- **Editar una macro.** Haz doble clic en la macro de la lista (haz doble clic en la columna "Id" de la lista). Esto abrirá la macro en una nueva vista de C# Script, donde podrás modificar el código. Pulsa Ctrl+S para guardar los cambios de código. Si necesitas editar otras propiedades de la macro (descripción emergente, contexto de la macro, etc.), usa la opción de menú **C# Script > Edit Macro...**.

# Próximos pasos

- @personalizing-te3
- @boosting-productivity-te3

# Lecturas adicionales

- @csharp-scripts
- @useful-script-snippets