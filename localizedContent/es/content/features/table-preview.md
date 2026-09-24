---
uid: table-preview
title: Vista previa de tabla
author: Morten Lønskov
updated: 2026-09-14
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

Una **Vista previa de tabla** muestra el contenido de una tabla, fila por fila, sin escribir una consulta. Haz clic con el botón derecho en una tabla en @tom-explorer-view y elige **Vista previa de datos** o selecciona la tabla y pulsa **Ctrl+R**.

![Vista previa de datos](~/content/assets/images/preview-data-big.png)

Puedes abrir una vista previa de varias tablas a la vez y organizarlas como quieras. Cada vista previa es un documento normal, así que puedes acoplarla, dejarla flotante o moverla a un segundo monitor.

## Cómo leer la cuadrícula

Tabular Editor ejecuta una consulta DAX que devuelve solo tantas filas como puede mostrar la vista y luego va cargando más a medida que te desplazas. Hasta dónde puedes desplazarte depende del modo de almacenamiento y del motor:

| Tabla                                                                                                              | Desplazamiento                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Importación, en un motor que admite [`WINDOW`](https://dax.guide/window), cuando la tabla tiene una clave primaria | La tabla completa. La paginación usa `WINDOW` con la clave primaria                                        |
| Importación, sin compatibilidad con `WINDOW` o sin clave primaria                                                  | Solo las primeras filas; la vista previa indica que el desplazamiento está deshabilitado                                   |
| DirectQuery                                                                                                        | Solo las primeras filas, hasta el valor de la preferencia **Límite de filas**; unos mensajes informativos explican por qué |

Los metadatos de la vista previa se almacenan en caché durante la sesión, por lo que al volver a abrir una vista previa no se vuelve a consultar el servidor. Usa **Actualizar vista previa** para volver a leerlos si, por ejemplo, el modelo se ha procesado fuera de Tabular Editor.

Si una columna calculada está en un estado no válido, sus celdas muestran _(Calculation needed)_. Usa **Calcular tabla** en la barra de herramientas o **Volver a calcular tabla...** en el menú contextual de la columna para ponerla al día.

![Volver a calcular tabla](~/content/assets/images/recalculate-table.png)

## Orden de las columnas

De forma predeterminada, las columnas aparecen en el orden en que las devuelve el motor, que se corresponde aproximadamente con el orden interno de las columnas y a menudo parece arbitrario. Marca _Ordenar alfabéticamente las columnas de la Vista previa de tabla_ en @preferencias para que sigan el mismo orden que usa el Explorador TOM.

## Encontrar una columna en una tabla ancha

Al seleccionar una columna en @tom-explorer-view, la vista previa se desplaza hasta esa columna y la resalta. Esta opción está activada de forma predeterminada y puede desactivarse para una vista previa concreta con **Seguir la columna seleccionada** en la barra de herramientas, o para todas las vistas previas en @preferencias.

## Barra de herramientas

La barra de herramientas de **Vista previa de tabla** y el menú **Vista previa de tabla** correspondiente incluyen los mismos comandos:

| Comando                                                                          | Qué hace                                                                                                                                                                                                                  |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Suplantación de identidad...** | Selecciona la identidad con la que se ejecuta la consulta de vista previa para ver los datos que vería un usuario concreto                                                                                                |
| **Actualizar vista previa**                                                      | Vuelve a leer la tabla y descarta los metadatos en caché                                                                                                                                                                  |
| **Actualización automática**                                                     | Actualiza esta vista previa automáticamente cada vez que se hagan cambios en el modelo implementado. La configuración predeterminada para las nuevas vistas previas se toma de @preferencias |
| **Seguir la columna seleccionada**                                               | Sigue la selección de columnas del Explorador TOM, como se describe arriba                                                                                                                                                |
| **Calcular tabla**                                                               | Vuelve a calcular las columnas calculadas de la tabla                                                                                                                                                                     |

## Menú contextual

Además de los comandos estándar de la cuadrícula (ordenación, filtrado, mejor ajuste, selector de columnas), la cuadrícula de vista previa añade:

| Comando                                                                              | Dónde aparece                                               | Qué hace                                                                                                                      |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Bloquear el ancho de las columnas**                                                | Encabezado de columna                                       | Impide que la cuadrícula cambie el tamaño de las columnas al desplazarte y cargar más filas                                   |
| **Editar expresión...**              | Encabezado de una columna calculada                         | Abre la expresión DAX de esa columna en el **Editor de expresiones**                                                          |
| **Recalcular la tabla calculada...** | Encabezado de una columna calculada que no está actualizada | Recalcula la tabla                                                                                                            |
| **Mostrar la Consulta DAX real...**  | En cualquier lugar de la cuadrícula                         | Abre un nuevo documento editable de [Consulta DAX](xref:dax-query) que contiene la consulta que hay detrás de la vista previa |

### Mostrar la consulta DAX real

**Mostrar la consulta DAX real...** toma la consulta que está ejecutando la vista previa, incluidos los filtros y la ordenación que hayas aplicado en la cuadrícula, la formatea y la abre en un nuevo documento de Consulta DAX. No se ejecuta automáticamente; edítala y ejecútala cuando estés listo.

Los contenedores de paginación se omiten deliberadamente, de modo que obtienes la consulta sobre los datos que estás viendo, en lugar de la consulta sobre una sola pantalla de esos datos.

> [!NOTE]
> La vista **Consulta DAX** tiene un comando con el mismo nombre en su cuadrícula de resultados, pero hace algo distinto: muestra la última consulta ejecutada en una ventana de solo lectura en lugar de abrir un documento nuevo.

## Filtrado

Cada encabezado de columna tiene una lista desplegable de filtro con los valores distintos de la columna. En una columna con muchos valores distintos, la lista está limitada por _Max. valores en el menú desplegable de filtro_ en @preferences; de forma predeterminada, 5000. Los valores que superen ese límite no se muestran en la lista y no se pueden marcar directamente. Aumenta ese límite si los necesitas, teniendo en cuenta que, al abrir la lista desplegable, se ejecutará una consulta más pesada.

## Preferencias

Todos los ajustes mencionados en esta página se encuentran en **Herramientas > Preferencias > Exploración de datos > Vista previa de tabla**. Consulta @preferences para ver la lista completa.

## Pasos a seguir

- @dax-query
- @pivot-grid
- @tom-explorer-view
