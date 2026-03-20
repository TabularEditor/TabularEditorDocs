---
uid: script-library-beginner
title: C# Scripts para principiantes
author: Morten Lønskov
updated: 2023-02-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Biblioteca de C# Scripts: scripts para principiantes

Estos son scripts más básicos, fáciles de entender o modificar. Tienen un alcance definido y una complejidad limitada; no necesitas tener un conocimiento sólido del lenguaje C# para usarlos, entenderlos y modificarlos. Por eso, son un buen punto de partida para empezar a escribir C# Scripts en Tabular Editor.

<br>
<br>

| <div style="width:250px">Nombre del script</div>                                           | Propósito                                                                                                                                                               | Caso de uso                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Contar filas de una tabla](xref:script-count-rows)                                        | Evalúa un COUNTROWS ( 'Table' ) de una tabla seleccionada.                                                                           | Cuando quieres comprobar cuántas filas hay en una tabla o si se ha cargado.                                                                                                                      |
| [Crear medidas de suma a partir de columnas](xref:script-create-sum-measures-from-columns) | Crea medidas SUM ( 'Table'[Column] ) a partir de cualquier columna seleccionada. | Cuando tienes muchas columnas en una tabla o modelo nuevo y necesitas crear muchas medidas de una sola vez.                                                                                      |
| [Crear tabla de medidas](xref:script-create-measure-table)                                 | Crea una tabla de medidas                                                                                                                                               | Cuando quieres crear una tabla vacía para usarla como tabla de medidas de organización                                                                                                                           |
| [Crear grupos de tablas](xref:script-create-table-groups)                                  | Organiza el modelo en grupos de tablas                                                                                                                                  | Cuando quieres organizar automáticamente tus tablas con la funcionalidad de grupos de tablas de Tabular Editor 3                                                                                                 |
| [Crear parámetro M](xref:script-create-m-parameter)                                        | Crear un nuevo parámetro M en 'Expresiones compartidas'                                                                                                                 | Cuando quieres crear un parámetro para usarlo en otras consultas de Power Query (particiones M / Expresiones compartidas).                                                    |
| [Editar particiones ocultas](xref:script-edit-hidden-partitions)                           | Muestra las propiedades de las particiones ocultas en Calc. Grupos y Calc. Tablas                                                       | Cuando necesitas ver o editar las propiedades TOM de estas particiones ocultas.                                                                                                                  |
| [Dar formato a medidas numéricas](xref:script-format-numeric-measures)                     | Da formato a las medidas elegidas                                                                                                                                       | Cuando quieres aplicar rápidamente una cadena de formato a las medidas seleccionadas actualmente                                                                                                                 |
| [Mostrar dependencias de los Data source](xref:script-show-data-source-dependencies)       | Muestra las dependencias de los Data source                                                                                                                             | Para los Data source explícitos (heredados), puede ser difícil saber exactamente dónde se usan. Este script muestra qué partición hace referencia al Data source seleccionado |
| [Crear parámetros de campo](xref:create-field-parameter)                                   | Crear rápidamente una tabla de parámetros de campo                                                                                                                      | Elige los objetos que deben formar parte del parámetro de campo y el script se encargará del resto                                                                                                               |
| [Mostrar valores únicos de columna](xref:script-display-unique-column-values)              | Mostrar valores únicos en una columna                                                                                                                                   | Cuando quieres ver los valores únicos de la columna seleccionada actualmente                                                                                                                                     |