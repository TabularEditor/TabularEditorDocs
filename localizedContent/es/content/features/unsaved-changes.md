---
uid: unsaved-changes
title: Indicadores de cambios sin guardar
author: Daniel Otykier
updated: 2026-09-23
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

Tabular Editor 3 marca los objetos y las propiedades que difieren de la última versión guardada del modelo. Esto incluye los cambios realizados mediante [C# Scripts](xref:csharp-scripts), macros y el [Asistente de IA](xref:ai-assistant). La marca desaparece al guardar, revertir o deshacer el cambio.

Los indicadores aparecen en dos lugares:

- En el [Explorador TOM](xref:tom-explorer-view), los objetos modificados se muestran con una fila coloreada y una insignia en el icono: naranja (editado), verde (agregado) y rojo (eliminado). Estos son los colores de la vista de comparación del modelo que se muestra al desplegar.
- En la [vista de propiedades](xref:properties-view), las propiedades modificadas muestran una fila en naranja claro.

![Explorador TOM con medidas editadas, agregadas y eliminadas resaltadas, y la vista de propiedades con la fila de Descripción modificada resaltada](~/content/assets/images/unsaved-changes/overview.png)

Ambas vistas tienen un botón **Mostrar cambios** en la barra de herramientas y un comando **Revertir** en el menú contextual.

> [!NOTE]
> Los indicadores registran los cambios con respecto al origen desde el que se cargó el modelo o en el que se guardó por última vez. Desplegar el modelo en otra base de datos no las borra.

## Indicadores de cambios en el Explorador TOM

Cada objeto del árbol se marca según el cambio que tenga desde el último guardado:

- Los objetos **editados** muestran una fila en naranja claro y una insignia con un punto naranja. Esto abarca cualquier propiedad modificada, incluidos los cambios en un subobjeto que no tiene nodo en el árbol, como la política de actualización de una tabla o la configuración de `AlternateOf` de una columna.
- Los objetos **agregados** reciben una fila verde claro y una insignia verde con un **+**. Una tabla nueva y todas sus columnas nuevas aparecen en verde. Editar un objeto agregado no hace que pase de verde a naranja.
- Los objetos **eliminados** muestran una fila en rojo claro, un distintivo rojo con **−** y el nombre tachado. Consulta [Objetos eliminados](#deleted-objects).

Las tablas, las carpetas de visualización, los grupos de tablas y el nodo **Modelo** muestran un relleno rayado cuando algo que contienen ha cambiado. La insignia del icono es verde cuando todos los cambios bajo ellos son adiciones, y naranja en caso contrario.

Dentro de una selección, el resaltado de la selección tiene prioridad sobre el color de la fila, y la insignia del icono sigue marcando los objetos modificados. Los distintivos de error y advertencia tienen prioridad sobre el distintivo de cambio.

> [!TIP]
> Si te cuesta distinguir las filas verdes de las rojas, selecciona **Modo de daltonismo** en el grupo **Accesibilidad**, en **Herramientas > Preferencia > Tabular Editor > Interfaz de usuario**. Los objetos agregados se muestran entonces en verde azulado en lugar de verde, tanto aquí como en la vista de comparación del modelo.

### Mostrar cambios

El botón **Mostrar cambios** de la barra de herramientas del Explorador TOM filtra el árbol para mostrar los objetos con cambios no guardados, además de las tablas, carpetas y grupos que los contienen. Mientras el filtro esté activo, el título de la vista muestra **Explorador TOM (Changed)**.

![Explorador TOM con el filtro Mostrar cambios activo, que muestra solo los objetos modificados y sus contenedores](~/content/assets/images/unsaved-changes/tom-explorer-show-changes.png)

El filtro se combina con los demás conmutadores de la barra de herramientas y con el cuadro de búsqueda. Por ejemplo, al ocultar columnas con **Ctrl+2** también se ocultan las columnas modificadas en la vista filtrada.

## Indicadores de cambios en la vista de propiedades

Cuando seleccionas un objeto modificado, las propiedades modificadas se resaltan con la misma fila en color naranja claro. Una fila contraída que contiene un subobjeto, como la fila **KPI** de una medida o la fila **política de actualización** de una tabla, se marca cuando cambia algo dentro del subobjeto. En las filas indexadas, como **Anotaciones**, solo se marca la anotación modificada. Cuando se seleccionan varios objetos, una fila de propiedad se marca si alguno de los objetos seleccionados cambió esa propiedad.

El botón **Mostrar cambios** de la barra de herramientas de la vista de propiedades oculta las filas sin cambios. Mientras el filtro está activo, el título de la vista es **Propiedades (modificadas)**.

![Vista de propiedades con el filtro Mostrar cambios activo, que muestra solo las propiedades modificadas](~/content/assets/images/unsaved-changes/properties-show-changes.png)

## Revertir cambios

**Archivo > Recargar desde disco** descarta todos los cambios no guardados y vuelve a cargar el modelo desde su origen. Si el modelo se abrió desde un servidor, el comando es **Archivo > Recargar desde el servidor**. **Revertir** deshace los cambios individuales y deja intactos todos los demás cambios no guardados.

Una reversión funciona igual que introducir el valor anterior o volver a crear manualmente el objeto eliminado: Tabular Editor actualiza las referencias DAX y los objetos dependientes, y añade la reversión a la pila de deshacer como un único paso. Para deshacer una reversión, usa **Editar > Deshacer** (**Ctrl+Z**).

### Revertir una sola propiedad

Haz clic con el botón derecho en una fila marcada de la vista de propiedades y elige **Revertir** para restaurar su valor guardado. Los demás cambios no guardados del objeto permanecen intactos.

![Vista de propiedades con las filas Descripción y Cadena de formato modificadas y el comando Revertir en el menú contextual](~/content/assets/images/unsaved-changes/revert-property.png)

**Revertir** solo está habilitado en las filas con cambios no guardados. Con varios objetos seleccionados, **Revertir** en una fila combinada restaura la propiedad en todos los objetos seleccionados que la hayan modificado, como un único paso de deshacer. **Revertir** en una fila contenedora como **Anotaciones** restaura todas sus anotaciones: las anotaciones editadas vuelven a sus valores guardados, las anotaciones agregadas se eliminan y las anotaciones eliminadas se restauran.

### Revertir un objeto o una rama del modelo

Haz clic con el botón derecho en un objeto marcado del Explorador TOM y elige **Revertir** para devolver el objeto y todo lo que hay debajo de él a su último estado guardado. **Revertir** también está disponible en tablas, carpetas de visualización, grupos de tablas y en el nodo **Modelo** cuando algo debajo de ellos ha cambiado. **Revertir** en el nodo **Modelo** descarta todos los cambios no guardados del modelo, como un único paso de deshacer.

![Menú contextual del Explorador TOM en una medida editada con la opción Revertir](~/content/assets/images/unsaved-changes/revert-object.png)

Cuando reviertes un objeto o una rama:

- Las propiedades editadas vuelven a sus valores guardados.
- Los objetos agregados desde el último guardado se eliminan.
- Los objetos eliminados desde el último guardado se restauran tal como estaban guardados, incluidos el KPI de una medida eliminada o los niveles de jerarquía y las relaciones de una columna eliminada.
- Los objetos de otras partes del modelo conservan sus cambios sin guardar.

Si parte de una reversión falla, un mensaje de **Reversión incompleta** enumera los fallos y Tabular Editor aplica el resto. Por ejemplo, no se puede restaurar un objeto eliminado si otro objeto ya usa su nombre y no puede eliminarse.

## Objetos eliminados

Eliminar un objeto no lo quita del Explorador TOM. Hasta que guardes el modelo, el objeto permanece en su sitio con el nombre tachado, una fila de color rojo claro y una insignia roja **−**. Cuando se muestran las columnas de información, la columna **Tipo de objeto** muestra, por ejemplo, **Medida (Eliminada)**.

![Explorador TOM con una medida eliminada tachada en una fila roja](~/content/assets/images/unsaved-changes/deleted-objects.png)

Haz clic con el botón derecho en un objeto eliminado y elige **Restaurar** para devolverlo al estado en que estaba cuando lo eliminaste. Si el objeto tenía cambios sin guardar antes de que lo eliminaras, esos cambios también se restauran y siguen marcados, y puedes revertirlos por separado. Para restaurar varios objetos eliminados en un solo paso, selecciónalos todos y elige **Restaurar**.

No puedes editar, cambiar el nombre, arrastrar ni desplegar un objeto eliminado, y nunca es un destino válido para soltar o pegar. Seleccionar un objeto eliminado no selecciona ningún objeto del modelo, por lo que la vista de propiedades no muestra nada y el menú contextual solo incluye **Restaurar**. Una selección que mezcla objetos eliminados y activos no muestra ni **Restaurar** ni los comandos habituales del objeto.

Los C# Script acceden a los objetos eliminados seleccionados a través de `Selected.Deleted`, como se describe en [Scripting](#scripting).

### Agrupar los objetos eliminados en un solo nodo

Si seleccionas **Agrupar objetos eliminados bajo un nodo "Objetos eliminados"** en la sección **Cambios no guardados** de **Herramientas > Preferencias > Tabular Editor > Explorador TOM**, los objetos eliminados de una tabla, jerarquía, rol o grupo de tablas se muestran bajo un único nodo **Objetos eliminados** al final de su contenedor, independientemente de las carpetas de visualización en las que estuvieran. El nodo tiene una fila roja y una insignia de eliminado, y los objetos que contiene aparecen tachados. Haz clic con el botón derecho en el nodo y elige **Restaurar** para restaurar todo lo que contiene en un solo paso.

![Explorador TOM con una medida eliminada bajo un nodo Objetos eliminados al final de su tabla](~/content/assets/images/unsaved-changes/deleted-objects-group.png)

### Conservar los objetos eliminados entre guardados

De forma predeterminada, los objetos eliminados permanecen visibles hasta que guardas. Para cambiarlo, establece la preferencia **Mantener visibles los objetos eliminados** en una de sus otras dos opciones:

- **Nunca**: El Explorador TOM oculta los objetos eliminados inmediatamente. Para restaurarlos, usa **Revertir** en su contenedor o **Editar > Deshacer**.
- **Hasta que se cierre el modelo**: Los objetos eliminados permanecen visibles y se pueden restaurar durante toda la sesión de edición, incluso después de guardar, mientras su eliminación siga en la pila de deshacer. Restaurar un objeto eliminado antes del último guardado lo vuelve a crear y queda marcado como añadido. Un objeto que creaste y eliminaste en la misma sesión aparece solo si lo editaste o guardaste el modelo mientras existía.

## Cuándo se limpian los indicadores

Una marca refleja la diferencia actual con respecto al último estado guardado. Guardar el modelo en un archivo, una carpeta o una base de datos borra todas las marcas de una vez. La marca también se borra al revertir el cambio, al deshacer hasta volver al último guardado o al restablecer manualmente una propiedad a su valor guardado. Si deshaces más allá del último guardado, los objetos que se deshicieron se marcan como modificados, y al rehacer un cambio se restaura su marca.

## Preferencias

La configuración de los indicadores se encuentra en la sección **Cambios no guardados** de **Herramientas > Preferencias > Tabular Editor > Explorador TOM**:

![Sección de cambios no guardados de la página de preferencias del Explorador TOM](~/content/assets/images/unsaved-changes/preferences.png)

- **Marcar objetos con cambios no guardados** (habilitado): Colorea las filas, añade insignias a los iconos de los objetos agregados, editados y eliminados en el Explorador TOM, y aplica un tramado a sus contenedores. No afecta a la visibilidad de los objetos eliminados ni a **Mostrar cambios**.
- **Mantener visibles los objetos eliminados** (Hasta que se guarde el modelo): Cuánto tiempo permanecen los objetos eliminados en el Explorador TOM. Consulta [Mantener los objetos eliminados entre guardados](#keeping-deleted-objects-across-saves).
- **Agrupar objetos eliminados en un nodo "Objetos eliminados"** (deshabilitado): Agrupa los objetos eliminados de un contenedor bajo un único nodo. Consulta [Agrupar los objetos eliminados bajo un único nodo](#gathering-deleted-objects-under-one-node).
- **Marcar propiedades con cambios no guardados en el panel de propiedades** (habilitado): Colorea las filas de las propiedades modificadas en la vista de propiedades. No afecta a **Mostrar cambios** en la vista de propiedades.

Consulta @preferences para ver las demás preferencias de esta página.

## Scripts

Los [C# Scripts](xref:csharp-scripts) y las macros pueden leer la misma información sobre los cambios y ejecutar las mismas operaciones de reversión mediante estos miembros, que tiene cada objeto del modelo:

- `HasUnsavedChanges` devuelve `true` cuando el objeto, o cualquier elemento por debajo de él, difiere del último estado guardado. En el objeto `Model`, indica si el modelo tiene cambios no guardados.
- `Revert()` revierte el objeto y sus elementos secundarios en un único paso de deshacer. El método también existe en colecciones como `Selected.Measures` y en `Model` para todo el modelo. Si una parte de la reversión falla, lanza una excepción que enumera las partes que no pudo revertir.
- `Revert("PropertyName")` restaura una propiedad a su valor guardado, por ejemplo `Revert("Expression")` o `Revert("Annotations[MyAnnotation]")`. No hace nada si la propiedad no ha cambiado.

Contenedores como las tablas, las jerarquías y los roles tienen una colección `DeletedObjects` que enumera los objetos que se han eliminado de ellos en la sesión actual. Cada entrada tiene `Name`, `ObjectType` y `Parent`, además de un método `Restore()`. `Restore()` en la colección restaura todos los elementos.

`Selected.Deleted` devuelve los objetos eliminados seleccionados en el Explorador TOM. Los objetos eliminados no aparecen en `Selected.Measures`, `Selected.Columns` ni en los otros accesores.

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
