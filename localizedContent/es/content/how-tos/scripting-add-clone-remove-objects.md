---
uid: how-to-add-clone-remove-objects
title: Cómo agregar, clonar y eliminar objetos
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo agregar, clonar y eliminar objetos

Los C# Scripts pueden crear nuevos objetos del modelo, clonar los existentes y eliminarlos. Este artículo aborda los patrones de agregar, clonar y eliminar.

## Referencia rápida

```csharp
var table = Model.Tables["Sales"];
var measure = table.Measures["Revenue"];

// Add objects -- all parameters after the first are optional.
// See sections below for parameter details.
table.AddMeasure("Name", "DAX Expression", "Display Folder");
table.AddCalculatedColumn("Name", "DAX Expression", "Display Folder");
table.AddDataColumn("Name", "SourceColumn", "Display Folder", DataType.String);
table.AddHierarchy("Name", "Display Folder", table.Columns["Year"], table.Columns["Month"]);
Model.AddCalculatedTable("Name", "DAX Expression");
Model.AddPerspective("Name");
Model.AddRole("Name");
Model.AddTranslation("da-DK");

// Relationships
var rel = Model.AddRelationship();
rel.FromColumn = Model.Tables["Sales"].Columns["ProductKey"];   // many (N) side
rel.ToColumn = Model.Tables["Product"].Columns["ProductKey"];   // one (1) side

// Clone
var clone = measure.Clone("New Name");                         // same table
var cloneToOther = measure.Clone("New Name", true, Model.Tables["Reporting"]); // different table

// Delete (always materialize with ToList() before modifying a collection in a loop)
measure.Delete();
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

## Agregar medidas

`AddMeasure()` crea y devuelve una nueva medida en una tabla. El primer parámetro es el nombre, el segundo es una expresión DAX y el tercero es la carpeta de visualización. Todos los parámetros, excepto el primero, son opcionales.

Captura el objeto devuelto en una variable para establecer propiedades adicionales. Este patrón es el mismo en todos los métodos `Add*`.

```csharp
var table = Model.Tables["Sales"];

// Create a measure and set properties on the returned object
var m = table.AddMeasure(
    "Revenue",                   // name
    "SUM('Sales'[Amount])"       // DAX expression
);
m.FormatString = "#,##0.00";
m.Description = "Total sales amount";

// With display folder
var m2 = table.AddMeasure(
    "Cost",                      // name
    "SUM('Sales'[Cost])",        // DAX expression
    "Financial"                  // display folder
);
```

## Agregar columnas

```csharp
// Calculated column -- first parameter is the name, second is a DAX expression
var cc = table.AddCalculatedColumn(
    "Profit",                              // name
    "'Sales'[Amount] - 'Sales'[Cost]"      // DAX expression
);
cc.DataType = DataType.Decimal;
cc.FormatString = "#,##0.00";

// Data column -- maps to a source column in the partition query
var dc = table.AddDataColumn(
    "Region",              // name
    "RegionName",          // source column name
    "Geography",           // display folder
    DataType.String        // data type
);
```

> [!WARNING]
> Agregar una columna de datos no modifica la consulta de partición de la tabla. Debes actualizar la expresión M o la consulta SQL por separado para incluir una columna de origen que coincida con el parámetro `sourceColumn`.

## Agregar jerarquías

El parámetro `levels` es variádico. Pasa cualquier número de columnas en una sola llamada para crear automáticamente los niveles correspondientes.

```csharp
var dateTable = Model.Tables["Date"];
var h = dateTable.AddHierarchy(
    "Calendar",                        // name
    "",                                // display folder
    dateTable.Columns["Year"],         // level 1
    dateTable.Columns["Quarter"],      // level 2
    dateTable.Columns["Month"]         // level 3
);
```

O agrega niveles de uno en uno:

```csharp
var h = dateTable.AddHierarchy("Fiscal");
h.AddLevel(dateTable.Columns["FiscalYear"]);
h.AddLevel(dateTable.Columns["FiscalQuarter"]);
h.AddLevel(dateTable.Columns["FiscalMonth"]);
```

## Agregar tablas calculadas

```csharp
var ct = Model.AddCalculatedTable(
    "DateKey List",                    // name
    "VALUES('Date'[DateKey])"          // DAX expression
);
```

## Agregar relaciones

`AddRelationship()` crea y devuelve una relación vacía. Debes establecer las columnas explícitamente.

`FromColumn` es el lado de muchos (N) y `ToColumn` es el lado de uno (1). Tabular Editor no detecta la dirección automáticamente. Un truco mnemotécnico útil: F de From, F de Fact (tabla de hechos; el lado de muchos).

Las relaciones nuevas tienen como valor predeterminado `CrossFilteringBehavior.OneDirection` e `IsActive = true`. Establece estos valores solo si necesitas que sean distintos.

```csharp
var rel = Model.AddRelationship();
rel.FromColumn = Model.Tables["Sales"].Columns["ProductKey"];   // many side (fact)
rel.ToColumn = Model.Tables["Product"].Columns["ProductKey"];   // one side (dimension)

