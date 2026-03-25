---
uid: diagram-view
title: Vista de diagrama
author: Morten Lønskov
updated: 2025-04-24
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Vista de diagrama

La **Vista de diagrama** en Tabular Editor 3 es una representación visual del modelo semántico. Ofrece una disposición intuitiva para ver las tablas, sus columnas y las relaciones entre ellas. Es especialmente útil para entender el esquema de un vistazo, crear relaciones y presentar modelos a las partes interesadas. Un diagrama puede guardarse como un archivo independiente. Consulta <xref:supported-files#diagram-file-te3diag> para obtener más información.

> [!NOTE]
> Recomendamos crear varios diagramas más pequeños en lugar de unos pocos diagramas grandes. Cuando un diagrama contiene más de unas 20 tablas, se vuelve rápidamente abrumador y difícil de comprender.

Después de cargar un modelo en Tabular Editor 3, selecciona la opción de menú **Archivo > Nuevo > Diagrama** para crear un diagrama nuevo, o bien abre un diagrama nuevo desde la barra de herramientas principal y arrastra y suelta una tabla desde el Explorador TOM hasta la ventana del diagrama.

## Uso de la Vista de diagrama

## Agregar tablas

Agrega las tablas iniciales al diagrama de cualquiera de estas formas:

- (Multi-)seleccione tablas en el Explorador TOM, luego haga clic con el botón derecho y elija **Agregar al diagrama**.
- (Multi-)seleccione tablas en el Explorador TOM y, después, arrástrelas al diagrama
- Use la opción de menú **Diagrama > Agregar tablas...** y, en el cuadro de diálogo, (multi-)seleccione las tablas que desea agregar.
  ![Diagrama: Agregar tablas](~/content/assets/images/diagram-add-tables.png)

  Para agregar tablas adicionales al diagrama, utilice de nuevo la técnica anterior o haga clic con el botón derecho en una tabla existente del diagrama y elija una de las siguientes opciones:

  - **Agregar tablas que filtran esta tabla**: Agrega al diagrama todas las tablas que pueden filtrar, directa o indirectamente a través de otras tablas, la tabla seleccionada actualmente. Útil cuando empieza desde una tabla de hechos.
  - **Agregar todas las tablas relacionadas**: Agrega al diagrama todas las tablas que están directamente relacionadas con la tabla seleccionada actualmente. Útil cuando empieza desde una tabla de dimensión.
    ![Agregar tablas relacionadas](~/content/assets/images/add-related-tables.png)

  Antes de continuar, reorganice y cambie el tamaño de las tablas del diagrama según sus preferencias, o use la función **Diagrama > Organizar automáticamente** para que Tabular Editor 3 disponga las tablas automáticamente.

## Modificar relaciones utilizando el diagrama

Para agregar una nueva relación entre dos tablas, localice la columna en la tabla de hechos (lado de muchos) de la relación y arrástrela hasta la columna correspondiente de la tabla de dimensión (lado de uno). Confirma la configuración de la relación y haz clic en **Aceptar**.

![Crear relación](~/content/assets/images/create-relationship.png)

Para editar una relación existente, haga clic con el botón derecho sobre ella y seleccione **Editar relación**. El menú contextual también incluye accesos directos para invertir o eliminar una relación, como se muestra en la captura de pantalla siguiente.

![Editar diagrama de relaciones](~/content/assets/images/edit-relationship-diagram.png)

> [!NOTE]
> También puede crear relaciones sin usar un diagrama, mediante el Explorador TOM. Localiza la columna desde la que debe comenzar la relación (lado “muchos” / lado de la tabla de hechos), haz clic con el botón derecho y elige **Crear > Relación desde**. Especifique la columna de destino en el cuadro de diálogo Crear relación que aparece en la pantalla.

## Guardar un diagrama

Para guardar un diagrama, simplemente utilice la opción **Archivo > Guardar** (CTRL+S). Tabular Editor 3 le pedirá que guarde el diagrama si cierra el documento o la aplicación mientras el diagrama tenga cambios sin guardar.

