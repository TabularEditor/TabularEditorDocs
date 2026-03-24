---
uid: semantic-bridge-metric-view-object-model
title: Modelo de objetos de la Metric View de Semantic Bridge
author: Greg Baldini
updated: 2025-01-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Modelo de objetos de la Metric View

<!--
SUMMARY: Overview of the Metric View object model built into the Semantic Bridge.
-->

> [!NOTE]
> Semantic Bridge, tal y como se publicó en la versión 3.25.0, es una característica MVP.
> Tiene limitaciones, como se documenta a continuación, y la API y el alcance de la funcionalidad están sujetos a cambios.
> Este modelo de objetos carece claramente de muchas de las capacidades disponibles en TOMWrapper, con las que quizá esté familiarizado a partir de un C# Script para manipular un modelo tabular.
> Como se indica en las [limitaciones de Semantic Bridge](xref:semantic-bridge#mvp-limitations), actualmente solo admitimos metadatos de Metric View v0.1.

Semantic Bridge incluye un modelo de objetos que representa una Metric View de Databricks.
Esto te permite trabajar con Metric Views mediante programación a través de C# Scripts, de forma similar a como trabajas con un modelo tabular a través de TOMWrapper.

Aparte de la [GUI de importación](xref:semantic-bridge#interface), todo el acceso y la interacción con una Metric View se realizan mediante C# Scripts.
Todo el contenido de este documento hace referencia al código C# que usarás en un [C# Script](xref:csharp-scripts).

<a name="loading-and-accessing-the-metric-view"></a>
## Carga y acceso a la Metric View

Puedes cargar una Metric View con [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Load_System_String_) o [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Deserialize_System_String_).
Esto almacena la Metric View deserializada como [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Model).
Esta propiedad devuelve un objeto [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View), que es la raíz del grafo de objetos de la Metric View.

```csharp
// Cargar una Metric View desde el disco
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");

// Acceder a la View cargada
var view = SemanticBridge.MetricView.Model;
Output($"Versión de Metric View: {view.Version}\r\nOrigen: {view.Source}");
```

Al igual que un modelo tabular —y a diferencia de la mayoría de los demás objetos a los que quizá esté acostumbrado en un C# Script—, Metric View es persistente entre varias ejecuciones del script.
Esto significa que puedes cargar una Metric View una sola vez y hacer referencia a ella en ejecuciones posteriores de scripts sin tener que volver a cargarla cada vez.
Solo se carga una única Metric View y está disponible en todos los scripts como `SemanticBridge.MetricView.Model`, como se mencionó anteriormente.
Este comportamiento es similar al del modelo tabular en scripts de C#, que siempre está disponible simplemente como `Model`.

## Objetos de dominio

El modelo de objetos consta de cuatro tipos principales que se corresponden con la estructura de un archivo YAML de una Metric View:
No repetimos aquí toda la especificación, por lo que te animamos a consultar la [documentación de Metric View de Databricks](https://learn.microsoft.com/en-us/azure/databricks/metric-views/).

| Referencia de la API                                                                       | Descripción                                                                         |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View)           | El objeto raíz que representa la Metric View completa                               |
| [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join)           | Una definición de unión que conecta una tabla de dimensiones con la tabla de hechos |
| [`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) | Una definición de campo (columna) en la Metric View              |
| [`Medida`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure)      | Una definición de agregación que representa la lógica de negocio                    |

> [!NOTE]
> En el modelo de objetos, seguimos las convenciones de nomenclatura de C#, por lo que usamos `PascalCase` para todos los nombres de tipos y propiedades del modelo de objetos.
> La especificación YAML de Metric View sigue una convención de nomenclatura `snake_case`.
> En general, nos centramos en el modelo de objetos de C#, que es un componente de Semantic Bridge.
> Además de cambiar la capitalización, no modificamos ninguna convención de nomenclatura del YAML.

### Vista

El objeto [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) es la raíz de la Metric View y contiene:

- `Version`: La versión de la especificación de Metric View (p. ej., "0.1")
- `Source`: Los datos de origen de la tabla de hechos (p. ej., "catalog.schema.table")
- `Filter`: Expresión booleana SQL opcional que se aplica a todas las consultas
- `Joins`: Colección de definiciones de unión
- `Dimensions`: Colección de definiciones de dimensiones (campos)
- `Measures`: Colección de definiciones de medidas

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Versión: {view.Version}");
sb.AppendLine($"Origen: {view.Source}");
sb.AppendLine($"Filtro: {view.Filter ?? "(ninguno)"}");
sb.AppendLine($"Uniones: {view.Joins?.Count ?? 0}");
sb.AppendLine($"Dimensiones: {view.Dimensions?.Count ?? 0}");
sb.AppendLine($"Medidas: {view.Measures?.Count ?? 0}");

Output(sb.ToString());
```

#### Traducción y validación de `View`

La propiedad `View.Source` se convierte en la tabla de hechos del modelo tabular, con el nombre `'Fact'`.
Si `Source` es una referencia de tabla o vista de 3 partes, se traduce a una partición M que accede al objeto SQL por su nombre.
Si `Source` no es una referencia de tabla o vista de 3 partes, se traduce a una partición M con una consulta SQL incrustada, siendo la totalidad de la cadena `Source` la propia consulta SQL.
La propiedad `Filter` se ignora a efectos de la traducción.

Para evaluar las reglas de validación, primero se comprueba `View` y después se valida cada colección en este orden: `Joins`, luego `Dimensions` y, por último, `Measures`.
La validación de la tabla de hechos `Source` se realiza en una regla de validación del objeto `View`.

### Join

Un [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join) representa una tabla de dimensiones que se une a la tabla de hechos:

- `Name`: Nombre de la tabla unida (se usa como alias)
- `Source`: Tabla de origen o consulta para el join (p. ej., "catalog.schema.dimension_table")
- `On`: Expresión booleana SQL opcional para la condición del join
- `Using`: Lista opcional de nombres de columna para el join (alternativa a `On`)
- `Joins`: Uniones secundarias (para esquemas en copo de nieve)

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var join in view.Joins ?? [])
{
    sb.AppendLine($"Join: {join.Name}");
    sb.AppendLine($"  Source: {join.Source}");
    if (!string.IsNullOrEmpty(join.On))
        sb.AppendLine($"  On: {join.On}");
    if (join.Using != null && join.Using.Count > 0)
        sb.AppendLine($"  Using: {string.Join(", ", join.Using)}");
}

Output(sb.ToString());
```

#### Traducción y validación de `Join`

No se admiten `Join`s anidados; es decir, solo se puede traducir un esquema en estrella estricto.
Para la traducción, solo se admiten joins `On` con un equijoin de un único campo.
Cada `Join` se convierte en una tabla Tabular, con una partición M definida según las mismas reglas que para la propiedad `View.Source`.

Los `Join`s se validan en el orden en que aparecen en la definición de la Metric View.

### Dimensión

Una [`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) representa un campo (columna) en la Metric View:

- `Name`: el nombre para mostrar de la dimensión
- `Expr`: La expresión SQL que define la dimensión (ya sea una referencia a una columna o una expresión SQL)

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var dim in view.Dimensions ?? [])
{
    sb.AppendLine($"Dimension: {dim.Name}");
    sb.AppendLine($"  Expression: {dim.Expr}");
}

