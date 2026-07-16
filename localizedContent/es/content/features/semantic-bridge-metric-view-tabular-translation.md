---
uid: semantic-bridge-metric-view-tabular-traducción
title: Traducción de Metric View a Tabular
author: Greg Baldini
updated: 2026-06-30
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

# Traducción de Metric View a Tabular

<!--
SUMMARY: Describes the process and specifics of translating a Metric View to a TOM model.
-->

> [!NOTE]
> El Semantic Bridge está en versión preliminar pública.
> La versión 3.25.0 admite metadatos de Metric View v0.1 y la versión 3.26.2 admite metadatos de Metric View v1.1.
> Las limitaciones se describen a continuación.

Esta página describe cómo funciona la traducción al importar una definición de Metric View a un modelo tabular.

## Proceso de traducción

La traducción de una Metric View a un modelo tabular se realiza en varios pasos:

1. Leer el YAML del disco
2. Deserializar el YAML
3. Validar que el YAML deserializado represente una Metric View válida
4. Si es una Metric View válida, se almacena como la Metric View cargada actualmente, de forma similar a como existe un modelo tabular cargado con el que interactúas.
   Si no es una Metric View válida, el proceso se detiene aquí y hay mensajes de diagnóstico disponibles.
5. Analizar la Metric View e intentar transformarla en una representación intermedia
6. Intentar transformar la representación intermedia en un modelo tabular

La interfaz de importación se encarga de todo por ti, pero también puedes usar C# Scripts para personalizar distintos pasos del proceso y trabajar con Metric View de forma programática, de manera similar a como lo haces con un modelo tabular.
En concreto, puedes

- cargar una Metric View desde el disco con [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A): la carga la pone a disposición en C# Scripts como [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model), pero no importa la estructura en el modelo tabular
- deserializar una Metric View desde una cadena con [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A): al igual que al cargarla, el modelo queda disponible como [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model), pero no se importa
- guardar una Metric View en el disco con [`SemanticBridge.MetricView.Save`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Save%2A)
- serializar una Metric View a una cadena con [`SemanticBridge.MetricView.Serialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Serialize%2A).
- validar una Metric View usando un sistema similar al [Best Practice Analyzer](xref:best-practice-analyzer) con [`SemanticBridge.MetricView.Validate`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate%2A)
  - puedes crear tus propias reglas de validación personalizadas con [`SemanticBridge.MetricView.MakeValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRule%2A) y sus versiones simplificadas
- importar una Metric View a Tabular con [`SemanticBridge.MetricView.ImportToTabularFromFile`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.ImportToTabularFromFile%2A), que hace exactamente lo mismo que la GUI de importación, o [`SemanticBridge.MetricView.ImportToTabular`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.ImportToTabular%2A), que es similar, pero opera sobre la Metric View cargada actualmente, en lugar de leer una desde el disco.

### Notas de traducción por objeto

Los cuatro elementos siguientes, `View`, `Join`, `Field` y `medida`, son los objetos principales de una definición de Metric View que se convierten en objetos TOM.
El resto de los metadatos de la definición de Metric View se ignoran o bien modifican con precisión la forma en que se traducen estos objetos.

> [!NOTE]
> La traducción se realiza sobre el modelo de objetos de Metric View, por lo que describimos todo en esos términos.
> Consulta [la documentación del modelo de objetos de Metric View](xref:semantic-bridge-metric-view-object-model) para conocer los detalles del modelo de objetos y cómo se ajusta a la especificación YAML.

#### Traducción de `View`

- traducir
  - `Source`: se convierte en la única tabla de hechos, llamada 'Fact', en el modelo TOM
  - `Comment`: se convierte en `Model.Description` en TOM
  - `Joins`: consulta `Join`
  - `Fields`: consulta `Field`
  - `Measures`: consulta `medida`
- no traducir
  - `Filter`
  - `Materialization`

