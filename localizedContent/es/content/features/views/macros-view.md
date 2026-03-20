---
uid: macros-view
title: Vista de macros
author: Morten Lønskov
updated: 2023-03-22
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Negocios
          full: true
        - edition: Empresarial
          full: true
---

# Vista de macros

Las macros son una función potente de Tabular Editor que te permiten automatizar tareas repetitivas o crear acciones personalizadas para tus modelos. Una macro es un script escrito en C# que puede acceder al Tabular Object Model (TOM) y manipularlo.

Puedes crear, editar, ejecutar y administrar macros desde el menú Macros de Tabular Editor.

> [!TIP]
> Puedes anidar tus macros en carpetas anteponiendo al nombre de tu macro el siguiente patrón `FolderName\\MacroName`

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/macros-view.png" alt="Macro Window" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Ventana de macros en Tabular Editor. Ofrece una visión general de todas tus macros guardadas. </figcaption>
</figure>

> [!NOTE]
> La Vista de macros muestra una lista de todas las macros guardadas actualmente en tu archivo `%localappdata%\TabularEditor3\MacroActions.json`.

- Puedes eliminar una macro haciendo clic en el botón "X" en la esquina superior izquierda de la vista.
- Puedes editar una macro haciendo doble clic en el elemento de la lista. Esto abrirá un [documento de C# Script](xref:csharp-scripts) que contiene el código que se ejecutará cuando se invoque la macro. Para guardar los cambios en la macro, haz clic en el botón de la barra de herramientas "Editar macro..." (consulta la captura de pantalla siguiente) o usa el elemento de menú **C# Script > Editar macro...**.
- Para crear una macro nueva, empieza creando un [C# Script](xref:csharp-scripts) y luego guárdalo como macro usando el elemento de menú **C# Script > Guardar como macro...**.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/edit-macro.png" alt="Edit Macro Button" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> Cuando tengas una macro abierta, puedes volver a guardarla eligiendo "Editar macro..." </figcaption>
</figure>

## Pasos siguientes

- @creating-macros
