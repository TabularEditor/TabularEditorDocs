---
uid: macros-view
title: Macros view
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Macros view

![Macros View](~/images/macros-view.png)

The macros view displays a list of all macros currently saved in your `%localappdata%\TabularEditor3\MacroActions.json` file.

- You can delete a macro by clicking on the "X" button at the top left corner of the view.
- You can edit a macro by double-clicking on the list item. This will bring up a [C# script document](xref:csharp-scripts) containing the code that will be executed when the macro is invoked. To save your changes to the macro, click the "Edit Macro..." toolbar button (see screenshot below) or use the **C# Script > Edit Macro...** menu option.
- To create a new macro, start by creating a new [C# script](xref:csharp-scripts), then save it as a macro using the **C# Script > Save as Macro...** menu option.

![Edit Macro](~/images/edit-macro.png)

## Next steps

- @creating-macros
