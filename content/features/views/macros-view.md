---
uid: macros-view
title: Macros view
author: Morten Lønskov
updated: 2023-03-22
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
# Macros view
Macros are a powerful feature of Tabular Editor that allow you to automate repetitive tasks or create custom actions for your models. A macro is a script written in C# that can access and manipulate the Tabular Object Model (TOM). 

You can create, edit, run and manage macros from the Macros menu in Tabular Editor.

> [!TIP]
> You can nest your macros in folders by prefixing your macro name in the following pattern `FolderName\MacroName`

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/macros-view.png" alt="Macro Window" style="width: 500px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Macro window in Tabular Editor. Provides an overview of all your saved Macros </figcaption>
</figure>

> [!NOTE]
> The macros view displays a list of all macros currently saved in your `%localappdata%\TabularEditor3\MacroActions.json` file.

- You can delete a macro by clicking on the "X" button at the top left corner of the view.
- You can edit a macro by double-clicking on the list item. This will bring up a [C# script document](xref:csharp-scripts) containing the code that will be executed when the macro is invoked. To save your changes to the macro, click the "Edit Macro..." toolbar button (see screenshot below) or use the **C# Script > Edit Macro...** menu item.
- To create a new macro, start by creating a new [C# script](xref:csharp-scripts), then save it as a macro using the **C# Script > Save as Macro...** menu item.


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/edit-macro.png" alt="Edit Macro Button" style="width: 500px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 2:</strong> When you have a Macro open you can save it back by choosing "Edit Macro..." </figcaption>
</figure>


## Next steps

- @creating-macros
