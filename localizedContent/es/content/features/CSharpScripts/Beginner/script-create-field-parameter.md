---
uid: crear-parametro-de-campo
title: Crear parámetro de campo
author: Daniel Otykier
updated: 2024-01-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Crear parámetros de campo en

## Objetivo del script

Si quieres crear parámetros de campo en un modelo de Power BI con Tabular Editor o en un modelo de Direct Lake.

> [!TIP]
> ¿Quieres ver el script en acción? Echa un vistazo a este [vídeo de Guy in a Cube](https://www.youtube.com/watch?v=Cg6zRhwF-Ro), donde Patrick LeBlanc explica cómo usarlo paso a paso.

## Script

### Selecciona columnas o medidas para crear una tabla de parámetros de campo

```csharp
// Antes de ejecutar el script, selecciona las medidas o columnas que
// quieras usar como parámetros de campo (mantén pulsada la tecla CTRL para seleccionar varios
// objetos). Además, puedes cambiar el nombre de la tabla de parámetros de campo
// a continuación. NOTA: Si se usa en Power BI Desktop, debes habilitar las características no admitidas
// en Archivo > Preferencias (TE2) o Herramientas > Preferencias (TE3).
var name = "Parameter";

if(Selected.Columns.Count == 0 && Selected.Measures.Count == 0) throw new Exception("No columns or measures selected!");

// Construye el DAX para la tabla calculada en función de la selección actual:
var objects = Selected.Columns.Any() ? Selected.Columns.Cast<ITabularTableObject>() : Selected.Measures;
var dax = "{\n    " + string.Join(",\n    ", objects.Select((c,i) => string.Format("(\"{0}\", NAMEOF('{1}'[{0}]), {2})", c.Name, c.Table.Name, i))) + "\n}";

// Agrega la tabla calculada al modelo:
var table = Model.AddCalculatedTable(name, dax);

// En TE2, las columnas no se crean automáticamente a partir de una expresión DAX, así que 
// tendremos que agregarlas manualmente:
var te2 = table.Columns.Count == 0;
var nameColumn = te2 ? table.AddCalculatedTableColumn(name, "[Value1]") : table.Columns["Value1"] as CalculatedTableColumn;
var fieldColumn = te2 ? table.AddCalculatedTableColumn(name + " Fields", "[Value2]") : table.Columns["Value2"] as CalculatedTableColumn;
var orderColumn = te2 ? table.AddCalculatedTableColumn(name + " Order", "[Value3]") : table.Columns["Value3"] as CalculatedTableColumn;

if(!te2) {
    // Cambia el nombre de las columnas que se agregaron automáticamente en TE3:
    nameColumn.IsNameInferred = false;
    nameColumn.Name = name;
    fieldColumn.IsNameInferred = false;
    fieldColumn.Name = name + " Fields";
    orderColumn.IsNameInferred = false;
    orderColumn.Name = name + " Order";
}
// Establece las propiedades restantes para que funcionen los parámetros de campo
// Ver: https://twitter.com/markbdi/status/1526558841172893696
nameColumn.SortByColumn = orderColumn;
nameColumn.GroupByColumns.Add(fieldColumn);
fieldColumn.SortByColumn = orderColumn;
fieldColumn.SetExtendedProperty("ParameterMetadata", "{\"version\":3,\"kind\":2}", ExtendedPropertyType.Json);
fieldColumn.IsHidden = true;
orderColumn.IsHidden = true;
```

### Explicación

Antes de ejecutar el script, el usuario debe seleccionar en el Explorador TOM las medidas o columnas que quiere incluir en su tabla de parámetros de campo.
A continuación, los objetos seleccionados se insertan en una tabla calculada, que se configura automáticamente como tabla de parámetros de campo.

