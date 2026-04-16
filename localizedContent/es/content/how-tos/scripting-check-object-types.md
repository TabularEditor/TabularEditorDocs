---
uid: how-to-check-object-types
title: Cómo comprobar los tipos de objetos
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo comprobar los tipos de objetos

La jerarquía de TOM se basa en la herencia. `Column` es una clase base abstracta con los subtipos `DataColumn`, `CalculatedColumn` y `CalculatedTableColumn`. `Table` tiene los subtipos `CalculatedTable` y `CalculationGroupTable`. Use el tipo base cuando trabaje con propiedades compartidas como `Name`, `Description`, `IsHidden`, `FormatString` o `DisplayFolder`. Convierta a un subtipo concreto cuando necesite propiedades específicas del tipo, como `Expression` en `CalculatedColumn` o `SourceColumn` en `DataColumn`.

## Referencia rápida

```csharp
// Pattern matching -- checks type AND casts in one step
if (col is CalculatedColumn cc)
    Info(cc.Expression);  // Expression is only on CalculatedColumn, not base Column

// Filter a collection by type
var calcCols = Model.AllColumns.OfType<CalculatedColumn>();
var calcGroups = Model.Tables.OfType<CalculationGroupTable>();

// Runtime type name (use only for display/logging, not for logic)
var typeName = obj.GetType().Name;   // "DataColumn", "Measure", etc.
```

> [!NOTE]
> La coincidencia de patrones con declaración de variable (`col is CalculatedColumn cc`) requiere el compilador Roslyn en Tabular Editor 2. Configúrelo en **Archivo > Preferencias > General > Ruta del compilador**. Consulte [Compilar con Roslyn](xref:advanced-scripting#compiling-with-roslyn) para obtener más información. Tabular Editor 3 admite esto de forma predeterminada.

## Jerarquía de tipos

Las principales relaciones de herencia en el wrapper de TOM:

| Tipo base                                                                                                     | Subtipos                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| (xref:TabularEditor.TOMWrapper.Column)     | (xref:TabularEditor.TOMWrapper.DataColumn), (xref:TabularEditor.TOMWrapper.CalculatedColumn), (xref:TabularEditor.TOMWrapper.CalculatedTableColumn) |
| (xref:TabularEditor.TOMWrapper.Table)      | (xref:TabularEditor.TOMWrapper.CalculatedTable), (xref:TabularEditor.TOMWrapper.CalculationGroupTable)                                                                                                                 |
| (xref:TabularEditor.TOMWrapper.Partition)  | (xref:TabularEditor.TOMWrapper.MPartition), (xref:TabularEditor.TOMWrapper.EntityPartition), (xref:TabularEditor.TOMWrapper.PolicyRangePartition)   |
| (xref:TabularEditor.TOMWrapper.DataSource) | (xref:TabularEditor.TOMWrapper.ProviderDataSource), (xref:TabularEditor.TOMWrapper.StructuredDataSource)                                                                                                               |

## Filtrado de colecciones por tipo

`OfType<T>()` funciona en cualquier colección y devuelve una secuencia filtrada que contiene solo elementos del tipo especificado. Devuelve una secuencia vacía si ningún elemento coincide.

```csharp
// All calculated columns in the model (empty if model has none)
var calculatedColumns = Model.AllColumns.OfType<CalculatedColumn>();

// All M partitions (Power Query)
var mPartitions = Model.AllPartitions.OfType<MPartition>();

// All calculation group tables
var calcGroups = Model.Tables.OfType<CalculationGroupTable>();

// All regular tables (exclude calculation groups and calculated tables)
var regularTables = Model.Tables.Where(t => t is not CalculationGroupTable && t is not CalculatedTable);
```

## Coincidencia de patrones con el operador is

La coincidencia de patrones hace dos cosas: comprueba si un valor es de un tipo determinado y, opcionalmente, lo convierte y lo asigna a una variable nueva. La forma `x is Type xx` pregunta «¿`x` es de tipo `Type`?» y, si es así, te proporciona `xx` como una variable de ese tipo exacto.

Esto equivale a:

```csharp
if (col is CalculatedColumn)
{
    var cc = (CalculatedColumn)col; // explicit cast
    // use cc...
}
```

Si solo necesitas la comprobación booleana, usa `x is Type` sin la variable. Si también necesitas propiedades específicas del subtipo, usa `x is Type xx`.

```csharp
foreach (var col in Model.AllColumns)
{
    // Expression is only available on CalculatedColumn, not the base Column type
    if (col is CalculatedColumn cc)
        Info($"{cc.Name}: {cc.Expression}");
    else if (col is DataColumn dc)
        Info($"{dc.Name}: data column in {dc.Table.Name}");
}
```

## Equivalente en LINQ dinámico

En las reglas de BPA, el filtrado por tipo se controla mediante el ámbito **Se aplica a** de la regla. Configúralo en el tipo de objeto de destino (por ejemplo, **columnas calculadas**) en lugar de filtrar por tipo en la expresión. No hay ninguna conversión de tipos al estilo de C# disponible en LINQ dinámico.

## Errores comunes

> [!IMPORTANT]
>
> - `Column` es abstracta, pero puedes acceder a todas las propiedades definidas en el tipo base (`Name`, `DataType`, `FormatString`, `IsHidden`, `Description`, `DisplayFolder`) sin necesidad de realizar ninguna conversión de tipo. Realiza la conversión a un subtipo solo cuando necesites propiedades específicas del subtipo, como `Expression` en `CalculatedColumn`.
> - `OfType<T>()` filtra y convierte a la vez. `Where(x => x is T)` solo filtra, dejándote con el tipo base. Prefiere `OfType<T>()` cuando necesites acceder a propiedades del subtipo.
> - Las columnas de la **tabla calculada** se administran automáticamente. Edita la `Expression` de la tabla calculada para agregar o cambiar columnas. No puedes agregarlas directamente.

## Ver también

- @csharp-scripts
- @using-bpa-sample-rules-expressions
- @how-to-navigate-tom-hierarchy
- @how-to-tom-interfaces
