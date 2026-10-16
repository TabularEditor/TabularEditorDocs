---
uid: formula-fix-up-dependencies
title: Corrección de fórmulas y dependencias de fórmulas
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Corrección de fórmulas y dependencias de fórmulas
Tabular Editor analiza continuamente las expresiones DAX de todas las medidas, columnas calculadas y tablas calculadas del modelo y crea un árbol de dependencias de estos objetos. La *corrección de fórmulas* utiliza el árbol: cuando cambia el nombre de un objeto, actualiza las expresiones DAX que hacen referencia a él. Habilítela con **Corrección automática de fórmula DAX** en **Herramientas > Preferencias > Tabular Editor > Operaciones de modelado** (**Archivo > Preferencias** en Tabular Editor 2).

Haga clic derecho en un objeto del Explorador TOM y elija **Mostrar dependencias...** para ver su árbol de dependencias.

![Cuadro de diálogo «Dependencias de objetos» que muestra los objetos de los que depende una medida](~/content/assets/images/formula-fixup-dependencies-01.png)