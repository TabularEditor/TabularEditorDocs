---
uid: dax-scripts
title: Script DAX
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Empresa
          full: true
        - edition: Empresarial
          full: true
---

# Script DAX

**Script DAX** le permite ver y editar expresiones DAX y propiedades básicas de varios objetos en un único documento. Esto resulta útil, por ejemplo, cuando una lógica de negocio compleja está repartida entre varias medidas.

Puede crear un script del código DAX para cualquier objeto del Explorador TOM que tenga expresiones DAX.

Para usar esta funcionalidad, localice en el Explorador TOM los objetos para los que desee generar un único documento. Seleccione varios objetos y, a continuación, haga clic con el botón derecho y elija **Script DAX**. Se crea un documento nuevo que contiene las expresiones DAX y las propiedades básicas de todos los objetos seleccionados. También puede generar un Script DAX para todos los objetos de una tabla o para todos los objetos del modelo, seleccionando, respectivamente, el objeto de tabla o el objeto de modelo.

![Dax Script](~/content/assets/images/dax-script.png)

Editar objetos mediante un Script DAX es ligeramente diferente a hacerlo mediante el **Editor de expresiones**. Con este último, los cambios se aplican de inmediato cuando navega a otro objeto. En un Script DAX, sin embargo, los cambios no se aplican hasta que lo haga explícitamente con la opción **Script > Aplicar** (F5). Si está conectado a una instancia de Analysis Services, puede usar la opción **Script > Aplicar y sincronizar** (SHIFT+F5) para aplicar los cambios y guardar a la vez los metadatos del modelo actualizados en Analysis Services.

Puede deshacer/rehacer los cambios realizados en un Script DAX usando los atajos de teclado habituales (Ctrl+Z / Ctrl+Y).

## Múltiples scripts DAX

Puede crear tantos documentos Script DAX como desee si prefiere tener varias ventanas de documento abiertas en lugar de una sola. De esta forma, puedes usar las funciones habituales del IDE para colocar los documentos uno al lado del otro, en monitores diferentes, etc. Ten en cuenta que el código de las ventanas de Script DAX no se actualiza automáticamente cuando se realizan cambios en la expresión o en las propiedades del objeto en el TOM. En otras palabras, si tienes dos o más Scripts DAX que contienen la definición del mismo objeto(s), el último Script DAX que se aplique (F5) siempre sobrescribirá cualquier cambio realizado mediante otros Scripts DAX o directamente a través de la **vista de propiedades**.

## Trabajar con archivos de Script DAX

Los Scripts DAX se pueden guardar como archivos de texto, usando la extensión `.te3daxs`. Para guardar un Script DAX como archivo, simplemente usa la opción **Archivo > Guardar** (Ctrl+S). Para abrir un Script DAX desde un archivo de texto, usa la opción **Archivo > Abrir > Archivo...** (Ctrl+O).

> [!NOTE]
> Los Scripts DAX no son específicos de un modelo, pero como las expresiones DAX pueden apuntar a medidas, columnas y tablas definidas en el modelo, no se garantiza que cualquier Script DAX pueda aplicarse a cualquier modelo. Los scripts DAX son especialmente útiles para trabajar con varios objetos DAX dentro de un único documento, en el contexto de un modelo de datos específico.

## Editor de Script DAX

El editor de Script DAX tiene todas las capacidades del editor DAX que se usa en otras partes de Tabular Editor 3. En concreto, autocompletado, autoformato, información de parámetros, etc.

Además, para gestionar fácilmente Scripts DAX extensos, se muestran dos listas desplegables en la parte superior de la vista de Script DAX. El menú desplegable de la izquierda te permite cambiar entre los objetos definidos en el script, mientras que el de la derecha te permite cambiar entre las propiedades del objeto actual.

![Navegación del Script DAX](~/content/assets/images/dax-script-navigation.png)

## Definir medidas

Si quieres incluir la definición de una medida a la que se hace referencia en el script, pero que todavía no está definida en el script, puedes hacerlo haciendo clic con el botón derecho en una referencia de medida y eligiendo la opción "Definir medida" o "Definir medida con dependencias".

![Definir medida con dependencias](~/content/assets/images/define-measure-with-deps.png)

## Atajos

Para aplicar el script al modelo, usa los siguientes atajos:

- **F5**: Aplicar el script completo a los metadatos del modelo local
- **Shift+F5**: Aplicar el script completo a los metadatos del modelo local y, a continuación, guardar los metadatos del modelo de nuevo en el origen
- **F8**: Aplicar la parte seleccionada actualmente del script a los metadatos del modelo local
- **Shift+F8**: Aplicar la parte seleccionada actualmente del script a los metadatos del modelo local y, a continuación, guardar los metadatos del modelo de nuevo en el origen

## Objetos DAX compatibles

Tabular Editor 3 admite la edición de los siguientes tipos de objetos mediante un Script DAX:

- Medidas (incluidos los KPI)
- Columnas calculadas
- Tablas calculadas
- Grupos de cálculo (incluidos los elementos de cálculo)

# Sintaxis del Script DAX

La sintaxis de los Scripts DAX es la siguiente:

