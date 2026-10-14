---
uid: object-properties-relationships
title: Propiedades de la relación
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

# Propiedades de la relación

<!--
SUMMARY: Reference for the properties of relationships, such as cardinality, cross filtering behavior and security filtering behavior.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Esta página describe las propiedades de las relaciones. Para ver las propiedades comunes a la mayoría de los objetos, consulta @object-properties-common.

## Relación

Una relación conecta una columna de una tabla con una columna de otra tabla, y un filtro aplicado a una tabla también filtra la otra. Por ejemplo, una relación de `Sales[ProductKey]` a `Product[ProductKey]` hace que un filtro en `Product[Color]` filtre las filas de `Sales`.

Toda relación tiene un lado _de origen_ y un lado _de destino_. En una relación típica de uno a varios, el lado de origen es la tabla con muchas filas por clave, como una tabla de hechos, y el lado de destino es la tabla con una fila por clave, como una tabla de dimensiones.

Tabular Editor 3 muestra una relación en el **Explorador TOM** con la columna de origen a la izquierda y la columna de destino a la derecha, por ejemplo `'Sales'[ProductKey] ∞←1 'Product'[ProductKey]`. Los símbolos del centro muestran la cardinalidad de cada lado (`∞` para `Many`, `1` para `One`) y la dirección del filtro (`←` para una sola dirección, `↔` para ambas direcciones). El nombre se actualiza cuando cambias las columnas, las cardinalidades o el comportamiento de filtrado cruzado. Tabular Editor 2 usa el mismo orden de columnas sin símbolos de cardinalidad, y su flecha muestra la dirección del filtro como `-->` para una sola dirección o `<-->` para ambas direcciones; por ejemplo, `'Sales'[ProductKey] --> 'Product'[ProductKey]`.

