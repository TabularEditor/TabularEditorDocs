---
uid: personalizing-te3
title: Personalización y configuración de Tabular Editor 3 para adaptarlo a tus necesidades
author: Daniel Otykier
updated: 2021-09-28
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

# Personalización y configuración de Tabular Editor 3 para adaptarlo a tus necesidades

Tabular Editor 3 ofrece una amplia gama de opciones de configuración que te permiten ajustar la herramienta a tus necesidades específicas y a tu flujo de trabajo preferido. En este artículo, te guiaremos a través de la configuración que los desarrolladores de modelos suelen ajustar con más frecuencia.

A la mayoría de las opciones tratadas en este artículo se accede desde la opción de menú **Herramientas > Preferencias**. A lo largo del artículo, enumeraremos las configuraciones individuales con el siguiente formato para facilitar la consulta:

**_Nombre de la configuración_ (valor predeterminado)**<br/>Descripción de la configuración.

> [!TIP]
> Usa el **cuadro de búsqueda** en la parte superior del cuadro de diálogo de preferencias para localizar rápidamente ajustes por nombre o palabra clave. La búsqueda filtra el árbol de preferencias en tiempo real, ayudándote a ir directamente a la configuración que necesitas.

# Características generales

La primera página que encontrarás en el cuadro de diálogo **Preferencias** es **Tabular Editor > Características** (consulta la captura de pantalla a continuación). A continuación se muestra una breve descripción de las características de esta página y para qué se suelen usar:

![Preferencias: características generales](~/content/assets/images/pref-general-features.png)

## Power BI

Estas configuraciones son especialmente útiles para los desarrolladores que usan Tabular Editor 3 como [herramienta externa para Power BI Desktop](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools).

##### _Permitir operaciones de modelado no compatibles_ (deshabilitado)

Las herramientas externas para Power BI Desktop tienen algunas [limitaciones](xref:desktop-limitations). De forma predeterminada, Tabular Editor 3 te impedirá hacer cambios no compatibles en el Data model. Puede haber algunas características avanzadas de modelado que funcionen bien, aunque no estén admitidas; consulta el enlace anterior. Para desbloquear todos los objetos y propiedades del Tabular Object Model, habilita esta configuración.

##### _Ocultar advertencias de fecha/hora automáticas_ (deshabilitado)

Cuando la configuración "Fecha/hora automática" de Power BI Desktop está habilitada, se crean automáticamente varias tablas calculadas. Por desgracia, estas tablas incluyen código DAX que hace que el analizador de DAX integrado de Tabular Editor 3 muestre un mensaje de advertencia. Para ocultar estas advertencias, habilita esta configuración.

##### _Salto de línea en la primera línea de DAX_ (deshabilitado)

En Power BI Desktop es habitual insertar un salto de línea en la primera línea de una expresión DAX, debido a cómo la barra de fórmulas muestra el código DAX. Si a menudo alternas entre Tabular Editor y Power BI Desktop, considera habilitar esta opción para que Tabular Editor 3 inserte el salto de línea automáticamente cada vez que se edite una expresión DAX desde la herramienta.

## Sincronización de metadatos

Estas opciones controlan el comportamiento de Tabular Editor 3 cuando los metadatos del modelo se cargan desde una base de datos en una instancia de Analysis Services. Estas opciones especifican cómo Tabular Editor 3 gestiona los cambios de metadatos aplicados a la base de datos desde fuera de la aplicación; por ejemplo, cuando otro usuario modifica la base de datos o cuando tú cambias el modelo desde Power BI Desktop mientras usas Tabular Editor 3 como herramienta externa.

##### _Avisar cuando los metadatos locales no estén sincronizados con el modelo implementado_ (habilitado)

Cuando esta opción está activada, Tabular Editor muestra un mensaje de advertencia al intentar guardar cambios si otro usuario o proceso ha modificado la base de datos desde que los metadatos del modelo se cargaron en tu instancia de Tabular Editor.

##### _Seguir los cambios externos del modelo_ (habilitado)

Esta opción solo es relevante para instancias locales de Analysis Services (es decir, procesos msmdsrv.exe que se ejecutan en la misma máquina que Tabular Editor). Cuando está activada, Tabular Editor inicia un seguimiento en Analysis Services y te notifica si se realizan cambios externos.

##### _Actualizar automáticamente los metadatos locales del Tabular Object Model_ (habilitado)

Cuando el mecanismo de seguimiento descrito anteriormente está habilitado, esta opción permite que Tabular Editor actualice automáticamente los metadatos del modelo cuando se detecta un cambio externo. Esto es útil si alternas con frecuencia entre Power BI Desktop y Tabular Editor 3, ya que garantiza que los cambios realizados en Power BI Desktop se sincronicen automáticamente con Tabular Editor.

