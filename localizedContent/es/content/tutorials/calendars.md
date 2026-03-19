---
uid: calendars
title: Calendarios (inteligencia temporal mejorada)
author: Daniel Otykier y María José Ferreira
updated: 2026-01-22
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

# Calendarios (inteligencia temporal mejorada)

La versión de septiembre de 2025 de Power BI Desktop incorporó una nueva característica en versión preliminar pública llamada **Inteligencia temporal mejorada** (también conocida como **Inteligencia temporal basada en calendario**). Esta característica le permite definir calendarios personalizados en su modelo semántico, lo que habilita cálculos de inteligencia temporal en distintos sistemas de calendario, como los fiscales, los minoristas (4-4-5, 4-5-4, 5-4-4), el ISO y otros calendarios no gregorianos.

A diferencia de las funciones clásicas de inteligencia temporal, que asumen un calendario gregoriano estándar, las nuevas funciones basadas en calendario derivan su comportamiento de las asignaciones explícitas de columnas que defina en su tabla de fechas. Este enfoque también incorpora cálculos de inteligencia temporal a nivel de semana que antes resultaban difíciles de realizar.

Para más información sobre cómo funciona la inteligencia temporal basada en calendario, consulta:

- [Presentación de la inteligencia temporal basada en calendario en DAX](https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/) (SQLBI)
- [Versión preliminar de la inteligencia temporal basada en calendario](https://powerbi.microsoft.com/en-us/blog/calendar-based-time-intelligence-time-intelligence-tailored-preview/) (Microsoft)

## Definición de un calendario

![Crear un calendario](~/content/assets/images/tutorials/calendar-create.png)

1. Haz clic con el botón derecho en una tabla de tu modelo (normalmente una tabla de fechas) y selecciona **Crear > Calendario...**.
2. Asigne un nombre al calendario; por ejemplo, `Fiscal`.

Una vez que se agregan calendarios a una tabla, se mostrarán en el Explorador TOM, en el nodo **Calendars**:

![Calendario en el Explorador TOM](~/content/assets/images/tutorials/calendar-tom-explorer.png)

Antes de poder usar un calendario en sus cálculos de DAX, debe configurarlo asignando las columnas de la tabla a las categorías de unidades de tiempo correspondientes.

## Editor de calendario

La versión de enero de 2026 de Tabular Editor 3 incorporó un **Editor de calendario** dedicado que ofrece una interfaz completa para configurar calendarios. El editor muestra todas las categorías de unidades de tiempo en una cuadrícula estructurada con descripciones emergentes útiles y realiza una validación en tiempo real para ayudarle a evitar errores de configuración.

### Abrir el Editor de calendario

Puede abrir el Editor de calendario de cualquiera de las siguientes formas:

- Haga doble clic en un calendario existente debajo de una tabla en el Explorador TOM.
- Haga clic con el botón derecho en un calendario existente debajo de una tabla en el Explorador TOM y elija **Editar calendario...**.
- Seleccione un calendario en el Explorador TOM y, luego, abra el menú **Calendario** y elija **Editar calendario...**.
- Abra el menú **Vista** y elija **Editor de calendario**.

![Editor de calendario](~/content/assets/images/tutorials/calendar-editor.png)

### Diseño del Editor de calendario

El Editor de calendario se divide en dos áreas principales:

1. **Cuadrícula de calendarios (panel izquierdo)**
   Una cuadrícula vertical donde cada calendario se muestra como una columna y las categorías de unidades de tiempo se muestran como filas. Las filas se organizan jerárquicamente por año, trimestre, mes, semana y día. En esta cuadrícula puedes:

   - Selecciona la tabla de la que el calendario debe tomar sus columnas (normalmente una tabla de fechas) en la fila **Tabla**.
   - Asigna columnas a categorías de unidad de tiempo seleccionando una opción en el menú desplegable de cada celda.
   - Consulta los resultados de validación en tiempo real mediante iconos y descripciones emergentes.
   - Crea calendarios adicionales con la columna **+ Agregar calendario** (si tu modelo requiere varias definiciones de calendario).
   - Cambia el nombre de los calendarios editando el nombre directamente en la cuadrícula.
   - Elimina calendarios haciendo clic con el botón derecho en una columna de calendario.

2. **Panel de contexto (panel derecho)**
   Un panel de detalles que cambia según tu selección en la cuadrícula de calendarios:

   - **Columnas asociadas**: Cuando seleccionas una fila de unidad de tiempo que tiene una columna asignada, este panel te permite seleccionar columnas asociadas adicionales.
   - **Columnas relacionadas con el tiempo**: Cuando seleccionas la fila "Columnas relacionadas con el tiempo" en la parte inferior de la cuadrícula, este panel te permite marcar columnas como relacionadas con el tiempo.

![Diseño del Editor de calendario que muestra la cuadrícula de calendarios y el panel de contexto](~/content/assets/images/tutorials/calendar-editor-parts.png)

### Asignar columnas a unidades de tiempo

La cuadrícula de calendarios muestra todas las categorías de unidades de tiempo disponibles. Para asignar una columna a una unidad de tiempo, haz clic en una celda de unidad de tiempo debajo de una columna de calendario en la cuadrícula. Esto abre un menú desplegable donde puedes seleccionar la **columna principal** para esa unidad de tiempo.

![Seleccionar una columna en el menú desplegable](~/content/assets/images/tutorials/calendar-dropdown-column-selection.png)

No necesitas asignar todas las unidades de tiempo; solo las que se apliquen a la estructura de tu calendario y para las que tu tabla tenga las columnas adecuadas.

Las unidades de tiempo se dividen en categorías **completas** (que identifican de forma única un período por sí mismas) y categorías **parciales** (que requieren asignar primero una unidad de tiempo principal). Pasa el cursor sobre cualquier fila de unidad de tiempo para ver una descripción emergente con el formato de datos esperado y ejemplos.

![Descripción emergente de una unidad de tiempo completa que muestra la descripción y ejemplos](~/content/assets/images/tutorials/calendar-complete-time-unit-tooltip.png)

En el caso de las unidades de tiempo parciales, la descripción emergente también muestra qué unidades de tiempo principales deben asignarse:

![Descripción emergente de una unidad de tiempo parcial que muestra dependencias](~/content/assets/images/tutorials/calendar-partial-time-unit-tooltip.png)

#### Ejemplo: usar unidades de tiempo parciales

En algunos casos, tu tabla de fechas puede no tener columnas que identifiquen de forma única unidades de tiempo completas como Trimestre o Mes (por ejemplo, "T1 2024" o "enero de 2024"). En su lugar, podrías tener columnas como `QuarterOfYear` (1-4) y `MonthOfYear` (1-12) que solo tienen sentido cuando se combinan con una columna de Año.

En este escenario, puedes mapear las unidades de tiempo parciales (`Quarter of Year`, `Month of Year`) junto con la unidad de tiempo completa `Year`. Esta es una configuración válida porque las unidades de tiempo parciales pueden obtener su contexto completo del mapeo de `Year`.

![Una configuración de calendario con unidades de tiempo parciales](~/content/assets/images/tutorials/calendar-simple-example.png)

> [!TIP]
> Para ver las columnas disponibles y sus valores mientras configuras tu calendario, haz clic con el botón derecho en tu tabla de fechas en el Explorador TOM y elige **Vista previa de datos**.
>
> ![Opción Vista previa de datos en el menú contextual](~/content/assets/images/tutorials/calendar-preview-data-button.png)
>
> Después, puedes acoplar la ventana de Vista previa de datos junto al Editor de calendario para consultarla fácilmente.
>
> ![Acoplando la ventana de Vista previa de datos](~/content/assets/images/tutorials/calendar-dock-example.png)
>
> Como alternativa, puedes usar la ventana **Consulta DAX** para consultar tu tabla de fechas y mantenerla visible junto al Editor de calendario.

Con la Vista previa de tabla de la tabla de fechas acoplada, puedes ver los valores de las columnas mientras configuras tu calendario:

![Editor de calendario con la Vista previa de tabla de la tabla de fechas](~/content/assets/images/tutorials/calendar-configured-example.png)

**Unidades de tiempo completas:**

| Unidad de tiempo | Descripción                    | Ejemplos                       |
| ---------------- | ------------------------------ | ------------------------------ |
| Año              | El año                         | 2024, 2025                     |
| Trimestre        | El trimestre incluyendo el año | T1 2024, T2 2025               |
| Mes              | El mes incluyendo el año       | Enero de 2023, Febrero de 2024 |
| Semana           | La semana incluyendo el año    | Semana 50 de 2023, W50-2023    |
| Fecha            | La fecha                       | 31/12/2025, 3/4/2023           |

**Unidades de tiempo parciales** (requieren que se asigne una unidad de tiempo principal):

| Unidad de tiempo     | Descripción                      | Ejemplos             | Requiere  | O requiere uno de                                                                                                                                                                                                                                                                                                                          |
| -------------------- | -------------------------------- | -------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Trimestre del año    | El trimestre del año             | Q1, Trimestre 2, YQ1 | Año       |                                                                                                                                                                                                                                                                                                                                            |
| Mes del año          | El mes del año                   | Enero, M11, 11       | Año       |                                                                                                                                                                                                                                                                                                                                            |
| Mes del trimestre    | El mes dentro del trimestre      | 1, QM2               | Trimestre | <ul><li>Trimestre del año + Año</li></ul>                                                                                                                                                                                                                                                                                                  |
| Semana del año       | La semana del año                | Semana 50, W50, 50   | Año       |                                                                                                                                                                                                                                                                                                                                            |
| Semana del trimestre | La semana dentro de un trimestre | QW10, 10             | Trimestre | <ul><li>Trimestre del año + Año</li></ul>                                                                                                                                                                                                                                                                                                  |
| Semana del mes       | La semana dentro de un mes       | MW2, 2               | Mes       | <ul><li>Mes del año + Año</li><li>Mes del trimestre + Trimestre</li><li>Mes del trimestre + Trimestre del año + Año</li></ul>                                                                                                                                                                                                              |
| Día del año          | El día del año                   | 365, D1              | Año       |                                                                                                                                                                                                                                                                                                                                            |
| Día del trimestre    | El día dentro de un trimestre    | QD2, 50              | Trimestre | <ul><li>Trimestre del año + Año</li></ul>                                                                                                                                                                                                                                                                                                  |
| Día del mes          | El día del mes                   | MD10, 30             | Mes       | <ul><li>Mes del año + año</li><li>Mes del trimestre + trimestre</li><li>Mes del trimestre + trimestre del año + año</li></ul>                                                                                                                                                                                                              |
| Día de la semana     | El día de la semana              | WD5, 5               | Semana    | <ul><li>Semana del año + año</li><li>Semana del trimestre + trimestre</li><li>Semana del trimestre + trimestre del año + año</li><li>Semana del mes + mes</li><li>Semana del mes + mes del año + año</li><li>Semana del mes + mes del trimestre + trimestre</li><li>Semana del mes + mes del trimestre + trimestre del año + año</li></ul> |

### Columnas asociadas

Cuando asignas una columna a una unidad de tiempo, esa columna se convierte en la **columna principal** de esa unidad de tiempo. De forma opcional, puedes añadir **columnas asociadas** que representen la misma unidad de tiempo en un formato diferente.

Por ejemplo, si asignas una columna numérica `MonthNumber` (que contiene valores 1-12) a "Month of Year", puede que también quieras asociar una columna `MonthName` (que contiene "January", "February", etc.) con la misma unidad de tiempo. Ambas columnas representan el mismo concepto, pero en formatos distintos.

Para añadir columnas asociadas:

1. Selecciona en la cuadrícula una fila de unidad de tiempo que tenga una columna asignada.
2. En el panel **Columnas asociadas** de la derecha, marca las columnas que quieras asociar a esa unidad de tiempo.

Las columnas asociadas tienen el mismo comportamiento de filtro que la columna principal durante los cálculos de inteligencia temporal.

![Panel de columnas asociadas en el Editor de calendario](~/content/assets/images/tutorials/calendar-associated-columns.png)

## Limitaciones conocidas del Editor de calendario

- **Columnas "Ordenar por" y columnas asociadas**

Cuando una columna se usa como columna **Ordenar por** de una columna principal de la unidad de tiempo, Analysis Services la trata implícitamente como una columna asociada. No deberías añadir explícitamente esa columna de Ordenar por como columna asociada en el Editor de calendario, ya que esto provocará un error de Analysis Services (asignación duplicada).

Por ejemplo, si estableces `MonthName` como columna principal para "Mes del año" y `MonthName` tiene configurada `MonthNumber` como su columna Ordenar por, entonces `MonthNumber` queda asociada implícitamente. En este caso, no necesitas (ni debes) añadir `MonthNumber` como columna asociada explícita. La columna Ordenar por seguirá proporcionando el comportamiento mejorado del calendario esperado (incluida la gestión correcta de `FILTER` y `REMOVEFILTERS()`), ya que la asociación se infiere.

Ten en cuenta que este comportamiento es asimétrico: si, en su lugar, estableces la columna Ordenar por (p. ej., `MonthNumber`) como columna principal de unidad de tiempo, entonces la columna de presentación (p. ej., `MonthName`) **no** se trata automáticamente como asociada. En ese caso, si lo deseas, puedes añadir explícitamente la columna de visualización como columna asociada.

- **Las columnas ocultas no se muestran**

Las columnas cuya propiedad **Hidden** está establecida en `True` no aparecen en las listas desplegables de columnas del Editor de calendario ni en los paneles **Columnas asociadas** y **Columnas relacionadas con el tiempo**. Esto es un comportamiento no deseado, ya que es posible que las columnas ocultas aún deban usarse para la configuración del calendario (por ejemplo, las columnas de clave numérica usadas para ordenar suelen ocultarse a los usuarios finales).

Una versión futura de Tabular Editor solucionará estas limitaciones.

### Columnas relacionadas con el tiempo

Además de asignar columnas a categorías específicas de unidades de tiempo, puedes marcar columnas como **relacionadas con el tiempo**. Las columnas relacionadas con el tiempo son columnas de tu tabla de fechas que no encajan en una categoría específica de unidad de tiempo, pero aun así deberían recibir un tratamiento especial durante los cálculos de inteligencia temporal.

Algunos ejemplos de columnas relacionadas con el tiempo:

- `IsHoliday` - Un indicador que señala si la fecha es un día festivo
- `IsWeekday` - Un indicador que señala si la fecha es un día laborable
- `FiscalPeriodName` - Una etiqueta descriptiva para el período fiscal

**Cómo se comportan las columnas relacionadas con el tiempo:**

- Durante los **desplazamientos laterales** (como `DATEADD` o `SAMEPERIODLASTYEAR`), se conservan los filtros en las columnas relacionadas con el tiempo, manteniendo la misma granularidad.
- Durante los **desplazamientos jerárquicos** (como `DATESYTD` o `NEXTMONTH`), se eliminan los filtros en las columnas relacionadas con el tiempo.

Para más detalles sobre los desplazamientos laterales y jerárquicos, consulta [Comprender el desplazamiento lateral y el desplazamiento jerárquico](https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/#:~:text=Understanding%20lateral%20shift%20and%20hierarchical%20shift) (SQLBI).

Para configurar columnas relacionadas con el tiempo:

1. Selecciona la fila de **Columnas relacionadas con el tiempo** al final de la cuadrícula de calendarios.
2. En el panel **Columnas relacionadas con el tiempo** de la derecha, marca las columnas que quieras considerar como relacionadas con el tiempo.

![Panel de columnas relacionadas con el tiempo](~/content/assets/images/tutorials/calendar-time-related-columns.png)

### Aplicación de cambios

Los cambios realizados en el Editor de calendario se aplican al modelo local (pero no se guardan en disco) de dos maneras:

- Haz clic en el botón **Aceptar** de la barra de herramientas para aplicar los cambios al modelo local.
- Los cambios también se aplican automáticamente cuando sales del Editor de calendario (al perder el foco de la vista).

Puedes descartar los cambios pendientes haciendo clic en el botón **Cancelar** antes de cambiar a otra vista.

Para conservar los cambios, guarda el modelo.

## Validación en tiempo real

El Editor de calendario realiza una validación en tiempo real mientras configuras tus calendarios. Los avisos de validación se muestran mediante iconos y descripciones emergentes directamente en la cuadrícula, lo que te ayuda a identificar y resolver problemas antes de guardar.

Se aplican las siguientes reglas:

1. **Nombre de calendario único**
   Cada calendario debe tener un nombre único en el modelo semántico. Si creas un calendario con un nombre duplicado, el editor añade automáticamente un sufijo (p. ej., "(1)") para garantizar que sea único.

2. **Validación de dependencias de unidades de tiempo**
   Las unidades de tiempo parciales requieren que sus unidades de tiempo principales estén asignadas. Por ejemplo, si asignas una columna a "Día del mes", también debes asignar una columna a "Mes" (o a "Mes del año" + "Año", etc.). El editor resalta las celdas con dependencias faltantes y muestra una descripción emergente que explica qué unidades de tiempo principales son necesarias.

   ![Error de dependencia que muestra la unidad de tiempo principal que falta](~/content/assets/images/tutorials/calendar-dependency-error.png)

3. **Coherencia de categorías entre calendarios**
   Si tu modelo contiene varios calendarios, una columna debe estar asociada a la misma categoría de unidad de tiempo en todos los calendarios. Por ejemplo, si asignas una columna `FiscalYear` como "Año" en un calendario, no puedes asignar esa misma columna como "Semana del año" en otro calendario.

   ![Conflicto de categoría entre calendarios que muestra el error Time Unit Conflict](~/content/assets/images/tutorials/calendar-cross-category-validation.png)

## Configurar calendarios con el cuadro de diálogo de asignaciones de columnas

Como alternativa al Editor de calendario, puedes configurar un calendario haciendo clic con el botón derecho sobre él en el Explorador TOM y eligiendo la opción **Editar asignaciones de columna...**:

![Edición de las asignaciones de columnas del calendario](~/content/assets/images/edit-calendar-mappings.png)

Este cuadro de diálogo te permite añadir asociaciones de columnas de una en una. Haz clic en **Añadir asociación de columna** y elige **Asociación de columna** para añadir una nueva asignación. Para cada asociación, seleccionas una columna y la asignas a una categoría de unidad de tiempo. También puedes añadir más columnas asociadas a cada asignación; para ello, expande la propiedad **Columnas**.

![Asociaciones de columna en el Editor de colecciones](~/content/assets/images/tutorials/calendar-example.png)

#### Añadir columnas relacionadas con el tiempo en el cuadro de diálogo de asignaciones de columnas

Para añadir columnas relacionadas con el tiempo mediante este cuadro de diálogo, haz clic en **Añadir asociación de columna** y elige **Grupo de columnas**. Esto crea un grupo de columnas relacionadas con el tiempo, donde puedes añadir columnas que deben tratarse como relacionadas con el tiempo (consulta [Columnas relacionadas con el tiempo](#time-related-columns) para obtener más información sobre cómo se comportan estas columnas).

![Añadir un grupo de columnas para columnas relacionadas con el tiempo](~/content/assets/images/tutorials/calendar-collection-editor-column-group.png)

El editor de calendario se recomienda para la mayoría de los escenarios, ya que ofrece una visión más completa de todas las unidades de tiempo, descripciones emergentes útiles y mensajes de validación en tiempo real.

## Uso de calendarios en DAX

Una vez que hayas definido un calendario y asignado sus columnas, podrás usarlo en tus cálculos DAX. Los calendarios funcionan con las funciones de inteligencia temporal de DAX existentes que aceptan una columna de fecha como entrada (como [`TOTALYTD`](https://dax.guide/totalytd), [`CLOSINGBALANCEMONTH`](https://dax.guide/closingbalancemonth) y [`DATEADD`](https://dax.guide/dateadd)).

Además, se han incorporado 8 nuevas funciones DAX para la inteligencia temporal basada en semanas. Estas funciones solo funcionan con calendarios:

- [`CLOSINGBALANCEWEEK`](https://dax.guide/closingbalanceweek)
- [`OPENINGBALANCEWEEK`](https://dax.guide/openingbalanceweek)
- [`STARTOFWEEK`](https://dax.guide/startofweek)
- [`ENDOFWEEK`](https://dax.guide/endofweek)
- [`NEXTWEEK`](https://dax.guide/nextweek)
- [`PREVIOUSWEEK`](https://dax.guide/previousweek)
- [`DATESWTD`](https://dax.guide/dateswtd)
- [`TOTALWTD`](https://dax.guide/totalwtd)

Haz clic en los enlaces anteriores para obtener más información sobre cada función.