```dax
<DAX script>:
MEASURE 'Table name'[Measure name] [= [<DAX expression>]]
    [<Measure properties>]

COLUMN 'Table name'[Column name] [= [<DAX expression>]]
    [<Column properties>]

TABLE 'Table name' [= [<DAX expression>]]
    [<Table properties>]

CALCULATIONGROUP 'Table name'[Column name]
    [<Calculation Group properties>]
    CALCULATIONITEM "Item 1" [= [<DAX expression>]]
        [<Calculation Item properties>]
    CALCULATIONITEM "Item 2" [= [<DAX expression>]]
        [<Calculation Item properties>]
    ...

<Measure properties>:
    DetailRows = [<DAX expression>]
    DisplayFolder = ["string"]
    FormatString = ["string" / <DAX expression>]
    Description = ["string"]
    Visible = TRUE/FALSE
    KpiStatusExpression = [<DAX expression>]
    KpiStatusDescription = ["string"]
    KpiStatusGraphic = ["string"]
    KpiTrendExpression = [<DAX expression>]
    KpiTrendDescription = ["string"]
    KpiTrendGraphic = ["string"]
    KpiTargetExpression = [<DAX expression>]
    KpiTargetDescription = ["string"]
    KpiTargetFormatString = ["string"]

<Column properties>:
    DisplayFolder = ["string"]
    FormatString = ["string"]
    Description = ["string"]
    Visible = TRUE / FALSE
    Datatype = BOOLEAN / DOUBLE / INTEGER / DATETIME / CURRENCY / STRING

<Table properties>:
    Description = ["string"]
    Visible = TRUE / FALSE
    DetailRows = [<DAX expression>]

<Calculation Group properties>:
    Description = ["string"]
    Visible = TRUE / FALSE
    Precedence = <integer value>

<Calculation Item properties>
    Description = ["string"]
    Ordinal = <integer value>
    FormatString = [<DAX expression>]
```

> [!TIP]
> Los usuarios de TMDL sin duda habrán notado que hay algunas similitudes entre la sintaxis de los Scripts DAX y la sintaxis de TMDL. De hecho, TMDL se inspiró en los Scripts DAX. Sin embargo, para simplificar, los Scripts DAX solo admiten intencionadamente objetos que tengan una o varias expresiones DAX asociadas. Además, la sintaxis de los Scripts DAX está diseñada para ser compatible con la sección `DEFINE` de una consulta DAX (siempre que el Script DAX no especifique ninguna propiedad de objeto). TMDL, en cambio, se usa para definir todos los metadatos del modelo y no se limita a los objetos DAX. Sin embargo, los bloques de código TMDL no se pueden usar directamente en una consulta DAX, ya que la sintaxis para definir los nombres de los objetos en TMDL no es válida en DAX.

## Ejemplo 1: Medida

Como ejemplo, el siguiente script define la medida `[Internet Total Sales]` en la tabla `'Internet Sales'`. Además de la expresión DAX de la medida, el script también incluye la descripción y la cadena de formato de la medida.

```dax
----------------------------------
-- Medida: [Internet Total Sales]
----------------------------------
MEASURE 'Internet Sales'[Internet Total Sales] = SUM('Internet Sales'[Sales Amount])
    Description = "Devuelve la suma de todas las ventas por Internet"
    FormatString = "\$#,0.00;(\$#,0.00);\$#,0.00"
```

## Ejemplo 2: Medida con KPI de estado y objetivo

El siguiente Script DAX define la medida `[Internet Current Quarter Sales Performance]`, que incluye un KPI con una expresión de estado y otra de objetivo. El KPI de estado usa el gráfico "Shapes".

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
                IF(x < 1, -1, IF(x < 1.07, 0, 1))
            )
    , KpiStatusGraphic = "Shapes"
    , KpiTargetExpression = 1.1
```

## Ejemplo 3: Grupo de cálculo

El siguiente Script DAX define el grupo de cálculo `'Time Intelligence'` con la columna `[Period]`. El grupo de cálculo contiene 6 elementos de cálculo que realizan diversos cálculos de tiempo. Observe cómo el elemento `"YoY %"` aplica una cadena de formato diferente.

```dax
-----------------------------------------
-- Grupo de cálculo: 'Time Intelligence'
-----------------------------------------
CALCULATIONGROUP 'Time Intelligence'[Period]
    Description = "Utilice esta tabla para realizar cálculos de tiempo"

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

# Expresiones o propiedades sin especificar o vacías

A partir de Tabular Editor 3.16.0, es posible especificar expresiones y valores de propiedad vacíos en Scripts DAX, o incluso omitir por completo las expresiones del objeto.

Por ejemplo, el siguiente script creará una medida con una expresión DAX vacía, una cadena de formato vacía y sin carpeta de visualización. Si la medida ya existe, se actualizará para tener una expresión DAX vacía, una cadena de formato vacía y sin carpeta de visualización.

```dax
MEASURE 'Internet Sales'[Internet Total Sales] =
    , Description = "TODO: Consultar con el área de negocio cómo debe implementarse y formatearse."
    , FormatString =
    , DisplayFolder =
```

Ten en cuenta que la coma (`,`) antes de las propiedades que siguen a una expresión vacía es obligatoria. Las comas son opcionales cuando la expresión anterior no está vacía.

Si quieres conservar la expresión DAX existente de una medida, puedes omitir el signo `=` después del nombre del objeto:

```dax
MEASURE 'Internet Sales'[Internet Total Sales]
    DisplayFolder = "Totals"
```

El ejemplo anterior actualizará la medida `[Internet Total Sales]` para que tenga el `DisplayFolder` especificado, pero mantendrá la expresión DAX existente. El resto de las propiedades del objeto, como `Description` y `FormatString`, permanecerán sin cambios.

Estas nuevas características facilitan escribir scripts que solo actualizan propiedades concretas de un objeto, sin tener que especificar toda la definición del objeto. De este modo, los scripts se pueden reutilizar más fácilmente en distintos modelos.
