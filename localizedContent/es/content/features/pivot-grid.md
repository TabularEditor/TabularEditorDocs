---
uid: pivot-grid
title: Pivot Grids
author: Daniel Otykier
updated: 2026-10-11
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
# Pivot Grids

> [!NOTE]
> La información de este artículo se refiere a Tabular Editor 3.16.0 o versiones posteriores. Asegúrese de que está usando la última versión de Tabular Editor 3 para aprovechar las nuevas características y mejoras.

Al desarrollar modelos semánticos, es posible que a menudo desee comprobar que sus expresiones DAX devuelvan los valores esperados. Tradicionalmente, esto se hacía utilizando herramientas cliente como Excel o Power BI. Con Tabular Editor 3, puedes utilizar **cuadrículas dinámicas**, que funcionan de forma muy similar a las conocidas tablas dinámicas de Excel. Pivot Grid le permite crear rápidamente vistas resumidas de los datos de su modelo, lo que le permite probar el comportamiento de sus medidas DAX al filtrar y segmentar por varias columnas y jerarquías.

![Ejemplo de Pivot Grid](~/content/assets/images/pivot-grid-example.png)

La captura de pantalla anterior muestra un Pivot Grid que contiene dos medidas, «[Total Net Order Value]» y «[Net Orders]», que se segmentan horizontalmente por año, se filtran para 2021 y 2022, y verticalmente por la jerarquía de productos. Los usuarios de Tabular Editor 3 pueden utilizar esta función para asegurarse de que las expresiones DAX subyacentes a las medidas funcionan como se espera y para validar rápidamente los datos del modelo.

De forma predeterminada, Pivot Grid se actualiza automáticamente cada vez que guarda los cambios en el modelo semántico (Ctrl+S). De este modo, puede iterar rápidamente en sus expresiones DAX y ver los resultados en el Pivot Grid sin tener que esperar a que el modelo se actualice. Para ello, cambie sus medidas, guarde el modelo y vea directamente la nueva definición de medida reflejada en el Pivot Grid. Un buen flujo de trabajo consiste en abrir el Pivot Grid en una ventana separada mientras se trabaja en las expresiones DAX en el **Editor de expresiones** o utilizando un **Script DAX**.

> [!TIP]
> Algunas aclaraciones sobre la terminología:
> - **Campos** se refiere a las medidas del modelo, los KPI, las columnas y las jerarquías. En otras palabras, cualquier cosa que se pueda arrastrar al Pivot Grid.
> - Los **KPI** son un tipo especial de medida que se puede crear en Tabular Editor. Se muestran en el Pivot Grid al igual que las medidas, pero con un icono especial para indicar que son KPI. Cada KPI puede tener hasta 3 valores diferentes (objetivo, tendencia y estado), que se muestran por separado en el Pivot Grid.
> - Las **columnas** del Pivot Grid (como en el término «Área de columnas») no deben confundirse con las columnas del modelo. En el Pivot Grid, las columnas se usan para segmentar los datos horizontalmente, mientras que las filas se usan para segmentar los datos verticalmente.
> - Las **celdas** del Pivot Grid son los puntos de datos individuales en los que se cruzan una fila y una columna. Cada celda contiene un único valor, que es el resultado de la expresión DAX de la medida específica, evaluada en el contexto de filtro producido por los valores del *Área de filas* y del *Área de columnas*, en combinación con cualquier filtro aplicado a los campos del *Área de filtros*.

> [!NOTE]
> Es posible que los desarrolladores con experiencia en el ámbito multidimensional estén más familiarizados con los términos *Dimensiones* y *Atributos*. En los modelos semánticos, las *dimensiones* están representadas por *tablas* del modelo, y los *atributos* están representados por *columnas* del modelo. Las *jerarquías* en un modelo semántico son simplemente una forma de agrupar columnas, como en una jerarquía de calendario: Año > Trimestre > Mes > Día. Estas jerarquías solían llamarse *Jerarquías de atributos* o *Jerarquías definidas por el usuario* en los modelos multidimensionales.

## Creación de un Pivot Grid

Puede crear un Pivot Grid nuevo y vacío a través de la opción de menú **Archivo > Nuevo > Nuevo Pivot Grid**. Como alternativa, seleccione una o más medidas en el **Explorador TOM**, haga clic derecho o vaya al menú **Medida** y seleccione **Añadir a Pivot Grid**, para crear un nuevo Pivot Grid con las medidas seleccionadas.

