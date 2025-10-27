---
uid: script-count-things
title: Modellobjekte zählen
author: Kurt Buhler
updated: 2023-02-27
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---

# Objekte im Modell zählen

## Skriptzweck

Wenn Sie einen Überblick über den Inhalt eines Modells und die Anzahl der Objekte erhalten möchten:

- Wie viele Maße sind in einem Modell.
- Wie viele Spalten und berechnete Spalten sind in einem Modell.
- Wie viele Tabellen und berechnete Tabellen sind in einem Modell.
- Wie viele Beziehungen, inaktive Beziehungen usw.

## Skript

### Die Anzahl der Modellobjekte nach Typ zählen

```csharp
// Dieses Skript zählt Objekte in Ihrem Modell und zeigt sie in einem Pop-up-Informationsfeld an.
// Es nimmt keine Änderungen an diesem Modell vor.
//
// Verwenden Sie dieses Skript, wenn Sie ein neues Modell öffnen und einen "Hubschrauberperspektive" auf den Inhalt benötigen.
//
// Berechnungsgruppen und Berechnungselemente zählen
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

// Partitionen und DAX-Parameter zählen
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

// Durchschnittliche Messlänge
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


// Pop-up zurückgeben
Info ( "Im Modell sehen wir die folgenden Objekte:\n\n"

        + "-----------------------------------------\n"
        + "Datenobjekte\n"
        + "-----------------------------------------\n"
        + " ├─ PQ-Ausdrücke: " + Convert.ToString(Model.Expressions.Count()) + "\n"
        + " │\n"
        + " └─ Tabellen: " + Convert.ToString(Model.Tables.Count()) + "\n"
        + "       ├─ Tabellen mit inkrementeller Aktualisierung: " + 
            Convert.ToString(Model.Tables.Where(
                _ir => 
                Convert.ToString(_ir.EnableRefreshPolicy) 
                == 
                "True").Count()) + "\n"
                
        + "       │\n"
        + "       ├─ Berechnete Tabellen: " + 
            Convert.ToString(
                Model.Tables.Where(
                    _tables => 
                    Convert.ToString(_tables.Columns[0].Type) 
                    == 
                    "CalculatedTableColumn").Count()) + "\n"

        + "       │   ├─ What-if-Parameter: " + 
            Convert.ToString(_whatifparameters) + "\n"
        + "       │   └─ Feldparameter: " + 
            Convert.ToString(_fieldparameters) + "\n"
        + "       │\n"
        + "       ├─ M-Partitionen: " + 
            Convert.ToString(_partitions) + "\n"
        + "       │\n"
        + "       └─ Gesamttabellenspalten: " + 
            Convert.ToString(Model.AllColumns.Count()) + "\n\n"

        + "-----------------------------------------\n"
        + "DAX-Objekte\n"
        + "-----------------------------------------\n"
        + " ├─ Beziehungen: " + 
            Convert.ToString(Model.Relationships.Count()) + "\n"
        + " │   ├─ Bidirektional: " + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.CrossFilteringBehavior) 
                == 
                "BothDirections").Count()) + "\n"

        + " │   ├─ Viele-zu-Viele: " + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.FromCardinality) 
                == 
                "Many" 
                && 
                Convert.ToString(_relationships.ToCardinality) 
                == 
                "Many").Count()) + "\n"

        + " │   ├─ Eins-zu-Eins: " + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.FromCardinality) 
                == 
                "One" 
                && 
                Convert.ToString(_relationships.ToCardinality) 
                == 
                "One").Count()) + "\n"

        + " │   └─ Inaktiv: " + 
            Convert.ToString(Model.Relationships.Where(
                _relationships => 
                Convert.ToString(_relationships.IsActive) 
                == 
                "False").Count()) + "\n"

        + " │\n"
        + " ├─ Berechnungsgruppen: " + 
            Convert.ToString(_calcgroups) + "\n"
        + " │   └─ Berechnungselemente: " + 
            Convert.ToString(_calcitems) + "\n" 
        + " │\n"
        + " ├─ Berechnete Spalten: " + 
            Convert.ToString(Model.AllColumns.Where(
                _columns => 
                Convert.ToString(_columns.Type) 
                == 
                "Calculated").Count()) + "\n"

        + " │\n"
        + " └─ Measures: " + 
            Convert.ToString(_measures) + "\n" 
        + "     └─ Durchschn. DAX-Zeilen: " + 
            Convert.ToString(_numLines) + " Zeilen \n" 
        + "     └─ Durchschn. DAX-Zeichen: " + 
            Convert.ToString(_numChars) + " Zeichen \n\n" 
       
        + "-----------------------------------------\n"
        + "Sonstige Objekte\n"
        + "-----------------------------------------\n"
        + " ├─ Datensicherheitsrollen: " + 
            Convert.ToString(Model.Roles.Count()) + "\n"
        + " ├─ Explizite Datenquellen: " + 
            Convert.ToString(Model.DataSources.Count()) + "\n"
        + " ├─ Perspektiven: " + 
            Convert.ToString(Model.Perspectives.Count()) + "\n"
        + " └─ Übersetzungen: " + 
            Convert.ToString(Model.Cultures.Count()));
```

### Erklärung

Dieses Snippet durchläuft das Modell und zählt die verschiedenen Objekttypen und zeigt sie in einem hierarchischen "Knoten- und Baum"-Format an, das manuell konstruiert ist.
Sie können die Teile auskommentieren, die Sie nicht benötigen.

## Beispielausgabe

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-count-things-output.png" alt="Example of the dialog pop-up that informs the user of how many rows are in the selected table upon running the script." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Abbildung 1:</strong> Ein Beispiel der Info-Box-Ausgabe, die den Benutzer über die Anzahl der Objekte im Modell bei der Skriptausführung informiert. Wenn bestimmte Objekte nicht relevant sind, können sie vom Benutzer auskommentiert oder aus dem Skript entfernt werden, und das Skript kann erneut ausgeführt werden.</figcaption>
</figure>