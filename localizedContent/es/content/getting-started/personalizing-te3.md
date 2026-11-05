---
uid: personalizing-te3
title: Personalizar y configurar Tabular Editor 3 para adaptarlo a sus necesidades
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

# Personalizar y configurar Tabular Editor 3 para que se adapte a sus necesidades

Tabular Editor 3 ofrece una amplia gama de opciones de configuración que le permiten adaptar la herramienta a sus necesidades específicas y a su flujo de trabajo preferido. En este artículo, te guiaremos a través de los ajustes que suelen modificar con más frecuencia los desarrolladores de modelos individuales.

A la mayoría de los ajustes tratados en este artículo se accede a través de la opción de menú **Herramientas > Preferencias**. A lo largo del artículo, enumeraremos los ajustes individuales con el siguiente estilo, para facilitar su consulta:

***Nombre del ajuste* (valor predeterminado)**<br/>Descripción del ajuste.

> [!TIP]
> Utilice el **cuadro de búsqueda** situado en la parte superior del cuadro de diálogo Preferencias para localizar rápidamente los ajustes por nombre o palabra clave. La búsqueda filtra el árbol de preferencias en tiempo real, lo que te ayuda a ir directamente al ajuste que necesitas.

# Funciones generales

La primera página que encontrará en el cuadro de diálogo **Preferencias** es la página **Tabular Editor > Funciones** (vea la captura de pantalla a continuación). A continuación, encontrará una breve descripción de las funciones de esta página y para qué se utilizan habitualmente:

![Preferencias: Funciones generales](~/content/assets/images/pref-general-features.png)

## Power BI

