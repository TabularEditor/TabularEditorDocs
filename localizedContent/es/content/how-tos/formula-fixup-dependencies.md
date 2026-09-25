---
uid: formula-fix-up-dependencies
title: Corrección automática de fórmulas y dependencias de fórmulas
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Corrección automática de fórmulas y dependencias de fórmulas

Tabular Editor analiza continuamente las expresiones DAX de todas las medidas, columnas calculadas y tablas calculadas de tu modelo para construir un árbol de dependencias de estos objetos. This dependency tree is used for the Formula Fix-up functionality, which may be enabled under **Tools > Preferences** (**File > Preferences** in Tabular Editor 2). La Corrección automática de fórmulas actualiza la expresión DAX de cualquier medida, columna calculada o tabla calculada cada vez que se cambia el nombre de un objeto al que se hacía referencia en la expresión.

Para visualizar el árbol de dependencias, haz clic con el botón derecho en el objeto del árbol del explorador y selecciona "Mostrar dependencias..."

![image](~/content/assets/images/formula-fixup-dependencies-01.png)