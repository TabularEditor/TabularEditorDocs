---
uid: object-properties-medidas
title: Propiedades de las medidas y de los KPI
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

# Propiedades de las medidas y de los KPI

<!--
SUMMARY: Reference for the properties of measures and KPIs.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

En esta página se describen las propiedades de las medidas y de los KPI vinculados a ellas. Cada entrada indica el nombre de la propiedad en el Tabular Object Model (TOM), su tipo y su categoría. Para las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

## Medida

Una medida es una expresión DAX con nombre que se evalúa en el contexto de filtro de la consulta; por ejemplo, `SUM ( Sales[Amount] )`. La tabla a la que pertenece una medida determina dónde aparece la medida en la lista de campos y no afecta al cálculo. Para agregar medidas y editar sus expresiones en Tabular Editor 3, consulta @creating-and-testing-dax.

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
- [Mostrado en la perspectiva](xref:object-properties-common#shown-in-perspective)

### Cadena de formato

`FormatString` · string · Básico

El formato que aplican las herramientas cliente cuando muestran el valor de la medida, por ejemplo `#,0.00`, `0.0%` o `yyyy-mm-dd`. La sintaxis es la misma que la de la función DAX [FORMAT](https://dax.guide/format). Las consultas DAX devuelven el valor sin formato. Para elegir el formato en función del contexto de filtro, establece `FormatStringExpression`.

La regla @kb.bpa-format-string-measures del Best Practice Analyzer (BPA) marca las medidas numéricas y de fecha visibles que no tienen una cadena de formato. En Tabular Editor 3, el script @script-format-numeric-measures asigna cadenas de formato a las medidas seleccionadas.

### Tipo de datos

`DataType` · DataType · Metadatos · de solo lectura

El tipo de datos que devuelve la expresión de la medida, por ejemplo `Int64`, `Double`, `Decimal`, `String` o `DateTime`. El motor lo deduce a partir de la expresión. Es `Variant` cuando la expresión devuelve tipos distintos en contextos diferentes, por ejemplo, un número en un contexto y un texto en otro, y `Unknown` cuando la expresión contiene un error.

En un modelo que abres desde un archivo, el motor no ha establecido el tipo de datos. En Tabular Editor 3, cuando el análisis semántico está habilitado, la vista de propiedades muestra el tipo de datos que Tabular Editor infiere a partir de la expresión.

### Expresión

`Expression` · string · Opciones

La expresión DAX que calcula la medida. Edítala en el **Editor de expresiones**. En Tabular Editor 3, el Editor de expresiones forma parte de @dax-editor e incluye Code Assist y el subrayado de errores sintácticos y semánticos a medida que escribes. @code-actions sugieren mejoras en la expresión que puedes aplicar con un solo clic. El @dax-debugger recorre la expresión paso a paso y muestra los valores de sus partes. Necesita una conexión al modelo.

El script @script-find-replace reemplaza texto en las expresiones de muchas medidas a la vez. La regla de BPA @kb.bpa-expression-required marca las medidas con una expresión vacía.

### Expresión de cadena de formato dinámica

`FormatStringExpression` · string · Opciones · nivel de compatibilidad 1601+

Una expresión DAX que devuelve la cadena de formato que se va a usar, por ejemplo, para mostrar un símbolo de moneda distinto por país o para mostrar valores grandes en miles o millones. Esto se conoce como una _cadena de formato dinámica_. Dentro de la expresión, haz referencia al valor de la propia medida con `SELECTEDMEASURE()` o mediante el nombre de la medida.

Una medida no puede tener a la vez `FormatString` y `FormatStringExpression`. En Tabular Editor 3, al establecer `FormatStringExpression` se borra `FormatString` en la misma acción de deshacer. Cuando ambas están establecidas, por ejemplo mediante un C# Script, Tabular Editor 3 muestra el error "A measure is not allowed to have both its FormatString and FormatStringExpression property assigned" en la medida. Para volver a un formato estático, primero borra `FormatStringExpression` y después establece `FormatString`.

Para el error "A measure is not allowed to have both FormatString and Format Expression" en una medida de un modelo compuesto en Analysis Services, consulta @composite-model-measure-formatting.

### Expresión de filas de detalle

`DetailRowsExpression` · string · Opciones · nivel de compatibilidad 1400+

Una expresión de tabla DAX que define las filas que ve un usuario cuando obtiene detalles de un valor de esta medida, por ejemplo, con **Mostrar detalles** en una tabla dinámica de Excel. La expresión se evalúa en el contexto de filtro de la celda en la que se obtuvieron los detalles. Por ejemplo, `SELECTCOLUMNS ( Sales, "Order", Sales[OrderNumber], "Amount", Sales[Amount] )` devuelve el número de pedido y el importe de cada venta. Cuando la propiedad está vacía, la obtención de detalles devuelve las filas de la tabla subyacente con las columnas predeterminadas de la tabla.

Power BI no usa esta propiedad. Para establecer un valor predeterminado para todas las medidas de una tabla, usa `DefaultDetailRowsExpression` en la tabla (consulta @object-properties-tables). Para ver un ejemplo paso a paso, consulta @detail-rows-expression.

### Categoría de datos

`DataCategory` · cadena · Opciones · nivel de compatibilidad 1455 o superior

El tipo de valor que devuelve la medida y que las herramientas cliente usan para mostrarlo. Por ejemplo, Power BI muestra la URL devuelta como una imagen cuando la categoría es `ImageUrl` y como un enlace cuando es `WebUrl`. Las medidas usan las mismas categorías que las columnas. Consulta `DataCategory` en @object-properties-columns.

### KPI

`KPI` · KPI · Opciones

El KPI adjunto a esta medida, si existe. Un KPI agrega un objetivo, un estado y una tendencia a la medida. Consulta [KPI](#kpi-1) más abajo.

En Tabular Editor 3, para agregar un KPI desde la vista de propiedades, haz clic en **...** en la propiedad `KPI` vacía o haz clic con el botón derecho en la propiedad y selecciona **Agregar KPI**. Para quitarlo, haz clic con el botón derecho en la propiedad y selecciona **Quitar KPI**.

Tabular Editor 2 funciona igual. En Tabular Editor 2, también puedes hacer clic con el botón derecho en la medida en el **Explorador TOM** y seleccionar **Crear nuevo > KPI**. El KPI aparece entonces debajo de la medida, donde puedes eliminarlo.

## KPI

Un indicador clave de rendimiento (KPI) amplía una medida con un valor objetivo, un estado que compara la medida con el objetivo y una tendencia. Excel y SQL Server Management Studio muestran los KPI con iconos de estado y tendencia. Power BI no muestra los KPI definidos en el modelo y cuenta con su propio Visual de KPI.

Un KPI siempre pertenece a una sola medida y el valor de la propia medida es el _valor_ del KPI. El KPI no tiene nombre propio.

Para agregar un KPI en Tabular Editor 3, haz clic con el botón derecho en una medida y selecciona **Crear > KPI**. Un script DAX también puede definir una medida junto con su KPI. Consulta @dax-scripts.

### Propiedades comunes

- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

### Medida principal

`MeasureName` · string · Metadatos · de solo lectura · _acceso directo a_ el nombre de la medida

El nombre de la medida a la que pertenece este KPI.

### Medida

`Measure` · medida · Opciones · de solo lectura

La medida a la que pertenece este KPI. Los C# Scripts la usan para obtener la medida a partir del KPI. Tabular Editor 3 oculta esta propiedad en la vista de propiedades y muestra allí `MeasureName`.

### Expresión del objetivo

`TargetExpression` · string · Opciones

Una expresión DAX que devuelve el objetivo de la medida; por ejemplo, un número fijo como `1000000`, otra medida como `[Sales Budget]` o un cálculo.

### Cadena de formato del objetivo

`TargetFormatString` · string · Opciones

La cadena de formato del valor objetivo, con la misma sintaxis que `FormatString` en una medida.

### Descripción del objetivo

`TargetDescription` · string · Opciones

Una descripción del objetivo, que se muestra a los usuarios en las herramientas cliente que lo admiten.

### Expresión de estado

`StatusExpression` · string · Opciones

Una expresión DAX que compara la medida con el objetivo y devuelve un número entre `-1` y `1`, donde `-1` es malo, `0` es neutro y `1` es bueno. Las herramientas cliente usan este número para seleccionar el icono de `StatusGraphic`. Por ejemplo:

```dax
VAR Ratio = DIVIDE ( [Total Sales], [Sales Budget] )
RETURN
    SWITCH ( TRUE (), Ratio >= 1, 1, Ratio >= 0.9, 0, -1 )
```

### Gráfico de estado

`StatusGraphic` · string · Opciones

El conjunto de iconos que las herramientas cliente usan para mostrar el estado; se especifica como un nombre que la herramienta cliente reconozca, por ejemplo `Traffic Light` o `Shapes`.

En Tabular Editor 3, elige un nombre de la lista o escribe cualquier otro valor. Tabular Editor 3 acepta cualquier valor. La lista contiene `Cylinder`, `Faces`, `Five Bars Colored`, `Five Boxes Colored`, `Gauge`, `Gauge - Ascending`, `Gauge - Descending`, `Reversed Gauge`, `Reversed status arrow`, `Road Signs`, `Shapes`, `Smiley`, `Smiley Face`, `Standard Arrow`, `Status Arrow`, `Status Arrow - Ascending`, `Status Arrow - Descending`, `Thermometer`, `Three Circles Colored`, `Three Flags Colored`, `Three Stars Colored`, `Three Symbols Uncircled Colored`, `Three Triangles`, `Traffic Light`, `Traffic Light - Single` y `Variance Arrow`.

Excel solo reconoce algunos de estos nombres. En una tabla dinámica de Excel, estos nombres muestran su propio icono de estado:

| Gráfico de estado                            | Lo que muestra Excel                                                  |
| -------------------------------------------- | --------------------------------------------------------------------- |
| `Road Signs`                                 | Una marca de verificación cuando el estado es bueno                   |
| `Traffic Light`                              | Un semáforo                                                           |
| `Standard Arrow`                             | Una flecha gris                                                       |
| `Status Arrow - Ascending`, `Variance Arrow` | Una flecha de color que apunta hacia arriba cuando el estado es bueno |
| `Status Arrow - Descending`                  | Una flecha de color que apunta hacia abajo cuando el estado es bueno  |
| `Gauge - Ascending`, `Gauge - Descending`    | Un círculo oscuro o uno vacío                                         |

Todos los demás nombres, incluidos `Shapes`, `Thermometer`, `Smiley`, `Cylinder` y los nombres que Excel no reconoce, muestran un simple círculo de color.

### Descripción del estado

`StatusDescription` · cadena · Opciones

Una descripción del estado, que se muestra a los usuarios en las herramientas de cliente compatibles.

### Expresión de tendencia

`TrendExpression` · cadena · Opciones

Una expresión DAX que devuelve un número entre `-1` y `1` que muestra si la medida empeora (`-1`), se mantiene igual (`0`) o mejora (`1`) con el tiempo, por ejemplo, en comparación con el periodo anterior.

### Gráfico de tendencia

`TrendGraphic` · cadena · Opciones

El conjunto de iconos que las herramientas cliente usan para mostrar la tendencia, por ejemplo `Standard Arrow`, expresado como un nombre que la herramienta cliente reconoce. En Tabular Editor 3, selecciónalo de la misma lista de nombres que `StatusGraphic`, o escribe cualquier otro valor.

En Excel, la mayoría de los nombres muestran una flecha de color; `Standard Arrow` muestra una flecha gris y `Status Arrow - Descending` muestra una flecha que apunta hacia abajo cuando la tendencia es buena. Algunos nombres, como `Cylinder`, `Smiley Face` y `Traffic Light - Single`, muestran un círculo.

### Descripción de la tendencia

`TrendDescription` · cadena · Opciones

Una descripción de la tendencia, que se muestra a los usuarios en las herramientas de cliente compatibles.