// Only set these if you need non-default values:
// rel.CrossFilteringBehavior = CrossFilteringBehavior.BothDirections;
// rel.IsActive = false;
```

## Clonación de objetos

`Clone()` crea una copia con todas las propiedades, anotaciones y traducciones.

```csharp
// Clone within the same table
var original = Model.AllMeasures.First(m => m.Name == "Revenue");
var copy = original.Clone("Revenue Copy");

// Clone to a different table (with translations)
var copy2 = original.Clone("Revenue Copy", true, Model.Tables["Reporting"]);
```

## Generar medidas a partir de columnas

Un patrón habitual: recorre las columnas seleccionadas y crea medidas derivadas. Observa el uso de `DaxObjectFullName`, que devuelve la referencia DAX completa y con las comillas correctas (por ejemplo, `'Sales'[Amount]`) para evitar errores de comillas.

```csharp
foreach (var col in Selected.Columns)
{
    var m = col.Table.AddMeasure(
        "Sum of " + col.Name,
        "SUM(" + col.DaxObjectFullName + ")",
        col.DisplayFolder
    );
    m.FormatString = "0.00";
    col.IsHidden = true;
}
```

## Eliminar objetos

Invoca `Delete()` en cualquier objeto con nombre para eliminarlo. Al modificar una colección en un bucle (eliminando, agregando o moviendo objetos), llama siempre primero a `.ToList()` para materializar una instantánea.

```csharp
// Delete a single object
Model.AllMeasures.First(m => m.Name == "Temp").Delete();

// Delete multiple objects safely
Model.AllMeasures
    .Where(m => m.HasAnnotation("DEPRECATED"))
    .ToList()
    .ForEach(m => m.Delete());
```

## Errores comunes

> [!WARNING]
>
> - Llama siempre a `.ToList()` o `.ToArray()` antes de modificar objetos en un bucle. Sin ello, modificar la colección durante la iteración provoca: `"Collection was modified; enumeration operation may not complete."`
> - `AddRelationship()` crea una relación incompleta. Debes asignar tanto `FromColumn` como `ToColumn` antes de que el modelo se valide.
> - `Column` es una clase abstracta, pero puedes acceder a todas las propiedades base (`Name`, `DataType`, `FormatString`, `IsHidden`) sin necesidad de hacer un cast. Haz cast a un subtipo solo para propiedades específicas del tipo.
> - `Clone()` copia todos los metadatos, incluidas las anotaciones, las traducciones y la pertenencia a perspectivas. Elimina los metadatos no deseados después de clonar.

## Ver también

- @useful-script-snippets
- @script-create-sum-measures-from-columns
- @how-to-navigate-tom-hierarchy
- @how-to-use-selected-object
- (xref:TabularEditor.TOMWrapper.Measure) -- Referencia de la API de la clase medida
- (xref:TabularEditor.TOMWrapper.Column) -- Referencia de la API de la clase Column
- (xref:TabularEditor.TOMWrapper.Hierarchy) -- Referencia de la API de jerarquía
- (xref:TabularEditor.TOMWrapper.SingleColumnRelationship) -- Referencia de la API de relación
