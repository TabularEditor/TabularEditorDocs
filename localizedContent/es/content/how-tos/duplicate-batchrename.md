---
uid: duplicate-and-batch
title: Duplicación de objetos y cambio de nombre en lote
author: Morten Lønskov
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Duplicar objetos y renombrar en lote

El menú contextual, accesible con clic derecho, del árbol del Explorador le permite duplicar medidas y columnas. Los objetos duplicados tendrán el sufijo "copy" al final del nombre. Además, puede realizar cambios de nombre en lote seleccionando varios objetos y haciendo clic con el botón derecho en el árbol del Explorador.

![Batch rename dialog](~/content/assets/images/getting-started-te-03.png)

Puede usar RegEx para renombrar y, opcionalmente, elegir si también desea renombrar las traducciones.

A duplicated object keeps whatever error and warning indicators the original carried, so a copy of an object with an invalid expression is marked as invalid straight away.