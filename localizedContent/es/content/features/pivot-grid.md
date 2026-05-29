---
uid: pivot-grid
title: Pivot Grid
author: Daniel Otykier
updated: 2026-05-27
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

# Pivot Grid

> [!NOTE]
> La información de este artículo se aplica a Tabular Editor 3.16.0 o versiones posteriores. Asegúrate de estar usando la versión más reciente de Tabular Editor 3 para aprovechar las nuevas funciones y mejoras.

Al desarrollar modelos semánticos, a menudo querrás comprobar que tus expresiones DAX devuelven los valores esperados. Tradicionalmente, esto se hacía con herramientas cliente como Excel o Power BI. Con Tabular Editor 3, puedes usar **Pivot Grids**, que se comportan de forma muy similar a las conocidas tablas dinámicas de Excel. El Pivot Grid te permite crear rápidamente vistas resumidas de los datos de tu modelo y probar el comportamiento de tus medidas DAX al filtrar y segmentar por distintas columnas y jerarquías.

![Ejemplo de Pivot Grid](~/content/assets/images/pivot-grid-example.png)

La captura de pantalla anterior muestra un Pivot Grid que contiene dos medidas, `[Total Net Order Value]` y `[Net Orders]`, segmentado horizontalmente por Año, filtrado a 2021 y 2022, y verticalmente por la jerarquía de productos. Los usuarios de Tabular Editor 3 pueden usar esta característica para asegurarse de que las expresiones DAX de las medidas funcionan como se espera y para validar rápidamente los datos del modelo.

De forma predeterminada, el Pivot Grid se actualiza automáticamente cada vez que guardas cambios en el modelo semántico (Ctrl+S). Así, puedes iterar rápidamente sobre tus expresiones DAX y ver los resultados en el Pivot Grid sin tener que esperar a que se actualice el modelo: cambia tus medidas, guarda el modelo y verás directamente la nueva definición de la medida reflejada en el Pivot Grid. Un buen flujo de trabajo es abrir el Pivot Grid en una ventana independiente mientras trabajas en expresiones DAX en el **Editor de expresiones** o con un **Script DAX**.

> [!TIP]
> Algunas aclaraciones sobre la terminología:
>
> - El término **Campos** se refiere a las medidas, los KPI, las columnas y las jerarquías del modelo. En otras palabras, cualquier elemento que se pueda arrastrar al Pivot Grid.
> - **Los KPI** son un tipo especial de medida que puedes crear en Tabular Editor. Se muestran en el Pivot Grid igual que las medidas, pero con un icono especial que indica que son KPI. Cada KPI puede tener hasta 3 valores diferentes (objetivo, tendencia y estado), que se muestran por separado en el Pivot Grid.
> - **Las columnas** en el Pivot Grid (como en el término "Área de columnas") no deben confundirse con las columnas del modelo. En el Pivot Grid, las columnas se usan para segmentar los datos horizontalmente, mientras que las filas se usan para segmentarlos verticalmente.
> - **Las celdas** del Pivot Grid son los puntos de datos individuales donde se cruzan una fila y una columna. Cada celda contiene un único valor, que es el resultado de la expresión DAX de la medida concreta, evaluada en el contexto de filtro generado por los valores del _Área de filas_ y del _Área de columnas_, en combinación con cualquier filtro aplicado a los campos del _Área de filtros_.

> [!NOTE]
> Los desarrolladores con experiencia en modelos multidimensionales pueden estar más familiarizados con los términos _Dimensiones_ y _Atributos_. En los modelos semánticos, las _Dimensiones_ se representan mediante _tablas_ del modelo, y los _Atributos_ mediante _columnas_ del modelo. Las _Jerarquías_ de un modelo semántico son simplemente una forma de agrupar columnas, como en una jerarquía de calendario: Año > Trimestre > Mes > Día. Estas jerarquías solían llamarse _Jerarquías de atributos_ o _Jerarquías definidas por el usuario_ en los modelos multidimensionales.

## Crear un Pivot Grid

Puedes crear un nuevo Pivot Grid vacío mediante la opción de menú **Archivo > Nuevo > Nuevo Pivot Grid**. Como alternativa, selecciona una o más medidas en el **Explorador TOM** y haz clic con el botón derecho, o ve al menú **Medida** y selecciona **Agregar a Pivot Grid** para crear un nuevo Pivot Grid con las medidas seleccionadas.

![Crear Pivot Grid desde el Explorador TOM](~/content/assets/images/create-pivot-grid-from-TOM-Explorer.png)

Puedes crear tantos Pivot Grid como quieras.

> [!IMPORTANT]
> La opción para crear un Pivot Grid solo está disponible mientras Tabular Editor 3 esté conectado a una instancia de Analysis Services o al punto de conexión XMLA de Power BI / Fabric.

