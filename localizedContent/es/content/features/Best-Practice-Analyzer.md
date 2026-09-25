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

Best Practice Analyzer comprueba tu modelo con un conjunto de reglas y enumera todos los objetos que incumplen alguna de ellas. Se ejecuta en segundo plano mientras trabajas, por lo que el recuento de incidencias pendientes siempre está actualizado y puede corregir automáticamente muchos de los problemas que encuentra.

Una regla es una condición definida sobre los objetos del modelo, junto con un nivel de gravedad y una descripción. Las reglas abarcan cosas que es fácil hacer mal y costoso detectar más tarde: columnas calculadas que deberían trasladarse al origen, relaciones entre columnas con tipos de datos que no coinciden, medidas sin cadena de formato y objetos que se han dejado visibles cuando deberían estar ocultos.

Pulsa **F10** o haz clic en el recuento de incidencias de la ventana principal para abrir el Best Practice Analyzer. El análisis en segundo plano se puede desactivar desde **Herramientas > Preferencias > Best Practice Analyzer** (**Archivo > Preferencias** en Tabular Editor 2).

## Dónde ir después

| Página                                           | Qué cubre                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| @using-bpa                          | Trabajar con los resultados: la lista de incidencias, ir a un objeto, ignorar un objeto o una regla y generar o aplicar un script de corrección. También incluye la ventana Administrar reglas de BPA y las colecciones de reglas que enumera. |
| @built-in-bpa-rules                 | El conjunto de reglas curado que viene con Tabular Editor 3, sus categorías y cómo desactivar reglas individuales.                                                                                                                                                             |
| @using-bpa-sample-rules-expressions | Cómo escribir tus propias expresiones de reglas, con ejemplos prácticos.                                                                                                                                                                                                       |

El resto de esta página explica de dónde vienen las reglas y cómo incorporar reglas que residen fuera del modelo.

## Colecciones de reglas y precedencia

Las reglas se incorporan a un modelo mediante _colecciones_, que aparecen en la mitad superior de la ventana Administrar reglas de BPA. La directiva @using-bpa describe cada colección y dónde se almacenan sus reglas.

Si el mismo ID de regla aparece en más de una colección, el orden de precedencia va de arriba abajo en la lista: una regla definida dentro del modelo tiene prioridad sobre otra con el mismo ID definida en la máquina local. Esto te permite anular una regla compartida para ajustarla a una convención específica de un modelo.

Selecciona **(Reglas efectivas)** en la parte superior de la lista para ver las reglas que realmente se aplican una vez resuelta la precedencia. Cada regla muestra de qué colección proviene, y una regla tachada indica que ha sido anulada por una colección de mayor precedencia.

## Agregar una colección de reglas

Además de las colecciones integradas, del modelo, del usuario y de la máquina, puedes adjuntar archivos de reglas de otros lugares. Las colecciones agregadas de esta forma tienen precedencia sobre las reglas definidas dentro del modelo y, si agregas varias, puedes moverlas hacia arriba y hacia abajo para establecer su orden.

Haz clic en **Agregar...** en la ventana Administrar reglas de BPA y elige una de las siguientes opciones:

- **Crear nuevo archivo de reglas** crea un archivo `.json` vacío en la ubicación que elijas, listo para que agregues reglas.
- **Incluir archivo de reglas local** adjunta un archivo `.json` de reglas que ya tienes.
- **Incluir archivo de reglas desde una URL** adjunta reglas disponibles a través de HTTP o HTTPS; por ejemplo, las [reglas de BPA estándar](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json) publicadas por Microsoft. Las colecciones cargadas desde una dirección URL son de solo lectura.

![El cuadro de diálogo Agregar colección de reglas, que muestra las opciones Crear nuevo archivo de reglas, Incluir archivo de reglas local e Incluir archivo de reglas desde URL](~/content/assets/images/bpa-add-rule-collection.png)

En las dos opciones de archivo puedes almacenar la referencia como una ruta relativa, y conviene hacerlo cuando el archivo de reglas está en el mismo repositorio que el modelo. Una referencia relativa solo se resuelve cuando el propio modelo se ha cargado desde disco, ya que un modelo cargado desde un servidor no tiene un directorio de trabajo en el que basarse para resolverla. Un archivo en una unidad diferente o en un recurso compartido de red debe referenciarse mediante una ruta absoluta.

Puedes agregar, editar, clonar y eliminar reglas en cualquier colección en la que tengas acceso de escritura. **Mover a...** mueve o copia la regla seleccionada a otra colección.

## Marcadores de posición en las descripciones de las reglas

La descripción de una regla se muestra como información sobre herramientas en cada objeto que la incumple, así que conviene que mencione el objeto del que habla. Al mostrar la descripción, se sustituyen tres marcadores de posición:

| Marcador de posición | Se expande a                                              |
| -------------------- | --------------------------------------------------------- |
| `%object%`           | Una referencia DAX completa al objeto, cuando corresponda |
| `%objectname%`       | El nombre del objeto                                      |
| `%objecttype%`       | El tipo de objeto                                         |
