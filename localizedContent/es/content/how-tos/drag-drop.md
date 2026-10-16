---
uid: drag-drop
title: Arrastrar y soltar objetos
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Arrastrar y soltar objetos

Reorganiza un modelo en @tom-explorer-view, el mismo árbol que usas para explorarlo. Recoge los objetos donde los encuentres y suéltalos donde deban estar. No hay una superficie de modelado independiente a la que tengas que cambiar antes, y nada queda fuera de tu alcance solo porque la vista en la que estás no lo muestre.

La acción siempre es un movimiento. Tabular Editor muestra el cursor de movimiento cuando se permite soltar y el cursor de no permitido cuando no, y no hay ninguna tecla modificadora que convierta un arrastre en una copia. Para copiar un objeto, usa **Duplicar**; se describe en @duplicate-and-batch.

## Reorganizar carpetas de visualización

Arrastra una carpeta de visualización y todos los objetos que contiene se moverán con ella, incluidas las subcarpetas anidadas, que conservan su estructura. Para eso existe esta función: reestructurar la organización de carpetas de un modelo grande pasa a ser una sola acción por carpeta en lugar de una edición por medida.

<!-- IMAGE NEEDED: drag-drop-display-folders.gif
     An animation of a display folder being dragged onto another folder in the TOM Explorer,
     with the measures and subfolders beneath it following. Needs a model with at least two
     levels of nesting so the shape is visibly preserved.
     Alt text: "A display folder being dragged onto another folder in the TOM Explorer" -->

El resto de elementos del árbol se mueve del mismo modo:

- Selecciona varios objetos con **Ctrl+clic** o **Mayús+clic** y arrástralos juntos. Puedes mezclar medidas, columnas, jerarquías y carpetas siempre que estén en la misma tabla.
- Suelta los objetos directamente sobre el **nodo de la tabla** para sacarlos de su carpeta y devolverlos al nivel superior de la tabla.
- Suelta una carpeta dentro de otra para anidarla. Tabular Editor no permite soltar una carpeta dentro de una de sus propias subcarpetas, así que no puedes perder una rama dentro de sí misma.

Cada acción de soltar cuenta como un único paso de **Editar > Deshacer**, sin importar cuántos objetos afecte.

Las carpetas de visualización no son más que una propiedad de cadena de cada objeto, con `\\` separando los niveles; por ejemplo, `Sales\\Ratios` es la carpeta _Ratios_ dentro de _Sales_. Un objeto puede estar en más de una carpeta a la vez si separas las rutas con `;`.

## Mover un objeto a otra tabla

Las medidas y las columnas calculadas se pueden arrastrar a otra tabla, ya sea al nodo de la tabla o directamente a una de sus carpetas de visualización. Ningún otro tipo de objeto puede pasar de una tabla a otra de este modo.

Qué incluye el objeto:

- **Traducciones** de su nombre y descripción.
- **Pertenencia a perspectivas.** De forma predeterminada, el objeto conserva las perspectivas en las que estaba. Marca _Heredar la pertenencia de tabla al pegar o mover un objeto a una tabla_ en **Herramientas > Preferencias > Tabular Editor** para que adopte en su lugar la pertenencia de la tabla de destino.
- **El KPI**, en el caso de una medida que lo tenga.
- **Indicadores de error y advertencia.** Una expresión que no era válida antes del movimiento sigue marcada como no válida después, en lugar de parecer correcta hasta que la vuelvas a editar.

> [!WARNING]
> Mover una **columna calculada** a otra tabla elimina los elementos que dependían de ella en su posición anterior. Se elimina cualquier relación en la que participe, se elimina cualquier nivel de jerarquía construido sobre ella, se quita de calendarios y variaciones, y se borra cualquier _Ordenar por columna_ que apunte a ella. No se te pedirá que lo confirmes. **Editar > Deshacer** restaura todo en un solo paso, así que comprueba el modelo antes de hacer nada más.

El DAX que hace referencia a la columna por su tabla anterior, como `'Reseller Sales'[Margin]`, no se reescribe y sigue apuntando a la tabla de la que salió la columna. Las referencias a medidas se escriben como `[Measure]` sin tabla, por lo que no se ven afectadas. Ejecuta @using-bpa o revisa @messages-view tras un movimiento para detectar qué se rompió.

## Crear jerarquías y ordenar elementos de cálculo

- Arrastra una o varias **columnas sobre una jerarquía** para agregarlas como niveles. Suéltalas entre dos niveles existentes para elegir la posición. Se rechaza una columna que ya sea un nivel de esa jerarquía.
- Arrastra los **niveles** dentro de una jerarquía para reordenarlos, o sobre otra jerarquía de la misma tabla para moverlos allí.
- Arrastra los **elementos de cálculo** para reordenarlos dentro de su grupo de cálculo, o sobre otro grupo de cálculo para moverlos.

## Agrupar tablas