## Diseño del Pivot Grid

El Pivot Grid se divide en 4 áreas: **Área de filtro**, **Área de columnas**, **Área de filas** y **Área de datos**. Puedes arrastrar campos desde la **Lista de campos** o el **Explorador TOM** a estas áreas para crear un diseño de Pivot Grid. El **Área de datos** es donde se colocan las medidas o los KPI, mientras que el **Área de filas** y el **Área de columnas** se usan para segmentar los datos por jerarquías y columnas. El **Área de filtro** se usa para filtrar los datos en función de los valores de columnas o jerarquías.

![Pivot Grid vacío resaltado](~/content/assets/images/empty-pivot-grid-highlighted.png)

La captura de pantalla anterior muestra un diseño de Pivot Grid vacío. Los 4 cuadros vacíos de la parte inferior de la Lista de campos representan las 4 áreas del Pivot Grid. Puedes arrastrar campos desde la Lista de campos a estos cuadros de lista para crear un diseño de Pivot Grid. Como alternativa, puedes arrastrar campos directamente al Pivot Grid.

## Menú y barra de herramientas del Pivot Grid

De forma predeterminada, cuando un Pivot Grid es la ventana activa en Tabular Editor 3, están disponibles un menú **Pivot Grid** y una barra de herramientas. El menú contiene las mismas acciones que la barra de herramientas.

![Barra de herramientas de Pivot Grid](~/content/assets/images/pivot-grid-toolbar.png)

![Menú de Pivot Grid](~/content/assets/images/pivot-grid-menu.png)

Estas acciones son:

- **Suplantación...**: Muestra un cuadro de diálogo que te permite especificar un rol o un usuario que quieres suplantar a través del Pivot Grid. Esto es útil cuando quieres probar el comportamiento del modelo para distintos usuarios o roles, por ejemplo, cuando se ha aplicado [RLS u OLS](xref:data-security-about) al modelo.
- **Actualizar**: Vuelve a ejecutar la consulta generada por el Pivot Grid. Esto es útil cuando la actualización automática está desactivada o si se han realizado cambios en el modelo fuera de Tabular Editor 3.
- **Actualización automática**: Activa o desactiva la actualización automática. Cuando la actualización automática está activada, el Pivot Grid se actualizará automáticamente cada vez que guardes cambios en el modelo o cuando finalice una [operación de actualización de datos](xref:data-refresh-view).
- **Borrar filtros**: Borra todos los filtros del Pivot Grid.
- **Borrar**: Elimina todos los campos del Pivot Grid.
- **Mostrar valores vacíos en columnas**: Activa o desactiva la visualización de valores vacíos en el Pivot Grid para los campos que se agregan a su área de columnas.
- **Mostrar valores vacíos en filas**: Activa o desactiva la visualización de valores vacíos en el Pivot Grid para los campos que se agregan a su área de filas.
- **Lista de campos**: Muestra u oculta la lista de campos.

## Lista de campos

De forma predeterminada, la Lista de campos se muestra a la derecha del Pivot Grid. La Lista de campos contiene todos los campos (medidas, KPI, columnas y jerarquías) que están disponibles en el modelo. Puedes arrastrar campos desde la Lista de campos al Pivot Grid para crear una disposición. También puedes arrastrar campos entre las distintas áreas del Pivot Grid para reorganizar la disposición.

La propia Lista de campos puede acoplarse al lado izquierdo o derecho del Pivot Grid, arriba o abajo; también puede ocultarse o desacoplarse para que "flote" como una ventana independiente. Si tienes varios Pivot Grid abiertos, cada Pivot Grid tiene su propia Lista de campos.

Si no quieres que la Lista de campos se muestre de forma predeterminada, desactiva la opción **Mostrar siempre la lista de campos** en **Herramientas > Preferencias > Exploración de datos > Pivot Grid > Lista de campos**.

Puedes cambiar la disposición predeterminada de la Lista de campos en **Herramientas > Preferencias > Exploración de datos > Pivot Grid > Lista de campos > Disposición**. También puedes cambiar la disposición de cualquier lista de campos haciendo clic con el botón derecho en un área vacía de la Lista de campos y eligiendo la disposición deseada en el menú contextual.

![Configuración de la lista de campos](~/content/assets/images/field-list-settings.png)

De forma predeterminada, cualquier campo que agregues al Pivot Grid permanece visible en la Lista de campos. Si quieres ocultar los campos que se agregan al Pivot Grid, puedes desactivar la opción **Mantener los campos visibles** en **Herramientas > Preferencias > Exploración de datos > Pivot Grid > Lista de campos** (este comportamiento es similar a cómo funcionaba el Pivot Grid antes de Tabular Editor v. 3.16.0).