![Crear Pivot Grid desde el Explorador TOM](~/content/assets/images/create-pivot-grid-from-TOM-Explorer.png)

Puedes crear tantas Pivot Grids como quieras.

> [!IMPORTANT]
> La opción de crear un Pivot Grid solo está disponible mientras Tabular Editor 3 está conectado a una instancia de Analysis Services o al punto de conexión XMLA de Power BI / Fabric.

## Estructura del Pivot Grid

Pivot Grid se divide en 4 áreas: **Área de filtros**, **Área de columnas**, **Área de filas** y **Área de datos**. Puede arrastrar campos desde la **Lista de campos** o el **Explorador TOM** a estas áreas para crear una estructura de Pivot Grid. El **Área de datos** es donde coloca las medidas o los KPI, mientras que el **Área de filas** y el **Área de columnas** se utilizan para segmentar los datos por jerarquías y columnas. El **Área de filtros** se utiliza para filtrar los datos en función de los valores de las columnas o las jerarquías.

![Pivot Grid vacío resaltado](~/content/assets/images/empty-pivot-grid-highlighted.png)

La captura de pantalla anterior muestra una estructura de Pivot Grid vacía. Los 4 cuadros vacíos de la parte inferior de la Lista de campos representan las 4 áreas del Pivot Grid. Puede arrastrar campos desde la Lista de campos a estos cuadros de lista para crear una estructura de Pivot Grid. Como alternativa, puede arrastrar los campos directamente al Pivot Grid.

## Menú y barra de herramientas de Pivot Grid

De forma predeterminada, cuando una Pivot Grid es la ventana activa en Tabular Editor 3, están disponibles un menú y una barra de herramientas de **Pivot Grid**. El menú contiene las mismas acciones que la barra de herramientas.

![Barra de herramientas de Pivot Grid](~/content/assets/images/pivot-grid-toolbar.png)

![Menú de Pivot Grid](~/content/assets/images/pivot-grid-menu.png)

Estas acciones son:

- **Suplantación...**: Muestra un cuadro de diálogo que le permite especificar un rol o un usuario para suplantar a través del Pivot Grid. Esto resulta útil cuando desea probar el comportamiento de su modelo para diferentes usuarios o roles, como cuando se ha aplicado [RLS u OLS](xref:data-security-about) al modelo.
- **Actualizar**: Vuelve a ejecutar la consulta generada por el Pivot Grid. Esto resulta útil cuando la actualización automática está desactivada o si se han realizado cambios en el modelo fuera de Tabular Editor 3.
- **Actualización automática**: Activa o desactiva la actualización automática. Cuando la actualización automática está habilitada, Pivot Grid se actualizará automáticamente cada vez que guarde los cambios en el modelo, o cuando se complete una [operación de actualización de datos](xref:data-refresh-view).
- **Borrar filtros**: Borra todos los filtros del Pivot Grid.
- **Borrar**: Quita todos los campos del Pivot Grid.
- **Mostrar valores vacíos en columnas**: Activa o desactiva la visualización de valores vacíos en el Pivot Grid para los campos que se añaden al área de columnas del Pivot Grid.
- **Mostrar valores vacíos en filas**: Activa o desactiva si los valores vacíos deben mostrarse en el Pivot Grid, para los campos que se añaden al Área de Filas del Pivot Grid.
- **Lista de campos**: Activa o desactiva la lista de campos.

## Lista de campos

De forma predeterminada, la Lista de campos se muestra en el lado derecho del Pivot Grid. La lista de campos contiene todos los campos (medidas, KPI, columnas y jerarquías) que están disponibles en el modelo. Puede arrastrar campos de la Lista de campos al Pivot Grid para crear un diseño. También puedes arrastrar campos entre las diferentes áreas del Pivot Grid para reorganizar la estructura.

La propia Lista de campos se puede acoplar al lado izquierdo o derecho del Pivot Grid, por encima o por debajo, se puede ocultar o se puede desacoplar para que «flote» como una ventana independiente. Si tienes varias Pivot Grids abiertas, cada Pivot Grid tiene su propia lista de campos.

