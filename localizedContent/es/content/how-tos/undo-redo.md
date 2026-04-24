---
uid: undo-redo
title: Compatibilidad con Deshacer/Rehacer
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## Compatibilidad con Deshacer/Rehacer

Cualquier cambio que hagas en Tabular Editor se puede deshacer con CTRL+Z y, a continuación, rehacer con CTRL+Y. No hay límite en el número de operaciones que se pueden deshacer, pero la pila se restablece cuando abres un archivo Model.bim o cargas un modelo desde una base de datos.

Al eliminar objetos del modelo, todas las traducciones, perspectivas y relaciones que hagan referencia a los objetos eliminados también se eliminan automáticamente (mientras que Visual Studio normalmente muestra un mensaje de error indicando que el objeto no se puede eliminar). Al eliminar objetos del modelo, todas las traducciones, perspectivas y relaciones que hagan referencia a los objetos eliminados también se eliminan automáticamente (mientras que Visual Studio normalmente muestra un mensaje de error indicando que el objeto no se puede eliminar). Ten en cuenta que, aunque Tabular Editor puede detectar [dependencias de fórmulas DAX](xref:formula-fix-up-dependencies), Tabular Editor no te avisará si eliminas una medida o una columna que se usa en la expresión DAX de otra medida o columna calculada.