En Tabular Editor 3, puedes arrastrar una o varias tablas sobre un **grupo de tablas** para incluirlas en él. Si sueltas tablas sobre otra tabla, pasarán al grupo en el que esté esa tabla; así también es como se sacan tablas de un grupo: suéltalas sobre una tabla que no esté en ninguno.

Los grupos de tablas son una función práctica de Tabular Editor para organizar el árbol. Se almacenan como una anotación y no forman parte de los metadatos del modelo, por lo que no aparecen en Power BI ni en Analysis Services.

## Carpetas de visualización y traducciones

Al arrastrar, cambias la carpeta de visualización _de la traducción que estás viendo actualmente_ en el Explorador TOM, y solo esa.

- Si no hay ninguna traducción seleccionada, que es la opción predeterminada, al arrastrar se escribe la carpeta de visualización sin traducir. Los nombres traducidos de las carpetas de visualización se dejan exactamente como estaban, por lo que en esas configuraciones regionales los objetos permanecen en la carpeta anterior.
- Con una configuración regional seleccionada en la lista desplegable de traducción del Explorador TOM, al arrastrar se escribe la carpeta de visualización traducida de esa configuración regional y se deja intacta la carpeta sin traducir.

Así que reorganizar carpetas en la vista predeterminada no arrastra las traducciones. Vuelve a sincronizar las traducciones en el @metadata-translation-editor, o ejecuta la regla integrada de Best Practice Analyzer para los objetos que tienen una carpeta de visualización pero no una carpeta de visualización traducida, cuya corrección copia el valor sin traducir en cada configuración regional.

Mover un objeto a otra tabla es la excepción: sus propias traducciones se conservan al moverlo.

## Qué se puede arrastrar y adónde puede ir

| Arrastrar                                | En                                             | Resultado                                    |
| ---------------------------------------- | ---------------------------------------------- | -------------------------------------------- |
| Medidas, columnas, jerarquías y carpetas | Una carpeta de visualización en la misma tabla | Los objetos se mueven a esa carpeta          |
| Lo mismo                                 | El nodo de la tabla                            | Los objetos salen de su carpeta              |
| Medidas y columnas calculadas            | Otra tabla, o una carpeta dentro de ella       | Los objetos se mueven a esa tabla            |
| Columnas                                 | Una jerarquía o uno de sus niveles             | Las columnas se añaden como niveles          |
| Niveles                                  | La misma jerarquía, u otra de la misma tabla   | Los niveles se reordenan o se mueven         |
| Elementos de cálculo                     | Su grupo, u otro grupo de cálculo              | Los elementos se reordenan o se mueven       |
| Tablas                                   | Un grupo de tablas o otra tabla                | Las tablas pasan a formar parte de ese grupo |

Las particiones, los roles, las perspectivas, las relaciones, los Data source y las expresiones compartidas no se pueden arrastrar. Los objetos eliminados desde el último guardado, que aparecen tachados en el árbol, tampoco se pueden arrastrar ni usar como destino para soltar. Los objetos solo aparecen donde el árbol está configurado para mostrarlos, así que tienes que activar las carpetas de visualización y los grupos de tablas en la barra de herramientas antes de poder soltarlos ahí.

## Hacer lo mismo mediante un script

Las carpetas de visualización son una propiedad, por lo que un script establece la cadena directamente. Usa `\\` en una cadena normal de C#, o una cadena literal:

```csharp
Selected.Measures.SetDisplayFolder(@"Sales\Ratios");
Model.Tables["Sales"].Measures["Margin %"].DisplayFolder = @"Sales\Ratios";
Model.Tables["Sales"].Measures["Margin %"].TranslatedDisplayFolders["da-DK"] = @"Salg\Nøgletal";
```

Una medida se mueve entre tablas con `MoveTo`, que conserva sus indicadores de error exactamente igual que al arrastrarla:

```csharp
Model.Tables["Sales"].Measures["Margin %"].MoveTo(Model.Tables["Reseller Sales"]);
```

Las columnas calculadas no tienen `MoveTo`. Usa la misma acción que usa el árbol:

```csharp
var column = Model.Tables["Sales"].Columns["Margin"];
column.Handler.Actions.MoveObject(column, Model.Tables["Reseller Sales"], false, null);
```

Los grupos de tablas también son una propiedad: `Model.Tables["Sales"].TableGroup = "Facts";`. Consulta @csharp-scripts para ver cómo ejecutar todo esto.

## Arrastrar en otras partes de la aplicación

El Explorador TOM es el único lugar donde, al arrastrar, se cambia la estructura del modelo, pero también sirve como origen de varias otras acciones de arrastrar y soltar:

- Arrastra un objeto al editor de DAX o C# para insertar su nombre completo, en lugar de escribirlo. Consulta @dax-editor.
- Arrastra tablas desde el árbol hasta un diagrama de modelo abierto para agregarlas. Dentro del diagrama, arrastra una columna sobre una columna de otra tabla para crear una relación entre ambas. Consulta @diagram-view.
- Arrastra columnas, medidas o jerarquías a un Pivot Grid para agregarlas como campos.
