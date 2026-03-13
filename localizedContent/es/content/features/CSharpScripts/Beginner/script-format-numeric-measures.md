---
uid: script-formato-medidas-numericas
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

## Propósito del script

Te permite establecer rápidamente cadenas de formato predeterminadas para las medidas seleccionadas.

<br></br>

> [!NOTE]
> El script usa ciertos estándares de nomenclatura, así que quizá quieras ajustarlo para que encaje con los tuyos. <br></br>

## Script

### Título del script

```csharp
// Este script está pensado para dar formato a todas las medidas con una cadena de formato predeterminada
foreach (var ms in Selected.Measures) {
//No establecer la cadena de formato en medidas ocultas
	if (ms.IsHidden) continue;
// Si la cadena de formato está vacía, continuar. 
	if (!string.IsNullOrWhiteSpace(ms.FormatString)) continue;
//Si el tipo de datos es int, establecer una cadena de formato de número entero
	if (ms.DataType == DataType.Int64) ms.FormatString = "#,##0";
//Si el tipo de datos es double o decimal 
	if (ms.DataType == DataType.Double || ms.DataType == DataType.Decimal) {
    //y el nombre contiene # o QTY, entonces establecer la cadena de formato como un número entero
		if (ms.Name.Contains("#")
			|| ms.Name.IndexOf("QTY", StringComparison.OrdinalIgnoreCase) >= 0) ms.FormatString = "#,##0";
		//si no, establecer una cadena de formato decimal. 
    else ms.FormatString = "#,##0.00";
	}
}
```

### Explicación

El script toma cada una de las medidas seleccionadas y recorre cada una de ellas para establecer una cadena de formato predeterminada según diversas condiciones.