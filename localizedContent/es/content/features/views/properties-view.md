---
uid: properties-view
title: Vista de propiedades
author: Daniel Otykier
updated: 2026-09-16
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Uso de la cuadrícula de propiedades en Tabular Editor

La vista de propiedades en Tabular Editor te permite inspeccionar y modificar las propiedades de cualquier objeto en tu modelo tabular.
Accedes a la vista de propiedades seleccionando un objeto en el Explorador TOM. A continuación, verás una lista de propiedades relevantes para el tipo de objeto seleccionado, como nombre, descripción, tipo de datos, cadena de formato, etc.
También puedes acceder a propiedades avanzadas que no están disponibles en otras herramientas como Visual Studio o Power BI Desktop.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/properties-view.png" alt="Properties View" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Ejemplo de propiedades de una tabla. Cada objeto tiene propiedades diferentes según su tipo </figcaption>
</figure>

La vista de propiedades te ayuda a:

- Ver y modificar las propiedades de cualquier objeto del modelo, como tablas, columnas, medidas, jerarquías, relaciones, particiones, roles y perspectivas.
- Filtrar y ordenar las propiedades por nombre o categoría mediante el cuadro de búsqueda y los botones en la parte superior de la vista.
- Copiar y pegar valores de propiedades entre distintos objetos con los atajos Ctrl+C y Ctrl+V.
- Deshacer y rehacer cambios de propiedades con los atajos Ctrl+Z y Ctrl+Y.
- Puedes usar atajos de teclado para navegar y editar rápidamente las propiedades. Por ejemplo, puedes presionar Ctrl+Arriba o Ctrl+Abajo para moverte entre propiedades; presionar Enter o F2 para editar el valor de una propiedad; presionar Esc para cancelar la edición; presionar Ctrl+S para guardar los cambios;

> [!TIP]
> Puedes seleccionar varios objetos para ver las propiedades que tienen en común y editarlas en bloque. Esto puede ser útil para establecer cadenas de formato, por ejemplo.

## Toolbar

The toolbar at the top of the Properties view contains the following buttons:

- **Categorized**: Groups the properties into categories such as _Basic_, _Metadata_ and _Options_.
- **Alphabetical**: Lists all properties in a single, alphabetically sorted list.
- **Show changes**: Hides all properties that have not changed since the model was last saved, so that only the properties with [unsaved changes](xref:unsaved-changes) remain. While the filter is active, the title of the view reads **Properties (Changed)**.
- **Property descriptions**: Shows or hides the description pane at the bottom of the view, which explains the currently selected property.
- **Search box**: Filters the list of properties by name.

## Unsaved changes

Properties that differ from the last saved version of the model are drawn with a light orange row background. When several objects are selected, a row is marked if any of the selected objects changed that property.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/unsaved-changes/revert-property.png" alt="Properties view with unsaved changes" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 2:</strong> A measure with unsaved changes to its Description and Format String. The <strong>Revert</strong> option puts a single property back to its saved value.</figcaption>
</figure>

Right-click a marked row and choose **Revert** to put that property back to the value it had at the last save, without touching any other unsaved changes. The revert is a single step on the undo stack, so **Ctrl+Z** brings the change back. See @unsaved-changes for details, including how to revert whole objects from the TOM Explorer, and how to turn the indicators off under **Tools > Preferences**.

## Docking

De forma predeterminada, la vista de propiedades se encuentra en la esquina inferior derecha, pero también puedes abrirla pulsando F4 en tu teclado. También puedes acoplarla a cualquiera de los lados de la ventana principal o desacoplarla para que aparezca en una ventana independiente.
