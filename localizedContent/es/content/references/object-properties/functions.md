---
uid: object-properties-functions
title: Propiedades de funciones y conjuntos
author: Jeroen ter Heerdt
updated: 2026-10-05
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Admite funciones y conjuntos, pero no Namespace, PackageId ni PackageVersion"
    - product: Tabular Editor 3
      since: 3.23.0
      note: "Las funciones definidas por el usuario requieren la versión 3.23.0 o posterior. Los conjuntos se admiten en todas las versiones."
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Propiedades de funciones y conjuntos

<!--
SUMMARY: Reference for the properties of DAX user-defined functions and of sets.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

En esta página se enumeran las propiedades de las funciones DAX definidas por el usuario y de los conjuntos. Para las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

## Función

Una función definida por el usuario (UDF) es una función DAX reutilizable que defines una vez en el modelo y a la que puedes llamar desde cualquier expresión DAX, incluidas otras funciones. Acepta parámetros, que pueden ser valores, tablas o referencias a columnas y medidas, y devuelve un valor o una tabla. Las UDF pertenecen al modelo y el **Explorador TOM** las muestra en la carpeta **Funciones**.

Las UDF requieren un nivel de compatibilidad de 1702 o superior. Azure Analysis Services y SQL Server Analysis Services no las admiten. Para una introducción completa, consulta @udfs.

