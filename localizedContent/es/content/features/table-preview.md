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

Una **Vista previa de tabla** muestra el contenido de una tabla, fila por fila, sin escribir una consulta. Haz clic con el botón derecho en una tabla del @tom-explorer-view y selecciona **Previsualizar datos**, o selecciona la tabla y pulsa **Ctrl+R**.

![Vista previa de datos](~/content/assets/images/preview-data-big.png)

Puedes abrir una vista previa de varias tablas a la vez y organizarlas como quieras. Cada vista previa es un documento normal, así que puedes acoplarla, hacerla flotante o moverla a un segundo monitor.

## Cómo interpretar la cuadrícula

Tabular Editor ejecuta una Consulta DAX que devuelve solo tantas filas como puede mostrar la vista y, a medida que te desplazas, va cargando más. Hasta dónde puedes desplazarte depende del modo de almacenamiento y del motor:

| Tabla                                                                                                                  | Desplazamiento                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Importación, en un motor que admite [`WINDOW`](https://dax.guide/window) y en el que la tabla tiene una clave primaria | Toda la tabla. La paginación usa `WINDOW` sobre la clave primaria                                          |
| Importación, sin compatibilidad con `WINDOW` o sin una clave primaria                                                  | Solo las primeras filas; la vista previa indica que el desplazamiento está desactivado                                     |
| DirectQuery                                                                                                            | Solo las primeras filas, hasta el valor de la preferencia **Límite de filas**; unos mensajes informativos explican por qué |

Los metadatos de la vista previa se almacenan en caché durante la sesión, por lo que al volver a abrir una vista previa no se vuelve a consultar el servidor. Usa **Actualizar vista previa** para volver a leerla si, por ejemplo, el modelo se ha procesado fuera de Tabular Editor.

Si una columna calculada está en un estado no válido, sus celdas muestran _(Calculation needed)_. Usa **Calcular tabla** en la barra de herramientas o **Recalcular tabla...** en el menú contextual de la columna para ponerla al día.

![Recalcular tabla](~/content/assets/images/recalculate-table.png)

## Orden de las columnas

De forma predeterminada, las columnas aparecen en el orden en que el motor las devuelve, que se corresponde aproximadamente con el orden interno de las columnas y a menudo parece arbitrario. Marca _Ordenar alfabéticamente las columnas de la Vista previa de tabla_ en @preferencias para que sigan el mismo orden que usa el Explorador TOM.

## Encontrar una columna en una tabla ancha

Al seleccionar una columna en @tom-explorer-view, la vista previa se desplaza hasta esa columna y la resalta. Esto está activado de forma predeterminada y puedes desactivarlo para una sola vista previa con **Seguir la columna seleccionada** en la barra de herramientas, o para todas las vistas previas en @preferencias.

## Barra de herramientas

La barra de herramientas de **Vista previa de tabla** y el menú **Vista previa de tabla** correspondiente incluyen los mismos comandos:

| Comando                                                             | Qué hace                                                                                                                                                                                                           |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Suplantación...** | Elige la identidad con la que se ejecuta la consulta de vista previa para ver los datos que vería un usuario concreto                                                                                              |
| **Actualizar vista previa**                                         | Vuelve a leer la tabla y descarta los metadatos en caché                                                                                                                                                           |
| **Actualización automática**                                        | Actualiza esta vista previa automáticamente cada vez que se hagan cambios en el modelo implementado. El valor predeterminado para las nuevas vistas previas proviene de @preferencias |
| **Seguir la columna seleccionada**                                  | Sigue la selección de columnas del Explorador TOM, como se describe más arriba                                                                                                                                     |
| **Calcular tabla**                                                  | Vuelve a calcular las columnas calculadas de la tabla                                                                                                                                                              |

## Menú contextual

Además de los comandos estándar de la cuadrícula (ordenación, filtrado, mejor ajuste, selector de columnas), la cuadrícula de vista previa añade:

| Comando                                                                             | Dónde aparece                                               | Qué hace                                                                                                                        |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Bloquear el ancho de las columnas**                                               | Encabezado de columna                                       | Evita que la cuadrícula redimensione las columnas mientras te desplazas y se cargan más filas al paginar                        |
| **Editar expresión...**             | Encabezado de una columna calculada                         | Abre la expresión DAX de esa columna en el **Editor de expresiones**                                                            |
| **Recalcular tabla calculada...**   | Encabezado de una columna calculada que no está actualizada | Recalcula la tabla                                                                                                              |
| **Mostrar la Consulta DAX real...** | En cualquier lugar de la cuadrícula                         | Abre un documento nuevo y editable de [Consulta DAX](xref:dax-query) que contiene la consulta que hay detrás de la vista previa |

### Mostrar la Consulta DAX real

**Mostrar la Consulta DAX real...** toma la consulta que ejecuta la vista previa, incluidos los filtros y la ordenación que has aplicado en la cuadrícula, la formatea y la abre como un nuevo documento de Consulta DAX. No se ejecuta automáticamente; edítala y ejecútala cuando quieras.

Los envoltorios de paginación se omiten deliberadamente, de modo que obtienes la consulta sobre los datos que estás viendo, en lugar de la consulta sobre una sola pantalla.

> [!NOTE]
> La vista **Consulta DAX** tiene un comando con el mismo nombre en su cuadrícula de resultados, pero hace algo distinto: muestra la última consulta ejecutada en una ventana de solo lectura en lugar de abrir un documento nuevo.

## Filtrado

Cada encabezado de columna incluye un menú desplegable de filtro con los valores distintos de la columna. En una columna con muchos valores distintos, la lista está limitada por _Máx. valores en el menú desplegable de filtro_ en @Preferencias; el valor predeterminado es 5.000. Los valores que superan ese límite no se muestran en la lista y no se pueden marcar directamente. Aumenta el límite si los necesitas, teniendo en cuenta que al abrir el menú desplegable se ejecuta una consulta más costosa.

## Preferencias

Todas las opciones mencionadas en esta página se encuentran en **Herramientas > Preferencias > Exploración de datos > Vista previa de tabla**. Consulte @preferencias para ver la lista completa.

## Pasos a seguir

- @dax-query
- @pivot-grid
- @tom-explorer-view
