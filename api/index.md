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

Take a look at the [`ScriptHost` methods](xref:TabularEditor.Shared.Scripting.ScriptHost#methods) for an overview of useful methods that are also available when writing scripts in Tabular Editor.

## Example

```csharp
// Displays a dialog to the user prompting them to select a measure:
var myMeasure = SelectMeasure();

// Creates a new measure on the first table of the model, with the same name and expression
// as the previously selected measure:
Model.Tables.First().AddMeasure(myMeasure.Name + " copy", myMeasure.Expression);
```

For more examples, see <xref:useful-script-snippets>.