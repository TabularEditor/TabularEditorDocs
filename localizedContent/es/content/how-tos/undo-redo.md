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

## Deshacer en editores de texto

En Tabular Editor 3, **Ctrl+Z** y **Ctrl+Y** actúan sobre la parte de la ventana que tiene el foco. Cuando el foco está en un control de texto, estos atajos deshacen y rehacen lo escrito en ese control. Los controles de texto incluyen los documentos de consulta DAX, los documentos de script DAX y de **C# Script**, el **Editor de expresiones** y cualquier celda que estés editando en la vista de **Propiedades**. Cada control de texto tiene su propio historial de deshacer, independiente de la pila de deshacer del modelo. Cuando el foco está en el Explorador TOM o en otra vista, los atajos deshacen y rehacen los cambios del modelo. En el cuadro de chat de AI Assistant, **Ctrl+Z** y **Ctrl+Y** no deshacen ni rehacen los cambios del modelo.

El foco permanece en el documento de script después de ejecutar un C# Script o aplicar un script DAX. Al pulsar **Ctrl+Z** allí, se deshace lo escrito en el script. Si el texto del script se pegó o insertó en un solo paso, **Ctrl+Z** lo elimina por completo y **Ctrl+Y** lo restaura.

Para deshacer un cambio en el modelo mientras un control de texto o el cuadro de chat de AI Assistant tiene el foco, haz una de las siguientes opciones:

- haz clic en el Explorador TOM y, después, pulsa **Ctrl+Z**
- abre el menú **Editar** y selecciona la opción que lleva el nombre del último cambio del modelo, como **Deshacer C# Script (MCP)**. Cuando un control de texto tiene el foco, esta entrada aparece en la parte superior del menú, por encima de **Deshacer escritura**.

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
