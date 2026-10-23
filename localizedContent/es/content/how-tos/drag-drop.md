---
uid: drag-drop
title: Arrastrar y soltar objetos
author: Morten Lønskov
updated: 2026-10-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Arrastrar y soltar objetos

Arrastrar y soltar en la @tom-explorer-view desplaza objetos entre carpetas de visualización, tablas, jerarquías, grupos de cálculos y grupos de tablas. Al arrastrar, siempre se mueve un objeto, y ninguna tecla modificadora lo convierte en una copia. Mientras arrastra, el cursor de movimiento indica dónde se puede soltar y el cursor de prohibición de soltar indica dónde no se puede. **Duplicar**, descrito en @duplicate-and-batch, copia un objeto.

## Mover carpetas de visualización

Arrastre una carpeta de visualización a otra carpeta para moverla. Todos los objetos y subcarpetas que contiene se desplazan con ella, y se mantiene la estructura de subcarpetas.

<!-- SE NECESITA IMAGEN: drag-drop-display-folders.gif
     Una animación de una carpeta de visualización que se arrastra a otra carpeta en el Explorador TOM,
     con las medidas y las subcarpetas que hay debajo siguiendo el movimiento. Se necesita un modelo con al menos dos
     niveles de anidamiento para que la forma se conserve visiblemente.
     Texto alternativo: «Una carpeta de visualización que se está arrastrando a otra carpeta en el Explorador TOM» -->

También puedes:

- Seleccionar varios objetos con **Ctrl+clic** o **Mayús+clic** y arrastrarlos juntos. Puede combinar medidas, columnas, jerarquías y carpetas si están en la misma tabla.
- Soltar objetos en el nodo de la tabla para sacarlos de su carpeta y llevarlos al nivel superior de la tabla.
- Soltar una carpeta sobre otra carpeta para anidarla. No puedes soltar una carpeta en una de sus propias subcarpetas.

Cada vez que se suelta un elemento se cuenta como un paso de deshacer (**Ctrl+Z**), independientemente de cuántos objetos se muevan.