Output(sb.ToString());
```

#### `Dimension`: Traducción y validación

Cada `Dimension` se convierte en una columna del modelo tabular.
Si `Expr` es una referencia de campo no calificada, se agrega a la tabla de hechos.
Si `Expr` es una referencia calificada (por ejemplo, `table.field`), se agrega a la tabla creada para el `Join` con el mismo nombre que la parte de tabla de la referencia calificada; si la parte de tabla es `source`, se agrega a la tabla de hechos.
Tanto si la referencia de campo es calificada como si no lo es, el campo se agrega como una [`TOMWrapper.DataColumn`](xref:TabularEditor.TOMWrapper.DataColumn).
Si `Expr` es una expresión SQL, se agrega como [`TOMWrapper.CalculatedColumn`](xref:TabularEditor.TOMWrapper.CalculatedColumn).
Cuando `Expr` es una expresión SQL, intentamos extraer todas las referencias de campo; si todas las referencias de campo comparten la misma parte de tabla, se agrega a la tabla creada para ese `Join`; de lo contrario, se agrega a la tabla de hechos.
No traducimos las expresiones SQL de las propiedades `Dimension.Expr`; la expresión SQL se incluye como un comentario en la expresión DAX de la `CalculatedColumn`.
Depende del usuario traducir estas expresiones.
Intentamos identificar todas las referencias de campo en la expresión SQL y agregarlas al modelo tabular como columnas `DataColumn` si aún no existen como una `Dimension` de Metric View.

Algunos ejemplos:

| `Expr`                                                | Traducido como tipo | Añadido a la tabla | Nota                                                                                              |
| ----------------------------------------------------- | ------------------- | ------------------ | ------------------------------------------------------------------------------------------------- |
| `field1`                                              | `DataColumn`        | `'Fact'`           | las referencias de campo sin calificar son equivalentes a las calificadas con `source`            |
| `source.field2`                                       | `DataColumn`        | `'Fact'`           | `source` es una referencia a la propiedad `View.Source`, también conocida como la tabla de hechos |
| `dimCustomer.key`                                     | `DataColumn`        | `'dimCustomer'`    | debe haber un `Join` cuya propiedad `Name` sea `dimCustomer`                                      |
| `CONCAT(dimCustomer.FirstName, dimCustomer.LastName)` | `CalculatedColumn`  | `'dimCustomer'`    | todas las partes de tabla del nombre cualificado se refieren al mismo nombre                      |
| `CONCAT(dimGeo.Country, dimCustomer.Address)`         | `CalculatedColumn`  | `'Fact'`           | hay varias partes de tabla diferentes                                                             |

Las `Dimension`s se validan en el orden en que aparecen en la definición de Metric View.

### Medida

Una [`medida`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) representa una agregación con nombre y lógica de negocio:

- `Name`: El nombre para mostrar de la medida
- `Expr`: La expresión de agregación SQL que define la medida

```csharp
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var measure in view.Measures ?? [])
{
    sb.AppendLine($"Medida: {measure.Name}");
    sb.AppendLine($"  Expresión: {measure.Expr}");
}

