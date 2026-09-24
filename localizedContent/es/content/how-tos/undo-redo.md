---
uid: undo-redo
title: Compatibilidad con Deshacer/Rehacer
author: Morten Lønskov
updated: 2026-09-16
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Compatibilidad con Deshacer/Rehacer

Cualquier cambio que hagas en Tabular Editor se puede deshacer con **Ctrl+Z** y rehacer con **Ctrl+Y**. No hay límite en la cantidad de operaciones que puedes deshacer, pero la pila se restablece cuando cargas un modelo diferente, ya sea desde un archivo o desde una base de datos.

Una operación que afecta a muchos objetos se deshace en un solo paso. Arrastrar una carpeta de visualización llena de medidas a un nuevo elemento padre, cambiar el nombre en lote de varios objetos o aplicar un script de corrección de Best Practice Analyzer; cada una de estas acciones se deshace con un solo **Ctrl+Z**.

## Eliminar objetos

Al eliminar un objeto, también se elimina todo lo que dependía de él. En el caso de una columna, eso incluye las relaciones en las que participa, los niveles de jerarquía creados sobre ella y sus traducciones, así como las perspectivas a las que pertenece. En Tabular Editor 3, también se quita de los calendarios y las variaciones que la usaban, y se borra cualquier configuración de _Ordenar por columna_ que apunte a ella.

Deshacer restaura el objeto _y_ todo lo que se eliminó junto con él, en un solo paso.

Tabular Editor te avisa antes de eliminar algo que tenga consecuencias. Si eliminas un único objeto al que hacen referencia otros objetos, se te informa y se te pide confirmación, indicando lo que ocurrirá:

- Otros objetos hacen referencia al objeto mediante expresiones DAX, por lo que esas expresiones dejarán de funcionar.
- La columna se usa en una o varias jerarquías, por lo que se eliminarán los niveles correspondientes.
- La columna se usa en una o varias relaciones, por lo que esas relaciones se eliminarán.
- En Tabular Editor 3, la columna se usa en uno o varios calendarios, por lo que se quitará de ellos.

Al eliminar varios objetos a la vez, siempre se pide confirmación, aunque no se detalla qué objeto origina cada advertencia.

Un único objeto del que no depende nada se elimina sin confirmación, porque deshacer está a una sola tecla de distancia. Si prefieres que se te pregunte siempre, marca **Mostrar siempre advertencias al eliminar** en **Herramientas > Preferencias > Explorador TOM > Eliminar** en Tabular Editor 3.

> [!NOTE]
> Eliminar un objeto no reescribe el DAX que hacía referencia a él. Las expresiones dependientes conservan la referencia, que ahora queda huérfana, y se reportan como errores en el Report @messages-view. Esto es distinto de cambiar el nombre: en ese caso, [la corrección de fórmulas](xref:formula-fix-up-dependencies) actualiza por ti las expresiones que hacen referencia al objeto.

## Deshacer y cambios no guardados

En Tabular Editor 3, deshacer y los indicadores de cambios no guardados usan el mismo punto de referencia. Deshacer hasta volver al estado en que se guardó el modelo por última vez borra todos los indicadores; rehacer hace que vuelvan a aparecer. Deshacer _más allá_ del último punto de guardado hace que reaparezcan los indicadores de los objetos que se revirtieron.

**Revert** es la herramienta más directa cuando quieres descartar un cambio concreto, en lugar de retroceder por la pila de deshacer hasta llegar a él. Restaura una sola propiedad, un objeto, una tabla o todo el modelo a su último estado guardado en un único paso reversible, sin afectar a ninguna otra edición no guardada. Consulta @unsaved-changes.
