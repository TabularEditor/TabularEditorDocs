---
uid: dax-query
title: Consultas DAX
author: Morten Lønskov
updated: 2025-08-27
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

Tabular Editor incluye una ventana integrada de Consulta DAX para escribir y ejecutar consultas DAX sobre el modelo semántico.

Un caso de uso muy común de las Consultas DAX es la Consulta DAX generada por el [Analizador de rendimiento de Power BI](https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/), que permite copiar la consulta de cada Visual para solucionar problemas, depurar o realizar un análisis de rendimiento detallado.

La ventana se puede abrir mientras estás conectado a un modelo semántico desde el menú **Archivo > Nuevo > Consulta DAX** o mediante el acceso directo de la barra de herramientas.

![Consulta Dax Nueva](~/content/assets/images/features/dax_query_window/create_new_dax_query.png)

El Editor de DAX integrado y con reconocimiento de contexto garantiza que, al iniciar una nueva consulta, solo estén disponibles las dos palabras clave válidas de DAX: DEFINE o EVALUATE (Presione Ctrl+Space para comprobarlo usted mismo)

## Opciones de Consulta DAX

La ventana de consultas de DAX tiene seis opciones de consulta distintas.

![Barra de herramientas de Consulta Dax](~/content/assets/images/features/dax_query_window/dax_query_toolbar.png)

1. **Ejecutar (F5)**: Si hay una selección, ejecuta el DAX seleccionado; de lo contrario, ejecuta la consulta completa en el editor de Consulta DAX.
2. **Ejecutar consulta completa**: Ejecuta la consulta completa en el Editor de Consulta DAX
3. **Ejecutar selección (Mayús+F5)**: Si hay una selección, la ejecuta. De lo contrario, ejecuta la instrucción EVALUATE donde se encuentre el cursor en ese momento.
4. **Detener**: Este botón cancela la ejecución de la consulta actual.
5. **Ejecutar consulta automáticamente**: Permite hacer un seguimiento del modelo semántico conectado y actualizar los resultados de la consulta cada vez que algo cambie en el modelo. Esto puede ser útil para entender, por ejemplo, cómo cambia el resultado de una medida si la modificas.
6. **Mantener la ordenación y el filtrado**: Permite a los usuarios controlar cómo se mantienen la ordenación y el filtrado en la cuadrícula(s) de resultados al ejecutar consultas. Hay tres preferencias disponibles:
   - **Nunca**: La ordenación y el filtrado se restablecen cada vez que se ejecuta la consulta.
   - **Cuando se modifica la consulta**: La ordenación y el filtrado se restablecen solo cuando cambia la estructura de la consulta.
   - **Siempre**: La ordenación y el filtrado se conservan mientras las columnas sigan estando en la nueva consulta.

Los valores predeterminados de las preferencias "Ejecutar consulta automáticamente" y "Mantener la ordenación y el filtrado" se pueden configurar en el cuadro de diálogo de Preferencias: **Herramientas > Preferencias... > Exploración de datos > Consulta DAX** > Básico.

### Añadir o actualizar medidas, columnas y tablas con consultas DAX

Tabular Editor (3.12.0 y versiones posteriores) permite agregar o cambiar medidas directamente desde la ventana de Consulta DAX.

A partir de Tabular Editor 3.23.0, "Aplicar" y "Aplicar selección" también procesan las instrucciones DEFINE COLUMN y DEFINE TABLE. Tabular Editor creará en el modelo las columnas o tablas calculadas correspondientes, o actualizará sus expresiones si ya existen.

Hay cuatro opciones para aplicar al modelo las medidas, columnas y tablas definidas en la Consulta DAX:

![Consulta DAX Aplicar medida](~/content/assets/images/features/dax_query_window/dax_query_apply_measure.png)

La opción "Aplicar" sincroniza la expresión DAX de todas las medidas, columnas o tablas definidas explícitamente en la consulta con la definición del objeto. Se crean las medidas, columnas o tablas que aún no existan.

"Aplicar medidas y sincronizar" aplica la expresión DAX a la definición de las medidas, columnas o tablas y guarda el modelo.

Las opciones "Aplicar selección" y "Aplicar selección y sincronizar" solo aplican las medidas, columnas o tablas incluidas en la selección actual del editor de consultas.

A diferencia de la [funcionalidad de Script DAX](xrefid:dax-scripts), de este modo solo puede actualizarse la propiedad de expresión de una medida, ya que la sintaxis de la Consulta DAX no permite especificar otras propiedades, como la descripción, la carpeta de visualización, etc.

La opción "Aplicar" también se ha añadido al menú contextual al hacer clic con el botón derecho.

![Consulta Dax Aplicar Clic Derecho](~/content/assets/images/features/dax_query_window/dax_query_apply_measure_right_click.png)

Los atajos de teclado para estos comandos son:

- Aplicar (F7)
- Aplicar medidas y sincronizar (Mayús+F7)
- Aplicar selección (F8)
- Aplicar selección y sincronizar (Mayús+F8)

## Ejemplo de Consulta DAX

Una Consulta DAX siempre devuelve una tabla de resultados, y la forma más sencilla de crear una es evaluar una tabla dentro del modelo.

```DAX
EVALUATE
Products
```

![Consulta Dax Evaluar tabla](~/content/assets/images/features/dax_query_window/evaluate_table.png)

También es posible devolver el valor de una medida, pero se requiere un constructor de tablas {} alrededor del nombre de la medida para convertir el valor escalar en una tabla de 1x1.

```DAX
EVALUATE
{ [Invoice Lines] }
```

![Consulta Dax Evaluar medida](~/content/assets/images/features/dax_query_window/evaluate_measure.png)

### Varias instrucciones EVALUATE

Es perfectamente posible tener varias instrucciones EVALUATE dentro de la misma Consulta DAX. Este tipo de consulta se encuentra con mayor frecuencia en las consultas del Analizador de rendimiento de Power BI.

Ambas tablas se devuelven en la siguiente instrucción, pero como pestañas separadas en el panel de resultados.

```DAX
EVALUATE
Products

EVALUATE
Customers
```

![Consulta Dax Evaluar varias tablas](~/content/assets/images/features/dax_query_window/multiple_evaluate_table.png)

## Depuración de Consulta DAX

Las Consultas DAX son uno de los dos lugares donde es posible ejecutar el [Depurador de DAX](xrefid:dax-debugger); el otro es el Pivot Grid.

El Depurador de DAX permite comprender cómo funciona DAX dentro de una sola celda. Para iniciar el depurador, basta con hacer clic con el botón derecho en la celda deseada y elegir "Depurar celda"; esto iniciará el depurador en el contexto de la celda seleccionada.

![Consulta Dax Depurador](~/content/assets/images/features/dax_query_window/dax_query_open_dax_debugger.gif)

## Exportar resultados de la Consulta DAX

Tabular Editor 3, a partir de la versión 3.16.0, incorpora la nueva capacidad de exportar los resultados de una Consulta DAX a CSV o Excel. Tras ejecutar la Consulta DAX, se activa un botón en la barra de herramientas que permite guardar los resultados localmente en formato CSV o Excel.

> [!TIP]
> Para exportar más de 1001 filas, seleccione "haga clic para obtener todas las filas" después de ejecutar la Consulta DAX

![Consulta Dax Exportar datos](~/content/assets/images/features/dax_query_window/dax_query_export_data.png)