Estos ajustes son especialmente útiles para los desarrolladores que utilizan Tabular Editor 3 como [herramienta externa para Power BI Desktop](https://docs.microsoft.com/power-bi/transform-model/desktop-external-tools).

##### *Permitir operaciones de modelado no compatibles* (deshabilitado)

Las herramientas externas para Power BI Desktop tienen algunas [limitaciones](xref:desktop-limitations). De forma predeterminada, Tabular Editor 3 impedirá que el usuario realice cambios no admitidos en el modelo de datos. Puede haber algunas funciones avanzadas de modelado que funcionen bien, aunque no sean compatibles según el enlace anterior. Para desbloquear todos los objetos y propiedades del modelo de objetos tabulares, habilite este ajuste.

##### *Ocultar advertencias de fecha/hora automática* (deshabilitado)

Cuando el ajuste «Fecha/hora automática» de Power BI Desktop está habilitado, se crean automáticamente varias tablas calculadas. Por desgracia, estas tablas contienen código DAX que activa un mensaje de advertencia del analizador DAX integrado de Tabular Editor 3. Para ocultar estas advertencias, habilite esta configuración.

##### *Salto de línea en la primera línea de DAX* (desactivado)

En Power BI Desktop es habitual insertar un salto de línea en la primera línea de una expresión DAX, debido a la forma en que la barra de fórmulas muestra el código DAX. Si sueles pasar de Tabular Editor a Power BI Desktop y viceversa, plantéate activar esta opción para que Tabular Editor 3 inserte el salto de línea automáticamente cada vez que se edite una expresión DAX a través de la herramienta.

## Sincronización de metadatos

Estos ajustes controlan el comportamiento de Tabular Editor 3 cuando se cargan los metadatos del modelo desde una base de datos en una instancia de Analysis Services. Los ajustes especifican cómo debe gestionar Tabular Editor 3 los cambios de metadatos aplicados a la base de datos desde fuera de la aplicación, por ejemplo, cuando otro usuario realiza un cambio en la base de datos o cuando usted realiza un cambio en el modelo a través de Power BI Desktop mientras se utiliza Tabular Editor 3 como herramienta externa.

##### *Advertir cuando los metadatos locales no estén sincronizados con el modelo implementado* (habilitado)

Cuando esto está marcado, Tabular Editor muestra un mensaje de advertencia cuando intenta guardar cambios, si otro usuario o proceso ha realizado un cambio en la base de datos desde que se cargaron los metadatos del modelo en su instancia de Tabular Editor.

##### *Rastrear cambios externos del modelo* (habilitado)

Esta opción solo es relevante para las instancias locales de Analysis Services (es decir, los procesos msmdsrv.exe que se ejecutan en el mismo equipo que Tabular Editor). Cuando está marcada, Tabular Editor inicia un seguimiento en Analysis Services y le notifica si se realizan cambios externos.

##### *Actualizar metadatos del Tabular Object Model local automáticamente* (habilitado)

Cuando el mecanismo de seguimiento descrito anteriormente está habilitado, esta opción permite que Tabular Editor actualice automáticamente los metadatos del modelo cuando se detecta un cambio externo. Esto resulta útil si sueles alternar entre Power BI Desktop y Tabular Editor 3, ya que garantiza que los cambios realizados en Power BI Desktop se sincronicen automáticamente con Tabular Editor.

##### *Limpiar rastros huérfanos de Tabular Editor*

Normalmente, Tabular Editor 3 debería detener y eliminar automáticamente cualquier seguimiento de AS iniciado debido a los ajustes anteriores. Sin embargo, si la aplicación se cerró prematuramente, es posible que los rastros nunca se detengan. Al hacer clic en este botón, se eliminarán todos los rastros de AS iniciados por cualquier instancia de Tabular Editor en la instancia actual de Analysis Services.

> [!NOTE]
> El botón de limpieza solo está disponible cuando Tabular Editor está conectado a una instancia de Analysis Services.

# Configuración del Explorador TOM

Los siguientes ajustes controlan varios aspectos del Explorador TOM. Puede encontrar estos ajustes en **Tabular Editor > Explorador TOM**:

![Ajustes del Explorador TOM](~/content/assets/images/unsaved-changes/preferences.png)

##### *Mostrar rama completa* (desactivada)

Al filtrar el Explorador TOM, Tabular Editor 3 muestra de forma predeterminada todos los elementos de la jerarquía que coinciden con la cadena de filtro, incluidos sus elementos principales. Si también desea ver todos los elementos secundarios (aunque estos no coincidan con la cadena de filtro), habilite esta opción.

##### *Mostrar siempre advertencias de eliminación* (desactivado)

Si prefiere que Tabular Editor 3 le solicite confirmar todas las eliminaciones de objetos, habilite este ajuste. De lo contrario, Tabular Editor 3 solo le solicitará que confirme las eliminaciones de varios objetos o las eliminaciones de objetos a los que hacen referencia otros objetos.

> [!NOTE]
> Todas las operaciones de eliminación en Tabular Editor 3 se pueden deshacer pulsando CTRL+Z.

# Configuración general del editor de DAX

El editor DAX de Tabular Editor 3 es altamente configurable, y es fácil sentirse abrumado por los numerosos ajustes disponibles. En esta sección se destacan los ajustes más comunes e importantes. Localice la configuración general en **Editores de texto > Editor de DAX > General**:

![Configuración general del editor DAX](~/content/assets/images/dax-editor-general.png)

## General

Los ajustes *Números de línea*, *Plegado de código*, *Espacios en blanco visibles* y *Guías de sangría* se pueden usar para activar o desactivar varias funciones visuales del editor. En la captura de pantalla siguiente, se han habilitado las cuatro opciones:

![Espacios en blanco visibles](~/content/assets/images/visible-whitespace.png)

##### *Usar tabulaciones* (desactivado)

Cuando esto está marcado, se inserta un carácter de tabulación (`\t`) cada vez que se pulsa la tecla TAB. De lo contrario, se inserta un número de espacios correspondiente al ajuste *Ancho de sangría*.

##### *Estilo de comentario* (barras diagonales)

DAX admite comentarios de línea que usan barras diagonales (`//`) o guiones (`--`). Este ajuste determina qué estilo de comentario se utiliza cuando Tabular Editor 3 genera código DAX, como cuando se utiliza la función de script DAX.

## Configuración de DAX

Estos ajustes determinan ciertos comportamientos del analizador de código DAX. El ajuste *Configuración regional* es simplemente una cuestión de preferencia. Todos los demás ajustes solo son relevantes cuando Tabular Editor 3 no puede determinar la versión de Analysis Services utilizada, como ocurre, por ejemplo, cuando se carga directamente un archivo Model.bim. En este caso, Tabular Editor intenta adivinar en qué versión se implementará el modelo, en función del nivel de compatibilidad especificado en el modelo, pero, dependiendo de la versión real del destino de la implementación, puede haber varias diferencias en el lenguaje DAX que Tabular Editor no puede determinar. Si Tabular Editor informa de errores semánticos/de sintaxis incorrectos, es posible que tengas que ajustar estos ajustes.

# Formato automático

En la página **Editores de texto > Editor de DAX > Formato automático**, encontrará una amplia gama de ajustes para controlar cómo se formatea su código DAX.

![Ajustes de formato automático](~/content/assets/images/auto-formatting-settings.png)

##### *Formatear código automáticamente mientras escribe* (habilitado)

Esta opción aplicará automáticamente ciertas reglas de formato siempre que se produzcan determinadas pulsaciones de teclas. Por ejemplo, cuando se cierra un paréntesis, esta función garantizará que todo lo que esté dentro de los paréntesis se formatee de acuerdo con los demás ajustes de esta página.

##### *Formatear llamadas a funciones automáticamente* (habilitado)

Esta opción controla específicamente si el formateo automático de las llamadas a funciones (es decir, el espaciado entre los argumentos y los paréntesis) debe producirse cuando se cierra un paréntesis.

##### *Sangrado automático* (habilitado)

Esta opción aplica sangría automáticamente a los argumentos de la función cuando se inserta un salto de línea dentro de una llamada a función.

##### *Llaves automáticas* (habilitado)

Esta opción inserta automáticamente la llave o comilla de cierre cada vez que se introduce una llave o comilla de apertura.

##### *Envolver selección* (habilitada)

Cuando está habilitada, esta opción envuelve automáticamente la selección actual con la llave de cierre cuando se introduce una llave de apertura.

## Reglas de formato

Estos ajustes controlan cómo se formatean los espacios en blanco del código DAX, tanto cuando se produce el formateo automático como cuando el código se formatea manualmente (utilizando las opciones del menú **Formatear DAX**).

##### *Espacio después de funciones* (desactivado)

# [Habilitado](#tab/tab1)

```DAX
SUM ( 'Sales'[Amount] )
```

# [Deshabilitado](#tab/tab2)

```DAX
SUM( 'Sales'[Amount] )
```

***

##### *Nueva línea después de funciones* (deshabilitada)

Se aplica solo cuando una llamada a función debe dividirse en varias líneas.

# [Habilitado](#tab/tab3)

```DAX
SUM
(
    'Sales'[Amount]
)
```

# [Deshabilitado](#tab/tab4)

```DAX
SUM(
    'Sales'[Amount]
)
```

***

##### *Nueva línea antes del operador* (habilitada)

Se aplica solo cuando una operación binaria debe dividirse en varias líneas.

# [Habilitado](#tab/tab5)

```DAX
[Internet Total Sales]
    + [Reseller Total Sales]
```

# [Deshabilitado](#tab/tab6)

```DAX
[Internet Total Sales] +
    [Reseller Total Sales]
```

***

##### *Rellenar paréntesis* (habilitado)

# [Habilitado](#tab/tab7)

```DAX
SUM( Sales[Amount] )
```

# [Desactivado](#tab/tab8)

```DAX
SUM(Sales[Amount])
```

***

##### *Límite de línea de formato largo* (120)

El número máximo de caracteres que se pueden mantener en una sola línea antes de que una expresión se divida en varias líneas, al usar la opción **Formatear DAX (líneas largas)**.

##### *Límite de línea de formato corto* (60)

El número máximo de caracteres que se pueden mantener en una sola línea antes de que una expresión se divida en varias líneas, al usar la opción **Formatear DAX (líneas cortas)**.

> [!NOTE]
> La mayoría de los ajustes anteriores solo se aplican cuando se utiliza el formateador DAX integrado (predeterminado).

## Mayúsculas y comillas

Además de formatear los espacios en blanco del código DAX, Tabular Editor 3 también puede corregir las referencias a objetos y las mayúsculas y minúsculas de las funciones y palabras clave.

##### *Corregir calificadores de medida/columna* (habilitado)

Cuando esto está marcado, los prefijos de tabla se eliminan automáticamente de las referencias de medidas y se insertan automáticamente en las referencias de columnas.

##### *Mayúsculas preferidas para palabras clave* (predeterminado = MAYÚSCULAS)

Este ajuste le permite cambiar las mayúsculas y minúsculas utilizadas para las palabras clave, como `ORDER BY`, `VAR`, `EVALUATE`, etc. Esto también se aplica cuando se inserta una palabra clave a través de la función de autocompletar, incluidos los valores fijos de las palabras clave de las funciones que las utilizan. Consulta @preferences para ver la lista completa.

##### *Mayúsculas preferidas para funciones* (predeterminado = MAYÚSCULAS)

Este ajuste le permite cambiar las mayúsculas y minúsculas utilizadas para las funciones, como `CALCULATE(...)`, `SUM(...)`, etc. Esto también se aplica cuando se inserta una función a través de la función de autocompletar.

##### *Corregir mayúsculas de palabras clave/funciones* (habilitado)

Cuando esto está marcado, las mayúsculas y minúsculas de las palabras clave y las funciones se corrigen automáticamente cada vez que el código se formatea automáticamente o manualmente.

##### *Corregir mayúsculas de referencias de objetos* (habilitado)

DAX es un lenguaje que no distingue entre mayúsculas y minúsculas. Cuando esto está habilitado, las referencias a tablas, columnas y medidas se corrigen automáticamente de modo que las mayúsculas coincidan con el nombre físico de los objetos a los que se hace referencia. Esta corrección se realiza siempre que el código se formatee automáticamente o manualmente.

##### *Entrecomillar siempre tablas* (desactivado)

Hacer referencia a ciertos nombres de tablas no requiere que vayan entre comillas simples en DAX. Sin embargo, si prefiere que las referencias a tablas vayan siempre entre comillas, independientemente del nombre de la tabla, puede marcar esta opción.

##### *Prefijar siempre las columnas de extensión* (desactivado)

Las columnas de extensión se pueden definir sin un nombre de tabla. Cuando esto está marcado, el editor de DAX siempre añadirá el prefijo de la tabla a una columna de extensión, incluso si el nombre de la tabla está en blanco. En ese caso, la referencia de columna tendrá el siguiente formato: `''[Extension Column]`.

# Próximos pasos

- @boosting-productivity-te3