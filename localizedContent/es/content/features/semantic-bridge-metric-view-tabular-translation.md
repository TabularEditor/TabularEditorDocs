---
uid: semantic-bridge-metric-view-tabular-translation
title: Metric View to Tabular translation
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

# Metric View to Tabular translation

<!--
SUMMARY: Describes the process and specifics of translating a Metric View to a TOM model.
-->

> [!NOTE]
> The Semantic Bridge is in public preview.
> The 3.25.0 release supports Metric View v0.1 metadata, and the 3.26.2 release supports Metric View v1.1 metadata.
> Limitations are described below.

This page describes how translation works when importing a Metric View definition into a Tabular model.

## Proceso de traducción

La traducción de una Metric View a un modelo tabular se realiza en varios pasos:

1. Leer el YAML del disco
2. Deserializar el YAML
3. Validar que el YAML deserializado represente una Metric View válida
4. If it is a valid Metric View, store it as the currently loaded Metric View, similar to how there is a loaded Tabular model that you interact with.
   If it is not a valid Metric View, the process stops here and diagnostic messages are available.
5. Analizar la Metric View e intentar transformarla en una representación intermedia
6. Intentar transformar la representación intermedia en un modelo tabular

The import GUI handles all of this for you, but you can also use C# scripts to customize different steps of the process and operate on the Metric View programmatically, similarly to how you are used to doing with a Tabular model.
En concreto, puedes

- load a Metric View from disk with [`SemanticBridge.MetricView.Load`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Load%2A): loading makes it available in C# scripts as [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model), but does not import the structure into the Tabular model
- deserialize a Metric View from a string with [`SemanticBridge.MetricView.Deserialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Deserialize%2A): similar to loading, the model is available as [`SemanticBridge.MetricView.Model`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Model), but is not imported
- save a Metric View to disk with [`SemanticBridge.MetricView.Save`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Save%2A)
- serialize a Metric View to a string with [`SemanticBridge.MetricView.Serialize`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Serialize%2A).
- validate a Metric View using a system that is similar to the [Best Practice Analyzer](xref:best-practice-analyzer) with [`SemanticBridge.MetricView.Validate`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate%2A)
  - you can create your own custom validation rules with [`SemanticBridge.MetricView.MakeValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRule%2A) and its simpler versions
- import a Metric View to Tabular with [`SemanticBridge.MetricView.ImportToTabularFromFile`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.ImportToTabularFromFile%2A), which does the exact same as the import GUI, or [`SemanticBridge.MetricView.ImportToTabular`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.ImportToTabular%2A), which is similar, but operates on the currently loaded Metric View, rather than reading one from disk.

### Per object translation notes

The four items below, `View`, `Join`, `Field`, and `Measure`, are the core objects of a Metric View definition that become TOM objects.
Other metadata in the Metric View definition are either ignored or modify exactly how these objects are translated.

> [!NOTE]
> The translation is performed upon the Metric View object model, so we discuss everything in these terms.
> See [the Metric View object model docs](xref:semantic-bridge-metric-view-object-model) for specifics of the object model and how it aligns to the YAML spec.

#### `View` translation

- translate
  - `Source`: becomes the single fact table, named 'Fact' in the TOM model
  - `Comment`: becomes TOM `Model.Description`
  - `Joins`: see `Join`
  - `Fields`: see `Field`
  - `Measures`: see `Measure`
- do not translate
  - `Filter`
  - `Materialization`

Si `Source` es una referencia de tabla o vista de 3 partes, se traduce a una partición M que accede al objeto SQL por su nombre.
Si `Source` no es una referencia de tabla o vista de 3 partes, se traduce a una partición M con una consulta SQL incrustada, siendo la totalidad de la cadena `Source` la propia consulta SQL.

The `Filter` property is ignored for purposes of translation;
if you need the logic included in `Filter`, you will have to manually add this.
The `Filter` expression applies to all queries against the Metric View, and so a full automated translation would require joining all tables named in `Joins` in generated M code in TOM.

Any defined `Materialization` is ignored for the purposes of translation;
these are query optimization metadata for executing queries on Databricks and not relevant to a TOM model.

#### `Join` translation

- translated
  - `Name`: becomes TOM table name
  - `Source`: becomes M partition on table
  - `On`: becomes a TOM relationship
  - `Joins`: become additional TOM tables
  - `Cardinality`
- untranslated
  - `Using`
  - `Rely`

`Join`s each become a TOM table, with an M partition defined according to the same rules as for the `View.Source` property.

`On` equijoins (e.g., `source.fk = dimTable.pk`) become TOM relationships.
Any other predicate in an `On` property is not translated as a relationship.

Trees of `Join`s in a Metric View are translated as TOM tables in a chain of N:1 relationships, where the cardinalities are supported (see note on cardinality below).
This represents a snowflake model schema.

