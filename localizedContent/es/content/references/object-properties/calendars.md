---
uid: object-properties-calendars
title: Propiedades del calendario
author: Jeroen ter Heerdt
updated: 2026-10-05
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.23.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Propiedades del calendario

<!--
SUMMARY: Reference for the properties of calendars, time unit column associations and time-related column groups, used by calendar-based time intelligence.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

En esta página se enumeran las propiedades de los calendarios y de los dos tipos de grupos de columnas que componen un calendario. Para las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

Los calendarios son los objetos que hay detrás de la _inteligencia temporal basada en calendarios_, también conocida como _inteligencia temporal mejorada_. Un calendario indica a las funciones de inteligencia temporal de DAX qué columnas de una tabla de fechas contienen el año, el trimestre, el mes, la semana, etc. Con un calendario, funciones como `TOTALYTD` y `DATEADD` funcionan con calendarios fiscales, minoristas (4-4-5) y otros calendarios no gregorianos, y se habilitan funciones basadas en semanas como `TOTALWTD`.

Un calendario se compone de grupos de columnas:

- una **asociación de columnas de unidad de tiempo** asigna una columna y, opcionalmente, algunas columnas asociadas a una unidad de tiempo como **Año** o **Mes del año**
- un **grupo de columnas relacionadas con el tiempo** enumera columnas relacionadas con el tiempo sin pertenecer a una única unidad de tiempo, como un indicador `IsHoliday`

Los tres objetos requieren un nivel de compatibilidad 1701 o superior. En Tabular Editor 3, el **Editor de calendario** muestra todo el calendario en una sola cuadrícula y resalta los errores en él mientras trabajas. Consulta @calendars.

## Calendario

Un calendario pertenece a una tabla, normalmente la tabla de fechas, y define una forma de dividir el tiempo, por ejemplo `Gregorian` o `Fiscal`. Una tabla puede tener más de un calendario. En DAX, se hace referencia a un calendario por su nombre en lugar de una columna de fecha, por ejemplo:

```dax
TOTALYTD ( [Sales Amount], 'Fiscal' )
```

Los nombres de los calendarios deben ser únicos en todo el modelo.

