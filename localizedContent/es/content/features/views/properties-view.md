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

## Barra de herramientas

La barra de herramientas en la parte superior de la vista de propiedades contiene los botones siguientes:

- **Por categorías**: Agrupa las propiedades en categorías como _Básico_, _Metadatos_ y _Opciones_.
- **Alfabético**: Muestra todas las propiedades en una sola lista ordenada alfabéticamente.
- **Mostrar cambios**: Oculta todas las propiedades que no han cambiado desde la última vez que se guardó el modelo, de modo que solo queden las propiedades con [cambios no guardados](xref:unsaved-changes). Mientras el filtro está activo, el título de la vista es **Propiedades (cambiadas)**.
- **Descripciones de propiedades**: Muestra u oculta el panel de descripción en la parte inferior de la vista, que explica la propiedad seleccionada actualmente.
- **Cuadro de búsqueda**: Filtra la lista de propiedades por nombre.

## Cambios no guardados

Las propiedades que difieren de la última versión guardada del modelo se muestran con un fondo de fila naranja claro. Cuando se seleccionan varios objetos, se marca una fila si alguno de los objetos seleccionados ha cambiado esa propiedad.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/unsaved-changes/revert-property.png" alt="Properties view with unsaved changes" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> Una medida con cambios no guardados en las propiedades Descripción y Cadena de formato. La opción <strong>Revertir</strong> restaura una sola propiedad a su valor guardado.</figcaption>
</figure>

Haga clic con el botón derecho en una fila marcada y elija **Revertir** para restaurar esa propiedad al valor que tenía la última vez que se guardó, sin afectar a ningún otro cambio no guardado. La reversión cuenta como un único paso en la pila de deshacer, por lo que **Ctrl+Z** vuelve a aplicar el cambio. Consulte @unsaved-changes para obtener más detalles, incluido cómo revertir objetos completos desde el Explorador TOM y cómo desactivar los indicadores en **Herramientas > Preferencias**.

## Acoplamiento

De forma predeterminada, la vista de propiedades se encuentra en la esquina inferior derecha, pero también puedes abrirla pulsando F4 en tu teclado. También puedes acoplarla a cualquiera de los lados de la ventana principal o desacoplarla para que aparezca en una ventana independiente.
