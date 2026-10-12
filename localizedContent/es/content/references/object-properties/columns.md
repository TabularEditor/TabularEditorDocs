---
uid: object-properties-columns
title: Column properties
author: Jeroen ter Heerdt
updated: 2026-10-09
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

# Column properties

<!--
SUMMARY: Reference for the properties of data columns, calculated columns, calculated table columns, and the Alternate Of and Variation objects that belong to columns.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

This page lists the properties of the three kinds of columns and of the two objects that belong to a column, Alternate Of and Variation. For properties that most objects share, see @object-properties-common.

A table contains three kinds of columns:

- a **data column** gets its values from the table's partitions, for example from a Power Query (M) query or a SQL query
- a **calculated column** gets its values from a DAX expression that's evaluated for each row of the table
- a **calculated table column** is a column of a calculated table, defined by the calculated table's DAX expression

[Properties of all columns](#properties-of-all-columns) describes the properties that the three kinds share. The sections after it list the properties that are specific to one kind of column.

## Properties of all columns

These properties apply to data columns, calculated columns and calculated table columns.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Display Folder](xref:object-properties-common#display-folder)
- [Hidden](xref:object-properties-common#hidden)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Changed Properties](xref:object-properties-common#changed-properties)
- [DAX identifier](xref:object-properties-common#dax-identifier)
- [Mensaje de error](xref:object-properties-common#error-message)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Estado](xref:object-properties-common#state)
- [Etiqueta de linaje](xref:object-properties-common#lineage-tag)
- [Etiqueta de linaje de origen](xref:object-properties-common#source-lineage-tag)
- [Nombres traducidos](xref:object-properties-common#translated-names)
- [Descripciones traducidas](xref:object-properties-common#translated-descriptions)
- [Carpetas de visualización traducidas](xref:object-properties-common#translated-display-folders)
- [Sinónimos](xref:object-properties-common#synonyms)
- [Mostrado en perspectiva](xref:object-properties-common#shown-in-perspective)

### Tipo de datos

`DataType` · DataType · Básico

El tipo de datos de los valores de la columna. Determina cómo el motor almacena los valores y qué funciones y operadores DAX los admiten. Ambas columnas de una relación deben tener el mismo tipo de datos.

| Valor        | Significado                                                                                                                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `String`     | Texto. Se denomina **Texto** en Power BI.                                                                                                                        |
| `Int64`      | Un número entero de 64 bits. Se denomina **Número entero** en Power BI.                                                                                          |
| `Double`     | Un número de punto flotante de 64 bits. Se denomina **Número decimal** en Power BI. Los totales pueden mostrar pequeñas diferencias de redondeo. |
| `Decimal`    | Un número de punto fijo con cuatro cifras decimales. Se llama **Número decimal fijo** en Power BI. Úsalo para importes monetarios.               |
| `DateTime`   | Una fecha y una hora. Power BI lo muestra como **Fecha**, **Hora** o **Fecha/hora**, según la cadena de formato.                                                 |
| `Boolean`    | `TRUE` o `FALSE`.                                                                                                                                                                |
| `Binario`    | Datos binarios, como los bytes de una imagen. DAX no puede usar valores binarios y Power BI no carga columnas binarias.                                          |
| `Automático` | Solo para uso interno.                                                                                                                                                           |
| `Unknown`    | El valor inicial de una columna nueva. El motor lo reemplaza por el tipo de datos real cuando la columna se guarda en el servidor.                               |
| `Variant`    | Un valor que puede ser de distintos tipos. Se usa solo para medidas.                                                                                             |

La **vista de propiedades** muestra algunos valores con un nombre más largo; por ejemplo, `Int64` como **Entero / Número entero (int64)** y `Decimal` como **Moneda / Número decimal fijo (decimal)**. La lista desplegable enumera todos los valores de la tabla, incluidos `Automático`, `Desconocido` y `Variant`, y los acepta todos. Para una columna de datos, elige uno de los siete primeros valores.

Para una columna de datos, el tipo de datos debe coincidir con los datos que devuelve la consulta de la partición; de lo contrario, el motor convierte los valores durante la actualización. Si una conversión falla, por ejemplo, con un texto que no es un número, la actualización falla. Cambiar el tipo de datos en Tabular Editor no modifica la consulta de la partición: si cambias una columna de `String` a `Int64`, haz también que la consulta devuelva números enteros, por ejemplo, cambiando el tipo en Power Query.

En las columnas calculadas y las columnas de tablas calculadas, el tipo de datos viene determinado por la expresión. Consulta [Tipo de datos inferido](#data-type-inferred).

La regla @kb.bpa-relationship-same-datatype del Best Practice Analyzer (BPA) marca las relaciones entre columnas que tienen tipos de datos diferentes.

### Cadena de formato

`FormatString` · cadena · Básico

El formato que las herramientas cliente aplican cuando muestran los valores de la columna, por ejemplo, `#,0`, `0.00%` o `yyyy-mm-dd`. La sintaxis es la misma que la de la función DAX [FORMAT](https://dax.guide/format). Las consultas DAX devuelven el valor sin formato. El formato también se aplica a las medidas implícitas que Power BI crea cuando el autor del Report arrastra una columna numérica a un Visual.

Las columnas numéricas y de fecha visibles sin una cadena de formato muestran valores sin procesar, como `1234567.891` o una fecha con un componente de hora. Consulta @kb.bpa-format-string-columns.

### Ordenar por columna

`SortByColumn` · Columna · Básico

Otra columna de la misma tabla cuyos valores establecen el orden de los valores de esta columna. Por ejemplo, ordena la columna `Month Name` por la columna `Month Number` para mostrar los meses en orden de calendario.

Cada valor de esta columna debe tener exactamente un valor en la columna de ordenación. Por ejemplo, `January` debe tener siempre el número de mes `1`. Si un valor tiene más de un valor de ordenación, el motor informa de un error cuando la columna se actualiza o se recalcula.

> [!NOTE]
> Cuando un Report agrupa por una columna que tiene una columna de ordenación, Power BI también agrupa por la columna de ordenación. Como resultado, `CALCULATE ( [Sales], REMOVEFILTERS ( 'Date'[Month Name] ) )` mantiene el filtro en `'Date'[Month Number]` y devuelve un resultado sin cambios. Quita el filtro de ambas columnas o de toda la tabla.

El C# Script @script-create-date-table crea una tabla de fechas y establece `SortByColumn` en las columnas de nombres.

### Resumir por

`SummarizeBy` · Función de agregado · Básico

La agregación que las herramientas cliente aplican cuando el autor del Report arrastra la columna a un Visual como valor, sin una medida. Power BI lo denomina _resumen predeterminado_ y la medida que crea sobre la marcha, _medida implícita_.

| Valor            | Significado                                                                                                                  |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `Predeterminado` | La herramienta cliente lo decide. Las columnas numéricas se suman y las demás no se resumen. |
| `None`           | Don't summarize. Power BI shows it as **Don't summarize**.                                   |
| `Sum`            | The sum of the values.                                                                                       |
| `Min`            | The smallest value.                                                                                          |
| `Max`            | The largest value.                                                                                           |
| `Count`          | The number of values.                                                                                        |
| `Average`        | The average of the values.                                                                                   |
| `DistinctCount`  | The number of distinct values.                                                                               |

In Power BI Desktop, a numeric column with `Default` behaves like `Sum`: it shows with the Σ icon in the **Data** pane and is added to a visual as **Sum of** the column. A text column with `Default` isn't summarized. Excel ignores this property, and a PivotTable only aggregates through measures.

Set `None` on numeric columns that aren't meaningful to add up, such as keys, years, phone numbers or unit prices, or report authors get totals such as the sum of all customer IDs. See @kb.bpa-do-not-summarize-numeric.

`SummarizeBy` has no effect on DAX or on explicit measures. When `DiscourageImplicitMeasures` is enabled on the model (see @object-properties-model), Power BI creates no implicit measures and this property has no effect. The C# script @script-create-sum-measures-from-columns creates a `SUM` measure for each selected column and hides the column.

### Alignment

`Alignment` · Alignment · Options

The horizontal alignment of the column's values in client tools that support it.

| Valor     | Significado                                                                                                          |
| --------- | -------------------------------------------------------------------------------------------------------------------- |
| `Default` | The client tool decides. Most tools align numbers to the right and text to the left. |
| `Left`    | Align to the left.                                                                                   |
| `Right`   | Align to the right.                                                                                  |
| `Center`  | Center the values.                                                                                   |

Power BI ignores this property. Table and matrix visuals always align text to the left and numbers to the right, and you set other alignments in the formatting options of the visual. In an Excel PivotTable connected to the model, right- and center-aligned columns also show with the default alignment.

### Alternate Of

`AlternateOf` · AlternateOf · Options · compatibility level 1460+

Makes this column part of a user-defined aggregation. An aggregation table holds pre-aggregated data, for example sales per customer and product. `AlternateOf` maps this column to the column of the detail table that it stands in for and sets how the values were aggregated, and the engine then answers queries from the smaller aggregation table when it can.

The property appears at compatibility level 1460 or higher and stays empty until you add an Alternate Of. In Tabular Editor 2 and Tabular Editor 3, click the **...** button of the empty property, or right-click the property and choose **Add Alternate Of**. The new Alternate Of has `Summarization` `Sum`. Expand the property to set the properties described under [Alternate Of](#alternate-of-1). To remove it, right-click the property and choose **Remove Alternate Of**. For a walkthrough, see @user-defined-aggregations.

The C# script @script-implement-user-defined-aggregations sets up the detail table for a selected aggregation table and configures `AlternateOf` on its numeric columns.

### Data Category

`DataCategory` · string · Options

El tipo de valor que contiene la columna, que las herramientas cliente utilizan para tratar la columna de forma especial. Por ejemplo, Power BI coloca en un mapa una columna con la categoría `City`, muestra como imagen una columna con la categoría `ImageUrl` y muestra como un enlace en el que se puede hacer clic una columna con la categoría `WebUrl`. Déjalo vacío para una columna normal.

En Tabular Editor 3, la lista desplegable muestra todas las categorías que define el protocolo, en orden alfabético, y también puedes escribir cualquier otro valor. El valor no se valida, así que escríbelo exactamente como aparece en la lista. Power BI usa estas categorías:

| Valor             | Se muestra en Power BI como | Uso                                                                                                            |
| ----------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `Address`         | Dirección                   | Direcciones de calle.                                                                          |
| `City`            | Ciudad                      | Nombres de ciudades.                                                                           |
| `County`          | Condado                     | Nombres de condados.                                                                           |
| `StateOrProvince` | Estado o provincia          | Nombres de estados o provincias.                                                               |
| `PostalCode`      | Código postal               | Códigos postales o ZIP.                                                                        |
| `Country`         | País/región                 | Nombres o códigos de países o regiones.                                                        |
| `Continent`       | Continente                  | Nombres de continentes.                                                                        |
| `Place`           | Lugar                       | Nombres o descripciones de una ubicación que no encajan en ninguna otra categoría.             |
| `Latitude`        | Latitud                     | Latitud en grados decimales, por ejemplo `51.5072`.                                            |
| `Longitude`       | Longitud                    | Longitud en grados decimales, por ejemplo `-0.1276`.                                           |
| `WebUrl`          | URL web                     | Enlaces en los que los usuarios pueden hacer clic.                                             |
| `ImageUrl`        | URL de imagen               | Las direcciones URL de imágenes que los Visual muestran como imágenes.                         |
| `Barcode`         | Código de barras            | Códigos de barras que la aplicación móvil de Power BI escanea para aplicar FILTER a un Report. |

Las categorías geográficas indican a los Visual de mapa qué tipo de ubicación es un valor; por ejemplo, que `Paris` es una `City`.

La lista desplegable muestra dos de las categorías como `WebURL` e `ImageURL` y no tiene ninguna entrada de `Barcode`. Power BI no distingue entre mayúsculas y minúsculas, por lo que tanto `ImageUrl` como `ImageURL` muestran el valor como una imagen en un Visual de tabla, y tanto `WebUrl` como `WebURL` lo muestran como un enlace. El Tabular Object Model (TOM) almacena el valor exactamente como lo escribe. Power BI acepta `Barcode`, pero un Visual de tabla muestra el valor como texto sin formato; solo lo usan las aplicaciones móviles de Power BI.

El protocolo define muchas más categorías, por ejemplo `Id`, `Image` y categorías de tiempo como `Years` y `Months`, que usaban las herramientas más antiguas. Power BI ignora la mayoría de ellas. La lista desplegable también muestra `PaddedDateTableDates`, una categoría que usa Power BI y que el protocolo no define. Power BI Desktop escribe las categorías de tiempo en las columnas de sus tablas automáticas de fecha/hora: `PaddedDateTableDates` en la columna de fecha, y `Years`, `Quarters`, `QuarterOfYear`, `Months`, `MonthOfYear` y `DayOfMonth` en las demás columnas.

<!-- TODO (not verifiable from TE3 source): whether Power BI uses these column categories for anything, or only writes them. -->

Para marcar una tabla como tabla de fechas, establece la propiedad `DataCategory` de la tabla en `Time` (consulta @object-properties-tables) y establece `IsKey` en `true` en la columna de fecha de la tabla.

### Orden de visualización

`DisplayOrdinal` · int · Opciones

Un número que las herramientas cliente pueden usar para ordenar las columnas de una tabla, por ejemplo `10`, `20`, `30`. Solo importa el orden relativo, así que dejar huecos permite insertar una columna más adelante.

Power BI lo ignora y el panel **Datos** de Power BI Desktop muestra las columnas en orden alfabético, independientemente de su `DisplayOrdinal`. Para agrupar columnas allí, usa carpetas de visualización.

### Sugerencia de codificación

`EncodingHint` · EncodingHintType · Opciones · nivel de compatibilidad 1400+

Una sugerencia para el motor sobre cómo comprimir una columna numérica en memoria. Sin una sugerencia, el motor elige una codificación cuando carga los datos por primera vez y más tarde puede volver a codificar la columna durante la actualización, lo que lleva tiempo. Con una sugerencia, el motor empieza con la codificación sugerida.

| Valor     | Significado                                                                                                                                                                                                                                            |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Default` | Lo decide el motor.                                                                                                                                                                                                                    |
| `Hash`    | Almacena cada valor distinto una sola vez, en un diccionario, y hace referencia a él por su posición. Va bien para columnas con pocos valores distintos o con valores muy separados entre sí, como las columnas clave. |
| `Value`   | Almacena los propios valores, reducidos mediante un poco de aritmética. Va bien para columnas numéricas que agregas y cuyos valores están próximos entre sí, como cantidades o importes.                               |

El motor aún puede elegir una codificación distinta, y las columnas de texto siempre usan codificación hash. Establece una sugerencia solo cuando hayas visto, por ejemplo en el Analizador VertiPaq, que la codificación del motor ralentiza la actualización o hace que el modelo sea grande.

### Columnas de «Agrupar por»

`GroupByColumns` · GroupingColumnCollection · Opciones · de solo lectura · nivel de compatibilidad 1400+

Otras columnas de la misma tabla que el motor también usa para agrupar cada vez que una consulta utiliza esta columna. Las filas que tienen el mismo valor en esta columna permanecen separadas cuando sus valores en una columna de agrupación son distintos.

Power BI usa esto para los parámetros de campo. La columna con los nombres de campo se agrupa por la columna con las referencias de campo, lo que mantiene en filas separadas dos campos con el mismo nombre para mostrar. Consulta @create-field-parameter.

Los clientes MDX, como Excel, tratan estas columnas como una clave compuesta, por lo que no puedes colocar en una tabla dinámica una columna con columnas de agrupación sin las columnas por las que está agrupada.

La propiedad aparece en los modelos de Power BI y Fabric con nivel de compatibilidad 1400 o superior. Puedes cambiar las columnas de la colección: en Tabular Editor 3, haz clic en el botón **...** para abrir un cuadro de diálogo con las demás columnas de la tabla y seleccionar las columnas por las que agrupar. TOM guarda las columnas en el objeto `RelatedColumnDetails` de la columna, y Tabular Editor elimina ese objeto cuando quitas la última columna.

### Disponible en MDX

`IsAvailableInMDX` · bool · Opciones

Si el motor crea una _jerarquía de atributos_ para la columna, necesaria para las consultas MDX. El valor predeterminado es `true`. Las tablas dinámicas de Excel usan MDX y solo pueden colocar una columna en filas o columnas cuando esta propiedad es `true`. Power BI usa DAX y funciona sin jerarquías de atributos.

Establecerlo en `false` en columnas ocultas que las consultas MDX no usan, como las claves externas y las columnas que solo se usan en medidas, ahorra memoria y tiempo de actualización. Manténlo en `true` para las columnas usadas en jerarquías, como columna de ordenación, en variaciones o en calendarios, y para las columnas que necesitan los usuarios de Excel. Consulta @kb.bpa-set-isavailableinmdx-false y @kb.bpa-set-isavailableinmdx-true-necessary. La regla @kb.bpa-hide-foreign-keys marca las columnas de clave externa que no están ocultas.

### Tipo de datos inferido

`IsDataTypeInferred` · bool · Opciones

Si el motor deduce por sí mismo el tipo de datos de la columna e ignora el valor de `DataType`. It mostly matters for calculated columns and calculated table columns, whose data type follows from the DAX expression.

In Tabular Editor 3, while this is `true` on a calculated column or calculated table column, `DataType` is read-only and Tabular Editor updates it from the expression as you edit it, without a connection to a server. Set it to `false` to pick a data type yourself. When you set it back to `true` on a calculated table column, `DataType` resets to the data type of the column that the expression gets its values from.

<!-- TODO (not verifiable from TE3 source): document the effect of this property on data columns. TE3 has no special handling for data columns. -->

### Default Image

`IsDefaultImage` · bool · Options

Marks the column as the image that represents a row of the table, for example a product photo. It's one of the _table behavior_ settings that Power View used. No current client uses it: Power View is retired, Power BI ignores it and Excel PivotTables ignore table behavior settings.

### Default Label

`IsDefaultLabel` · bool · Options

Marks the column as the label that identifies a row of the table to users, for example the product name. It's a table behavior setting that Power View used. No current client uses it. Power View and Power BI Q&A both supported it and are both retired.

### Clave

`IsKey` · bool · Options

Marks the column as the key of the table, the column whose values identify each row. A table has at most one key column: when you set `IsKey` to `true` on a column, Tabular Editor sets it to `false` on the other columns of the table and leaves `IsUnique` and `IsNullable` unchanged. The key column can't contain duplicate or blank values, so a refresh that loads duplicates fails.

When you mark a table as a date table in Power BI, `IsKey` is set on the date column and the table's `DataCategory` is `Time`.

The BPA rule @kb.bpa-date-table-exists flags a model that has no calendar, no table with `DataCategory` `Time` and no `DateTime` key column.

### Nullable

`IsNullable` · bool · Options

Whether the column can contain blank (null) values. The default is `true`. Si se establece en `false`, la actualización falla cuando el origen devuelve un valor vacío, lo que sirve como comprobación de la calidad de los datos. Una columna clave nunca permite valores en blanco, sea cual sea el valor de esta propiedad.

### Único

`IsUnique` · bool · Opciones

Indica si la columna contiene solo valores únicos. El motor lo aplica y un valor duplicado hace que falle la actualización de una columna de datos. En una columna de una tabla calculada, el propio guardado falla, porque el motor vuelve a calcular la tabla de inmediato. El error dice "La columna 'Key' de la tabla 'Sales' contiene un valor duplicado 'a' y esto no está permitido en columnas del lado uno de una relación de varios a uno ni en columnas que se usan como clave principal de una tabla". Actívala solo en columnas cuya unicidad esté garantizada, como la clave de una tabla de dimensiones.

Para ver los valores distintos de una columna en un modelo en modo conectado, ejecuta el C# Script @script-display-unique-column-values.

### Mantener filas únicas

`KeepUniqueRows` · bool · Opciones

Una configuración de comportamiento de tabla de Power View pensada para mantener separadas las filas que comparten un valor en esta columna cuando sus claves difieren; por ejemplo, dos clientes con el mismo nombre. Cuando es `false`, esas filas se agrupan por valor.

Ningún cliente actual la tiene en cuenta. Power BI la ignora y, en una tabla dinámica de Excel sobre SQL Server 2025 Analysis Services, dos clientes con el mismo nombre se muestran en una sola fila tanto si `KeepUniqueRows` es `true` como si es `false`. Para mostrarlos por separado, haz que los valores sean únicos, por ejemplo añadiendo el número de cliente al nombre.

### Tipo de proveedor del origen

`SourceProviderType` · string · Opciones

El tipo de datos de la columna en el Data source, en los términos propios del Data source, por ejemplo `nvarchar` o `WChar`. El motor puede usarlo para generar consultas contra el origen en modo DirectQuery. Tabular Editor 3 nunca lo rellena, tampoco cuando importa una tabla, así que solo tiene un valor si se lo asignas tú o alguna otra herramienta. La mayoría de los modelos, incluidos los de Power BI, lo dejan vacío.

<!-- TODO (not verifiable from TE3 source): confirm which other tools fill in Source Provider Type (for example the Visual Studio table import wizard) and in which format (OLE DB type names or SQL type names). -->

### Comportamiento de indexación de cadenas

`StringIndexingBehavior` · IndexingBehavior · Opciones · nivel de compatibilidad 1706+

Indica si el motor crea un índice en una columna de texto y si lo guarda para reutilizarlo después de reiniciar.

| Valor      | Significado                                                                                                                          |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `Off`      | No se crea ningún índice.                                                                                            |
| `Auto`     | La opción predeterminada. Crea el índice cuando sea necesario, sin guardarlo.                        |
| `Explicit` | Crea y guarda el índice solo cuando se ejecuta una actualización de tipo `RefreshIndex`.                             |
| `Full`     | Crea y guarda el índice durante una actualización completa, un recálculo o una actualización de tipo `RefreshIndex`. |

En Power BI Desktop, cuyo motor admite el nivel de compatibilidad 1706, el motor acepta `Off` y `Auto` y rechaza `Explicit` y `Full` con el error "Persist String Index feature is disabled". Las versiones recientes de la biblioteca TOM solo permiten valores distintos de `Auto` a partir del nivel de compatibilidad 1707.

<!-- TODO (not verifiable from TE3 source): document what the string index is used for (text search such as CONTAINSSTRING?) and when Explicit and Full become available. -->

### Comportamiento de la indexación de texto completo

`FullTextIndexingBehavior` · IndexingBehavior · Opciones · nivel de compatibilidad 1708+

Indica si el motor crea un índice de texto completo en una columna de texto y lo guarda. El índice de texto completo habilita las funciones DAX `TEXTCONTAINS` y `TEXTSIMILARITY`. El valor predeterminado es `Off`.

| Valor      | Significado                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------------------- |
| `Off`      | La opción predeterminada. No se crea ningún índice de texto completo.    |
| `Auto`     | La biblioteca TOM no describe este valor para la indexación de texto completo.           |
| `Explicit` | Crea y guarda el índice solo cuando se ejecuta una actualización de tipo `RefreshIndex`. |
| `Full`     | Crea y guarda el índice durante la actualización.                                        |

<!-- TODO (not verifiable from TE3 source): what Auto does for full-text indexing, and which engines support compatibility level 1708. -->

### Posición del detalle de la tabla

`TableDetailPosition` · int · Opciones

Agrega la columna al _conjunto de campos predeterminado_ de la tabla; es decir, las columnas que una herramienta cliente muestra cuando un usuario agrega toda la tabla a un Report o profundiza para ver los detalles. Un número positivo incluye la columna y las columnas aparecen en orden ascendente según este número. El valor predeterminado es `-1`, lo que excluye la columna. Power View y **Mostrar detalles** en Excel usaban el conjunto de campos predeterminado.

Excel ya no lo usa para el desglose: **Mostrar detalles** en una tabla dinámica de Excel devuelve las columnas de la tabla independientemente del valor de `TableDetailPosition`. Para elegir las columnas del desglose, establece `DefaultDetailRowsExpression` en la tabla (consulta @object-properties-tables) o `DetailRowsExpression` en una medida (consulta @object-properties-measures).

### Variaciones

`Variations` · VariationCollection · Opciones · de solo lectura

Las variaciones de esta columna. Una variación es otro elemento que una herramienta cliente muestra cuando un usuario selecciona esta columna. Power BI usa variaciones para _fecha y hora automáticas_. Consulta [Variation](#variation).

### Seguridad a nivel de objeto

`ObjectLevelSecurity` · ColumnOLSIndexer · Traducciones, Perspectivas, Seguridad · de solo lectura · nivel de compatibilidad 1400+ · _acceso directo a_ los permisos de columna de cada rol

La configuración de seguridad a nivel de objetos (OLS) de esta columna en cada rol del modelo. La propiedad aparece en el nivel de compatibilidad 1400 o superior cuando el modelo tiene al menos un rol. Expándela para ver una entrada por rol, con uno de estos valores:

| Valor     | Significado                                                                                                                                                                                                                     |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Default` | Ninguna configuración específica para la columna. La columna sigue la configuración de su tabla en el rol. En TOM, el rol no tiene ningún permiso de columna para esta columna. |
| `None`    | Los usuarios del rol no pueden ver ni consultar la columna. Para ellos, la columna no existe y los Visuales que la usen muestran un error.                                                      |
| `Read`    | Users in the role can see and query the column.                                                                                                                                                                 |

You can change the value for each role. When you pick `None` or `Read`, Tabular Editor adds a column permission for the column to the role's table permission for the column's table, and creates that table permission if the role doesn't have one yet. When you pick `Default`, Tabular Editor removes the column permission. You can also set the same values on the role, under **OLS Column Permissions** (see @object-properties-security). See @data-security-setup-ols.

You can't combine row-level security from one role with object-level security from another. When a user is a member of such a combination of roles, the engine returns an error at query time.

Observed on SQL Server 2025 Analysis Services, the settings combine like this:

- `Default` follows the table: when the role's table permission is `Read`, the column is visible, and when it's `None`, the whole table is hidden, including this column
- a column can't be less restrictive than its table, and the engine rejects `Read` on a column whose table is `None`
- when a user is a member of several roles that all use OLS, the permissions add up, and the user can see a table or column if any of the roles allows it
- row-level and object-level security in the same role work together, for example a row filter on a table that the role hides with OLS still filters the related tables

## Data column

A data column gets its values from the table's partitions, in a Power BI model usually a Power Query (M) query. The column has the properties under [Properties of all columns](#properties-of-all-columns) and the one below.

In Tabular Editor 3, the @import-tables wizard creates data columns with their data types and source column mappings, and **Update table schema** updates them when the source changes.

### Source Column

`SourceColumn` · string · Basic

The name of the column in the result of the partition query that this column gets its values from. It must match the name that the query returns. If it doesn't, for example after someone renamed a column in Power Query, the refresh fails.

The column's `Name` and `SourceColumn` are separate, so you can rename the column in the model without changing the query and the other way round. Renaming a column in Tabular Editor leaves `SourceColumn` unchanged. With formula fix-up turned on, Tabular Editor updates the DAX expressions that refer to the renamed column. See @formula-fix-up-dependencies.

Every data column needs a source column. See @kb.bpa-data-column-source.

When a column is renamed in the source, **Update table schema** in Tabular Editor 3 reports a removed and a new column. Combine the two into a single `SourceColumn` update to keep the DAX formulas that use the column working.

## Calculated column

A calculated column gets its values from a DAX expression that's evaluated once for each row of the table when the table is refreshed. The engine stores the result like the values of a data column, which takes memory and makes the values fast to read. Use a calculated column for values that you slice, filter or group by, and a measure for values that you only aggregate.

The column has the properties under [Properties of all columns](#properties-of-all-columns) and the ones below. To add a calculated column in Tabular Editor 3, see @creating-and-testing-dax.

### Expresión

`Expression` · string · Options

The DAX expression that calculates the value for each row, for example:

```dax
Sales[Quantity] * Sales[Unit Price]
```

The expression is evaluated in a _row context_, so it refers to the columns of the current row directly. To get a value from a related table, use [RELATED](https://dax.guide/related), for example `RELATED ( Product[Category] )`.

The engine recalculates the column when the table is refreshed, or when you change the expression and save the model to a connected server. In Tabular Editor 3, you edit the expression in the **Expression Editor** of the @dax-editor. The @table-preview shows the calculated values, or **(Calculation needed)** when the column must be recalculated first.

### Contexto de expresión

`ExpressionContext` · ExpressionContext · Options · compatibility level 1705+

Whether the column has one value for everyone or is evaluated per user.

| Valor         | Significado                                                                                                                                |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `Standard`    | La opción predeterminada. The column is calculated during refresh and has one value per row for all users. |
| `UserContext` | The column is evaluated per user, and the expression can call functions such as `USERPRINCIPALNAME`.                       |

Las columnas calculadas estándar, las tablas calculadas, los filtros de seguridad a nivel de filas y las relaciones no pueden usar una columna de contexto de usuario. Consulta @user-context-calculated-columns.

## Columna de tabla calculada

Una columna de tabla calculada es una columna de una tabla calculada. La expresión DAX de la tabla define qué columnas existen, sus tipos de datos y sus valores; para agregar o quitar columnas, cambia esa expresión.

Tabular Editor 3 analiza la expresión en cuanto la cambias y agrega, quita y actualiza las columnas para que coincidan con ella. Esto funciona sin conexión a un servidor, por lo que las columnas también se mantienen actualizadas en un modelo que editas sin conexión. Tabular Editor 2 solo actualiza las columnas cuando guardas el modelo en una base de datos a la que estás conectado; después de guardar, recarga desde el servidor las columnas de la tabla. Cuando editas un archivo de modelo en Tabular Editor 2, las columnas se mantienen tal como están; puedes agregar una con **Crear nuevo > Columna de tabla calculada** y no puedes eliminarlas.

Puedes cambiar las propiedades de visualización de la columna, como `FormatString`, `IsHidden` y `SortByColumn`. Para cambiar el nombre de la columna, primero establece `IsNameInferred` en `false`. La columna tiene las propiedades descritas en [Properties of all columns](#properties-of-all-columns) y las que se indican a continuación.

### Columna de origen

`SourceColumn` · string · Básico · de solo lectura

El nombre de la columna en el resultado de la expresión de la tabla calculada de la que esta columna obtiene sus valores. Tabular Editor 3 la establece cuando analiza la expresión, y el motor la establece cuando el modelo se guarda en un servidor. Cambiar el nombre de la columna no cambia este valor, lo que mantiene el vínculo entre la columna y la expresión.

El valor tiene uno de estos dos formatos:

- `Table[Column]`, sin comillas alrededor del nombre de la tabla, para una columna que la expresión toma de otra tabla; por ejemplo, `Date[Year]` para `SUMMARIZE ( 'Date', 'Date'[Year] )`
- `[Column]` para una columna que crea la expresión; por ejemplo, `[Sales Amount]` para `ADDCOLUMNS ( ..., "Sales Amount", ... )`, o `[Value]` para un constructor de tablas o `UNION`

### Nombre inferido

`IsNameInferred` · bool · Opciones

Si el nombre de la columna sigue el nombre definido en la expresión de la tabla calculada. Cuando es `true`, el motor y Tabular Editor 3 cambian el nombre de la columna para que coincida con la expresión, por ejemplo, cuando cambia la expresión. Set it to `false` to keep a name that you gave the column yourself.

In Tabular Editor 3, `Name` is read-only while `IsNameInferred` is `true`. When you set it back to `true`, the column gets the name of the column that the expression takes it from, if there is one.

A C# script that creates a field parameter, for example, sets `IsNameInferred` to `false` on its columns to keep the names it gives them. See @create-field-parameter.

## Alternate Of

An Alternate Of object sits on a column of an aggregation table. It maps that column to a column, or to the whole table, of the detail table that it summarizes, and sets how the values were aggregated. With these mappings in place, the engine answers a query from the aggregation table when it can and skips the detail table, which is usually much larger and often in DirectQuery mode. This setup is called _user-defined aggregations_. For a walkthrough, see @user-defined-aggregations.

Alternate Of needs compatibility level 1460 or higher. It doesn't appear as a separate object in the **TOM Explorer**. To set the properties below, expand the column's `AlternateOf` property in the **Properties view**.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Object Type](xref:object-properties-common#object-type)

### Base Column

`BaseColumn` · Column · Options

The column in the detail table that this column aggregates. For example, the `Sales Amount` column of a `Sales Agg` table has base column `Sales[Sales Amount]` with summarization `Sum`.

Set either `BaseColumn` or `BaseTable`. Setting `BaseColumn` clears `BaseTable`.

### Base Table

`BaseTable` · Table · Options

The detail table whose rows this column counts. Use it with `Summarization` `Count` for a column that holds the number of detail rows, which lets the engine answer `COUNTROWS ( Sales )` from the aggregation table.

Set either `BaseColumn` or `BaseTable`. Setting `BaseTable` clears `BaseColumn` and sets `Summarization` to `Count`, and changing `Summarization` to any other value clears `BaseTable`. The **Properties view** only shows `BaseTable` when `Summarization` is `Count`.

### Columna

`Column` · Column · Options · read-only

The column of the aggregation table that this Alternate Of belongs to. The **Properties view** hides it, and you can use it in C# scripts.

### Summarization

`Summarization` · SummarizationType · Options

How the values in this column were aggregated from the base column or base table.

| Valor     | Significado                                                                                                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `GroupBy` | A group-by column that holds the same values as the base column. Required when the aggregation table isn't related to the dimension tables, for example when the detail table is a wide, flat table. |
| `Sum`     | The sum of the base column.                                                                                                                                                                                          |
| `Count`   | The number of rows of the base table, or the number of non-blank values of the base column.                                                                                                                          |
| `Min`     | The smallest value of the base column.                                                                                                                                                                               |
| `Max`     | The largest value of the base column.                                                                                                                                                                                |

For all summarizations except `Count`, the column must have the same data type as its base column, so a `Sum` of a `Decimal` base column is also `Decimal`. A `Count` column must be a whole number (`Int64`), whatever the data type of the base column. To let the engine answer `DISTINCTCOUNT` from the aggregation table, add the column with `GroupBy`, which also works when the aggregation table is related to the dimension tables. No distinct count summarization exists.

## Variation

A variation is something else that a client tool shows when a user picks a column. Power BI uses variations for auto date/time: for each date column, Power BI Desktop creates a hidden date table, a relationship to it and a variation on the date column. When a report author picks the date column, Power BI shows the **Date Hierarchy** of the hidden date table.

Variations mostly occur in Power BI and Fabric models. Tabular Editor shows the `Variations` property of a column at compatibility level 1400 or higher, in Analysis Services models too. If your model has its own date table, turn off auto date/time in Power BI Desktop to remove the hidden date tables and their variations. See @kb.bpa-remove-auto-date-table.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Parent Column

`Column` · Column · Basic · read-only

The column this variation belongs to.

### Default Column

`DefaultColumn` · Column · Options

A column of the related table that the client tool shows when a user picks the parent column. Set either this or `DefaultHierarchy`. The variations that Power BI Desktop creates for auto date/time use `DefaultHierarchy` and leave `DefaultColumn` empty.

<!-- TODO (not verifiable from TE3 source): confirm whether Default Column and Default Hierarchy are mutually exclusive, and when Power BI uses Default Column. TE3 doesn't enforce either rule. -->

### Default Hierarchy

`DefaultHierarchy` · Hierarchy · Options

A hierarchy of the related table that the client tool shows when a user picks the parent column. For auto date/time, this is the **Date Hierarchy** of the hidden `LocalDateTable_...` table.

### Predeterminado

`IsDefault` · bool · Options

Whether this is the default variation of the column. When a column has more than one variation, the client tool shows the default one when a user picks the column.

### Relación

`Relationship` · Relationship · Options

The relationship from the parent column to the table that holds the default column or default hierarchy. For auto date/time, it's the relationship from the date column to its hidden date table.
