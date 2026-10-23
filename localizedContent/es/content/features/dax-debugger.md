---
uid: dax-debugger
title: Depurador DAX
author: Daniel Otykier
updated: 2026-10-12
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

> [!NOTE]
> El depurador de DAX se introdujo en la versión 3.2.0. La información de este artículo está sujeta a cambios a medida que añadamos más funciones al depurador.

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/m4g9BxcUf4U" title="Reproductor de vídeo de YouTube" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

No es ningún secreto que DAX es un lenguaje relativamente complejo y difícil de dominar. La mayoría de los desarrolladores de modelos de datos probablemente se hayan encontrado en alguna ocasión con una situación en la que el código DAX no devolvía el resultado esperado. En esta situación, resulta útil desglosar el código, variable por variable y llamada a función por llamada a función, para comprender mejor qué está ocurriendo.

Hasta ahora, este «desglose» del código era una tarea tediosa y que requería mucho tiempo, que a menudo implicaba capturar las consultas DAX ejecutadas por las herramientas cliente para desglosarlas y ejecutar partes más pequeñas de las consultas en [DAX Studio](https://daxstudio.org/) o [SQL Server Management Studio](https://docs.microsoft.com/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15).

Tabular Editor 3 introduce el concepto de **depurador de DAX**, una herramienta que facilita mucho el proceso de adentrarse en el código DAX de tu modelo. A nivel conceptual, el depurador es similar a los depuradores de IDE tradicionales, como el que se encuentra en Visual Studio al desarrollar aplicaciones en C#.

## Requisitos previos
El depurador de DAX analiza el código DAX de su modelo y genera consultas DAX adecuadas para evaluar subexpresiones, contextos de fila, etc., lo que le permite recorrer el código de forma interactiva.

Para que esto funcione, Tabular Editor 3 debe operar en **modo conectado** o **modo espacio de trabajo**, como cuando se cargan los metadatos del modelo directamente desde Power BI Desktop o desde cualquier otra instancia de Analysis Services.

# Primeros pasos

Mientras Tabular Editor 3 está conectado a una instancia de Analysis Services, el depurador se puede iniciar de dos maneras diferentes:

- A través de un Pivot Grid
- A través de una consulta DAX

Una vez iniciado el depurador, se le presentan varias vistas nuevas que proporcionan información contextual sobre el código que se está depurando, así como una vista de script DAX que resalta la parte del código que se está depurando en ese momento.

> [!TIP]
> Antes de iniciar una sesión de depuración, plantéate formatear tu código DAX para que sea más fácil de leer.

# Depuración a través de un Pivot Grid

1. Cree una nueva Pivot Grid (**Archivo > Nuevo > Pivot Grid**)
2. Añade la medida que quieres depurar al Pivot Grid. Puedes:
  - Arrastrar una medida desde el Explorador TOM, o
  - Hacer clic con el botón derecho en una medida en el Explorador TOM y elegir **Agregar a Pivot Grid**, o
  - Seleccionar la medida de la lista de campos del Pivot Grid (**Pivot Grid > Mostrar campos**)
3. (Opcional) Añada una o más columnas o jerarquías al Pivot Grid en el área de Filtros, el área de Columnas o el área de Filas.
4. Haga clic con el botón derecho en la celda de valor dentro del Pivot Grid y elija **Depurar este valor**.

![Depurar desde la tabla dinámica](~/content/assets/images/features/debug-from-pivot.png)

# Depuración mediante una consulta DAX

1. Cree una nueva consulta DAX (**Archivo > Nuevo > Consulta DAX**).
2. Escriba o pegue la consulta DAX. Por lo general, debería tratarse de una consulta formada por una llamada `SUMMARIZECOLUMNS` con una o más medidas (explícitas), como la generada por los elementos visuales en Power BI.

> [!TIP]
> Puede usar el [Analizador de rendimiento](https://docs.microsoft.com/power-bi/create-reports/desktop-performance-analyzer) en Power BI Desktop para capturar la consulta generada por los elementos visuales.

3. Pulse F5 para ejecutar la consulta en Tabular Editor 3. Localice el valor que desea depurar, haga clic con el botón derecho en la celda y elija **Depurar**.

![Depurar desde una consulta](~/content/assets/images/features/debug-from-query.png)

# Vistas de depuración

El depurador ofrece las siguientes vistas (si están ocultas, se puede acceder a ellas a través del menú **Depurar > Ventanas**).

- Variables locales
- Vigilancia
- Contexto de evaluación
- Árbol de llamadas

## Variables locales
Esta vista enumera las columnas, las medidas y las variables dentro del ámbito de ejecución actual y muestra sus valores. También muestra el valor de la subexpresión actual que se está depurando. Los valores de esta lista se actualizan automáticamente al pasar a una subexpresión diferente o cuando se cambia el contexto de evaluación. **Los valores locales siempre se evalúan en el elemento seleccionado actualmente del árbol de llamadas**.

![Locales](~/content/assets/images/locals.png)

Puede inspeccionar un valor local haciendo clic en el botón de la lupa dentro de la columna **Valor**. Esto abrirá un cuadro de diálogo emergente que mostrará el valor con más detalles. Esto resulta especialmente útil si el valor inspeccionado es una tabla.

![Inspeccionar el valor de las variables locales](~/content/assets/images/inspect-locals.png)

Si prefiere inspeccionar el valor de las variables locales en una ventana de consulta DAX separada, puede desactivar la opción **Usar inspector emergente** en **Herramientas > Preferencias > Depurador de DAX > Variables locales**.

![Ajustes del depurador de Dax](~/content/assets/images/features/dax-debugger-settings.png)

## Vigilancia
Esta vista le permite introducir cualquier expresión DAX, que se calculará dentro del contexto de evaluación actual. Puede introducir expresiones escalares y de tabla, así como usar todas las funciones DAX disponibles y hacer referencia a variables dentro del ámbito de evaluación actual. Los valores de observación se actualizan automáticamente al pasar a una subexpresión diferente o cuando se cambia el contexto de evaluación. **Los valores de Observación siempre se evalúan en el ámbito del elemento seleccionado actualmente en la pila del contexto de evaluación**.

![Observar](~/content/assets/images/watch.png)

Para añadir rápidamente una variable, una medida o una subexpresión a la vista «Observar», simplemente resalte una parte del código y arrástrela a la vista «Observar». También puede colocar el cursor sobre la expresión que desea añadir, luego hacer clic derecho y elegir **Vigilar esta expresión**:

![Agregar rápidamente a Observar](~/content/assets/images/quick-add-to-watch.png)

Para añadir, duplicar o eliminar expresiones de vigilancia, use el menú contextual que aparece al hacer clic con el botón derecho en la vista de vigilancia:

![Menú contextual de Observar](~/content/assets/images/watch-context-menu.png)

La opción **Generar consulta** es idéntica al botón de la lupa de la columna **Valor**, resaltado en la captura de pantalla siguiente. Al hacer clic en esta opción, el depurador abrirá un nuevo documento de consulta DAX, que define el contexto del cálculo, así como el cálculo en sí, lo que le permite inspeccionar los resultados con más detalle. Esto resulta especialmente útil cuando la expresión de inspección es una expresión de tabla, como se muestra a continuación:

![Inspeccionar Variables de seguimiento](~/content/assets/images/inspect-watch.png)

> [!TIP]
> ¿Cuál es la diferencia entre la vista **Locales** y la vista **Observar**?
> - **Locales** muestra los valores de las columnas, las medidas, las variables y otras subexpresiones relevantes, dentro del ámbito de ejecución actual, incluido el valor de la subexpresión seleccionada actualmente en el árbol de llamadas.
> - **Observar** le permite introducir cualquier expresión DAX, que se calculará dentro del contexto de evaluación actual.

## Contexto de evaluación
Esta vista proporciona información sobre el contexto de evaluación DAX de la subexpresión actual. Por ejemplo, una expresión `CALCULATE` podría realizar una transición de contexto o añadir un filtro al contexto de evaluación, o un iterador `SUMX` podría añadir un contexto de fila.

![Contexto de evaluación](~/content/assets/images/evaluation-context.png)

Puede hacer doble clic en un elemento de la pila del contexto de evaluación para centrar la atención en ese elemento. Esto hará que todas las expresiones **Vigilar** se vuelvan a evaluar en el nuevo contexto (es decir, todos los contextos desde la parte inferior de la pila hasta el elemento en el que se encuentra el foco actualmente, incluido este). Esto se ilustra en la animación a continuación. Observe también cómo puede inspeccionar el valor de columnas individuales en el contexto de fila activo desplazándose por las filas dentro de cualquier iteración activa:

![Árbol de llamadas](~/content/assets/images/navigating-evaluation-context.gif)

También puedes activar o desactivar filtros individuales desde el contexto de filtro externo (por ejemplo, agrupar columnas en la llamada [`SUMMARIZECOLUMNS`](https://dax.guide/summarizecolumns) que generó la consulta o los filtros especificados en un Pivot Grid). Esto se ilustra en la animación a continuación. Los filtros activados de esta manera se aplicarán tanto a «Observar» como a «Locales».

![Árbol de llamadas](~/content/assets/images/toggle-filters.gif)

Por último, puede examinar las primeras 1000 filas de cualquier iterador, estableciendo el contexto de fila actual en una fila específica dentro de esas primeras 1000, haciendo clic en el botón Zoom de la columna **Fila**.

![Explorar contextos de fila](~/content/assets/images/browse-row-contexts.png)

## Árbol de llamadas
Esta vista ofrece un esquema de todo el cálculo y le permite navegar fácilmente entre subexpresiones haciendo doble clic (también puede usar teclas de acceso directo para navegar). El árbol también proporciona información sobre las transiciones de contexto, las iteraciones y los contextos de fila. Las ramas de código que no se ejecutarán (por ejemplo, en una llamada `IF` o `SWITCH`, o cuando un iterador está vacío) aparecen tachadas.

![Árbol de llamadas](~/content/assets/images/call-tree.png)

A medida que navega entre los elementos del árbol de llamadas, el script DAX de depuración resaltará el código correspondiente al elemento del árbol de llamadas, al tiempo que indicará (con un fondo gris) la ruta seguida para llegar al código resaltado, como se muestra a continuación:

![Árbol de llamadas](~/content/assets/images/navigating-call-tree.gif)

Observe cómo se actualizan los valores de la vista **Locales** a medida que se navega por el árbol. También puede navegar hasta una subexpresión colocando el cursor sobre la expresión, haciendo clic derecho y eligiendo la opción **Entrar en selección** (Ctrl+B).

![Entrar en selección](~/content/assets/images/debugger-step-into-selection.png)

## Predicados escalares

Los predicados escalares utilizados en los argumentos de filtro de las funciones [`CALCULATE`](https://dax.guide/calculate) o [`CALCULATETABLE`](https://dax.guide/calculatetable) se tratan de una forma especial, en la vista **Locales**.

Por ejemplo, la siguiente medida usa un predicado escalar para mostrar solo las ventas realizadas en EE. UU. o Canadá.

```dax
CALCULATE(
    [Total Sales],
    Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
)
```

A primera vista, parece que la expresión de la línea 3 devolvería un valor escalar (verdadero/falso). Sin embargo, en DAX, los filtros son tablas. En realidad, el predicado escalar se convierte en una expresión de tabla mediante la función [`FILTER`](https://dax.guide/filter), como se muestra a continuación:

```dax
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(Geography[Country Region Code]),
        Geography[Country Region Code] = "US" || Geography[Country Region Code] = "CA"
    )
)
```

La función `FILTER` es un iterador que recorre la tabla `ALL(Geography[Country Region Code])`, es decir, todos los valores únicos de la columna «Country Region Code» de la tabla «Geography». Los iteradores generan un contexto de filtro para cada fila de la iteración. A continuación, el predicado escalar se evalúa en cada uno de esos contextos de fila. En el caso de la función `FILTER`, solo se conservan las filas para las cuales el predicado se evalúa como `TRUE`. En este ejemplo, la función `FILTER` devolvería una tabla con 1 columna («Country Region Code») y 2 filas («US» y «CA»).

Al depurar un predicado escalar, la vista **Locales** mostrará dos elementos especiales, **(Expresión actual)** y **(Expresión de filtro)**. A continuación, se describen:

![Depurar predicados escalares](~/content/assets/images/features/debug-scalar-predicates.png)

En la captura de pantalla anterior:

1. Este es el predicado escalar que se está depurando actualmente. Aunque esta subexpresión parece una que debería devolver un valor escalar (verdadero/falso), en realidad devuelve una tabla.
2. **(Expresión actual)**: Este es el valor *escalar* del predicado, cuando se evalúa dentro del *contexto de fila* actual generado por la función `FILTER` como se ha descrito anteriormente. En la captura de pantalla, el valor escalar se evalúa como «False», porque el valor de [Country Region Code] en el contexto de fila actual es «AU», como se puede ver en la vista **Watch** (4). Podemos usar la vista **Contexto de evaluación** (5) para desplazarnos por las filas de la iteración una a una.
3. **(Expresión de filtro)**: Esta es la expresión de *tabla* generada por la función `FILTER`, como se ha descrito anteriormente. En la captura de pantalla, se trata de una tabla de 1 x 2 que contiene los valores «US» y «CA». Al hacer clic en el botón de la lupa, se abrirá una ventana emergente que muestra los valores de la tabla en una cuadrícula.
4. Podemos usar la ventana **Observar** para evaluar cualquier expresión DAX dentro del contexto de evaluación actual. En este caso, como tenemos un contexto de fila activo, podemos hacer referencia directamente a las columnas del contexto de fila, como `Geography[Country Region Code]`. Podemos ver que el valor actual de esta columna es «AU», por lo que el predicado escalar (2) se evalúa como «False».
5. Podemos usar la vista **Contexto de evaluación** para desplazarnos por las filas de la iteración, una por una. Esto actualizará los valores en la vista **Locales**, así como en la vista **Observar**, para reflejar los valores en el contexto de fila actual.

## Accesos directos de teclado

Use los siguientes atajos de teclado para navegar rápidamente por el árbol de llamadas:

- **Entrar en (F11)**: entra en el primer elemento secundario del elemento actual en el árbol de llamadas. Si no hay más elementos secundarios, salta al siguiente elemento del mismo nivel.
- **Salir de (Mayús+F11)**: sale al elemento primario del elemento actual en el árbol de llamadas.
- **Pasar por encima (F10)**: salta al siguiente parámetro de la función, a la siguiente subexpresión de una operación aritmética o entra en la llamada a la función actual (si se trata de una función no trivial).
- **Paso atrás (Mayús-F10)**: salta al parámetro de función anterior, a la subexpresión anterior de una operación aritmética o sale al elemento principal del elemento actual si no hay parámetros ni subexpresiones antes del elemento actual.
- **Entrar en selección (Ctrl+B)**: salta a la expresión situada bajo el cursor. Si varias rutas conducen a la misma expresión (por ejemplo, cuando varias medidas hacen referencia a una medida y a estas medidas), aparecerá un cuadro de diálogo para que elija la ruta.
- **Siguiente fila (F9)**: desplaza el contexto de fila de la iteración más interna a la siguiente fila del iterador.
- **Fila anterior (Mayús-F9)**: desplaza el contexto de fila de la iteración más interna a la fila anterior del iterador.

# Limitaciones y problemas conocidos

Actualmente, el depurador de DAX tiene las siguientes limitaciones:

- **UDF:** Actualmente no se admiten las funciones definidas por el usuario (UDF). Si se encuentra una UDF en el código que se está depurando, el depurador puede comportarse de forma inesperada.
- Solo se admite un subconjunto de expresiones de tabla DAX al depurar una consulta DAX (por ejemplo, se pueden depurar las consultas que dependen de [SUMMARIZECOLUMNS](https://dax.guide/summarizecolumns), mientras que otras funciones de tabla no se admiten actualmente). Por lo general, se admiten las consultas generadas por Power BI (que se pueden capturar a través del analizador de rendimiento de Power BI Desktop).
- Actualmente no se admiten consultas que contengan medidas implícitas o cálculos con ámbito de consulta.
- Al explorar las primeras 1000 filas de un iterador que surge de una expresión de tabla filtrada, es posible que la fila seleccionada en la ventana de exploración no siempre corresponda al contexto de fila actual en la pila de contextos de evaluación (escriba «CALCULATETABLE('<nombre de la tabla>')» en la ventana **Observar** para inspeccionar el contexto de fila actual).
- Actualmente, el depurador solo permite depurar expresiones DAX en medidas.
- Los [cálculos visuales](https://learn.microsoft.com/power-bi/transform-model/desktop-visual-calculations-overview) no se pueden depurar, ya que se definen mediante columnas con ámbito de consulta. El depurador no admite actualmente objetos de ámbito de consulta.
- Si un elemento de cálculo modifica una medida en el contexto de filtro, los resultados parciales que se muestran en la vista Variables/Locales del depurador pueden ser incorrectos.

Si tiene algún problema con el depurador, aparte de los mencionados anteriormente, publíquelo en nuestro [seguidor de problemas](https://github.com/TabularEditor/TabularEditor3/issues) en el sitio de GitHub de asistencia a la comunidad de TE3.

# Hoja de ruta

Tenemos previsto añadir muchas funciones adicionales al Depurador de DAX con el tiempo, para solucionar los problemas mencionados anteriormente y para que la herramienta sea aún más potente. Como siempre, los comentarios son más que bienvenidos. Utilice el [área de debates](https://github.com/TabularEditor/TabularEditor3/discussion) para solicitar funciones y participar en debates generales.

**¡Feliz depuración!**
