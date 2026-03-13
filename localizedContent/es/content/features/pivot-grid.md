---
uid: pivot-grid
title: Pivot Grids
author: Daniel Otykier
updated: 2024-05-28
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
> La información de este artículo se aplica a Tabular Editor 3.16.0 o posterior. Asegúrese de estar usando la versión más reciente de Tabular Editor 3 para aprovechar las nuevas funciones y mejoras.

Al desarrollar modelos semánticos, a menudo puede querer comprobar que sus expresiones DAX devuelven los valores esperados. Tradicionalmente, esto se hacía con herramientas cliente como Excel o Power BI. Con Tabular Editor 3, puede usar **Pivot Grids**, que se comportan de forma muy similar a las conocidas tablas dinámicas de Excel. El Pivot Grid le permite crear rápidamente vistas resumidas de los datos de su modelo, lo que le permite probar el comportamiento de sus medidas DAX al filtrar y segmentar por distintas columnas y jerarquías.

![Ejemplo de Pivot Grid](~/content/assets/images/pivot-grid-example.png)

La captura de pantalla anterior muestra un Pivot Grid con dos medidas, `[Total Net Order Value]` y `[Net Orders]`, segmentado horizontalmente por Año, filtrado a 2021 y 2022, y verticalmente por la jerarquía de productos. Los usuarios de Tabular Editor 3 pueden usar esta función para asegurarse de que las expresiones DAX detrás de las medidas funcionan como se espera y para validar rápidamente los datos del modelo.

De forma predeterminada, el Pivot Grid se actualiza automáticamente cada vez que guarda cambios en el modelo semántico (Ctrl+S). Así, puede iterar rápidamente sobre sus expresiones DAX y ver los resultados en el Pivot Grid sin tener que esperar a que el modelo se actualice: cambie sus medidas, guarde el modelo y verá la nueva definición reflejada directamente en el Pivot Grid. Un buen flujo de trabajo consiste en abrir el Pivot Grid en una ventana independiente mientras trabaja en expresiones DAX en el **Editor de expresiones** o mediante un **Script DAX**.

> [!TIP]
> Algunas aclaraciones sobre la terminología:
>
> - **Campos** hace referencia a las medidas, KPI, columnas y jerarquías del modelo. En otras palabras, todo lo que se pueda arrastrar al Pivot Grid.
> - Los **KPIs** son un tipo especial de medida que se puede crear en Tabular Editor. Se muestran en el Pivot Grid igual que las medidas, pero con un icono especial para indicar que son KPIs. Cada KPI puede tener hasta 3 valores diferentes (objetivo, tendencia y estado), que se muestran por separado en el Pivot Grid.
> - Las **columnas** del Pivot Grid (como en el término "Área de columnas") no deben confundirse con las columnas del modelo. En el Pivot Grid, las columnas se usan para segmentar los datos horizontalmente, mientras que las filas se usan para segmentar los datos verticalmente.
> - Las **celdas** del Pivot Grid son los puntos de datos individuales donde se cruzan una fila y una columna. Cada celda contiene un único valor, que es el resultado de la expresión DAX de la medida específica, evaluada bajo el contexto de filtro producido por los valores del _Área de filas_ y el _Área de columnas_, en combinación con cualquier filtro aplicado a los campos del _Área de filtros_.

> [!NOTE]
> Los desarrolladores con experiencia en modelos multidimensionales pueden estar más familiarizados con los términos _Dimensiones_ y _Atributos_. En los modelos semánticos, las _Dimensiones_ se representan mediante _tablas_ del modelo, y los _Atributos_ se representan mediante _columnas_ del modelo. Las _jerarquías_ en un modelo semántico son simplemente una forma de agrupar columnas, como en una jerarquía de calendario: Año > Trimestre > Mes > Día. En los modelos multidimensionales, estas jerarquías antes se llamaban _Jerarquías de atributos_ o _Jerarquías definidas por el usuario_.

## Crear un Pivot Grid

Puedes crear un Pivot Grid nuevo y vacío desde la opción de menú **Archivo > Nuevo > Nuevo Pivot Grid**. Como alternativa, selecciona una o varias medidas en el **Explorador TOM**, haz clic con el botón derecho o ve al menú **Medida** y selecciona **Agregar al Pivot Grid** para crear un nuevo Pivot Grid con las medidas seleccionadas.

![Crear un Pivot Grid desde el Explorador TOM](~/content/assets/images/create-pivot-grid-from-TOM-Explorer.png)

