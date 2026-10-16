---
uid: object-properties-model
title: Propiedades del modelo
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

# Propiedades del modelo

<!--
SUMMARY: Reference for the properties of the model object, such as culture, collation, default storage mode and Direct Lake behavior.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Esta página trata las propiedades del objeto del modelo. Cada entrada indica el nombre de la propiedad en el Tabular Object Model (TOM), su tipo y su categoría. Para las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

## Modelo

El modelo es el objeto raíz de un modelo semántico. Todas las tablas, relaciones, roles, perspectivas y configuraciones regionales forman parte de él. Sus propiedades se aplican a todo el modelo, como la configuración regional usada para el formato, el modo de almacenamiento predeterminado y las opciones que cambian el comportamiento de Power BI y del motor. Para verlas, selecciona el nodo **Modelo** en la parte superior del **Explorador TOM**.

Muchas propiedades del modelo requieren un nivel de compatibilidad mínimo, y algunas se aplican solo a modelos de Power BI y Fabric o solo a Analysis Services. La vista de propiedades oculta las propiedades que no se aplican al modelo actual. Consulta @update-compatibility-level.

Las propiedades de la categoría **Opciones de acceso a datos** controlan cómo el motor de Power Query (M), también llamado motor de mashup, obtiene los datos durante la actualización. Se aplican solo a los datos que el modelo carga mediante M, es decir, Data sources de tipo origen de datos estructurado y particiones de M. No tienen efecto en los Data sources heredados (de proveedor) ni en las consultas DirectQuery. De forma predeterminada, en TOM las tres opciones están en `false`, y Power BI Desktop habilita `LegacyRedirects` y `ReturnErrorValuesAsNull` en los modelos nuevos.

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM reference only says these are "options for the M data engine". Confirm that they have no effect on provider data sources and DirectQuery, and that the Power BI service honors all three. -->

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Nombres traducidos](xref:object-properties-common#translated-names)
- [Descripciones traducidas](xref:object-properties-common#translated-descriptions)

### Base de datos

`Database` · Base de datos · Básico · de solo lectura

La base de datos que contiene el modelo. Expande la propiedad para ver y cambiar la configuración de la base de datos, como el **nivel de compatibilidad**, que determina las características y propiedades que admite el modelo.

En Tabular Editor 3, puedes editar estos ajustes en `Database`:

- **Nombre** e **ID**: el nombre y el ID de la base de datos. Cambiarlos no tiene ningún efecto en una base de datos ya implementada.
- **nivel de compatibilidad** y **Modo de compatibilidad**. Cuando estás conectado a un servidor, Tabular Editor 3 rechaza un nivel de compatibilidad que el servidor no admite.
- **Descripción**, **Comportamiento de caracteres Unicode** y **Visible**.

Estos ajustes son de solo lectura y solo muestran un valor cuando estás conectado a un servidor: **Versión**, **Tamaño estimado** (en MB), **Último procesamiento**, **Última actualización**, **Última actualización del esquema**, **Marca de tiempo de creación**, **Nombre del servidor** y **Versión del servidor**.

Tabular Editor 2 muestra los mismos ajustes en `Database`, excepto **Comportamiento de caracteres Unicode**, y muestra **Tamaño estimado** como `EstimatedSize`.

No puedes reducir el nivel de compatibilidad después de aumentarlo. Consulta @update-compatibility-level y @change-compatibility-mode. La regla de Best Practice Analyzer (BPA) @kb.bpa-powerbi-latest-compatibility marca los modelos de Power BI que no usan el nivel de compatibilidad más reciente.

### Habilitar Fast Combine

`FastCombine` · bool · Opciones de acceso a datos · nivel de compatibilidad 1400+

Cuando se establece en `true`, Power Query ignora los niveles de privacidad de los Data sources. Equivale a la opción **Ignorar los niveles de privacidad y posiblemente mejorar el rendimiento** en Power BI Desktop.

Los niveles de privacidad impiden que Power Query envíe datos de un origen a otro, por ejemplo, al plegar valores de un archivo de Excel en una consulta SQL. Con los niveles de privacidad aplicados, la actualización puede ser más lenta o fallar con un error `Formula.Firewall` cuando una consulta combina orígenes. Habilita esta opción solo cuando confíes en todos los Data sources del modelo.

### Habilitar redirecciones heredadas

`LegacyRedirects` · bool · Opciones de acceso a datos · nivel de compatibilidad 1400+

Cuando es `true`, Power Query sigue una redirección de una dirección HTTPS a una dirección HTTP, y los datos viajan sin cifrar. El valor predeterminado de TOM es `false`. Power BI Desktop lo habilita en los modelos nuevos.

### Devolver valores de error como nulos

`ReturnErrorValuesAsNull` · bool · Opciones de acceso a datos · nivel de compatibilidad 1400+

Cuando es `true`, un valor que provoca un error durante la actualización, por ejemplo texto que no se puede convertir a un número, se carga como un valor en blanco. Cuando es `false`, el valor predeterminado de TOM, el error hace que la actualización falle. Power BI Desktop lo habilita en los modelos nuevos. Con `true`, los valores no válidos se convierten en valores en blanco sin generar un error, lo que oculta problemas de calidad de los datos.

### Intercalación

`Collation` · string · Opciones

Las reglas que usa el motor para comparar y ordenar texto, expresadas como un nombre de intercalación de Windows. La intercalación determina si las comparaciones distinguen mayúsculas y minúsculas, y si distinguen acentos. Por ejemplo, con `Latin1_General_CI_AS` (no distingue mayúsculas y minúsculas), `apple` y `Apple` son el mismo valor en una columna, en las relaciones y en las comparaciones de DAX. Con `Latin1_General_CS_AS` (distingue mayúsculas y minúsculas), son valores distintos.

Cuando se deja en blanco, se aplica la intercalación predeterminada del servidor o del servicio. Configúrala cuando los datos dependan de distinguir entre mayúsculas y minúsculas; por ejemplo, en códigos de producto en los que `ab1` y `AB1` sean productos distintos, o para un modelo de Direct Lake en un Warehouse de Fabric que distinga entre mayúsculas y minúsculas (consulta @direct-lake-guidance).

Configura la intercalación cuando crees el modelo o antes de agregar cualquier tabla. La API de TOM tiene operaciones independientes, `UpdateCollation` y `UpdateCulture`, para cambiar la intercalación y la configuración regional de un modelo que ya existe en un servidor. En SQL Server Analysis Services y Azure Analysis Services, después de un cambio así, debes volver a establecer las credenciales del Data source.

Tabular Editor no usa esas operaciones. Si cambias `Collation` en la vista de propiedades y guardas en una base de datos que ya contiene tablas, el cambio se rechaza y aparece el error "Las propiedades de configuración regional y de intercalación del objeto Model solo se pueden cambiar antes de que se haya creado cualquier otro objeto". SQL Server 2025 Analysis Services, Azure Analysis Services y el servicio de Power BI devuelven este error, y en SQL Server 2025 Analysis Services la base de datos conserva su intercalación anterior.

### Configuración regional

`configuración regional` · string · Opciones

El idioma y la región del modelo, en forma de nombre de configuración regional, como `en-US` o `de-DE`. El motor la utiliza para dar formato a los valores; por ejemplo, el separador decimal y el formato de fecha que usa la función `FORMAT` cuando no se le especifica una configuración regional, y para ordenar y comparar texto de forma sensible al idioma. También es el idioma de los nombres y descripciones no traducidos del modelo. Las traducciones para otros idiomas se representan como configuraciones regionales en la colección `Cultures`. Selecciona la configuración regional en la lista de la vista de propiedades.

Según Microsoft, no se puede cambiar la configuración regional una vez que la utiliza un objeto secundario. En la práctica, esto se aplica en cuanto el modelo contiene cualquier otro objeto, como una tabla. Tabular Editor 3 acepta el cambio en la vista de propiedades, y el motor lo rechaza al guardar con el error "Las propiedades de configuración regional y de intercalación del objeto Model solo se pueden cambiar antes de que se haya creado cualquier otro objeto". SQL Server 2025 Analysis Services, el servicio de Power BI y Azure Analysis Services devuelven este error. Para cambiar la configuración regional de un modelo que ya existe en un servidor, la API de TOM tiene una operación `UpdateCulture` independiente.

### Configuración regional de la consulta de origen

`SourceQueryCulture` · string · Opciones · nivel de compatibilidad 1520+

La configuración regional que usa Power Query para interpretar valores durante la actualización, por ejemplo cuando convierte el texto `1.234,5` en un número o `03/04/2026` en una fecha. Es la misma configuración que **Configuración regional para importar**, dentro de **Configuración regional**, en Power BI Desktop.

Establécela cuando los datos de origen usen un formato distinto de `configuración regional`, por ejemplo un modelo en `en-US` que carga archivos CSV escritos en `de-DE`. Si está vacío, Power Query usa `configuración regional`. Si se establece, tiene prioridad sobre `configuración regional` durante la actualización. Por ejemplo, en un modelo con `configuración regional` establecida en `en-US`, `Date.FromText ( "01/02/2024" )` devuelve el 2 de enero de 2024 cuando `SourceQueryCulture` está vacío, y el 1 de febrero de 2024 cuando es `nl-NL`. En un modelo nuevo guardado desde Power BI Desktop, contiene la **Configuración regional para importar** del archivo, por ejemplo `en-NL`.

### Modo predeterminado

`DefaultMode` · ModeType · Opciones

El modo de almacenamiento de las particiones cuyo `Mode` está establecido en `Default`. Las particiones con un modo explícito conservan su modo cuando cambia esta propiedad. Consulta @object-properties-partitions.

| Valor         | Significado                                                                                                                                                                                                             |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Import`      | Los datos se cargan en la memoria del modelo durante la actualización. Las consultas no se envían al origen de datos.                                                                   |
| `DirectQuery` | Los datos permanecen en el origen. Cada consulta se traduce en una consulta dirigida al origen de datos.                                                                                |
| `DirectLake`  | Los datos se leen directamente de las tablas Delta en OneLake. Solo para Fabric, nivel de compatibilidad 1604 o superior. Consulta @direct-lake-sql-model. |

El tipo de modo de almacenamiento también admite los valores `Dual`, `Push` y `Default`. Tabular Editor 3 solo admite `Import`, `DirectQuery` o `DirectLake` para el modelo, y `DirectLake` solo en las ediciones que admiten Direct Lake. `Default` se aplica solo a las particiones, donde significa "usar el `DefaultMode` del modelo".

En Analysis Services, establece `DefaultMode` en `DirectQuery` para convertir todo el modelo en un modelo DirectQuery. Power BI Desktop establece el modo en cada partición.

Para convertir tablas Import a Direct Lake en OneLake, utiliza el script @script-convert-import-to-dlol.

### Vista de datos predeterminada

`DefaultDataView` · DataViewType · Opciones

Para los modelos DirectQuery en Analysis Services: las particiones que el motor usa para responder a las consultas. Las particiones de muestra contienen un subconjunto de los datos y se usan al diseñar un modelo DirectQuery en Visual Studio. Las particiones con `DataView` establecido en `Default` heredan esta configuración.

| Valor     | Significado                                                                                                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Full`    | Las consultas usan las particiones cuyo `DataView` es `Full` o `Default`. Use esta opción para modelos en memoria y para modelos DirectQuery implementados. |
| `Sample`  | Las consultas usan las particiones cuyo `DataView` es `Sample` o `Default`, lo cual resulta útil mientras se diseña el modelo.                                              |
| `Default` | Solo es válido en particiones, donde significa "usar el `DefaultDataView` del modelo".                                                                                      |

Power BI no usa vistas de datos.

SQL Server 2025 Analysis Services acepta `Sample` en el nivel de compatibilidad 1700. Una tabla con una partición `DirectQuery` y particiones `Import` cuyo `DataView` es `Sample` se guarda sin errores.

<!-- TODO (not verifiable from TE3 source): whether the engine still uses sample partitions anywhere at compatibility level 1400 and higher (the save is accepted, the effect isn't observable). -->

### Medida predeterminada

`DefaultMeasure` · Medida · Opciones · nivel de compatibilidad 1400+

La medida que usan los clientes MDX, como Excel, cuando una consulta no especifica una medida. Selecciónela en la lista de medidas del modelo. Si está vacío, el motor elige la medida. Power BI y las consultas DAX no usan una medida predeterminada.

### Versión predeterminada del Data source de Power BI

`DefaultPowerBIDataSourceVersion` · PowerBIDataSourceVersion · Opciones · nivel de compatibilidad 1450+

El formato que Power BI usa para almacenar las definiciones de Data source en el modelo.

| Valor        | Significado                                                                                                                                                                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PowerBI_V1` | Formato heredado. Las expresiones M se almacenan directamente en las cadenas de conexión de los Data source.                                                                                                                               |
| `PowerBI_V2` | Formato heredado. Los Data source usan expresiones M compartidas.                                                                                                                                                                          |
| `PowerBI_V3` | El formato de _metadatos mejorados_, que admite operaciones básicas de administración de particiones. Requiere un nivel de compatibilidad 1465 o superior. Power BI Desktop lo usa en todos los modelos nuevos desde 2020. |

Power BI usa esta propiedad cuando convierte un modelo de un formato anterior. Para editar un modelo a través del punto de conexión XMLA se requiere `PowerBI_V3`. No lo cambies en un modelo que creó Power BI.

Cuando creas un modelo de Power BI con nivel de compatibilidad 1450 o superior, Tabular Editor 3 establece esta propiedad en `PowerBI_V3`. Tabular Editor 3 trata un modelo con `PowerBI_V3` y un modo de compatibilidad desconocido como un modelo de Power BI. Cuando abres un modelo de Power BI Desktop o un archivo .pbit con la configuración que limita la edición a las características que admite Power BI, un modelo que no es `PowerBI_V3` se abre en modo de solo lectura.

### Máximo predeterminado de conexiones de Data source

`DataSourceDefaultMaxConnections` · int · Opciones · nivel de compatibilidad 1510+

El número máximo de conexiones que el motor abre al mismo tiempo a un único Data source durante la actualización. El valor predeterminado es `10`. Se aplica a los Data sources cuyo `MaxConnections` es `-1` y a los Data sources que no tienen ningún objeto de Data source en el modelo; este es el caso de la mayoría de los modelos de Power BI, donde el Data source se define en M.

Auméntalo para actualizar más tablas o particiones en paralelo cuando el origen pueda soportar la carga, o redúcelo para proteger un origen con mucha carga. El servicio aún puede limitar el número de conexiones.

<!-- TODO (not verifiable from TE3 source): whether 0 or -1 have a special meaning on this property during refresh. SSAS 2025 accepts both on save without validation. -->

### Comportamiento de anulación de variables de Data source

`DataSourceVariablesOverrideBehavior` · DataSourceVariablesOverrideBehaviorType · Opciones · nivel de compatibilidad 1475+

Si un comando de actualización puede sobrescribir las variables de Data source del modelo, por ejemplo, para dirigir la actualización a otro servidor o a otra base de datos distinta de la definida en el modelo.

| Valor         | Significado                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| `No permitir` | Se rechazan las sobrescrituras de variables de Data source. |
| `Permitir`    | Se permiten las sobrescrituras de variables de Data source. |

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM reference only says "Queries won't allow / allow data source variables override". Confirm what "data source variables" are and which commands can override them (possibly related to @refresh-overrides). -->

### Comportamiento de Direct Lake

`DirectLakeBehavior` · DirectLakeBehavior · Opciones · nivel de compatibilidad 1604+

Qué hace un modelo Direct Lake cuando una consulta no se puede responder en modo Direct Lake; por ejemplo, cuando una tabla supera los límites establecidos de la capacidad, cuando una tabla es una vista SQL o cuando el punto de conexión de análisis SQL aplica seguridad a nivel de filas. En ese caso, el modelo puede _volver a_ DirectQuery contra el punto de conexión de análisis SQL.

| Valor             | Significado                                                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `Automatic`       | La consulta vuelve a DirectQuery cuando es necesario. Es la opción predeterminada.                         |
| `DirectLakeOnly`  | El fallback está deshabilitado. Una consulta que no puede ejecutarse en modo Direct Lake produce un error. |
| `DirectQueryOnly` | Todas las consultas usan DirectQuery. Use esta opción para probar o comparar el rendimiento.               |

El fallback suele ser mucho más lento que Direct Lake, y `DirectLakeOnly` convierte un fallback lento en un error. La propiedad solo se aplica a Direct Lake en SQL. Direct Lake en OneLake nunca vuelve a DirectQuery. Consulta @direct-lake-guidance y @direct-lake-sql-model.

### Comportamiento predeterminado de indexación de Direct Lake

`DefaultDirectLakeIndexingBehavior` · DirectLakeIndexingBehavior · Opciones · nivel de compatibilidad de versión preliminar

Cómo el motor crea y conserva los índices específicos de Direct Lake del modelo. La biblioteca TOM de Microsoft describe los valores de la siguiente manera:

| Valor            | Significado                                                                                                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Auto`           | Crea índices en memoria durante la carga de datos o la ejecución de consultas cuando es necesario, tal como lo describe la biblioteca TOM.                                     |
| `Explicit`       | El modelo crea y conserva el índice solo cuando se solicita mediante una operación de _actualizar índices_. Los demás tipos de actualización no crean índices. |
| `Full`           | El modelo crea y conserva índices como parte de las operaciones _refresh full_, _refresh calculate_ y _refresh indexes_.                                                       |
| `Predeterminado` | Use el comportamiento predeterminado del modelo para la creación y persistencia de índices.                                                                                    |

Esta propiedad requiere un nivel de compatibilidad en versión preliminar y Tabular Editor 3 no la muestra en la vista de propiedades. Puedes establecerla en un C# Script.

### Desaconsejar modelos compuestos

`DiscourageCompositeModels` · bool · Opciones · nivel de compatibilidad 1560+

Cuando se establece en `true`, los autores de Report no pueden crear un modelo compuesto sobre este modelo; es decir, no pueden conectarse a él con DirectQuery y combinarlo con otros datos. Cuando un autor de Report se conecta a un modelo publicado que tiene esta opción establecida en `true`, Power BI Desktop no muestra **Realizar cambios en este modelo** y el autor no puede agregar otros datos al Report. Solo es posible una conexión en vivo al modelo.

### Desaconsejar medidas implícitas

`DiscourageImplicitMeasures` · bool · Opciones · nivel de compatibilidad 1470+

Cuando es `true`, los autores de Report en Power BI no pueden crear _medidas implícitas_; es decir, la suma o el recuento que Power BI calcula al arrastrar una columna numérica a un Visual. Los autores de Report solo pueden usar las medidas definidas en el modelo, y la configuración `SummarizeBy` de las columnas deja de aplicarse en los Report.

Los modelos con grupos de cálculo deben tenerla habilitada, porque los grupos de cálculo solo se aplican a las medidas explícitas. Power BI Desktop y Tabular Editor 3 la activan cuando agregas un grupo de cálculo. Mientras el modelo contenga un grupo de cálculo, no puedes volver a establecerla en `false` en Tabular Editor 3.

### Desaconsejar medidas de Report

`DiscourageReportMeasures` · bool · Opciones

Cuando es `true`, Power BI desaconseja a los autores de Report que creen medidas de nivel de Report en Report con conexión en vivo a este modelo.

No puedes establecer esta propiedad. La biblioteca TOM solo lo permite en un nivel de compatibilidad interno (2147483647), por lo que Tabular Editor y cualquier otra herramienta que use TOM rechazan el cambio en todos los niveles de compatibilidad publicados. Tabular Editor 3 no la muestra en la vista de propiedades.

### Forzar nombres únicos

`ForceUniqueNames` · bool · Opciones · nivel de compatibilidad 1465+

Cuando es `true`, una medida no puede tener el mismo nombre que ninguna columna del modelo en ninguna tabla; de este modo, una referencia DAX como `[Amount]` siempre apunta a un único objeto. Cuando es `false`, una medida puede compartir nombre con una columna de otra tabla, y las referencias a columnas necesitan el nombre de la tabla para distinguirlas de la medida.

En SQL Server 2025 Analysis Services, el motor permite volver a establecerlo en `false`. Con `false`, una medida sigue sin poder tener el mismo nombre que una columna de su propia tabla. El motor rechaza establecerlo en `true` mientras una medida tenga el mismo nombre que una columna de otra tabla; por eso, primero cambia el nombre de esas medidas o columnas. La comparación no distingue entre mayúsculas y minúsculas.

Un modelo nuevo en Power BI Desktop tiene `ForceUniqueNames` establecido en `false`, y Power BI Desktop permite cambiarlo a cualquiera de los dos valores.

### Paralelismo máximo por consulta

`MaxParallelismPerQuery` · int · Opciones · nivel de compatibilidad 1569+

El número máximo de operaciones del motor de almacenamiento que el motor ejecuta en paralelo para una sola consulta DAX. Es especialmente importante en DirectQuery, donde cada operación es una consulta independiente al origen. Un valor más alto puede acelerar los Visuales cuando el origen puede soportar las consultas adicionales, y un valor más bajo protege el origen.

El valor predeterminado es `0`, lo que deja la decisión en manos del servicio. El servicio de Power BI acepta cualquier valor sin validarlo, incluidos números negativos y valores de hasta `100000`.

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM reference describes this as "maximum degree of parallelism for query in formula engine". Confirm that 0 means "let the service decide", the valid range, and whether it applies to Import models too. -->

### Paralelismo máximo por actualización

`MaxParallelismPerRefresh` · int · Opciones · nivel de compatibilidad 1568+

El número máximo de tareas, como tablas o particiones, que una actualización procesa en paralelo. El servicio puede seguir limitando el número en función de los recursos de la capacidad. Redúcelo para disminuir la carga sobre el Data source, o auméntalo para actualizar más rápido cuando el Data source y la capacidad puedan soportarlo.

El valor predeterminado es `-1`, lo que deja el número en manos del servicio. El servicio de Power BI acepta cualquier valor sin validarlo.

<!-- TODO (not verifiable from TE3 source): confirm that -1 means "let the service decide", and the valid range. -->

En Tabular Editor 3, también puedes establecer el paralelismo máximo para una sola operación de actualización en el [diálogo de actualización avanzada](xref:advanced-refresh).

### Política de acceso a metadatos

`MetadataAccessPolicy` · MetadataCategory · Opciones · nivel de compatibilidad 1703+

Qué metadatos pueden ver los usuarios con permiso de lectura cuando consultan los metadatos del modelo, por ejemplo, con las DMV o con las funciones DAX `INFO`. No se aplica a los usuarios con permiso de escritura o de administración.

| Valor                    | Significado                                                                                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Inherited`              | Use el comportamiento que define el sistema.                                                                                           |
| `Basic`                  | Los lectores no pueden acceder a metadatos confidenciales del modelo, como las definiciones de medidas u otras expresiones de cálculo. |
| `CalculationDefinitions` | Los lectores también pueden leer los metadatos relacionados con las definiciones de cálculo.                                           |

Establezca `Basic` cuando la lógica del modelo sea confidencial y los lectores solo necesiten usarla. `MetadataAccessPolicy` no oculta ningún dato. Para proteger los datos, consulte @roles-and-rls.

<!-- TODO (not verifiable from TE3 source): the meanings above come from Microsoft's TOM library. Confirm what the system-defined behavior for Inherited is (workspace, tenant or service setting) and exactly which metadata Basic hides. -->

### Comportamiento de la expresión de selección

`SelectionExpressionBehavior` · SelectionExpressionBehaviorType · Opciones · nivel de compatibilidad 1609+

Lo que devuelven los grupos de cálculo del modelo cuando un usuario selecciona varios elementos de cálculo o ninguno y el grupo de cálculo no tiene `MultipleOrEmptySelectionExpression`, y cómo se comportan los subtotales cuando un Visual se agrupa por el grupo de cálculo.

| Valor       | Significado                                                                                                                                                                                                                             |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Automatic` | El valor predeterminado. Actualmente es igual que `NonVisual`. Según Microsoft, los modelos con un futuro nivel de compatibilidad superior usarán `Visual`.                             |
| `Visual`    | Una selección múltiple o vacía devuelve `BLANK()`. Cuando un Visual se agrupa por el grupo de cálculo, los subtotales se calculan evaluando la medida seleccionada en el contexto del grupo de cálculo. |
| `NonVisual` | Una selección múltiple o vacía devuelve `SELECTEDMEASURE()`. Cuando un Visual se agrupa por el grupo de cálculo, los subtotales se ocultan.                                                             |

Consulte @object-properties-calculation-groups.

### Comportamiento del filtro de valores

`ValueFilterBehavior` · ValueFilterBehaviorType · Opciones · nivel de compatibilidad 1606+

Cómo `SUMMARIZECOLUMNS` aplica filtros a dos o más columnas de la misma tabla. Power BI genera `SUMMARIZECOLUMNS` para casi todos los Visual, por lo que esta propiedad afecta a la mayoría de las consultas del Report.

| Valor         | Significado                                                                                                                                                                                                                                                                                                                                    |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Automatic`   | El valor predeterminado. Según Microsoft, actualmente significa `Coalesced`. Microsoft planea que, en el futuro, los nuevos modelos configurados en `Automatic` usen `Independent`.                                                                                                            |
| `Coalesced`   | Los filtros de columnas de la misma tabla se combinan y solo se mantienen las combinaciones que existen en la tabla. Esto se conoce como _auto-exist_. Esto puede hacer que las medidas devuelvan resultados inesperados, por ejemplo, cuando una medida elimina uno de los filtros con `ALL`. |
| `Independent` | Cada filtro se aplica por separado, sin auto-exist.                                                                                                                                                                                                                                                                            |

Cambiar esta propiedad puede modificar las cifras de los Reports existentes, por lo que conviene probar los Reports de un modelo en uso antes de cambiarla. Un modelo nuevo guardado desde Power BI Desktop tiene `ValueFilterBehavior` establecido en `Independent`.

### Atributos de M

`MAttributes` · string · Opciones · nivel de compatibilidad 1535+

Atributos del documento de sección de Power Query que contiene las expresiones M del modelo, en forma de registro de M. Un modelo nuevo guardado desde Power BI Desktop lo deja vacío.

<!-- TODO (not verifiable from TE3 source): which tools or scenarios fill in M Attributes, with an example value. -->

### Ubicación de almacenamiento

`StorageLocation` · string · Opciones

Solo para Analysis Services: la carpeta del disco del servidor donde el motor almacena los archivos de datos del modelo. Si está vacío, se usa la carpeta de datos predeterminada del servidor. Power BI y Fabric no usan esta propiedad. Azure Analysis Services acepta un valor sin generar un error.

<!-- TODO (not verifiable from TE3 source): whether SQL Server Analysis Services 2016 and later or Azure Analysis Services still use Storage Location (the value is accepted, the effect isn't observable). -->

### Tiene cambios locales

`HasLocalChanges` · bool · Opciones · solo de lectura

Indica si el modelo tiene cambios que aún no se han guardado en el motor. Este es el propio estado de TOM, independiente de los cambios no guardados en Tabular Editor. Siempre es `false` para un modelo que no está conectado a un motor, como uno que se ha abierto desde un archivo. Tabular Editor 3 no muestra esta propiedad en la vista de propiedades. Puedes leerla en un C# Script.

En Tabular Editor 3, @unsaved-changes muestra qué objetos y propiedades difieren de la última versión guardada del modelo.

### Expresiones

`Expressions` · colección de expresiones compartidas · Opciones · solo lectura · nivel de compatibilidad 1400+

Las expresiones compartidas del modelo, como los parámetros de Power Query y las consultas a las que hacen referencia otras consultas. Selecciona **...** para editar la colección, o trabaja con ellas en la carpeta **Expresiones compartidas** del **Explorador TOM**. Consulta @object-properties-data-sources. El script @script-create-m-parameter agrega un parámetro de Power Query con un C# Script.

### Query Group

`QueryGroups` · colección de Query Groups · Opciones · solo de lectura · nivel de compatibilidad 1480+

Las carpetas que agrupan las consultas y los parámetros de Power Query, como se muestra en el panel **Consultas** de Power BI Desktop. Consulta @object-properties-data-sources.

### Colección de información de enlace

`BindingInfoCollection` · colección de objetos de información de enlace · Opciones · solo de lectura · nivel de compatibilidad 1608+

Sugerencias que indican a Fabric qué conexión de datos usar para un Data source en el modelo, por ejemplo, después de implementar el modelo en otro Workspace. Consulta **Sugerencia de enlace de datos** en @object-properties-data-sources.

### Funciones

`Functions` · colección de funciones · Opciones · solo lectura · nivel de compatibilidad 1702+

Las funciones DAX definidas por el usuario (UDFs) del modelo. Consulta @object-properties-functions y @udfs. La regla de BPA @kb.bpa-udf-use-compound-names marca las funciones cuyos nombres no contienen un separador `.` o `_`.

### Configuraciones regionales

`Cultures` · colección de configuraciones regionales · traducciones, perspectivas, seguridad · de solo lectura

Las configuraciones regionales, o traducciones, del modelo. Cada configuración regional contiene los nombres, las descripciones y las carpetas de visualización traducidos para un idioma. Selecciona **...** para agregar o quitar configuraciones regionales. Para editar las traducciones, usa las propiedades de traducción de cada objeto o, en Tabular Editor 3, el @metadata-translation-editor. Consulta @object-properties-perspectives-cultures y @how-to-work-with-perspectives-translations. Para exportar las traducciones de una configuración regional a un archivo JSON y volver a importarlas, consulta @import-export-translations.

### Perspectivas

`Perspectives` · colección de perspectivas · traducciones, perspectivas, seguridad · de solo lectura

Las perspectivas del modelo. Selecciona **...** para agregar o quitar perspectivas. Para elegir qué objetos muestra cada perspectiva, usa `InPerspective` en cada objeto o, en Tabular Editor 3, el @perspective-editor. Consulta @object-properties-perspectives-cultures. La regla de BPA @kb.bpa-perspectives-no-objects marca las perspectivas que no contienen tablas visibles.

### Roles

`Roles` · colección de roles · traducciones, perspectivas, seguridad · de solo lectura

Los roles de seguridad del modelo. Los roles controlan quién puede consultar el modelo y qué datos puede ver, mediante la seguridad a nivel de filas y la seguridad a nivel de objetos. Selecciona **...** para agregar o quitar roles. Consulta @object-properties-security y @roles-and-rls. Para obtener instrucciones paso a paso, consulta @data-security-setup-rls y @data-security-setup-ols.
