---
uid: script-count-rows
title: Contar filas de una tabla
author: Kurt Buhler
updated: 2023-02-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Contar filas en una tabla

## Objetivo del script

Si quieres ver cuántas filas se han cargado en una tabla o comprobar rápidamente si la tabla se ha cargado en absoluto.
Este script requiere una conexión a un modelo remoto o una conexión mediante el modo del área de trabajo.

## Script

### Contar las filas de la tabla seleccionada

```csharp
// Este script cuenta las filas de una tabla seleccionada y muestra el resultado en un cuadro de información emergente.
// No escribe ningún cambio en este modelo.
//
// Usa este script cuando quieras comprobar si una tabla se ha cargado o cuántas filas tiene.
//
// Obtener el nombre de la tabla
string _TableName = 
    Selected.Table.DaxObjectFullName;

// Contar filas de la tabla
string _dax = 
    "{ FORMAT( COUNTROWS (" + _TableName + "), \"#,##0\" ) }";

// Evaluar DAX
string _TableRows = 
    Convert.ToString(EvaluateDax( _dax ));

// Devolver el resultado en una ventana emergente
Info ( "Número de filas en " + _TableName + ": " + _TableRows);
```

### Explicación

Este fragmento recorre el modelo y cuenta los distintos tipos de objetos, mostrándolos en un formato jerárquico de "nodo y árbol" construido manualmente.
Puedes comentar

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-count-rows-output.png" alt="Example of the dialog pop-up that informs the user of how many rows are in the selected table upon running the script." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Un ejemplo del cuadro de información que aparece para indicar al usuario cuántas filas hay en la tabla seleccionada al ejecutar este script.</figcaption>
</figure>