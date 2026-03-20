---
uid: script-create-sum-measures-from-columns
title: Crear una medida SUM a partir de una columna
author: Morten Lønskov
updated: 2023-02-22
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Crear una medida SUM a partir de una columna

## Propósito del script

Si quieres crear rápidamente varias medidas que hagan SUM sobre las columnas que selecciones, este script lo hace por ti.

## Secuencia de comandos

### Crear medidas a partir de columnas

```csharp
// Crea una medida SUM para cada columna seleccionada actualmente y oculta la columna.
foreach(var c in Selected.Columns)
{
    var newMeasure = c.Table.AddMeasure(
        "Suma de " + c.Name,                    // Nombre
        "SUM(" + c.DaxObjectFullName + ")",    // Expresión DAX
        c.DisplayFolder                        // Carpeta de visualización
    );
    
    // Establece la cadena de formato de la nueva medida:
    newMeasure.FormatString = "0.00";

    // Añade documentación:
    newMeasure.Description = "Esta medida es la suma de la columna " + c.DaxObjectFullName;

    // Oculta la columna base:
    c.IsHidden = true;
}
```

### Explicación

Este fragmento usa la función `<Table>.AddMeasure(<name>, <expression>, <displayFolder>)` para crear una nueva medida en la tabla. Usamos la propiedad `DaxObjectFullName` para obtener el nombre completo de la columna y usarlo en la expresión DAX: `'TableName'[ColumnName]`.

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/create-sum-measures-from-columns.png" alt="Example of measures created with the script" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Un ejemplo de medidas creadas con este script.</figcaption>
</figure>