La regla @kb.bpa-date-table-exists del Best Practice Analyzer (BPA) señala un modelo que no tiene ningún calendario ni ninguna tabla de fechas marcada.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Etiqueta de linaje](xref:object-properties-common#lineage-tag)
- [Etiqueta de linaje de origen](xref:object-properties-common#source-lineage-tag)

### Grupos de columnas del calendario

`CalendarColumnGroups` · CalendarColumnGroupCollection · Básico · solo lectura

Los grupos de columnas que componen el calendario; es decir, las asociaciones de columnas con unidades de tiempo y los grupos de columnas relacionados con el tiempo. Este es el nombre de la colección en el Tabular Object Model (TOM). La **vista de propiedades** muestra la misma colección con el nombre de `ColumnMappings`. En un C# Script, puedes usar cualquiera de los dos nombres.

### Asignaciones de columnas

`ColumnMappings` · CalendarColumnGroupCollection · Básico · solo lectura · _acceso directo a_ **Grupos de columnas del calendario**

La misma colección que `CalendarColumnGroups`, con el nombre que muestra la **vista de propiedades**. Puedes agregar, modificar y quitar los grupos de la colección. En Tabular Editor 3, haz doble clic en el calendario en la @tom-explorer-view para abrir el **Editor de calendario**. Tanto el botón **...** de la propiedad como **Editar asignaciones de columnas...** en el menú contextual del calendario en el **Explorador TOM** abren un editor de colecciones.

## Asociación de columna con unidad de tiempo

Una asociación de columna con unidad de tiempo vincula una columna de la tabla con una unidad de tiempo del calendario; por ejemplo, la columna `Fiscal Year` con **Año** o la columna `Month Name` con **Mes del año**. La columna asignada es la _columna principal_. Puedes agregar _columnas asociadas_ que contengan la misma unidad de tiempo en otro formato, como un número de mes junto a un nombre de mes.

Cada unidad de tiempo solo puede asignarse una vez en cada calendario. El **Editor de calendario** tiene una fila por unidad de tiempo, y el método `AddTimeUnit` en C# Script falla cuando el calendario ya tiene asignada esa unidad de tiempo. Una columna solo puede pertenecer a una unidad de tiempo en un calendario, y debe asignarse a la misma unidad de tiempo en todos los calendarios del modelo. El **Editor de calendario** de Tabular Editor 3 muestra un error cuando una columna se asigna a distintas unidades de tiempo en dos calendarios, o cuando la columna de ordenación de una columna principal es la columna principal de otra unidad de tiempo.

### Propiedades comunes

- [Tipo de objeto](xref:object-properties-common#object-type)

### Columna principal

`PrimaryColumn` · Columna · Básico

La columna que contiene los valores de esta unidad de tiempo. Sus valores deben ajustarse a la unidad de tiempo: una columna asignada a **Mes** identifica un mes junto con su año, como `January 2025`, y una columna asignada a **Mes del año** solo identifica el mes, como `January` o `1`.

Si la columna principal tiene una `SortByColumn`, el motor también trata la columna de ordenación como una columna asociada, por lo que no es necesario añadirla.

Para ver los valores de las columnas mientras las asignas, abre una @table-preview de la tabla de fechas y ancla la vista junto al **Editor de calendario**.

### Unidad de tiempo

`TimeUnit` · TimeUnit · Básico

La unidad de tiempo que representa la columna principal. Una unidad de tiempo _completa_ identifica un período por sí sola. Una unidad de tiempo _parcial_ solo identifica un período junto con una unidad de tiempo mayor, que el calendario también debe asignar. Por ejemplo, **Mes del año** necesita **Año**.

| Valor                  | Tipo                          | Significado                                                                                             | Valores de ejemplo         |
| ---------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------- |
| `Año`                  | Completa                      | El año.                                                                                 | `2024`, `FY2025`           |
| `Semester`             | Completa                      | El semestre que incluye el año.                                                         | `H1 2024`                  |
| `SemesterOfYear`       | Parcial; requiere `Año`       | El semestre dentro del año.                                                             | `H1`, `1`                  |
| `Trimestre`            | Completo                      | El trimestre incluye el año.                                                            | `Q1 2024`                  |
| `TrimestreDelAño`      | Parcial, requiere `Año`       | El trimestre dentro del año.                                                            | `Q1`, `1`                  |
| `TrimestreDelSemestre` | Parcial, requiere `Semestre`  | El trimestre dentro del semestre.                                                       | `1`, `2`                   |
| `Mes`                  | Completo                      | El mes incluye el año.                                                                  | `enero de 2024`, `2024-01` |
| `MesDelAño`            | Parcial, requiere `Año`       | El mes dentro del año.                                                                  | `enero`, `1`               |
| `MesDelSemestre`       | Parcial, requiere `Semestre`  | El mes dentro del semestre.                                                             | de `1` a `6`               |
| `MesDelTrimestre`      | Parcial, necesita `Trimestre` | El mes dentro del trimestre.                                                            | de `1` a `3`               |
| `Semana`               | Completo                      | La semana que incluye el año.                                                           | `W50-2023`                 |
| `WeekOfYear`           | Parcial, necesita `Año`       | La semana dentro del año.                                                               | `W50`, `50`                |
| `WeekOfSemester`       | Parcial, necesita `Semestre`  | La semana dentro del semestre.                                                          | de `1` a `27`              |
| `WeekOfQuarter`        | Parcial, necesita `Trimestre` | La semana dentro del trimestre.                                                         | de `1` a `14`              |
| `WeekOfMonth`          | Parcial, necesita `Mes`       | La semana dentro del mes.                                                               | de `1` a `6`               |
| `Fecha`                | Completo                      | La fecha.                                                                               | `2025-12-31`               |
| `DayOfYear`            | Parcial; requiere `Year`      | El día del año.                                                                         | De `1` a `366`             |
| `DayOfSemester`        | Parcial; requiere `Semester`  | El día dentro del semestre.                                                             | De `1` a `184`             |
| `DayOfQuarter`         | Parcial; requiere `Quarter`   | El día dentro del trimestre.                                                            | De `1` a `92`              |
| `DayOfMonth`           | Parcial; requiere `Month`     | El día del mes.                                                                         | De `1` a `31`              |
| `DayOfWeek`            | Parcial; requiere `Week`      | El día de la semana.                                                                    | De `1` a `7`               |
| `Unknown`              |                               | No se ha establecido ninguna unidad de tiempo. No es una opción válida. |                            |

Una unidad de tiempo parcial también puede obtener su unidad mayor a partir de una combinación de otras unidades parciales. Por ejemplo, **Mes del año** junto con **Año** es suficiente para **Día del mes**. Consulta la tabla de dependencias en @calendars.

TOM define las unidades de tiempo de semestre (`Semester`, `SemesterOfYear`, `QuarterOfSemester`, `MonthOfSemester`, `WeekOfSemester` y `DayOfSemester`), y Power BI no las incluye entre sus categorías de calendario. Tabular Editor 3 las oculta en la lista desplegable **Unidad de tiempo** de la **vista de propiedades** y en el **Editor de calendario**; además, oculta `Unknown` de la lista desplegable. Solo verás estos valores cuando un C# Script u otra herramienta los haya establecido.

El motor admite las unidades de tiempo de semestre. En Power BI Desktop, se aceptan los calendarios creados con unidades de tiempo de semestre, por ejemplo **Año**, **Semestre**, **Semestre del año**, **Mes** y **Fecha**, y las funciones de inteligencia temporal como `DATESYTD` y `SAMEPERIODLASTYEAR` funcionan con ellos. El motor rechaza un calendario que asigna la misma unidad de tiempo dos veces, y una columna asignada a unidades de tiempo distintas en dos calendarios de la misma tabla.

Las dependencias de la tabla también se aplican a las unidades de tiempo de semestre. Al guardar, el motor acepta un calendario que no las cumple, por ejemplo, un calendario con solo **Semestre del año** y **Fecha**. El motor las aplica cuando una consulta usa el calendario: una unidad parcial solo cuenta cuando su unidad superior también está asignada, de modo que **Trimestre del semestre** funciona como el trimestre del calendario solo junto con **Semestre**. Una función de inteligencia temporal que necesita una unidad que el calendario no tiene produce un error como "'DATESYTD' usa el calendario 'Fiscal', que no define todas las categorías necesarias para esta operación. Como mínimo, asegúrate de que la categoría 'Año' esté etiquetada". Las funciones basadas en el año, como `DATESYTD` y `SAMEPERIODLASTYEAR`, siempre necesitan una unidad de **Año**, y **Semestre** no cuenta como tal.

### Columnas asociadas

`AssociatedColumns` · AssociatedColumnCollection · Opciones · solo de lectura

Otras columnas que contienen la misma unidad de tiempo que la columna principal, en un formato distinto. Por ejemplo, cuando `Month Number` es la columna principal de **Mes del año**, puedes agregar `Month Name` y `Month Short Name` como columnas asociadas. Las funciones de inteligencia temporal tratan un filtro sobre cualquiera de estas columnas como si fuera un filtro sobre la columna principal.

Puedes agregar y quitar columnas de la colección, por ejemplo, en el panel **Columnas asociadas** del **Editor de calendario**.

## Grupo de columnas relacionadas con el tiempo

Un grupo de columnas relacionadas con el tiempo enumera columnas que describen fechas sin estar asignadas a una única unidad de tiempo, por ejemplo `IsHoliday`, `IsWorkingDay` o `Fiscal Period Name`. Las funciones de inteligencia temporal tratan los filtros sobre estas columnas según el tipo de desplazamiento que realizan:

- un _desplazamiento lateral_, que solo realizan `DATEADD` y `SAMEPERIODLASTYEAR`, conserva los filtros en ellas, de modo que los días laborables de este mes se trasladan a los días laborables del mismo mes del año pasado
- un _desplazamiento jerárquico_, que realizan todas las demás funciones de inteligencia temporal, por ejemplo `DATESYTD` o `NEXTMONTH`, elimina sus filtros

Todas las funciones de inteligencia temporal mantienen los filtros sobre columnas de la tabla que el calendario no menciona en absoluto, ni como unidad de tiempo ni en un grupo relacionado con el tiempo. Agrega una columna a un grupo relacionado con el tiempo solo si quieres que los desplazamientos jerárquicos eliminen los filtros aplicados a ella.

Cuando una tabla tiene más de un calendario, el motor aplica estas reglas a cada calendario de la tabla, incluidos los calendarios que la función no utiliza.

### Propiedades comunes

- [Tipo de objeto](xref:object-properties-common#object-type)

### Columnas

`Columns` · AssociatedColumnCollection · Opciones · de solo lectura

Las columnas del grupo. Puedes agregar y quitar columnas de la colección, por ejemplo en el panel **Columnas relacionadas con el tiempo** del **Editor de calendario**.
