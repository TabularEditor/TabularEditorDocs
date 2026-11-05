---
uid: dax-query
title: Consultas DAX
author: Morten Lønskov
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
# Consultas DAX

Tabular Editor dispone de una ventana de consultas DAX integrada para escribir y lanzar consultas DAX contra el modelo semántico.

Un caso de uso muy extendido de las consultas DAX es la consulta DAX generada por el [analizador de rendimiento de Power BI](https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/), donde es posible copiar la consulta de cada elemento visual para solucionar problemas, depurar o realizar un análisis detallado del rendimiento.

La ventana se puede abrir mientras se está conectado a un modelo semántico de cualquiera de estas tres formas:

- el menú **Archivo > Nuevo > Consulta DAX**
- el acceso directo de la barra de herramientas
- **Mostrar consulta DAX real...** en el menú contextual de una @table-preview, que abre un nuevo documento de consulta que contiene la consulta subyacente a la vista previa, incluidos el filtro y la ordenación.

![Nueva consulta Dax](~/content/assets/images/features/dax_query_window/create_new_dax_query.png)

El editor DAX integrado, que tiene en cuenta el contexto, garantiza que solo estén disponibles las dos palabras clave DAX válidas al iniciar una nueva consulta: DEFINE o EVALUATE (pulse Ctrl+Espacio para comprobarlo usted mismo).

## Opciones de consulta DAX

La ventana de consultas DAX tiene seis opciones de consulta diferentes.

![Barra de herramientas de consultas Dax](~/content/assets/images/features/dax_query_window/dax_query_toolbar.png)


1. **Ejecutar (F5)**: Si hay una selección, ejecuta el DAX seleccionado; de lo contrario, ejecuta la consulta completa en el editor de consultas DAX.
2. **Ejecutar consulta completa**: Ejecuta la consulta completa en el editor de consultas DAX.
3. **Ejecutar selección (Mayús+F5)**: Si hay una selección, la ejecuta. De lo contrario, ejecuta la instrucción EVALUATE donde se encuentre actualmente el cursor.
4. **Detener**: Este botón cancela la ejecución de la consulta actual.
5. **Ejecutar consulta automáticamente**: Permite realizar un seguimiento del modelo semántico conectado y actualizar los resultados de la consulta cada vez que se produce un cambio en el modelo. Esto puede ser útil para comprender, por ejemplo, cómo cambia el resultado de una medida si se modifica.
6. **Mantener ordenación y filtrado**: Permite a los usuarios controlar cómo se mantienen la ordenación y el filtrado en las cuadrículas de resultados al ejecutar consultas. Hay tres preferencias disponibles:
   - **Nunca**: La ordenación y el filtrado se restablecen cada vez que se ejecuta la consulta.
   - **Cuando se modifica la consulta**: La ordenación y el filtrado se restablecen solo cuando cambia la estructura de la consulta.
   - **Siempre**: La ordenación y el filtrado se mantienen mientras las columnas permanezcan en la nueva consulta.