Puedes crear y editar relaciones en la vista **Propiedades** o, en Tabular Editor 3, en @diagram-view. Para crear relaciones a partir de las claves primarias y externas definidas en Databricks Unity Catalog, usa el script @script-create-databricks-relationships.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Propiedades modificadas](xref:object-properties-common#changed-properties)
- [Mensaje de error](xref:object-properties-common#error-message)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Estado](xref:object-properties-common#state)

### Columna de origen

`FromColumn` · Columna · Básico

La columna del lado de origen de la relación. En una relación de uno a varios, suele ser la columna de clave externa de la tabla de hechos, por ejemplo `Sales[ProductKey]`. Al elegir una columna, también se establece `FromTable`.

### Cardinalidad de origen

`FromCardinality` · Cardinalidad de extremo de relación · Básico

Cuántas filas del lado de origen pueden tener el mismo valor en `FromColumn`.

| Valor  | Significado                                                                                                                                                                                                                            |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Many` | Varias filas pueden tener el mismo valor. Es la configuración habitual para el lado de origen.                                                                                                         |
| `One`  | Cada valor aparece como máximo una vez en la columna.                                                                                                                                                                  |
| `None` | La cardinalidad no está especificada. No lo use. El cuadro de diálogo de la relación en Tabular Editor 3 solo muestra `One` y `Many`, y el **Explorador TOM** muestra `None` como `0`. |

### Columna de destino

`ToColumn` · Columna · Básico

La columna del lado de destino de la relación. En una relación de uno a muchos, esta es la columna clave de la tabla de dimensiones, por ejemplo `Product[ProductKey]`. Al elegir una columna, también se establece `ToTable`.

La regla @kb.bpa-relationship-same-datatype del Best Practice Analyzer (BPA) señala las relaciones en las que `FromColumn` y `ToColumn` tienen tipos de datos diferentes.

### Cardinalidad de destino

`ToCardinality` · RelationshipEndCardinality · Básico

Cuántas filas del lado de destino pueden tener el mismo valor en `ToColumn`. Los valores son los mismos que en `FromCardinality`, y `One` es la configuración habitual. Las dos cardinalidades juntas definen el tipo de relación:

| Desde  | Hasta  | Relación                                                                                                                                                               |
| ------ | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Many` | `One`  | Muchos a uno. La relación estándar entre una tabla de hechos y una tabla de dimensiones.                                               |
| `One`  | `One`  | Uno a uno. Ambas columnas deben contener valores únicos.                                                                               |
| `Many` | `Many` | Muchos a muchos. Ninguna de las columnas necesita valores únicos. Requiere un nivel de compatibilidad 1500 o superior. |

Cuando una columna del lado `One` contiene valores duplicados, la actualización falla con un error. Las relaciones de muchos a muchos son relaciones _limitadas_: no agregan una fila en blanco para las claves que faltan y a menudo son más lentas que las relaciones de muchos a uno. Úsalas solo cuando los datos no tengan una clave única.

En el Tabular Object Model (TOM), el extremo "from" siempre es el lado "muchos" en una relación de uno a varios. Tabular Editor acepta `FromCardinality` `One` con `ToCardinality` `Many`, pero el motor lo rechaza al guardar con el error "From end cardinality must always be set to Many, unless la relación is One-To-One". Para relacionar las tablas en el otro sentido, intercambia las columnas de origen y de destino.

### Activo

`IsActive` · bool · Básico

Si la relación filtra los datos automáticamente. El motor rechaza un modelo en el que las relaciones activas crean más de una ruta entre dos tablas. Esto ocurre con más frecuencia cuando varias relaciones usan filtrado cruzado bidireccional.

Para una segunda relación entre las mismas tablas, por ejemplo de `Sales[ShipDate]` a `Date[Date]` junto a la activa de `Sales[OrderDate]`, establece `IsActive` en `false` y activa la relación en una medida con [USERELATIONSHIP](https://dax.guide/userelationship):

```dax
Sales by Ship Date =
CALCULATE ( [Total Sales], USERELATIONSHIP ( Sales[ShipDate], 'Date'[Date] ) )
```

En la Vista de diagrama de Tabular Editor 3, también puedes hacer clic con el botón derecho en una relación para activarla o desactivarla.

### ID

`ID` · string · Básico · solo de lectura

El identificador interno de la relación, que en TOM es el nombre de la relación. Power BI Desktop usa un GUID. Tabular Editor 3 y Tabular Editor 2 asignan a una relación nueva un nombre único que comienza por `New Single Column Relationship`. Usa el ID para referirte a una relación concreta en un C# Script o en un comando de Tabular Model Scripting Language (TMSL).

### Tabla de origen

`FromTable` · Tabla · Opciones · solo lectura

La tabla que contiene `FromColumn`. Para cambiarla, elige otra `FromColumn`. Tabular Editor 3 oculta esta propiedad en la vista **Propiedades**, donde `FromColumn` ya muestra la tabla. Aun así, puedes consultarla en un C# Script.

### Tabla de destino

`ToTable` · Tabla · Opciones · solo de lectura

La tabla que contiene `ToColumn`. Para cambiarla, selecciona otra `ToColumn`. Tabular Editor 3 oculta esta propiedad en la vista **Properties**. Aún puedes leerla en un C# Script.

### Comportamiento del filtrado cruzado

`CrossFilteringBehavior` · CrossFilteringBehavior · Opciones

La dirección en la que los filtros fluyen a través de la relación.

| Valor            | Significado                                                                                                                                                                                                                                                |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OneDirection`   | Un filtro en la tabla de destino filtra la tabla de origen. Por ejemplo, un filtro en `Product` filtra `Sales`. El valor predeterminado.                                                                   |
| `BothDirections` | Los filtros se propagan en ambas direcciones. Un filtro en `Sales` también filtra `Product`, por lo que un segmentador de datos en `Product` solo muestra los productos que tienen ventas en el contexto de filtro actual. |
| `Automatic`      | El motor analiza las relaciones y elige uno de los otros comportamientos mediante heurísticas.                                                                                                                                             |

SQL Server 2025 Analysis Services y Power BI Desktop almacenan una relación guardada con `Automatic` como `BothDirections`. En Power BI Desktop, un filtro en la tabla de origen también filtra la tabla de destino, igual que con `BothDirections`. Establece `BothDirections` explícitamente cuando quieras que los filtros se propaguen en ambas direcciones.

`BothDirections` ralentiza las consultas y aumenta la probabilidad de que las relaciones activas creen más de una ruta entre dos tablas, algo que el motor rechaza. Para filtrar en ambas direcciones en una sola medida, mantén la relación unidireccional y usa [CROSSFILTER](https://dax.guide/crossfilter) en la medida, por ejemplo `CROSSFILTER ( Sales[ProductKey], Product[ProductKey], BOTH )`.

El filtrado bidireccional solo se aplica a la seguridad a nivel de filas cuando también estableces `SecurityFilteringBehavior`. La regla de BPA @kb.bpa-many-to-many-single-direction marca las relaciones de muchos a muchos que filtran en ambas direcciones.

### Comportamiento del filtrado de seguridad

`SecurityFilteringBehavior` · SecurityFilteringBehavior · Opciones

La dirección en la que los filtros de seguridad a nivel de filas se propagan a través de la relación. Corresponde a **Aplicar filtro de seguridad en ambas direcciones** en Power BI Desktop.

| Valor            | Significado                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OneDirection`   | Los filtros de seguridad se propagan solo de la tabla de destino a la tabla de origen, incluso cuando `CrossFilteringBehavior` es `BothDirections`. El valor predeterminado.                                                                                                                                                                                            |
| `BothDirections` | Los filtros de seguridad se propagan en ambas direcciones. Válido solo cuando `CrossFilteringBehavior` es `BothDirections`.                                                                                                                                                                                                                                             |
| `None`           | Impide que los filtros de seguridad se propaguen del lado uno al lado muchos. Se aplica solo a relaciones limitadas en un modelo compuesto, donde una tabla procede de un modelo semántico de Power BI o de una base de datos de Analysis Services, y la otra procede de un Data source diferente. Requiere el nivel de compatibilidad 1561 o superior. |

Tabular Editor acepta `BothDirections` cuando `CrossFilteringBehavior` es `OneDirection`, pero el motor lo rechaza al guardar, con el error "cannot have SecurityFilterBehavior set to BothDirections when the CrossFilterBehavior is set to OneDirection". El mismo error se produce cuando vuelves a cambiar `CrossFilteringBehavior` a `OneDirection` en una relación que filtra la seguridad en ambas direcciones, así que cambia primero `SecurityFilteringBehavior`.

Un uso típico de `BothDirections` es la seguridad a nivel de filas dinámica, donde un filtro de una tabla de usuarios llega a una tabla de dimensiones a través de una tabla puente. Consulta @roles-and-rls y @data-security-setup-rls. Para comprobar que los filtros de seguridad llegan a las tablas correctas, prueba el rol mediante suplantación de identidad. Consulta @data-security-testing.

### Comportamiento de combinación por fecha

`JoinOnDateBehavior` · DateTimeRelationshipBehavior · Opciones

Cómo el motor hace coincidir los valores cuando ambas columnas tienen el tipo de datos `DateTime`.

| Valor          | Significado                                                                                                                                                                             |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DateAndTime`  | Los valores deben coincidir tanto en la fecha como en la hora. El valor predeterminado.                                                                 |
| `DatePartOnly` | El motor compara solo la parte de la fecha e ignora la hora. Por ejemplo, `2026-09-23 14:30` coincide con la fecha `2026-09-23` en una tabla de fechas. |

Use `DatePartOnly` cuando la columna de origen contenga una fecha y una hora, y la columna de destino sea una tabla de fechas con una fila por día. Con `DateAndTime`, solo coinciden los valores que sean exactamente a medianoche. Power BI Desktop usa `DatePartOnly` para las relaciones entre una columna de fecha/hora y su tabla automática de fecha/hora.

<!-- TODO (not verifiable from TE3 source): whether DatePartOnly works in DirectQuery. -->

### Confiar en la integridad referencial

`RelyOnReferentialIntegrity` · bool · Opciones

Para DirectQuery: cuando `true`, el motor asume que todos los valores de `FromColumn` existen en `ToColumn`, y las consultas SQL que envía al origen usan `INNER JOIN`. Cuando `false`, se utiliza `OUTER JOIN`. `INNER JOIN` suele ser más rápido. Coincide con **Asumir integridad referencial** en Power BI Desktop. La propiedad no tiene efecto en las tablas de importación.

Habilítela solo cuando el origen garantice que cada clave tenga una coincidencia, por ejemplo, mediante una restricción de clave externa. Si hay filas en el lado de origen sin coincidencia, faltarán en los resultados sin que se produzca ningún error.

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM documentation says this property is "unused; reserved for future use", while the TOM library's own description (shown in Tabular Editor) says DirectQuery queries use INNER JOIN when it's true. Confirm which engines and storage modes honor it. -->

### Tipo

`Type` · RelationshipType · Opciones · de solo lectura

El tipo de relación. El único valor es `SingleColumn`, una relación entre una columna de cada lado. Tabular Editor 3 oculta esta propiedad en la vista **Propiedades**.
