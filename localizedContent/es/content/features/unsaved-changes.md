---
uid: unsaved-changes
title: Indicadores de cambios sin guardar
author: Daniel Otykier
updated: 2026-10-11
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

Tabular Editor 3 marca los objetos y las propiedades que difieren de la última versión guardada del modelo. Esto incluye cambios procedentes de [C# Script](xref:csharp-scripts), macros y el [Asistente de IA](xref:ai-assistant). La marca desaparece cuando guarda, revierte o deshace el cambio.

Los indicadores aparecen en dos lugares:

- En el [Explorador TOM](xref:tom-explorer-view), los objetos modificados se muestran en una fila de color y con una insignia con un icono: naranja (editado), verde (añadido) y rojo (eliminado). Estos son los colores de la vista de comparación de modelos que se muestra al realizar la implementación.
- En la [vista Propiedades](xref:properties-view), las propiedades modificadas se muestran en una fila de color naranja claro.

![Explorador TOM con medidas modificadas, añadidas y eliminadas resaltadas, y la vista Propiedades con la fila Descripción modificada resaltada](~/content/assets/images/unsaved-changes/overview.png)

Ambas vistas tienen un botón de la barra de herramientas **Mostrar cambios** y un comando **Revertir** al que se accede haciendo clic con el botón derecho.

> [!NOTE]
> Los indicadores hacen un seguimiento de los cambios en relación con el origen desde el que se cargó el modelo o en el que se guardó por última vez. Implementar el modelo en una base de datos diferente no los elimina.

## Indicadores de cambios en el Explorador TOM

Cada objeto del árbol se marca según su cambio desde la última vez que se guardó:

- Los objetos **editados** se muestran en una fila de color naranja claro y con una insignia de punto naranja. Esto abarca cualquier propiedad modificada, incluidos los cambios en un subobjeto que no tenga ningún nodo en el árbol, como la directiva de actualización de una tabla o la configuración `AlternateOf` de una columna.
- Los objetos **añadidos** se muestran en una fila de color verde claro y con una insignia **+** de color verde. Una nueva tabla y todas sus nuevas columnas aparecen en verde. Editar un objeto añadido no hace que cambie de verde a naranja.
- Los objetos **eliminados** tienen una fila de color rojo claro, una insignia roja **−** y el nombre tachado. Consulte [Objetos eliminados](#deleted-objects).

Las tablas, las carpetas de visualización, los grupos de tablas y el nodo **Modelo** se rellenan con un sombreado cuando se ha modificado algo que está por debajo de ellos. Su insignia de icono es verde cuando todo lo que ha cambiado debajo de ellos es una adición, y naranja en caso contrario.

Dentro de una selección, el resaltado de la selección tiene prioridad sobre el color de la fila y el distintivo del icono sigue marcando los objetos modificados. Las insignias de error y advertencia tienen prioridad sobre la insignia de cambio.

> [!TIP]
> Si le resulta difícil distinguir las filas verdes de las rojas, seleccione **Modo daltonismo** en el grupo **Accesibilidad** en **Herramientas > Preferencias > Tabular Editor > Interfaz de usuario**. Los objetos añadidos aparecen entonces en color turquesa en lugar de verde, tanto aquí como en la vista de comparación de modelos.

### Mostrar cambios

El botón **Mostrar cambios** de la barra de herramientas del Explorador TOM filtra el árbol para mostrar los objetos con cambios sin guardar, además de las tablas, carpetas y grupos que los contienen. Mientras el filtro está activo, el título de la vista dice **Explorador TOM (Modificado)**.

![TOM Explorer con el filtro Mostrar cambios activo, mostrando solo los objetos modificados y sus contenedores](~/content/assets/images/unsaved-changes/tom-explorer-show-changes.png)

El filtro se combina con los demás botones de activación de la barra de herramientas y con el cuadro de búsqueda. Por ejemplo, ocultar columnas con **Ctrl+2** también oculta las columnas modificadas de la vista filtrada.

## Indicadores de cambios en la vista Propiedades

Cuando seleccionas un objeto modificado, las propiedades modificadas se muestran en la misma fila de color naranja claro. Una fila contraída que contiene un subobjeto, como la fila **KPI** de una medida o la fila **Política de actualización** de una tabla, se marca cuando se ha modificado algo dentro del subobjeto. En el caso de las filas indexadas, como **Anotaciones**, solo se marca la anotación modificada. Cuando se seleccionan varios objetos, se marca una fila de propiedades si alguno de los objetos seleccionados ha cambiado esa propiedad.

El botón **Mostrar cambios** de la barra de herramientas de la vista Propiedades oculta las filas que no han cambiado. Mientras el filtro está activo, el título de la vista dice **Propiedades (modificadas)**.

![Vista de propiedades con el filtro Mostrar cambios activo, que muestra solo las propiedades modificadas](~/content/assets/images/unsaved-changes/properties-show-changes.png)

## Deshacer cambios

**Archivo > Recargar desde el disco** descarta todos los cambios sin guardar y recarga el modelo desde su origen. Para un modelo abierto desde un servidor, el comando es **Archivo > Volver a cargar desde el servidor**. **Revertir** deshace cambios individuales y deja todos los demás cambios sin guardar en su sitio.

Una reversión funciona como si se introdujera el valor anterior o se volviera a crear manualmente el objeto eliminado: Tabular Editor actualiza las referencias DAX y los objetos dependientes, y añade la reversión a la pila de deshacer como un solo paso. Para deshacer una reversión, use **Editar > Deshacer** (**Ctrl+Z**).

### Revertir una sola propiedad

Haga clic derecho en una fila marcada en la vista Propiedades y elija **Revertir** para restaurar su valor guardado. Los demás cambios sin guardar del objeto se mantienen.

![Vista de propiedades con las filas «Descripción» y «Cadena de formato» modificadas y el comando «Revertir» al hacer clic con el botón derecho](~/content/assets/images/unsaved-changes/revert-property.png)

**Revertir** solo está habilitado en las filas con cambios sin guardar. Con varios objetos seleccionados, **Revertir** en una fila combinada revierte la propiedad en todos los objetos seleccionados que la hayan cambiado, como un solo paso de deshacer. **Revertir** en una fila de contenedor como **Anotaciones** revierte todas sus anotaciones: las anotaciones editadas vuelven a sus valores guardados, las anotaciones añadidas se eliminan y las anotaciones eliminadas se restauran.

### Revertir un objeto o una rama del modelo

Haga clic derecho en un objeto marcado en el Explorador TOM y elija **Revertir** para devolver el objeto y todo lo que hay debajo de él a su último estado guardado. **Revertir** también está disponible en tablas, carpetas de visualización, grupos de tablas y en el nodo **Modelo** cuando algo situado debajo de ellos ha cambiado. **Revertir** en el nodo **Modelo** descarta todos los cambios sin guardar en el modelo, como un solo paso de deshacer.

![Menú contextual del Explorador TOM en una medida editada con la opción Revertir](~/content/assets/images/unsaved-changes/revert-object.png)

Cuando revierte un objeto o una rama:

- Las propiedades editadas vuelven a sus valores guardados.
- Se eliminan los objetos añadidos desde el último guardado.
- Los objetos eliminados desde el último guardado se restauran tal y como estaban guardados, incluidos el KPI de una medida eliminada o los niveles de jerarquía y las relaciones de una columna eliminada.
- Los objetos situados en otras partes del modelo conservan sus cambios sin guardar.

Si falla parte de una reversión, un mensaje de **Reversión incompleta** enumera los fallos y Tabular Editor aplica el resto. Por ejemplo, un objeto eliminado no se puede restaurar si otro objeto utiliza ahora su nombre y no se puede eliminar.

## Objetos eliminados

Eliminar un objeto no lo quita del Explorador TOM. Hasta que guarde el modelo, el objeto permanece en su lugar con el nombre tachado, una fila de color rojo claro y una insignia roja **−**. Cuando se muestran las columnas de información, la columna **Tipo de objeto** indica, por ejemplo, **Medida (eliminada)**.

![Explorador TOM con una medida eliminada tachada en una fila roja](~/content/assets/images/unsaved-changes/deleted-objects.png)

Haga clic derecho en un objeto eliminado y elija **Restaurar** para restaurarlo tal y como estaba cuando lo eliminó. Si el objeto tenía cambios no guardados antes de eliminarlo, los cambios también se restauran y permanecen marcados, y puede revertirlos por separado. Para restaurar varios objetos eliminados en un solo paso, selecciónelos todos y elija **Restaurar**.

No puede editar, cambiar el nombre, arrastrar ni expandir un objeto eliminado, y nunca es un destino para soltar ni pegar. Al seleccionar un objeto eliminado no se selecciona un objeto del modelo, por lo que la vista Propiedades no muestra nada y el menú contextual solo contiene la opción **Restaurar**. Una selección que combina objetos eliminados y activos no tiene ni **Restaurar** ni los comandos de objetos normales.

Los scripts de C# acceden a los objetos eliminados seleccionados a través de `Selected.Deleted`, como se describe en [Scripting](#scripting).

### Agrupar objetos eliminados bajo un solo nodo

Si selecciona **Reunir los objetos eliminados bajo un nodo «Objetos eliminados»** en la sección **Cambios no guardados** de **Herramientas > Preferencias > Tabular Editor > Explorador de TOM**, los objetos eliminados de una tabla, una jerarquía, un rol o un grupo de tablas se mostrarán bajo un único nodo **Objetos eliminados** al final de su contenedor, independientemente de las carpetas de visualización en las que se encontraran. El nodo tiene una fila roja y una insignia de «Eliminado», y los objetos que se encuentran debajo están tachados. Haga clic derecho en el nodo y elija **Restaurar** para restaurar todo lo que hay debajo de él en un solo paso.

![Explorador TOM con una medida eliminada incluida en un nodo de Objetos eliminados al final de su tabla](~/content/assets/images/unsaved-changes/deleted-objects-group.png)

### Conservar los objetos eliminados entre guardados

De forma predeterminada, los objetos eliminados permanecen visibles hasta que guarda. Para cambiarlo, establezca la preferencia **Mantener visibles los objetos eliminados** en una de sus otras dos opciones:

- **Nunca**: El Explorador TOM oculta los objetos eliminados inmediatamente. Para restaurarlos, utilice **Revertir** en su contenedor o **Editar > Deshacer**.
- **Hasta que se cierre el modelo**: Los objetos eliminados permanecen visibles y se pueden restaurar durante toda la sesión de edición, incluso después de guardar, mientras su eliminación siga estando en la pila de deshacer. Al restaurar un objeto eliminado antes del último guardado, se vuelve a crear y se marca como añadido. Un objeto que haya creado y eliminado en la misma sesión solo aparecerá si lo editó o si guardó el modelo mientras existía.

## Cuándo desaparecen los indicadores

Una marca refleja la diferencia actual con respecto al último estado guardado. Al guardar el modelo en un archivo, una carpeta o una base de datos, se borran todas las marcas a la vez. Una marca también desaparece cuando se revierte el cambio, cuando se deshace hasta el punto del último guardado o cuando se vuelve a asignar manualmente a una propiedad su valor guardado. Si deshaces cambios más allá del último guardado, los objetos deshechos se marcan como modificados, y al rehacer un cambio se restaura su marca.

## Preferencias

La configuración de los indicadores se encuentra en la sección **Cambios no guardados** en **Herramientas > Preferencias > Tabular Editor > Explorador TOM**:

![Sección «Cambios sin guardar» de la página de preferencias del Explorador TOM](~/content/assets/images/unsaved-changes/preferences.png)

- **Marcar objetos con cambios sin guardar** (habilitado): Colorea las filas y coloca insignias en los iconos de los objetos añadidos, editados y eliminados en el Explorador TOM, y sombreada sus contenedores. No afecta a la visibilidad de los objetos eliminados ni a **Mostrar cambios**.
- **Mantener visibles los objetos eliminados** (hasta que se guarde el modelo): cuánto tiempo permanecen los objetos eliminados en el Explorador TOM. Consulte [Mantener los objetos eliminados entre guardados](#keeping-deleted-objects-across-saves).
- **Agrupar los objetos eliminados en un nodo «Objetos eliminados»** (desactivado): enumera los objetos eliminados de un contenedor en un solo nodo. Consulte [Agrupar objetos eliminados bajo un nodo](#gathering-deleted-objects-under-one-node).
- **Marcar las propiedades con cambios sin guardar en el panel «Propiedades»** (habilitado): Colorea las filas de las propiedades modificadas en la vista «Propiedades». No afecta a **Mostrar cambios** en la vista Propiedades.

Consulte @preferences para ver los demás ajustes de esta página.

## Secuencias de comandos

Los [scripts de C#](xref:csharp-scripts) y las macros pueden leer la misma información de cambios y ejecutar las mismas operaciones de reversión a través de estos miembros, que todos los objetos del modelo tienen:

- `HasUnsavedChanges` devuelve `true` cuando el objeto, o cualquier elemento por debajo de él, difiere del último estado guardado. En el objeto `Model`, devuelve si el modelo tiene algún cambio sin guardar.
- `Revert()` revierte el objeto y sus elementos secundarios como un solo paso de deshacer. El método también existe en colecciones como `Selected.Measures` y en `Model` para todo el modelo. Si falla alguna parte de la reversión, se produce una excepción que enumera las partes que no se han podido revertir.
- `Revert("PropertyName")` revierte una propiedad a su valor guardado; por ejemplo, `Revert("Expression")` o `Revert("Annotations[MyAnnotation]")`. No hace nada cuando la propiedad no ha cambiado.

Los contenedores, como las tablas, las jerarquías y los roles, tienen una colección `DeletedObjects` que enumera los objetos eliminados de ellos en la sesión actual. Cada entrada tiene un `Name`, un `ObjectType` y un `Parent`, así como un método `Restore()`. `Restore()` en la colección restaura todas las entradas.

`Selected.Deleted` devuelve los objetos eliminados seleccionados en el Explorador TOM. Los objetos eliminados no aparecen en `Selected.Measures`, `Selected.Columns` ni en los demás métodos de acceso.

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