Si `Source` es una referencia de tabla o vista de 3 partes, se traduce a una partición M que accede al objeto SQL por su nombre.
Si `Source` no es una referencia de tabla o vista de 3 partes, se traduce a una partición M con una consulta SQL incrustada, siendo la totalidad de la cadena `Source` la propia consulta SQL.

La propiedad `Filter` se ignora a efectos de la traducción;
si necesitas incluir la lógica de `Filter`, tendrás que agregarla manualmente.
La expresión `Filter` se aplica a todas las consultas contra la Metric View y, por lo tanto, una traducción totalmente automatizada requeriría unir todas las tablas indicadas en `Joins` en el código M generado en TOM.

Se ignora cualquier `Materialization` definida a efectos de la traducción;
se trata de metadatos de optimización de consultas para ejecutar consultas en Databricks y no son relevantes para un modelo TOM.

#### Traducción de `Join`

- traducido
  - `Name`: se convierte en el nombre de la tabla en TOM
  - `Source`: se convierte en una partición M de la tabla
  - `On`: se convierte en una relación en TOM
  - `Joins`: se convierten en tablas TOM adicionales
  - `Cardinality`
- sin traducir
  - `Using`
  - `Rely`

Cada `Join` se convierte en una tabla TOM, con una partición M definida según las mismas reglas que para la propiedad `View.Source`.

Los equijoins de `On` (por ejemplo, `source.fk = dimTable.pk`) se convierten en relaciones TOM.
Cualquier otro predicado de la propiedad `On` no se traduce en una relación.

Los árboles de `Join` en una Metric View se traducen como tablas TOM en una cadena de relaciones N:1, siempre que se admitan las cardinalidades (consulta la nota sobre la cardinalidad más abajo).
Esto representa un esquema de copo de nieve.

