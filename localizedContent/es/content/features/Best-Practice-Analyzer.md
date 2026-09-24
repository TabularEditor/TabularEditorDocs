---
uid: best-practice-analyzer
title: Best Practice Analyzer
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Best Practice Analyzer

El Best Practice Analyzer comprueba tu modelo con un conjunto de reglas y enumera todos los objetos que infringen alguna de esas reglas. Se ejecuta en segundo plano mientras trabajas, por lo que el número de problemas pendientes siempre está actualizado y puede corregir muchos de los problemas que encuentra por ti.

Una regla es una condición definida sobre los objetos del modelo, además de un nivel de gravedad y una descripción. Las reglas cubren aspectos en los que es fácil equivocarse y resulta caro detectarlo más tarde: columnas calculadas que deberían trasladarse al origen, relaciones entre columnas con tipos de datos que no coinciden, medidas sin cadena de formato y objetos que se han dejado visibles cuando deberían estar ocultos.

Pulsa **F10** o haz clic en el recuento de problemas de la ventana principal para abrir el Best Practice Analyzer. Puedes desactivar el análisis en segundo plano en **Herramientas > Preferencias > Best Practice Analyzer** (**Archivo > Preferencias** en Tabular Editor 2).

## Dónde ir a continuación

| Página                                           | Qué cubre                                                                                                                                                                                                                                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| @using-bpa                          | Cómo trabajar con los resultados: la lista de problemas, ir a un objeto, ignorar un objeto o una regla y generar o aplicar un script de corrección. También se trata la ventana **Administrar reglas de BPA** y las colecciones de reglas que enumera. |
| @built-in-bpa-rules                 | El conjunto de reglas seleccionado incluido con Tabular Editor 3, sus categorías y cómo desactivar reglas individuales.                                                                                                                                                                |
| @using-bpa-sample-rules-expressions | Cómo escribir tus propias expresiones de regla, con ejemplos detallados.                                                                                                                                                                                                               |

El resto de esta página explica de dónde vienen las reglas y cómo incorporar reglas que están fuera del modelo.

## Colecciones de reglas y precedencia

Las reglas llegan a un modelo a través de _colecciones_, que aparecen en la mitad superior de la ventana **Administrar reglas de BPA**. @using-bpa describe cada colección y dónde se almacenan sus reglas.

Si el mismo ID de regla aparece en más de una colección, la precedencia va de arriba abajo en la lista: una regla definida dentro del modelo tiene prioridad sobre una regla con el mismo ID definida en la máquina local. Eso te permite sobrescribir una regla compartida para adaptarla a una convención específica de un modelo concreto.

Selecciona **(Reglas efectivas)** en la parte superior de la lista para ver las reglas que realmente se aplican una vez resuelta la precedencia. Cada regla muestra de qué colección procede, y una regla tachada indica que una colección con mayor precedencia la ha sobrescrito.

## Agregar una colección de reglas

Además de las colecciones integradas, del modelo, del usuario y de la máquina, puedes adjuntar archivos de reglas desde cualquier otra ubicación. Las colecciones agregadas de este modo tienen prioridad sobre las reglas definidas en el modelo y, si agregas varias, puedes moverlas arriba y abajo para establecer su orden.

En la ventana Administrar reglas de BPA, haz clic en **Agregar...** y elige una de estas opciones:

- **Crear nuevo archivo de reglas** crea un archivo `.json` vacío en la ubicación que elijas, listo para que agregues reglas.
- **Incluir archivo de reglas local** adjunta un archivo `.json` de reglas que ya tienes.
- **Incluir archivo de reglas desde una URL** adjunta reglas disponibles a través de HTTP o HTTPS; por ejemplo, las [reglas estándar de BPA](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json) publicadas por Microsoft. Las colecciones cargadas desde una URL son de solo lectura.

![El cuadro de diálogo Agregar colección de reglas, que muestra las opciones Crear nuevo archivo de reglas, Incluir archivo de reglas local e Incluir archivo de reglas desde una URL](~/content/assets/images/bpa-add-rule-collection.png)

En las dos opciones de archivo, puedes guardar la referencia como una ruta relativa; conviene hacerlo cuando el archivo de reglas está en el mismo repositorio que el modelo. Una referencia relativa solo se resuelve cuando el propio modelo se cargó desde el disco, ya que un modelo cargado desde un servidor no tiene un directorio de trabajo con respecto al que resolverla. Un archivo en otra unidad o en un recurso compartido de red debe indicarse mediante una ruta absoluta.

Puedes agregar, editar, clonar y eliminar reglas en cualquier colección para la que tengas permisos de escritura. **Mover a...** mueve o copia la regla seleccionada a otra colección.

## Marcadores de posición en las descripciones de reglas

La descripción de una regla se muestra como información sobre herramientas en cada objeto que la incumple; por eso conviene que mencione el objeto al que se refiere. Se sustituyen tres marcadores de posición cuando se muestra la descripción:

| Marcador de posición | Se expande a                                              |
| -------------------- | --------------------------------------------------------- |
| `%object%`           | Una referencia DAX completa al objeto, cuando corresponda |
| `%objectname%`       | El nombre del objeto                                      |
| `%objecttype%`       | El tipo del objeto                                        |
