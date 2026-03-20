---
uid: script-edit-hidden-partitions
title: Editar particiones ocultas
author: Morten Lønskov
updated: 2023-02-21
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Editar particiones ocultas

## Propósito del script

Las tablas calculadas, los grupos de cálculo y los parámetros de campo no muestran particiones en Tabular Editor. Esto es así a propósito, ya que por lo general no se deben ni se pueden editar. Sin embargo, aún se puede acceder a las propiedades de la partición y editarlas mediante el siguiente fragmento de script.

## Secuencia de comandos

```csharp
Selected.Table.Partitions[0].Output();
```

### Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/show-hidden-partitions.png" alt="An example of the output box that appears, letting the user view and edit hidden partitions in the model." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Un ejemplo del cuadro de salida que aparece y permite al usuario ver y editar las particiones ocultas del modelo.</figcaption>
</figure>