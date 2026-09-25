---
uid: undo-redo
title: Soporte para deshacer y rehacer
author: Morten Lønskov
updated: 2026-09-16
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Soporte para deshacer y rehacer

Cualquier cambio que realices en Tabular Editor se puede deshacer con **Ctrl+Z** y rehacer con **Ctrl+Y**. No hay límite en el número de operaciones que puedes deshacer, pero la pila se restablece cuando cargas un modelo distinto, ya sea desde un archivo o desde una base de datos.

Una operación que afecta a muchos objetos se deshace en un solo paso. Arrastrar una carpeta de visualización llena de medidas a otro elemento padre, cambiar el nombre de un lote de objetos o aplicar un script de corrección de Best Practice Analyzer: todo se deshace con un solo **Ctrl+Z**.

## Eliminar objetos

Al eliminar un objeto, también se elimina aquello que dependía de él. En el caso de una columna, eso incluye las relaciones en las que participa, los niveles de jerarquía basados en ella, sus traducciones y las perspectivas a las que pertenece. En Tabular Editor 3 también se elimina de cualquier calendario y variaciones que la usaran, y se borra cualquier configuración de _Ordenar por columna_ que apunte a ella.

Deshacer restaura el objeto _y_ todo lo que se eliminó junto con él, en un solo paso.

Tabular Editor te avisa antes de eliminar algo si eso tiene consecuencias. Si eliminas un único objeto al que hacen referencia otros objetos, se te avisa y se te pide confirmación, indicando qué ocurrirá:

- Otros objetos hacen referencia a este objeto mediante expresiones DAX, por lo que esas expresiones dejarán de funcionar.
- La columna se usa en una o varias jerarquías, por lo que se eliminarán los niveles correspondientes.
- La columna se usa en una o varias relaciones, por lo que esas relaciones se eliminarán.
- En Tabular Editor 3, la columna se usa en uno o varios calendarios, por lo que se eliminará de ellos.

Si eliminas varios objetos a la vez, siempre se te pedirá confirmación, aunque no se detalla qué objeto da lugar a cada advertencia.

Un único objeto del que no depende nada se elimina sin pedir confirmación, ya que puedes deshacerlo con una sola combinación de teclas. Si prefieres que se te pregunte siempre, marca **Mostrar siempre advertencias de eliminación** en **Herramientas > Preferencias > Explorador TOM > Eliminar** en Tabular Editor 3.

> [!NOTE]
> Eliminar un objeto no reescribe el DAX que hacía referencia a él. Las expresiones dependientes conservan la referencia, ahora colgante, y se reportan como errores en @messages-view. Esto es distinto de renombrar: en ese caso, la [corrección de fórmulas](xref:formula-fix-up-dependencies) actualiza por ti las expresiones que lo referencian.

## Deshacer y cambios sin guardar

En Tabular Editor 3, Deshacer y los indicadores de cambios sin guardar se basan en el mismo punto de referencia. Al deshacer hasta el estado en que se guardó por última vez el modelo se borran todos los indicadores; al rehacer, vuelven a aparecer. Deshacer _más allá_ del último punto de guardado hace que los indicadores reaparezcan en los objetos que se deshicieron.

**Revert** es la herramienta más directa cuando quieres descartar un cambio concreto, en lugar de recorrer la pila de deshacer hasta llegar a él. Restablece una sola propiedad, un objeto, una tabla o todo el modelo a su último estado guardado en un único paso que se puede deshacer, sin afectar a ninguna otra edición sin guardar. Consulta @unsaved-changes.
