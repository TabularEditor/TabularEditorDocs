---
uid: object-properties-partitions
title: Propiedades de la partición
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

# Propiedades de la partición

<!--
SUMMARY: Reference for the properties of partitions (legacy, calculated, M, entity and policy range partitions), incremental refresh policies and data coverage definitions.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Esta página describe las propiedades de las particiones, las políticas de actualización para la actualización incremental y las definiciones de cobertura de datos. Para las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

Una partición define de dónde procede una parte de los datos de una tabla. Todas las tablas, salvo los grupos de cálculo, tienen al menos una partición, y la mayoría tienen exactamente una. Cada tipo de partición describe su origen de forma distinta:

| Tipo                                                | Tipo de origen | De dónde proceden los datos                                                                                                                            |
| --------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Partición heredada (de consulta) | `Query`        | Una consulta nativa, normalmente SQL, sobre un Data source heredado (proveedor).                                    |
| Partición calculada                                 | `Calculated`   | La expresión DAX de una tabla calculada.                                                                                               |
| Partición de M                                      | `M`            | Una expresión de Power Query (M). Power BI y la mayoría de los modelos modernos usan este tipo.     |
| Partición de entidad                                | `Entity`       | Una entidad con nombre, como una tabla Delta en un Lakehouse o en un Warehouse. Las tablas Direct Lake usan este tipo. |
| Partición por intervalo de la política              | `PolicyRange`  | Un intervalo de fechas de la política de actualización incremental de la tabla. El motor crea estas particiones.       |

