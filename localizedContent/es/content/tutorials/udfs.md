---
uid: udfs
title: Funciones DAX definidas por el usuario
author: Daniel Otykier
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
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

# Funciones DAX definidas por el usuario

Las funciones DAX definidas por el usuario (UDF de DAX) son una funcionalidad de los modelos semánticos. La característica pasó a versión preliminar con la actualización de septiembre de 2025 de Power BI Desktop y está [disponible de forma general](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/DAX-User-Defined-Functions-Generally-Available/ba-p/5185738) desde la versión de junio de 2026 de Power BI.

Una función DAX definida por el usuario es una función DAX reutilizable que puedes invocar en cualquier expresión DAX del modelo, incluidas otras funciones.
Para una introducción a las UDF de DAX en Tabular Editor 3, consulta la entrada del blog [Cómo empezar a usar las UDF en Tabular Editor 3](https://tabulareditor.com/blog/how-to-get-started-using-udfs-in-tabular-editor-3).

## Comprender las UDF de DAX

Una UDF de DAX tiene una lista de parámetros y una expresión DAX que calcula un resultado a partir de ellos. Los parámetros pueden ser valores escalares, tablas o referencias a objetos del modelo, y el resultado puede ser un valor escalar o una tabla.

Para obtener más información sobre cómo funcionan las UDF de DAX, consulta el artículo de SQLBI [Introducing user-defined functions in DAX](https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/).

## Requisitos previos

Las UDF de DAX requieren un modelo con nivel de compatibilidad **1702 o superior**.

## Crear tu primera UDF de DAX

### Paso 1: Configurar el modelo

Comprueba el nivel de compatibilidad del modelo:

1. Abre tu modelo en Tabular Editor 3.
2. Selecciona el nodo raíz (**Model**) en el **Explorador TOM**.
3. En la vista **Propiedades**, expande la propiedad **Database** y comprueba que el **nivel de compatibilidad** sea **1702** o superior.
4. Si es inferior, actualiza el nivel de compatibilidad y guarda el modelo.

![Establecer el nivel de compatibilidad](~/content/assets/images/tutorials/udfs-cl1702.png)

### Paso 2: Agregar una nueva función

1. En el **Explorador TOM**, busca la carpeta **Functions** dentro de tu modelo.
2. Haz clic con el botón derecho en la carpeta **Functions**.
3. Selecciona **Crear > Función definida por el usuario**.
4. Asigna un nombre a la función. Los nombres pueden contener guiones bajos y puntos, pero no espacios ni otros caracteres especiales.

![Creación de una UDF de DAX](~/content/assets/images/tutorials/new-udf.png)

**Modelo > Agregar función definida por el usuario** también agrega una UDF de DAX.

También puedes crear UDF de DAX desde la sección **DEFINE** de una **Consulta DAX** mediante **Consulta > Aplicar** (**F7**). Para aplicar solo algunas de las definiciones de la consulta, selecciónalas y pulsa **F8** (**Aplicar selección**).

![Crear una UDF de DAX desde una Consulta DAX](~/content/assets/images/tutorials/udf-from-query.png)

### Paso 3: Definir tu función

Introduce la definición de la función en el **Editor de expresiones**. Por ejemplo, esta función suma dos números:

```dax
// Adds two numbers together
(
    x, // The first number
    y  // The second number
)
=> x + y
```

> [!TIP]
> La acción de código **Use correct UDF syntax** del Editor de expresiones reescribe la expresión en una sintaxis UDF de DAX válida.

## Sintaxis y estructura de las UDF de DAX

### Sintaxis básica

Una definición de UDF de DAX tiene esta estructura:

```dax
FUNCTION FunctionName =
    // Optional comment describing the function
    (
        parameter1, // Parameter description
        parameter2, // Parameter description
        // ... more parameters
    )
    => expression_using_parameters
```

### Modo de evaluación de parámetros

Cada parámetro se pasa **por valor** o **por referencia** y, a menos que especifiques lo contrario, se pasa por valor.

Un parámetro pasado por valor se comporta como una variable DAX definida con `VAR`: el argumento se evalúa una vez cuando se llama a la función, y cada referencia al parámetro dentro de la función devuelve ese valor.

Un parámetro pasado por referencia se comporta como una medida: cada referencia al parámetro dentro de la función se evalúa en el contexto de evaluación en el que aparece.

Establece el modo con dos puntos (`:`) después del nombre del parámetro, seguido de `VAL` (por valor) o `EXPR` (por referencia). Si lo omites, el parámetro es `VAL`:

```dax
(
    x: VAL,   // Pass-by-value parameter - the DAX expression is evaluated once when the function is called, and the result is "copied" into the function
    y: EXPR   // Pass-by-reference parameter - can be any DAX expression which will observe whatever context the parameter is later referenced under
)
=>
ROW(
    "x", x,
    "x modified", CALCULATE(x, Product[Color] = "Red"),
    "y", y, 
    "y modified", CALCULATE(y, Product[Color] = "Red")
)
```

Si llamas a esta función con la misma referencia de medida para ambos parámetros, por ejemplo `MyFunction([Some Measure], [Some Measure])`, solo los resultados de `y` cambian según el contexto de filtro:

![Paso por valor vs paso por referencia](~/content/assets/images/tutorials/udf-pass-by-ref.png)

Para restringir el tipo del parámetro, que es opcional, escribe un tipo de datos antes del modo de evaluación, por ejemplo `x: INT64 VAL` o `y: TABLE EXPR`. Si se especifica un tipo, los argumentos se convierten implícitamente a ese tipo, y Tabular Editor 3 usa ese tipo en las sugerencias de autocompletado para el código que llama a la función.

Tabular Editor 3 valida los argumentos según los tipos de parámetro declarados. Si llamas a una UDF de DAX con un argumento que no coincide con el tipo de su parámetro, como un valor escalar donde se espera un parámetro `TABLEREF`, el Analizador semántico informa de una advertencia o un error.

Para consultar la lista completa de restricciones, consulta la [especificación de Microsoft para las UDF de DAX](https://learn.microsoft.com/dax/best-practices/dax-user-defined-functions).

### Parámetros opcionales con expresiones predeterminadas

Tabular Editor 3.26.2 y las versiones posteriores admiten parámetros opcionales con expresiones predeterminadas. Para hacer que un parámetro sea opcional, agrega `= expression` después del nombre del parámetro y de cualquier indicación de tipo o de modo de evaluación. Si el llamador omite el argumento, la expresión predeterminada proporciona el valor.

```dax
FUNCTION AddTax =
    (
        amount: NUMERIC,        // Required parameter
        taxRate: NUMERIC = 0.1  // Optional parameter, defaults to 10%
    )
    => amount * (1 + taxRate)
```

Si llamas a `AddTax(10)`, obtienes `11`, mientras que si llamas a `AddTax(10, 0.25)`, obtienes `12.5`.

Los parámetros opcionales siguen estas reglas:

- Puedes dejar vacío un argumento para usar su valor predeterminado; por ejemplo, `MyFunc(1,,3)` omite el segundo argumento. El número mínimo de argumentos lo determina la posición del parámetro obligatorio situado más a la derecha.
- Una expresión predeterminada solo puede hacer referencia a nombres (columnas, tablas, medidas, funciones) visibles donde se define la función, y no puede hacer referencia a otro parámetro de la misma función.
- La comprobación de tipos con respecto a la indicación de tipo de un parámetro solo se aplica cuando se usa la expresión predeterminada; en cambio, un argumento pasado explícitamente se comprueba con respecto a esa indicación.

## Uso de las UDF de DAX en tu modelo

### En expresiones de objetos

Puedes llamar a una UDF de DAX desde cualquier expresión DAX del modelo, y el autocompletado sugiere las UDF de DAX mientras escribes.

### En Scripts DAX

Los scripts DAX pueden definir y llamar a las UDF de DAX:

```dax
-- Function: MyFuncRenamed
FUNCTION MyFuncRenamed =
    // Adds two numbers together
    (
        x: INT64, // The first number
        y: INT64  // The second number
    )
    => x + y

-- Measure: [New Measure]
MEASURE 'Date'[New Measure] = MyFuncRenamed(1,2)
```

### En Consultas DAX

Además de aplicar al modelo una UDF de DAX desde la sección **DEFINE** de una consulta, puedes hacer clic con el botón derecho en una llamada a una función en una consulta DAX y elegir **Define Function** para agregar la definición de la función a la sección **DEFINE**:

![Define Function desde la consulta](~/content/assets/images/tutorials/udf-define.png)

El menú contextual de una llamada a una UDF de DAX tiene estos comandos:

- **Ver la definición** (**Alt+F12**): abre un editor de solo lectura con la definición de la función debajo del cursor.
- **Ir a definición** (**F12**): va a la definición de la función en el editor si la consulta o el script actuales la definen; en caso contrario, va a la función en la carpeta **Functions**.
- **Función insertada**: reemplaza la llamada por el cuerpo de la función, con los parámetros sustituidos por los argumentos.
- **Define Function** (solo en scripts DAX y consultas DAX): agrega la definición de la función a la sección **DEFINE** si aún no está allí.
- **Define Function with dependencies** (solo para scripts DAX y Consultas DAX): también agrega las definiciones de las UDF de DAX a las que llama la función.

## Administrador de paquetes DAX

El [DAX Package Manager](xref:dax-package-manager), disponible en Tabular Editor 3.24.0 y versiones posteriores, busca, instala y administra bibliotecas de UDF de DAX y admite el feed de [DaxLib](https://daxlib.org).

Los administradores del sistema pueden desactivar el acceso al Administrador de paquetes DAX especificando una [directiva de grupo](xref:policies).

## Características avanzadas

### Corrección automática de fórmulas

Cuando cambias el nombre de una UDF de DAX, Tabular Editor 3 actualiza todas las referencias a ella en el modelo, igual que hace con las medidas y otros objetos.

### Ver la definición

**Ver la definición** muestra la definición de una UDF de DAX debajo del cursor sin salir del documento actual.

![Ver la definición para las UDF de DAX](~/content/assets/images/tutorials/udf-peek-definition.png)

### Vista de dependencias

La vista **Dependencias de DAX** (**Shift+F12**) muestra, para una UDF de DAX, lo siguiente:

- **Objetos que dependen de la función**: las medidas, columnas y otros objetos que llaman a la función
- **Objetos de los que depende la función**: las medidas, columnas y otros objetos a los que hace referencia la función

### Cambio de nombre por lotes

La opción **Cambio de nombre por lotes** (**F2**) del menú contextual del Explorador TOM permite cambiar el nombre de varias UDF de DAX seleccionadas a la vez, con patrones de búsqueda y reemplazo y expresiones regulares opcionales.

### Espacios de nombres

En DAX no hay espacios de nombres, así que asigna a las UDF de DAX nombres inequívocos que indiquen de dónde procede la función, usando `.` como separador de espacios de nombres; por ejemplo, `DaxLib.Convert.CelsiusToFahrenheit`. El Explorador TOM muestra en una jerarquía las UDF de DAX con nombres de este tipo. Para activar o desactivar la jerarquía, usa **Agrupar funciones definidas por el usuario por espacio de nombres** en la barra de herramientas situada sobre el Explorador TOM. El botón aparece solo en modelos con nivel de compatibilidad 1702 o superior.

![UDFs de DAX agrupadas por espacio de nombres](~/content/assets/images/udf-namespaces-tom-explorer.png)

Cada UDF de DAX también tiene una propiedad `Namespace` que establece su posición en la jerarquía del Explorador TOM sin cambiar su nombre, de forma similar a las carpetas de visualización de las medidas. Por ejemplo, si usas el cambio de nombre por lotes para quitar el espacio de nombres de sus nombres, establece `Namespace` para mantenerlas agrupadas en el Explorador TOM.

> [!NOTE]
> La propiedad `Namespace` no afecta al código DAX, así que, para llamar a una UDF de DAX, usa su nombre completo, incluidas todas las partes del espacio de nombres.

## Las UDF de DAX y el control de código fuente

Si almacenas el modelo como una estructura de carpetas, Tabular Editor puede escribir cada UDF de DAX en su propio archivo. Sin este nivel de serialización, todas las funciones se almacenan en `Database.json`, y las ediciones en paralelo de distintas funciones pueden entrar en conflicto en ese archivo.

Selecciona el nivel **Funciones definidas por el usuario (UDFs)** en **Modelo > opciones de serialización...**. Si vas a guardar un modelo en una carpeta por primera vez, selecciona esta opción en **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta** (consulta [Guardar en carpeta](xref:save-to-folder#user-defined-functions-udfs)).

## Buenas prácticas

### Convenciones de nomenclatura

- usa nombres que describan el propósito de la función
- antepone a las UDF de DAX las iniciales de tu organización, por ejemplo `ACME.CalculateDiscount`
- usa nombres compuestos con un carácter separador (`.` o `_`), por ejemplo `Finance.CalcProfit` o `My_CalcProfit`. Un nombre compuesto no puede entrar en conflicto con una función DAX integrada que Microsoft agregue más adelante. Consulta la [regla BPA integrada](xref:kb.bpa-udf-use-compound-names)

### Documentación

- añade un comentario que describa lo que hace la función
- documenta el propósito de cada parámetro y el tipo de datos esperado
- incluye ejemplos de uso en los comentarios

```dax
// Calculates the percentage change between two values
// Usage: PercentChange(100, 110) returns 0.10 (10% increase)
(
    oldValue: DOUBLE,    // The original value
    newValue: DOUBLE     // The new value to compare against
)
=> DIVIDE(newValue - oldValue, oldValue)
```

Tabular Editor 3 muestra estos comentarios en las sugerencias de autocompletado y en la información sobre herramientas.

![Autocompletado de UDFs de DAX con comentarios](~/content/assets/images/tutorials/udf-comment-tooltips.png)

## Casos de uso habituales

### Operaciones matemáticas

```dax
// Calculate compound interest
(
    principal: DOUBLE,
    rate: DOUBLE,
    periods: INT64
)
=> principal * POWER(1 + rate, periods)
```

### Manipulación de cadenas

```dax
// Format a full name from first and last name components
(
    firstName: STRING,
    lastName: STRING
)
=> TRIM(firstName) & " " & TRIM(lastName)
```

### Cálculos de fechas

```dax
// Get the fiscal year based on a date (fiscal year starts July 1)
(
    inputDate: DATETIME
)
=> IF(MONTH(inputDate) >= 7, YEAR(inputDate) + 1, YEAR(inputDate))
```

### Lógica de negocio

```dax
// Apply tiered discount based on quantity
(
    quantity: INT64
)
=> SWITCH(
    TRUE(),
    quantity >= 100, 0.15,
    quantity >= 50,  0.10,
    quantity >= 25,  0.05,
    0
)
```

## Solución de problemas

### Problemas frecuentes

**La función no aparece en el autocompletado**

Comprueba lo siguiente, en este orden:

1. Si la definición de la función tiene un error semántico, como la falta de un contexto de fila o un `MATCHBY` no válido, el autocompletado oculta la función, pero sigue mostrando su calltip. Corrige el error en la función.
2. El autocompletado solo ofrece una UDF de DAX cuando su tipo de valor devuelto encaja con el argumento que estás completando. El tipo de valor devuelto se infiere a partir del cuerpo de la función: una función que devuelve una tabla no se ofrece donde se espera un escalar, ni viceversa. Excepciones:
   - los argumentos de filtro, como el segundo y los argumentos posteriores de [`CALCULATE`](https://dax.guide/calculate), aceptan cualquiera de los dos
   - una función cuyo cuerpo es un parámetro `EXPR` sin tipo se ofrece en todas partes
3. Las UDF de DAX para cálculos Visual solo aparecen en los cálculos Visual, mientras que las demás UDF de DAX solo aparecen fuera de ellos.
4. No se ofrece una función dentro de su propia definición.

**Errores de restricción de parámetros**

- revisa los tipos de parámetros que has especificado
- comprueba que los argumentos coinciden con los tipos de parámetros
- consulta la documentación de Microsoft para ver los tipos de restricción admitidos

**La función no funciona tras el despliegue**

- comprueba que el destino admite las UDF de DAX; el Power BI Service las admite a partir de la versión de junio de 2026 (consulta [Limitaciones](#limitations)).

## Limitaciones

- Las UDF de DAX requieren el nivel de compatibilidad 1702 o superior. Azure Analysis Services y SQL Server Analysis Services no admiten las UDF de DAX.
- Las UDF de DAX no pueden ser recursivas (llamarse a sí mismas).

> [!NOTE]
> Los parámetros opcionales con expresiones predeterminadas se incorporaron con la [disponibilidad general](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/DAX-User-Defined-Functions-Generally-Available/ba-p/5185738) de las UDF de DAX en junio de 2026. Las versiones de Tabular Editor 3 anteriores a la 3.26.2 muestran un error falso en la sintaxis de la expresión predeterminada.