Si no desea que la lista de campos se muestre de forma predeterminada, desmarque la opción **Mostrar siempre lista de campos** en **Herramientas > Preferencias > Exploración de datos > Pivot Grid > Lista de campos**.

Puede cambiar el diseño predeterminado de la lista de campos en **Herramientas > Preferencias > Exploración de datos > Cuadrícula dinámica > Lista de campos > Diseño**. También puede cambiar el diseño de cualquier lista de campos haciendo clic con el botón derecho en un área vacía de la lista de campos y eligiendo el diseño deseado en el menú contextual.

![Ajustes de la lista de campos](~/content/assets/images/field-list-settings.png)

De forma predeterminada, cualquier campo que añada al Pivot Grid permanece visible en la Lista de campos. Si desea ocultar los campos que se añaden al Pivot Grid, puede desmarcar la opción **Mantener campos visibles** en **Herramientas > Preferencias > Exploración de datos > Pivot Grid > Lista de campos** (este comportamiento es similar al funcionamiento del Pivot Grid antes de Tabular Editor v. 3.16.0).

Si está trabajando en un modelo grande y complejo y espera que las medidas utilizadas en el Pivot Grid sean relativamente lentas, puede marcar la opción **Aplazar la actualización del diseño** en la parte inferior de la Lista de campos. Esto evitará que Pivot Grid actualice el diseño cada vez que añada o elimine un campo, lo que puede ser útil si tiene intención de realizar varios cambios en el diseño de Pivot Grid antes de actualizarlo. Pulse el botón **Actualizar** para aplicar los cambios al Pivot Grid.

> [!IMPORTANT]
> Las columnas sin una jerarquía de atributos (IsAvailableIn MDX = false) no se pueden usar en el Pivot Grid y no se muestran en la lista de campos.

## Personalización de Pivot Grids

### Añadir campos

Hay varias formas de añadir un campo a un Pivot Grid:

**Desde el Explorador TOM:**

- Haga clic derecho en una o más *medidas* y elija **Agregar a Pivot Grid**.
- Haga clic con el botón derecho en una *columna* o *jerarquía* y elija cualquiera de las opciones **Agregar a tabla dinámica** (elija entre filas, columnas o filtros).
- Si una medida, columna o jerarquía ya se muestra en el Pivot Grid, las opciones del botón derecho le permitirán **Quitar del Pivot Grid**. Además, verá opciones para mover columnas o jerarquías entre las diferentes áreas del Pivot Grid.
- Todas las opciones anteriores también están disponibles a través de los menús **Medida**, **Columna** y **Jerarquía** (respectivamente), cuando se seleccionan uno o más de dichos objetos en el Explorador TOM.
- Además de lo anterior, también puede arrastrar una o más medidas, columnas o jerarquías del Explorador TOM a las áreas de Pivot Grid.

![Añadir una jerarquía a Pivot Grid a través del Explorador TOM](~/content/assets/images/add-through-tom-explorer.png)

**Desde la lista de campos:**

- Arrastre un campo de la Lista de campos al Pivot Grid.
- Arrastre un campo de la Lista de Campos a los cuadros de lista de áreas situados en la parte inferior de la Lista de Campos para añadirlo al Pivot Grid.
- Haga clic con el botón derecho en un campo de la Lista de Campos para ver las opciones para agregarlo al Pivot Grid.
- Si un campo ya aparece en el Pivot Grid, el menú contextual que se abre al hacer clic con el botón derecho también tendrá una opción para quitar el campo o moverlo a un área diferente (solo campos de columna/jerarquía).
- Al hacer doble clic en un campo, este se agregará inmediatamente al Pivot Grid. Las medidas/KPI se añaden al Área de Datos, mientras que las columnas y las jerarquías se añaden al Área de Filtros.

![Añadir a través de la lista de campos](~/content/assets/images/add-through-field-list.png)

### Ajuste de campos

Después de agregar los campos al Pivot Grid, puede ajustar el ancho de las columnas para que se adapten mejor a su contenido. Al hacer doble clic en un separador de encabezado de columna, se ajustará automáticamente el ancho de la columna para que se adapte al contenido de la columna. También puede arrastrar el separador del encabezado de la columna para ajustar manualmente el ancho de la columna. Por último, puede usar las opciones del menú contextual **Ajustar al contenido** o **Establecer ancho...** haciendo clic con el botón derecho en el encabezado de la columna.