##### _Limpiar seguimientos huérfanos de Tabular Editor_

Normalmente, Tabular Editor 3 debería detener y eliminar automáticamente cualquier seguimiento de AS iniciado debido a las opciones anteriores. Sin embargo, si la aplicación se cerró de forma prematura, es posible que esos seguimientos nunca se detengan. Al hacer clic en este botón, se eliminarán todos los seguimientos de AS iniciados por cualquier instancia de Tabular Editor en la instancia actual de Analysis Services.

> [!NOTE]
> El botón de limpieza solo está disponible cuando Tabular Editor está conectado a una instancia de Analysis Services.

# Configuración del Explorador TOM

Las opciones siguientes controlan varios aspectos del Explorador TOM. Puedes encontrar estos ajustes en **Tabular Editor > Explorador TOM**:

![Ajustes del Explorador Tom](~/content/assets/images/tom-explorer-settings.png)

##### _Mostrar toda la rama_ (desactivado)

Al filtrar el Explorador TOM, de forma predeterminada, Tabular Editor 3 muestra todos los elementos de la jerarquía que coinciden con la cadena de filtro, incluidos sus elementos padre. Si también quieres ver todos los elementos secundarios (aunque no coincidan con la cadena de filtro), habilita esta opción.

##### _Mostrar siempre advertencias de eliminación_ (desactivado)

Si prefieres que Tabular Editor 3 te pida confirmar todas las eliminaciones de objetos, habilita esta opción. De lo contrario, Tabular Editor 3 solo te pedirá que confirmes las eliminaciones de varios objetos o las eliminaciones de objetos a los que hacen referencia otros objetos.

> [!NOTE]
> Todas las operaciones de eliminación en Tabular Editor 3 se pueden deshacer pulsando CTRL+Z.

# Ajustes generales del Editor de DAX

El Editor de DAX de Tabular Editor 3 es muy configurable y es fácil sentirse abrumado por la gran cantidad de ajustes disponibles. Esta sección destaca los ajustes más comunes e importantes. Encuentra los ajustes generales en **Editores de texto > Editor de DAX > General**:

![General del Editor de Dax](~/content/assets/images/dax-editor-general.png)

## General

Los ajustes _Números de línea_, _Plegado de código_, _Espacios en blanco visibles_ y _Guías de sangría_ sirven para activar o desactivar varias características Visuales del editor. En la captura de pantalla siguiente, se han habilitado las cuatro opciones:

![Espacios en blanco visibles](~/content/assets/images/visible-whitespace.png)

##### _Usar tabulaciones_ (desactivado)

Al marcar esta opción, se inserta un carácter de tabulación (`\t`) cada vez que se pulsa la tecla TAB. De lo contrario, se inserta un número de espacios correspondiente al ajuste _Ancho de sangría_.

##### _Estilo de comentario_ (barras inclinadas)

DAX admite comentarios de línea con barras (`//`) o guiones (`--`). Este ajuste determina qué estilo de comentario se usa cuando Tabular Editor 3 genera código DAX, por ejemplo, al usar la funcionalidad de scripts DAX.

## Ajustes de DAX

Estas opciones determinan determinados comportamientos del analizador de código DAX. La opción _Locale_ es simplemente una cuestión de preferencia. El resto de las opciones solo son relevantes cuando Tabular Editor 3 no puede determinar la versión de Analysis Services utilizada, como ocurre, por ejemplo, cuando se carga directamente un archivo Model.bim. En este caso, Tabular Editor intenta deducir en qué versión se implementará el modelo, basándose en el nivel de compatibilidad especificado en el modelo; sin embargo, en función de la versión real del destino de implementación, pueden existir distintas diferencias en el lenguaje DAX que Tabular Editor no puede determinar. Si Tabular Editor muestra errores semánticos o de sintaxis incorrectos en el Report, es posible que tengas que ajustar estas configuraciones.

# Formato automático

En la página **Editores de texto > Editor de DAX > Formato automático**, encontrarás una amplia variedad de configuraciones para controlar cómo se formatea tu código DAX.

![Configuración de formato automático](~/content/assets/images/auto-formatting-settings.png)

##### _Formatear automáticamente el código al escribir_ (habilitado)

Esta opción aplicará automáticamente determinadas reglas de formato cuando se produzcan ciertas pulsaciones de teclas. Por ejemplo, al cerrar un paréntesis, esta función se asegura de que todo lo que esté dentro del paréntesis se formatee según el resto de las configuraciones de esta página.

##### _Formatear automáticamente las llamadas a funciones_ (habilitado)

Esta opción controla específicamente si el formato automático de las llamadas a funciones (es decir, el espaciado entre argumentos y paréntesis) debe aplicarse cuando se cierra un paréntesis.

