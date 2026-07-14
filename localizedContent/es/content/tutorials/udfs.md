---
uid: udfs
title: Funciones DAX definidas por el usuario
author: Daniel Otykier
updated: 2026-06-24
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

Las UDF de DAX (funciones DAX definidas por el usuario) son una característica de los modelos semánticos. La característica pasó a versión preliminar con la actualización de septiembre de 2025 de Power BI Desktop y está [disponible de forma general](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/DAX-User-Defined-Functions-Generally-Available/ba-p/5185738) desde la versión de junio de 2026 de Power BI.

La característica te permite crear funciones DAX reutilizables que puedes invocar desde cualquier expresión DAX de tu modelo, incluso desde otras funciones. Esta potente característica te ayuda a mantener la coherencia, reducir la duplicación de código y crear expresiones DAX más fáciles de mantener.

Tabular Editor 3 es compatible con las UDFs a partir de la versión 3.23.0, aunque recomendamos usar [3.23.1](xref:release-3-23-1) (o una versión posterior) para aprovechar diversas correcciones de errores y mejoras.

Para una introducción más detallada a las UDFs en Tabular Editor 3, consulta [esta entrada del blog](https://tabulareditor.com/blog/how-to-get-started-using-udfs-in-tabular-editor-3).

## Comprender las UDFs

Las UDFs pueden entenderse como funciones DAX personalizadas que defines una vez y puedes usar en todo tu modelo. Defines qué parámetros acepta la función, que pueden ser valores escalares o de tipo tabla, o incluso referencias a objetos, y luego proporcionas la expresión DAX que usa esos parámetros para calcular un resultado, que también puede ser escalar o de tipo tabla.

Para obtener más información sobre cómo funcionan las UDF de DAX, recomendamos [este artículo de SQLBI](https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/).

## Requisitos previos

Antes de poder crear y usar UDFs en Tabular Editor 3, asegúrate de que:

- El nivel de compatibilidad de tu modelo es **1702 o superior**

## Crear tu primera UDF

### Paso 1: Configurar el modelo

Primero, comprueba que el nivel de compatibilidad del modelo sea el adecuado para las UDF:

1. Abre tu modelo en Tabular Editor 3
2. Selecciona el nodo raíz ("Model") en el **Explorador TOM**
3. En el panel **Propiedades**, expande la propiedad **Database** y, a continuación, comprueba que el **nivel de compatibilidad** esté establecido en **1702** o superior
4. Si es necesario, actualiza el nivel de compatibilidad y guarda tu modelo

![Establecer el nivel de compatibilidad](~/content/assets/images/tutorials/udfs-cl1702.png)

### Paso 2: Agregar una nueva función

1. En el **Explorador TOM**, busca la carpeta **Functions** dentro de tu modelo
2. Haz clic con el botón derecho en la carpeta **Functions**
3. Selecciona **Create > User-Defined Function**
4. Asigna a tu función un nombre descriptivo (no se permiten espacios ni caracteres especiales; se admiten guiones bajos y puntos)

![Creación de una UDF](~/content/assets/images/tutorials/new-udf.png)

También puedes agregar una UDF desde la opción de menú **Model > Add User-Defined Function**.

Como alternativa, puedes crear UDFs directamente desde la sección **DEFINE** de una Consulta DAX, pulsando F7 (Aplicar) o usando la opción del menú **Query > Apply**. Si tu consulta contiene varias definiciones con ámbito de consulta, también puedes seleccionar solo un subconjunto y pulsar F8 (Aplicar selección).

![Crear una UDF desde una Consulta DAX](~/content/assets/images/tutorials/udf-from-query.png)

### Paso 3: Definir tu función

En el **Editor de expresiones**, define tu función usando la sintaxis correcta de las UDF.

Aquí tienes un ejemplo básico que suma dos números:

```dax
// Suma dos números
(
    x, // El primer número
    y  // El segundo número
)
=> x + y
```

> [!TIP]
> Usa la acción de código **"Use correct UDF syntax"** en el Editor de expresiones si necesitas ayuda con la estructura de sintaxis correcta.

## Sintaxis y estructura de UDF

### Sintaxis básica

Las UDFs siguen esta estructura general:

```dax
FUNCTION FunctionName =
    // Comentario opcional que describe la función
    (
        parameter1, // Descripción del parámetro
        parameter2, // Descripción del parámetro
        // ... más parámetros
    )
    => expression_using_parameters
```

### Modo de evaluación de parámetros

Un aspecto clave de las UDF es que los parámetros pueden definirse en uno de dos modos: **paso por valor** y **paso por referencia**. De forma predeterminada, y a menos que especifiques lo contrario, un parámetro se pasará **por valor**. En la práctica, esto significa que el parámetro se comporta igual que una variable de DAX (es decir, definida mediante la palabra clave `VAR`) dentro de la expresión de la UDF. En otras palabras, cuando se invoca la UDF, los valores de los parámetros se «copian» en la función y cualquier referencia a ese parámetro dentro de la función devolverá siempre el mismo valor.

En cambio, los parámetros de **paso por referencia** se comportan más como las medidas. Es decir, el resultado de evaluar el parámetro _dentro de la función_ puede variar según el contexto de evaluación.

Para especificar el modo de evaluación, incluye una especificación del parámetro después del nombre del parámetro, separada por dos puntos (`:`). La especificación puede ser `VAL` o `EXPR` para «paso por valor» y «paso por referencia», respectivamente. Como se mencionó anteriormente, «paso por valor» es el modo predeterminado, por lo que `VAL` se entiende implícitamente si no se especifica. Por ejemplo:

```dax
(
    x: VAL,   // Parámetro por valor: la expresión DAX se evalúa una vez cuando se llama a la función y el resultado se «copia» en la función
    y: EXPR   // Parámetro por referencia: puede ser cualquier expresión DAX que tenga en cuenta el contexto en el que luego se haga referencia al parámetro
)
=>
ROW(
    "x", x,
    "x modified", CALCULATE(x, Product[Color] = "Red"),
    "y", y, 
    "y modified", CALCULATE(y, Product[Color] = "Red")
)
```

Si llamas a la función anterior con una referencia a una medida para cada parámetro, por ejemplo `MyFunction([Some Measure], [Some Measure])`, obtendrás resultados diferentes para el parámetro `y` según el contexto de filtro actual, como se muestra en la captura de pantalla siguiente:

![Paso por valor vs paso por referencia](~/content/assets/images/tutorials/udf-pass-by-ref.png)

Además de especificar el modo de evaluación, también puedes restringir el tipo de parámetro indicando un tipo de datos antes del modo de evaluación; por ejemplo, `x: INT64 VAL` o `y: TABLE EXPR`.

Estas especificaciones de tipo son opcionales, pero si se indican, realizarán una conversión de tipo implícita en los argumentos que se pasen a la función y también afectarán a las sugerencias de autocompletado en Tabular Editor 3 al escribir código DAX que llame a la función.

Tabular Editor 3 valida los argumentos según los tipos de parámetro declarados. Si llama a una UDF con un argumento que no coincide con el tipo de su parámetro —por ejemplo, si pasa un valor escalar cuando se espera un parámetro `TABLEREF`—, el Analizador semántico genera un Report de advertencia o un error.

Consulta la [especificación de Microsoft para las UDF](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions) para ver la lista completa de restricciones disponibles.

### Parámetros opcionales con expresiones predeterminadas

A partir de la versión 3.26.2, Tabular Editor 3 admite parámetros opcionales con expresiones predeterminadas. Añade `= expression` después del nombre del parámetro (y después de cualquier indicación de tipo o modo de evaluación) para que el parámetro sea opcional. Cuando quien llama omite el argumento, la expresión predeterminada proporciona el valor.

```dax
FUNCTION AddTax =
    (
        amount: NUMERIC,        // Parámetro obligatorio
        taxRate: NUMERIC = 0.1  // Parámetro opcional; el valor predeterminado es 10 %
    )
    => amount * (1 + taxRate)
```

Si llamas a `AddTax(10)`, obtienes `11`, mientras que si llamas a `AddTax(10, 0.25)`, obtienes `12.5`.

Los parámetros opcionales se rigen por algunas reglas:

- Puedes dejar vacío un argumento para usar su valor predeterminado; por ejemplo, `MyFunc(1,,3)` omite el segundo argumento. El número mínimo de argumentos lo determina la posición del parámetro obligatorio situado más a la derecha.
- Una expresión predeterminada solo puede hacer referencia a nombres (columnas, tablas, medidas, funciones) visibles donde se define la función, y no puede hacer referencia a otro parámetro de la misma función.
- La comprobación de tipos con respecto a la indicación de tipo de un parámetro solo se aplica cuando se usa la expresión predeterminada; en cambio, un argumento pasado explícitamente se comprueba con respecto a esa indicación.

## Uso de las UDF en tu modelo

### En expresiones de objetos

Una vez que hayas creado una UDF, puedes usarla en cualquier expresión DAX de tu modelo. El autocompletado de Tabular Editor 3 te sugerirá tus UDF a medida que escribes.

### En Scripts DAX

Las UDF también están disponibles al trabajar con Scripts DAX:

```dax
-- Función: MyFuncRenamed
FUNCTION MyFuncRenamed =
    // Suma dos números
    (
        x: INT64, // El primer número
        y: INT64  // El segundo número
    )
    => x + y

-- Medida: [New Measure]
MEASURE 'Date'[New Measure] = MyFuncRenamed(1,2)
```

### En Consultas DAX

Tabular Editor 3 incorpora nuevas y potentes funciones para trabajar con UDF en Consultas DAX. Ya mencionamos antes cómo puedes "aplicar" una UDF desde la sección **DEFINE** de una Consulta DAX, para que pase a formar parte permanente de tu modelo. Además, si estás usando una UDF dentro de una Consulta DAX, puedes hacer clic con el botón derecho en la invocación de la función y elegir **Define Function** para generar automáticamente la definición de la función en la sección **DEFINE** de tu consulta:

![Define Function desde la consulta](~/content/assets/images/tutorials/udf-define.png)

Como puedes ver en la pantalla anterior, al hacer clic con el botón derecho en una invocación de UDF, están disponibles las siguientes opciones:

- **Ver la definición** (Alt+F12): Abre un editor anidado de solo lectura debajo de la posición actual del cursor, mostrándote la definición de la función
- **Ir a definición** (F12): Navega hasta la definición de la función en la carpeta **Functions** de tu modelo o, si la función está definida en la consulta o el script actual, hasta la definición de la función dentro del editor
- **función insertada**: Reemplaza la invocación de la función por la definición real de la función, sustituyendo los parámetros por los argumentos reales proporcionados a la función
- **Define Function** (solo para Scripts DAX o Consultas DAX): Genera la definición de la función en la sección **DEFINE** de tu consulta, si aún no existe allí
- **Define Function with dependencies** (solo para Scripts DAX o Consultas DAX): Similar a la anterior, pero también genera definiciones para cualquier otra UDF de la que dependa la función

## Administrador de paquetes DAX

Tabular Editor 3.24.0 incorpora una nueva función llamada **Administrador de paquetes DAX**, que te permite descubrir, instalar y administrar bibliotecas de UDF de DAX fácilmente desde Tabular Editor. De inicio, el administrador de paquetes es compatible con la popular fuente de [DaxLib](https://daxlib.org), que contiene una amplia variedad de UDF útiles para distintos escenarios.

Los administradores del sistema pueden desactivar el acceso al Administrador de paquetes DAX especificando una [directiva de grupo](xref:policies).

## Características avanzadas

### Corrección de fórmulas

Cuando cambias el nombre de una UDF, Tabular Editor 3 actualiza automáticamente todas las referencias en tu modelo, al igual que con las medidas y otros objetos.

### Ver la definición

La característica **Ver la definición** funciona con las UDF, permitiéndote ver rápidamente la implementación de la función sin salir de tu contexto actual.

![Ver la definición para las UDF](~/content/assets/images/tutorials/udf-peek-definition.png)

### Vista de dependencias

Las UDF aparecen en la vista **Dependencias de DAX** (Shift+F12), mostrando lo siguiente:

- **Objetos que dependen de la función**: Qué medidas, columnas, etc. usan la UDF
- **Objetos de los que depende la función**: A qué medidas, columnas, etc. hace referencia la UDF

### Cambio de nombre por lotes

Cuando seleccionas varias UDFs en el Explorador TOM, puedes usar la opción **Renombrar en lote** (F2) desde el menú contextual de clic derecho para cambiarles el nombre a todas de una sola vez, mediante patrones de búsqueda y sustitución y, opcionalmente, expresiones regulares.

### Espacios de nombres

El concepto de "espacio de nombres" no existe en DAX, pero se recomienda nombrar las UDFs de forma que se eviten ambigüedades y quede claro el origen de la UDF. Por ejemplo, `DaxLib.Convert.CelsiusToFahrenheit` (usando '.' como separador de espacios de nombres). Cuando una UDF se nombra así, el Explorador TOM la mostrará en una jerarquía basada en esos nombres. Puedes alternar la visualización de las UDFs por espacio de nombres mediante el botón de alternancia **Agrupar funciones definidas por el usuario por espacio de nombres** de la barra de herramientas situada encima del Explorador TOM (nota: este botón solo es visible cuando trabajas con un modelo con nivel de compatibilidad 1702 o superior).

![UDFs de DAX agrupadas por espacio de nombres](~/content/assets/images/udf-namespaces-tom-explorer.png)

En Tabular Editor, las UDFs también tienen una _propiedad_ "Namespace", que te permite personalizar el espacio de nombres de cada UDF de forma individual sin cambiar el nombre real del objeto UDF. Esto es muy similar a las carpetas de visualización de las medidas. Establecer un valor para la propiedad "Namespace" distinto del que se podría inferir a partir del nombre de la UDF resulta útil, por ejemplo, si quieres renombrar en lote (F2) varias UDFs para eliminar los espacios de nombres del nombre de cada una, pero aun así quieres mantenerlas bien organizadas en el Explorador TOM.

> [!NOTE]
> Esta característica de organización en Tabular Editor no afecta al código DAX. Aun así, cuando llames a una UDF tendrás que escribir el nombre completo, incluidas las partes del espacio de nombres.

## Buenas prácticas

### Convenciones de nomenclatura

- Usa nombres descriptivos que indiquen claramente el propósito de la función
- Considera anteponer a las UDF las iniciales de tu organización (por ejemplo, `ACME.CalculateDiscount`)
- Evita nombres genéricos que puedan entrar en conflicto con futuras funciones de DAX
- Usa nombres compuestos con un carácter separador (`.` o `_`). Por ejemplo, `Finance.CalcProfit` o `My_CalcProfit`. Esto evita que tu UDF deje de funcionar si Microsoft introduce una función DAX integrada con el mismo nombre. Consulta la [regla BPA integrada](xref:kb.bpa-udf-use-compound-names) para obtener más detalles

### Documentación

- Incluye siempre comentarios que describan lo que hace la función
- Documenta el propósito de cada parámetro y el tipo de datos esperado
- Incluye ejemplos de uso en tus comentarios

```dax
// Calcula el cambio porcentual entre dos valores
// Uso: PercentChange(100, 110) devuelve 0.10 (0,10), es decir, un aumento del 10%
(
    oldValue: DOUBLE,    // El valor original
    newValue: DOUBLE     // El nuevo valor con el que comparar
)
=> DIVIDE(newValue - oldValue, oldValue)
```

Tabular Editor 3 detecta automáticamente cualquier comentario y lo muestra correctamente en las sugerencias de autocompletado y en las descripciones emergentes.

![Autocompletado de UDFs con comentarios](~/content/assets/images/tutorials/udf-comment-tooltips.png)

## Casos de uso habituales

### Operaciones matemáticas

```dax
// CALCULATE el interés compuesto
(
    principal: DOUBLE,
    rate: DOUBLE,
    periods: INT64
)
=> principal * POWER(1 + rate, periods)
```

### Manipulación de cadenas

```dax
// Dar formato a un nombre completo a partir del nombre y el apellido
(
    firstName: STRING,
    lastName: STRING
)
=> TRIM(firstName) & " " & TRIM(lastName)
```

### Cálculos de fechas

```dax
// Obtener el año fiscal en función de una fecha (el año fiscal comienza el 1 de julio)
(
    inputDate: DATETIME
)
=> IF(MONTH(inputDate) >= 7, YEAR(inputDate) + 1, YEAR(inputDate))
```

### Lógica de negocio

```dax
// Aplicar un descuento por tramos según la cantidad: 0,15; 0,10; 0,05
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

- Comprueba que la función se haya guardado correctamente
- Comprueba que no haya errores de sintaxis en la definición de la función
- Asegúrate de que estás usando la función en un contexto compatible

**Errores de restricción de parámetros**

- Revisa los tipos de parámetros que has especificado
- Asegúrate de que estás pasando valores compatibles a la función
- Consulta la documentación de Microsoft para ver los tipos de restricción admitidos

**La función no funciona tras el despliegue**

- Comprueba que tu entorno de destino admite UDFs (nivel de compatibilidad 1702 o superior). El servicio Power BI admite las UDF a partir de la versión de junio de 2026. Azure Analysis Services y SQL Server Analysis Services no admiten las UDF.

## Limitaciones

- Las UDF requieren un nivel de compatibilidad 1702 o superior; Azure Analysis Services y SQL Server Analysis Services no las admiten
- Las UDFs no pueden ser recursivas (llamarse a sí mismas)

> [!NOTE]
> Con la [disponibilidad general](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/DAX-User-Defined-Functions-Generally-Available/ba-p/5185738) de las UDF en junio de 2026, las UDF admiten parámetros opcionales con expresiones predeterminadas. Tabular Editor 3 admite esta sintaxis desde la versión 3.26.2. Las versiones anteriores muestran un mensaje de error incorrecto cuando usas la sintaxis de expresión predeterminada.

---

Las UDFs en Tabular Editor 3 proporcionan una forma potente de crear código DAX reutilizable y fácil de mantener. Si sigues estas directrices y buenas prácticas, podrás crear una biblioteca de funciones que mejorará la coherencia de tu modelo y reducirá el tiempo de desarrollo.