El valor `ManyToOne` de `Cardinality` se traduce como una relación TOM N:1.
Una `Cardinality` sin valor, o un `Join` sin esta propiedad configurada, se considera `ManyToOne` de forma predeterminada, según la [documentación de Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#joins).
Otros valores de `Cardinality` aún no se admiten para su traducción como una relación.

Los joins `Using` no se admiten para la traducción; no generan una relación TOM.

`Rely` no se propaga al modelo TOM de ninguna manera.

En los casos en que no se crea una relación TOM, aun así creamos una tabla TOM y traducimos todos los `Fields` de Metric View a columnas TOM, como se describe en otras secciones.

> [!NOTE]
> Databricks ha introducido recientemente un nuevo patrón que usa la cardinalidad `OneToMany` en varios subárboles de `Join` para implementar un modelo de múltiples hechos.
> Aún no traducimos este patrón por completo: incorporamos todas las tablas, campos y medidas, pero no creamos todas las relaciones.
> Se muestra una advertencia de diagnóstico al importar un modelo que sigue este patrón.

#### Traducción de `Field`

- traducidos
  - `Name`
  - `DisplayName`
  - `Expr`
  - `Comment`: se convierte en la propiedad `Description` de la columna TOM
  - `Format`: se convierte en la propiedad `FormatString` de la columna TOM; consulta la sección siguiente sobre la traducción de `Format`
- sin traducir
  - `Synonyms`

Cada `Field` se convierte en una columna del modelo tabular.

El `Name` de la columna TOM es `Field.DisplayName` si está definido;
de lo contrario, es `Field.Name`.

Si `Expr` es una referencia de campo no calificada, se agrega a la tabla de hechos.
Si `Expr` es una referencia calificada (por ejemplo, `table.field`),
entonces se agrega a la tabla creada para el `Join` con el mismo nombre que la parte de tabla de la referencia calificada;
si la parte de tabla es `source`, se agrega a la tabla de hechos.
Tanto si la referencia de campo es calificada como si no lo es,
el campo se agrega como una [`TOMWrapper.DataColumn`](xref:TabularEditor.TOMWrapper.DataColumn).
Si `Expr` es una expresión SQL,
se agrega como [`TOMWrapper.CalculatedColumn`](xref:TabularEditor.TOMWrapper.CalculatedColumn).
Cuando `Expr` es una expresión SQL, extraemos todas las referencias de campo;
si todas las referencias de campo comparten la misma parte de tabla,
la agregamos a la tabla creada para ese `Join`;
de lo contrario, la agregamos a la tabla de hechos.
Identificamos todas las referencias de campo en la expresión SQL y las agregamos al modelo tabular como `DataColumn`s si todavía no existen como un `Field` de Metric View.
No traducimos las expresiones SQL de las propiedades `Field.Expr`;
la expresión SQL se incluye como un comentario en la expresión DAX de la `CalculatedColumn`.
Depende del usuario traducir estas expresiones.

Algunos ejemplos:

| `Expr`                                                | Traducido como tipo | Añadido a la tabla | Nota                                                                                              |
| ----------------------------------------------------- | ------------------- | ------------------ | ------------------------------------------------------------------------------------------------- |
| `field1`                                              | `DataColumn`        | `'Fact'`           | las referencias de campo sin calificar son equivalentes a las calificadas con `source`            |
| `source.field2`                                       | `DataColumn`        | `'Fact'`           | `source` es una referencia a la propiedad `View.Source`, también conocida como la tabla de hechos |
| `dimCustomer.key`                                     | `DataColumn`        | `'dimCustomer'`    | debe haber un `Join` cuya propiedad `Name` sea `dimCustomer`                                      |
| `CONCAT(dimCustomer.FirstName, dimCustomer.LastName)` | `CalculatedColumn`  | `'dimCustomer'`    | todas las partes de tabla del nombre cualificado se refieren al mismo nombre                      |
| `CONCAT(dimGeo.Country, dimCustomer.Address)`         | `CalculatedColumn`  | `'Fact'`           | hay varias partes de tabla diferentes                                                             |

#### Traducción de `Measure`

- traducido
  - `Name`
  - `DisplayName`
  - `Expr`: se convierte en la propiedad `Expression` de la medida TOM; consulta la sección siguiente sobre la traducción de SQL a DAX
  - `Comment`: se convierte en la propiedad `Description` de la medida TOM
  - `Format`: se convierte en la propiedad `FormatString` de la medida TOM; consulta la sección siguiente sobre la traducción de `Format`
- sin traducir
  - `Synonyms`
  - `Window`

Todas las medidas se agregan a la tabla de hechos.

El `Name` de la medida TOM es el `Measure.DisplayName` de la Metric View si existe; de lo contrario, es el `Measure.Name` de la Metric View.

`Expr` se traduce a DAX o se pasa como comentario en los casos en que no podemos traducir automáticamente la medida.
Identificamos todas las referencias a campos en la expresión SQL y las agregamos al modelo tabular como `DataColumn`s si aún no existen como `Field` en la Metric View.

Las especificaciones de ventana no se traducen y hacen que se recurra a un comentario DAX, independientemente del SQL de `Expr`.

### Traducción de `Format`

El `Format` de una Metric View se traduce a un `FormatString` de TOM en el objeto que lo contiene.
El destino es una cadena de formato de estilo VBA, como la que se usa en los modelos TOM.
La traducción se hace con el mejor esfuerzo posible:
si podemos crear una cadena de formato que coincida exactamente con la configuración de `Format`, lo hacemos;
si no podemos crear un equivalente exacto, recurrimos a un equivalente aproximado y emitimos una advertencia que podrás revisar después de la importación.

Los formatos de moneda, porcentaje y número se traducen sin problemas:
la moneda se convierte en un prefijo con símbolo monetario en un formato numérico con separador de miles,
el porcentaje se convierte en un formato de porcentaje que respeta el número de decimales declarado,
y el número respeta el número de decimales declarado y el separador de miles, y la abreviatura científica se convierte en un formato exponencial.

Las fechas de año-mes-día se traducen sin problemas a un formato de fecha ISO;
las fechas según la configuración regional con mes largo y con mes numérico se traducen sin problemas a los formatos con nombre `Long Date` y `Short Date`;
y los formatos de hora con hora-minuto y con hora-minuto-segundo se traducen sin problemas a los formatos con nombre `Short Time` y `Long Time`.

Los formatos restantes no pueden traducirse con precisión y generan una advertencia:
la abreviatura numérica compacta y el formato de bytes recurren a un formato numérico simple;
la fecha según la configuración regional con mes corto recurre a `Long Date`;
la fecha de año-semana recurre a una fecha ISO;
y un formato combinado de fecha y hora recurre a un formato ISO compuesto.

### Traducción de SQL a DAX

Las Metric Views proporcionan una capa estructurada sobre expresiones SQL, por lo que parte de traducir una Metric View consiste en traducir SQL a DAX y M en el modelo tabular.
Las agregaciones admitidas son sum, count, distinct count, max, min y average.
La aritmética básica, los patrones de recuento habituales, las referencias a medidas y la precedencia de los paréntesis son compatibles con la traducción de SQL a DAX.

> [!WARNING]
> Tenga en cuenta que SQL y DAX son lenguajes diferentes con semánticas distintas.
> No podemos garantizar que una medida traducida se comporte de forma idéntica entre el SQL de Metric View y el DAX tabular que generamos.
> Las agregaciones básicas definidas sobre campos de la tabla de hechos deberían comportarse igual, mientras que las agregaciones definidas sobre campos de las tablas de dimensiones tienen más probabilidades de producir resultados no deseados.

## Términos comunes en Metric Views y modelos tabulares

Para los usuarios que quizá no estén familiarizados ni con Metric Views ni con modelos tabulares, a continuación ofrecemos una piedra de Rosetta incompleta.
Nos referimos a los nombres de los objetos de Metric View en función de su representación en YAML, y a los de Tabular en función del nombre del tipo de objeto en TMDL/TMSL.

| Término general | Nombre en Tabular | Nombre en Metric View                                | Descripción                                                                                                                         | Nota                                                                                                                                                                                                                                                                                                                                   |
| --------------- | ----------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| hecho           | tabla             | fuente                                               | Una tabla que contiene claves foráneas hacia las dimensiones y valores cuantitativos que se van a agregar                           | una Metric View tiene un único hecho, sin nombre, que se registra como el atributo `source` en el nivel raíz del YAML. Los modelos tabulares no diferencian entre tipos de tablas: si una tabla es una tabla de hechos solo puede inferirse                                                            |
| dimensión       | tabla             | unión                                                | Una tabla que contiene atributos descriptivos y una clave principal con la que se relaciona el hecho                                | Los modelos tabulares no diferencian, por lo que el rol de "dimensión" solo se infiere, igual que con un hecho.                                                                                                                                                                                                        |
| partición       | partición         | fuente (solo para joins)          | Un objeto para la administración de datos que contiene un subconjunto de datos en una tabla                                         | Las tablas de un modelo tabular pueden tener muchas particiones y deben tener al menos una. El hecho de Metric View, como se mencionó anteriormente, se define únicamente como una fuente, pero las uniones de Metric View también tienen una propiedad `source`, que actúa, en términos generales, como una partición |
| campo           | columna           | campo                                                | Una columna en una tabla                                                                                                            |                                                                                                                                                                                                                                                                                                                                        |
| medida          | medida            | medida                                               | Un valor cuantitativo que se agrega conforme a la lógica de negocio del modelo                                                      | Las medidas en un modelo tabular se escriben en DAX y, en una Metric View, en SQL                                                                                                                                                                                                                                                      |
| join o relación | relación          | join.on o join.using | Una correspondencia entre los campos clave de dos tablas: una clave externa en una y una clave principal en la otra | Las relaciones son objetos explícitos en un modelo tabular y se definen implícitamente como una propiedad del objeto `join` en el YAML de Metric View                                                                                                                                                                                  |

## Referencias adicionales

- @semantic-bridge
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- @semantic-bridge-how-tos
- [Documentación de la API de Metric View](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
