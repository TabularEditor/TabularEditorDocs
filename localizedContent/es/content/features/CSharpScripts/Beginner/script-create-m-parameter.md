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

## Propósito del script

Si quieres crear un nuevo parámetro M dinámico para usarlo en consultas de Power Query (particiones M o expresiones compartidas).

## Secuencia de comandos

### Crear una nueva partición M

```csharp
// Este script crea un nuevo parámetro M en las 'Expresiones compartidas' de un modelo.
//
// Crea una nueva expresión compartida llamada "New Parameter"
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

// Muestra un mensaje con instrucciones sobre cómo configurar y usar el parámetro
Info ( 
    "Se ha creado una nueva expresión compartida llamada 'New Parameter', que es una plantilla de parámetro M." + 
    "\n------------------------------------------------------\n" + 
    "Para configurarlo:" +
    "\n------------------------------------------------------\n    " + 
    "1. Reemplaza el texto 'New Parameter' por el valor de parámetro deseado\n    " +
    "2. Establece el tipo de datos correctamente\n    " +
    "3. Reemplaza cualquier valor encontrado en las particiones M por la referencia al parámetro." );
```

### Explicación

Este fragmento crea un nuevo parámetro M en 'Expresiones compartidas', al que puedes hacer referencia desde las consultas de Power Query de tus particiones M.

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-new-m-parameter.png" alt="An example of the Info box that appears to inform the user that the M Parameter was successfully created, and recommending next steps to configure / use it in the M Partitions." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Un ejemplo del cuadro informativo que aparece para informar al usuario de que el parámetro M se creó correctamente y recomendar los siguientes pasos para configurarlo / usarlo en las particiones M.</figcaption>
</figure>