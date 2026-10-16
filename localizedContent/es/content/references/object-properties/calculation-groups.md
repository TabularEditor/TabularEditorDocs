---
uid: object-properties-calculation-groups
title: Propiedades del grupo de cálculo
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

# Propiedades del grupo de cálculo

<!--
SUMMARY: Reference for the properties of calculation groups and calculation items.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Esta página describe las propiedades de los grupos de cálculo y los elementos de cálculo. Un grupo de cálculo siempre pertenece a una tabla de grupos de cálculo. Las propiedades de esa tabla, incluidos los accesos directos a las propiedades del propio grupo de cálculo, se describen en @object-properties-tables. Para ver las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

## Grupo de cálculo

Un grupo de cálculo es un conjunto de elementos de cálculo que cambia la forma en que se calculan las medidas. Por ejemplo, un grupo de cálculo de inteligencia temporal puede tener los elementos `Current`, `YTD` y `Prior year`. Cuando el autor de un Report coloca la columna del grupo de cálculo en un segmentador y selecciona `YTD`, cada medida del Visual muestra su valor acumulado en el año, sin necesidad de crear una medida YTD independiente para cada medida.

Un grupo de cálculo no tiene nombre propio y se identifica por su tabla de grupos de cálculo. No puedes seleccionar el grupo de cálculo en el **Explorador TOM**. Selecciona la tabla de grupos de cálculo, donde la vista **Propiedades** muestra las propiedades del grupo de cálculo como `CalculationGroupDescription`, `CalculationGroupAnnotations` y `CalculationGroupPrecedence` (consulta @object-properties-tables). En C# Script, accedes al objeto de grupo de cálculo a través de `CalculationGroupTable.CalculationGroup`.

En Tabular Editor 3, creas un grupo de cálculo haciendo clic con el botón derecho en el modelo o en la carpeta **Tablas** y eligiendo **Crear > Grupo de cálculo**. Microsoft documenta los grupos de cálculo para el nivel de compatibilidad 1500 o superior, que incluye todos los modelos semánticos de Power BI. Tabular Editor 3 muestra la opción de menú a partir del nivel de compatibilidad 1470, que es cuando el Tabular Object Model (TOM) incorporó los grupos de cálculo. Consulta @creating-and-testing-dax.

### Propiedades comunes

- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Tipo de objeto](xref:object-properties-common#object-type)

### Precedencia

`Precedence` · int · Opciones

El orden en que se aplican los grupos de cálculo cuando una consulta usa elementos de más de un grupo de cálculo, por ejemplo, un grupo de inteligencia temporal y un grupo de conversión de divisas. El grupo de cálculo con la precedencia más alta se aplica primero, lo que hace que su elemento de cálculo sea el más externo. Cuando ese elemento llama a [SELECTEDMEASURE](https://dax.guide/selectedmeasure), el motor usa el resultado del elemento de cálculo del grupo con la siguiente precedencia inferior, y así sucesivamente hasta llegar a la medida.

El orden cambia el resultado cuando los elementos de cálculo no son conmutativos. Con un grupo de inteligencia temporal que tiene un elemento `YTD` y un grupo que tiene un elemento `Average per day`, el acumulado en el año del promedio diario difiere del promedio diario del valor acumulado en el año. En este ejemplo, un grupo de cálculo con precedencia `200` tiene el elemento `SELECTEDMEASURE () * 2` y otro con precedencia `100` tiene el elemento `SELECTEDMEASURE () + 2`. Al seleccionar ambos elementos en una medida que devuelve `10`, se obtiene `( 10 + 2 ) * 2 = 24`.

El valor predeterminado de TOM es `0`. Asigna a cada grupo de cálculo del modelo una precedencia distinta de `0` o superior. El motor rechaza un modelo en el que dos grupos de cálculo tienen la misma precedencia, con un error como "Calculation Group precedence must be greater or equal zero and unique within Model".

Cuando agregas o pegas un grupo de cálculo cuya precedencia ya la usa otro grupo de cálculo del modelo, Tabular Editor la establece en un valor superior en uno a la precedencia más alta del modelo. También puedes establecerla en la tabla del grupo de cálculo como `CalculationGroupPrecedence`. En un documento @dax-scripts de Tabular Editor 3, la estableces con la propiedad `Precedence` del grupo de cálculo.

## Elemento de cálculo

Un elemento de cálculo es una entrada de un grupo de cálculo, por ejemplo, `YTD`. Los autores de Report ven su nombre como un valor en la columna del grupo de cálculo, y su expresión define cómo cambia la medida cuando se selecciona el elemento. Dentro de la expresión, [SELECTEDMEASURE](https://dax.guide/selectedmeasure) devuelve la medida que se está evaluando.

Un grupo de cálculo sin elementos de cálculo no tiene ningún efecto. La regla @kb.bpa-calculation-groups-no-items del Best Practice Analyzer (BPA) marca los grupos de cálculo que no contienen elementos.

La propiedad `Description` de un elemento de cálculo es solo para desarrolladores. Power BI Desktop no la muestra, por ejemplo, cuando un autor de Report pasa el cursor sobre el elemento en un segmentador.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Mensaje de error](xref:object-properties-common#error-message)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Estado](xref:object-properties-common#state)

### Ordinal

`Ordinal` · int · Básico · nivel de compatibilidad 1500+

La posición del elemento de cálculo dentro de su grupo de cálculo, a partir de `0`. Las herramientas cliente ordenan los elementos según este valor; por ejemplo, para mostrar `Current`, `MTD`, `QTD` y `YTD` en ese orden en un segmentador. El motor lo expone a través de la columna ordinal de la tabla del grupo de cálculo.

El valor `-1` significa que el elemento no tiene posición. Según Microsoft, los elementos con `-1` no se incluyen en la ordenación y aparecen antes que los elementos ordenados en un Report. Si ningún elemento tiene un ordinal, las herramientas cliente ordenan los elementos alfabéticamente.

Tabular Editor 3 mantiene los ordinales de un grupo de cálculo numerados `0`, `1`, `2` y así sucesivamente, sin huecos ni duplicados:

- cuando arrastras elementos de cálculo para reordenarlos en el **Explorador TOM**, Tabular Editor renumera todos los elementos del grupo
- cuando escribes un nuevo `Ordinal` en la vista de **Propiedades**, Tabular Editor mueve el elemento a esa posición y renumera los demás elementos
- cuando escribes `-1`, Tabular Editor establece el ordinal de todos los elementos del grupo a `-1`, lo que elimina el orden personalizado
- cuando agregas un elemento de cálculo, recibe el número siguiente al ordinal más alto del grupo, a menos que aún no haya ningún elemento del grupo con ordinal

Solo puedes establecer `Ordinal` para un elemento de cálculo a la vez. Tabular Editor 2 renumera los ordinales de la misma forma cuando arrastras elementos de cálculo para reordenarlos en el **Explorador TOM** o escribes un nuevo `Ordinal`.

También puedes arrastrar elementos de cálculo a otro grupo de cálculo para moverlos allí. Consulta @drag-drop.

### Expresión

`Expression` · string · Opciones

La expresión DAX que el motor evalúa en lugar de la medida cuando se selecciona este elemento de cálculo. Usa [SELECTEDMEASURE](https://dax.guide/selectedmeasure) para referirte a la medida. Este es un elemento de acumulado hasta la fecha:

```dax
CALCULATE ( SELECTEDMEASURE (), DATESYTD ( 'Date'[Date] ) )
```

Este elemento deja la medida sin cambios y funciona como valor predeterminado:

```dax
SELECTEDMEASURE ()
```

La expresión se aplica a todas las medidas de la consulta, incluidas las medidas que devuelven texto. Para limitarla a algunas medidas, comprueba la medida con [ISSELECTEDMEASURE](https://dax.guide/isselectedmeasure) o [SELECTEDMEASURENAME](https://dax.guide/selectedmeasurename), por ejemplo:

```dax
IF (
    ISSELECTEDMEASURE ( [Total Sales], [Total Cost] ),
    CALCULATE ( SELECTEDMEASURE (), DATESYTD ( 'Date'[Date] ) ),
    SELECTEDMEASURE ()
)
```

Los elementos de cálculo se aplican solo a las medidas, y las columnas que se agregan de forma implícita no se ven afectadas. Power BI activa `DiscourageImplicitMeasures` en el modelo cuando agregas un grupo de cálculo (consulta @object-properties-model).

En Tabular Editor 3, escribe la expresión en el **Editor de expresiones** del @dax-editor, con autocompletado e información de parámetros.

### Expresión de cadena de formato dinámica

`FormatStringExpression` · string · Opciones

Una expresión DAX que devuelve la cadena de formato de la medida cuando se selecciona este elemento de cálculo. Déjalo vacío para conservar el formato propio de la medida. Configúralo cuando el elemento cambie el tipo de valor que devuelve la medida, por ejemplo, un porcentaje interanual:

```dax
"0.0%"
```

También puedes hacer que el formato dependa del contexto, por ejemplo, de un símbolo de moneda. Dentro de la expresión, [SELECTEDMEASUREFORMATSTRING](https://dax.guide/selectedmeasureformatstring) devuelve la propia cadena de formato de la medida, que puedes usar como valor de reserva. En este ejemplo se usa una tabla `Currency` con una columna `Format`:

```dax
SELECTEDVALUE ( 'Currency'[Format], SELECTEDMEASUREFORMATSTRING () )
```

La expresión debe devolver un único valor de texto. Las expresiones de cadena de formato dinámicas en los elementos de cálculo no requieren un nivel de compatibilidad independiente y están disponibles en cualquier lugar donde lo estén los grupos de cálculo. Cuando varios grupos de cálculo se aplican a una medida, el motor usa solo la expresión de cadena de formato dinámica del grupo de cálculo con mayor precedencia. Para quitar la expresión, borra el valor.