Todos los tipos comparten las propiedades descritas en [Propiedades de todas las particiones](#propiedades-de-todas-las-particiones). Las secciones siguientes enumeran las propiedades específicas de cada tipo.

## Propiedades de todas las particiones

Estas propiedades se aplican a cada tipo de partición. La vista **Propiedades** solo muestra las que se aplican al tipo seleccionado; por ejemplo, `Query` solo se muestra en las particiones heredadas y `QueryGroup` solo en las particiones M. Cuando una tabla tiene una sola partición con el mismo nombre que la tabla, al cambiar el nombre de la tabla también se cambia el nombre de la partición.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Mensaje de error](xref:object-properties-common#error-message)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Estado](xref:object-properties-common#state)

### Data source

`DataSource` · DataSource · Básico

El Data source contra el que se ejecuta la consulta de la partición. Tabular Editor muestra esta propiedad en las particiones heredadas (de consulta) y en las particiones de entidad, donde puedes elegir uno de los Data sources del modelo en el menú desplegable. Las particiones de rango de directiva también muestran la propiedad, pero ahí siempre está vacía.

Las particiones M no usan esta propiedad. Su expresión M nombra el Data source directamente, por ejemplo `Sql.Database("myserver", "mydb")`, o hace referencia a un origen de datos estructurado o a una expresión compartida. Consulta @object-properties-data-sources.

### Expresión

`Expression` · string · Básico

La expresión que rellena la partición con datos. La vista **Propiedades** solo la muestra en las particiones calculadas, donde contiene la expresión DAX de la tabla calculada. En las particiones heredadas, el mismo texto aparece como `Query`, y en las particiones M como `MExpression`.

El **Explorador TOM** no muestra las particiones de las tablas calculadas (incluidos los parámetros de campo) ni de los grupos de cálculo. Edita la expresión DAX mediante `Expression` en la tabla calculada, o abre las propiedades de la partición con el script @script-edit-hidden-partitions.

En un script en C#, `Expression` lee y escribe la expresión de las particiones heredadas, calculadas y M. Al establecerla en cualquier otro tipo de partición, como una partición de entidad, se produce un error.

### Query

`Query` · string · Básico

La consulta nativa que el motor envía al Data source heredado para rellenar la partición, por ejemplo:

```sql
SELECT * FROM dbo.FactSales WHERE OrderDate >= '2024-01-01'
```

`Query` solo aparece en las particiones heredadas (de consulta). Es un alias de `Expression` y ambos nombres leen y escriben el mismo valor. El motor envía la consulta tal cual, así que escríbela en el dialecto propio del origen. Si divides una tabla grande en varias particiones heredadas y sus cláusulas `WHERE` se solapan o dejan huecos, algunas filas se cargan dos veces o no se cargan.

En Tabular Editor 3, un perfil de sobrescritura de actualización reemplaza la consulta de una partición durante una sola actualización, por ejemplo, para cargar solo las 10 000 primeras filas durante el desarrollo. Consulta @refresh-overrides.

### Procesado por última vez

`RefreshedTime` · DateTime · Metadatos · solo lectura

La fecha y hora en que el motor actualizó por última vez la partición. Úsalo para confirmar que una actualización afectó a una partición, por ejemplo, después de una actualización programada o de una actualización incremental que solo actualiza las particiones más recientes.

Un modelo abierto desde un archivo muestra el valor almacenado en el archivo, si existe. El valor solo es fiable cuando estás conectado a un servidor o trabajas en el modo @workspace-mode.

Cuando la opción de serialización **Ignore timestamps** está activada (es la predeterminada; consulta las preferencias en @preferences), Tabular Editor omite las marcas de tiempo al guardar el modelo en un archivo `.bim` o en una carpeta en formato JSON. Estas marcas de tiempo son `RefreshedTime` y las marcas de tiempo de modificación del modelo y sus objetos. Tabular Model Definition Language (TMDL) nunca almacena marcas de tiempo, por lo que un modelo guardado como TMDL no tiene ningún valor de `RefreshedTime`, independientemente de cómo esté configurada la opción.

En Tabular Editor 3, actualiza una sola partición haciendo clic con el botón derecho en ella en el **Explorador TOM**, eligiendo **Actualizar partición** y luego el tipo de actualización. La @data-refresh-view muestra el progreso de la actualización.

### DataCoverageDefinition

`DataCoverageDefinition` · DataCoverageDefinition · Opciones · nivel de compatibilidad 1603+

La [definición de cobertura de datos](#data-coverage-definition) opcional de la partición, que describe las filas que contiene una partición de DirectQuery. Cuando una consulta solo solicita filas fuera de ese intervalo, el motor evita consultar el origen. Las tablas híbridas la usan en la partición de DirectQuery que contiene los datos recientes, junto a las particiones importadas con datos más antiguos.

Tabular Editor muestra esta propiedad en el nivel de compatibilidad 1603 y superior, en las particiones en modo `DirectQuery` o `Dual` y en cualquier partición que ya tenga una definición de cobertura de datos. Usa las acciones de la propiedad para agregar o quitar la definición, o para editar su expresión. En esas mismas particiones, el **Editor de expresiones** muestra la expresión de la definición de cobertura de datos, y escribir allí una expresión en una partición sin definición agrega una.

### Vista de datos

`DataView` · DataViewType · Opciones

Para los modelos de DirectQuery en Analysis Services: si la partición contiene todos los datos o una muestra de ellos. Una partición de muestra contiene un pequeño subconjunto importado de una tabla de DirectQuery para diseñar el modelo en Visual Studio. Las consultas de las herramientas cliente usan el conjunto completo de datos.

| Valor            | Significado                                                                                              |
| ---------------- | -------------------------------------------------------------------------------------------------------- |
| `Full`           | La partición contiene todos los datos.                                                   |
| `Muestra`        | La partición contiene una muestra de los datos para usarla mientras se diseña el modelo. |
| `Predeterminado` | La partición usa el `DefaultDataView` del modelo.                                        |

El Tabular Object Model (TOM) solo define estos tres valores. Según la documentación de Microsoft sobre el modo DirectQuery, la característica **Establecer como muestra** del diseñador de modelos de Visual Studio no se admite actualmente. Power BI no usa vistas de datos, así que deje esta propiedad en su valor predeterminado en los modelos de Power BI y Fabric.

### Modo

`Mode` · ModeType · Opciones

El modo de almacenamiento de la partición, que determina cómo accede el motor a los datos que contiene.

| Valor            | Significado                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Import`         | Los datos se cargan en la memoria del modelo durante la actualización. Las consultas no se envían al origen.                                                                                                                                                                                                                                                                    |
| `DirectQuery`    | Los datos permanecen en el origen. Cada consulta se traduce en una consulta al origen, por ejemplo, en SQL.                                                                                                                                                                                                                                                                     |
| `Dual`           | La partición actúa como Import o DirectQuery, según cuál produzca la mejor consulta en un modelo compuesto. Normalmente se usa para tablas de dimensiones relacionadas tanto con tablas de hechos importadas como con tablas de hechos en DirectQuery. Nivel de compatibilidad 1455+.                                                                           |
| `DirectLake`     | Los datos se leen directamente de tablas Delta en OneLake y se cargan en memoria bajo demanda. Solo en Fabric. Se usa con particiones de entidad. Nivel de compatibilidad 1604+. No está disponible en las ediciones de Tabular Editor que no admiten Direct Lake. Consulta @direct-lake-guidance. |
| `Push`           | Los datos se envían a la partición a través de la API REST de Power BI, como en un modelo semántico de tipo push. No hay ninguna consulta de origen. Solo el servicio de Power BI lo admite.                                                                                                                                                                    |
| `Predeterminado` | La partición usa el `DefaultMode` del modelo. Consulta @object-properties-model.                                                                                                                                                                                                                                                                                   |

El modo se establece por partición y normalmente todas las particiones de una tabla tienen el mismo modo. La principal excepción es una tabla híbrida, en la que una directiva de actualización incremental importa las particiones históricas y mantiene la más reciente en modo DirectQuery (consulta `Mode` en [política de actualización](#refresh-policy)).

Cambiar una tabla de `Import` a `DirectQuery` elimina sus datos importados, y algunas características, como las columnas calculadas que usan determinadas funciones DAX, no funcionan en DirectQuery. Para convertir una tabla de Direct Lake a importación o viceversa, consulta @script-convert-dlol-to-import y @script-convert-import-to-dlol.

Tabular Editor acepta cualquier combinación de modos. Al guardar, el motor rechaza las combinaciones que no admite, y SQL Server Analysis Services es mucho más estricto que Power BI. Analysis Services de SQL Server 2025:

- rechaza las particiones `Dual` con el error `may not operate in Dual mode`
- rechaza los modelos que mezclan datos importados con DirectQuery, tanto dentro de una tabla como entre tablas, por lo que no son posibles los modelos compuestos ni las tablas híbridas
- solo permite una partición `DirectQuery` por tabla

La única combinación que acepta es el patrón antiguo de DirectQuery: una partición `DirectQuery` más particiones `Import` con `DataView` establecido en `Sample`.

El servicio de Power BI acepta una partición `Import` y una `DirectQuery` en la misma tabla, incluso sin una política de actualización. Las tablas `Dual` y las relaciones entre tablas importadas y tablas DirectQuery en ambos sentidos también funcionan allí. El servicio mantiene la regla de una partición `DirectQuery` por tabla y rechaza una partición `DirectQuery` o `Dual` cuya expresión no haga referencia a un Data source, como una construida a partir de datos literales con `#table`.

### Query Group

`QueryGroup` · QueryGroup · Opciones · nivel de compatibilidad 1480+

El Query Group (carpeta) en el que aparece la consulta M de la partición, en el editor de Power Query de Power BI Desktop. Solo organiza las consultas en ese editor y no afecta ni a la actualización ni a la lista de campos. Tabular Editor muestra esta propiedad solo en las particiones M, donde eliges uno de los Query Group del modelo en la lista desplegable o lo dejas vacío. Para los Query Group, consulta @object-properties-data-sources.

### Tipo de origen

`SourceType` · PartitionSourceType · Opciones · solo lectura

El tipo de partición, que se establece al crearla. Para cambiar el tipo, crea una partición nueva del tipo correcto y elimina la anterior.

| Valor              | Significado                                                                                                                                                            |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Query`            | Una partición heredada con una consulta nativa contra un origen de datos del proveedor.                                                                |
| `Calculated`       | La partición de una tabla calculada, rellenada mediante una expresión DAX.                                                                             |
| `None`             | La partición no tiene origen. Los datos se insertan en ella, por ejemplo, en un modelo semántico push.                                 |
| `M`                | Una partición M con una expresión de Power Query (M).                                                                               |
| `Entity`           | Una partición de entidad que lee una entidad con nombre, como una tabla en un Lakehouse. Direct Lake usa este tipo.                    |
| `PolicyRange`      | Una partición generada por una política de actualización incremental.                                                                                  |
| `CalculationGroup` | La partición de una tabla de un grupo de cálculo. No contiene ningún origen; el motor la rellena a partir de los elementos de cálculo. |
| `Inferida`         | Una partición para la que el motor genera la consulta automáticamente. Nivel de compatibilidad 1563+.                                  |

TOM también define el valor `Parquet` para un nivel de compatibilidad interno que Microsoft no publica, por lo que no aparece en tus modelos.

<!-- TODO (not verifiable from TE3 source): which kind of table or model feature creates Inferred partitions. TOM only says "populated by executing a query generated by the system" (CL 1563+), and TE3 has no special handling for it. Same open question as on @object-properties-tables. -->

## Particiones heredadas y calculadas

Las particiones heredadas (de consulta) y las particiones calculadas no tienen propiedades más allá de las que se indican en [Propiedades de todas las particiones](#properties-of-all-partitions).

- una **partición heredada** (`Query`) usa `DataSource` y `Query`. Los modelos la usan con orígenes de datos del proveedor, normalmente en modelos de Analysis Services con un nivel de compatibilidad inferior a 1400. Consulta @import-tables. La regla @kb.bpa-avoid-provider-partitions-structured del Best Practice Analyzer (BPA) señala las particiones heredadas que usan un origen de datos estructurado, una combinación que Power BI no admite.
- una **partición calculada** (`Calculated`) pertenece a una tabla calculada y usa `Expression`. Edita la expresión DAX en la propia tabla calculada (consulta `Expression` en @object-properties-tables). El **Explorador TOM** no muestra las particiones de las tablas calculadas. Para abrir una partición, usa el script @script-edit-hidden-partitions.

## Partición de M

Una partición de M rellena la tabla con el resultado de una expresión de Power Query (M). Es el tipo de partición predeterminado en los modelos de Power BI y en los modelos de Analysis Services con nivel de compatibilidad 1400 o superior. La expresión M normalmente parte de una función de origen, como `Sql.Database`, o de una expresión compartida, y termina con la tabla que se va a cargar.

### Propiedades comunes

Las mismas que en [todas las particiones](#properties-of-all-partitions).

### Atributos

`Attributes` · cadena · Opciones

Atributos M adicionales almacenados con el origen de la partición. La mayoría de los modelos lo dejan vacío, y Power BI Desktop también lo deja vacío, incluso en tablas con una política de actualización incremental.

<!-- TODO (not verifiable from TE3 source): which tools or scenarios fill in Attributes on an M partition. -->

### Expresión M

`MExpression` · string · Opciones

La expresión de Power Query (M) que devuelve los datos de la partición. Edítala en el **Editor de expresiones**. Por ejemplo:

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data]
in
    Sales
```

La expresión debe devolver una tabla cuyas columnas coincidan con los valores de `SourceColumn` de las columnas de datos de la tabla (consulta @object-properties-columns). Si en el origen se cambia el nombre de una columna o se elimina, la actualización fallará hasta que actualices las columnas de la tabla, por ejemplo con **Actualizar esquema de tabla** (consulta @import-tables).

Las partes que comparten varias particiones, como el nombre del servidor, pueden ir en una expresión compartida o en un parámetro M al que las expresiones hagan referencia por nombre. Consulta @script-create-m-parameter. En Tabular Editor 3, @script-create-and-replace-parameter también reemplaza el valor por el nuevo parámetro en todas las particiones M.

En Tabular Editor 3, el script @script-format-power-query da formato a la expresión M de la partición seleccionada mediante un servicio de formato externo.

## Partición de entidad

Una partición de entidad lee sus datos de un objeto con nombre, una _entidad_. Cada tabla de Direct Lake tiene una partición de entidad que apunta a una tabla Delta en un Lakehouse o un Warehouse de Fabric. Una expresión compartida contiene la conexión al Lakehouse o al Warehouse, y la partición hace referencia a ella mediante `ExpressionSource`.

Consulta @direct-lake-sql-model y @direct-lake-guidance. En Tabular Editor 3, el asistente @import-tables crea tablas de Direct Lake a partir de un Lakehouse o un Warehouse de Fabric.

### Propiedades comunes

Las mismas que en [todas las particiones](#properties-of-all-partitions).

### Nombre de entidad

`EntityName` · string · Opciones

El nombre del objeto de origen que lee la partición; por ejemplo, la tabla Delta `FactSales` del Lakehouse. Al igual que el `SourceColumn` de una columna, debe coincidir exactamente con el nombre en el origen. Cambiar el nombre de la tabla en el modelo no cambia el nombre de la entidad, así que la tabla puede tener un nombre más descriptivo que el del origen. Si se cambia el nombre de la tabla de origen, actualiza `EntityName` para que coincida o la partición fallará la próxima vez que se procese o actualice el modelo.

<!-- TODO (not verifiable from TE3 source): whether Entity Name is case-sensitive for Direct Lake. -->

Si los cambios que haces en `EntityName` se revierten después de actualizar el modelo en Power BI, consulta @direct-lake-entity-updates-reverting.

### Origen de la expresión

`ExpressionSource` · NamedExpression · Opciones

La expresión compartida que contiene la conexión al origen. En un modelo Direct Lake, normalmente es una expresión compartida llamada `DatabaseQuery`, el nombre que le asigna el asistente de importación de Tabular Editor 3. Su expresión M depende del tipo de Direct Lake:

- **Direct Lake en SQL**: `Sql.Database("<SQL endpoint>", "<lakehouse or warehouse name>")`
- **Direct Lake en OneLake**: `AzureStorage.DataLake("https://onelake.dfs.fabric.microsoft.com/<workspace ID>/<item ID>", [HierarchicalNavigation=true])`

Tabular Editor distingue ambos tipos por la función M de esa expresión compartida y considera que una partición de entidad sin un origen de expresión es Direct Lake en SQL. Todas las tablas Direct Lake de un modelo suelen apuntar a la misma expresión compartida.

Para que un modelo Direct Lake apunte a otro Lakehouse o Warehouse, por ejemplo, al pasarlo de desarrollo a producción, cambia la expresión M de esa expresión compartida. Las particiones siguen apuntando a ella. El script @script-convert-dlsql-to-dlol cambia un modelo de Direct Lake en SQL a Direct Lake en OneLake modificando esa misma expresión M.

### Nombre del esquema

`SchemaName` · cadena · Opciones · nivel de compatibilidad 1604+

El esquema del objeto de origen, para Lakehouse y Warehouse que usan esquemas; por ejemplo, `dbo` o `sales`. Déjalo vacío cuando el origen no tenga esquemas. Junto con `EntityName`, identifica la tabla de origen.

La documentación de Microsoft describe esta propiedad como reservada para uso futuro. Tabular Editor la muestra en el nivel de compatibilidad 1604 y superior.

<!-- TODO (not verifiable from TE3 source): whether Direct Lake now uses Schema Name for schema-enabled lakehouses, despite the "reserved for future use" description in TOM. -->

## Partición de rango de la política

Una partición de rango de la política contiene un intervalo de fechas de una tabla que usa actualización incremental. El motor crea, combina y elimina estas particiones cuando aplica la política de actualización de la tabla; por ejemplo, durante una actualización en el servicio de Power BI o cuando seleccionas **Aplicar política de actualización** en Tabular Editor. Cada partición cubre un periodo, como un día, un mes, un trimestre o un año, y los periodos más antiguos se combinan en particiones más grandes con el tiempo. La consulta M de una partición de rango de la política es la `SourceExpression` de la política de actualización, usando `Start` y `End` de la partición como valores de `RangeStart` y `RangeEnd`.

Consulta @incremental-refresh-about, @incremental-refresh-setup y @incremental-refresh-modify. En Tabular Editor 3, el cuadro de diálogo @advanced-refresh aplica la política de actualización como parte de una actualización con una fecha de vigencia que eliges, para probar cómo se comporta la política en otro momento. Al implementar desde Tabular Editor 3, puedes omitir las particiones regidas por una política de actualización. Consulta @deployment.

### Propiedades comunes

Igual que en [todas las particiones](#properties-of-all-partitions).

### End

`End` · DateTime · Política de actualización

El final del intervalo de fechas que cubre la partición. La partición contiene las filas con fecha anterior a `End`, y el motor pasa el valor como `RangeEnd` al actualizar la partición. El motor lo establece cuando aplica la política de actualización.

### Granularity

`Granularity` · RefreshGranularityType · Política de actualización

El tamaño del período que cubre la partición.

| Valor       | Significado                                                |
| ----------- | ---------------------------------------------------------- |
| `Día`       | Un día.                                    |
| `Mes`       | Un mes natural.                            |
| `Trimestre` | Un trimestre natural.                      |
| `Año`       | Un año natural.                            |
| `Inválido`  | No se ha establecido ninguna granularidad. |

Los períodos recientes suelen ser pequeños (días o meses) y se combinan en otros mayores (trimestres y, después, años) a medida que salen de la ventana de actualización incremental.

### RefreshBookmark

`RefreshBookmark` · string · Política de actualización · de solo lectura

El valor que `PollingExpression` de la política de actualización devolvió para esta partición en la última actualización; por ejemplo, la fecha de modificación más reciente dentro del intervalo de la partición. Está vacío cuando la política no tiene ninguna expresión de sondeo. En la siguiente actualización, el motor vuelve a evaluar la expresión de sondeo y solo actualiza la partición si el valor ha cambiado. Así es como funciona **Detectar cambios en los datos** en Power BI Desktop.

La propiedad es de solo lectura en Tabular Editor y en la biblioteca TOM, pero un comando `alter` de Tabular Model Scripting Language (TMSL) puede establecer `refreshBookmark` en una partición, por ejemplo, con el valor de una cadena vacía. En la siguiente actualización, con la política de actualización aplicada, el motor compara el resultado del sondeo con el Bookmark guardado y solo actualiza las particiones en las que difieren; por eso, cambiar el Bookmark fuerza la actualización de esa partición. Una actualización con `applyRefreshPolicy` establecido en `false` actualiza las particiones sin leer ni actualizar los Bookmarks.

### Inicio

`Start` · DateTime · política de actualización

El inicio del intervalo de fechas que cubre la partición. La partición contiene las filas con fecha igual o posterior a `Start`, y el motor pasa el valor como `RangeStart` cuando actualiza la partición. Al igual que `End`, el motor lo establece cuando aplica la política de actualización.

## Política de actualización

Una política de actualización define cómo el motor particiona y actualiza una tabla de forma incremental: cuánto historial conservar (la _ventana deslizante_), cuánto de los datos más recientes actualizar cada vez (la _ventana incremental_) y la consulta M de cada partición. El motor usa la política para crear y mantener las [particiones de rango de la política](#policy-range-partition) de la tabla.

La política de actualización se encuentra en la tabla, en **actualización incremental**, en la vista **Propiedades**. Establece **Habilitado** (`EnableRefreshPolicy`) en `true` en la tabla y, después, expande **política de actualización** para editar las propiedades siguientes. Consulta `RefreshPolicy` en @object-properties-tables.

Con `RollingWindowPeriods` establecido en `5`, `RollingWindowGranularity` en `Year`, `IncrementalPeriods` en `10` e `IncrementalGranularity` en `Day`, la tabla conserva cinco años de historial y cada actualización solo vuelve a cargar los últimos diez días.

Consulta @incremental-refresh-about, @incremental-refresh-policy, @incremental-refresh-setup, @incremental-refresh-modify y @incremental-refresh-schema. El script @script-implement-incremental-refresh configura una política de actualización para una tabla de importación a partir de una columna de fecha que selecciones, incluidos los parámetros `RangeStart` y `RangeEnd`.

### Propiedades comunes

- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

### Granularidad incremental

`IncrementalGranularity` · RefreshGranularityType · Opciones

La unidad de `IncrementalPeriods`: `Day`, `Month`, `Quarter` o `Year`. `Invalid` significa que la política aún no está configurada. La unidad también es el tamaño de las particiones de la ventana incremental; por ejemplo, una partición por día del rango que se actualiza para `Day`.

### Períodos incrementales

`IncrementalPeriods` · int · Opciones

Cuántos períodos, contados hacia atrás desde hoy, actualiza el motor en cada actualización. Con `IncrementalGranularity` establecido en `Day` y `IncrementalPeriods` en `10`, cada actualización vuelve a cargar los últimos diez días y deja intactas las particiones más antiguas. Una ventana más amplia hace que las actualizaciones sean más lentas, y una ventana demasiado pequeña no detecta cambios en filas más antiguas.

### Desplazamiento de períodos incrementales

`IncrementalPeriodsOffset` · int · Opciones

Desplaza la ventana incremental con respecto a hoy, en unidades de `IncrementalGranularity`:

- `0` hace que la ventana termine en el período actual
- un valor negativo la desplaza al pasado; por ejemplo, `-1` con `Day` actualiza hasta e incluido ayer, por lo que la tabla solo contiene días completos
- un valor positivo la desplaza al futuro, para orígenes que contienen filas con fechas futuras, como las previsiones

La opción **Actualizar solo días completos** del cuadro de diálogo de actualización incremental de Power BI Desktop establece `IncrementalPeriodsOffset` en `-1`.

### Modo

`Mode` · RefreshPolicyMode · Opciones · nivel de compatibilidad 1565+

Si el período más reciente también se importa o se mantiene en DirectQuery para mostrar datos en tiempo real.

| Valor    | Significado                                                                                                                                                                                                                                                                                                                                                               |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Import` | Se importan todas las particiones, incluida la más reciente. Los datos estarán tan actualizados como la última actualización.                                                                                                                                                                                                             |
| `Hybrid` | Se importan las particiones históricas y el motor agrega una partición de DirectQuery para las filas posteriores a la ventana incremental. Las consultas siempre ven las filas más recientes en el origen y la tabla se convierte en una tabla híbrida. Solo para Power BI Premium, Premium Per User y Power BI Embedded. |

Una tabla híbrida envía al origen las consultas del período actual. Una [definición de cobertura de datos](#data-coverage-definition) en la partición de DirectQuery evita las consultas al origen para filas fuera del período actual. Microsoft recomienda el modo de almacenamiento dual para las tablas relacionadas con una tabla híbrida.

### Tipo de política

`PolicyType` · RefreshPolicyType · Opciones · solo de lectura

El tipo de política de actualización. El único valor es `Basic`, la política descrita en esta página, y no puedes cambiarlo desde Tabular Editor.

### Expresión de sondeo

`PollingExpression` · string · Opciones

Una expresión M opcional que el motor evalúa para cada partición en la ventana incremental antes de actualizarla. Normalmente devuelve la fecha de modificación más reciente o el recuento de filas del intervalo de la partición. El motor almacena el resultado en el `RefreshBookmark` de la partición y solo actualiza la partición cuando el valor ha cambiado desde la última actualización. Cuando la propiedad está vacía, todas las particiones de la ventana incremental se actualizan cada vez.

La expresión puede usar `RangeStart` y `RangeEnd`, igual que `SourceExpression`. Este ejemplo devuelve la última fecha de modificación en el intervalo de la partición:

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data],
    InRange = Table.SelectRows(Sales, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd),
    LastModified = List.Max(InRange[ModifiedDate])
in
    LastModified
```

Power BI Desktop rellena esta propiedad cuando seleccionas **Detectar cambios en los datos** en el cuadro de diálogo de actualización incremental. En Tabular Editor, edita la expresión de sondeo en el **Editor de expresiones** seleccionando la tabla y eligiendo **Expresión de sondeo** en la lista desplegable. Consulta [Configurar 'Detectar cambios en los datos'](xref:incremental-refresh-modify#configure-detect-data-changes).

### Granularidad de la ventana móvil

`RollingWindowGranularity` · RefreshGranularityType · Opciones

La unidad de `RollingWindowPeriods`: `Day`, `Month`, `Quarter` o `Year`. `Invalid` significa que la política aún no está configurada.

### Períodos de la ventana móvil

`RollingWindowPeriods` · int · Opciones

Cuántos períodos completos del historial, contados hacia atrás desde hoy, mantiene la tabla además del período actual, que está incompleto. Con `RollingWindowGranularity` establecido en `Year` y `RollingWindowPeriods` en `5`, la tabla conserva los últimos cinco años completos en particiones anuales, más el año actual hasta la fecha en particiones trimestrales, mensuales o diarias. Cuando un período sale de la ventana, el motor elimina su partición y los datos que contiene en la siguiente actualización.

La ventana móvil debe ser mayor que la ventana incremental, que constituye su parte más reciente.

### Expresión de origen

`SourceExpression` · string · Opciones

La expresión M que el motor usa como consulta para cada partición de rango de la directiva que crea. Debe filtrar el origen por una columna de fecha con los parámetros M `RangeStart` y `RangeEnd`, que el motor establece con los valores `Start` y `End` de cada partición. Por ejemplo:

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data],
    InRange = Table.SelectRows(Sales, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd)
in
    InRange
```

Use `>=` en un parámetro y `<` en el otro. Con `>=` y `<=`, una fila que cae exactamente en un límite se carga en dos particiones.

`RangeStart` y `RangeEnd` deben existir en el modelo como parámetros M (expresiones compartidas) de tipo `DateTime`. Si la columna de fecha del origen es una clave entera como `20240131`, convierta los parámetros a ese formato dentro del paso de filtro. Si el filtro no se pliega en el origen, el origen devuelve todas las filas para cada partición.

Las particiones de intervalo de la política no almacenan una consulta propia, y cada actualización de una de ellas usa la `SourceExpression` actual. Un cambio entra en vigor en la siguiente actualización, pero solo para las particiones que esa actualización reprocesa. Una actualización con la política de actualización aplicada, que es la que ejecuta el servicio Power BI, solo reprocesa las particiones incrementales y las particiones históricas conservan los datos que cargaron con la expresión anterior. Para recargarlas todas con la nueva expresión, ejecute una actualización completa de la tabla con `applyRefreshPolicy` establecido en `false`.

## Definición de cobertura de datos

Una definición de cobertura de datos describe, como expresión DAX, qué filas contiene una partición. El motor la usa para omitir una partición de DirectQuery cuando una consulta solo solicita filas que la partición no puede contener. En una tabla híbrida sin ella, cada consulta sobre la tabla también consulta el origen a través de la partición de DirectQuery, incluso cuando la consulta solo solicita datos del año pasado que ya están importados.

La definición pertenece a una única partición. Agréguela mediante [DataCoverageDefinition](#datacoveragedefinition) en la partición.

### Propiedades comunes

- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Mensaje de error](xref:object-properties-common#error-message)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Estado](xref:object-properties-common#state)

### Expresión

`Expression` · cadena · Opciones

Una expresión DAX que devuelve `TRUE` para las filas que abarca la partición. Por ejemplo, para una partición de DirectQuery que solo contiene el año actual:

```dax
RELATED ( 'Date'[Year] ) = 2026
```

El motor confía en la expresión y no la contrasta con los datos. Si la expresión excluye una fila que está en la partición, las consultas omiten esa fila sin avisar, así que actualiza la expresión cuando cambie la consulta de la partición.

Para editarla, selecciona la partición en el **Explorador TOM** y elige la expresión de definición de cobertura de datos en la lista desplegable del **Editor de expresiones**.

El motor no valida la expresión al guardar. Analysis Services de SQL Server 2025 aceptó todas las expresiones que se probaron, incluidos los filtros de columna, las listas `IN`, `RELATED` y texto que no es DAX en absoluto; además, acepta una definición en una partición `Import`, donde la definición no tiene ningún propósito. Comprueba tú mismo la expresión antes de desplegar.

<!-- TODO (not verifiable from TE3 source): which DAX constructs are honored at query time in Power BI hybrid tables, and that a wrong definition silently leaves rows out of query results (needs a real hybrid table, which SSAS doesn't support). -->

### Partición

`Partition` · partición · Opciones · solo lectura

La partición a la que pertenece esta definición de cobertura de datos. La vista de **Propiedades** no la muestra. En scripts de **C# Script**, úsalo para volver desde la definición a su partición.