Si estás trabajando en un modelo grande y complejo, y esperas que las medidas usadas en el Pivot Grid sean relativamente lentas, puedes activar la opción **Aplazar la actualización del diseño** en la parte inferior de la lista de campos. Esto evita que el Pivot Grid actualice el diseño cada vez que agregas o quitas un campo, lo que puede ser útil si piensas hacer varios cambios en el diseño del Pivot Grid antes de actualizarlo. Haz clic en el botón **Actualizar** para aplicar los cambios al Pivot Grid.

> [!IMPORTANT]
> Las columnas sin jerarquía de atributos (IsAvailableIn MDX = false) no se pueden usar en el Pivot Grid y no se muestran en la Lista de campos.

## Personalización de Pivot Grids

### Agregar campos

Hay varias formas de agregar un campo al Pivot Grid:

**Desde el Explorador TOM:**

- Haz clic con el botón derecho en una o varias _medidas_ y elige **Agregar al Pivot Grid**.
- Haz clic con el botón derecho en una _columna_ o _jerarquía_ y elige cualquiera de las opciones de **Agregar al Pivot Grid** (filas, columnas o filtros).
- Si una medida, columna o jerarquía ya se muestra en el Pivot Grid, las opciones al hacer clic con el botón derecho te permitirán **Quitar del Pivot Grid**. además, verás opciones para mover columnas o jerarquías entre las distintas áreas del Pivot Grid.
- Todas las opciones anteriores también están disponibles en los menús **medida**, **Columna** y **Jerarquía** (respectivamente) cuando seleccionas uno o varios objetos de ese tipo en el Explorador TOM.
- Además de lo anterior, también puedes arrastrar una o varias medidas, columnas o jerarquías desde el Explorador TOM hasta las áreas del Pivot Grid.

![Agregar jerarquía al Pivot Grid desde el Explorador TOM](~/content/assets/images/add-through-tom-explorer.png)

**Desde la Lista de campos:**

- Arrastra un campo desde la Lista de campos hasta el Pivot Grid.
- Arrastra un campo desde la Lista de campos hasta los cuadros de lista de áreas, en la parte inferior de la Lista de campos, para agregarlo al Pivot Grid.
- Haz clic con el botón derecho en un campo de la Lista de campos para ver opciones que permiten agregarlo al Pivot Grid.
- Si un campo ya se muestra en el Pivot Grid, el menú contextual que aparece al hacer clic con el botón derecho también incluirá una opción para quitar el campo o moverlo a otra área (solo para campos de columna o jerarquía).
- Al hacer doble clic en un campo, se agregará inmediatamente al Pivot Grid. Las medidas y los KPI se agregan al Área de datos, mientras que las columnas y las jerarquías se agregan al Área de filtros.

![Agregar desde la Lista de campos](~/content/assets/images/add-through-field-list.png)

### Ajustar campos

Después de agregar campos al Pivot Grid, puedes ajustar el ancho de las columnas para adaptarlo mejor a su contenido. Al hacer doble clic en el separador del encabezado de una columna, el ancho de la columna se ajustará automáticamente al contenido. También puedes arrastrar el separador del encabezado de la columna para ajustar manualmente el ancho de la columna. Por último, puedes usar las opciones **Ajuste óptimo** o **Establecer ancho...** del menú contextual haciendo clic con el botón derecho en el encabezado de la columna.

![Columnas con ajuste óptimo 2](~/content/assets/images/best-fit-columns-2.png)

Para aplicar un "Ajuste óptimo" o establecer un ancho específico en píxeles para todas las columnas del Pivot Grid al mismo tiempo, haz clic con el botón derecho en el encabezado "Valores" y selecciona la opción deseada en el menú contextual.

De forma predeterminada, los encabezados de campo se expanden verticalmente para ajustarse al contenido del nombre del campo. Si quieres limitar la altura de los encabezados de campo a una sola fila, puedes desactivar la opción **Ajustar texto en encabezados de campo** en **Herramientas > Preferencia > Pivot Grid > Encabezados de campo**.

Para cambiar el orden de los campos en el Pivot Grid, puedes arrastrarlos entre las distintas áreas del Pivot Grid. También puedes arrastrar campos dentro de la misma área para cambiar su orden. Para quitar un campo del Pivot Grid, arrástralo de vuelta a la Lista de campos o haz clic con el botón derecho en el campo y elige **Quitar del Pivot Grid** en el menú contextual.

Si quieres que las medidas se muestren en filas en lugar de en columnas, arrastra el campo "Valores" del Área de columnas al Área de filas.

### Reglas de visualización

Puedes agregar reglas de visualización a las celdas de los Pivot Grids, lo que resulta útil para resaltarlas en función de sus valores; por ejemplo, para detectar mejor los valores atípicos. Para agregar reglas de visualización, haz clic con el botón derecho en cualquier celda del Área de datos del Pivot Grid y elige las reglas que desees aplicar en el menú contextual (consulta la siguiente captura de pantalla).

