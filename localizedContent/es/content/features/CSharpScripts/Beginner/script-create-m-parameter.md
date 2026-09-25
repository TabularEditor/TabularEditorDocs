---
uid: script-create-m-parameter
title: Crear parámetro M
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Crear partición M

## Objetivo del script

Si quieres crear un nuevo parámetro M dinámico para usarlo en consultas de Power Query (particiones M o expresiones compartidas).

## Script

### Crear una nueva partición M

```csharp
// This script creates a new M parameter in the 'Shared Expressions' of a model.
//
// Create a new shared expression called "New Parameter"
Model.AddExpression( 
    "New Parameter", 
    @"
""Parameter Text"" meta
[
	IsParameterQuery = true,
	IsParameterQueryRequired = true,
	Type = type text
]"
);

// Provides an output informing how to configure and use the parameter
Info ( 
    "Created a new Shared Expression called 'New Parameter', which is an M Parameter template." + 
    "\n------------------------------------------------------\n" + 
    "To configure:" +
    "\n------------------------------------------------------\n    " + 
    "1. Replace the text 'New Parameter' with the desired parameter value\n    " +
    "2. Set the data type appropriately\n    " +
    "3. Replace any values found in the M partitions with the parameter reference." );
```

### Explicación

Este fragmento crea un nuevo parámetro M en 'Expresiones compartidas', al que puedes hacer referencia desde las consultas de Power Query de tus particiones M.

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-new-m-parameter.png" alt="An example of the Info box that appears to inform the user that the M Parameter was successfully created, and recommending next steps to configure / use it in the M Partitions." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Un ejemplo del cuadro informativo que aparece para informar al usuario de que el parámetro M se creó correctamente y recomendar los siguientes pasos para configurarlo / usarlo en las particiones M.</figcaption>
</figure>