Tabular Editor 2 también admite las UDF y las muestra en la carpeta **Funciones**. Para agregar una en Tabular Editor 2, haz clic con el botón derecho en la carpeta y elige **Nueva función definida por el usuario**. Tabular Editor 2 no tiene las propiedades `Namespace`, `PackageId` y `PackageVersion`.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Oculto](xref:object-properties-common#hidden)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Propiedades modificadas](xref:object-properties-common#changed-properties)
- [Mensaje de error](xref:object-properties-common#error-message)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Estado](xref:object-properties-common#state)
- [Etiqueta de linaje](xref:object-properties-common#lineage-tag)
- [Etiqueta de linaje de origen](xref:object-properties-common#source-lineage-tag)

En DAX, llamas a una función por su nombre, así que el nombre no puede contener espacios. Puede contener puntos y guiones bajos. Usa un nombre compuesto, como `Finance.Margin` o `ACME_Margin`, para evitar conflictos con una función DAX integrada que Microsoft pueda agregar más adelante. Consulta @kb.bpa-udf-use-compound-names. Cuando cambias el nombre de una función, Tabular Editor 3 actualiza las referencias a ella en todo el modelo, igual que @formula-fix-up-dependencies hace con las medidas y las columnas.

### Espacio de nombres

`Namespace` · string · Básico · _almacenado como una anotación_ (`TE_Group`)

El grupo en el que aparece la función en @tom-explorer-view cuando está activada la agrupación de funciones definidas por el usuario por espacio de nombres. Activa la agrupación con el interruptor situado encima del **Explorador TOM**. Tabular Editor determina el espacio de nombres en este orden:

1. si la función tiene una anotación `TE_Group`, ese es el espacio de nombres
2. de lo contrario, si el nombre de la función contiene un punto, el espacio de nombres es la parte anterior al último punto; por ejemplo, `DaxLib.Convert.CelsiusToFahrenheit` está en el espacio de nombres `DaxLib.Convert`
3. de lo contrario, si la función tiene una anotación `DAXLIB_PackageId` (consulta [PackageId](#packageid)), el espacio de nombres es el identificador del paquete
4. de lo contrario, el espacio de nombres está vacío

Puedes establecer un espacio de nombres distinto sin cambiar el nombre de la función. Tabular Editor lo almacena en la anotación `TE_Group` de la función, que se guarda con el modelo. Para volver a usar el espacio de nombres derivado del nombre, restablece la propiedad o borra el valor. Al igual que una carpeta de visualización, el espacio de nombres solo organiza el **Explorador TOM** y, en DAX, siempre llamas a la función por su nombre completo.

Por ejemplo, si [cambias el nombre en lote](xref:duplicate-and-batch) de un conjunto de funciones para quitar el prefijo `DaxLib.Convert.` de sus nombres, establece su espacio de nombres en `DaxLib.Convert` para mantenerlas agrupadas.

### Id. de paquete

`PackageId` · string · Metadatos · solo lectura · _almacenado como anotación_ (`DAXLIB_PackageId`)

El identificador del paquete de [DaxLib](https://daxlib.org) del que procede la función, leído de la anotación `DAXLIB_PackageId` de la función. Los paquetes de DaxLib colocan esta anotación en sus funciones. La **vista de propiedades** solo muestra `PackageId` y `PackageVersion` cuando la función tiene esta anotación, por lo que las funciones que has escrito tú no los muestran.

El DAX Package Manager de Tabular Editor 3 quita las anotaciones `DAXLIB_` cuando instala una función y realiza el seguimiento del paquete mediante propiedades extendidas, como se describe en [PackageVersion](#packageversion). Verás estas propiedades en las funciones de un paquete de DaxLib que se añadieron al modelo sin el DAX Package Manager. Consulta @dax-package-manager.

### Versión del paquete

`PackageVersion` · string · Metadatos · solo lectura · _almacenado como anotación_ (`DAXLIB_PackageVersion`)

La versión del paquete de DaxLib del que procede la función, leída de la anotación `DAXLIB_PackageVersion` de la función.

El DAX Package Manager no usa `PackageId` ni `PackageVersion`. Realiza el seguimiento de los paquetes instalados en propiedades extendidas. En el modelo, `TabularEditor_ModelDaxPkgTable` y `TabularEditor_ModelDaxPkgSeq` enumeran los paquetes instalados. En cada función, `TabularEditor_ObjDaxPkgHandle` registra a qué paquete pertenece la función y `TabularEditor_ObjDaxPkgContentHash` registra cuál era su expresión cuando se instaló. Si cambias la expresión de una función que procede de un paquete, cuando más tarde actualices o quites el paquete aparecerá un mensaje preguntando qué hacer con la función modificada.

Para que el DAX Package Manager deje de realizar el seguimiento de una función, elimina sus dos propiedades extendidas: `TabularEditor_ObjDaxPkgHandle` y `TabularEditor_ObjDaxPkgContentHash`. Al quitar el paquete, la función ya no se elimina y el paquete sigue apareciendo como instalado. Si más tarde actualizas o reinstalas el paquete, aparecerá un mensaje sobre el conflicto con la función existente del mismo nombre. Si quitas solo `TabularEditor_ObjDaxPkgContentHash`, la función se considera modificada y cada actualización mostrará un mensaje al respecto. La documentación del DAX Package Manager advierte de que cambiar manualmente estas propiedades extendidas puede provocar un comportamiento inesperado.

### Expresión

`Expression` · string · Opciones

La lista de parámetros y el cuerpo de la función en notación lambda: los parámetros entre paréntesis, luego `=>` y después la expresión DAX que los usa. Por ejemplo:

```dax
// Returns the relative change between two values
(
    oldValue: NUMERIC,  // The original value
    newValue: NUMERIC   // The value to compare against
)
=> DIVIDE ( newValue - oldValue, oldValue )
```

Cada parámetro puede tener un tipo, como `NUMERIC`, `STRING` o `TABLE`, y un modo de evaluación. `VAL`, el valor predeterminado, evalúa el argumento una vez antes de que se ejecute la función, como una variable. `EXPR` pasa la expresión en sí, que se evalúa en el contexto en el que la función la usa, como una medida. Un parámetro seguido de `= expression` es opcional. Consulta @udfs para ver la sintaxis completa.

Tabular Editor 3 muestra los comentarios de la expresión en las sugerencias de autocompletado y en las descripciones emergentes cuando llamas a la función.

En Tabular Editor 3, puedes editar funciones junto con otros objetos en un documento @dax-scripts, con la palabra clave `FUNCTION`. También puedes escribir una función en la sección `DEFINE` de una @dax-query y aplicar la consulta para agregar la función al modelo.

## Conjunto

Un conjunto pertenece a una tabla y contiene una expresión DAX. El Tabular Object Model (TOM) lo describe como un _conjunto calculado_. Los conjuntos solo se admiten en modelos de Power BI y Fabric, con nivel de compatibilidad 1400 o superior. En un modelo en modo de compatibilidad de Analysis Services, la biblioteca TOM rechaza un nuevo conjunto con el error "is not supported at AnalysisServices mode".

Los conjuntos no aparecen en el **Explorador TOM**. Para agregar, editar o quitar los conjuntos de una tabla, selecciona la tabla y haz clic en el botón **...** de la propiedad `Sets` (consulta @object-properties-tables). La **vista de propiedades** solo muestra esa propiedad para modelos en modo de compatibilidad de Power BI con nivel de compatibilidad 1400 o superior.

<!-- TODO (not verifiable from TE3 source): what a Set is used for. TOM only describes it as a "calculated set" on a table with a DAX expression that can be static or dynamic. It looks like the equivalent of an MDX named set (for example for Excel PivotTables), but that isn't documented. Confirm with the TE/TOM team. -->

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Carpeta de visualización](xref:object-properties-common#display-folder)
- [Oculto](xref:object-properties-common#hidden)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Mensaje de error](xref:object-properties-common#error-message)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Estado](xref:object-properties-common#state)
- [Carpetas de visualización traducidas](xref:object-properties-common#translated-display-folders)

### Expresión

`Expression` · string · Opciones

La expresión DAX que define el conjunto.

<!-- TODO (not verifiable from TE3 source): what kind of DAX expression a set expects (a table expression that returns the members of the set?); add an example. TOM only says "The DAX expression that is evaluated for the calculated set." -->

### Dinámico

`IsDynamic` · bool · Opciones

Indica si el conjunto es estático o dinámico. Un conjunto estático se evalúa una vez, y sus miembros no cambian en función de los filtros de una consulta. Un conjunto dinámico se evalúa para cada consulta, en su contexto, y sus miembros pueden cambiar en función de los filtros.

<!-- TODO (not verifiable from TE3 source): the static/dynamic behavior. It's based on how named sets work in MDX; TOM only says "Indicates whether the set is static or dynamic". -->
