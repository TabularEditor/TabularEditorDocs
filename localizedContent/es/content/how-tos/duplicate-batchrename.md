---
uid: duplicate-and-batch
title: Duplicación de objetos y cambio de nombre en lote
author: Morten Lønskov
updated: 2026-10-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Duplicar objetos y renombrar en lote

El menú contextual, accesible con clic derecho, del árbol del Explorador le permite duplicar medidas y columnas. Los objetos duplicados tendrán el sufijo "copy" al final del nombre. Además, puede realizar cambios de nombre en lote seleccionando varios objetos y haciendo clic con el botón derecho en el árbol del Explorador.

![Cuadro de diálogo para renombrar en lote](~/content/assets/images/getting-started-te-03.png)

Puede usar RegEx para renombrar y, opcionalmente, elegir si también desea renombrar las traducciones.

Un objeto duplicado conserva todos los indicadores de error y advertencia que tenía el original, por lo que una copia de un objeto con una expresión no válida se marca como no válida de inmediato.

Si el original se muestra en más de una carpeta de visualización, la copia aparece en todas ellas y se selecciona después de crearse. Esto también se aplica cuando copia y pega un objeto.
