---
uid: script-count-things
title: Contar objetos del modelo
author: Kurt Buhler
updated: 2023-02-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Contar elementos en el modelo

## Propósito del script

Si quieres obtener una visión general de lo que hay en un modelo y cuántos objetos contiene:

- Cuántas medidas hay en un modelo.
- Cuántas columnas y columnas calculadas hay en un modelo.
- Cuántas tablas y tablas calculadas hay en un modelo.
- Cuántas relaciones, relaciones inactivas, etc., hay.

## Script

### Contar el número de objetos del modelo por tipo

```csharp
// Este script cuenta los objetos de tu modelo y los muestra en un cuadro de información emergente.
// No realiza ningún cambio en este modelo.
//
// Usa este script cuando abras un modelo nuevo y necesites una 'vista de helicóptero' del contenido.
//
// Contar grupos de cálculo y elementos de cálculo
int _calcgroups = 0;
int _calcitems = 0;
foreach (  var _calcgroup  in Model.CalculationGroups )
{
    _calcgroups = _calcgroups + 1;
    foreach (  var _item  in _calcgroup.CalculationItems )
    {
        _calcitems = _calcitems + 1;
    }
}

// Contar particiones y parámetros de DAX
int _partitions = 0;
int _whatifparameters = 0;
int _fieldparameters = 0;
foreach (  var _table  in Model.Tables )
{
    foreach (  var _partition  in _table.Partitions )
    {
        string _type = Convert.ToString(_partition.SourceType);
        string _exp = Convert.ToString(_partition.Expression);
        if ( _type == "M" )
        {
            _partitions = _partitions + 1;
        }
        else if ( _type == "Calculated" && _exp.Contains("NAMEOF") )
        {
            _fieldparameters = _fieldparameters + 1;
        }
        else if ( _type == "Calculated" && _exp.Contains("GENERATESERIES") )
        {
            _whatifparameters = _whatifparameters + 1;
        }
            
    }
}

// Promedio de la longitud de las medidas
decimal _numLines = 0;
decimal _numChars = 0;
int _measures = Model.AllMeasures.Count();
foreach ( var _measure in Model.AllMeasures )
{
    _numLines = _numLines + _measure.Expression.Split("\n").Length;
    _numChars = _numChars + _measure.Expression.Length;
}
_numLines = Math.Round(_numLines / _measures, 1);
_numChars = Math.Round(_numChars / _measures, 1);


// Mostrar el cuadro de información emergente
Info ( "En el modelo, vemos los siguientes objetos:\n\n"

        + "-----------------------------------------\n"
        + "Objetos de datos\n"
        + "-----------------------------------------\n"
        + " ├─ Expresiones de PQ: " + Convert.ToString(Model.Expressions.Count()) + "\n"
        + " │\n"
        + " └─ Tablas: " + Convert.ToString(Model.Tables.Count()) + "\n"
        + "       ├─ Tablas con actualización incremental: " + 
            Convert.ToString(Model.Tables.Where(
                _ir => 
                Convert.ToString(_ir.EnableRefreshPolicy) 
                == 
                "True").Count()) + "\n"
                
        + "       │\n"
        + "       ├─ Tablas calculadas: " + 
            Convert.ToString(
                Model.Tables.Where(
                    _tables => 
                    Convert.ToString(_tables.Columns[0].Type) 
                    == 
                    "CalculatedTableColumn").Count()) + "\n"

        + "       │   ├─ Parámetros What if: " + 
            Convert.ToString(_whatifparameters) + "\n"
        + "       │   └─ Parámetros de campo: " + 
            Convert.ToString(_fieldparameters) + "\n"
        + "       │\n"
        + "       ├─ Particiones de M: " + 
            Convert.ToString(_partitions) + "\n"
        + "       │\n"
        + "       └─ Total de columnas de tablas: " + 
            Convert.ToString(Model.AllColumns.Count()) + "\n\n"

        + "-----------------------------------------\n"
        + "Objetos DAX\n"
        + "-----------------------------------------\n"
        + " ├─ Relaciones: " + 
            Convert.ToString(Model.Relationships.Count()) + "\n"
        + " │   ├─ Bidireccionales: " + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.CrossFilteringBehavior) 
                == 
                "BothDirections").Count()) + "\n"

        + " │   ├─ De muchos a muchos: " + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.FromCardinality) 
                == 
                "Many" 
                && 
                Convert.ToString(_relationships.ToCardinality) 
                == 
                "Many").Count()) + "\n"

        + " │   ├─ De uno a uno: " + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.FromCardinality) 
                == 
                "One" 
                && 
                Convert.ToString(_relationships.ToCardinality) 
                == 
                "One").Count()) + "\n"

        + " │   └─ Inactivas: " + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.IsActive) 
                == 
                "False").Count()) + "\n"

        + " │\n"
        + " ├─ Grupos de cálculo: " + 
            Convert.ToString(_calcgroups) + "\n"
        + " │   └─ Elementos de cálculo: " + 
            Convert.ToString(_calcitems) + "\n" 
        + " │\n"
        + " ├─ Columnas calculadas: " + 
            Convert.ToString(Model.AllColumns.Where(
                _columns => 
                Convert.ToString(_columns.Type) 
                == 
                "Calculated").Count()) + "\n"

        + " │\n"
        + " └─ Medidas: " + 
            Convert.ToString(_measures) + "\n" 
        + "     └─ Promedio de líneas de DAX: " + 
            Convert.ToString(_numLines) + " líneas \n" 
        + "     └─ Promedio de caracteres de DAX: " + 
            Convert.ToString(_numChars) + " caracteres \n\n" 
       
        + "-----------------------------------------\n"
        + "Otros objetos\n"
        + "-----------------------------------------\n"
        + " ├─ Roles de seguridad de datos: " + 
            Convert.ToString(Model.Roles.Count()) + "\n"
        + " ├─ Fuentes de datos explícitas: " + 
            Convert.ToString(Model.DataSources.Count()) + "\n"
        + " ├─ Perspectivas: " + 
            Convert.ToString(Model.Perspectives.Count()) + "\n"
        + " └─ Traducciones: " + 
            Convert.ToString(Model.Cultures.Count()));
```

### Explicación

Este fragmento recorre el modelo y cuenta los distintos tipos de objeto, mostrándolos en un formato jerárquico de tipo «árbol de nodos», construido manualmente.
Puedes comentar las partes que no necesites para tus propósitos.

## Ejemplo de salida

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-count-things-output.png" alt="Example of the dialog pop-up that informs the user of how many rows are in the selected table upon running the script." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Un ejemplo de la salida del cuadro de información, que indica al usuario el número de objetos del modelo al ejecutar el script. Si hay objetos que no son de interés, el usuario puede comentarlos o eliminarlos del script y volver a ejecutarlo.</figcaption>
</figure>