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

## Selección y navegación

Un diagrama y el Explorador TOM mantienen seleccionado el mismo objeto. Al hacer clic en una tabla, una columna o una relación en el diagrama, se selecciona en el árbol sin apartar el foco del diagrama. A la inversa, al seleccionar una tabla o una columna en el árbol, se resalta en todos los diagramas abiertos y, si es una columna, se desplaza hasta ponerla a la vista dentro del recuadro de su tabla.

Esto también funciona para la navegación que no realizas manualmente en el árbol: las acciones de **Ir a** y los resultados de búsqueda también se resaltan en los diagramas.

Una selección que no se resuelve en una única tabla o columna —ya sea porque incluye varios objetos o ninguno— quita el resaltado del diagrama, en lugar de dejar uno obsoleto.

> [!NOTE]
> Seleccionar un objeto en el Explorador TOM nunca convierte un diagrama en el documento activo. Si hay un diagrama abierto en segundo plano, se actualiza sin interrumpirte y sigues trabajando donde estabas.

Haz doble clic en una relación para abrir **Editar relación**.

## Guardar un diagrama

Para guardar un diagrama, usa la opción **Archivo > Guardar** (**Ctrl+S**). Tabular Editor 3 te pedirá que guardes el diagrama si cierras el documento o la aplicación mientras el diagrama tenga cambios sin guardar.

> [!TIP]
> El mismo archivo de diagrama puede cargarse para diferentes Data model. Los diagramas hacen referencia a las tablas por su nombre. Las tablas que no estén presentes en el modelo al cargar el diagrama simplemente se eliminan del diagrama.

> [!NOTE]
> Cada vez que agregue o modifique una relación, deberá ejecutar una actualización de tipo "calculate" en el Data model antes de que las relaciones puedan usarse al consultar el modelo.
