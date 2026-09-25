---
uid: unsaved-changes
title: Indicadores de cambios sin guardar
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

# Indicadores de cambios sin guardar

Tabular Editor 3 marca todos los objetos y propiedades que difieren de la última versión guardada del modelo. Los cambios se marcan tanto si se hicieron a mano como mediante un [C# Script](xref:csharp-scripts), una macro o el [Asistente de IA](xref:ai-assistant), y las marcas desaparecen en cuanto se guarda, se revierte o se deshace el cambio.

Los indicadores aparecen en dos lugares:

- En el [Explorador TOM](xref:tom-explorer-view), los objetos modificados aparecen con una fila resaltada y una insignia en el icono, con los mismos colores que la vista de comparación de modelos que se muestra al desplegar: naranja para los objetos editados, verde para los objetos agregados y rojo para los objetos eliminados. Los objetos eliminados siguen siendo visibles, tachados, en el lugar que ocupaban, y las tablas y carpetas que contienen objetos modificados aparecen con un relleno rayado.
- En la [vista de propiedades](xref:properties-view), las propiedades que difieren del modelo guardado reciben una fila sombreada en naranja.

![Cambios sin guardar en el Explorador TOM y la vista de propiedades](~/content/assets/images/unsaved-changes/overview.png)

Ambas vistas tienen un botón **Mostrar cambios** en la barra de herramientas que filtra la vista para mostrar solo lo que ha cambiado, y ambas ofrecen, al hacer clic con el botón derecho, la opción **Revertir**, que devuelve una sola propiedad, un solo objeto o toda una rama del modelo a su estado guardado, sin afectar a ningún otro cambio sin guardar.

> [!NOTE]
> Los indicadores registran los cambios con respecto al origen desde el que se cargó el modelo o en el que se guardó por última vez. Desplegar el modelo en otra base de datos no los borra, ya que el modelo cargado sigue siendo distinto de su propio origen.

## Indicadores de cambios en el Explorador TOM

Cada objeto del árbol se resalta y recibe una insignia según lo que le haya ocurrido desde la última vez que se guardó:

- Los objetos **editados** reciben una fila de color naranja claro y una insignia con un punto naranja en el icono. Esto incluye cualquier propiedad modificada, incluidos los cambios en un subobjeto que no tiene su propio nodo en el árbol, como la política de actualización de una tabla o la configuración de _Alternate Of_ de una columna.
- Los objetos **agregados** reciben una fila verde claro y una insignia verde con un **+**. Una tabla nueva y todas sus columnas nuevas aparecen en verde. Editar una propiedad de un objeto recién agregado mantiene el objeto en verde, ya que sigue siendo nuevo en comparación con el modelo guardado.
- Los objetos **eliminados** aparecen con una fila de color rojo claro y una insignia roja **−**, y su nombre se muestra tachado. Consulta [Objetos eliminados](#deleted-objects) más abajo.

Las tablas, las carpetas de visualización, los grupos de tablas y el nodo **Modelo** también se marcan cuando cambia algo por debajo de ellos: su fila recibe un relleno rayado y su icono muestra la insignia de ese cambio. Verde cuando solo se han agregado objetos; naranja en caso contrario. Esto te permite seguir los cambios en un árbol contraído o usar el filtro **Mostrar cambios** para ver solo los objetos modificados.

Cuando se selecciona un objeto, el resaltado normal de selección tiene prioridad sobre el tinte, por lo que una selección múltiple sigue siendo legible. La insignia del icono sigue marcando los objetos modificados dentro de la selección. Las insignias de error y advertencia también tienen prioridad sobre la insignia de cambio, por lo que un objeto con un error semántico conserva su insignia de error incluso cuando tiene cambios sin guardar.

> [!TIP]
> Si te cuesta distinguir las filas verdes de las rojas, activa **Modo para daltónicos** en **Herramientas > Preferencias > Interfaz de usuario > Accesibilidad**. Los objetos agregados se marcan entonces en color verde azulado en lugar de verde, tanto aquí como en la vista de comparación de modelos.

### Mostrar cambios

El botón **Mostrar cambios** de la barra de herramientas del Explorador TOM filtra el árbol para mostrar solo los objetos con cambios sin guardar, junto con las tablas, carpetas y grupos necesarios para llegar a ellos. Mientras el filtro está activo, el título de la vista es **Explorador TOM (Con cambios)**.

![Filtro Mostrar cambios en el Explorador TOM](~/content/assets/images/unsaved-changes/tom-explorer-show-changes.png)

El filtro se aplica junto con los demás controles de alternancia de la barra de herramientas y el cuadro de búsqueda. Por ejemplo, al ocultar columnas con **Ctrl+2** también se ocultan las columnas modificadas en la vista filtrada.

## Indicadores de cambios en la vista de propiedades

Cuando seleccionas un objeto modificado, las propiedades que difieren del modelo guardado se muestran con el mismo tono naranja claro. Una fila contraída que contiene un subobjeto, como la fila **KPI** de una medida o la fila **política de actualización** de una tabla, se marca cuando cambia algo dentro del subobjeto. Para las filas indexadas, como **Anotaciones**, solo se marca la anotación individual que cambió.

Cuando se seleccionan varios objetos, una fila de propiedad se marca si alguno de los objetos seleccionados cambió esa propiedad.

El botón **Mostrar cambios** de la barra de herramientas de la vista de propiedades oculta todas las filas sin cambios, de modo que solo queden las propiedades modificadas. Mientras el filtro está activo, el título de la vista es **Propiedades (Con cambios)**.

![Filtro Mostrar cambios en la vista de propiedades](~/content/assets/images/unsaved-changes/properties-show-changes.png)

## Revertir cambios

**Archivo > Recargar desde disco** descarta de una sola vez todos los cambios sin guardar, al recargar desde su origen los metadatos del modelo. En un modelo abierto desde un servidor, el comando se llama **Recargar desde el servidor**. Las opciones de **Revertir** que aparecen más abajo deshacen cambios individuales y dejan intactos todos los demás cambios sin guardar.

Una operación de revertir se comporta exactamente igual que volver a escribir el valor anterior o recrear manualmente el objeto eliminado: las referencias DAX se corrigen, los objetos dependientes se recalculan y toda la operación se convierte en un único paso en la pila de deshacer. Si cambias de idea, con **Editar > Deshacer** (**Ctrl+Z**) restauras el cambio revertido.

### Revertir una sola propiedad

Haz clic con el botón derecho en una fila marcada en la vista de propiedades y elige **Revertir** para restablecer esa propiedad al valor que tenía la última vez que guardaste. Todos los demás cambios sin guardar del objeto se mantienen.

![Revertir una sola propiedad](~/content/assets/images/unsaved-changes/revert-property.png)

La opción **Revertir** solo está habilitada en las filas que tienen cambios sin guardar. Si seleccionas varios objetos, **Revertir** en una fila combinada revierte la propiedad en todos los objetos seleccionados que la hayan cambiado, como un único paso que puedes deshacer. **Revertir** en una fila de contenedor como **Anotaciones** revierte todas las anotaciones de una vez: las anotaciones editadas vuelven a sus valores guardados, las anotaciones agregadas se eliminan y las anotaciones eliminadas reaparecen.

### Revertir un objeto o una rama del modelo

Haz clic con el botón derecho en un objeto marcado en el Explorador TOM y elige **Revertir** para devolver el objeto y todo lo que hay debajo de él al estado en el que estaba la última vez que guardaste. **Revertir** también está disponible en tablas, carpetas de visualización, grupos de tablas y en el nodo **Modelo**, aunque esos elementos no estén marcados, siempre que algo que esté debajo haya cambiado. Si eliges **Revertir** en el nodo **Modelo**, descartas todos los cambios sin guardar del modelo como un único paso que puedes deshacer.

![Revertir un objeto en el Explorador TOM](~/content/assets/images/unsaved-changes/revert-object.png)

Al revertir un objeto o una rama del modelo:

- Las propiedades editadas vuelven a sus valores guardados.
- Los objetos agregados desde el último guardado se eliminan.
- Los objetos eliminados desde el último guardado vuelven exactamente como se guardaron, incluido el KPI de una medida eliminada o los niveles de jerarquía y las relaciones de una columna eliminada.
- Los objetos de otras partes del modelo conservan sus cambios sin guardar.

Todo lo que no se pueda revertir se enumera en **Mensajes** mediante un mensaje de **Reversión incompleta**, y el resto de la reversión se mantiene. Esto sucede, por ejemplo, cuando el nombre de un objeto eliminado se ha asignado después a un objeto nuevo que no se puede eliminar.

## Objetos eliminados

Al eliminar un objeto, este no se quita del Explorador TOM. Hasta que se guarde el modelo, el objeto permanece donde estaba, tachado en una fila de color rojo claro, con una insignia roja **−** en el icono. Cuando se muestran las columnas de información, la columna **Tipo de objeto** muestra, por ejemplo, **medida (eliminada)**. Así, una eliminación es tan fácil de detectar como una edición.

![Objetos eliminados en el Explorador TOM](~/content/assets/images/unsaved-changes/deleted-objects.png)

Haz clic con el botón derecho en un objeto eliminado y elige **Restaurar** para devolverlo exactamente al estado en que estaba justo antes de eliminarlo. Si el objeto tenía ediciones sin guardar antes de eliminarse, estas reaparecen con él y siguen marcadas, para que puedan revertirse por separado. Puedes seleccionar varios objetos eliminados y restaurarlos en un solo paso.

Los objetos eliminados son marcadores de posición, no objetos del modelo:

- No se pueden editar, cambiar de nombre, arrastrar ni expandir, y nunca se pueden usar como destino para arrastrar y soltar o pegar.
- Seleccionarlos no selecciona ningún objeto del modelo. La vista de propiedades no muestra nada, y el menú contextual solo ofrece **Restaurar**.
- Una selección que mezcla objetos eliminados y activos no ofrece ni **Restaurar** ni las acciones habituales de los objetos.
- Desaparecen en cuanto se guarda el modelo.

Los C# Scripts pueden acceder a los objetos eliminados seleccionados mediante `Selected.Deleted`. Consulta [Scripting](#scripting) más abajo.

### Agrupar los objetos eliminados en un solo nodo

Si prefieres no mezclar los objetos eliminados con los activos, activa **Agrupar los objetos eliminados bajo un nodo "Objetos eliminados"** en **Herramientas > Preferencias > Explorador TOM > Cambios no guardados**. Los objetos eliminados de una tabla, jerarquía, rol o grupo de tablas se muestran entonces juntos bajo un único nodo **Objetos eliminados** al final de su contenedor, independientemente de las carpetas de visualización en las que estuvieran antes. El nodo adopta el resaltado rojo y su propia insignia de eliminado, y los objetos que contiene aparecen tachados. Haz clic con el botón derecho en el nodo y elige **Restaurar** para recuperar todo lo que contiene en un solo paso.

![Objetos eliminados agrupados bajo un solo nodo](~/content/assets/images/unsaved-changes/deleted-objects-group.png)

### Conservar los objetos eliminados entre guardados

De forma predeterminada, los objetos eliminados permanecen visibles hasta que se guarda el modelo, ya que son cambios no guardados como cualquier otro. La preferencia **Mantener visibles los objetos eliminados** ofrece dos alternativas:

- **Nunca**: Los objetos eliminados desaparecen del Explorador TOM de inmediato. Aun así, pueden restaurarse con **Revertir** en su contenedor o con **Editar > Deshacer**.
- **Hasta que se cierre el modelo**: Los objetos eliminados siguen visibles durante toda la sesión de edición, incluso entre guardados, y se pueden restaurar. Restaurar un objeto que se eliminó antes del último guardado lo crea de nuevo, por lo que después queda marcado como objeto agregado. Los objetos que se crearon y se eliminaron entre dos guardados solo se conservan si en algún momento se editaron o se guardaron. Un objeto que se creó y se eliminó sin llegar a modificarse no deja rastro.

## Cuándo se limpian los indicadores

Un objeto o una propiedad pierde su marca cuando deja de diferir del último estado guardado del modelo. Esto sucede cuando:

- Se guarda el modelo, ya sea en un archivo, una carpeta o una base de datos. Todos los indicadores se limpian a la vez.
- El cambio se revierte, ya sea con **Revertir** en el Explorador TOM o en la vista de propiedades, o mediante **Archivo > Recargar desde disco** (**Recargar desde el servidor**), lo que descarta todos los cambios.
- El cambio se deshace con **Editar > Deshacer** hasta volver al punto del último guardado. Volver a aplicar el cambio hace que reaparezca la marca y, si se deshace _más allá_ del último guardado, se marcan en su lugar los objetos revertidos.
- Una propiedad se restablece manualmente a su valor original. Tabular Editor 3 compara el valor actual con el guardado, por lo que una edición sin cambios netos no cuenta como cambio.

## Preferencias

Los indicadores se pueden ajustar en **Herramientas > Preferencias > Explorador TOM**, en la sección **Cambios no guardados**:

![Preferencias de cambios no guardados](~/content/assets/images/unsaved-changes/preferences.png)

- **Marcar objetos con cambios no guardados** (activado): Tiñe las filas y añade una insignia a los iconos de los objetos agregados, editados y eliminados en el Explorador TOM, y marca sus contenedores con un relleno rayado. Si se desmarca, los objetos eliminados siguen visibles y el filtro **Mostrar cambios** sigue funcionando.
- **Mantener visibles los objetos eliminados** (Hasta que se guarde el modelo): Cuánto tiempo permanecen los objetos eliminados en el Explorador TOM. Consulta [Mantener los objetos eliminados entre guardados](#keeping-deleted-objects-across-saves).
- **Agrupar los objetos eliminados bajo un nodo "Objetos eliminados"** (desactivado): Muestra juntos los objetos eliminados de un contenedor bajo un único nodo, en lugar de mantener cada uno en su ubicación original. Consulta [Agrupar los objetos eliminados bajo un único nodo](#gathering-deleted-objects-under-one-node).
- **Marcar las propiedades con cambios sin guardar en el panel Propiedades** (activado): Tiñe las filas de las propiedades modificadas en la vista de propiedades. Cuando esta opción no está marcada, el filtro **Mostrar cambios** de la vista de propiedades sigue funcionando.

Consulta @preferences para ver las demás preferencias de esta página. Los colores utilizados para los objetos añadidos se pueden ajustar para personas con daltonismo en **Herramientas > Preferencias > Interfaz de usuario > Accesibilidad**.

## Scripts

La misma información y las mismas operaciones están disponibles para los [C# Scripts](xref:csharp-scripts) y las macros, lo que permite que un C# Script inspeccione qué ha cambiado y revierta parte de un modelo sin tocar el resto.

Cada objeto del modelo expone los siguientes miembros:

- `HasUnsavedChanges` devuelve `true` cuando el objeto, o cualquier elemento por debajo de él, difiere del último estado guardado. En el objeto `Model`, esto indica si el modelo tiene algún cambio no guardado.
- `Revert()` restaura el objeto y todo lo que hay por debajo de él al estado guardado, en un único paso que se puede deshacer. El mismo método existe en colecciones como `Selected.Measures` y en `Model` para todo el modelo. Si falla parte de la restauración, se genera una excepción que enumera lo que no se pudo restaurar.
- `Revert("PropertyName")` restaura una sola propiedad a su valor guardado, por ejemplo `Revert("Expression")` o `Revert("Annotations[MyAnnotation]")`. No hace nada si la propiedad no ha cambiado.

Los contenedores, como tablas, jerarquías y roles, exponen una colección `DeletedObjects` que enumera los objetos eliminados de estos contenedores en la sesión actual. Cada entrada tiene `Name`, `ObjectType` y `Parent`, además de un método `Restore()`. Llamar a `Restore()` en la colección restaura todos los elementos de una vez.

En el Explorador TOM, los objetos eliminados que estén seleccionados actualmente están disponibles a través de `Selected.Deleted`. Dado que los objetos eliminados no son objetos del modelo, nunca aparecen en `Selected.Measures`, `Selected.Columns` ni en los demás accesores.

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
