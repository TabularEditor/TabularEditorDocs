---
uid: dax-script-introduction
title: Uso de la característica Script DAX
author: Daniel Otykier
updated: 2021-10-08
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Uso de la característica Script DAX

En el [artículo anterior](xref:creating-and-testing-dax), aprendiste a agregar y editar objetos calculados como medidas, columnas calculadas, etc. en tu modelo.

A medida que tu modelo crece en complejidad, puede llegar un momento en el que resulte engorroso navegar por el Explorador TOM o ir saltando entre medidas al crear y mantener la lógica de negocio. No es raro tener largas cadenas de dependencias entre medidas y, por ese motivo, a veces resulta útil reunir todo el código DAX que compone la lógica de negocio en un único documento.

Este es precisamente el propósito de la nueva característica **Script DAX** introducida en Tabular Editor 3.

Para usar esta característica, busca en el Explorador TOM los objetos para los que quieras generar un único documento. Selecciona varios objetos, haz clic con el botón derecho y elige **Script DAX**. Se crea un nuevo documento que contiene las expresiones DAX y las propiedades básicas de todos los objetos seleccionados. También puedes generar un Script DAX para todos los objetos de una tabla o para todos los objetos del modelo seleccionando, respectivamente, la tabla o el objeto del modelo.

![Script Dax](~/content/assets/images/dax-script.png)

Editar objetos mediante un Script DAX es ligeramente distinto de hacerlo desde el **Editor de expresiones**. Con este último, los cambios se aplican de inmediato cuando cambias a otro objeto. En un Script DAX, sin embargo, los cambios no se aplican hasta que los aplicas explícitamente mediante la opción **Script > Aplicar** (F5). Si estás conectado a una instancia de Analysis Services, puedes usar la opción **Script > Aplicar y sincronizar** (SHIFT+F5) para aplicar los cambios y, al mismo tiempo, guardar los metadatos actualizados del modelo en Analysis Services.

## Trabajar con archivos de Script DAX

Los Scripts DAX se pueden guardar como archivos de texto con la extensión `.te3daxs`. Para guardar un Script DAX como archivo, basta con usar la opción **Archivo > Guardar** (Ctrl+S). Para abrir un Script DAX desde un archivo de texto, utiliza la opción **Archivo > Abrir > Archivo...** (Ctrl+O).

> [!NOTE]
> Los Scripts DAX no son específicos de un modelo, pero como las expresiones DAX pueden hacer referencia a medidas, columnas y tablas definidas en el modelo, no se garantiza que cualquier Script DAX pueda aplicarse a cualquier modelo. Los Scripts DAX resultan especialmente útiles para trabajar con varios objetos DAX dentro de un único documento, en el contexto de un Data model específico.

## Editor de Scripts DAX

El editor de Scripts DAX ofrece todas las capacidades del editor de DAX que se usa en otras partes de Tabular Editor 3. En concreto, autocompletado, formato automático, sugerencias emergentes, etc.

Además, para gestionar fácilmente Scripts DAX de gran tamaño, se muestran dos menús desplegables en la parte superior de la vista de Script DAX. El menú desplegable de la izquierda permite pasar de un objeto a otro definido en el script, mientras que el de la derecha permite pasar de una propiedad a otra del objeto actual.

![Navegación del script Dax](~/content/assets/images/dax-script-navigation.png)

## Definir medidas

Si quieres incluir la definición de una medida a la que se hace referencia en el script, pero que aún no está definida en él, puedes hacerlo haciendo clic con el botón derecho en una referencia de medida y eligiendo la opción "Definir medida" o "Definir medida con dependencias".

![Definir medida con dependencias](~/content/assets/images/define-measure-with-deps.png)

## Atajos

Para aplicar el script al modelo, usa los siguientes atajos:

- **F5**: Aplicar el script completo a los metadatos del modelo local
- **Shift+F5**: Aplicar el script completo a los metadatos del modelo local y, a continuación, guardar los metadatos del modelo de vuelta al origen
- **F8**: Aplicar la parte del script seleccionada actualmente a los metadatos del modelo local
- **Shift+F8**: Aplicar la parte del script seleccionada actualmente a los metadatos del modelo local y, a continuación, guardar los metadatos del modelo de vuelta al origen

## Objetos DAX compatibles

Tabular Editor 3 permite editar los siguientes tipos de objetos mediante un Script DAX:

- Medidas (incluidos los KPI)
- Columnas calculadas
- Tablas calculadas
- Grupos de cálculo (incluidos los elementos de cálculo)

# Sintaxis del Script DAX

La sintaxis de los Scripts DAX es la siguiente:

