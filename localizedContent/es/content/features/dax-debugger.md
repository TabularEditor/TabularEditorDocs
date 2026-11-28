---
uid: dax-debugger
title: Depurador DAX
author: Daniel Otykier
updated: 2026-11-25
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
# Depurador DAX

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/m4g9BxcUf4U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

No es ningún secreto que DAX es un lenguaje relativamente complejo y difícil de dominar. La mayoría de los desarrolladores de modelos de datos probablemente han experimentado una situación en la que el código DAX no devolvió el resultado esperado. En este caso, ayuda desglosar el código, variable por variable y llamada a función por llamada a función, para entender mejor qué está pasando.

Hasta ahora, este «desglose» del código era una tarea tediosa y que llevaba mucho tiempo, y a menudo implicaba capturar consultas DAX ejecutadas por herramientas cliente para poder desglosarlas y ejecutar partes más pequeñas de las consultas en [DAX Studio](https://daxstudio.org/) o [SQL Server Management Studio](https://docs.microsoft.com/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15).

Tabular Editor 3 introduce el **Depurador de DAX**, una herramienta que hace que el proceso de depurar paso a paso el código DAX de tu modelo sea mucho, mucho más sencillo. A nivel conceptual, el depurador es similar a los depuradores tradicionales de los IDE, como el que se encuentra en Visual Studio al desarrollar aplicaciones C#.

## Requisitos previos

El Depurador de DAX analiza el código DAX de tu modelo y genera consultas DAX adecuadas para evaluar subexpresiones, contextos de fila, etc., lo que te permite recorrer el código de forma interactiva.

Para que esto funcione, Tabular Editor 3 debe operar en modo **conectado** o en **modo del área de trabajo**, como cuando se cargan los metadatos del modelo directamente desde Power BI Desktop o desde cualquier otra instancia de Analysis Services.

# Primeros pasos

Mientras Tabular Editor 3 está conectado a una instancia de Analysis Services, el depurador se puede iniciar de una de estas dos maneras:

- Mediante una Pivot Grid
- A través de una consulta DAX

Una vez iniciado el depurador, se le presentan varias vistas nuevas que proporcionan información contextual sobre el código que se está depurando. La parte del código que se está depurando en ese momento se resalta en una vista de script de depuración cuando pertenece al modelo, y en la consulta DAX cuando la consulta la define.

> [!TIP]
> Antes de iniciar una sesión de depuración, considera dar formato a tu código DAX para que sea más fácil de leer.

# Depuración mediante un Pivot Grid

1. Crea un nuevo Pivot Grid (**Archivo > Nuevo > Pivot Grid**)
2. Agrega la medida que quieras depurar al Pivot Grid. Puedes elegir entre lo siguiente:

- Arrastrar una medida desde el Explorador TOM, o
- Hacer clic con el botón derecho en una medida en el Explorador TOM y elegir **Agregar a Pivot Grid**, o
- Seleccionar la medida desde la lista de campos del Pivot Grid (**Pivot Grid > Mostrar campos**)
3. (Opcional) Añada una o más columnas o jerarquías al Pivot Grid en el área de Filtros, el área de Columnas o el área de Filas.
4. Haz clic con el botón derecho en la celda de valor dentro del Pivot Grid y elige **Depurar este valor**.

![Depurar desde tabla dinámica](~/content/assets/images/features/debug-from-pivot.png)

# Depuración mediante una Consulta DAX

1. Crea una nueva consulta DAX (**Archivo > Nuevo > Consulta DAX**).
2. Escriba o pegue la consulta DAX. Por lo general, debería tratarse de una consulta formada por una llamada `SUMMARIZECOLUMNS` con una o más medidas (explícitas), como la generada por los elementos visuales en Power BI. Las medidas pueden ser medidas del modelo o medidas que la consulta define con `DEFINE MEASURE`.

> [!TIP]
> Puedes usar el [Performance Analyzer](https://docs.microsoft.com/power-bi/create-reports/desktop-performance-analyzer) en Power BI Desktop para capturar la consulta generada por los objetos Visual.

3. Pulsa F5 para ejecutar la consulta en Tabular Editor 3. Localice el valor que desea depurar, haga clic con el botón derecho en la celda y elija **Depurar celda**.

![Menú contextual en una celda de resultados de una consulta DAX, que muestra la opción «Depurar celda»](~/content/assets/images/features/debug-from-query.png)

# Vistas de depuración

El depurador proporciona las siguientes vistas (si están ocultas, puedes acceder a ellas mediante el menú **Depurar > Ventanas**).

- Variables locales
- Inspección
- Contexto de evaluación
- Árbol de llamadas

## Variables locales

Esta vista enumera las columnas, las medidas y las variables dentro del ámbito de ejecución actual y muestra sus valores. También muestra el valor de la subexpresión actual que se está depurando. Los valores de esta lista se actualizan automáticamente al avanzar a otra subexpresión o cuando se cambia el contexto de evaluación. **Los valores locales siempre se evalúan en el elemento actualmente seleccionado del árbol de llamadas**.

![Variables locales](~/content/assets/images/locals.png)

Puede inspeccionar un valor de variables locales haciendo clic en el botón de la lupa dentro de la columna **Valor**. Se abrirá un cuadro de diálogo emergente que muestra el valor con más detalle. Esto es especialmente útil si el valor inspeccionado es una tabla.

![Inspeccionar valor de variables locales](~/content/assets/images/inspect-locals.png)

Si prefiere inspeccionar el valor de las variables locales en una ventana de consulta DAX independiente, puede desactivar la opción **Usar inspector emergente** en **Herramientas > Preferencias > Tabular Editor > Depurador de DAX > Variables locales**.

![Página de preferencias del Depurador DAX con las secciones Variables locales, Observación y Consultas DAX](~/content/assets/images/features/dax-debugger-settings.png)

## Inspección

Esta vista le permite introducir cualquier expresión DAX, que se calculará dentro del contexto de evaluación actual. Puede introducir expresiones escalares y de tabla, puede usar todas las funciones DAX disponibles y hacer referencia a variables dentro del ámbito de evaluación actual. Los valores de seguimiento se actualizan automáticamente al avanzar a otra subexpresión o cuando se cambia el contexto de evaluación. **Los valores de seguimiento siempre se evalúan en el ámbito del elemento actualmente seleccionado en la pila del contexto de evaluación**.

![Inspección](~/content/assets/images/watch.png)

Para añadir rápidamente una variable, una medida o una subexpresión a la vista Inspección, simplemente resalte una parte del código y arrástrela a la vista Inspección. También puede colocar el cursor sobre la expresión que quiera añadir; luego haga clic con el botón derecho y elija **Inspeccionar esta expresión**:

![Añadir rápidamente a Inspección](~/content/assets/images/quick-add-to-watch.png)

Para añadir, duplicar o eliminar expresiones de Inspección, utilice el menú contextual con clic derecho de la vista Inspección:

![Menú contextual de Inspección](~/content/assets/images/watch-context-menu.png)

La opción **Generar consulta** es idéntica al botón de la lupa de la columna **Valor**, como se resalta en la captura de pantalla siguiente. Al hacer clic en esto, el depurador abrirá un nuevo documento de Consulta DAX, que define tanto el contexto del cálculo como el propio cálculo, lo que te permitirá inspeccionar los resultados con más detalle. Esto resulta especialmente útil cuando la expresión de seguimiento es una expresión de tabla, como se muestra a continuación:

![Inspeccionar la ventana de inspección](~/content/assets/images/inspect-watch.png)

> [!TIP]
> ¿Cuál es la diferencia entre la vista **Locals** y la vista **Watch**?
>
> - **Locals** muestra los valores de las columnas, medidas, variables y otras subexpresiones relevantes dentro del ámbito de ejecución actual, incluido el valor de la subexpresión seleccionada actualmente en el árbol de llamadas.
> - **Watch** le permite introducir cualquier expresión DAX, que se calculará dentro del contexto de evaluación actual.

## Contexto de evaluación

Esta vista proporciona información sobre el contexto de evaluación de DAX de la subexpresión actual. Por ejemplo, una expresión `CALCULATE` puede realizar una transición de contexto o agregar un filtro al contexto de evaluación, o un iterador `SUMX` puede agregar un contexto de fila.

![contexto de evaluación](~/content/assets/images/evaluation-context.png)

Puede hacer doble clic en un elemento de la pila de contexto de evaluación, para llevar el foco a ese elemento. Esto hará que todas las expresiones de **Watch** se vuelvan a evaluar en el nuevo contexto (es decir, todos los contextos desde la parte inferior de la pila hasta e incluyendo el elemento actualmente enfocado). Esto se ilustra en la animación siguiente. Fíjese también en cómo puede inspeccionar el valor de columnas individuales en el contexto de fila activo desplazándose por las filas dentro de cualquier iteración activa:

![Árbol de llamadas](~/content/assets/images/navigating-evaluation-context.gif)

También puedes activar o desactivar filtros individuales del contexto de filtro externo (por ejemplo, las columnas de agrupación en la llamada a [`SUMMARIZECOLUMNS`](https://dax.guide/summarizecolumns) que generó la consulta o los filtros especificados en un Pivot Grid). Esto se ilustra en la animación siguiente. Los filtros activados o desactivados de esta manera se aplicarán tanto a Watch como a Locals.

![Árbol de llamadas](~/content/assets/images/toggle-filters.gif)

Por último, puede examinar las primeras 1000 filas de cualquier iterador y establecer el contexto de fila actual en una fila específica dentro de esas primeras 1000 haciendo clic en el botón Zoom de la columna **Fila**.

![Explorar contextos de fila](~/content/assets/images/browse-row-contexts.png)

## Árbol de llamadas

Esta vista ofrece un esquema de todo el cálculo y le permite navegar fácilmente entre subexpresiones haciendo doble clic (también puede usar teclas de acceso directo para la navegación). El árbol también proporciona información sobre transiciones de contexto, iteraciones y contextos de fila. Las ramas de código que no se ejecutarán (por ejemplo, en una llamada a `IF` o `SWITCH`, o cuando un iterador está vacío) se muestran tachadas.

![Árbol de llamadas](~/content/assets/images/call-tree.png)

A medida que navegas entre los elementos del árbol de llamadas, el script de depuración de DAX resaltará el código correspondiente al elemento del árbol de llamadas y, además, indicará (con un fondo gris) la ruta seguida para llegar al código resaltado, como se muestra a continuación:

![Árbol de llamadas](~/content/assets/images/navigating-call-tree.gif)

Fíjate en cómo se actualizan los valores de la vista **Locals** a medida que navegas por el árbol. También puedes ir a una subexpresión colocando el cursor sobre la expresión, haciendo clic con el botón derecho y seleccionando la opción **Entrar en la selección** (Ctrl+B).

![Entrar en la selección](~/content/assets/images/debugger-step-into-selection.png)

## Funciones y código definido por la consulta

El depurador entra en las [funciones definidas por el usuario de DAX](xref:udfs) (UDF de DAX) y en las medidas y funciones que define una consulta DAX.

### Entrar en funciones

Entra en una UDF de DAX de la misma manera que entra en una referencia de medida. Esto funciona para las funciones del modelo y para las funciones que la consulta DAX define con `DEFINE FUNCTION`.

En el **Árbol de llamadas**, una llamada a función tiene un nodo secundario por cada argumento pasado a un parámetro `VAL`, seguido de un nodo `Function F(params)`, como `Function Scale(x, f)`, con el cuerpo de la función debajo. Los argumentos pasados a `EXPR` y los parámetros de tipo referencia aparecen en el cuerpo, en cada lugar en el que el cuerpo utiliza el parámetro. Un nodo que se refiere a un parámetro muestra el nombre del parámetro con el argumento tal como está escrito en el punto de llamada, como `x: [Sales Amount]`, en una línea y truncado a 60 caracteres. Si la llamada omite un argumento opcional, el nodo muestra el valor predeterminado del parámetro.

![Árbol de llamadas con un nodo de llamada a función, su nodo Function Scale(x, f) y los nodos de parámetros, junto a «Locales» mostrando los parámetros](~/content/assets/images/features/dax-debugger-call-tree-function.png)

Mientras el elemento actual se encuentre dentro del cuerpo de una función, **Locales** mostrará los parámetros de la función, cada uno con el argumento que le pasa la llamada, y ocultará las variables del código de llamada. Un parámetro `VAL` muestra el valor calculado en el punto de llamada, y un parámetro `EXPR` o de tipo referencia muestra su argumento evaluado en el contexto de evaluación actual. Cuando el elemento actual está dentro de un argumento pasado a un parámetro `EXPR`, **Locales** muestra el ámbito en el que está escrito el argumento: las variables del código llamante y los parámetros de la función contenedora si la llamada está dentro de otra función.

### Código definido en la consulta DAX

Cuando depura una celda de una consulta DAX, las medidas y funciones que la consulta define con `DEFINE MEASURE` o `DEFINE FUNCTION` se resaltan en la propia consulta DAX. La vista del script de depuración contiene las medidas del modelo, seguidas de las funciones del modelo, y se abre solo cuando el código depurado utiliza medidas o funciones del modelo. A medida que vas pasando del código de la consulta al código del modelo, la vista que contiene el elemento actual pasa a primer plano. Haga clic con el botón derecho en el código de la consulta DAX para usar **Entrar en selección** (**Ctrl+B**) y los comandos de observación, como en la vista de script de depuración.

Si la consulta redefine una medida o función del modelo, la redefinición se aplica únicamente al código propio de la consulta. Las medidas y funciones del modelo que utilizan el objeto redefinido mantienen la definición del modelo, al igual que cuando se ejecuta la consulta.

![Consulta DAX en proceso de depuración, con el cuerpo de la función resaltado en la consulta y el botón Detener depuración en la barra de herramientas Depuración](~/content/assets/images/features/dax-debugger-query-debugging.png)

La consulta DAX es de solo lectura mientras la depura, y el autocompletado no se abre en la consulta ni en la vista del script de depuración. Si escribe, pega o elimina texto en la consulta, aparece el mensaje **¿Detener depuración?** con el mensaje «No se puede editar una consulta DAX mientras se está depurando. ¿Desea detener la depuración para editar la consulta?»:

- **Aceptar** detiene la depuración. La modificación no se aplica, así que repítala una vez que la consulta sea editable.
- **Cancelar** mantiene la depuración y deja la consulta sin cambios.

Seleccione **No volver a preguntar** antes de seleccionar **Aceptar** para detener la depuración sin que aparezca el mensaje en futuras modificaciones. Para que vuelva a aparecer el mensaje, seleccione **Preguntar antes de editar una consulta DAX que se está depurando** en **Herramientas > Preferencias > Tabular Editor > Depurador de DAX > Consultas DAX**.

![Mensaje «¿Desea detener la depuración?» con la casilla de verificación «No volver a preguntar»](~/content/assets/images/features/dax-debugger-stop-debugging-prompt.png)

Si cierra la consulta DAX o la vista del script de depuración mientras depura, aparecerá el mensaje **¿Detener depuración?**. Seleccione **Aceptar** para detener la depuración y cerrar el documento.

### Detener depuración

Seleccione **Detener depuración** en la barra de herramientas **Depurar** o en el menú **Depurar** para finalizar la sesión. La consulta DAX vuelve a ser editable y se cierran la vista del script de depuración y las ventanas **Locales**, **Observación**, **Contexto de evaluación** y **Árbol de llamadas**. Cerrar el documento depurado o el modelo también finaliza la sesión y cierra las ventanas. En la siguiente sesión, las ventanas se abrirán de nuevo donde las dejó, con las mismas expresiones de vigilancia. **Detener depuración** no tiene ningún atajo de teclado predeterminado; asigne uno en **Herramientas > Preferencias > Tabular Editor > Teclado**.

## Predicados escalares

Los predicados escalares usados en los argumentos de filtro de las funciones [`CALCULATE`](https://dax.guide/calculate) o [`CALCULATETABLE`](https://dax.guide/calculatetable) se tratan de forma especial en la vista **Locals**.

Por ejemplo, la siguiente medida usa un predicado escalar para mostrar solo las ventas realizadas en EE. UU. o Canadá.

```dax
CALCULATE(
    [Total Sales],
    Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
)
```

A primera vista, la expresión de la línea 3 parece que devolverá un valor escalar (verdadero/falso). Sin embargo, en DAX, los filtros son tablas. En realidad, el predicado escalar se convierte en una expresión de tabla mediante la función [`FILTER`](https://dax.guide/filter), como se muestra a continuación:

```dax
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(Geography[Country Region Code]),
        Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
    )
)
```

La función `FILTER` es un iterador que recorre la tabla `ALL(Geography[Country Region Code])`, es decir, todos los valores únicos de la columna "Country Region Code" de la tabla "Geography". Los iteradores generan un contexto de filtro para cada fila de la iteración. A continuación, el predicado escalar se evalúa en cada uno de esos contextos de fila. En el caso de la función `FILTER`, solo se conservan las filas en las que el predicado se evalúa como `TRUE`. En este ejemplo, la función `FILTER` devolvería una tabla con 1 columna ("Country Region Code") y 2 filas ("US" y "CA").

Al depurar un predicado escalar, la vista **Locals** mostrará dos elementos especiales: **(Expresión actual)** y **(Expresión de filtro)**. Se describen a continuación:

![Depurar predicados escalares](~/content/assets/images/features/debug-scalar-predicates.png)

En la captura anterior:

1. Este es el predicado escalar que se está depurando en este momento. Aunque esta subexpresión parece que debería devolver un valor escalar (verdadero/falso), en realidad devuelve una tabla.
2. **(Expresión actual)**: Este es el valor _escalar_ del predicado cuando se evalúa dentro del _contexto de fila_ actual generado por la función `FILTER`, tal y como se describió anteriormente. En la captura de pantalla, el valor escalar se evalúa como `False`, porque el valor de [Country Region Code] en el contexto de fila actual es "AU", como se puede ver en la vista **Watch** (4). Podemos usar la vista **Contexto de evaluación** (5) para desplazarnos por las filas de la iteración, una por una.
3. **(Expresión de filtro)**: Esta es la expresión de _tabla_ generada por la función `FILTER`, tal y como se describió anteriormente. En la captura de pantalla, se trata de una tabla 1x2 que contiene los valores "US" y "CA". Al hacer clic en el botón de la lupa, se abrirá una ventana emergente que muestra los valores de la tabla en una cuadrícula.
4. Podemos usar la ventana **Watch** para evaluar cualquier expresión DAX dentro del contexto de evaluación actual. En este caso, como tenemos un contexto de fila activo, podemos hacer referencia directamente a columnas del contexto de fila, como `Geography[Country Region Code]`. Podemos ver que el valor actual de esta columna es "AU", por lo que el predicado escalar (2) se evalúa como `False`.
5. Podemos usar la vista **Contexto de evaluación** para desplazarnos por las filas de la iteración, una por una. Esto actualizará los valores de las vistas **Locals** y **Watch** para que reflejen los valores del contexto de fila actual.

## Atajos de teclado

Usa los siguientes atajos de teclado para navegar rápidamente por el árbol de llamadas:

- **Step in (F11)**: entra en el primer elemento secundario del elemento actual en el árbol de llamadas. Si no hay más elementos secundarios, salta al siguiente elemento del mismo nivel.
- **Step out (Mayús-F11)**: vuelve al elemento padre del elemento actual en el árbol de llamadas.
- **Step over (F10)**: salta al siguiente parámetro de la función, a la siguiente subexpresión de una operación aritmética, o entra en la llamada a la función actual (si es una función no trivial).
- **Step back (Mayús-F10)**: salta al parámetro anterior de la función, a la subexpresión anterior de una operación aritmética o vuelve al elemento padre del elemento actual si no hay parámetros ni subexpresiones antes del elemento actual.
- **Step into selection (Ctrl-B)**: salta a la expresión situada bajo el cursor. Si varias rutas conducen a la misma expresión (por ejemplo, cuando una medida está referenciada por varias medidas y dichas medidas), un cuadro de diálogo le pedirá que elija la ruta.
- **Next row (F9)**: cambia el contexto de fila de la iteración más interna a la siguiente fila del iterador.
- **Previous row (Mayús-F9)**: cambia el contexto de fila de la iteración más interna a la fila anterior del iterador.

**Detener depuración** no tiene ningún método abreviado de teclado predeterminado. Consulte [Detener depuración](#stop-debugging).

# Limitaciones y problemas conocidos

El depurador de DAX tiene las siguientes limitaciones:

- Solo se admite un subconjunto de expresiones de tabla DAX al depurar una consulta DAX (por ejemplo, se pueden depurar consultas que dependen de [SUMMARIZECOLUMNS](https://dax.guide/summarizecolumns), mientras que otras funciones de tabla no son compatibles). Por lo general, se admiten las consultas generadas por Power BI (que se pueden capturar a través del analizador de rendimiento de Power BI Desktop).
- Solo se pueden depurar celdas que devuelvan una medida, ya sea una medida del modelo o una que la consulta defina con `DEFINE MEASURE`. No se pueden depurar las celdas de las columnas de expresiones en línea, como `"Twice", Twice([Sales Amount])` en una llamada `SUMMARIZECOLUMNS`, ni las medidas implícitas.
- No se admiten las expresiones de **Observación** que hacen referencia a una medida de ámbito de consulta o a un parámetro de función.
- Al examinar las primeras 1000 filas de un iterador que proviene de una expresión de tabla filtrada, la fila seleccionada en la ventana de exploración puede no corresponder siempre al contexto de fila actual en la pila de contexto de evaluación (escribe `CALCULATETABLE('<table name>')` en la ventana **Watch** para inspeccionar el contexto de fila actual).
- El depurador solo permite depurar expresiones DAX en medidas.
- No se pueden depurar las celdas que dependen de columnas con ámbito de consulta. Esto incluye los [cálculos visuales](https://learn.microsoft.com/power-bi/transform-model/desktop-visual-calculations-overview), que se definen mediante columnas con ámbito de consulta.
- Si una medida se modifica mediante un elemento de cálculo en el contexto de filtro, los resultados parciales mostrados en la vista Watch / Locals del depurador pueden ser incorrectos.

Si encuentras un problema con el depurador, distinto de los indicados anteriormente, publícalo en nuestro [seguimiento de incidencias](https://github.com/TabularEditor/TabularEditor3/issues) en el sitio de soporte de la comunidad de TE3 en GitHub.

# Hoja de ruta

Tenemos previsto añadir muchas más funciones al Depurador de DAX a lo largo del tiempo, para abordar los problemas anteriores y hacer que la herramienta sea aún más completa. Como siempre, los comentarios son más que bienvenidos. Por favor, utilice la [sección de Discusiones](https://github.com/TabularEditor/TabularEditor3/discussion) para solicitar nuevas funciones y para debates generales.

**¡Feliz depuración!**
