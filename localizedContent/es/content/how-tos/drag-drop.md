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

Reorganizas un modelo en @tom-explorer-view, el mismo árbol que usas para navegar por él. Recoge los objetos donde los encuentres y suéltalos donde deben ir. No existe una superficie de modelado aparte a la que tengas que cambiar primero, y nada queda fuera de tu alcance solo porque la vista en la que estás no lo represente.

El gesto siempre es de mover. Tabular Editor muestra el cursor de mover cuando se permite soltar y el cursor de prohibido cuando no; no hay ninguna tecla modificadora que convierta el arrastre en una copia. Para copiar un objeto, usa **Duplicar**, como se describe en @duplicate-and-batch.

## Reorganizar carpetas de visualización

Arrastra una carpeta de visualización y se moverán con ella todos los objetos que contiene, incluidas las subcarpetas anidadas, que conservan su estructura. Esta es la razón de ser de la función: reestructurar la organización de carpetas de un modelo grande requiere un solo gesto por carpeta en lugar de una edición por medida.

<!-- IMAGE NEEDED: drag-drop-display-folders.gif
     An animation of a display folder being dragged onto another folder in the TOM Explorer,
     with the measures and subfolders beneath it following. Needs a model with at least two
     levels of nesting so the shape is visibly preserved.
     Alt text: "A display folder being dragged onto another folder in the TOM Explorer" -->

Todo lo demás en el árbol se mueve de la misma manera:

- Selecciona varios objetos con **Ctrl+clic** o **Mayús+clic** y arrástralos a la vez. Puedes mezclar medidas, columnas, jerarquías y carpetas siempre que estén en la misma tabla.
- Suelta los objetos sobre el propio **nodo de tabla** para sacarlos de su carpeta y devolverlos al nivel superior de la tabla.
- Suelta una carpeta dentro de otra carpeta para anidarla. Tabular Editor no permite soltar una carpeta dentro de una de sus propias subcarpetas, así que una rama no puede acabar dentro de sí misma.

Cada operación de soltar equivale a un solo paso de **Editar > Deshacer**, sin importar cuántos objetos afecte.

