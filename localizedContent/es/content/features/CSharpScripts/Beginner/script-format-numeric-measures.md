---
uid: script-format-numeric-measures
title: Formatear medidas numéricas
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Formatear medidas numéricas

## Objetivo del script

Te permite establecer rápidamente cadenas de formato predeterminadas para las medidas seleccionadas.

<br></br>

> [!NOTE]
> El script usa ciertos estándares de nomenclatura, así que quizá quieras ajustarlo para que encaje con los tuyos. <br></br>

## Script

### Título del script

```csharp
// This script is meant to format all measures with a default formatstring
foreach (var ms in Selected.Measures) {
//Don't set format string on hidden measures
	if (ms.IsHidden) continue;
// If the format string is empty continue. 
	if (!string.IsNullOrWhiteSpace(ms.FormatString)) continue;
//If the data type is int set a whole number format string
	if (ms.DataType == DataType.Int64) ms.FormatString = "#,##0";
//If the datatype is double or decimal 
	if (ms.DataType == DataType.Double || ms.DataType == DataType.Decimal) {
    //and the name contains # or QTY then set the format string to a whole number
		if (ms.Name.Contains("#")
			|| ms.Name.IndexOf("QTY", StringComparison.OrdinalIgnoreCase) >= 0) ms.FormatString = "#,##0";
		//otherwise set it a decimal format string. 
    else ms.FormatString = "#,##0.00";
	}
}
```

### Explicación

El script toma cada una de las medidas seleccionadas y recorre cada una de ellas para establecer una cadena de formato predeterminada según diversas condiciones.