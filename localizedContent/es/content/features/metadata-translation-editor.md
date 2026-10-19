---
uid: metadata-translation-editor
title: Metadata Translation Editor
author: Morten Lønskov
updated: 2026-10-11
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
# Metadata Translation Editor

El **Metadata Translation Editor** proporciona una visión general de los nombres, las descripciones y las carpetas de visualización traducidos de los objetos traducibles del modelo. Puede iniciar el Metadata Translation Editor a través del menú **Ver**. Como alternativa, si solo necesita editar ciertas traducciones, selecciónelas en el **Explorador TOM** (mantenga pulsada la tecla CTRL o MAYÚS para seleccionar varias), luego haga clic con el botón derecho y elija **Mostrar en editor de traducción de metadatos**.

![Metadata Translation Editor](~/content/assets/images/metadata-translation-editor.png)

Utiliza los campos de entrada del editor de traducción de metadatos para añadir/eliminar o editar rápidamente las traducciones de los nombres de los objetos, las descripciones y los nombres de las carpetas de visualización para el idioma correspondiente. Las tres primeras columnas del editor le permiten cambiar los nombres predeterminados, las descripciones y los nombres de las carpetas de visualización de los objetos. Puede usar Deshacer (Ctrl+Z) y Rehacer (Ctrl+Y) de la forma habitual.

Para eliminar una traducción, borre su celda y pulse **Intro**. Al borrar la celda predeterminada **Descripción** o **Carpeta para mostrar**, se vacía esa propiedad. No se puede borrar el **Nombre** predeterminado. Las celdas **Carpeta para mostrar** del modelo, las tablas, los niveles de jerarquía y las perspectivas son de solo lectura.

## Barra de herramientas del Metadata Translation Editor

Mientras el Metadata Translation Editor está activo, la barra de herramientas que lo acompaña ofrece las siguientes opciones:

- ![Metadata Translation Editor Nueva traducción](~/content/assets/images/metadata-translation-editor-add-translation.png) **Nueva traducción**: Este botón añade una nueva traducción al modelo. La traducción aparece en el Metadata Translation Editor. 
- ![Editor de traducción de metadatos Ocultar miembros](~/content/assets/images/perspective-editor-hide-members.png) **Mostrar/ocultar objetos ocultos**: Habilite esta opción si desea ver todos los objetos en el Editor de traducción de metadatos, incluidos los objetos ocultos.
- ![Metadata Translation Editor Ocultar nombres](~/content/assets/images/metadata-translation-editor-name.png) **Mostrar/Ocultar nombres**: Desactive esta opción si no desea ver las columnas de traducción de nombres en Metadata Translation Editor.
- ![Metadata Translation Editor Ocultar descripciones](~/content/assets/images/metadata-translation-editor-description.png) **Mostrar/ocultar descripciones**: Desactive esta opción si no desea ver las columnas de traducción de descripciones en Metadata Translation Editor.
- ![Editor de traducción de metadatos Mostrar/ocultar carpetas de visualización](~/content/assets/images/perspective-editor-folder.png) **Mostrar/ocultar carpetas de visualización**: Desactive esta opción si no desea ver las columnas de traducción de carpetas de visualización en el Editor de traducción de metadatos.

## Trabajar con muchas traducciones

Si está trabajando en un modelo con muchas traducciones, puede resultar poco práctico mostrar todas a la vez. Puede reorganizar el orden de visualización de las traducciones en el Metadata Translation Editor arrastrando los encabezados de las columnas, lo que facilita la comparación de las traducciones una al lado de la otra. Además, puedes añadir/eliminar traducciones del editor en cualquier momento a través del menú contextual que aparece al hacer clic con el botón derecho:

<!-- VOLVER A HACER CAPTURA DE PANTALLA (3.27.1): metadata-translation-editor-columns-bands.png. El menú contextual de la cabecera ya no tiene la opción Mostrar fila de filtro automático. -->
![Columnas del Metadata Translation Editor](~/content/assets/images/metadata-translation-editor-columns-bands.png)