Los valores predeterminados de las preferencias «Ejecutar consulta automáticamente» y «Conservar ordenación y filtrado» se pueden configurar en el cuadro de diálogo Preferencias: **Herramientas > Preferencias... > Exploración de datos > Consulta DAX** > Básico. La sección **Mantener los documentos abiertos al cambiar de modelo** de la misma página controla lo que sucede con las consultas DAX abiertas cuando se abre un modelo diferente. Consulte [Cambiar de modelo](#switching-models).

### Cambiar de modelo

Cuando abre un modelo diferente, las consultas DAX abiertas permanecen abiertas y se conectan al nuevo modelo. Si se selecciona **Ejecutar automáticamente consultas DAX de forma predeterminada**, la consulta se ejecuta de nuevo con el nuevo modelo; de lo contrario, se ejecuta con el nuevo modelo la próxima vez que la ejecute. Si el nuevo modelo no tiene una base de datos con la que ejecutarse, como un modelo cargado desde un archivo sin una base de datos de área de trabajo, la consulta permanece abierta y no se puede ejecutar.

Para cerrar las consultas DAX cuando abra un modelo diferente, desmarque **Mantener abiertas las consultas DAX cuando se abra un modelo diferente** en **Herramientas > Preferencias > Exploración de datos > Consulta DAX**. La opción está seleccionada de forma predeterminada.

### Añadir o actualizar medidas, columnas y tablas con consultas DAX

Tabular Editor (3.12.0 y versiones posteriores) tiene la capacidad de añadir o cambiar medidas directamente a través de la ventana de consultas DAX.

A partir de Tabular Editor 3.23.0, las opciones Aplicar y Aplicar selección también procesan las sentencias DEFINE COLUMN y DEFINE TABLE. Tabular Editor creará las columnas/tablas calculadas correspondientes en su modelo o actualizará sus expresiones si ya existen.

Hay cuatro opciones para aplicar al modelo medidas, columnas y tablas definidas mediante consultas DAX: 

![Aplicar medida de consulta Dax](~/content/assets/images/features/dax_query_window/dax_query_apply_measure.png)

La opción «Aplicar» sincroniza la expresión DAX de todas las medidas, columnas o tablas definidas explícitamente en la consulta con la definición del objeto. Se crean todas las medidas, columnas o tablas que aún no existan.

«Aplicar medidas y sincronizar» aplica la expresión DAX a la definición de las medidas, columnas o tablas y guarda el modelo.

Las opciones «Aplicar selección» y «Aplicar selección y sincronizar» solo aplicarán las medidas, columnas o tablas dentro de la selección actual del editor de consultas.

A diferencia de la [función Script DAX](xref:dax-scripts), solo se puede actualizar de esta manera la propiedad de expresión de una medida, ya que la sintaxis de las consultas DAX no admite la especificación de otras propiedades, como Descripción, Carpeta de visualización, etc.

La opción «Aplicar» también se ha añadido al menú contextual que aparece al hacer clic con el botón derecho.

![Aplicar consulta Dax con clic derecho](~/content/assets/images/features/dax_query_window/dax_query_apply_measure_right_click.png)

Los accesos directos para estos comandos son:

- Aplicar (F7)
- Aplicar medidas y sincronizar (Mayús+F7)
- Aplicar selección (F8)
- Aplicar selección y sincronizar (Mayús+F8)

## Ejemplo de consulta DAX

Una consulta DAX siempre devuelve una tabla de resultados, y la forma más sencilla de consulta DAX que se puede crear es una que evalúe una tabla dentro del modelo.

```DAX
EVALUATE
Products
```

![Consulta Dax: evaluar tabla](~/content/assets/images/features/dax_query_window/evaluate_table.png)

También es posible devolver el valor de una medida, pero se requiere un constructor de tablas {} alrededor del nombre de la medida para convertir el valor escalar en una tabla 1x1.

```DAX
EVALUATE
{ [Invoice Lines] }
```

![Consulta Dax: Evaluar una medida](~/content/assets/images/features/dax_query_window/evaluate_measure.png)

### Múltiples sentencias EVALUATE

Es perfectamente posible tener varias sentencias EVALUATE dentro de la misma consulta DAX. Este tipo de consulta se encuentra con mayor frecuencia en las consultas del analizador de rendimiento de Power BI.

Ambas tablas se devuelven en la siguiente sentencia, pero como pestañas de filas separadas en el panel de resultados.

```DAX
EVALUATE
Products

EVALUATE
Customers
```

![Evaluar varias tablas en una consulta Dax](~/content/assets/images/features/dax_query_window/multiple_evaluate_table.png)

## Depuración de consultas DAX

Las consultas DAX son uno de los dos lugares donde es posible ejecutar el [Depurador DAX](xref:dax-debugger); el otro es el Pivot Grid.

El depurador de DAX permite comprender cómo funciona DAX dentro de una sola celda. Para iniciar el depurador, simplemente haga clic con el botón derecho en la celda deseada y elija «Depurar celda», lo que iniciará el depurador en el contexto de la celda elegida.

![Depurador de consultas Dax](~/content/assets/images/features/dax_query_window/dax_query_open_dax_debugger.gif)

## Exportar los resultados de una consulta DAX

Tabular Editor 3, a partir de la versión 3.16.0, introduce la nueva función de exportar los resultados de una consulta DAX a CSV o Excel. Después de ejecutar la consulta DAX, se activa un botón en la barra de herramientas que permite a los usuarios guardar los resultados localmente en formato CSV o Excel.

> [!TIP]
> Para exportar más de 1001 filas, seleccione «Haga clic para obtener todas las filas» después de ejecutar la consulta DAX.

![Exportar datos de una consulta Dax](~/content/assets/images/features/dax_query_window/dax_query_export_data.png)
