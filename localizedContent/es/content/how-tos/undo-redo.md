---
uid: undo-redo
title: Soporte para deshacer y rehacer
author: Morten Lønskov
updated: 2026-10-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Soporte para deshacer y rehacer

Presiona **Ctrl+Z** para deshacer un cambio y **Ctrl+Y** para rehacerlo. La pila de deshacer no tiene límite de tamaño y se vacía cuando cargas otro modelo, ya sea desde un archivo o desde una base de datos. Una operación que cambia muchos objetos, como arrastrar una carpeta, un cambio de nombre por lotes o una corrección del Best Practice Analyzer (BPA), cuenta como un solo paso de deshacer.

## Undo in text editors

In Tabular Editor 3, **Ctrl+Z** and **Ctrl+Y** act on the part of the window that has focus. When focus is in a text control, the shortcuts undo and redo typing in that control. Text controls include DAX query, DAX script and C# script documents, the **Expression Editor** and a cell you're editing in the **Properties** view. Each text control has its own undo history, separate from the model undo stack. When focus is in the TOM Explorer or another view, the shortcuts undo and redo model changes. In the AI Assistant chat box, **Ctrl+Z** and **Ctrl+Y** don't undo or redo model changes.

Focus stays in the script document after you run a C# script or apply a DAX script. Pressing **Ctrl+Z** there undoes typing in the script. If the script text was pasted or inserted in one step, **Ctrl+Z** removes all of it, and **Ctrl+Y** restores it.

To undo a model change while a text control or the AI Assistant chat box has focus, do one of the following:

- click the TOM Explorer, then press **Ctrl+Z**
- open the **Edit** menu and select the entry named after the last model change, such as **Undo C# script (MCP)**. When a text control has focus, this entry appears at the top of the menu, above **Undo typing**.

## Eliminar objetos

Al eliminar un objeto, también se elimina lo que depende de él. En el caso de una columna, Tabular Editor elimina:

- las relaciones que usan la columna
- los niveles de jerarquía basados en la columna
- sus traducciones y sus pertenencias a perspectivas
- en Tabular Editor 3, sus entradas en calendarios y variaciones

En Tabular Editor 3, también borra la propiedad `SortByColumn` de las columnas ordenadas por la columna eliminada.

Deshacer restaura el objeto y los objetos que dependen de él en un solo paso.

Si el objeto que vas a eliminar tiene otros objetos que dependen de él, un cuadro de diálogo de confirmación enumera las consecuencias:

- Si las expresiones DAX hacen referencia al objeto, esas expresiones dejan de funcionar.
- Si la columna se usa en jerarquías, se eliminan los niveles correspondientes.
- Si la columna se usa en relaciones, esas relaciones se eliminan.
- En Tabular Editor 3, si la columna se usa en calendarios, se quita de ellos.

Eliminar varios objetos a la vez siempre muestra un cuadro de diálogo de confirmación, pero el cuadro no enumera las consecuencias por objeto.

Si un objeto no tiene objetos dependientes, se elimina sin pedir confirmación. En Tabular Editor 3, selecciona **Mostrar siempre las advertencias de eliminación** en la sección **Eliminación**, en **Herramientas > Preferencias > Tabular Editor > Explorador TOM**, para confirmar cada eliminación.

> [!NOTE]
> Eliminar un objeto no reescribe el DAX que hace referencia a él. Las expresiones dependientes conservan la referencia y se Reportan como errores en @messages-view. Cuando cambias el nombre de un objeto, la [corrección de fórmulas](xref:formula-fix-up-dependencies) actualiza las expresiones que hacen referencia a él.

## Deshacer y cambios sin guardar

En Tabular Editor 3, los indicadores de cambios no guardados reflejan la pila de deshacer. Al deshacer hasta el último estado guardado, todos los indicadores se borran y al rehacer vuelven a mostrarse. Al deshacer cambios anteriores al último guardado, se muestran indicadores en los objetos que se revirtieron.

**Revertir** descarta un cambio y conserva los posteriores. Restaura una propiedad, un objeto, una tabla o todo el modelo a su último estado guardado, sin afectar a tus otros cambios sin guardar, y puedes deshacer la reversión. Consulta @unsaved-changes.
