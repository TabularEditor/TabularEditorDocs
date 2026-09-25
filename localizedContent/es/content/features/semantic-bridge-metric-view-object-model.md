---
uid: semantic-bridge-metric-view-object-model
title: Modelo de objetos de la Metric View de Semantic Bridge
author: Greg Baldini
updated: 2026-06-29
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
> El Puente semántico está disponible en versión preliminar pública.
> La versión 3.25.0 admite metadatos de Metric View v0.1 y la versión 3.26.2 admite metadatos de Metric View v1.1.

El Puente semántico incluye un modelo de objetos que representa una [Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/).
Esto te permite trabajar con Metric Views mediante programación a través de C# Scripts, de forma similar a como trabajas con un modelo tabular a través de TOMWrapper.

Aparte de la [GUI de importación](xref:semantic-bridge#interface), todo el acceso y la interacción con una Metric View se realizan mediante C# Scripts.
Todo el contenido de este documento hace referencia al código C# que usarías en un [C# Script](xref:csharp-scripts).

## Carga y acceso a la Metric View

Puedes cargar una Metric View con [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) o [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A).
Esto almacena la Metric View deserializada en [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model).
Esta propiedad devuelve un objeto [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View), que es la raíz del grafo de objetos de la Metric View.

```csharp {compile}
// Load a Metric View from disk
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");

// Access the loaded View
var view = SemanticBridge.MetricView.Model;
Output($"Metric View version: {view.Version}\r\nSource: {view.Source}");
```

Al igual que un modelo tabular —y a diferencia de la mayoría de los demás objetos a los que quizá esté acostumbrado en un C# Script—, Metric View es persistente entre varias ejecuciones del script.
Esto significa que puedes cargar una Metric View una sola vez y hacer referencia a ella en ejecuciones posteriores de scripts sin tener que volver a cargarla cada vez.
Solo se carga una única Metric View y está disponible en todos los scripts como `SemanticBridge.MetricView.Model`, como se mencionó anteriormente.
Este comportamiento es similar al del modelo tabular en scripts de C#, que siempre está disponible simplemente como `Model`.

[!INCLUDE [sample](../how-tos/includes/sample-metricview.md)]

## Objetos de dominio

El modelo de objetos consta de cuatro tipos principales que se corresponden con la estructura de un archivo YAML de la Metric View.
No repetimos aquí toda la especificación, así que te recomendamos que consultes la [documentación de Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/)
y nuestra [propia referencia de la API para el modelo de objetos](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView).

| Referencia de la API                                                                  | Descripción                                                                         |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| [`View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View)      | El objeto raíz que representa la Metric View completa                               |
| [`Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join)      | Una definición de unión que conecta una tabla de dimensiones con la tabla de hechos |
| [`Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field)    | Una definición de campo (columna) en la Metric View              |
| [`Medida`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) | Una definición de agregación que representa la lógica de negocio                    |

La mayoría de las propiedades y atributos de una Metric View tienen una representación estructurada en el modelo de objetos,
pero no los trataremos en este documento,
ya que todos son representaciones directas de la especificación de Metric View y están documentados en la referencia de la API mencionada anteriormente.

> [!NOTE]
> El modelo de objetos se introdujo en Tabular Editor 3.25.0 con compatibilidad con Metric View v0.1.
> La compatibilidad con Metric View v1.1 se agregó en Tabular Editor 3.26.2;
> esto incluye las propiedades `Comment` y `Materialization` en `View`,
> `Cardinality` y `Rely` en `Join`,
> `Comment`, `DisplayName`, `Synonyms` y `Format` en `Field` y `medida`,
> y `Window` en `medida`.

> [!NOTE]
> En el modelo de objetos, seguimos las convenciones de nomenclatura de C#: `PascalCase` para todos los nombres de tipos y propiedades.
> La especificación YAML de Metric View sigue una convención de nomenclatura `snake_case`.
> La serialización y la deserialización convierten entre ambos, por lo que los C# Scripts usan `PascalCase` y el YAML que leemos y escribimos mantiene el `snake_case` conforme a la especificación.

### Vista

[El objeto `View`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View) es el elemento raíz de la Metric View y contiene:

- `Version`: La versión de la especificación de Metric View (p. ej., "1.1")
- `Source`: Los datos de origen de la tabla de hechos (p. ej., "catalog.schema.table")
- `Filter`: Expresión booleana SQL opcional que se aplica a todas las consultas
- `Comment`: Descripción opcional de la Metric View
- `Joins`: Colección de definiciones de unión; colección vacía, pero no nula, si no hay ningún `Join`
- `Fields`: Colección de definiciones de campo; colección vacía, pero no nula, si no hay ningún `Field`
- `Measures`: Colección de definiciones de medidas; colección vacía, pero no nula, si no hay ningún `Measure`
- `Materialization`: Configuración de materialización para la aceleración de consultas cuando se hospeda en Databricks; [consulta la referencia de la API `Materialization`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Materialization)

```csharp {run id=view-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Version: {view.Version}");
sb.AppendLine($"Source: {view.Source}");
sb.AppendLine($"Filter: {view.Filter ?? "(none)"}");
sb.AppendLine($"Joins: {view.Joins.Count}");
sb.AppendLine($"Fields: {view.Fields.Count}");
sb.AppendLine($"Measures: {view.Measures.Count}");

Output(sb.ToString());
```

**Salida**

```
Version: 1.1
Source: sales.fact.orders
Filter: (none)
Joins: 3
Fields: 6
Measures: 6
```

### Join

[Un `Join`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Join) representa una tabla de dimensiones que se une a la tabla de hechos:

- `Name`: Nombre de la tabla unida (se usa como alias)
- `Source`: Tabla de origen o consulta para el join (p. ej., "catalog.schema.dimension_table")
- `On`: Expresión booleana SQL opcional para la condición del join
- `Using`: Lista opcional de nombres de columna para el join (alternativa a `On`)
- `Joins`: Uniones secundarias (para esquemas en copo de nieve)
- `ParentJoin`: si se trata de una unión anidada, `ParentJoin` apunta a la unión padre; de lo contrario, es `null`
- `Cardinality`: controla la relación entre `View.Source` o `ParentJoin` y este `Join`; [consulta la referencia de la API `JoinCardinality`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.JoinCardinality)
- `Rely`: Sugerencias para el optimizador sobre la relación de este `Join` con su unión padre; [consulta la referencia de la API `Rely`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Rely)

```csharp {run id=join-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var join in view.Joins)
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

**Salida**

```
Join: product
  Source: sales.dim.product
  On: source.product_id = product.product_id
Join: customer
  Source: sales.dim.customer
  On: source.customer_id = customer.customer_id
Join: date
  Source: sales.dim.date
  On: source.order_date = date.date_key
```

### Campo

[Un `Field`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field) representa un campo (columna) en la Metric View:

- `Name`: El nombre del campo, al que se hace referencia en las expresiones de Metric View
- `Expr`: La expresión SQL que define el campo (ya sea una referencia a una columna o una expresión SQL)
- `Comment`: Descripción opcional del campo
- `DisplayName`: Nombre para mostrar opcional y legible del campo
- `Synonyms`: Nombres alternativos opcionales del campo, usados por herramientas de IA y BI
- `Format`: Especificación opcional del formato de visualización para los valores del campo; [consulta la referencia de la API `Format`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format)

```csharp {run id=field-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var field in view.Fields)
{
    sb.AppendLine($"Field: {field.Name}");
    sb.AppendLine($"  Expression: {field.Expr}");
}

Output(sb.ToString());
```

**Salida**

```
Field: product_name
  Expression: product.product_name
Field: product_category
  Expression: product.category
Field: customer_segment
  Expression: customer.segment
Field: order_date
  Expression: date.full_date
Field: order_year
  Expression: date.year
Field: order_month
  Expression: date.month_name
```

### Medida

[Una `medida`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Measure) representa una agregación con nombre con lógica de negocio:

- `Name`: El nombre de la medida, al que se hace referencia en las expresiones de Metric View como `MEASURE(<name>)`
- `Expr`: La expresión de agregación SQL que define la medida
- `Comment`: Descripción opcional de la medida
- `DisplayName`: Nombre para mostrar opcional y legible de la medida
- `Synonyms`: Nombres alternativos opcionales de la medida, usados por herramientas de IA y BI
- `Format`: Especificación opcional del formato de visualización para los valores de la medida; [consulta la referencia de la API `Format`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format)
- `Window`: Lista opcional de especificaciones de ventana para agregaciones con ventana o semiaditivas; [consulta la referencia de la API `Window`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Window)

```csharp {run id=measure-props setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

foreach (var measure in view.Measures)
{
    sb.AppendLine($"Measure: {measure.Name}");
    sb.AppendLine($"  Expression: {measure.Expr}");
}

Output(sb.ToString());
```

**Salida**

```
Measure: total_revenue
  Expression: SUM(revenue)
Measure: gross_margin
  Expression: SUM(revenue) - SUM(cost)
Measure: order_count
  Expression: COUNT(*)
Measure: avg_order_value
  Expression: AVG(revenue)
Measure: revenue_to_budget
  Expression: (SUM(revenue) - SUM(budget)) / SUM(budget)
Measure: unique_customers
  Expression: COUNT(DISTINCT customer_id)
```

## Directivas using

Al trabajar con el modelo de objetos de Metric View en C# Script, es posible que necesite agregar una directiva using para evitar conflictos de nombres con tipos que tienen nombres similares en el Tabular Object Model.
Recomendamos asignar un alias al espacio de nombres:

```csharp {compile}
// Alias to avoid conflicts with TOM types like Measure
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var view = SemanticBridge.MetricView.Model;

// Now you can reference types explicitly
foreach (MetricView.Field field in view.Fields)
{
    // ...
}
```

## Interacción con el modelo de objetos

Este documento describe los patrones de uso del modelo de objetos.
Consulta [las guías prácticas de Semantic Bridge para ver ejemplos detallados listos para copiar y pegar](xref:semantic-bridge-how-tos).

### Puntero al `View` padre

Todos los objetos principales de Metric View descritos en este documento heredan de [`MetricViewObjectBase`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.MetricViewObjectBase) para su funcionalidad principal.
Entre otras cosas, esto significa que cada uno contiene un puntero `View` que remite a la Metric View en la que está definido.
Esto te permite inspeccionar toda la Metric View cuando trabajas con cualquiera de estos objetos.

```csharp {compile}
SemanticBridge.MetricView.Load("C:/path/to/metricview.yaml");
var v = SemanticBridge.MetricView.Model; // alias the Metric View as v just for concision
var f = v.Fields.FirstOrDefault(); // f is the first field defined in the Metric View
Output(f.View == v); // the field, f, lets you navigate up to the containing view
```

### Agregar objetos

Nunca creas una instancia de `View`, `Join`, `Field` o `Medida` directamente.
En su lugar, deserializa o carga un `View` base, o usa los distintos métodos `Add`:

- Nueva Metric View:
  - [`Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A) YAML en una cadena de texto
  - [`Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A) un archivo YAML desde el disco
- Agregar objetos
  - [`view.AddJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddJoin%2A)
  - [`view.AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A)
  - [`view.AddMedida`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddMeasure%2A)

Tanto `Deserialize` como `Load` establecen la variable global `SemanticBridge.MetricView.Model` para que puedas interactuar con ella en scripts.
Todos los métodos `Add` devuelven el nuevo objeto que se acaba de agregar para que puedas interactuar con él y establecer propiedades adicionales;
esto refleja la interacción con los objetos TOM que ya conoces en C# Script.

### Modificar propiedades

El modelo de objetos de Metric View es mutable en su totalidad, por lo que puedes establecer propiedades directamente.
El autocompletado de C# en Tabular Editor 3 te ayudará a encontrar las propiedades y los tipos correctos que debes usar.
Todas las propiedades y sus tipos se encuentran en [la documentación de la API](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView).

### Acceso a objetos por nombre

La `View` raíz contiene colecciones de `Joins`, `Fields` y `Medidas`.
Cada `Join` contiene una colección secundaria `Joins`.
Cada uno puede indexarse por nombre;
esto busca el objeto secundario por su propiedad `Name`.
Esta búsqueda no distingue entre mayúsculas y minúsculas, igual que el comportamiento predeterminado en Databricks SQL.

### Versiones de Metric View

Seguimos la [documentación de Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/) para mantenernos al día con la especificación.
Todas las propiedades están anotadas con la versión en la que se introdujeron.
Gracias a esto, el modelo de objetos generará excepciones y mostrará diagnósticos si intentas establecer una propiedad que no está permitida para una versión determinada de la especificación.
Recomendamos ejecutar siempre [`SemanticBridge.MetricView.Validate();`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate) después de modificar una Metric View en un C# Script;
esto comprobará que todas las reglas de validación predeterminadas se cumplan correctamente.

## Referencias

- [Documentación de la API del espacio de nombres `MetricView`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-metric-view-validation
- @semantic-bridge-metric-view-tabular-traducción
- [Guías prácticas de Semantic Bridge para ver ejemplos detallados](xref:semantic-bridge-how-tos)
- [Documentación de Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/)
- [Especificación YAML de Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference)