Puedes crear tantos Pivot Grid como quieras.

> [!IMPORTANT]
> La opción de crear un Pivot Grid solo está disponible mientras Tabular Editor 3 esté conectado a una instancia de Analysis Services o al punto de conexión XMLA de Power BI / Fabric.

## Diseño del Pivot Grid

El Pivot Grid se divide en 4 áreas: **Área de filtros**, **Área de columnas**, **Área de filas** y **Área de datos**. Puedes arrastrar campos desde la **Lista de campos** o el **Explorador TOM** a estas áreas para crear un diseño de Pivot Grid. El **Área de datos** es donde colocas medidas o KPIs, mientras que el **Área de filas** y el **Área de columnas** se usan para segmentar los datos por jerarquías y columnas. El **Área de filtros** se usa para filtrar los datos en función de los valores de columnas o jerarquías.

![Pivot Grid vacío resaltado](~/content/assets/images/empty-pivot-grid-highlighted.png)

La captura de pantalla anterior muestra un diseño de Pivot Grid vacío. Los 4 cuadros vacíos en la parte inferior de la Lista de campos representan las 4 áreas del Pivot Grid. Puedes arrastrar campos de la Lista de campos a estos cuadros de lista para crear un diseño de la Pivot Grid. También puedes arrastrar campos directamente a la Pivot Grid.

## Menú y barra de herramientas de Pivot Grid

De forma predeterminada, cuando la Pivot Grid es la ventana activa en Tabular Editor 3, están disponibles un menú y una barra de herramientas de **Pivot Grid**. El menú contiene las mismas acciones que la barra de herramientas.

![Barra de herramientas de Pivot Grid](~/content/assets/images/pivot-grid-toolbar.png)

![Menú de Pivot Grid](~/content/assets/images/pivot-grid-menu.png)

Estas acciones son:

- **Suplantación...**: Muestra un cuadro de diálogo que te permite especificar un rol o usuario para suplantar a través de la Pivot Grid. Esto es útil cuando quieres probar el comportamiento de tu modelo para distintos usuarios o roles, por ejemplo, cuando se ha aplicado [RLS u OLS](xref:data-security-about) al modelo.
- **Actualizar**: Vuelve a ejecutar la consulta generada por la Pivot Grid. Esto es útil cuando la actualización automática está deshabilitada o si se han realizado cambios en el modelo fuera de Tabular Editor 3.
- **Actualización automática**: Activa o desactiva la actualización automática. Cuando la actualización automática está habilitada, la Pivot Grid se actualizará automáticamente cada vez que guardes cambios en el modelo o cuando finalice una [operación de actualización de datos](xref:data-refresh-view).
- **Borrar filtros**: Borra todos los filtros de la Pivot Grid.
- **Borrar**: Quita todos los campos de la Pivot Grid.
- **Mostrar valores vacíos en columnas**: Activa o desactiva la visualización de valores vacíos en la Pivot Grid para los campos que se agreguen al área de columnas de la Pivot Grid.
- **Mostrar valores vacíos en filas**: Activa o desactiva la visualización de valores vacíos en la Pivot Grid para los campos que se agreguen al área de filas de la Pivot Grid.
- **Lista de campos**: Activa o desactiva la lista de campos.

## Lista de campos

De forma predeterminada, la Lista de campos se muestra a la derecha de la Pivot Grid. La Lista de campos contiene todos los campos (medidas, KPIs, columnas y jerarquías) disponibles en el modelo. Puedes arrastrar campos de la Lista de campos a la Pivot Grid para crear un diseño. También puedes arrastrar campos entre las distintas áreas de la Pivot Grid para reorganizar el diseño.

La Lista de campos se puede acoplar al lado izquierdo o derecho de la Pivot Grid, encima o debajo; también se puede ocultar o desacoplar para que "flote" como una ventana independiente. Si tienes varias Pivot Grids abiertas, cada Pivot Grid tiene su propia Lista de campos.

Si prefieres que la Lista de campos no se muestre de forma predeterminada, desmarca la opción **Mostrar siempre la lista de campos** en **Herramientas > Preferencias > Exploración de datos > Pivot Grid > Lista de campos**.

Puedes cambiar el diseño predeterminado de la Lista de campos en **Herramientas > Preferencias > Exploración de datos > Pivot Grid > Lista de campos > Diseño**. También puedes cambiar el diseño de cualquier Lista de campos: haz clic con el botón derecho en un área vacía de la Lista de campos y selecciona el diseño que desees en el menú contextual.

