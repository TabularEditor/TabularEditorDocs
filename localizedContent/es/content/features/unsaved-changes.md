---
uid: unsaved-changes
title: Indicadores de cambios no guardados
author: Daniel Otykier
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Indicadores de cambios no guardados

Tabular Editor 3 marca todos los objetos y propiedades que difieren de la última versión guardada del modelo. Los cambios se marcan tanto si se hicieron a mano como si se hicieron mediante un [C# Script](xref:csharp-scripts) o una macro, o mediante el [Asistente de IA](xref:ai-assistant), y las marcas desaparecen en cuanto el cambio se guarda, se revierte o se deshace.

Los indicadores aparecen en dos lugares:

- En el [Explorador TOM](xref:tom-explorer-view), los objetos modificados se muestran con una fila resaltada y una insignia en su icono, con los mismos colores que la vista de comparación de modelos que se muestra al desplegar: naranja para los objetos editados, verde para los objetos añadidos y rojo para los objetos eliminados. Los objetos eliminados permanecen visibles, tachados, donde estaban, y las tablas y carpetas que contienen objetos modificados muestran un relleno rayado.
- En la [vista de propiedades](xref:properties-view), las propiedades que difieren del modelo guardado se muestran con una fila resaltada en naranja.

![Cambios no guardados en el Explorador TOM y la vista de propiedades](~/content/assets/images/unsaved-changes/overview.png)

Ambas vistas tienen un botón **Mostrar cambios** en la barra de herramientas que filtra la vista para mostrar solo lo que ha cambiado, y ambas ofrecen una opción **Revertir** al hacer clic con el botón derecho que devuelve una sola propiedad, un solo objeto o toda una rama del modelo a su estado guardado, sin afectar a ningún otro cambio sin guardar.

> [!NOTE]
> Los indicadores registran los cambios con respecto al origen desde el que se cargó el modelo o en el que se guardó por última vez. Desplegar el modelo en una base de datos diferente no los borra, ya que el modelo cargado sigue siendo distinto de su propio origen.

## Indicadores de cambios en el Explorador TOM

Cada objeto del árbol se resalta con un color y una insignia según lo que le haya ocurrido desde el último guardado:

- **Editados**: los objetos reciben una fila naranja clara y una insignia de punto naranja en su icono. Esto abarca cualquier propiedad modificada, incluidos los cambios en un subobjeto que no tiene un nodo propio en el árbol, como la política de actualización de una tabla o la configuración _Alternate Of_ de una columna.
- **Añadidos**: los objetos reciben una fila verde clara y una insignia verde **+**. Una tabla nueva y todas sus columnas nuevas aparecen en verde. Editar una propiedad de un objeto recién agregado hace que permanezca en verde, ya que el objeto sigue siendo nuevo en comparación con el modelo guardado.
- Los objetos **eliminados** reciben una fila de color rojo claro y una insignia roja **−**, y su nombre aparece tachado. Consulta [Objetos eliminados](#deleted-objects) más abajo.

Las tablas, las carpetas de visualización, los grupos de tablas y el nodo **Modelo** también se marcan cuando cambia algo debajo de ellos: su fila recibe un relleno rayado y su icono recibe la insignia del cambio que haya debajo. Verde cuando solo se agregaron objetos, y naranja en caso contrario. Esto te permite seguir los cambios en un árbol contraído o usar el filtro **Mostrar cambios** para ver solo los objetos modificados.

Cuando se selecciona un objeto, el resaltado de selección normal tiene prioridad sobre el tinte, por lo que una selección múltiple sigue siendo legible. La insignia del icono sigue marcando los objetos modificados dentro de la selección. Las insignias de error y advertencia también tienen prioridad sobre la insignia de cambio, por lo que un objeto con un error semántico conserva su insignia de error incluso cuando tiene cambios sin guardar.

> [!TIP]
> Si te cuesta distinguir las filas verdes de las rojas, activa el **Modo de daltonismo** en **Herramientas > Preferencias > Interfaz de usuario > Accesibilidad**. A partir de ese momento, los objetos agregados se marcan en color verde azulado en lugar de verde, tanto aquí como en la vista de comparación de modelos.

### Mostrar cambios

El botón **Mostrar cambios** de la barra de herramientas del Explorador TOM filtra el árbol para mostrar solo los objetos con cambios sin guardar, junto con las tablas, carpetas y grupos necesarios para llegar hasta ellos. Mientras el filtro está activo, el título de la vista muestra **Explorador TOM (Modificado)**.

![Filtro Mostrar cambios en el Explorador TOM](~/content/assets/images/unsaved-changes/tom-explorer-show-changes.png)

El filtro se aplica junto con los demás conmutadores de la barra de herramientas y el cuadro de búsqueda. Por ejemplo, ocultar columnas con **Ctrl+2** también oculta de la vista filtrada las columnas modificadas.

## Indicadores de cambio en la vista de propiedades

Al seleccionar un objeto modificado, las propiedades que difieren del modelo guardado se muestran con el mismo tinte naranja claro. Una fila contraída que contiene un subobjeto, como la fila **KPI** de una medida o la fila de la **política de actualización** de una tabla, se marca cuando cambia algo dentro del subobjeto. En las filas indexadas, como **Anotaciones**, solo se marca la anotación individual que ha cambiado.

Cuando se seleccionan varios objetos, se marca una fila de propiedad si alguno de los objetos seleccionados cambió esa propiedad.

El botón **Mostrar cambios** de la barra de herramientas de la vista de propiedades oculta todas las filas sin cambios, de modo que solo queden las propiedades modificadas. Mientras el filtro está activo, el título de la vista muestra **Propiedades (Modificado)**.

![Filtro Mostrar cambios en la vista de propiedades](~/content/assets/images/unsaved-changes/properties-show-changes.png)

## Revertir cambios

**Archivo > Recargar desde disco** descarta de una vez todos los cambios no guardados al recargar los metadatos del modelo desde su origen. El comando aparece como **Recargar desde el servidor** en un modelo abierto desde un servidor. En cambio, las siguientes opciones **Revertir** deshacen cambios individuales y dejan intactos todos los demás cambios no guardados.

Una reversión se comporta exactamente igual que volver a escribir el valor anterior o recrear manualmente el objeto eliminado: las referencias DAX se actualizan, los objetos dependientes se recalculan y toda la reversión pasa a ser un único paso en la pila de deshacer. Si cambias de idea, basta con **Editar > Deshacer** (**Ctrl+Z**) para recuperar el cambio revertido.

### Revertir una sola propiedad

Haz clic con el botón derecho en una fila marcada de la vista de propiedades y elige **Revertir** para devolver esa propiedad al valor que tenía la última vez que se guardó. Todos los demás cambios no guardados del objeto permanecen tal cual.

![Revertir una sola propiedad](~/content/assets/images/unsaved-changes/revert-property.png)

La opción **Revertir** solo está habilitada en las filas que tienen cambios no guardados. Con varios objetos seleccionados, usar **Revertir** en una fila combinada revierte la propiedad en todos los objetos seleccionados en los que se haya cambiado, como un único paso que se puede deshacer. **Revertir** en una fila contenedora como **Anotaciones** revierte todas las anotaciones de una vez: las anotaciones editadas vuelven a sus valores guardados, las anotaciones agregadas se eliminan y las anotaciones eliminadas vuelven a aparecer.

### Revertir un objeto o una rama del modelo

Haz clic con el botón derecho en un objeto marcado del Explorador TOM y elige **Revertir** para devolver el objeto, y todo lo que hay debajo de él, al estado que tenía la última vez que se guardó. **Revertir** también está disponible en tablas, carpetas de visualización, grupos de tablas y el nodo **Modelo**, aunque estos no estén marcados, siempre que haya cambiado algo dentro de ellos. Elegir **Revertir** en el nodo **Modelo** descarta todos los cambios no guardados del modelo como un único paso que se puede deshacer.

![Revertir un objeto en el Explorador TOM](~/content/assets/images/unsaved-changes/revert-object.png)

Al revertir un objeto o una rama:

- Las propiedades editadas vuelven a sus valores guardados.
- Los objetos agregados desde la última vez que se guardó se eliminan.
- Los objetos eliminados desde el último guardado vuelven exactamente como se guardaron, incluido el KPI de una medida eliminada, o los niveles de jerarquía y las relaciones de una columna eliminada.
- Los objetos de otras partes del modelo conservan sus cambios no guardados.

Todo lo que no pueda restaurarse se enumera en **Mensajes** con el mensaje **Reversión incompleta**, y el resto de la reversión se aplica. Esto ocurre, por ejemplo, cuando el nombre de un objeto eliminado se asignó posteriormente a un objeto nuevo que no puede quitarse.

## Objetos eliminados

Al eliminar un objeto, este no desaparece del Explorador TOM. Hasta que se guarde el modelo, el objeto permanece donde estaba, tachado en una fila de color rojo claro, con una insignia roja **−** en su icono. Cuando se muestran las columnas de información, la columna **Tipo de objeto** muestra, por ejemplo, **medida (Eliminada)**. Así, una eliminación es tan fácil de detectar como una edición.

![Objetos eliminados en el Explorador TOM](~/content/assets/images/unsaved-changes/deleted-objects.png)

Haz clic con el botón derecho en un objeto eliminado y elige **Restaurar** para recuperarlo exactamente como estaba justo antes de eliminarlo. Si el objeto tenía cambios sin guardar antes de que se eliminara, estos se restauran con él y siguen marcados para que puedan revertirse por separado. Puedes seleccionar varios objetos eliminados a la vez y restaurarlos en un solo paso.

Los objetos eliminados son marcadores de posición, no objetos del modelo:

- No se pueden editar, cambiar de nombre, arrastrar ni desplegar, y nunca se incluyen como destino al arrastrar y soltar o al pegar.
- Al seleccionarlos no se selecciona ningún objeto del modelo. La vista de propiedades no muestra nada y el menú contextual solo ofrece **Restaurar**.
- Una selección que combina objetos eliminados y activos no ofrece ni **Restaurar** ni las acciones habituales del objeto.
- Desaparecen en cuanto se guarda el modelo.

Los C# Script pueden acceder a los objetos eliminados seleccionados mediante `Selected.Deleted`. Consulta [Scripting](#scripting) más abajo.

### Agrupar los objetos eliminados bajo un único nodo

Si prefieres no mezclar los objetos eliminados con los activos, activa **Agrupar los objetos eliminados bajo un nodo "Objetos eliminados"** en **Herramientas > Preferencias > Explorador TOM > Cambios no guardados**. Los objetos eliminados de una tabla, jerarquía, rol o grupo de tablas se muestran entonces juntos bajo un único nodo **Objetos eliminados** al final de su contenedor, independientemente de las carpetas de visualización en las que estuvieran antes. El nodo adopta el resaltado rojo y su propia insignia de eliminado; los objetos que hay debajo aparecen tachados. Haz clic con el botón derecho en el nodo y elige **Restaurar** para recuperar todo lo que contiene en un solo paso.

![Objetos eliminados agrupados bajo un mismo nodo](~/content/assets/images/unsaved-changes/deleted-objects-group.png)

### Conservar los objetos eliminados entre guardados

De forma predeterminada, los objetos eliminados siguen visibles hasta que se guarda el modelo, ya que son cambios no guardados como cualquier otro. La preferencia **Mantener visibles los objetos eliminados** ofrece dos alternativas:

- **Nunca**: Los objetos eliminados desaparecen del Explorador TOM de inmediato. Aun así, se pueden recuperar con **Revertir** en su contenedor o con **Editar > Deshacer**.
- **Hasta que se cierre el modelo**: Los objetos eliminados siguen visibles durante toda la sesión de edición, incluso entre guardados, y se pueden restaurar. Restaurar un objeto que se eliminó antes del último guardado lo vuelve a crear, por lo que pasa a marcarse como objeto agregado. Los objetos que se crearon y se eliminaron entre dos guardados solo se conservan si se editaron o se guardaron en algún momento. Un objeto que se creó y se eliminó sin haberse modificado nunca no deja rastro.

## Cuándo desaparecen los indicadores

Un objeto o una propiedad pierde su marca cuando deja de diferir del último estado guardado del modelo. Esto ocurre cuando:

- Se guarda el modelo, ya sea en un archivo, una carpeta o una base de datos. Todos los indicadores desaparecen de inmediato.
- El cambio se revierte, ya sea con **Revertir** en el Explorador TOM o en la vista de propiedades, o con **Archivo > Recargar desde disco** (**Recargar desde el servidor**), que descarta todos los cambios.
- El cambio se deshace con **Editar > Deshacer** hasta volver al punto del último guardado. Rehacer el cambio vuelve a mostrar la marca, y deshacer _más allá_ del último guardado marca, en su lugar, los objetos revertidos.
- Una propiedad se restablece manualmente a su valor original. Tabular Editor 3 compara el valor actual con el guardado, por lo que una edición sin efecto neto no cuenta como cambio.

## Preferencias

Los indicadores se pueden ajustar en **Herramientas > Preferencias > Explorador TOM**, en la sección **Cambios no guardados**:

![Preferencias de cambios no guardados](~/content/assets/images/unsaved-changes/preferences.png)

- **Marcar objetos con cambios no guardados** (activado): Colorea las filas y añade un distintivo a los iconos de los objetos agregados, editados y eliminados en el Explorador TOM, y marca sus contenedores con un relleno rayado. Cuando se desmarca, los objetos eliminados siguen visibles y el filtro **Mostrar cambios** sigue funcionando.
- **Mantener visibles los objetos eliminados** (Hasta que se guarde el modelo): Cuánto tiempo permanecen los objetos eliminados en el Explorador TOM. Consulta [Mantener visibles los objetos eliminados entre guardados](#keeping-deleted-objects-across-saves).
- **Agrupar los objetos eliminados bajo un nodo "Deleted objects"** (desactivado): Muestra juntos, bajo un solo nodo, los objetos eliminados de un contenedor, en lugar de mostrarlos por separado donde estaban antes. Consulta [Agrupar los objetos eliminados bajo un solo nodo](#gathering-deleted-objects-under-one-node).
- **Marcar las propiedades con cambios sin guardar en el panel Propiedades** (activado): tiñe las filas de las propiedades modificadas en la vista de propiedades. Si se desmarca, el filtro **Mostrar cambios** de la vista de propiedades seguirá funcionando.

Consulta @preferences para ver las demás preferencias de esta página. Los colores que se usan para los objetos agregados se pueden ajustar para usuarios con daltonismo en **Herramientas > Preferencias > Interfaz de usuario > Accesibilidad**.

## Scripts

La misma información y las mismas operaciones también están disponibles para los [C# Scripts](xref:csharp-scripts) y las macros, lo que permite que un C# Script inspeccione lo que ha cambiado y revierta parte de un modelo sin afectar al resto.

Todos los objetos del modelo exponen los siguientes miembros:

- `HasUnsavedChanges` devuelve `true` cuando el objeto, o cualquiera de los elementos que contiene, difiere del último estado guardado. En el objeto `Model`, esto indica si el modelo tiene cambios sin guardar.
- `Revert()` devuelve el objeto y todo lo que contiene al estado guardado, en un único paso que se puede deshacer. El mismo método existe en colecciones como `Selected.Measures` y en `Model` para todo el modelo. Si falla una parte de la reversión, se genera una excepción que enumera lo que no se pudo restaurar.
- `Revert("PropertyName")` revierte una sola propiedad a su valor guardado; por ejemplo, `Revert("Expression")` o `Revert("Annotations[MyAnnotation]")`. No hace nada cuando la propiedad no ha cambiado.

Los contenedores, como las tablas, las jerarquías y los roles, exponen una colección `DeletedObjects` que enumera los objetos que se eliminaron de ellos en la sesión actual. Cada entrada tiene `Name`, `ObjectType` y `Parent`, además de un método `Restore()`. Llamar a `Restore()` en la colección restaura todos ellos a la vez.

En el Explorador TOM, se puede acceder a los objetos eliminados que están seleccionados actualmente mediante `Selected.Deleted`. Como los objetos eliminados no son objetos del modelo, nunca aparecen en `Selected.Measures`, `Selected.Columns` ni en los demás accesores.

```csharp
// List the measures with unsaved changes in the selected tables:
Selected.Tables
    .SelectMany(t => t.Measures)
    .Where(m => m.HasUnsavedChanges)
    .Output();

// Revert only the format strings of the selected measures, keeping their other edits:
Selected.Measures.Revert("FormatString");

// Put an entire table back to its saved state:
Model.Tables["Sales"].Revert();

// Bring back everything that was deleted from the selected table:
Selected.Table.DeletedObjects.Restore();

// Restore the deleted objects currently selected in the TOM Explorer:
Selected.Deleted.Restore();
```
