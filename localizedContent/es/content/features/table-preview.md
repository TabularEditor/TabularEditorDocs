---
uid: table-preview
title: Vista previa de tabla
author: Morten Lønskov
updated: 2026-09-23
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
# Vista previa de tabla

Una **vista previa de tabla** muestra las filas de una tabla sin necesidad de escribir una consulta. Haga clic con el botón derecho en una tabla de la @tom-explorer-view y elija **Vista previa de los datos**, o seleccione la tabla y pulse **Ctrl+R**. Las vistas previas se abren como documentos, por lo que puede abrir varias a la vez y anclarlas, hacerlas flotantes o moverlas a otro monitor.

![Vista previa de tabla de la tabla Internet Sales con el menú desplegable de filtro de una columna de fecha abierto](~/content/assets/images/preview-data-big.png)

## Lectura de la cuadrícula

Tabular Editor ejecuta una consulta DAX que devuelve las filas que la vista puede mostrar y carga más filas a medida que te desplazas. El rango de desplazamiento depende del modo de almacenamiento y del motor:

- Una tabla importada con una clave principal, en un motor que admita [`WINDOW`](https://dax.guide/window), se desplaza por toda la tabla. La paginación utiliza `WINDOW` con respecto a la clave primaria.
- Una tabla importada sin clave principal, o en un motor sin compatibilidad con `WINDOW`, muestra solo las primeras filas, y la vista previa indica que el desplazamiento está deshabilitado.
- Una tabla DirectQuery muestra solo las primeras filas, hasta la preferencia **Límite de filas**, con un mensaje que indica que la exploración paginada no está disponible para las tablas DirectQuery. Filtra la cuadrícula o escribe una consulta DAX para ver filas específicas.

Los metadatos de la vista previa se almacenan en caché para la sesión, y al volver a abrir una vista previa no se consulta de nuevo al servidor. Si el modelo se procesó fuera de Tabular Editor, seleccione **Actualizar vista previa**.

Si una columna calculada está en un estado no válido, sus celdas muestran el texto «(se necesita cálculo)». Seleccione **Calcular tabla** en la barra de herramientas o **Recalcular tabla...** en el menú contextual del encabezado de la columna para actualizarla.

![Menú contextual del encabezado de columna en la vista previa de tabla con la opción «Recalcular tabla» seleccionada, encima de las celdas que indican que es necesario realizar un cálculo](~/content/assets/images/recalculate-table.png)

## Orden de las columnas

De forma predeterminada, las columnas aparecen en el orden en que el motor las devuelve. **Ordenar las columnas de la vista previa de la tabla alfabéticamente** en @preferences las ordena por nombre, como lo hace el Explorador TOM.

## Buscar una columna en una tabla ancha

De forma predeterminada, al seleccionar una columna en la @tom-explorer-view, la vista previa se desplaza hasta esa columna y la resalta. Desactive **Seguir la columna seleccionada** en la barra de herramientas para desactivar esta función en una vista previa, o **Seguir la columna seleccionada en el Explorador TOM** en @preferences para todas las vistas previas.

## Barra de herramientas

La barra de herramientas **Vista previa de tabla** y el menú **Vista previa de tabla** tienen los mismos comandos:

| Comando | Qué hace |
|---|---|
| **Simulación de usuario...** | Establece la identidad con la que se ejecuta la consulta de vista previa, para mostrar los datos que ve un usuario concreto. |
| **Actualizar vista previa** | Vuelve a leer la tabla y descarta los metadatos almacenados en caché. |
| **Actualización automática** | Actualiza esta vista previa automáticamente cuando cambia el modelo implementado. El valor predeterminado para las nuevas vistas previas se establece en @preferences. |
| **Seguir columna seleccionada** | Sigue la selección de columnas en el Explorador TOM. Consulte [Buscar una columna en una tabla ancha](#finding-a-column-in-a-wide-table). |
| **Calcular tabla** | Vuelve a calcular las columnas calculadas de la tabla. |

## Menú contextual

Además de los comandos estándar de la cuadrícula (ordenar, filtrar, ajustar al contenido, selector de columnas), la cuadrícula de vista previa dispone de estos comandos:

| Comando | Dónde aparece | Qué hace |
|---|---|---|
| **Bloquear anchos de columna** | Encabezado de columna | Evita que la cuadrícula cambie el tamaño de las columnas a medida que se desplaza y carga más filas. |
| **Editar expresión...** | Encabezado de una columna calculada | Abre la expresión DAX de la columna en el **Editor de expresiones**. |
| **Recalcular tabla...** | Encabezado de una columna calculada que no está actualizada | Recalcula la tabla. |
| **Mostrar consulta DAX real...** | En cualquier parte de la cuadrícula | Abre un nuevo documento [consulta DAX](xref:dax-query) editable con la consulta que hay detrás de la vista previa. |

### Mostrar consulta DAX real

**Mostrar consulta DAX real...** formatea la consulta que ejecuta la vista previa, incluidos el filtro y la ordenación aplicados en la cuadrícula, y la abre como un nuevo documento de consulta DAX sin ejecutarla. La consulta no tiene lógica de paginación y devuelve todas las filas filtradas.

> [!NOTE]
> La vista **Consulta DAX** tiene un comando con el mismo nombre en su cuadrícula de resultados, que muestra la última consulta ejecutada en una ventana de solo lectura.

## Filtrado

Cada encabezado de columna tiene un menú desplegable de filtros que enumera los valores distintos de la columna, hasta el límite establecido por **Máx. valores en el menú desplegable de filtros** en @preferences (5000 de forma predeterminada). Los valores que superan el límite no se muestran, y aumentar el límite hace que la consulta del menú desplegable sea más lenta.

## Preferencias

Los ajustes de esta página se encuentran en **Herramientas > Preferencias > Exploración de datos > Vista previa de tabla**. Consulta @preferences para ver la lista completa.

## Próximos pasos

- @dax-query
- @pivot-grid
- @tom-explorer-view