![Configuración de la Lista de campos](~/content/assets/images/field-list-settings.png)

De forma predeterminada, cualquier campo que agregues al Pivot Grid sigue siendo visible en la Lista de campos. Si quieres ocultar los campos que se agregan al Pivot Grid, puedes desmarcar la opción **Mantener los campos visibles** en **Herramientas > Preferencias > Exploración de datos > Pivot Grid > Lista de campos** (este comportamiento es similar a como funcionaba Pivot Grid antes de Tabular Editor v. 3.16.0).

Si trabajas con un modelo grande y complejo, y esperas que las medidas usadas en el Pivot Grid tarden relativamente en calcularse, puedes activar la opción **Aplazar actualización del diseño** en la parte inferior de la Lista de campos. Esto evita que el Pivot Grid actualice el diseño cada vez que agregas o quitas un campo, lo que puede ser útil si quieres hacer varios cambios en el diseño del Pivot Grid antes de actualizarlo. Pulsa el botón **Actualizar** para aplicar los cambios al Pivot Grid.

> [!IMPORTANT]
> Las columnas sin una jerarquía de atributos (IsAvailableIn MDX = false) no se pueden usar en el Pivot Grid y no se muestran en la Lista de campos.

## Personalización de Pivot Grids

### Agregar campos

Hay varias formas de agregar un campo a un Pivot Grid:

**Desde el Explorador TOM:**

- Haz clic con el botón derecho en una o varias _medidas_ y elige **Agregar al Pivot Grid**.
- Haz clic con el botón derecho en una _columna_ o _jerarquía_ y elige cualquiera de las opciones de **Agregar a tabla dinámica** (elige entre filas, columnas o filtros).
- Si una medida, columna o jerarquía ya se muestra en el Pivot Grid, las opciones al hacer clic con el botón derecho te permitirán **Quitar del Pivot Grid**. además, verás opciones para mover columnas o jerarquías entre las distintas áreas del Pivot Grid.
- Todas las opciones anteriores también están disponibles en los menús **Medida**, **Columna** y **Jerarquía** (respectivamente), cuando se seleccionan uno o varios de estos objetos en el Explorador TOM.
- Además de lo anterior, también puedes arrastrar una o varias medidas, columnas o jerarquías desde el Explorador TOM a las áreas del Pivot Grid.

![Agregar jerarquía a Pivot Grid desde el Explorador TOM](~/content/assets/images/add-through-tom-explorer.png)

**Desde la Lista de campos:**

- Arrastra un campo desde la Lista de campos al Pivot Grid.
- Arrastra un campo desde la Lista de campos a los cuadros de lista de las áreas, en la parte inferior de la Lista de campos, para agregarlo al Pivot Grid.
- Haz clic con el botón derecho en un campo de la Lista de campos para ver las opciones para añadirlo al Pivot Grid.
- Si un campo ya se muestra en el Pivot Grid, el menú contextual al hacer clic con el botón derecho también incluirá una opción para quitar el campo o moverlo a otra área (solo para campos de columna/jerarquía).
- Al hacer doble clic en un campo, este se añade inmediatamente al Pivot Grid. Las medidas y los KPI se añaden al Área de datos, mientras que las columnas y las jerarquías se añaden al Área de filtros.

![Agregar mediante la Lista de campos](~/content/assets/images/add-through-field-list.png)

### Ajuste de campos

Después de añadir campos al Pivot Grid, puedes ajustar el ancho de las columnas para adaptarlo mejor a su contenido. Al hacer doble clic en el separador del encabezado de una columna, el ancho de la columna se ajustará automáticamente para adaptarse a su contenido. También puedes arrastrar el separador del encabezado de la columna para ajustar el ancho manualmente. Por último, puedes usar las opciones del menú contextual **Mejor ajuste** o **Establecer ancho...** haciendo clic con el botón derecho en el encabezado de la columna.

![Mejor ajuste de columnas 2](~/content/assets/images/best-fit-columns-2.png)

Para aplicar un "Mejor ajuste" o establecer un ancho específico en píxeles para todas las columnas del Pivot Grid al mismo tiempo, haz clic con el botón derecho en el encabezado "Valores" y selecciona la opción deseada en el menú contextual.