> [!TIP]
> El mismo archivo de diagrama se puede cargar para diferentes modelos de datos. Los diagramas hacen referencia a las tablas por sus nombres. Las tablas que no estén presentes en el modelo al cargar el diagrama simplemente se eliminan del diagrama.

> [!NOTE]
> Cada vez que agregue o modifique una relación, deberá ejecutar una actualización de "cálculo" en el modelo de datos antes de que se puedan usar las relaciones al consultar el modelo.

## Características del diagrama

### Menú contextual para acciones en tablas

Al hacer clic con el botón derecho en cualquier parte de la Vista de diagrama, se abre un menú contextual que ofrece acceso rápido a varias opciones:

![Menú contextual del diagrama](~/content/assets/images/diagram-context-menu.png)

- **Agregar tablas...**: Abre un cuadro de diálogo para agregar manualmente tablas adicionales al diagrama.
- **Agregar tablas que filtran esta tabla**: Incorpora automáticamente las tablas relacionadas que filtran la tabla actual.
- **Agregar todas las tablas relacionadas**: Carga todas las tablas que comparten una relación con la tabla seleccionada.
- **Edit relationship**: Opens the relationship editor for the selected relationship. Only visible when a relationship is selected.
- **Invert relationship**: Swaps the from and to sides of the selected relationship. Only visible when a relationship is selected.
- **Activate relationship**: Activates an inactive relationship. Only visible when an inactive relationship is selected.
- **Deactivate relationship**: Deactivates an active relationship. Only visible when an active relationship is selected.
- **Ajustar a la página**: Ajusta el zoom del diagrama para que quepan todas las tablas visibles.
- **Auto-Arrange**: Automatically arrange tables into a star schema.
- **Quitar del diagrama**: Oculta la tabla seleccionada de la vista actual.
- **Delete relationship**: Deletes the selected relationship from the model. Only visible when a relationship is selected.

### Indicadores de relación

Las relaciones entre tablas se muestran mediante flechas direccionales:

- `1 - *`: Indica una relación de uno a muchos.
- `* - *`: Indica una relación de muchos a muchos.
- `➝`: Indica una relación unidireccional, donde la flecha define la dirección del filtro de la relación.
- `⟷`: Indica una relación de filtrado cruzado bidireccional.

Estos marcadores visuales permiten evaluar rápidamente la direccionalidad del filtro y la cardinalidad.

### Alternador de visualización de columnas

Hay un **conmutador de chevrón** en la esquina superior derecha de cada tabla. Al hacer clic en él, podrás alternar entre las siguientes opciones:

![Conmutador de chevrón del diagrama](~/content/assets/images/diagram-chevron-toggle.png)

- **Todas las columnas**: Muestra todas las columnas.
- **Solo columnas clave**: Muestra solo las claves primarias y foráneas.
- **Sin columnas**: Oculta todas las columnas y muestra solo el encabezado de la tabla.

El conmutador ayuda a reducir el desorden, especialmente en modelos complejos con muchas columnas, y facilita centrarse en las relaciones.

### Iconos de tipo de datos de columna

Cada columna del diagrama va acompañada de un icono que representa su tipo de datos:

- <img src="~/content/assets/images/icons/String.svg" alt="Text Icon" width="16" height="16"> para valores de cadena o texto
- <img src="~/content/assets/images/icons/Integer.svg" alt="Integer Icon" width="16" height="16"> para números enteros
- <img src="~/content/assets/images/icons/Double.svg" alt="Double Icon" width="16" height="16"> para números decimales de doble precisión / de coma flotante
- <img src="~/content/assets/images/icons/Currency.svg" alt="Currency Icon" width="16" height="16"> para valores de moneda / números decimales de punto fijo
- <img src="~/content/assets/images/icons/Binary.svg" alt="Binary Icon" width="16" height="16"> para valores binarios
- <img src="~/content/assets/images/icons/TrueFalse.svg" alt="Boolean Icon" width="16" height="16"> para valores booleanos (verdadero/falso)
- <img src="~/content/assets/images/icons/Calendar.svg" alt="Date Icon" width="16" height="16"> para valores de fecha y hora

Esta referencia visual rápida respalda la validación rápida de datos y ayuda a comprender las estructuras de datos.