`Cardinality` of `ManyToOne` is translated as a TOM N:1 relationship.
An unpopulated `Cardinality` or a `Join` without this property set is treated as `ManyToOne` by default, in accordance with [Metric View docs](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#joins).
Other values for `Cardinality` are not yet supported for translation as a relationship.

`Using` joins are not supported for translation; these do not yield a TOM relationship.

`Rely` is not propagated into the TOM model in any way.

In cases where a TOM relationship is not created, we still create a TOM table and translate all Metric View `Fields` to TOM columns as described elsewhere.

> [!NOTE]
> Databricks has recently introduced a new pattern using `OneToMany` cardinality against multiple `Join` sub-trees to implement a multi-fact model.
> We do not yet translate this pattern fully: we bring over all tables, fields, and measures, but do not create all relationships.
> A diagnostic warning is shown when importing a model following this pattern.

#### `Field` translation

- translated
  - `Name`
  - `DisplayName`
  - `Expr`
  - `Comment`: becomes TOM column's `Description` property
  - `Format`: becomes TOM column's `FormatString` property; see section below on `Format` translation
- untranslated
  - `Synonyms`

Each `Field` becomes a column in the Tabular model.

The TOM column's `Name` is `Field.DisplayName` if it is populated,
otherwise it is `Field.Name`.

Si `Expr` es una referencia de campo no calificada, se agrega a la tabla de hechos.
If the `Expr` is a qualified reference (e.g., `table.field`),
then it is added to the table created for the `Join` with the same name as the table-part of the qualified reference;
if the table-part is `source`, it is added to the fact table.
In both the qualified and unqualified field reference cases,
the field is added as a [`TOMWrapper.DataColumn`](xref:TabularEditor.TOMWrapper.DataColumn).
If the `Expr` is a SQL expression,
then it is added as [`TOMWrapper.CalculatedColumn`](xref:TabularEditor.TOMWrapper.CalculatedColumn).
When the `Expr` is a SQL expression, we extract all field references;
if all field references share the same table-part,
then we add it to the table created for that `Join`,
otherwise we add it to the fact table.
We identify all field references in the SQL expression and add those to the Tabular model as `DataColumn`s if they do not already exist as a Metric View `Field`.
We do not translate SQL expressions for `Field.Expr` properties;
the SQL expression is included as a comment in the DAX expression for the `CalculatedColumn`.
Depende del usuario traducir estas expresiones.

Algunos ejemplos:

| `Expr`                                                | Traducido como tipo | Añadido a la tabla | Nota                                                                                              |
| ----------------------------------------------------- | ------------------- | ------------------ | ------------------------------------------------------------------------------------------------- |
| `field1`                                              | `DataColumn`        | `'Fact'`           | las referencias de campo sin calificar son equivalentes a las calificadas con `source`            |
| `source.field2`                                       | `DataColumn`        | `'Fact'`           | `source` es una referencia a la propiedad `View.Source`, también conocida como la tabla de hechos |
| `dimCustomer.key`                                     | `DataColumn`        | `'dimCustomer'`    | debe haber un `Join` cuya propiedad `Name` sea `dimCustomer`                                      |
| `CONCAT(dimCustomer.FirstName, dimCustomer.LastName)` | `CalculatedColumn`  | `'dimCustomer'`    | todas las partes de tabla del nombre cualificado se refieren al mismo nombre                      |
| `CONCAT(dimGeo.Country, dimCustomer.Address)`         | `CalculatedColumn`  | `'Fact'`           | hay varias partes de tabla diferentes                                                             |

#### `Measure` translation

- translated
  - `Name`
  - `DisplayName`
  - `Expr`: becomes TOM measure's `Expression` property; see section below on SQL -> DAX translation
  - `Comment`: becomes TOM measure's `Description` property
  - `Format`: becomes TOM measure's `FormatString` property; see section below on `Format` translation
- untranslated
  - `Synonyms`
  - `Window`

Todas las medidas se agregan a la tabla de hechos.

The TOM measure's `Name` is the Metric View's `Measure.DisplayName` if it exists,
otherwise it is the Metric View's `Measure.Name`.

`Expr` is translated to DAX or passed through as a comment in cases where we cannot automatically translate the measure.
We identify all field references in the SQL expression and add those to the Tabular model as `DataColumn`s if they do not already exist as a Metric View `Field`.

Window specifications are not translated and cause fallback to a DAX comment, regardless of the SQL in `Expr`.

### `Format` translation

A Metric View `Format` is translated to a TOM `FormatString` on the object that carries it.
The target is a VBA-style format string, as used in TOM models.
The translation is best-effort:
if we can create a format string that exactly matches the configuration of the `Format`, then we do so;
if we cannot create an exact equivalent, then we fall back to an approximate equivalent and emit a warning you can review after import.

Currency, percentage, and number formats translate cleanly:
currency becomes a currency-symbol prefix on a grouped numeric format,
percentage becomes a percent format that honors the declared decimal places,
and number honors the declared decimal places and group separator, with the scientific abbreviation becoming an exponential format.

Year-month-day dates translate cleanly to an ISO date format;
locale long-month and locale numeric-month dates translate cleanly to the `Long Date` and `Short Date` named formats;
and hour-minute and hour-minute-second times translate cleanly to the `Short Time` and `Long Time` named formats.

The remaining formats cannot be precisely translated and emit a warning:
the compact number abbreviation and the byte format fall back to a plain numeric format;
the locale short-month date falls back to `Long Date`;
the year-week date falls back to an ISO date;
and a combined date-and-time format falls back to an ISO composite.

### SQL -> DAX translation

Las Metric Views proporcionan una capa estructurada sobre expresiones SQL, por lo que parte de traducir una Metric View consiste en traducir SQL a DAX y M en el modelo tabular.
Las agregaciones admitidas son sum, count, distinct count, max, min y average.
Basic arithmetic, common counting patterns, measure references, and parenthesis precedence are all supported for SQL->DAX translation.

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

## Additional references

- @semantic-bridge
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- @semantic-bridge-how-tos
- [Metric View API docs](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