![Ajustar al contenido las columnas 2](~/content/assets/images/best-fit-columns-2.png)

Para aplicar un «Ajuste óptimo» o establecer un ancho específico en píxeles para todas las columnas del Pivot Grid simultáneamente, haga clic con el botón derecho en el encabezado «Valores» y seleccione la opción deseada en el menú contextual.

De forma predeterminada, los encabezados de campo se expanden verticalmente para adaptarse al nombre del campo. Para limitar los encabezados de campo a una sola fila, desmarque **Ajuste de línea en encabezados de campo** en **Herramientas > Preferencias > Exploración de datos > Cuadrícula dinámica > Encabezados de campo**.

Para cambiar el orden de los campos en el Pivot Grid, puede arrastrar los campos entre las diferentes áreas del Pivot Grid. También puedes arrastrar campos dentro de la misma área para cambiar su orden. Para quitar un campo del Pivot Grid, arrástrelo de nuevo a la Lista de campos o haga clic con el botón derecho en el campo y elija **Quitar del Pivot Grid** en el menú contextual.

Si quieres que las medidas se muestren en filas en lugar de en columnas, arrastra el campo «Valores» del área de columnas al área de filas.

### Reglas de visualización

Puede añadir reglas de visualización a las celdas de las tablas dinámicas, lo cual resulta útil para resaltar las celdas según sus valores, por ejemplo, para detectar mejor los valores atípicos. Para añadir reglas de visualización, haga clic con el botón derecho en cualquier celda del Área de Datos del Pivot Grid y elija qué reglas aplicar en el menú contextual (vea la captura de pantalla a continuación).

![Personalización de Pivot Grids](~/content/assets/images/customizing-pivot-grids.png)

## Conservar los diseños de Pivot Grid

Cuando cierre un Pivot Grid, Tabular Editor le pedirá que guarde el diseño del Pivot Grid. Si decide guardar el diseño, la próxima vez que abra la cuadrícula dinámica, se restaurará con el mismo diseño que tenía cuando la cerró. También puede guardar el diseño de un Pivot Grid manualmente pulsando (Ctrl+S) o utilizando la opción **Archivo > Guardar**, mientras Pivot Grid sea la ventana activa.

La extensión de archivo utilizada para guardar las estructuras de Pivot Grid es «.te3pivot». Se trata de un archivo json sencillo que especifica qué objetos del modelo se muestran en el Pivot Grid y en qué áreas se colocan. Se hace referencia a los objetos por su nombre y por su etiqueta de linaje (si existe), por lo que, por lo general, el diseño de Pivot Grid se puede restaurar incluso si el modelo se ha modificado desde que se guardó el diseño.