```dax
<DAX script>:
MEASURE 'Nombre de tabla'[Nombre de medida] = <DAX expression>
    [<Measure properties>]

COLUMN 'Nombre de tabla'[Nombre de columna] = <DAX expression>
    [<Column properties>]

TABLE 'Nombre de tabla' = <DAX expression>
    [<Table properties>]

CALCULATIONGROUP 'Nombre de tabla'[Nombre de columna]
    [<Calculation Group properties>]
    CALCULATIONITEM "Item 1" = <DAX expression>
        [<Calculation Item properties>]
    CALCULATIONITEM "Item 2" = <DAX expression>
        [<Calculation Item properties>]
    ...

<Measure properties>:
    DetailRows = <DAX expression>
    DisplayFolder = "string"
    FormatString = "string"
    Description = "string"
    Visible = TRUE/FALSE
    KpiStatusExpression = <DAX expression>
    KpiStatusDescription = "string"
    KpiStatusGraphic = "string"
    KpiTrendExpression = <DAX expression>
    KpiTrendDescription = "string"
    KpiTrendGraphic = "string"
    KpiTargetExpression = <DAX expression>
    KpiTargetDescription = "string"
    KpiTargetFormatString = "string"

<Column properties>:
    DisplayFolder = "string"
    FormatString = "string"
    Description = "string"
    Visible = TRUE / FALSE
    Datatype = BOOLEAN / DOUBLE / INTEGER / DATETIME / CURRENCY / STRING

<Table properties>:
    Description = "string"
    Visible = TRUE / FALSE
    DetailRows = <DAX expression>

<Calculation Group properties>:
    Description = "string"
    Visible = TRUE / FALSE
    Precedence = <integer value>

<Calculation Item properties>
    Description = "string"
    Ordinal = <integer value>
    FormatString = <DAX expression> 
```

## Ejemplo 1: Medida

Como ejemplo, el script siguiente define la medida `[Internet Total Sales]` en la tabla `'Internet Sales'`. Además de la expresión DAX de la medida, el script también incluye la descripción de la medida y la cadena de formato.

```dax
----------------------------------
-- Medida: [Internet Total Sales]
----------------------------------
MEASURE 'Internet Sales'[Internet Total Sales] = SUM('Internet Sales'[Sales Amount])
    Description = "Devuelve la suma de todas las ventas por Internet"
    FormatString = "\$#,0,00;(\$#,0,00);\$#,0,00"
```

## Ejemplo 2: Medida con KPI de estado y objetivo

El Script DAX siguiente define la medida `[Internet Current Quarter Sales Performance]`, que incluye un KPI con una expresión de estado y una expresión de objetivo. El KPI de estado utiliza el gráfico "Shapes".

```dax
--------------------------------------------------------
-- Medida: [Internet Current Quarter Sales Performance]
--------------------------------------------------------
MEASURE 'Internet Sales'[Internet Current Quarter Sales Performance] =
    IFERROR(
        [Internet Current Quarter Sales] / [Internet Previous Quarter Sales Proportion to QTD],
        BLANK()
    )
    , KpiStatusExpression =
        VAR x = [Internet Current Quarter Sales Performance]
        RETURN
            IF(
                ISBLANK( x ),
                BLANK(),
                IF(x < 1, -1, IF(x < 1.07, 0, 1)) -- 1,07
            )
    , KpiStatusGraphic = "Shapes"
    , KpiTargetExpression = 1.1 -- 1,1
```

## Ejemplo 3: grupo de cálculo

El script DAX siguiente define el grupo de cálculo `'Time Intelligence'` con la columna `[Period]`. El grupo de cálculo contiene 6 elementos de cálculo que realizan diversos cálculos de inteligencia temporal. Fíjate en cómo el elemento `"YoY %"` aplica una cadena de formato diferente.

```dax
-----------------------------------------
-- grupo de cálculo: 'Time Intelligence'
-----------------------------------------
CALCULATIONGROUP 'Time Intelligence'[Period]
    Description = "Usa esta tabla para realizar cálculos de inteligencia temporal"

    CALCULATIONITEM "Current" = SELECTEDMEASURE()
        Ordinal = 0

    CALCULATIONITEM "MTD" = TOTALMTD(SELECTEDMEASURE(), 'Calendar'[Date])
        Ordinal = 1

    CALCULATIONITEM "YTD" = TOTALYTD(SELECTEDMEASURE(), 'Calendar'[Date])
        Ordinal = 2

    CALCULATIONITEM "PY" = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Calendar'[Date]))
        Ordinal = 3

    CALCULATIONITEM "YoY" = 
        SELECTEDMEASURE()
         - CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Calendar'[Date]))
        Ordinal = 4

    CALCULATIONITEM "YoY %" = 
        VAR lastYear = 
            CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Calendar'[Date]))
        RETURN
            DIVIDE(
                SELECTEDMEASURE() - lastYear,
                lastYear
            )
        FormatString = "Percent"
        Ordinal = 5
```

# Siguientes pasos

- @bpa
- @cs-scripts-and-macros
- @personalizing-te3