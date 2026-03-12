---
uid: api-index
title: API de scripting
author: Daniel Otykier
updated: 2026-01-27
---

# API de Tabular Editor

Esta es la documentación de la API de Tabular Editor para las capacidades de scripting en C#.

En concreto, los objetos disponibles para scripting son los que se encuentran en las bibliotecas **TOMWrapper.dll**, **TabularEditor3.Shared.dll** y **SemanticBridge.dll**.

## Primeros pasos

Al escribir un script en Tabular Editor, los dos objetos que se usan con más frecuencia son [`Selected`](xref:TabularEditor.Shared.Interaction.Selection), que le permite acceder a los objetos seleccionados actualmente en el Explorador TOM, y [`Model`](xref:TabularEditor.TOMWrapper.Model), que le permite acceder a cualquier objeto dentro del modelo de datos cargado actualmente. Ambos objetos están disponibles como propiedades miembro en el objeto global [`ScriptHost`](xref:TabularEditor.Shared.Scripting.ScriptHost).

Además, el objeto `ScriptHost` contiene métodos estáticos que se exponen al script como métodos globales (es decir, métodos que puede llamar sin el prefijo `ScriptHost`). Estos métodos también se conocen como los @script-helper-methods.

## Ejemplo

```csharp
// Muestra un cuadro de diálogo para que el usuario seleccione una medida:
var myMeasure = SelectMeasure();

// Crea una nueva medida en la primera tabla del modelo, con el mismo nombre y expresión
// que la medida seleccionada previamente:
Model.Tables.First().AddMeasure(myMeasure.Name + " copy", myMeasure.Expression);
```

Para ver más ejemplos, consulte <xref:useful-script-snippets>.
