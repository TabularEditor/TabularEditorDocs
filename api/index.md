---
uid: api-index
title: Scripting API
author: Daniel Otykier
updated: 2022-06-16
---

# Tabular Editor API

This is the API documentation for Tabular Editor's C# scripting capabilities.

Specifically, the objects available for scripting are those found in the **TOMWrapper.dll** and **TabularEditor3.Shared.dll** libraries.

## Getting started

When writing a script in Tabular Editor, the two most common objects used are [`Selected`](xref:TabularEditor.Shared.Interaction.Selection), which lets you access objects currently selected in the TOM Explorer, and [`Model`](xref:TabularEditor.TOMWrapper.Model), which lets you access any object within the currently loaded data model. Both these objects are available as member properties on the global [`ScriptHost`](xref:TabularEditor.Shared.Scripting.ScriptHost) object.

In addition, the `ScriptHost` object holds static methods which are exposed to the script as global methods (i.e. methods you can call without the `ScriptHost` prefix). These methods are also known as @script-helper-methods.

## Example

```csharp
// Displays a dialog to the user prompting them to select a measure:
var myMeasure = SelectMeasure();

// Creates a new measure on the first table of the model, with the same name and expression
// as the previously selected measure:
Model.Tables.First().AddMeasure(myMeasure.Name + " copy", myMeasure.Expression);
```

For more examples, see <xref:useful-script-snippets>.