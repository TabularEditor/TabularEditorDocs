---
uid: messages-view
title: Vista de mensajes
author: Daniel Otykier
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
# Vista de mensajes

La vista Mensajes de Tabular Editor 3 es una ventana de herramientas que muestra varios tipos de mensajes relacionados con el conjunto de datos actual. 

> [!TIP]
> Puede hacer doble clic en un mensaje para saltar al origen del error en el árbol del modelo o en el editor de scripts.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/messages-view.png" alt="Vista de mensajes" style="width: 500px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Ventana de mensajes en Tabular Editor. Proporciona una descripción general de todas las advertencias y los errores de su conjunto de datos </figcaption>
</figure>


Los mensajes se agrupan por **Origen**, como el analizador semántico, el editor de expresiones o Analysis Services. Cada fila tiene estas columnas:

| Columna | Muestra |
| -- | -- |
| **Objeto** | El objeto o documento al que pertenece el mensaje. |
| **Tipo** | La gravedad del mensaje: error, advertencia o información. |
| **Mensaje** | El texto del mensaje. |
| **Causado por** | En el caso de un error en cascada, el objeto cuyo error lo causa. En el caso de un error raíz, el número de errores dependientes que provoca. |
| **Línea** y **Columna** | La posición del mensaje en la expresión o en el documento. |

Los errores son expresiones o estructuras que Analysis Services rechaza, como una expresión no válida en un elemento de cálculo o una dependencia circular. Las advertencias señalan expresiones que funcionan pero que no siguen las prácticas recomendadas, como las referencias de medidas completamente calificadas.

## Errores en cascada y causas raíz

Cuando una expresión tiene un error, todas las expresiones que hacen referencia a ella también presentan un error, como una medida que falla únicamente porque falla una medida a la que hace referencia. Se trata de *errores en cascada*, y el error al que se remontan es el *error raíz*.

La columna **Causado por** muestra un valor diferente para cada tipo de error:

- En un error en cascada, indica el nombre del objeto con el error raíz, seguido de **+N** cuando el error se remonta a más de un error raíz.
- En un error raíz, muestra **+N errores dependientes**, contando los errores que causa directa e indirectamente.

Para trabajar con errores en cascada, haga clic derecho en una fila de la vista de mensajes:

- **Ir a la causa raíz** abre el error raíz en el editor de expresiones con el error resaltado. El comando solo aparece en los errores en cascada.
- **Mostrar errores en cascada** muestra u oculta los errores en cascada. Desactívala para mostrar solo los errores raíz que debes corregir. El ajuste está activado de forma predeterminada y se guarda entre sesiones.

Un objeto con un error propio y una referencia a un objeto roto muestra dos filas: un error raíz y un error en cascada. Los errores de Analysis Services y los errores en consultas DAX, scripts DAX y Pivot Grids nunca son en cascada.

## Copiar mensajes
La vista de mensajes permite copiar el mensaje de error con Ctrl+C.
 
A partir de Tabular Editor 3.23.0, Ctrl+C copia la celda seleccionada de forma predeterminada. Use Ctrl+Mayús+C (o Copiar fila en el menú contextual) para copiar a nivel de fila.

> [!TIP]
> Haga clic con el botón derecho en una celda para elegir **Copiar celda** o **Copiar fila**. El mismo menú incluye las opciones **Ir a la causa raíz** y **Mostrar errores en cascada**.


![Copiar en la vista de mensajes](~/content/assets/images/messages-view-copy.png)

