---
uid: creating-macros
title: Creating macros
author: Morten Lønskov
updated: 2023-12-07
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# (Tutorial) Creating macros

Macros are C# scripts that have been saved in Tabular Editor to be easily reused across semantic models.
Saving a script as a  Macro will allow that macro to be used when right clicking on the objects in the TOM Explorer making it simple to apply the script to your model.

> [!NOTE] 
> In Tabular Editor 2, the feature to reuse C# Script is called @custom-actions.

## Creating a Macro

The first step in creating a Macro is to create and test a C# script. 

> [!TIP]
>One easy way to get started with C# scripting is to use the built in record function that lets you record the actions you take in the TOM Explorer.
>This way you can see how to interact with the different model objects and create reusable scripts.
>Another way is to reuse existing scripts such as those in our [script library](xref:csharp-script-library).
>In this tutorial we use the script [Format Numeric Measures](xref:script-format-numeric-measures) to showcase the Macro functionality.

Once the script works according requirements the script can be saved using the toolbar button "Save as Macro" which will open the "Save Macro" window.

![Macro Create infobox](~/content/assets/images/features/macros/macro_tutorial_create_infobox.png)

The "Save Macro" window allows three options:
1. Macro Name: Give the Macro a name and use backslash "\" to create folder path for the macro (See below)
2. Provide a tooltip for the Macro to remember what it does in detail
3. Select a context where the Macro should be available. 

![Macro Save infobox](~/content/assets/images/features/macros/macro_tutorial_save_window.png)

In the above example the Macro will be saved in a folder called Formatting\Beginner and the script is called "Format Numeric Measures". It will be saved in the context of measures.

### Macro Context
Macros are saved in a "valid context" that determines which objects in the model the script can be applied to. 

This Macro can then be used when Right Clicking on a measure in the TOM Explorer. The context given while saving the Macro determines which objects will show the Macro when right clicking on that object.

Tabular Editor will suggest a context based on the script that is being saved. 

![Macro Menu Shortcut](~/content/assets/images/features/macros/macro_tutorial_menu_shortcut.png)

## Edit a Macro

A macro can be opened by double clicking it in the Macro pane and after editing the C# script saved using _Ctrl + S_ or the Edit Macro button. 

![Macro Edit Infobox](~/content/assets/images/features/macros/macro_tutorial_edit_infobox.png)


## Macro JSON file

Macros are stored in the %LocalAppFolder%/TabularEditor3 as a JSON file called MacroActions.json. For more information on file types in Tabular Editor please see [Supported File Types](xref:supported-files#macroactionsjson)

## Macro file example

An example of a MacroActions.JSON file can be found here. It contains several of the C# scripts from our script library: [Download example MacroActions File](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


