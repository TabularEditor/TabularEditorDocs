---
uid: roles-and-rls
title: Roles y seguridad a nivel de filas
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## Roles y seguridad a nivel de filas

Los roles son visibles en el Árbol del Explorador. Puedes hacer clic con el botón derecho en el árbol para crear nuevos roles, eliminar o duplicar roles existentes. Puedes ver y editar los miembros de cada rol. Para ello, localiza el rol en el árbol del Explorador y ve a la propiedad "Miembros del rol" en la cuadrícula de propiedades. Ten en cuenta que, al implementar, el [Asistente de implementación](../features/deployment.md) no implementa los miembros del rol de forma predeterminada.

La mayor ventaja de trabajar con roles en Tabular Editor es que cada objeto de tabla tiene una propiedad "Filtros de nivel de fila", que te permite ver y editar los filtros definidos en esa tabla para todos los roles:

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/RLSTableContext.png)

Por supuesto, también puedes ver los filtros de todas las tablas en un rol concreto, de forma similar a la interfaz de usuario de SSMS o Visual Studio:

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/RLSRoleContext.png)