---
uid: perspective-editor
title: Editor de perspectivas
author: Šarūnas Jučius
updated: 2022-03-16
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

# Editor de perspectivas

> [!NOTE]
> Para agregar perspectivas a modelos que se ejecuten en SSAS o Azure AS, necesitarás una licencia de la Edición Enterprise de Tabular Editor 3.

El **Editor de perspectivas** ofrece una vista rápida de la asignación de perspectivas a los objetos del modelo (tablas, columnas, jerarquías y medidas). Puedes abrir el Editor de perspectiva desde el menú **Ver**. Como alternativa, si solo necesitas editar ciertas perspectivas, selecciónalas en el **Explorador TOM** (mantén pulsadas las teclas CTRL o SHIFT para seleccionar varias) y, a continuación, haz clic con el botón derecho y elige **Mostrar en el Editor de perspectiva**.

![Editor de perspectivas](~/content/assets/images/perspective-editor.png)

Usa las casillas de verificación del Editor de perspectiva para agregar o quitar rápidamente varios objetos de una perspectiva. Puedes usar Deshacer (Ctrl+Z) y Rehacer (Ctrl+Y) de la forma habitual. Ten en cuenta que los cambios realizados a través del Editor de perspectiva se aplican de inmediato al TOM, aunque aún tendrás que guardar (Ctrl+S) o implementar el modelo para que los cambios se reflejen en Analysis Services / Power BI.

## Barra de herramientas del Editor de perspectivas

Mientras el Editor de perspectivas está activo, la barra de herramientas que lo acompaña ofrece las siguientes opciones:

- ![Editor de perspectiva: Agregar perspectiva](~/content/assets/images/perspective-editor-add-perspective.png) **Nueva perspectiva**: Este botón agrega una nueva perspectiva al modelo. La perspectiva se mostrará en el Editor de perspectivas.
- ![Editor de perspectiva: Mostrar u ocultar opciones ocultas](~/content/assets/images/perspective-editor-hide-members.png) **Mostrar/ocultar opciones ocultas**: Activa esta opción si quieres ver todos los objetos en el Editor de perspectiva, incluidos los objetos ocultos.
- ![Editor de perspectiva: Carpetas de visualización](~/content/assets/images/perspective-editor-folder.png) **Mostrar/ocultar carpetas de visualización**: Activa este botón de alternancia si quieres que el Editor de perspectiva agrupe los objetos de las tablas (medidas, jerarquías, columnas) por carpetas de visualización.

## Trabajar con varias perspectivas

Si estás trabajando en un modelo con muchas perspectivas, puede resultar poco práctico mostrarlas todas a la vez. Puedes reorganizar el orden de visualización de las perspectivas en el Editor de perspectivas arrastrando los encabezados de las columnas; así, será más fácil comparar las perspectivas una junto a otra. Además, puedes añadir o quitar perspectivas del editor en cualquier momento desde el menú contextual al hacer clic con el botón derecho:

![Columnas en el Editor de perspectivas](~/content/assets/images/perspective-editor-columns.png)