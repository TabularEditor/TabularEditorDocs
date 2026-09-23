## Agregar tablas

Agrega las tablas iniciales al diagrama de cualquiera de estas maneras:

- (Multi-)selecciona tablas en el Explorador TOM y, a continuación, haz clic con el botón derecho y elige **Agregar al diagrama**.
- Selecciona (Multi-)tablas en el Explorador TOM y, después, arrástralas al diagrama
- Usa la opción de menú **Diagrama > Agregar tablas...** y (multi-)selecciona las tablas que quieras agregar en el cuadro de diálogo.
  ![Diagrama: Agregar tablas](~/content/assets/images/diagram-add-tables.png)

Para agregar más tablas al diagrama, vuelve a usar la técnica anterior o haz clic con el botón derecho en una tabla existente del diagrama y elige una de estas opciones:

- **Agregar tablas que filtren esta tabla**: Agrega al diagrama todas las tablas que puedan filtrar, directa o indirectamente a través de otras tablas, la tabla seleccionada. Útil cuando empiezas desde una tabla de hechos.
- **Agregar todas las tablas relacionadas**: Agrega al diagrama todas las tablas que estén directamente relacionadas con la tabla seleccionada. Útil cuando empiezas desde una tabla de dimensión.
  ![Agregar tablas relacionadas](~/content/assets/images/add-related-tables.png)

Antes de continuar, reorganiza y cambia el tamaño de las tablas en el diagrama según tus preferencias, o usa la función **Diagrama > Organizar automáticamente** para que Tabular Editor 3 distribuya las tablas automáticamente.

## Modificar relaciones con el diagrama

Para agregar una nueva relación entre dos tablas, localiza la columna en la tabla de hechos (lado de muchos) de la relación y arrástrala a la columna correspondiente en la tabla de dimensión (lado de uno). Confirma la configuración de la relación y pulsa **OK**.

![Crear relación](~/content/assets/images/create-relationship.png)

Para editar una relación existente, haz clic con el botón derecho sobre ella y elige **Editar relación**. El menú contextual también incluye accesos directos para invertir o eliminar una relación, como se muestra en la captura de pantalla siguiente.

![Editar diagrama de relación](~/content/assets/images/edit-relationship-diagram.png)

> [!NOTE]
> También puedes crear relaciones sin usar un diagrama, desde el Explorador TOM. Localiza la columna desde la que debe comenzar la relación (lado de muchos / lado de la tabla de hechos), haz clic con el botón derecho y elige **Crear > Relación desde**. Especifica la columna de destino en el cuadro de diálogo Crear relación que aparece en pantalla.

## Selection and navigation

A diagram and the TOM Explorer keep the same object selected. Clicking a table, a column or a relationship in the diagram selects it in the tree, without pulling focus away from the diagram. Going the other way, selecting a table or a column in the tree highlights it in every open diagram, scrolling a column into view inside its table shape.

This works for navigation you did not perform by hand in the tree: **Go to** actions and search results highlight in your diagrams too.

A selection that does not resolve to a single table or column, whether several objects or none, clears the diagram's highlight rather than leaving a stale one behind.

> [!NOTE]
> Selecting an object in the TOM Explorer never switches the active document to a diagram. If a diagram is open in the background it updates quietly, and you keep working where you were.

Double-click a relationship to open **Edit relationship**.

## Guardar un diagrama

To save a diagram, use the **File > Save** (**Ctrl+S**) option. Tabular Editor 3 prompts you to save the diagram if you close the document or the application while the diagram has unsaved changes.

> [!TIP]
> El mismo archivo de diagrama puede cargarse para diferentes Data model. Los diagramas hacen referencia a las tablas por su nombre. Las tablas que no estén presentes en el modelo al cargar el diagrama simplemente se eliminan del diagrama.

> [!NOTE]
> Cada vez que agregue o modifique una relación, deberá ejecutar una actualización de tipo "calculate" en el Data model antes de que las relaciones puedan usarse al consultar el modelo.