Output(sb.ToString());
```

#### Traducción y validación de `Measure`

Todas las medidas se agregan a la tabla de hechos.
Las agregaciones simples se traducen a expresiones DAX.
Una agregación simple es una única agregación de un único campo (p. ej., `SUM(table.field)`).
Las agregaciones admitidas son sum, count, distinct count, max, min y average.
Otras expresiones se incluyen tal cual como comentario en la expresión DAX de la medida tabular.
Intentamos identificar todas las referencias a campos en la expresión SQL y añadirlas al modelo tabular como `DataColumn`s si aún no existen como una `Dimension` de Metric View.

> [!WARNING]
> SQL y DAX son lenguajes distintos con semánticas diferentes.
> Es posible que una medida traducida automáticamente no exprese el mismo cálculo tanto en Databricks Metric Views como en modelos tabulares.
> Depende del usuario comprobar que todo el código funciona como se espera.

Las `medida`s se validan en el orden en que aparecen en la definición de Metric View.

## Directivas using

Al trabajar con el modelo de objetos de Metric View en C# Script, es posible que necesite agregar una directiva using para evitar conflictos de nombres con tipos que tienen nombres similares en el Tabular Object Model.
Recomendamos asignar un alias al espacio de nombres:

```csharp
// Alias para evitar conflictos con tipos de TOM como Measure
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var view = SemanticBridge.MetricView.Model;

// Ahora puedes hacer referencia explícita a los tipos
foreach (MetricView.Dimension dim in view.Dimensions ?? [])
{
    // ...
}
```

## Ejemplo completo

A continuación se muestra un script completo que carga una Metric View y genera un resumen de su contenido:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// Cargar la Metric View
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

// Resumen con sb.AppendLine
sb.AppendLine("=== Resumen de la Metric View ===");
sb.AppendLine($"Versión: {view.Version}");
sb.AppendLine($"Origen: {view.Source}");

if (view.Joins != null && view.Joins.Count > 0)
{
    sb.AppendLine($"\nUniones ({view.Joins.Count}):");
    foreach (var join in view.Joins)
    {
        sb.AppendLine($"  - {join.Name} -> {join.Source}");
    }
}

if (view.Dimensions != null && view.Dimensions.Count > 0)
{
    sb.AppendLine($"\nDimensiones ({view.Dimensions.Count}):");
    foreach (var dim in view.Dimensions)
    {
        sb.AppendLine($"  - {dim.Name}: {dim.Expr}");
    }
}

if (view.Measures != null && view.Measures.Count > 0)
{
    sb.AppendLine($"\nMedidas ({view.Measures.Count}):");
    foreach (var measure in view.Measures)
    {
        sb.AppendLine($"  - {measure.Name}: {measure.Expr}");
    }
}

Output(sb.ToString());
```

## Referencias

- [Documentación de la API del espacio de nombres `MetricView`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
- @semantic-bridge-how-tos
- [Documentación de Databricks Metric View](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)
- [Especificación YAML de Databricks Metric View](https://learn.microsoft.com/en-us/azure/databricks/metric-views/data-modeling/syntax)
