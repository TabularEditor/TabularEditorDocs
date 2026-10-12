---
uid: object-properties-hierarchies
title: Propiedades de jerarquía y nivel
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

# Propiedades de jerarquía y nivel

<!--
SUMMARY: Reference for the properties of hierarchies and their levels.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Esta página describe las propiedades de las jerarquías definidas por el usuario y de sus niveles. Para ver las propiedades comunes a la mayoría de los objetos, consulta @object-properties-common.

## Jerarquía

Una jerarquía es una lista ordenada de columnas con nombre de una tabla, por la que los autores de Reports desglosan los datos en Visuals y tablas dinámicas; por ejemplo, `Year` > `Quarter` > `Month` > `Date` o `Category` > `Subcategory` > `Product`. Cada paso es un nivel. Las jerarquías no cambian la forma en que se almacenan ni se calculan los datos.

Todos los niveles de una jerarquía deben proceder de la tabla a la que pertenece la jerarquía. Para crear una jerarquía entre tablas, primero incorpora las columnas a una sola tabla, por ejemplo, con columnas calculadas que usen [RELATED](https://dax.guide/related).

En el **Explorador TOM**, puedes agregar niveles a una jerarquía arrastrando columnas sobre ella. Consulta @drag-drop.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Carpeta de visualización](xref:object-properties-common#display-folder)
- [Oculto](xref:object-properties-common#hidden)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Propiedades modificadas](xref:object-properties-common#changed-properties)
- [Mensaje de error](xref:object-properties-common#error-message)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Estado](xref:object-properties-common#state)
- [Etiqueta de linaje](xref:object-properties-common#lineage-tag)
- [Etiqueta de linaje de origen](xref:object-properties-common#source-lineage-tag)
- [Nombres traducidos](xref:object-properties-common#translated-names)
- [Descripciones traducidas](xref:object-properties-common#translated-descriptions)
- [Carpetas de visualización traducidas](xref:object-properties-common#translated-display-folders)
- [Sinónimos](xref:object-properties-common#synonyms)
- [Mostrado en la perspectiva](xref:object-properties-common#shown-in-perspective)

### Ocultar miembros

`HideMembers` · HierarchyHideMembersType · Opciones · nivel de compatibilidad 1400+

Indica si las herramientas cliente ocultan los miembros con un valor en blanco. Úselo para jerarquías _irregulares_, en las que algunas ramas tienen menos niveles que otras. En una jerarquía geográfica `Country` > `State` > `City`, por ejemplo, algunos países no tienen estados y, con `Default`, el usuario ve un miembro vacío en el nivel `State` entre el país y sus ciudades. La vista **Propiedades** muestra `HideMembers` en el nivel de compatibilidad 1400 o superior.

| Valor              | Significado                                                                                                                               |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `Predeterminado`   | Muestra todos los miembros, incluidos los que están en blanco. Úselo para una jerarquía equilibrada.      |
| `HideBlankMembers` | Oculta un miembro cuando su valor está en blanco, y sus miembros secundarios aparecen directamente bajo el miembro padre. |

Solo se ocultan los miembros en blanco y un valor de marcador de posición como `N/A` sigue apareciendo. Excel respeta esta propiedad. Power BI la ignora y muestra los miembros en blanco.

<!-- TODO (not verifiable from TE3 source): whether the engine treats an empty string as blank (Excel hiding real BLANK() members is confirmed on SSAS 2025). -->

## Nivel

Un nivel es un paso dentro de una jerarquía. Cada nivel apunta a una columna de la tabla de la jerarquía y tiene su propio nombre, que puede ser distinto del de la columna. Por ejemplo, un nivel llamado `Month` puede apuntar a una columna llamada `MonthName`.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Propiedades modificadas](xref:object-properties-common#changed-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Etiqueta de linaje](xref:object-properties-common#lineage-tag)
- [Etiqueta de linaje de origen](xref:object-properties-common#source-lineage-tag)
- [Nombres traducidos](xref:object-properties-common#translated-names)
- [Descripciones traducidas](xref:object-properties-common#translated-descriptions)
- [Sinónimos](xref:object-properties-common#synonyms)

Los niveles no tienen `IsHidden` ni `DisplayFolder` propios y, en las perspectivas, siguen su jerarquía. Si traduces el nombre de la jerarquía, traduce también los nombres de sus niveles. La regla @kb.bpa-translate-hierarchy-levels del Best Practice Analyzer (BPA) señala los niveles de las jerarquías visibles que no tienen un nombre traducido en una o varias configuraciones regionales del modelo.

### Columna

`Column` · Column · Básico

La columna que proporciona los valores del nivel. Debe ser una columna de la misma tabla que la jerarquía, y una columna solo puede usarse una vez en la misma jerarquía. El nivel muestra los valores de la columna en el orden de clasificación de la columna. Para mostrar los meses en orden del calendario, establece `SortByColumn` en la columna del nombre del mes (consulta @object-properties-columns).

Una columna oculta sigue funcionando en una jerarquía. Oculta las columnas del nivel para que los usuarios exploren los datos a través de la jerarquía.

### Ordinal

`Ordinal` · int · Básico

La posición del nivel dentro de la jerarquía, empezando por `0` para el nivel superior. Los ordinales de los niveles de una jerarquía deben ser `0`, `1`, `2`, etc., sin huecos ni duplicados.

Tabular Editor 3 mantiene la numeración de los ordinales:

- cuando arrastras los niveles para reordenarlos en el **Explorador TOM**, Tabular Editor renumera todos los niveles de la jerarquía
- cuando eliminas un nivel, Tabular Editor vuelve a numerar los niveles restantes para cerrar el hueco
- cuando escribes un nuevo `Ordinal` en la vista de **Propiedades**, Tabular Editor mueve el nivel a esa posición y vuelve a numerar los demás niveles
- cuando agregas un nivel, va al final de la jerarquía, a menos que sueltes la columna entre dos niveles existentes

Solo puedes establecer `Ordinal` para un nivel a la vez. Tabular Editor 2 renumera los ordinales de los niveles del mismo modo cuando arrastras los niveles para reordenarlos y cuando eliminas un nivel.

También puedes arrastrar niveles a otra jerarquía de la misma tabla para moverlos allí. Consulta @drag-drop.