De forma predeterminada, los encabezados de campo se expandirán verticalmente para adaptarse al contenido del nombre del campo. Si quieres limitar la altura de los encabezados de campo a una sola fila, puedes desactivar la opción **Ajustar texto en encabezados de campo** en **Herramientas > Preferencias > Pivot Grid > Encabezados de campo**.

Para cambiar el orden de los campos en el Pivot Grid, puedes arrastrar campos entre las distintas áreas del Pivot Grid. También puedes arrastrar campos dentro de la misma área para cambiar su orden. Para quitar un campo del Pivot Grid, arrástralo de vuelta a la Lista de campos o haz clic con el botón derecho en el campo y elige **Quitar del Pivot Grid** en el menú contextual.

Si quieres que las medidas se muestren en filas en lugar de en columnas, arrastra el campo "Valores" del Área de columnas al Área de filas.

### Reglas de visualización

Puedes añadir reglas de visualización a las celdas de los Pivot Grid, lo cual resulta útil para resaltarlas en función de sus valores; por ejemplo, para detectar mejor los valores atípicos. Para añadir reglas de visualización, haz clic con el botón derecho en cualquier celda del Área de datos del Pivot Grid y elige qué reglas aplicar desde el menú contextual (consulta la captura de pantalla a continuación).

![Personalizar Pivot Grid](~/content/assets/images/customizing-pivot-grids.png)

## Persistencia de diseños del Pivot Grid

Al cerrar un Pivot Grid, Tabular Editor te pedirá que guardes el diseño del Pivot Grid. Si decides guardar el diseño, la próxima vez que abras el Pivot Grid se restaurará con el mismo diseño que tenía cuando lo cerraste. También puedes guardar el diseño de un Pivot Grid manualmente pulsando (Ctrl+S) o usando la opción **Archivo > Guardar**, mientras el Pivot Grid sea la ventana activa.

La extensión de archivo usada para guardar diseños del Pivot Grid es `.te3pivot`. Es un archivo json sencillo que especifica qué objetos del modelo se muestran en el Pivot Grid y en qué áreas se colocan. Se hace referencia a los objetos por su nombre y su etiqueta de linaje (si existe), por lo que, por lo general, el diseño de Pivot Grid puede restaurarse incluso si el modelo se ha modificado desde que se guardó el diseño.

> [!NOTE]
> Es posible abrir un diseño de Pivot Grid que se creó en un modelo diferente, pero tenga en cuenta que los campos del diseño pueden no existir en el modelo al que está conectado actualmente. En esos casos, el Pivot Grid mostrará un mensaje de advertencia y se quitarán del diseño los campos que no existan en el modelo. El mensaje de advertencia se puede desactivar en **Herramientas > Preferencias > Exploración de datos > Pivot Grid > Mostrar advertencia si Pivot Grid no coincide con el modelo**.

## Características adicionales

El Pivot Grid tiene algunas funciones más que conviene conocer:

- Si hace clic con el botón derecho en un campo, tendrá la opción **Ir a** ese campo. Esto pone el Explorador TOM en primer plano, con el objeto de modelo equivalente seleccionado. Para las medidas y las columnas calculadas, se enfocará el **Editor de expresiones**, en el que se mostrará la expresión DAX de la medida.
- Si hace clic con el botón derecho en una celda del Pivot Grid, puede seleccionar la opción **Depurar este valor**. Esto iniciará el [**DAX Debugger**](xref:dax-debugger) a partir de la medida específica y el contexto de filtro que generaron el valor de la celda.
- Mientras un Pivot Grid se está **actualizando**, algunos elementos de la barra de herramientas se deshabilitan y las acciones del menú contextual no están disponibles temporalmente.

## Limitaciones y problemas conocidos

A continuación se muestra una lista de limitaciones y problemas conocidos de los Pivot Grid en Tabular Editor 3.16.0, que estamos trabajando para resolver en próximas versiones:

- Reglas de formato (como conjuntos de iconos, barras de datos, etc.) no se conservan correctamente al guardar un diseño de Pivot Grid como archivo `.te3pivot`.
- Si abre un archivo .te3pivot en un modelo distinto de aquel del que se guardó el diseño, los campos que no existan en el modelo actual se eliminarán del diseño. Al pulsar Guardar (Ctrl+S), se guardará el diseño con esos campos ya eliminados. Es posible que cambiemos este comportamiento en una versión futura para que el archivo .te3pivot no se sobrescriba sin una confirmación explícita.