> [!NOTE]
> Puede abrir una estructura de Pivot Grid que se haya creado en un modelo diferente. Si el diseño utiliza campos que no existen en el modelo al que está conectado, aparece una advertencia y esos campos se eliminan del diseño. Lo mismo sucede cuando un Pivot Grid abierto se mantiene abierto y conectado a un modelo diferente, como se describe en [Cambiar de modelo](#switching-models). Para desactivar la advertencia, desmarque **Mostrar advertencia si Pivot Grid no coincide con el modelo** en **Herramientas > Preferencias > Exploración de datos > Pivot Grid**.

## Cambiar de modelo

Cuando abre un modelo diferente, los Pivot Grids abiertos permanecen abiertos y se conectan al nuevo modelo. Cada Pivot Grid conserva su estructura de campos, y cualquier campo que el nuevo modelo no contenga se elimina de la estructura. Cuando se eliminan campos, aparece una advertencia: «El modelo que se acaba de abrir no contiene todos los campos utilizados por este Pivot Grid. Los campos que faltan se han quitado de la estructura». Si el nuevo modelo no tiene datos para explorar, como un modelo cargado desde un archivo sin una base de datos de área de trabajo, Pivot Grid se vacía.

Si la opción **Actualización automática** está desactivada para un Pivot Grid, la cuadrícula mantiene su diseño y sus valores anteriores hasta que haga clic en **Actualizar** o abra su Lista de campos. En ese momento, se conecta al nuevo modelo y elimina los campos que faltan.

Si una Pivot Grid abierta tiene campos en su diseño, aparece la confirmación **Las Pivot Grids se volverán a vincular al nuevo modelo** antes de que se abra el nuevo modelo:

- **Sí** abre el nuevo modelo.
- **Sí, no volver a preguntar** abre el nuevo modelo y desactiva la preferencia **Mostrar advertencia si Pivot Grid no coincide con el modelo**, lo que desactiva tanto esta confirmación como la advertencia sobre los campos eliminados.
- **Cancelar** mantiene el modelo actual cargado con todos los documentos sin cambios.

Para conservar el diseño original, haga clic en **Cancelar** y guarde una copia del Pivot Grid con **Archivo > Guardar como** antes de cambiar de modelo.

Desmarque **Mantener las Pivot Grids abiertas cuando se abra un modelo diferente** en **Herramientas > Preferencias > Exploración de datos > Pivot Grid** para cerrar las Pivot Grids cuando abra un modelo diferente. La opción está seleccionada de forma predeterminada.

## Funciones adicionales

Pivot Grid tiene algunas funciones más que es útil conocer:

- Si hace clic con el botón derecho en un campo, tendrá la opción de **Ir a** ese campo. Esto hace que el Explorador TOM pase a primer plano, con el objeto de modelo equivalente seleccionado. En el caso de las medidas y las columnas calculadas, se resaltará el **Editor de expresiones**, con la expresión DAX de la medida mostrada.
- Si hace clic con el botón derecho en una celda del Pivot Grid, puede seleccionar la opción **Depurar este valor**. Esto iniciará el [**Depurador de DAX**](xref:dax-debugger) a partir de la medida y el contexto de filtro específicos que produjeron el valor de la celda.
- Mientras un Pivot Grid se está **actualizando**, ciertos elementos de la barra de herramientas están desactivados y las acciones del menú contextual no están disponibles temporalmente.

## Limitaciones y problemas conocidos

A continuación se muestra una lista de limitaciones y problemas conocidos con las Pivot Grids en Tabular Editor 3.16.0, que estamos trabajando para solucionar en futuras versiones:

- Las reglas de formato (como los conjuntos de iconos, las barras de datos, etc.) no se conservan correctamente al guardar una estructura de Pivot Grid como archivo «.te3pivot».
- Si abre un archivo «.te3pivot» en un modelo diferente al modelo desde el que se guardó el diseño, o cambia de modelo mientras está abierto un Pivot Grid guardado, los campos que no existan en el modelo actual se eliminarán del diseño. Si a continuación guarda (**Ctrl+S**), el archivo «.te3pivot» se sobrescribe sin esos campos.
- Las columnas que usan la propiedad **Agrupar por columnas** (incluidas las columnas de parámetros de campo) no se pueden agregar por sí solas al área de filas o al área de columnas. Si lo hace, se producirá el error «La columna X forma parte de una clave compuesta, pero no todas las columnas de la clave compuesta están incluidas en la expresión o en su expresión dependiente». Esta es una limitación general de los clientes MDX y también se produce cuando se utiliza una columna de este tipo en una tabla dinámica de Excel. Para evitarlo, agregue la columna Agrupar por relacionada al Pivot Grid *antes* de agregar la columna dependiente. Por ejemplo, si «[ProductKey]» está configurado como la columna «Agrupar por» de «[ProductName]», añada primero «[ProductKey]» al área de filas o al área de columnas y, a continuación, añada «[ProductName]».
- Aplicar una ordenación explícita ascendente o descendente a una columna del área de filas o del área de columnas ordena los valores alfabéticamente como cadenas, independientemente del tipo de datos de la columna. Las fechas con formato de fecha larga (por ejemplo, «4 de mayo de 2024») y los números enteros se ordenan lexicográficamente en lugar de cronológica o numéricamente. Esta es una limitación de la forma en que los clientes MDX ordenan, y se produce el mismo comportamiento en una tabla dinámica de Excel conectada al modelo. Para obtener un orden cronológico o numérico, confíe en el orden natural de la columna (no aplique un orden explícito) o utilice la propiedad **Ordenar por columna** en la columna del modelo para señalar una columna con un valor subyacente que se pueda ordenar.