![Personalización de Pivot Grids](~/content/assets/images/customizing-pivot-grids.png)

## Conservar diseños de Pivot Grid

Al cerrar un Pivot Grid, Tabular Editor te pedirá que guardes el diseño del Pivot Grid. Si decides guardar el diseño, la próxima vez que abras el Pivot Grid se restaurará con el mismo diseño que tenía al cerrarlo. También puedes guardar manualmente el diseño de un Pivot Grid pulsando (Ctrl+S) o usando la opción **Archivo > Guardar**, mientras el Pivot Grid es la ventana activa.

La extensión de archivo que se usa para guardar diseños de Pivot Grid es `.te3pivot`. Se trata de un archivo json sencillo que especifica qué objetos del modelo se muestran en el Pivot Grid y en qué áreas se ubican. Los objetos se referencian por su nombre y su etiqueta de linaje (si existe), por lo que el diseño del Pivot Grid, por lo general, puede restaurarse incluso si el modelo se ha modificado desde que se guardó el diseño.

> [!NOTE]
> Es posible abrir un diseño de Pivot Grid que se haya creado en otro modelo, pero ten en cuenta que los campos del diseño pueden no existir en el modelo al que estás conectado actualmente. En esos casos, el Pivot Grid mostrará un mensaje de advertencia y todos los campos que no existan en el modelo se quitarán del diseño. Puedes desactivar el mensaje de advertencia en **Herramientas > Preferencia > Exploración de datos > Pivot Grid > Mostrar advertencia si Pivot Grid no coincide con el modelo**.

## Funciones adicionales

El Pivot Grid tiene algunas funciones adicionales que es útil conocer:

- Si haces clic con el botón derecho en un campo, tendrás la opción de **Ir a** ese campo. Esto llevará el foco al Explorador TOM, con el objeto del modelo equivalente seleccionado. En el caso de las medidas y las columnas calculadas, el **Editor de expresiones** pasará a primer plano y se mostrará la expresión DAX correspondiente.
- Si haces clic con el botón derecho en una celda del Pivot Grid, puedes seleccionar la opción **Depurar este valor**. Esto iniciará el [**DAX Debugger**](xref:dax-debugger) a partir de la medida concreta y del contexto de filtro que produjeron el valor de la celda.
- Mientras un Pivot Grid se está **actualizando**, algunos elementos de la barra de herramientas se deshabilitan y las acciones del menú contextual dejan de estar disponibles temporalmente.

## Limitaciones y problemas conocidos

A continuación tienes una lista de las limitaciones y los problemas conocidos de los Pivot Grid en Tabular Editor 3.16.0 que estamos trabajando para corregir en versiones futuras:

- Las reglas de formato (como conjuntos de iconos, barras de datos, etc.) no se conservan correctamente al guardar un diseño de Pivot Grid como archivo `.te3pivot`.
- Si abres un archivo .te3pivot en un modelo distinto de aquel del que se guardó el diseño, los campos que no existan en el modelo actual se eliminarán del diseño. Al pulsar Guardar (Ctrl+S), se guardará el diseño con esos campos eliminados. Es posible que cambiemos este comportamiento en una versión futura para que el archivo .te3pivot no se sobrescriba sin una confirmación explícita.
- Las columnas que usan la propiedad **Group By Columns** (incluidas las columnas de parámetros de campo) no se pueden agregar por sí solas al Área de filas ni al Área de columnas. Si lo haces, se producirá el error _"Column X is part of a composite key, but not all columns of the composite key are included in the expression or its dependent expression"_. Esta es una limitación general de los clientes MDX y también se produce al usar una columna de este tipo en una tabla dinámica de Excel. Para evitarlo, agrega la columna Group By Column relacionada al Pivot Grid _antes_ de agregar la columna dependiente. Por ejemplo, si `[ProductKey]` está configurado como la Group By Column de `[ProductName]`, agrega primero `[ProductKey]` al Área de filas o al Área de columnas y, después, agrega `[ProductName]`.
- Al aplicar una ordenación ascendente o descendente explícita a una columna del Área de filas o del Área de columnas, los valores se ordenan alfabéticamente como cadenas, independientemente del tipo de datos de la columna. Las fechas con formato de fecha larga (por ejemplo, "4 de mayo de 2024") y los enteros se ordenan lexicográficamente en lugar de cronológicamente o numéricamente. Esta es una limitación de cómo ordenan los clientes MDX, y el mismo comportamiento se produce en una tabla dinámica de Excel conectada al modelo. Para obtener un orden cronológico o numérico, confía en la ordenación natural de la columna (no apliques una ordenación explícita) o usa la propiedad **Ordenar por columna** de la columna del modelo para que apunte a otra columna con un valor subyacente que se pueda ordenar.