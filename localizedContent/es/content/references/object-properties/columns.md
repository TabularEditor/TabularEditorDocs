---
uid: object-properties-columns
title: Propiedades de las columnas
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

# Propiedades de las columnas

<!--
SUMMARY: Reference for the properties of data columns, calculated columns, calculated table columns, and the Alternate Of and Variation objects that belong to columns.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

En esta página se enumeran las propiedades de los tres tipos de columnas y de los dos objetos que pertenecen a una columna: Alternate Of y Variation. Para las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

Una tabla contiene tres tipos de columnas:

- una **columna de datos** obtiene sus valores de las particiones de la tabla, por ejemplo, de una consulta de Power Query (M) o de una consulta SQL
- una **columna calculada** obtiene sus valores de una expresión DAX que se evalúa para cada fila de la tabla
- una **columna de tabla calculada** es una columna de una tabla calculada, definida por la expresión DAX de la tabla calculada

En [Propiedades de todas las columnas](#properties-of-all-columns) se describen las propiedades que comparten los tres tipos. En las secciones siguientes se enumeran las propiedades específicas de cada tipo de columna.

## Propiedades de todas las columnas

Estas propiedades se aplican a las columnas de datos, a las columnas calculadas y a las columnas de tablas calculadas.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Carpeta de visualización](xref:object-properties-common#display-folder)
- [Oculto](xref:object-properties-common#hidden)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Propiedades modificadas](xref:object-properties-common#changed-properties)
- [Identificador DAX](xref:object-properties-common#dax-identifier)
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
| `None`           | No resumas. Power BI lo muestra como **No resumir**.                                         |
| `Sum`            | La suma de los valores.                                                                                      |
| `Min`            | El valor más pequeño.                                                                                        |
| `Max`            | El valor más grande.                                                                                         |
| `Count`          | El número de valores.                                                                                        |
| `Average`        | El promedio de los valores.                                                                                  |
| `DistinctCount`  | El número de valores distintos.                                                                              |

En Power BI Desktop, una columna numérica con `Default` se comporta como `SUM`: se muestra con el icono Σ en el panel **Datos** y se agrega a un Visual como **SUM de** la columna. Una columna de texto con `Default` no se resume. Excel ignora esta propiedad y una tabla dinámica solo realiza agregaciones mediante medidas.

Establece `None` en las columnas numéricas que no tengan sentido sumar, como claves, años, números de teléfono o precios unitarios; de lo contrario, los autores de Reports obtendrán totales como la suma de todos los ID de cliente. Consulta @kb.bpa-do-not-summarize-numeric.

`SummarizeBy` no tiene efecto en DAX ni en las medidas explícitas. Cuando `DiscourageImplicitMeasures` está habilitado en el modelo (consulta @object-properties-model), Power BI no crea medidas implícitas y esta propiedad no tiene efecto. El C# Script @script-create-sum-measures-from-columns crea una medida `SUM` para cada columna seleccionada y oculta la columna.

### Alignment

`Alignment` · Alineación · Opciones

La alineación horizontal de los valores de la columna en las herramientas cliente que la admitan.

| Valor            | Significado                                                                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Predeterminado` | La herramienta cliente es quien decide. La mayoría de las herramientas alinean los números a la derecha y el texto a la izquierda. |
| `Izquierda`      | Alinear a la izquierda.                                                                                                                            |
| `Derecha`        | Alinear a la derecha.                                                                                                                              |
| `Centro`         | Centrar los valores.                                                                                                                               |

Power BI ignora esta propiedad. Los Visuales de tabla y matriz siempre alinean el texto a la izquierda y los números a la derecha; el resto de alineaciones se configuran en las opciones de formato del Visual. En una tabla dinámica de Excel conectada al modelo, las columnas alineadas a la derecha y al centro también se muestran con la alineación predeterminada.

### Alternativa de

`AlternateOf` · AlternateOf · Opciones · nivel de compatibilidad 1460+

Hace que esta columna forme parte de una agregación definida por el usuario. Una tabla de agregación contiene datos preagregados, por ejemplo, ventas por cliente y producto. `AlternateOf` asigna esta columna a la columna de la tabla de detalle a la que sustituye y establece cómo se agregaron los valores; cuando puede, el motor responde a las consultas usando la tabla de agregación más pequeña.

La propiedad aparece en el nivel de compatibilidad 1460 o superior y permanece vacía hasta que agregues una Alternativa de. En Tabular Editor 2 y Tabular Editor 3, haz clic en el botón **...** de la propiedad vacía o haz clic con el botón derecho en la propiedad y elige **Agregar Alternativa de**. El nuevo Alternate Of tiene `Summarization` `Sum`. Expande la propiedad para establecer las propiedades descritas en [Alternativa de](#alternate-of-1). Para quitarla, haz clic con el botón derecho en la propiedad y elige **Quitar Alternativa de**. Para ver una guía paso a paso, consulta @user-defined-aggregations.

El C# Script @script-implement-user-defined-aggregations prepara la tabla de detalle de una tabla de agregación seleccionada y configura `AlternateOf` en sus columnas numéricas.

### Categoría de datos

`DataCategory` · string · Opciones

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

Si el motor deduce por sí mismo el tipo de datos de la columna e ignora el valor de `DataType`. Importa sobre todo para las columnas calculadas y las columnas de tablas calculadas, cuyo tipo de datos se deriva de la expresión DAX.

En Tabular Editor 3, cuando este valor es `true` en una columna calculada o en una columna de una tabla calculada, `DataType` es de solo lectura y Tabular Editor lo actualiza a partir de la expresión a medida que la editas, sin conexión a un servidor. Establécelo en `false` para elegir tú mismo el tipo de datos. Cuando vuelves a establecerlo en `true` en una columna de una tabla calculada, `DataType` se restablece al tipo de datos de la columna de la que la expresión obtiene sus valores.

<!-- TODO (not verifiable from TE3 source): document the effect of this property on data columns. TE3 has no special handling for data columns. -->

### Imagen predeterminada

`IsDefaultImage` · bool · Opciones

Marca la columna como la imagen que representa una fila de la tabla, por ejemplo, una foto del producto. Es una de las configuraciones de _comportamiento de tabla_ que usaba Power View. Ningún cliente actual lo usa: Power View se ha retirado, Power BI lo ignora y las tablas dinámicas de Excel ignoran la configuración de comportamiento de tabla.

### Etiqueta predeterminada

`IsDefaultLabel` · bool · Opciones

Marca la columna como la etiqueta que identifica una fila de la tabla para los usuarios, por ejemplo, el nombre del producto. Es una configuración de comportamiento de tabla que usaba Power View. Ningún cliente actual lo usa. Power View y Power BI Q&A la admitían, y ambos han sido retirados.

### Clave

`IsKey` · bool · Opciones

Marca la columna como la clave de la tabla, la columna cuyos valores identifican cada fila. Una tabla tiene como máximo una columna clave: cuando estableces `IsKey` en `true` en una columna, Tabular Editor lo establece en `false` en las demás columnas de la tabla y deja `IsUnique` e `IsNullable` sin cambios. La columna clave no puede contener valores duplicados ni en blanco, por lo que una actualización que cargue duplicados falla.

Cuando marcas una tabla como tabla de fechas en Power BI, `IsKey` se establece en la columna de fecha y la `DataCategory` de la tabla se establece en `Time`.

La regla BPA @kb.bpa-date-table-exists marca un modelo que no tiene ningún calendario, ninguna tabla con `DataCategory` `Time` ni ninguna columna clave de tipo `DateTime`.

### Admite valores nulos

`IsNullable` · bool · Opciones

Indica si la columna puede contener valores en blanco (nulos). El valor predeterminado es `true`. Si se establece en `false`, la actualización falla cuando el origen devuelve un valor vacío, lo que sirve como comprobación de la calidad de los datos. Una columna clave nunca permite valores en blanco, sea cual sea el valor de esta propiedad.

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
| `Leer`    | Los usuarios asignados al rol pueden ver y consultar la columna.                                                                                                                                                |

Puedes cambiar el valor de cada rol. Cuando eliges `None` o `Read`, Tabular Editor agrega un permiso de columna para esa columna al permiso de tabla del rol para la tabla de la columna, y crea ese permiso de tabla si el rol aún no tiene uno. Cuando eliges `Default`, Tabular Editor quita el permiso de columna. También puedes establecer los mismos valores en el rol, en **Permisos de columna de OLS** (consulta @object-properties-security). Consulta @data-security-setup-ols.

No puedes combinar la seguridad a nivel de filas de un rol con la seguridad a nivel de objetos de otro. Cuando un usuario es miembro de una combinación de roles como esa, el motor devuelve un error en tiempo de consulta.

En SQL Server 2025 Analysis Services, se ha observado que la configuración se combina así:

- `Default` sigue a la tabla: cuando el permiso de tabla del rol es `Read`, la columna es visible, y cuando es `None`, se oculta toda la tabla, incluida esta columna
- una columna no puede ser menos restrictiva que su tabla, y el motor rechaza `Read` en una columna cuya tabla es `None`
- cuando un usuario es miembro de varios roles que usan OLS, los permisos se acumulan, y el usuario puede ver una tabla o columna si alguno de los roles lo permite
- la seguridad a nivel de filas y la seguridad a nivel de objetos en el mismo rol funcionan juntas; por ejemplo, un filtro de filas en una tabla que el rol oculta con OLS sigue filtrando las tablas relacionadas

## Columna de datos

Una columna de datos obtiene sus valores de las particiones de la tabla; en un modelo de Power BI, normalmente de una consulta de Power Query (M). La columna tiene las propiedades descritas en [Properties of all columns](#properties-of-all-columns) y la siguiente.

En Tabular Editor 3, el asistente @import-tables crea columnas de datos con sus tipos de datos y asignaciones de columnas de origen, y **Actualizar esquema de la tabla** las actualiza cuando cambia el origen.

### Columna de origen

`SourceColumn` · cadena · Básico

El nombre de la columna en el resultado de la consulta de la partición de la que esta columna obtiene sus valores. Debe coincidir con el nombre que devuelve la consulta. Si no coincide, por ejemplo, después de que alguien haya cambiado el nombre de una columna en Power Query, la actualización falla.

Los valores de `Name` y `SourceColumn` de la columna son independientes, por lo que puedes cambiar el nombre de la columna en el modelo sin cambiar la consulta, y viceversa. Cambiar el nombre de una columna en Tabular Editor deja `SourceColumn` sin cambios. Con la corrección automática de fórmulas activada, Tabular Editor actualiza las expresiones DAX que hacen referencia a la columna renombrada. Consulta @formula-fix-up-dependencies.

Toda columna de datos necesita una columna de origen. Consulta @kb.bpa-data-column-source.

Cuando se cambia el nombre de una columna en la fuente, **Actualizar esquema de tabla** en Tabular Editor 3 indica que se ha quitado una columna y se ha agregado otra nueva. Combina ambas en una sola actualización de `SourceColumn` para que las fórmulas DAX que usan la columna sigan funcionando.

## Columna calculada

Una columna calculada obtiene sus valores de una expresión DAX que se evalúa una vez por cada fila de la tabla al actualizarla. El motor almacena el resultado igual que los valores de una columna de datos, lo que consume memoria y permite leer los valores con rapidez. Usa una columna calculada para los valores por los que segmentas, filtras o agrupas, y una medida para los valores que solo agregas.

La columna tiene las propiedades de [Propiedades de todas las columnas](#properties-of-all-columns) y las que se indican a continuación. Para agregar una columna calculada en Tabular Editor 3, consulta @creating-and-testing-dax.

### Expresión

`Expression` · cadena · Opciones

La expresión DAX que calcula el valor de cada fila, por ejemplo:

```dax
Sales[Quantity] * Sales[Unit Price]
```

La expresión se evalúa en un _contexto de fila_, por lo que hace referencia directamente a las columnas de la fila actual. Para obtener un valor de una tabla relacionada, usa [RELATED](https://dax.guide/related), por ejemplo `RELATED ( Product[Category] )`.

El motor vuelve a calcular la columna cuando se actualiza la tabla o cuando cambias la expresión y guardas el modelo en un servidor conectado. En Tabular Editor 3, edita la expresión en el **Editor de expresiones** del @dax-editor. La @table-preview muestra los valores calculados o **(Es necesario recalcular)** cuando la columna debe recalcularse primero.

### Contexto de expresión

`ExpressionContext` · ExpressionContext · Opciones · nivel de compatibilidad 1705+

Si la columna tiene un valor para todos o se evalúa por usuario.

| Valor         | Significado                                                                                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Standard`    | La opción predeterminada. La columna se calcula durante la actualización y tiene un valor por fila para todos los usuarios. |
| `UserContext` | La columna se evalúa por usuario y la expresión puede llamar a funciones como `USERPRINCIPALNAME`.                                          |

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

Si el nombre de la columna sigue el nombre definido en la expresión de la tabla calculada. Cuando es `true`, el motor y Tabular Editor 3 cambian el nombre de la columna para que coincida con la expresión, por ejemplo, cuando cambia la expresión. Ponlo en `false` para conservar el nombre que tú mismo le asignaste a la columna.

En Tabular Editor 3, `Name` es de solo lectura cuando `IsNameInferred` es `true`. Cuando vuelves a establecerlo en `true`, la columna toma el nombre de la columna que la expresión usa como origen, si existe.

Por ejemplo, un C# Script que crea un parámetro de campo establece `IsNameInferred` en `false` en sus columnas para conservar los nombres que les asigna. Consulta @create-field-parameter.

## Alternativa de

Un objeto Alternate Of se encuentra en una columna de una tabla de agregación. Asigna esa columna a una columna, o a toda la tabla, de la tabla de detalle que resume, y define cómo se agregaron los valores. Con estas asignaciones configuradas, el motor responde a una consulta desde la tabla de agregación cuando puede y omite la tabla de detalle, que suele ser mucho más grande y a menudo está en modo DirectQuery. Esta configuración se denomina _agregaciones definidas por el usuario_. Para ver una guía paso a paso, consulta @user-defined-aggregations.

Alternate Of requiere un nivel de compatibilidad 1460 o superior. No aparece como un objeto independiente en el **Explorador TOM**. Para establecer las propiedades siguientes, expande la propiedad `AlternateOf` de la columna en la **vista de propiedades**.

### Propiedades comunes

- [Anotaciones](xref:object-properties-common#annotations)
- [Tipo de objeto](xref:object-properties-common#object-type)

### Columna base

`BaseColumn` · Columna · Opciones

La columna de la tabla de detalle que esta columna agrega. Por ejemplo, la columna `Sales Amount` de una tabla `Sales Agg` tiene como columna base `Sales[Sales Amount]` con la agregación `Sum`.

Establece `BaseColumn` o `BaseTable`. Al establecer `BaseColumn`, se borra `BaseTable`.

### Tabla base

`BaseTable` · Tabla · Opciones

La tabla de detalles cuyas filas cuenta esta columna. Úsalo con `Summarization` `Count` para una columna que contenga el número de filas de detalle, lo que permite al motor responder a `COUNTROWS ( Sales )` desde la tabla de agregación.

Establece `BaseColumn` o `BaseTable`. Al establecer `BaseTable`, se borra `BaseColumn` y se establece `Summarization` en `Count`, y cambiar `Summarization` a cualquier otro valor borra `BaseTable`. La **vista de propiedades** solo muestra `BaseTable` cuando `Summarization` es `Count`.

### Columna

`Column` · Columna · Opciones · solo lectura

La columna de la tabla de agregación a la que pertenece este "Alternate Of". La **vista de propiedades** la oculta y puedes usarla en C# Script.

### Agregación

`Summarization` · SummarizationType · Opciones

Cómo se agregaron los valores de esta columna a partir de la columna base o la tabla base.

| Valor     | Significado                                                                                                                                                                                                                                                                     |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GroupBy` | Una columna de agrupación que contiene los mismos valores que la columna base. Obligatorio cuando la tabla de agregación no está relacionada con las tablas de dimensiones; por ejemplo, cuando la tabla de detalle es una tabla ancha y plana. |
| `Sum`     | La suma de la columna base.                                                                                                                                                                                                                                     |
| `Count`   | El número de filas de la tabla base, o el número de valores no en blanco de la columna base.                                                                                                                                                                    |
| `Min`     | El valor más pequeño de la columna base.                                                                                                                                                                                                                        |
| `Max`     | El valor más grande de la columna base.                                                                                                                                                                                                                         |

Para todos los tipos de agregación salvo `Count`, la columna debe tener el mismo tipo de datos que su columna base, por lo que un `Sum` de una columna base `Decimal` también es `Decimal`. Una columna `Count` debe ser un número entero (`Int64`), independientemente del tipo de datos de la columna base. Para que el motor pueda responder a `DISTINCTCOUNT` desde la tabla de agregación, agrega la columna con `GroupBy`, lo cual también funciona cuando la tabla de agregación está relacionada con las tablas de dimensiones. No existe un resumen de recuento distinto.

## Variación

Una variación es otro elemento que muestra una herramienta cliente cuando un usuario selecciona una columna. Power BI usa variaciones para la fecha/hora automática: para cada columna de fecha, Power BI Desktop crea una tabla de fechas oculta, una relación con ella y una variación para la columna de fecha. Cuando el autor de un Report selecciona la columna de fecha, Power BI muestra la **Jerarquía de fechas** de la tabla de fechas oculta.

Las variaciones aparecen sobre todo en modelos de Power BI y Fabric. Tabular Editor muestra la propiedad `Variations` de una columna con un nivel de compatibilidad 1400 o superior; también en los modelos de Analysis Services. Si tu modelo tiene su propia tabla de fechas, desactiva la fecha/hora automática en Power BI Desktop para eliminar las tablas de fechas ocultas y sus variaciones. Consulta @kb.bpa-remove-auto-date-table.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

### Columna principal

`Column` · Columna · Básico · solo lectura

La columna a la que pertenece esta variación.

### Columna predeterminada

`DefaultColumn` · Columna · Opciones

Una columna de la tabla relacionada que la herramienta cliente muestra cuando un usuario selecciona la columna principal. Establece esta propiedad o `DefaultHierarchy`. Las variaciones que Power BI Desktop crea para la fecha/hora automática usan `DefaultHierarchy` y dejan `DefaultColumn` en blanco.

<!-- TODO (not verifiable from TE3 source): confirm whether Default Column and Default Hierarchy are mutually exclusive, and when Power BI uses Default Column. TE3 doesn't enforce either rule. -->

### Jerarquía predeterminada

`DefaultHierarchy` · Jerarquía · Opciones

Una jerarquía de la tabla relacionada que la herramienta cliente muestra cuando el usuario selecciona la columna principal. Para la fecha/hora automática, esta es la **Jerarquía de fechas** de la tabla oculta `LocalDateTable_...`.

### Predeterminado

`IsDefault` · bool · Opciones

Indica si esta es la variación predeterminada de la columna. Cuando una columna tiene más de una variación, la herramienta cliente muestra la predeterminada cuando el usuario selecciona la columna.

### Relación

`Relationship` · relación · Opciones

La relación desde la columna principal hasta la tabla que contiene la columna predeterminada o la jerarquía predeterminada. Para la fecha/hora automática, es la relación desde la columna de fecha hasta su tabla de fechas oculta.