Una carpeta de visualización es una propiedad de cadena de cada objeto, con `\` separando los niveles: `Sales\Ratios` es la carpeta Índices dentro de Ventas. Para mostrar un objeto en más de una carpeta, separe las rutas con `;`.

## Mover un objeto a otra tabla

Arrastre medidas y columnas calculadas a otra tabla o, en Tabular Editor 3, a una carpeta de visualización de esa tabla para moverlas allí, lo que no es posible con otros tipos de objetos.

En Tabular Editor 3, el traslado conserva lo siguiente del objeto:

- traducciones de su nombre y descripción
- la pertenencia a la perspectiva, a menos que seleccione **Heredar la pertenencia de la tabla cuando se pega/mueve un objeto a una tabla** en **Herramientas > Preferencias > Tabular Editor > Operaciones de modelado**, lo que otorga al objeto la pertenencia a la perspectiva de la tabla de destino
- KPI, para una medida que tenga uno
- los indicadores de error y advertencia, de modo que una expresión no válida siga marcada como no válida después del traslado

> [!WARNING]
> Cuando mueve una columna calculada a otra tabla, no aparece ninguna confirmación y se modifican los siguientes elementos:
>
> - Se eliminan las relaciones que usan la columna.
> - Se eliminan los niveles de jerarquía basados en la columna.
> - Se quita la columna de los calendarios y las variaciones.
> - Se borran las referencias `SortByColumn` a la columna.
>
> Pulse **Ctrl+Z** para deshacer el traslado y todos estos cambios en un solo paso.

El DAX que hace referencia a la columna por su tabla anterior, como `'Reseller Sales'[Margin]`, no se reescribe y sigue apuntando a la tabla que ha dejado la columna. Las referencias de medida se escriben como `[Measure]` sin una tabla, por lo que no se ven afectadas. Ejecute @using-bpa o consulte la @messages-view después de un traslado para detectar lo que se ha roto. En la vista de mensajes, desmarque **Mostrar errores en cascada** para mostrar solo las expresiones que necesita corregir.

## Crear jerarquías y ordenar elementos de cálculo

- Arrastre una o más columnas a una jerarquía para añadirlas como niveles. Suéltelas entre dos niveles existentes para elegir la posición. No puedes añadir una columna que ya sea un nivel de esa jerarquía.
- Arrastre niveles dentro de una jerarquía para reordenarlos, o a otra jerarquía de la misma tabla para moverlos allí.
- Arrastre elementos de cálculo para reordenarlos en su grupo de cálculos o a otro grupo de cálculos para moverlos.

## Agrupar tablas

> [!NOTE]
> Los grupos de tablas solo están disponibles en Tabular Editor 3.

Arrastre una o más tablas a un grupo de tablas para moverlas a él, o a otra tabla para moverlas al grupo de esa tabla. Si se colocan tablas en una tabla que no está en un grupo, se eliminarán de su grupo. Los grupos de tablas organizan el Explorador TOM y se almacenan como una anotación, que Power BI y Analysis Services ignoran.

## Carpetas de visualización y traducciones

Al arrastrar, la carpeta de visualización solo se cambia para la traducción seleccionada en el Explorador TOM:

- Si no se ha seleccionado ninguna traducción (opción predeterminada), al arrastrar se cambia la carpeta de visualización no traducida. Las carpetas de visualización traducidas no se modifican, por lo que las vistas traducidas siguen mostrando los objetos de la carpeta anterior.
- Con una cultura seleccionada en el menú desplegable de traducción del Explorador TOM, al arrastrar se cambia la carpeta de visualización traducida de esa cultura y se deja sin cambios la carpeta de visualización no traducida.

Actualice las traducciones en el @metadata-translation-editor o con la corrección de la regla del Best Practice Analyzer [Traducir carpetas de visualización para todas las culturas](xref:kb.bpa-translate-display-folders), que copia el valor no traducido en todas las culturas.

## Qué se puede arrastrar y dónde se puede colocar

| Arrastrar | Hacia | Resultado |
|---|---|---|
| Medidas, columnas, jerarquías, carpetas | Una carpeta de visualización de la misma tabla | Los objetos se desplazan a esa carpeta |
| Medidas, columnas, jerarquías, carpetas | El nodo de la tabla | Los objetos salen de su carpeta |
| Medidas, columnas calculadas | Otra tabla o una carpeta de esa tabla (carpeta: solo en Tabular Editor 3) | Los objetos se desplazan a esa tabla |
| Columnas | Una jerarquía o uno de sus niveles | Las columnas se añaden como niveles |
| Niveles | La misma jerarquía u otra de la tabla | Los niveles se reordenan o se desplazan |
| Elementos de cálculo | Su grupo u otro grupo de cálculo | Los elementos se reordenan o se mueven |
| Tablas (solo Tabular Editor 3) | Un grupo de tablas u otra tabla | Las tablas se desplazan a ese grupo |

Se aplican las siguientes limitaciones:

- Las particiones, los roles, las perspectivas, las relaciones, las fuentes de datos y las expresiones compartidas no se pueden arrastrar.
- En Tabular Editor 3.27.0 y versiones posteriores, los objetos eliminados desde el último guardado se muestran tachados en el árbol y no se pueden arrastrar ni soltar sobre ellos.
- Las carpetas de visualización y los grupos de tablas solo aceptan soltar elementos mientras están activados en la barra de herramientas del Explorador TOM.

## Realizar los mismos cambios desde un script

Un script mueve objetos entre carpetas de visualización estableciendo la cadena `DisplayFolder`. Utilice `\\` en una cadena de C# normal o en una cadena literal:

```csharp
Selected.Measures.SetDisplayFolder(@"Sales\Ratios");
Model.Tables["Sales"].Measures["Margin %"].DisplayFolder = @"Sales\Ratios";
Model.Tables["Sales"].Measures["Margin %"].TranslatedDisplayFolders["da-DK"] = @"Salg\Nøgletal";
```

`MoveTo` mueve una medida a otra tabla y conserva sus indicadores de error:

```csharp
Model.Tables["Sales"].Measures["Margin %"].MoveTo(Model.Tables["Reseller Sales"]);
```

La API de scripting no tiene ningún método para mover una columna calculada a otra tabla. En Tabular Editor 3, al establecer `TableGroup` se mueve una tabla a un grupo de tablas: `Model.Tables["Sales"].TableGroup = "Facts";`, en un script que ejecute como se describe en @csharp-scripts.

## Arrastrar a otras vistas

También puede arrastrar objetos desde el Explorador TOM a:

- el editor DAX o C#, para insertar el nombre totalmente calificado del objeto. Consulte @dax-editor.
- un diagrama de modelo abierto, para agregarle tablas. En el diagrama, arrastre una columna a una columna de otra tabla para crear una relación. Consulte @diagram-view.
- una [cuadrícula dinámica](xref:pivot-grid), para agregar columnas, medidas o jerarquías como campos.

El diagrama del modelo y la tabla dinámica solo están disponibles en Tabular Editor 3.
