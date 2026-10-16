---
uid: object-properties
title: Referencia de propiedades de los objetos
author: Jeroen ter Heerdt
updated: 2026-10-05
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

# Referencia de propiedades de los objetos

<!--
SUMMARY: Reference for every property that Tabular Editor shows in the Properties view, grouped by object type.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Todos los objetos de un modelo semántico, como una tabla, una columna o una medida, tienen un conjunto de propiedades. Estas propiedades proceden del Tabular Object Model (TOM), el modelo de objetos que Analysis Services, Power BI y Fabric usan para definir modelos semánticos. La @properties-view las muestra y los C# Scripts las leen y las escriben mediante el @api-index.

Esta referencia describe cada propiedad que muestra la vista de propiedades. Cuando Tabular Editor incluye una funcionalidad para una propiedad, como un editor, una regla de Best Practice Analyzer (BPA) o un C# Script, la entrada incluye un enlace a ella.

Para cambiar una propiedad, selecciona uno o varios objetos en la @tom-explorer-view y edita el valor en la vista de propiedades. Cuando seleccionas varios objetos, el nuevo valor se aplica a todos ellos. Consulta @editing-properties.

## Cómo se organiza esta referencia

@object-properties-common describe las propiedades que tienen la mayoría de los objetos, como `Name`, `Description` y `Annotations`. Cada una de las demás páginas trata una familia de objetos relacionados:

| Página                                                | Objetos                                                                                                                                    |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| @object-properties-common                | Propiedades compartidas por la mayoría de los objetos                                                                                      |
| @object-properties-model                 | Modelo                                                                                                                                     |
| @object-properties-tables                | Tabla, tabla calculada, tabla del grupo de cálculo                                                                                         |
| @object-properties-columns               | Columna de datos, columna calculada, columna de tabla calculada, alternativa de, variación                                                 |
| @object-properties-measures              | Medida, KPI                                                                                                                                |
| @object-properties-calculation-groups    | Grupo de cálculo, elemento de cálculo                                                                                                      |
| @object-properties-hierarchies           | Jerarquía, nivel                                                                                                                           |
| @object-properties-relationships         | Relación                                                                                                                                   |
| @object-properties-partitions            | Partición, partición M, partición de entidad, partición de rango de directiva, política de actualización, definición de cobertura de datos |
| @object-properties-data-sources          | Data source de proveedor y origen de datos estructurado, expresión compartida, Query Group, sugerencia de vinculación de datos             |
| @object-properties-security              | Rol, permiso de tabla, miembros del rol                                                                                                    |
| @object-properties-perspectives-cultures | Perspectiva, configuración regional                                                                                                        |
| @object-properties-calendars             | Calendario, grupo de columnas relacionadas con el tiempo, asociación de columnas de unidad de tiempo                                       |
| @object-properties-functions             | Función definida por el usuario, conjunto                                                                                                  |

Cada página tiene una sección para cada objeto. La sección comienza con enlaces a las propiedades comunes del objeto y, a continuación, incluye una entrada por cada propiedad. Dentro de cada objeto, las propiedades se enumeran por categoría, en el orden en que la vista de propiedades las muestra cuando se selecciona **Categorizado**. Las categorías son:

- **Básico**: las propiedades que se modifican con más frecuencia, como el nombre, la descripción y la cadena de formato.
- **Metadatos**: información sobre el objeto, como el tipo de objeto o los mensajes de error. La mayoría de estas propiedades son de solo lectura.
- **Opciones**: propiedades que cambian el comportamiento del objeto, como las expresiones, la agregación o el orden de clasificación.
- **Traducciones, Perspectivas, Seguridad**: traducciones por configuración regional, pertenencia a perspectivas y configuración de seguridad por rol.

Algunos objetos tienen otras categorías, como **Opciones de acceso a datos** en el modelo.

El encabezado de cada entrada es el nombre de la propiedad tal como aparece en la vista de propiedades. La línea debajo del encabezado indica el nombre TOM de la propiedad, su tipo y su categoría:

> **Nombre para mostrar**
> `TomName` · tipo · Categoría

El nombre TOM es el nombre que usas en un C# Script. Para algunas propiedades, el Tabular Model Definition Language (TMDL) usa otro nombre. Por ejemplo, TMDL guarda la `FormatStringExpression` de una medida como `formatStringDefinition`.

Cuando se aplican, estas partes van después de la categoría, en este orden:

- **solo lectura**: no se puede cambiar el valor.
- **nivel de compatibilidad NNNN+**: el nivel de compatibilidad mínimo del modelo, por ejemplo `nivel de compatibilidad 1540+`.
- un marcador para una propiedad que añade Tabular Editor. Consulta [Propiedades que añade Tabular Editor](#properties-that-tabular-editor-adds).

Por ejemplo, la entrada para la etiqueta de linaje empieza así:

> **etiqueta de linaje**
> `LineageTag` · string · Opciones · nivel de compatibilidad 1540+

## Propiedades que dependen del modelo

La vista de propiedades oculta las propiedades que no se aplican al modelo actual. Las propiedades que aparecen dependen de:

- el nivel de compatibilidad del modelo. Muchas propiedades requieren un nivel mínimo; por ejemplo, `LineageTag` requiere 1540 o superior. Para ver o cambiar el nivel de compatibilidad, selecciona el modelo y expande `Database` en la vista de propiedades.
- el modo de compatibilidad del modelo. Algunas propiedades existen solo para modelos de Power BI y Fabric, o solo para modelos de Analysis Services.
- el estado del objeto. Algunas propiedades solo aparecen cuando otra propiedad tiene un valor determinado. Por ejemplo, las propiedades de una política de actualización solo aparecen cuando la tabla tiene una configurada.

## Propiedades que agrega Tabular Editor

Casi todas las propiedades de la vista de propiedades son propiedades TOM: se guardan en el modelo y son visibles para cualquier herramienta que lo lea. Tabular Editor agrega algunas propiedades propias. La línea de metadatos las marca así:

| Marcador                        | Significado                                                                                                                                                                             | ¿Se guarda en el modelo?                           |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| _calculado_                     | Tabular Editor calcula el valor para mostrarlo, por ejemplo `DaxObjectFullName` o `ObjectTypeName`.                                                                     | No                                                 |
| _acceso directo a …_            | Muestra o edita una propiedad TOM de otro objeto. Por ejemplo, `SourceType` en una tabla muestra el tipo de origen de la primera partición de la tabla. | Sí, como la propiedad TOM a la que hace referencia |
| _almacenado como una anotación_ | Tabular Editor guarda el valor en una anotación del objeto, por ejemplo `TableGroup`.                                                                                   | Sí, como una anotación que solo Tabular Editor lee |

## Ver también

- @properties-view
- @tom-explorer-view
- @editing-properties
- @best-practice-analyzer
- @csharp-scripts
- @api-index
