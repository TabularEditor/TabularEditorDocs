---
uid: object-properties-tables
title: Propiedades de la tabla
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

# Propiedades de la tabla

<!--
SUMMARY: Reference for the properties of tables, calculated tables and calculation group tables.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Esta página trata las propiedades de los tres tipos de tablas en un modelo semántico: tablas normales, tablas calculadas y tablas de grupos de cálculo. La sección [Tabla](#table) describe las propiedades que comparten los tres tipos. Las secciones de las tablas calculadas y de las tablas de grupos de cálculo enumeran qué añaden y qué propiedades de tabla oculta para ellas la vista **Propiedades**. Para las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

## Tabla

Una tabla almacena filas de datos en columnas y contiene las medidas y jerarquías que le pertenecen. Una tabla normal obtiene sus datos de una o varias particiones, cada una con una consulta contra un Data source, por ejemplo, una expresión de Power Query (M) o una consulta SQL. El modo de la partición determina cómo se cargan los datos: Import, DirectQuery o Direct Lake.

En Tabular Editor 3, puedes agregar tablas desde un Data source con @import-tables y ver los datos de una tabla con @table-preview.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Oculto](xref:object-properties-common#hidden)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Propiedades modificadas](xref:object-properties-common#changed-properties)
- [Identificador DAX](xref:object-properties-common#dax-identifier)
- [Mensajes de error](xref:object-properties-common#error-message)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Etiqueta de linaje](xref:object-properties-common#lineage-tag)
- [Etiqueta de linaje de origen](xref:object-properties-common#source-lineage-tag)
- [Nombres traducidos](xref:object-properties-common#translated-names)
- [Descripciones traducidas](xref:object-properties-common#translated-descriptions)
- [Sinónimos](xref:object-properties-common#synonyms)
- [Mostrado en la perspectiva](xref:object-properties-common#shown-in-perspective)

### Grupo de tablas

`TableGroup` · string · Básico · _almacenado como una anotación_ (`TabularEditor_TableGroup`)

El grupo de tablas que contiene la tabla en el **Explorador TOM** de Tabular Editor 3. Los grupos de tablas funcionan como carpetas para las tablas; por ejemplo, para mantener separadas las tablas de hechos, las tablas de dimensiones y los grupos de cálculo. Déjalo vacío para mostrar la tabla en el nivel superior. Los grupos de tablas no se pueden anidar y las herramientas cliente, como Power BI y Excel, los ignoran.

El grupo se guarda con el modelo en la anotación `TabularEditor_TableGroup`, por lo que otros desarrolladores ven los mismos grupos. La vista **Propiedades** muestra `TableGroup` solo cuando los grupos de tablas están activados en el **Explorador TOM**. Consulta @table-groups.

En el **Explorador TOM**, también puedes hacer clic con el botón derecho en las tablas y elegir **Mover al grupo** o arrastrar tablas a un grupo de tablas (consulta @drag-drop). El script @script-create-table-groups coloca todas las tablas en grupos según su tipo y sus relaciones.

### Habilitar la política de actualización

`EnableRefreshPolicy` · bool · Actualización incremental · _atajo_: agrega o quita la **política de actualización** de la tabla

Activa o desactiva la actualización incremental de la tabla. Al establecerlo en `true`, se agrega una política de actualización a la tabla y se muestra la propiedad `RefreshPolicy`. Al establecerlo en `false`, se quita el objeto de política de actualización y se dejan las particiones de la tabla tal como están, incluidas las particiones de intervalo creadas por la política. Para volver a dejar la tabla con una partición M normal, sigue los pasos de [Eliminar la actualización incremental](xref:incremental-refresh-policy#removing-incremental-refresh-using-tabular-editor).

La actualización incremental solo está disponible para modelos de Power BI y Fabric. La vista **Propiedades** muestra `EnableRefreshPolicy` y `RefreshPolicy` cuando se cumplen todas estas condiciones:

- el modo de compatibilidad del modelo es Power BI
- el nivel de compatibilidad es 1450 o superior
- la tabla aún no tiene particiones, o tiene particiones M o de consulta en modo de importación o dual

En los modelos de Analysis Services, las particiones las creas y administras tú mismo. Consulta @incremental-refresh-about y @incremental-refresh-setup. El script @script-implement-incremental-refresh configura una política de actualización basada en una columna de fecha que selecciones, incluidos los parámetros `RangeStart` y `RangeEnd`.

### Política de actualización

`RefreshPolicy` · BasicRefreshPolicy · actualización incremental · nivel de compatibilidad 1450+

La política de actualización incremental de la tabla. Expándela en la vista **Propiedades** para definir cuánto historial conservar, cuánto actualizar, la expresión de origen y el resto de la configuración de la política. La configuración se describe en la sección de política de actualización de @object-properties-partitions. Consulta también @incremental-refresh-policy.

El motor crea las particiones de rango de la política la primera vez que se aplica la política, por ejemplo, al actualizar la tabla en el servicio de Power BI. Para aplicar la política desde Tabular Editor 3, haz clic con el botón derecho en la tabla en el **Explorador TOM** y elige **Aplicar política de actualización**. En Tabular Editor 2, la opción del menú es **Aplicar política de actualización**. Ambas versiones aplican la política solo cuando están conectadas al modelo y ya has guardado todos los cambios.

Para cambiar una política existente, consulta @incremental-refresh-modify. En Tabular Editor 3, puedes aplicar la política de actualización con una fecha efectiva distinta de la de hoy en el cuadro de diálogo @advanced-refresh, para probar cómo se comporta la política en otro momento.

### Fuente

`Source` · cadena · Metadatos · solo lectura · _calculado_

El nombre del Data source heredado (del proveedor) que consulta la primera partición de la tabla. Si las particiones usan distintos Data sources, solo verás el de la primera partición.

La vista **Propiedades** muestra `Source` solo cuando la primera partición es una partición de consulta o una partición M. En una partición M, el valor está vacío porque la conexión forma parte de la expresión M. No se muestra `Source` para tablas calculadas, tablas de grupo de cálculo, tablas Direct Lake ni tablas con particiones de intervalo de directiva.

Para enumerar las tablas que usan un Data source explícito (heredado), ejecuta el script @script-show-data-source-dependencies.

### Tipo de origen

`SourceType` · PartitionSourceType · Metadatos · solo lectura · _acceso directo al_ **Tipo de origen** de la primera partición

El tipo de origen que usa la primera partición de la tabla. En una tabla con particiones de distintos tipos, se muestra el tipo de la primera. Una tabla sin particiones muestra `None`.

La vista **Propiedades** oculta `SourceType` en las tablas calculadas y en las tablas de grupo de cálculo. En un C# Script, esos casos devuelven `Calculated` y `CalculationGroup`.

| Valor              | Significado                                                                                                                                                                                                |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Query`            | Las particiones ejecutan una consulta, por ejemplo SQL, contra un Data source heredado (del proveedor).                                                                 |
| `Calculated`       | La tabla es una tabla calculada y obtiene sus datos de una expresión DAX.                                                                                                                  |
| `None`             | No hay ningún origen definido. Los datos se envían a la tabla, por ejemplo en un modelo semántico push de Power BI.                                                        |
| `M`                | Las particiones usan una expresión de Power Query (M). Es lo más habitual en los modelos de Power BI. Nivel de compatibilidad 1400+.    |
| `Entity`           | Las particiones leen una entidad con nombre, como una tabla en un Lakehouse o un Warehouse. Lo usan las tablas Direct Lake. Nivel de compatibilidad 1400+. |
| `PolicyRange`      | Una política de actualización incremental creó las particiones. Nivel de compatibilidad 1450+.                                                                             |
| `CalculationGroup` | La tabla es una tabla de grupo de cálculo. Nivel de compatibilidad 1470+.                                                                                                  |
| `Inferred`         | El motor genera la consulta que rellena la partición. Nivel de compatibilidad 1563+.                                                                                       |

<!-- TODO (not verifiable from TE3 source): which kind of partition uses Inferred. TOM only says "The data in this partition is populated by executing a query generated by the system." -->

### Precedencia de origen alternativo

`AlternateSourcePrecedence` · int · Opciones · nivel de compatibilidad 1460+

El orden en que el motor tiene en cuenta esta tabla cuando busca una tabla de agregación que pueda responder a una consulta. Se aplica solo a las tablas de agregación; es decir, a tablas con columnas cuyo `AlternateOf` apunta a una columna de una tabla de detalle. Cuando más de una tabla de agregación puede responder a una consulta, el motor usa la que tiene el valor más alto. El valor predeterminado es `0`.

En Power BI Desktop, esta es la configuración **Precedencia** de **Administrar agregaciones**. Para configurar una tabla de agregación en Tabular Editor, consulta @user-defined-aggregations. El script @script-implement-user-defined-aggregations automatiza esos pasos para una tabla de hechos que selecciones.

### Calendarios

`Calendars` · colección de objetos Calendar · Opciones · nivel de compatibilidad 1701+

Los calendarios personalizados definidos en la tabla. Un calendario asigna las columnas de una tabla de fechas que contienen el año, el trimestre, el mes, la semana y la fecha; y las funciones de inteligencia temporal basadas en calendarios lo usan para trabajar con calendarios fiscales, de retail u otros calendarios no estándar. Los calendarios personalizados requieren el nivel de compatibilidad 1701 o superior. Consulta @object-properties-calendars.

En Tabular Editor 3, haz clic con el botón derecho en una tabla y elige **Crear > Calendario...** para agregar un calendario; después, asigna sus columnas en el **Editor de calendarios**. Consulta @calendars.

### Categoría de datos

`DataCategory` · string · Opciones

El tipo de datos que contiene la tabla, para las herramientas cliente. En Power BI, el valor `Time` marca la tabla como una tabla de fechas: Power BI usa la columna de fecha de la tabla (la columna con `IsKey` establecido en `true`) para la inteligencia temporal y desactiva la tabla automática de fecha y hora para esa tabla. **Marcar como tabla de fechas** en Power BI Desktop establece este valor.

Déjalo vacío o configúralo como `Regular` para todas las demás tablas. Los demás valores proceden de modelos multidimensionales, y solo los usan algunas características de Excel y herramientas cliente antiguas: `Geography`, `Organization`, `BillOfMaterials`, `Accounts`, `Customers`, `Products`, `Scenario`, `Quantitative`, `Utility`, `Currency`, `Rates`, `Channel` y `Promotion`. La lista desplegable de la vista **Propiedades** muestra estos valores y `Unknown`, y también puedes escribir un valor.

<!-- TODO (not verifiable from TE3 source): whether an empty value and "Regular" behave the same in the engine and client tools, and which client tools use the values other than Time. -->

En Tabular Editor, también puedes hacer clic con el botón derecho en la tabla en la vista @tom-explorer-view y elegir **Marcar como tabla de fechas...**. La regla @kb.bpa-date-table-exists del Best Practice Analyzer (BPA) señala los modelos que no tienen tabla de fechas. El script @script-create-date-table crea una tabla de fechas a partir de las columnas de fecha de tu modelo y establece `DataCategory` en `Time`.

### Expresión de filas de detalle predeterminada

`DefaultDetailRowsExpression` · string · Opciones · nivel de compatibilidad 1400+

Una expresión de tabla DAX que devuelve las filas que ve el usuario cuando realiza un drillthrough en una medida de esta tabla, por ejemplo con **Mostrar detalles** en una tabla dinámica de Excel. Se aplica a todas las medidas de la tabla que no tengan su propia `DetailRowsExpression` (consulta @object-properties-measures). Power BI no usa esta propiedad.

Esta expresión muestra el número de pedido, el cliente y el importe de cada fila de ventas:

```dax
SELECTCOLUMNS (
    Sales,
    "Order", Sales[OrderNumber],
    "Customer", RELATED ( Customer[Name] ),
    "Amount", Sales[Amount]
)
```

Consulta @detail-rows-expression. En Tabular Editor 3, escribe la expresión en el **Editor de expresiones** de @dax-editor, con autocompletado e información de parámetros. Para quitar la expresión, borra el valor.

### Comportamiento de indexación de Direct Lake

`DirectLakeIndexingBehavior` · DirectLakeIndexingBehavior · Opciones · nivel de compatibilidad de vista previa

Indica cuándo el motor genera y guarda los índices que usa para una tabla Direct Lake. Generar índices durante una actualización acelera las primeras consultas posteriores a la actualización, y generarlos bajo demanda acelera las actualizaciones. Se aplica solo a las tablas en modo Direct Lake.

El Tabular Object Model (TOM) todavía no ha asignado a esta propiedad un nivel de compatibilidad publicado; por eso, la vista **Properties** de la versión actual de Tabular Editor 3 la oculta en todos los modelos.

| Valor            | Significado                                                                                                                                                      |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Predeterminado` | Usa el valor predeterminado del modelo, configurado mediante **Default Direct Lake Indexing Behavior** en @object-properties-model. |
| `Automático`     | Crea índices en memoria durante la carga de datos o la ejecución de consultas cuando es necesario, tal como lo describe la biblioteca TOM.       |
| `Completo`       | El motor crea y guarda los índices como parte de una actualización completa, una actualización Calculate y una actualización de tipo indexes.    |
| `Explícito`      | El motor crea y guarda los índices solo cuando ejecutas una actualización de tipo indexes.                                                       |

<!-- TODO (not verifiable from TE3 source): the behavior of each value and which indexes this covers; check the Microsoft documentation once the feature is out of preview. -->

### Excluir de las agregaciones automáticas

`ExcludeFromAutomaticAggregations` · bool · Opciones · nivel de compatibilidad 1572+

Cuando es `true`, Power BI excluye la tabla al crear agregaciones automáticas. Las agregaciones automáticas son una característica de Power BI Premium y Fabric para modelos DirectQuery en la que el servicio crea tablas de agregación a partir de las consultas que recibe. Úsala en una tabla cuyos datos cambian con demasiada frecuencia para que una agregación en caché resulte útil.

<!-- TODO (not verifiable from TE3 source): the exact effect. TOM only says "An indication whether the table is excluded from the automatic aggregations feature." Is the table excluded as a source for aggregations, or are queries against it never answered from aggregations? -->

### Excluir de la actualización del modelo

`ExcludeFromModelRefresh` · bool · Opciones · nivel de compatibilidad 1480+

Cuando es `true`, una actualización del modelo completo omite las particiones de esta tabla si ya contienen datos. Las particiones sin datos se siguen actualizando, por lo que se cargará una tabla nueva o vaciada. Puedes seguir actualizando la tabla si la seleccionas explícitamente. Úsalo en tablas que cambian rara vez o que son costosas de cargar, como una tabla histórica grande o una tabla que un proceso independiente rellena.

En Analysis Services de SQL Server 2025, los tipos de actualización a nivel de modelo **Full**, **Automatic**, **Data only** y **Calculate** omiten la tabla cuando sus particiones contienen datos. **Clear values** sí borra los datos de la tabla, y la siguiente actualización del modelo vuelve a cargarla.

En Tabular Editor 3, puedes actualizar una sola tabla haciendo clic con el botón derecho sobre ella en el **Explorador TOM** y seleccionando **Refresh table**. Consulta @refresh-preview-query.

### Particiones

`Partitions` · colección de particiones · Opciones · solo lectura

Las particiones de la tabla. Cada partición define de dónde procede una parte de los datos de la tabla, por ejemplo, una expresión M, y puedes actualizar cada una por separado. La mayoría de las tablas tienen una sola partición. Las tablas de importación grandes suelen tener una partición por período, creada por ti o por una política de actualización incremental.

Haz clic en el botón de puntos suspensivos para abrir el editor de colecciones, donde puedes agregar, quitar y editar particiones. Consulta @object-properties-partitions sobre particiones.

La vista **Propiedades** muestra `Partitions` solo cuando la primera partición de la tabla es una partición M o una partición de consulta. Se oculta para tablas calculadas (incluidos los parámetros de campo), tablas de grupos de cálculo, tablas Direct Lake y tablas con particiones de rango de la directiva. Para ver y editar las particiones de las tablas calculadas y de las tablas de grupos de cálculo, ejecuta el script @script-edit-hidden-partitions.

### Privado

`IsPrivate` · bool · Opciones

Cuando es `true`, las herramientas cliente no muestran la tabla, ni siquiera a los desarrolladores que activan los objetos ocultos. Power BI Desktop la establece en la plantilla de tabla de fechas de la característica de fecha/hora automática (la tabla llamada `DateTableTemplate_` seguida de un GUID). Siempre está disponible en los modelos de Power BI y requiere el nivel de compatibilidad 1400 o superior en los modelos de Analysis Services.

En Power BI Desktop, una tabla privada no aparece en absoluto en el panel **Datos**, mientras que una tabla oculta sí puede mostrarse allí. SQL Server 2025 Analysis Services almacena el indicador y no actúa en consecuencia. En ambos casos, la tabla sigue apareciendo en la información de esquema que devuelve el motor, puedes consultarla con DAX y las medidas de otras tablas pueden usarla.

> [!NOTE]
> `IsPrivate` e `IsHidden` no son características de seguridad. Para proteger una tabla, usa la seguridad a nivel de objetos (consulta [Seguridad a nivel de objetos](#object-level-security)).

La regla de BPA @kb.bpa-remove-auto-date-table marca las tablas `DateTableTemplate_` y `LocalDateTable_` que crea la característica de fecha/hora automática, para que puedas reemplazarlas por una única tabla de fechas.

### Conjuntos

`Sets` · colección de Set · Opciones · solo lectura · nivel de compatibilidad 1400+

Los conjuntos calculados definidos en la tabla. Un conjunto es una expresión DAX con nombre que devuelve un conjunto de miembros, y las herramientas cliente pueden mostrarlo como una selección predefinida. Los conjuntos solo se admiten en modelos de Power BI: la vista **Propiedades** muestra `Sets` cuando el modo de compatibilidad del modelo es Power BI y el nivel de compatibilidad es 1400 o superior. Los conjuntos no aparecen como objetos en el **Explorador TOM**, por lo que se agregan y editan en el editor de colecciones de esta propiedad. Consulta @object-properties-functions.

<!-- TODO (not verifiable from TE3 source): what calculated sets are used for, and which client tools support them. -->

### Mostrar solo como variaciones

`ShowAsVariationsOnly` · bool · Opciones

Cuando es `true`, las herramientas cliente muestran la tabla en la lista de campos solo a través de una variación de columna que apunta a ella. Power BI Desktop lo establece en las tablas de fechas que crea la característica de fecha/hora automática (las tablas llamadas `LocalDateTable_` seguido de un GUID), que aparecen como la jerarquía de fechas bajo una columna de fecha. Consulta `Variations` en @object-properties-columns.

Siempre está disponible en los modelos de Power BI y requiere un nivel de compatibilidad 1400 o superior en los modelos de Analysis Services. SQL Server 2025 Analysis Services almacena la marca, pero no la aplica: la tabla sigue apareciendo en la información del esquema que leen las herramientas cliente, puedes consultarla con DAX y las medidas de otras tablas pueden usarla.

### Administrado por el sistema

`SystemManaged` · bool · Opciones · nivel de compatibilidad 1562+

Cuando es `true`, el motor o el servicio crea y elimina la tabla. No establezcas esta propiedad en tus propias tablas ni edites una tabla administrada por el sistema: Tabular Editor no bloquea esas ediciones.

Las tablas de fecha/hora automáticas que crea Power BI Desktop no están administradas por el sistema. Desktop establece `IsHidden` e `IsPrivate` en la tabla de plantilla, y `IsHidden` y `ShowAsVariationsOnly` en cada tabla de fecha local.

<!-- TODO (not verifiable from TE3 source): which features create system-managed tables, for example automatic aggregations. -->

### Seguridad a nivel de objeto

`ObjectLevelSecurity` · por rol · traducciones, perspectivas, seguridad · nivel de compatibilidad 1400+ · _acceso directo a_ los permisos de tabla de cada rol

El permiso de seguridad a nivel de objetos (OLS) de la tabla en cada rol del modelo. Expande la propiedad para ver una entrada por rol. La vista **Propiedades** muestra la propiedad solo cuando el modelo tiene al menos un rol. Tabular Editor almacena este permiso en el permiso de tabla de cada rol.

| Valor            | Significado                                                                                                                                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Predeterminado` | No hay ningún permiso establecido para este rol. Los miembros del rol pueden ver la tabla.                                                                                  |
| `Lectura`        | Los miembros del rol pueden ver y consultar la tabla.                                                                                                                                       |
| `Ninguno`        | La tabla y todo lo que depende de ella quedan ocultos para los miembros del rol. Las consultas y las medidas que hacen referencia a la tabla devuelven un error para ellos. |

Con `Ninguno`, la tabla y sus metadatos no existen para los miembros del rol, por lo que cualquier medida que haga referencia a la tabla produce un error para ellos. Consulta @data-security-setup-ols y @object-properties-security. Para comprobar que OLS y la seguridad a nivel de filas funcionan según lo previsto, pruébalas mediante suplantación en Tabular Editor 3. Consulta @data-security-testing.

### Seguridad a nivel de filas

`RowLevelSecurity` · por rol · Traducciones, Perspectivas, Seguridad · de solo lectura · _acceso directo a_ los permisos de tabla de cada rol

El filtro de seguridad a nivel de filas (RLS) de la tabla en cada rol del modelo. Expande la propiedad para ver una entrada por rol. Cada entrada es una expresión DAX que devuelve `TRUE` para las filas que pueden ver los miembros del rol, por ejemplo:

```dax
Customer[Country] = "Denmark"
```

La propiedad en sí es de solo lectura y editas la entrada de cada rol, que admite expresiones de varias líneas. La vista **Propiedades** muestra la propiedad solo cuando el modelo tiene al menos un rol. Tabular Editor almacena el filtro en el permiso de tabla de cada rol.

Una entrada vacía no aplica ningún filtro a la tabla para ese rol. Los filtros se propagan a través de las relaciones, de modo que un filtro en una tabla de dimensiones también filtra las tablas de hechos relacionadas con ella. Consulta @roles-and-rls, @data-security-setup-rls y @object-properties-security para obtener más información sobre el rol.

## Tabla calculada

Una tabla calculada obtiene sus datos de una expresión DAX; por ejemplo, una tabla de fechas creada con [CALENDAR](https://dax.guide/calendar) o una tabla que resume otra tabla. El motor evalúa la expresión al actualizar la tabla o el modelo y almacena el resultado como cualquier otra tabla importada.

Una tabla calculada tiene todas las propiedades de una [tabla](#table), además de `Expression`. Tiene exactamente una partición, que administra Tabular Editor, y no puede tener una política de actualización incremental. La vista **Propiedades** oculta `Partitions`, `Source`, `SourceType`, `EnableRefreshPolicy` y `RefreshPolicy` en las tablas calculadas y muestra `AlternateSourcePrecedence`.

Los parámetros de campo de Power BI son tablas calculadas. El script @create-field-parameter crea uno a partir de las columnas o medidas que selecciones.

### Propiedades comunes

Lo mismo que en las [tablas](#table).

### Expresión

`Expression` · string · Opciones · _acceso directo a_ la expresión de la partición calculada de la tabla

La expresión DAX que devuelve las filas de la tabla. Debe devolver una tabla, por ejemplo:

```dax
ADDCOLUMNS (
    CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2030, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month", FORMAT ( [Date], "mmm" )
)
```

Cada columna que devuelve la expresión se convierte en una columna de una tabla calculada (consulta @object-properties-columns). Agregar, quitar o cambiar el nombre de las columnas de esta manera afecta a otras expresiones DAX que hacen referencia a la tabla y a las jerarquías que usan sus columnas.

En Tabular Editor 3, las columnas cambian en cuanto cambias la expresión. Tabular Editor 3 las determina mediante su propio análisis semántico de DAX, que también funciona al editar un archivo de modelo sin conexión a Analysis Services o Power BI (consulta @creating-and-testing-dax). Tabular Editor 2 actualiza las columnas solo cuando guardas el modelo en una base de datos a la que estás conectado, recargando las columnas de la tabla desde el servidor después de guardar. Al editar un archivo de modelo en Tabular Editor 2, las columnas no cambian con la expresión.

Edita la expresión en el **Editor de expresiones**. En Tabular Editor 3, el **Editor de expresiones** de @dax-editor incluye autocompletado e información de parámetros. El motor vuelve a calcular los datos de la tabla cuando se actualiza la tabla y cuando se actualiza cualquier tabla de la que dependa. Después de cambiar la expresión, actualiza la tabla antes de usarla en un Report. Consulta [Actualización de datos](xref:refresh-preview-query#refreshing-data).

## Tabla de grupo de cálculo

Una tabla de grupo de cálculo contiene un grupo de cálculo. Tiene una columna con los nombres de los elementos de cálculo y, normalmente, una columna ordinal que establece el orden de los elementos. Los autores usan la columna como cualquier otra, por ejemplo, en una segmentación de datos, y el elemento de cálculo seleccionado cambia la forma en que se calculan las medidas del Report. Consulta @object-properties-calculation-groups para ver las propiedades del grupo de cálculo y sus elementos de cálculo.

Microsoft documenta los grupos de cálculo para el nivel de compatibilidad 1500 o superior, lo que incluye todos los modelos semánticos de Power BI. Tabular Editor 3 muestra **Crear > Grupo de cálculo** a partir del nivel de compatibilidad 1470, el nivel en el que TOM agregó los grupos de cálculo.

Una tabla de grupo de cálculo tiene las siguientes propiedades, además de las propiedades comunes. La mayoría son accesos directos a las propiedades del grupo de cálculo de la tabla, que no puedes seleccionar en el **Explorador TOM**. De las demás propiedades de tabla, la vista **Propiedades** solo muestra `TableGroup` y `DefaultDetailRowsExpression`. Los grupos de cálculo no admiten expresiones de filas de detalle, seguridad a nivel de filas ni seguridad a nivel de objetos, así que deja `DefaultDetailRowsExpression` vacío.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Oculto](xref:object-properties-common#hidden)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Nombres traducidos](xref:object-properties-common#translated-names)
- [Descripciones traducidas](xref:object-properties-common#translated-descriptions)
- [Mostrado en perspectiva](xref:object-properties-common#shown-in-perspective)

### Grupo de tablas

`TableGroup` · cadena · Básico · _almacenado como anotación_ (`TabularEditor_TableGroup`)

Igual que [Grupo de tablas](#table-group) en una tabla.

### Descripción del grupo de cálculo

`CalculationGroupDescription` · cadena · Básico · _acceso directo a_ la **Descripción** del grupo de cálculo

La descripción almacenada en el grupo de cálculo, independiente de la `Description` de la propia tabla. Las herramientas cliente no la muestran. Al pasar el cursor sobre una tabla de grupo de cálculo en el panel **Datos** de Power BI Desktop, aparece la `Description` de la tabla, mientras que la lista de campos de Excel no muestra ninguna descripción. Pon el texto para los autores de Report en la `Description` de la tabla y usa esta propiedad para notas destinadas a otros desarrolladores.

### Precedencia del grupo de cálculo

`CalculationGroupPrecedence` · int · Básico · _acceso directo a_ la **Precedencia** del grupo de cálculo

El orden en que se aplica el grupo de cálculo cuando una consulta utiliza más de un grupo de cálculo. Consulta `Precedence` en @object-properties-calculation-groups.

### Anotaciones del grupo de cálculo

`CalculationGroupAnnotations` · colección de pares de nombre/valor · Metadatos · solo de lectura · _acceso directo a_ las **Annotations** del grupo de cálculo

Las anotaciones almacenadas en el grupo de cálculo. La tabla tiene sus propias anotaciones (consulta [Anotaciones](xref:object-properties-common#annotations)). La propiedad en sí es de solo lectura. Haz clic en el botón de puntos suspensivos para abrir el editor de anotaciones, donde puedes agregar, modificar y quitar las anotaciones. Esto solo funciona con una tabla de grupo de cálculo seleccionada a la vez.

### Expresión de selección múltiple o vacía

`MultipleOrEmptySelectionExpression` · cadena · Opciones · nivel de compatibilidad 1605+ · _acceso directo al_ grupo de cálculo

Una expresión DAX que el motor evalúa en lugar de la medida cuando el filtro del grupo de cálculo selecciona más de un elemento de cálculo o no selecciona ninguno porque el filtro no coincide con ningún elemento. Usa [SELECTEDMEASURE](https://dax.guide/selectedmeasure) para hacer referencia a la medida. En niveles de compatibilidad inferiores a 1605, la vista **Propiedades** oculta esta propiedad y las demás propiedades de expresión de selección que aparecen a continuación. Para quitar la expresión, borra el valor.

Cuando la expresión está vacía, el grupo de cálculo no se aplica en esos casos, y [Comportamiento de la expresión de selección](xref:object-properties-model#selection-expression-behavior) en el modelo define qué devuelven las medidas:

- `Automatic` o `NonVisual`: el valor normal de la medida
- `Visual`: un valor en blanco

Un valor normal puede confundir a los usuarios; por ejemplo, cuando un usuario selecciona dos monedas en un grupo de cálculo de conversión de divisas y ve un total que no está en ninguna de las dos monedas. Esta expresión devuelve un mensaje de error:

```dax
ERROR ( "Select a single currency." )
```

Esta expresión devuelve un valor en blanco:

```dax
BLANK ()
```

En Tabular Editor 3, escribes la expresión en el **Editor de expresiones** del @dax-editor, con autocompletado e información de parámetros.

### Descripción de la expresión de selección múltiple o vacía

`MultipleOrEmptySelectionDescription` · cadena · Opciones · nivel de compatibilidad 1605+ · _acceso directo al_ grupo de cálculo

Una descripción de la expresión de selección múltiple o vacía para otros desarrolladores. Las herramientas de cliente no se lo muestran a los autores de Report.

### Expresión de cadena de formato dinámica para selección múltiple o vacía

`MultipleOrEmptySelectionFormatStringExpression` · cadena · Opciones · nivel de compatibilidad 1605+ · _acceso directo al_ grupo de cálculo

Una expresión DAX que devuelve la cadena de formato que se debe usar cuando se aplica la expresión de selección múltiple o vacía. Funciona como `FormatStringExpression` en un elemento de cálculo. Dentro de la expresión, [SELECTEDMEASUREFORMATSTRING](https://dax.guide/selectedmeasureformatstring) devuelve la cadena de formato de la medida.

### Expresión sin selección

`NoSelectionExpression` · cadena · Opciones · nivel de compatibilidad 1605+ · _acceso directo al_ grupo de cálculo

Una expresión DAX que el motor evalúa en lugar de la medida cuando no hay ningún filtro en el grupo de cálculo; es decir, cuando el usuario no ha seleccionado ningún elemento de cálculo. Cuando está vacía, las medidas devuelven su valor normal si no se selecciona nada. Úsala para establecer un cálculo predeterminado que los usuarios pueden reemplazar al seleccionar un elemento de cálculo. Las expresiones sin selección requieren el nivel de compatibilidad 1605 o superior.

En este ejemplo de conversión de divisas, los importes de ventas se almacenan en dólares estadounidenses y una tabla `Currency Rate` contiene los tipos de cambio diarios. La expresión convierte los importes a la divisa seleccionada en una tabla `Currency`, sin que el usuario tenga que seleccionar un elemento de cálculo:

```dax
IF (
    SELECTEDVALUE ( 'Currency'[CurrencyName], "US Dollar" ) = "US Dollar",
    SELECTEDMEASURE (),
    SUMX (
        VALUES ( 'Date'[Date] ),
        CALCULATE ( DIVIDE ( SELECTEDMEASURE (), MAX ( 'Currency Rate'[EndOfDayRate] ) ) )
    )
)
```

### Descripción de la expresión sin selección

`NoSelectionExpressionDescription` · cadena · Opciones · nivel de compatibilidad 1605+ · _acceso directo al_ grupo de cálculo

Una descripción de la expresión sin selección, para otros desarrolladores. Las herramientas de cliente no se lo muestran a los autores de Report.

### Expresión de cadena de formato dinámica sin selección

`NoSelectionFormatStringExpression` · cadena · Opciones · nivel de compatibilidad 1605+ · _acceso directo al_ grupo de cálculo

Una expresión DAX que devuelve la cadena de formato que se debe usar cuando se aplica la expresión sin selección. Funciona como `FormatStringExpression` en un elemento de cálculo. Dentro de la expresión, [SELECTEDMEASUREFORMATSTRING](https://dax.guide/selectedmeasureformatstring) devuelve la cadena de formato de la medida.
