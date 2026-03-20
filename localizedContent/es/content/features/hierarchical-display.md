---
uid: hierarchical-display
title: Visualización jerárquica
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Negocios
          full: true
        - edition: Empresarial
          full: true
---

## Visualización jerárquica

Los objetos del modelo cargado se muestran en el árbol del Explorador TOM. De forma predeterminada, todos los tipos de objetos (tablas visibles, roles, relaciones, etc.) se muestran. Si solo desea ver tablas, medidas, columnas y jerarquías, vaya al menú "Ver" y desactive "Mostrar todos los tipos de objetos".

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/AllObjectTypes.png)

Al expandir una tabla en el grupo "Tablas", encontrará las medidas, columnas y jerarquías que contiene la tabla, organizadas de forma predeterminada en sus respectivas carpetas de visualización. Así, los objetos se organizan de forma similar a como los usuarios finales los verían en las herramientas cliente:

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/DisplayFolders.png)

Utilice los botones inmediatamente encima del árbol del Explorador para activar o desactivar la visualización de objetos invisibles, carpetas de visualización, medidas, columnas y jerarquías, o para filtrar los objetos por nombre. Puede cambiar el nombre de un objeto seleccionándolo y después pulsando F2. Esto también funciona con las carpetas de visualización. Si hace doble clic en una medida o columna calculada, puede editar su [expresión DAX](dax-editor.md). Al hacer clic con el botón derecho se mostrará un menú contextual con una serie de accesos directos útiles para operaciones como establecer la visibilidad, incluir en una perspectiva, agregar columnas a una jerarquía, etc.
