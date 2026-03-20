---
uid: importing-tables-data-modeling
title: Importación de tablas y modelado del Data model
author: Daniel Otykier
updated: 2021-10-08
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

# Importación de tablas y modelado del Data model

Este artículo describe cómo usar el [Asistente de importación de tablas](#table-import-wizard) de Tabular Editor 3 para agregar nuevas tablas al modelo. También hay una sección sobre cómo [actualizar el esquema de la tabla](#updating-table-schema) de una tabla existente. Por último, explicamos cómo usar la [herramienta de diagramas](#working-with-diagrams) para definir y editar relaciones entre tablas.

## Asistente de importación de tablas

[!include[importing-tables1](../features/import-tables.partial.md)]

# Trabajar con diagramas

En Tabular Editor 3, los **diagramas** son documentos que puedes usar para visualizar y editar las relaciones entre las tablas del modelo. Puedes crear tantos diagramas como quieras para visualizar áreas concretas de tu modelo. Un diagrama se puede guardar como un archivo independiente. Consulta <xref:supported-files#diagram-file-te3diag> para obtener más información.

> [!NOTE]
> Recomendamos crear varios diagramas pequeños en lugar de unos pocos diagramas grandes. Cuando un diagrama contiene más de unas 20 tablas, enseguida se vuelve abrumador y difícil de entender.

Después de cargar un modelo en Tabular Editor 3, elige la opción de menú **Archivo > Nuevo > Diagrama** para crear un diagrama nuevo.

## Agregar tablas

Agrega las tablas iniciales al diagrama de cualquiera de estas maneras:

- (Multi-)selecciona tablas en el Explorador TOM y, a continuación, haz clic con el botón derecho y elige **Agregar al diagrama**.
- Selecciona (Multi-)tablas en el Explorador TOM y, después, arrástralas al diagrama
- Usa la opción de menú **Diagrama > Agregar tablas...** y (multi-)selecciona las tablas que quieras agregar en el cuadro de diálogo.
  ![Diagram Add Tables](~/content/assets/images/diagram-add-tables.png)

Para agregar más tablas al diagrama, vuelve a usar la técnica anterior o haz clic con el botón derecho en una tabla existente del diagrama y elige una de estas opciones:

- **Agregar tablas que filtren esta tabla**: Agrega al diagrama todas las tablas que puedan filtrar, directa o indirectamente a través de otras tablas, la tabla seleccionada. Útil cuando empiezas desde una tabla de hechos.
- **Agregar todas las tablas relacionadas**: Agrega al diagrama todas las tablas que estén directamente relacionadas con la tabla seleccionada. Útil cuando empiezas desde una tabla de dimensión.
  ![Add Related Tables](~/content/assets/images/add-related-tables.png)

Antes de continuar, reorganiza y cambia el tamaño de las tablas en el diagrama según tus preferencias, o usa la función **Diagrama > Organizar automáticamente** para que Tabular Editor 3 distribuya las tablas automáticamente.

## Modificar relaciones con el diagrama

Para agregar una nueva relación entre dos tablas, localiza la columna en la tabla de hechos (lado de muchos) de la relación y arrástrala a la columna correspondiente en la tabla de dimensión (lado de uno). Confirma la configuración de la relación y pulsa **OK**.

![Crear relación](~/content/assets/images/create-relationship.png)

Para editar una relación existente, haz clic con el botón derecho sobre ella y elige **Editar relación**. El menú contextual también incluye accesos directos para invertir o eliminar una relación, como se muestra en la captura de pantalla siguiente.

![Editar diagrama de relación](~/content/assets/images/edit-relationship-diagram.png)

> [!NOTE]
> También puedes crear relaciones sin usar un diagrama, desde el Explorador TOM. Localiza la columna desde la que debe comenzar la relación (lado de muchos / lado de la tabla de hechos), haz clic con el botón derecho y elige **Crear > Relación desde**. Especifica la columna de destino en el cuadro de diálogo Crear relación que aparece en pantalla.

## Guardar un diagrama

Para guardar un diagrama, simplemente usa la opción **Archivo > Guardar** (CTRL+S). Tabular Editor 3 te pedirá que guardes el diagrama si cierras el documento o la aplicación cuando el diagrama tenga cambios sin guardar.

> [!TIP]
> El mismo archivo de diagrama puede cargarse para diferentes Data model. Los diagramas hacen referencia a las tablas por su nombre. Las tablas que no estén presentes en el modelo al cargar el diagrama simplemente se eliminan del diagrama.

> [!NOTE]
> Cada vez que agregue o modifique una relación, deberá ejecutar una actualización de tipo "calculate" en el Data model antes de que las relaciones puedan usarse al consultar el modelo.

# Siguientes pasos

- @refresh-preview-query
- @creating-and-testing-dax