##### _Sangría automática_ (habilitado)

Esta opción aplica sangría automáticamente a los argumentos de las funciones cuando se inserta un salto de línea dentro de una llamada a función.

##### _Autocierre de llaves_ (habilitado)

Esta opción inserta automáticamente la llave o comilla de cierre cuando se introduce una llave o comilla de apertura.

##### _Encapsular la selección_ (habilitado)

Cuando está habilitada, esta opción envuelve automáticamente la selección actual con la llave de cierre cuando se introduce una llave de apertura.

## Reglas de formato

Estas configuraciones controlan cómo se formatea el espacio en blanco del código DAX, tanto cuando se aplica el formato automático como cuando el código se formatea manualmente (mediante las opciones del menú **Formatear DAX**).

##### _Espacio después de las funciones_ (deshabilitado)

# [Habilitado](#tab/tab1)

```DAX
SUM ( 'Sales'[Amount] )
```

# [Deshabilitado](#tab/tab2)

```DAX
SUM( 'Sales'[Amount] )
```

***

##### _Nueva línea después de las funciones_ (deshabilitado)

Solo se aplica cuando una llamada a una función debe dividirse en varias líneas.

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

##### _Nueva línea antes del operador_ (habilitado)

Solo se aplica cuando una operación binaria debe dividirse en varias líneas.

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

##### _Añadir espacios dentro de los paréntesis_ (habilitado)

# [Habilitado](#tab/tab7)

```DAX
SUM( Sales[Amount] )
```

# [Deshabilitado](#tab/tab8)

```DAX
SUM(Sales[Amount])
```

***

##### _Límite de línea en formato largo_ (120)

El número máximo de caracteres que se pueden mantener en una sola línea antes de que una expresión se divida en varias líneas, al usar la opción **Formato DAX (líneas largas)**.

##### _Límite de línea en formato corto_ (60)

El número máximo de caracteres que se pueden mantener en una sola línea antes de que una expresión se divida en varias líneas, al usar la opción **Formato DAX (líneas cortas)**.

> [!NOTE]
> La mayoría de los ajustes anteriores solo surten efecto al usar el formateador de DAX integrado (predeterminado).

## Uso de mayúsculas y comillas

Además de formatear los espacios en blanco del código DAX, Tabular Editor 3 también puede corregir las referencias a objetos y el uso de mayúsculas y minúsculas de funciones y palabras clave.

##### _Corregir calificadores de medidas/columnas_ (activado)

Cuando esta opción está marcada, los prefijos de tabla se eliminan automáticamente de las referencias a medidas y se insertan automáticamente en las referencias a columnas.

##### _Capitalización preferida de palabras clave_ (predeterminado = UPPER)

Esta configuración te permite cambiar el uso de mayúsculas/minúsculas en las palabras clave, como `ORDER BY`, `VAR`, `EVALUATE`, etc. Esto también se aplica cuando una palabra clave se inserta mediante la función de autocompletado.

##### _Capitalización preferida de funciones_ (predeterminado = UPPER)

Esta configuración te permite cambiar la capitalización de las funciones, como `CALCULATE(...)`, `SUM(...)`, etc. Esto también se aplica cuando una función se inserta mediante el autocompletado.

##### _Corregir mayúsculas/minúsculas de palabras clave y funciones_ (activado)

Cuando esta opción está marcada, el uso de mayúsculas/minúsculas en palabras clave y funciones se corrige automáticamente cada vez que el código se formatea automáticamente o de forma manual.

##### _Corregir mayúsculas/minúsculas de las referencias a objetos_ (activado)

DAX no distingue entre mayúsculas y minúsculas. Cuando está activado, las referencias a tablas, columnas y medidas se corrigen automáticamente para que el uso de mayúsculas/minúsculas coincida con el nombre físico de los objetos a los que se hace referencia. Esta corrección se realiza cada vez que el código se formatea automáticamente o de forma manual.

##### _Citar siempre las tablas_ (desactivado)

En DAX, para hacer referencia a determinados nombres de tabla no es necesario poner comillas simples alrededor. Sin embargo, si prefieres que las referencias a tablas vayan siempre entre comillas, independientemente del nombre de la tabla, puedes activar esta opción.

##### _Anteponer siempre el prefijo de tabla a las columnas de extensión_ (desactivado)

Las columnas de extensión se pueden definir sin un nombre de tabla. Cuando esta opción está seleccionada, el Editor de DAX siempre añadirá el prefijo de tabla a una columna de extensión, incluso si el nombre de la tabla está en blanco. En ese caso, la referencia a la columna se verá así: `''[Extension Column]`.

# Siguientes pasos

- @boosting-productivity-te3