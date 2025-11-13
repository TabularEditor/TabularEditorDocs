---
uid: api-index
title: Scripting-API
author: Daniel Otykier
updated: 2022-06-16
---

# Tabular Editor API

Dies ist die API-Dokumentation für die C#-Scripting-Funktionen von Tabular Editor.

Insbesondere sind die für Scripts verfügbaren Objekte diejenigen, die in den Bibliotheken **TOMWrapper.dll** und **TabularEditor3.Shared.dll** enthalten sind.

## Erste Schritte

Beim Schreiben eines Scripts in Tabular Editor gehören die beiden am häufigsten verwendeten Objekte zu [`Selected`](xref:TabularEditor.Shared.Interaction.Selection), mit dem Sie auf Objekte zugreifen können, die derzeit im TOM Explorer ausgewählt sind, und [`Model`](xref:TabularEditor.TOMWrapper.Model), mit dem Sie auf beliebige Objekte im derzeit geladenen Datenmodell zugreifen können. Beide Objekte sind als Membereigenschaften des globalen Objekts [`ScriptHost`](xref:TabularEditor.Shared.Scripting.ScriptHost) verfügbar.

Darüber hinaus enthält das `ScriptHost`-Objekt statische Methoden, die dem Script als globale Methoden zur Verfügung gestellt werden (d. h. Methoden, die Sie ohne das `ScriptHost`-Präfix aufrufen können). Diese Methoden werden auch als @script-helper-methods bezeichnet.

## Beispiel

```csharp
// Zeigt einen Dialog an, in dem der Benutzer aufgefordert wird, ein Measure auszuwählen:
var myMeasure = SelectMeasure();

// Erstellt ein neues Measure in der ersten Tabelle des Modells mit demselben Namen und
// demselben Ausdruck wie das zuvor ausgewählte Measure:
Model.Tables.First().AddMeasure(myMeasure.Name + " copy", myMeasure.Expression);
```

Weitere Beispiele finden Sie unter <xref:useful-script-snippets>.