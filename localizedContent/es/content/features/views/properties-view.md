---
uid: properties-view
title: Vista de propiedades
author: Morten Lønskov
updated: 2026-11-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
      note: "Property grid only, without the Basic and Advanced tabs"
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Uso de la vista Propiedades en Tabular Editor

La vista Propiedades muestra las propiedades de los objetos que selecciona en el Explorador TOM y le permite editarlas. En Tabular Editor 3, con la versión preliminar pública de la **vista Propiedades básicas** activada, la vista tiene dos pestañas en la parte inferior:

- **Básica**: un formulario con los campos que Power BI Desktop muestra en el panel **Propiedades** de su **Vista de modelo**, como el nombre, la descripción, la carpeta de visualización y el formato de una medida.
- **Avanzada**: la cuadrícula de propiedades con todas las propiedades del objeto, una barra de herramientas y un cuadro de búsqueda. También enumera las propiedades que Visual Studio y Power BI Desktop no muestran.

> [!NOTE]
> Las pestañas **Básica** y **Avanzada** son una versión preliminar pública. Hasta que actives la vista previa, la vista Propiedades solo mostrará la cuadrícula de propiedades descrita en la [pestaña Avanzado](#advanced-tab), como en Tabular Editor 2.

## Activar la pestaña «Básico»

1. Vaya a **Herramientas > Preferencias > Tabular Editor > Versiones preliminares públicas**.
2. Marque **Vista de propiedades básicas**.
3. Haga clic en **Aceptar**.

La vista Propiedades muestra las pestañas **Básica** y **Avanzada**. Para volver a la cuadrícula de propiedades sola, desmarque **Vista de propiedades básicas**. Consulte [Vistas previas públicas](xref:preferences#tabular-editor--public-previews).

## Elegir una pestaña

Haga clic en **Básica** o **Avanzada** en la parte inferior de la vista Propiedades para cambiar de pestaña. La pestaña en la que haga clic permanecerá seleccionada para todos los objetos y después de reiniciar. **Mostrar en Avanzado**, **Mostrar Avanzado** y saltar a una propiedad cambian a **Avanzado** sin modificar esa elección, por lo que, tras reiniciar, la vista se abre en la última pestaña en la que hizo clic.

Cuando activa la vista previa, la vista Propiedades se abre en **Básica**. Si desactivas la versión preliminar y la vuelves a activar, se abrirá en la pestaña que tenías. Para establecer la pestaña, cambie **Pestaña de la vista de propiedades** en **Vista de propiedades básicas** en **Herramientas > Preferencias > Tabular Editor > Vistas previas públicas**.

## Pestaña Básico

![Pestaña «Básica» de la vista «Propiedades» para una medida](~/content/assets/images/user-interface/properties-view-basic.png)

La pestaña **Básica** muestra un campo por propiedad, con su etiqueta encima. Una descripción tiene un cuadro de texto de varias líneas, una opción como **Está oculta** es un conmutador y una opción es una lista. Las listas utilizan los nombres que usa Power BI Desktop, como **Fecha/hora** para un tipo de datos o **No resumir** para el resumen de una columna. La pestaña **Básica** no tiene barra de herramientas.

Los campos de una sola línea, como las listas y los cuadros de texto, tienen aproximadamente 250 píxeles de ancho con un escalado del 100 %, por lo que se alinean. Un campo adopta el ancho de la vista cuando el valor que muestra es más ancho y se reduce cuando la vista es más estrecha. Una lista abierta puede ser más ancha que su campo, por lo que un elemento largo no ensancha el campo. El cuadro **Descripción** muestra una línea cuando su texto es corto y se amplía hasta cuatro líneas a medida que escribe.

Cuando el puntero del ratón está sobre una lista o sobre el cuadro **Descripción**, la rueda del ratón desplaza el formulario. Haga clic en **Descripción** para desplazarse por su texto.

Un valor que elija de una lista abierta se aplica de inmediato. Con el foco en una lista cerrada, **Arriba**, **Abajo**, **Inicio**, **Fin** o una letra recorren los valores sin aplicarlos. Pulse **Intro** o salga del campo para aplicar el valor, o pulse **Esc** para mostrar de nuevo el valor actual. Una lista en la que puedes escribir, como **Categoría de datos** o **Nivel de compatibilidad**, aplica el valor cuando pulsas **Intro**, sales del campo o seleccionas una opción de la lista, pero no mientras escribes.

**Carpeta para mostrar** y la **Cadena de conexión** de un origen de datos heredado tienen un botón **...** que abre el mismo cuadro de diálogo que en la pestaña **Avanzado**: **Elegir carpeta** para una carpeta para mostrar y el cuadro de diálogo de conexión para una cadena de conexión.

### Campos por tipo de objeto

Los campos dependen del tipo de objeto seleccionado:

| Objeto | Campos |
|---|---|
| Medida | **Nombre**, **Tabla de inicio**, **Descripción**, **Carpeta de visualización**, **Está oculta**, **Formato**, **Expresiones** |
| Columna | **Nombre**, **Descripción**, **Carpeta de visualización**, **Está oculta**, **Tipo de datos**, **Formato**, **Ordenar por columna**, **Categoría de datos**, **Resumir por**, **Puede ser nula**. Una columna importada también tiene **Columna de origen**, en primer lugar bajo **Datos**. Una columna calculada tiene **Expresiones**, antes de **Datos**. |
| Tabla | **Nombre**, **Descripción**, **Está oculta**, **Columna clave**, **Categoría de datos**, **Modo de almacenamiento**, **Expresiones**, **Seguridad a nivel de fila**. Una tabla calculada tiene **Expresiones** antes de **Datos**. |
| Grupo de cálculo | **Nombre**, **Descripción**, **Está oculto**, **Elementos de cálculo**, **Precedencia del grupo de cálculo** (con más de un grupo de cálculo), **Expresiones** |
| Relación | **De la tabla**, **De la columna**, **Cardinalidad**, **A la tabla**, **A la columna**, **Activar esta relación**, **Dirección del filtro cruzado** |
| Jerarquía | **Nombre**, **Descripción**, **Carpeta de visualización**, **Está oculta**, **Niveles** |
| Nivel | **Nombre**, **Descripción**, **Columna** |
| Elemento de cálculo | **Nombre**, **Descripción**, **Ordinal**, **Expresiones** |
| KPI | **Descripción** y una sección de **Estado**, **Objetivo** y **Tendencia**, cada una con su cuadro **Expresión** |
| Modelo | **Nombre**, **Descripción**, **Modo de compatibilidad**, **Nivel de compatibilidad**, **Culturas**, **Desaconsejar medidas implícitas** |
| Rol | **Nombre**, **Descripción**, **Permiso del modelo**, **Seguridad a nivel de fila** |
| Permiso de tabla | **Tabla** (solo lectura), **Expresiones** |
| Partición | **Nombre**, **Descripción**, **Expresiones** |
| Expresión compartida | **Nombre**, **Descripción**, **Expresiones** |
| Función DAX definida por el usuario | **Nombre**, **Descripción**, **Está oculta**, **Expresiones** |
| Calendario | **Nombre**, **Descripción**, **Asignaciones de columnas** |
| Origen de datos heredado | **Nombre**, **Descripción**, **Cadena de conexión** |
| Origen de datos de Power Query | **Nombre**, **Descripción**, **Protocolo**, los campos de dirección que están configurados, como **Servidor** y **Base de datos**, **Tipo de autenticación** |
| Perspectiva | **Nombre**, **Descripción**, **Editar en el editor de perspectivas** |
| Cultura | **Idioma**, **Editar en el editor de traducción de metadatos** |
| Carpeta para mostrar, grupo de tablas | **Nombre** |

Al cambiar el nombre de una carpeta de visualización, sus objetos se desplazan a la nueva carpeta, y al cambiar el nombre de un grupo de tablas, sus tablas se desplazan al nuevo grupo, como un solo paso de deshacer. Esto funciona de la misma manera que cambiar el nombre de la carpeta o del grupo en el Explorador TOM.

**Tabla de origen** mueve una medida a otra tabla, de la misma manera que al arrastrarla en el Explorador TOM. **Columna clave** establece la columna que identifica las filas de la tabla, y al elegir una columna se elimina el marcador de la columna que lo tenía. **Categoría de datos** establece el tipo de datos que contiene la tabla, como **Tiempo**. **Modo de almacenamiento** establece el modo de las particiones de la tabla en **Importar**, **DirectQuery** o **Doble**. Es de solo lectura para las tablas calculadas, Direct Lake, «push» y de rangos de políticas, así como para las tablas cuyas particiones tienen modos diferentes.

Un campo es de solo lectura cuando el modelo no permite el cambio. Por ejemplo, mientras Tabular Editor esté conectado a una versión de Power BI Desktop que restrinja las operaciones de modelado que pueden realizar las herramientas externas, **Tabla principal**, **Niveles** y **Elementos de cálculo** pueden estar en modo de solo lectura. Consulte [Operaciones de modelado compatibles](xref:desktop-integration#supported-modeling-operations).

Cuando el objeto seleccionado no tiene campos en la pestaña **Básico**, como un miembro de rol, la pestaña muestra el mensaje **Este objeto no tiene propiedades básicas.** Haga clic en **Mostrar avanzadas** para ver sus propiedades en la pestaña **Avanzadas**.

### Secciones

Cuando un formulario tiene más de un grupo de campos, los campos están en secciones separadas por una línea:

- **General**: el nombre, la descripción, la carpeta de visualización, la visibilidad y los demás campos del objeto.
- **Formato**: **Tipo de datos** y **Formato**.
- **Datos**: **Columna clave**, **Categoría de datos** y **Modo de almacenamiento** en una tabla, y **Columna de origen**, **Ordenar por columna**, **Categoría de datos**, **Resumir por** e **Es anulable** en una columna.
- **Conexión**: los campos de conexión de un origen de datos. Consulte [Orígenes de datos](#data-sources).
- **Niveles**: consulte [Niveles de jerarquía](#hierarchy-levels).
- **Elementos de cálculo**: consulte [Elementos de cálculo](#calculation-items).
- **Asignaciones de columnas**: consulte [Asignaciones de columnas de calendario](#calendar-column-mappings).
- **Precedencia de los grupos de cálculo**: consulte [Precedencia de los grupos de cálculo](#calculation-group-precedence).
- **Estado**, **Objetivo** y **Tendencia**: consulte [KPI](#kpis).
- **Expresiones**: consulte [Expresiones](#expressions).
- **Seguridad a nivel de fila**: consulte [Seguridad a nivel de fila](#row-level-security).

Haz clic en el encabezado de una sección para contraerla y vuelve a hacer clic para expandirla. Con el teclado, pulse **Tab** para desplazarse a un encabezado y **Espacio** o **Intro** para contraerlo. Una sección plegada permanece plegada para todos los objetos y después de un reinicio. Un formulario cuyos campos pertenecen todos a **General**, como una relación o el modelo, no tiene encabezados de sección.

Los encabezados **Datos**, **Niveles**, **Elementos de cálculo**, **Asignaciones de columnas**, **Precedencia de grupos de cálculo**, **Expresiones** y **Seguridad a nivel de fila** tienen un botón de información. Haga clic en él o pulse **F1** en el encabezado para leer qué hacer en la sección. En el caso de la mayoría de los objetos, la nota también enlaza con la documentación.

### Formato

En una medida o columna con un tipo de datos numérico o de fecha/hora, o en una medida cuyo tipo de datos aún no se conoce, **Formato** enumera los formatos que ofrece la pestaña **Avanzado**, seguidos de **Personalizado**:

- para números: **General**, **Número entero**, **Número decimal**, **Moneda**, **Porcentaje** y **Científico**
- para fechas: **General** y los patrones de fecha

El cuadro de texto situado debajo de la lista siempre muestra la cadena de formato. Al elegir un formato de número, se mantienen los decimales, el separador de millares y el estilo de los números negativos de la cadena de formato actual. Para escribir su propia cadena de formato, seleccione **Personalizado** o haga clic en el cuadro de texto, escriba la cadena de formato y pulse **Intro** o salga del cuadro. Pulse **Esc** para descartar lo que ha escrito. La lista muestra el formato que coincide con la cadena de formato, o **Personalizado** cuando no coincide ningún formato.

Una columna con un tipo de datos de texto, verdadero/falso o binario tiene un cuadro de texto para la cadena de formato, sin la lista. Para conocer la cadena de formato que escribe **Moneda**, consulta los ajustes de **Localización** en @preferences.

### Relaciones

Los extremos de una relación son **De tabla** y **De columna**, y **A tabla** y **A columna**. Cuando elige una tabla, se abre su lista de columnas, para que pueda elegir una columna de esa tabla. Cuando elige una **Tabla de destino**, se elige por usted la columna que coincide con la **Columna de origen**, como en el cuadro de diálogo **Editar relación**. La columna que elija se aplica de inmediato. Una tabla sin columna no se aplica, y si se deja el extremo, se muestra la relación tal como estaba. La **Cardinalidad** establece ambos extremos de la relación, por ejemplo, **Muchos a uno (\*:1)**, y la **Dirección del filtro cruzado** ofrece **Única**, **Ambas** y **Automática**.

Se marca un cambio como en el cuadro de diálogo **Editar relación**, y el resultado se muestra como un icono junto a la lista:

- No se aplica un error. Seleccionar la tabla del otro extremo es un error, porque una relación no puede unir una tabla consigo misma. El enfoque permanece en el extremo hasta que lo corrijas, o pulsa **Esc** para mostrar la relación tal como estaba.
- Se aplica una advertencia. Una columna de otro tipo de datos, o una columna que establece una segunda relación activa entre las mismas dos tablas, recibe una advertencia. Pulse **Ctrl+Z** para deshacer el cambio.

Mientras Tabular Editor está conectado a un modelo, la comprobación de integridad referencial se ejecuta en el servidor solo después de cambiar una columna, no cuando seleccionas una relación. En un modelo Direct Lake, no se ejecuta.

### Niveles de jerarquía

La sección **Niveles** de una jerarquía enumera sus niveles desde la parte superior, numerados. Cuando el nombre de un nivel difiere del nombre de su columna, la columna aparece después del nombre del nivel. Editar los niveles de la lista:

| Acción | Ratón | Teclado |
|---|---|---|
| Mover un nivel | Arrastrarlo a otra posición | **Alt+Flecha arriba** o **Alt+Flecha abajo** en el nivel seleccionado |
| Cambiar el nombre de un nivel | Hacer doble clic en su nombre | **F2** en el nivel seleccionado |
| Eliminar un nivel | Hacer clic en la **x** de la fila del nivel | **Supr** en el nivel seleccionado |

Para añadir un nivel, haga clic en **Añadir un nivel** y elija una columna. La lista muestra las columnas de la tabla que no están en la jerarquía, y la columna que elija se convierte en el nivel más bajo. Cada movimiento, cambio de nombre, eliminación o adición es un paso de deshacer.

Consulte @object-properties-hierarchies para ver las propiedades de las jerarquías y los niveles.

### Elementos de cálculo

La sección **Elementos de cálculo** de un grupo de cálculos enumera sus elementos de cálculo en orden, numerados. Mueva, cambie el nombre y elimine elementos de la misma manera que los niveles de jerarquía: arrastre un elemento o pulse **Alt+Flecha arriba** o **Alt+Flecha abajo**, haga doble clic en su nombre o pulse **F2**, y haga clic en su **x** o pulse **Supr**.

Haga clic en **Añadir un elemento de cálculo** para añadir un elemento al final de la lista. Se abre en el Editor de expresiones, donde puede escribir su DAX. Cada movimiento, cambio de nombre, eliminación o adición es un paso de deshacer.

Al mover un elemento, se numera el **Ordinal** de cada elemento a partir de 0 en el nuevo orden, incluso cuando los ordinales empezaban en 1 o tenían huecos. Es de esperar que el ordinal de cada elemento aparezca como modificado en una comparación de los archivos del modelo.

Un grupo de cálculos no tiene **Columna clave**, **Modo de almacenamiento** ni **Seguridad a nivel de fila**, porque el motor no los utiliza para los grupos de cálculos.

### Precedencia del grupo de cálculo

En un modelo con más de un grupo de cálculo, el formulario de un grupo de cálculo tiene una sección **Precedencia del grupo de cálculo**, que enumera todos los grupos de cálculo del modelo desde **Aplicado primero** hasta **Aplicado último**. El grupo con la prioridad más alta está en la parte superior, el grupo seleccionado aparece en negrita y el número de prioridad de cada grupo está a la derecha. Cuando más de un grupo de cálculos cambia la misma medida, se aplica primero el grupo que está más arriba en la lista.

Para cambiar el orden, arrastre un grupo a otra posición o selecciónelo y pulse **Alt+Flecha arriba** o **Alt+Flecha abajo**. Un desplazamiento reasigna los valores de precedencia que los grupos ya tienen en el nuevo orden, de modo que los grupos que no se desplazan conservan los suyos. Cuando dos grupos comparten un valor de precedencia, un movimiento numera cada grupo en su lugar, empezando por 0 para el grupo aplicado en último lugar. Cada movimiento es un paso de deshacer.

Consulte @object-properties-calculation-groups para ver la propiedad `Precedence`.

### Asignaciones de columnas de calendario

La sección **Asignaciones de columnas** de un calendario muestra un cuadro con una línea para cada unidad de tiempo y su columna principal. Una unidad con columnas asociadas muestra, por ejemplo, **+2 asociadas** después de su columna, y una línea **Relacionada con el tiempo** enumera las columnas relacionadas con el tiempo. Haga clic en el cuadro para editar las asignaciones en el [Editor de calendarios](xref:calendars). En el caso de un calendario sin asignaciones, el cuadro indica **No hay unidades de tiempo asignadas. Haga clic para asignar columnas en el Editor de calendarios.**

Consulte @object-properties-calendars para conocer las propiedades de los calendarios.

### Modelo

**Nivel de compatibilidad** muestra el nivel de compatibilidad actual del modelo y los niveles superiores que Tabular Editor reconoce para el modo de compatibilidad del modelo. En el caso de un modelo de Power BI, ese es el nivel actual y el nivel más alto que admite Power BI. Elige un nivel de la lista o escribe uno y pulsa Intro o sal del cuadro. Si un objeto del modelo necesita un nivel superior al que usted introduce, un error indica el nombre del objeto y el nivel no cambia. Un cambio de nivel de compatibilidad es un paso de deshacer. Consulte @update-compatibility-level.

El **modo de compatibilidad** es **Analysis Services** o **Power BI**. Cuando elige el otro modo, **Nivel de compatibilidad** enumera los niveles de ese modo. Si el modelo no puede usar el modo que elija, se mostrará un error y el modo no cambiará.

El **Modo de compatibilidad** y el **Nivel de compatibilidad** son de solo lectura cuando el modelo no permite el cambio.

**Culturas** es de solo lectura y enumera las culturas del modelo, con la cultura propia del modelo en primer lugar, por ejemplo **en-US (modelo), da-DK**. Un modelo sin culturas muestra **(ninguna)**. Para añadir o eliminar una cultura, utilice el nodo **Traducciones** en el Explorador TOM. El formulario de una cultura tiene un botón **Editar en el editor de traducción de metadatos**, y el formulario de una perspectiva tiene un botón **Editar en el editor de perspectivas**, que abren el editor en la cultura o perspectiva seleccionada.

### Orígenes de datos

Un origen de datos heredado muestra su **cadena de conexión**, con la contraseña sustituida por `********`. Edite el resto de la cadena de conexión y el origen de datos conservará su contraseña. Haga clic en **...** para crear la cadena de conexión en el cuadro de diálogo de conexión.

Un origen de datos de Power Query muestra su **Protocolo**, las partes de su dirección que están configuradas, como **Servidor** y **Base de datos**, y su **Tipo de autenticación**. Un campo que borres permanece en el formulario, vacío, hasta que se guarde el modelo, para que puedas escribir el nuevo valor. Para establecer otra parte de la dirección, use la pestaña **Avanzadas**.

### KPI

Un KPI tiene una sección de **Estado**, una de **Objetivo** y una de **Tendencia**, cada una de ellas comienza con su cuadro **Expresión**:

- **Estado**: **Expresión**, **Descripción** y **Gráfico**
- **Objetivo**: **Expresión**, **Descripción** y **Formato**
- **Tendencia**: **Expresión**, **Descripción** y **Gráfico**

Haga clic en un cuadro **Expresión** para escribir la expresión en el Editor de expresiones. Una sección cuya expresión está vacía se pliega. Un KPI no tiene sección **Expresiones** ni **Añadir una expresión**.

### Expresiones

La sección **Expresiones** muestra las expresiones DAX, M y SQL del objeto en cuadros. Cada cuadro muestra hasta cuatro líneas de su expresión y se desvanece cuando la expresión es más larga. Una etiqueta en la esquina del cuadro indica el idioma: **DAX**, **M** o **SQL**. Un cuadro vacío tiene un borde discontinuo. Haga clic en un cuadro o pulse **Intro** o **Espacio** cuando tenga el foco para abrir la expresión en el **Editor de expresiones**. El cursor se desplaza al Editor de expresiones, para que pueda empezar a escribir de inmediato.

La expresión principal del objeto siempre tiene un cuadro, por ejemplo, la **Expresión** de una medida o la consulta de una partición. Cuando está vacío, el cuadro indica, por ejemplo, **No establecido. Haga clic para escribir DAX en el Editor de expresiones.** Las otras expresiones, como **Expresión de cadena de formato** y **Expresión de filas de detalles**, tienen un cuadro cuando se establecen.

Para establecer otra expresión, haga clic en **Añadir una expresión**. La lista muestra las expresiones que aún no se han establecido, cada una con una línea que indica para qué sirve. Algunas entradas tienen un enlace a la página que las explica, por ejemplo, **Expresiones de filas de detalles**, que abre [Expresión de filas de detalles](xref:detail-rows-expression). Elija una entrada para añadir un cuadro vacío y ábralo en el Editor de expresiones. El cuadro vacío permanece hasta que seleccione otro objeto.

La sección **Expresiones** aparece cuando se selecciona un objeto, en todos los tipos de objetos con expresiones, excepto en los KPI. Consulte [KPI](#kpis).

### Seguridad a nivel de fila

Las tablas y los roles tienen una sección de **Seguridad a nivel de fila**. En una tabla, muestra un cuadro para cada rol que tenga un filtro en la tabla. En un rol, muestra un cuadro para cada tabla que filtra el rol. Haga clic en un cuadro para abrir el filtro en el Editor de expresiones.

Para añadir un filtro, haga clic en **Añadir un filtro para un rol** en una tabla, o en **Añadir un filtro en una tabla** en un rol, y elija el rol o la tabla. Se añade un filtro vacío y se abre en el Editor de expresiones. El **Permiso de modelo** del rol no cambia. **Editar > Deshacer** elimina el filtro en un solo paso.

Consulta @data-security-setup-rls para saber cómo escribir el filtro.

### Seleccionar varios objetos

Cuando selecciona varios objetos, la pestaña **Básico** muestra los campos que tienen en común. En la parte superior del formulario se indica cuántos objetos están seleccionados, por ejemplo, **3 medidas** o **5 objetos** cuando son de tipos diferentes. Un campo cuyo valor difiere entre los objetos muestra **(Múltiples valores)**. Una modificación establece el campo en todos los objetos seleccionados como un solo paso de deshacer, por lo que **Ctrl+Z** lo revierte en todos ellos.

Estos campos se aplican a un objeto a la vez y no aparecen cuando se seleccionan varios objetos:

- **Nombre** y **Columna clave**
- la **Columna** de un nivel y el **Ordinal** de un elemento de cálculo
- **De tabla**, **De columna**, **A tabla** y **A columna** de una relación
- **Tabla** de un permiso de tabla
- **Niveles**, **Elementos de cálculo**, **Asignaciones de columnas** y **Precedencia de grupos de cálculo**
- **Expresiones**, los cuadros **Expresión** de los KPI y **Seguridad a nivel de fila**
- los botones **Editar en el editor de perspectivas** y **Editar en el editor de traducción de metadatos**

### Propiedades en la pestaña Avanzado

Cuando el objeto seleccionado tiene valores en propiedades que solo muestra la pestaña **Avanzado**, una línea en la parte inferior del formulario indica cuántas, por ejemplo, **3 propiedades avanzadas tienen valores.** Si hay varios objetos seleccionados, la línea cuenta los objetos que tienen dichos valores. Traducciones, pertenencias a perspectivas, seguridad a nivel de objeto, anotaciones personalizadas y opciones modificadas con respecto a su recuento predeterminado. No se cuentan las etiquetas de linaje, los sinónimos, las propiedades de solo lectura, los valores que infiere Tabular Editor ni las anotaciones que escriben Power BI Desktop y Tabular Editor.

Haga clic en **Mostrar en Avanzado** para abrir la pestaña **Avanzado** con la opción **Solo propiedades avanzadas con valores** activada, de modo que la cuadrícula muestre únicamente esas propiedades. Para volver a ver todas las propiedades, desactive **Solo propiedades avanzadas con valores** en la barra de herramientas, seleccione otro objeto o cambie a **Básica**.

## Pestaña Avanzado

La pestaña **Avanzado** es una cuadrícula de propiedades con todas las propiedades del tipo de objeto seleccionado, como nombre, descripción, tipo de datos, cadena de formato, traducciones y anotaciones. Para obtener una descripción de cada propiedad, consulte @object-properties.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/properties-view.png" alt="Vista de propiedades" style="width: 500px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Ejemplo de propiedades de una tabla. Cada objeto tiene propiedades diferentes según su tipo </figcaption>
</figure>

En la pestaña **Avanzado**, puedes:

- Ver y modificar las propiedades de cualquier objeto del modelo, como tablas, columnas, medidas, jerarquías, relaciones, particiones, roles y perspectivas.
- Filtrar y ordenar las propiedades por nombre o categoría utilizando el cuadro de búsqueda y los botones de la parte superior de la vista.
- Copiar y pegar valores de propiedades entre diferentes objetos usando **Ctrl+C** y **Ctrl+V**.
- Deshacer y rehacer los cambios en las propiedades con **Ctrl+Z** y **Ctrl+Y**.
- navegar y editar propiedades con el teclado. Por ejemplo, pulse **Ctrl+Flecha arriba** o **Ctrl+Flecha abajo** para moverse entre propiedades, **Intro** o **F2** para editar el valor de una propiedad y **Esc** para cancelar la edición.

> [!TIP]
> Puede seleccionar varios objetos a la vez para ver las propiedades que tienen en común y editarlas de forma masiva. Esto puede ser útil para establecer cadenas de formato, por ejemplo.

### Barra de herramientas

La barra de herramientas situada en la parte superior de la pestaña **Avanzado** contiene los siguientes botones:

- **Categorizadas**: Agrupa las propiedades en categorías como *General*, *Metadatos* y *Opciones*.
- **Alfabético**: Enumera todas las propiedades en una única lista ordenada alfabéticamente.
- **Mostrar cambios**: Oculta todas las propiedades que no han cambiado desde la última vez que se guardó el modelo, de modo que solo queden las propiedades con [cambios no guardados](xref:unsaved-changes). Mientras el filtro está activo, el título de la vista dice **Propiedades (modificadas)**.
- **Solo propiedades avanzadas con valores**: Muestra únicamente las propiedades que contienen un valor y no aparecen en la pestaña **Básicas**. El botón solo se muestra mientras la vista previa de la **Vista de propiedades básicas** está activada. Consulte [Propiedades en la pestaña «Avanzado»](#properties-on-the-advanced-tab).
- **Descripciones de propiedades**: Muestra u oculta el panel de descripción en la parte inferior de la vista, que explica la propiedad seleccionada actualmente. Para obtener una descripción completa de cada propiedad, consulte @object-properties.
- **Cuadro de búsqueda**: filtra la lista de propiedades por nombre.

## Cambios sin guardar

En la pestaña **Avanzado**, las propiedades que difieren de la última versión guardada del modelo se muestran con un fondo de fila de color naranja claro. En la pestaña **Básico**, un campo modificado adquiere el mismo tono y un icono de cambio después de su etiqueta. Un cuadro de expresión modificado muestra el icono después de su nombre. Las filas modificadas en **Niveles**, **Elementos de cálculo** y **Precedencia de grupos de cálculo** también muestran el icono. Los encabezados **Niveles**, **Elementos de cálculo**, **Asignaciones de columnas**, **Precedencia de grupos de cálculo**, **Expresiones** y **Seguridad a nivel de fila** muestran el icono cuando se modifica algo en la sección. Cuando se seleccionan varios objetos, una propiedad se marca si alguno de los objetos seleccionados la ha cambiado.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/unsaved-changes/revert-property.png" alt="Vista de propiedades con cambios sin guardar" style="width: 500px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> Una medida con cambios no guardados en su descripción y en su cadena de formato. La opción <strong>Revertir</strong> devuelve una sola propiedad a su valor guardado.</figcaption>
</figure>

En la pestaña **Avanzado**, haga clic derecho en una fila marcada y elija **Revertir** para devolver esa propiedad al valor que tenía en el último guardado, sin afectar a ningún otro cambio sin guardar. La reversión es un solo paso en la pila de deshacer, por lo que **Ctrl+Z** vuelve a aplicar el cambio. Consulte @unsaved-changes para obtener más información, incluida la forma de revertir objetos completos desde el Explorador TOM y de desactivar los indicadores en **Herramientas > Preferencias**.

## Acoplamiento

La vista Propiedades se encuentra de forma predeterminada en la esquina inferior derecha, pero también puedes abrirla pulsando F4 en el teclado. También puedes acoplarla a cualquier lado de la ventana principal o desacoplarla como una ventana independiente.
