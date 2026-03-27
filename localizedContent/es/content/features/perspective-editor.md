---
uid: perspective-editor
title: Editor de perspectiva
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

# Editor de perspectiva

> [!NOTE]
> Para poder agregar perspectivas a modelos que se ejecutan en SSAS o Azure AS, necesitarás una licencia de la edición Enterprise de Tabular Editor 3.

El **Editor de perspectiva** ofrece una vista rápida de la asignación de perspectivas de los objetos del modelo (tablas, columnas, jerarquías y medidas). Puede abrir el Editor de perspectiva desde el menú **Ver**. Como alternativa, si solo necesita editar ciertas perspectivas, selecciónelas en el **Explorador TOM** (mantenga pulsadas las teclas CTRL o SHIFT para seleccionar varias) y, a continuación, haga clic con el botón derecho y elija **Mostrar en el Editor de perspectiva**.

![Editor de perspectiva](~/content/assets/images/perspective-editor.png)

Utilice las casillas de verificación del Editor de perspectiva para agregar o quitar rápidamente varios objetos de una perspectiva. Puede usar Deshacer (Ctrl+Z) y Rehacer (Ctrl+Y) de la forma habitual. Tenga en cuenta que los cambios realizados a través del Editor de perspectiva se aplican inmediatamente al TOM, aunque aún deberá guardar (Ctrl+S) o implementar su modelo para que los cambios se apliquen en Analysis Services / Power BI.

## Barra de herramientas del Editor de perspectiva

Mientras el Editor de perspectiva está activo, la barra de herramientas que lo acompaña ofrece las siguientes opciones:

- ![Perspective Editor Add Perspective](~/content/assets/images/perspective-editor-add-perspective.png) **Nueva perspectiva**: Este botón agrega una nueva perspectiva al modelo. La perspectiva se mostrará en el Editor de perspectiva.
- ![Perspective Editor Hide Members](~/content/assets/images/perspective-editor-hide-members.png) **Mostrar/ocultar opciones ocultas**: Active esta opción si desea ver todos los objetos en el Editor de perspectiva, incluidos los objetos ocultos.
- ![Perspective Editor Folder](~/content/assets/images/perspective-editor-folder.png) **Mostrar/ocultar carpetas de visualización**: Active este botón de conmutación si desea que el Editor de perspectiva agrupe los objetos de las tablas (medidas, jerarquías, columnas) por carpetas de visualización.

## Trabajar con varias perspectivas

Si trabajas en un modelo con muchas perspectivas, puede que no sea práctico mostrarlas todas a la vez. Puedes reorganizar el orden de visualización de las perspectivas en el Editor de perspectivas arrastrando los encabezados de las columnas, lo que facilita comparar perspectivas una junto a otra. Además, puedes añadir o quitar perspectivas del editor en cualquier momento desde el menú contextual con clic derecho:

![Columnas del Editor de perspectivas](~/content/assets/images/perspective-editor-columns.png)