Las carpetas de visualización no son más que una propiedad de cadena en cada objeto, con `\` separando los niveles, de modo que `Sales\Ratios` es la carpeta _Ratios_ dentro de _Sales_. Un objeto puede estar en más de una carpeta a la vez separando las rutas con `;`.

## Mover un objeto a otra tabla

Las medidas y las columnas calculadas se pueden arrastrar a otra tabla, ya sea al nodo de tabla o directamente a una de sus carpetas de visualización. Ningún otro tipo de objeto puede pasar de una tabla a otra de esta forma.

Qué acompaña al objeto:

- **Traducciones** de su nombre y su descripción.
- **Pertenencia a perspectivas.** De forma predeterminada, el objeto conserva las perspectivas de las que formaba parte. Marca _Heredar pertenencia a la tabla al pegar o mover un objeto a una tabla_ en **Herramientas > Preferencias > Tabular Editor** para que, en su lugar, adopte la pertenencia de la tabla de destino.
- **El KPI**, para una medida que lo tenga.
- **Indicadores de error y advertencia.** Una expresión que era inválida antes del movimiento sigue marcada como inválida después, en lugar de aparentar estar bien hasta que la vuelvas a editar.

> [!WARNING]
> Mover una **columna calculada** a otra tabla elimina los elementos que dependían de ella en su posición original. Se elimina cualquier relación en la que participe; se elimina cualquier nivel de jerarquía basado en ella; se quita de calendarios y variaciones; y se borra cualquier _Ordenar por columna_ que apunte a ella. No se te pedirá que lo confirmes. **Editar > Deshacer** lo restaura todo en un solo paso, así que revisa el modelo antes de hacer cualquier otra cosa.

El DAX que hace referencia a la columna mediante su tabla anterior, como `'Reseller Sales'[Margin]`, no se reescribe y sigue apuntando a la tabla de la que salió la columna. Las referencias a medidas se escriben como `[Measure]` sin tabla, así que no se ven afectadas. Ejecuta @using-bpa o revisa @messages-view después de un movimiento para detectar qué se ha roto.

## Crear jerarquías y ordenar elementos de cálculo

- Arrastra una o varias **columnas a una jerarquía** para agregarlas como niveles. Suéltalas entre dos niveles existentes para elegir la posición. Se rechaza una columna que ya sea un nivel de esa jerarquía.
- Arrastra los **niveles** dentro de una jerarquía para reordenarlos, o a otra jerarquía de la misma tabla para moverlos allí.
- Arrastra los **elementos de cálculo** para reordenarlos dentro de su grupo de cálculo, o a otro grupo de cálculo para moverlos.

## Agrupar tablas

En Tabular Editor 3 puedes arrastrar una o varias tablas a un **grupo de tablas** para incluirlas en él. Al soltar tablas sobre otra tabla, pasan al grupo en el que esté esa tabla. Así también se sacan tablas de un grupo: suéltalas sobre una tabla que no pertenezca a ningún grupo.

Los grupos de tablas son una función de Tabular Editor para organizar el árbol. Se almacenan como una anotación y no forman parte de los metadatos del modelo, por lo que no aparecen en Power BI ni en Analysis Services.

## Carpetas de visualización y traducciones

Al arrastrar, se cambia la carpeta de visualización _de la traducción que estás viendo en ese momento_ en el Explorador TOM, y únicamente esa.

- Si no hay ninguna traducción seleccionada, que es lo predeterminado, al arrastrar se asigna la carpeta de visualización sin traducir. Los nombres traducidos de las carpetas de visualización se mantienen exactamente como estaban, así que en esas configuraciones regionales los objetos se quedan en la carpeta anterior.
- Con una configuración regional seleccionada en el menú desplegable de traducción del Explorador TOM, el arrastre escribe la carpeta de visualización traducida de esa configuración regional y deja intacta la no traducida.

Por tanto, reorganizar carpetas en la vista predeterminada no se lleva consigo las traducciones. Vuelve a alinearlas en el editor de traducción @metadata-translation-editor o ejecuta la regla integrada de Best Practice Analyzer para los objetos que tienen una carpeta de visualización pero no una carpeta de visualización traducida; su corrección consiste en copiar el valor no traducido en todas las configuraciones regionales.

Trasladar un objeto a otra tabla es la excepción: sus propias traducciones se conservan al moverlo.

## Qué se puede arrastrar y adónde puede ir

| Arrastrar                                | A                                              | Resultado                                    |
| ---------------------------------------- | ---------------------------------------------- | -------------------------------------------- |
| Medidas, columnas, jerarquías y carpetas | Una carpeta de visualización en la misma tabla | Los objetos se mueven a esa carpeta          |
| Los mismos                               | El nodo de la tabla                            | Los objetos salen de su carpeta              |
| Medidas y columnas calculadas            | Otra tabla, o una carpeta dentro de ella       | Los objetos se mueven a esa tabla            |
| Columnas                                 | Una jerarquía o uno de sus niveles             | Las columnas se añaden como niveles          |
| Niveles                                  | La misma jerarquía u otra en la tabla          | Los niveles se reordenan o se mueven         |
| Elementos de cálculo                     | Su grupo u otro grupo de cálculo               | Los elementos se reordenan o se mueven       |
| Tablas                                   | Un grupo de tablas u otra tabla                | Las tablas pasan a formar parte de ese grupo |

Particiones, roles, perspectivas, relaciones, Data sources y expresiones compartidas no se pueden arrastrar. Los objetos eliminados desde el último guardado aparecen tachados en el árbol; tampoco se pueden arrastrar ni usar como destino al soltar. Los objetos solo aparecen donde el árbol está configurado para mostrarlos; por eso, las carpetas de visualización y los grupos de tablas deben activarse en la barra de herramientas antes de poder soltar elementos sobre ellos.

## Hacer lo mismo desde un script

Las carpetas de visualización son una propiedad, así que un script establece la cadena directamente. Usa `\\` en una cadena normal de C# o una cadena literal verbatim:

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

El Explorador TOM es el único lugar donde arrastrar cambia la estructura del modelo, pero desde ahí también puedes soltar elementos en varios lugares más:

- Arrastra un objeto al editor de DAX o C# para insertar su nombre completo, en lugar de escribirlo. Consulta @dax-editor.
- Arrastra tablas desde el árbol a un diagrama de modelo abierto para agregarlas. Dentro del diagrama, arrastra una columna sobre una columna de otra tabla para crear una relación entre ellas. Consulta @diagram-view.
- Arrastra columnas, medidas o jerarquías a una Pivot Grid para agregarlas como campos.
