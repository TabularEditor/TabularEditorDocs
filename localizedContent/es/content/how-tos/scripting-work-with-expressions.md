---
uid: how-to-work-with-expressions
title: Cómo trabajar con expresiones y propiedades DAX
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo trabajar con expresiones y propiedades DAX

Las medidas, las columnas calculadas, los elementos de cálculo, los KPI y las particiones tienen expresiones. En este artículo verás cómo leer, modificar y generar expresiones DAX, y cómo trabajar con la interfaz `IExpressionObject`.

## Referencia rápida

```csharp
// Read and set expressions
measure.Expression                                    // DAX formula string
measure.Expression = "SUM('Sales'[Amount])";          // set formula
measure.FormatString = "#,##0.00";                    // static format
measure.FormatStringExpression = "...";               // dynamic format (DAX)

// Calculated column
calcCol.Expression                                    // DAX formula

// Partition (M query)
partition.Expression                                  // M/Power Query expression

// DAX object names for code generation
column.DaxObjectFullName    // 'Sales'[Amount]
column.DaxObjectName        // [Amount]
measure.DaxObjectFullName   // 'Sales'[Revenue]
measure.DaxObjectName       // [Revenue]
table.DaxObjectFullName     // 'Sales'
table.DaxTableName          // 'Sales'

// Formatting
FormatDax(measure);         // queue for formatting
CallDaxFormatter();         // execute queued formatting

// Tokenizing
measure.Tokenize().Count    // DAX token count (complexity metric)
```

## Leer y modificar las expresiones de las medidas

```csharp
var m = Model.AllMeasures.First(m => m.Name == "Revenue");

// Read the current DAX
var dax = m.Expression;

// Replace a table reference in the expression
m.Expression = m.Expression.Replace("'Old Table'", "'New Table'");

// Set format string
m.FormatString = "#,##0.00";
```

## Propiedades de nombres de objetos DAX

Cada `IDaxObject` (tabla, columna, medida o jerarquía) tiene propiedades que devuelven su nombre en un formato compatible con DAX y con el entrecomillado adecuado.

| Propiedad           | Ejemplo de columna | Ejemplo de medida | Ejemplo de tabla |
| ------------------- | ------------------ | ----------------- | ---------------- |
| `DaxObjectName`     | `[Amount]`         | `[Revenue]`       | `'Sales'`        |
| `DaxObjectFullName` | `'Sales'[Amount]`  | `[Revenue]`       | `'Sales'`        |
| `DaxTableName`      | `'Sales'`          | `'Sales'`         | `'Sales'`        |

> [!NOTE]
> En el caso de las medidas, `DaxObjectFullName` devuelve el mismo valor que `DaxObjectName` (sin calificar). En DAX, no hace falta calificar las medidas con la tabla. En las columnas, `DaxObjectFullName` incluye el prefijo de la tabla.

Utilice estos valores al generar DAX para evitar errores con las comillas:

```csharp
// Generate a SUM measure for each selected column
foreach (var col in Selected.Columns)
{
    col.Table.AddMeasure(
        "Sum of " + col.Name,
        "SUM(" + col.DaxObjectFullName + ")",
        col.DisplayFolder
    );
}
```

## La interfaz IExpressionObject

Los objetos que contienen expresiones implementan (xref:TabularEditor.TOMWrapper.IExpressionObject). En Tabular Editor 2, esta interfaz solo proporciona la propiedad `Expression`. En Tabular Editor 3, agrega `GetExpression()`, `SetExpression()` y `GetExpressionProperties()` para trabajar con varios tipos de expresión en un mismo objeto.

```csharp
// Tabular Editor 2: use the Expression property directly
measure.Expression = "SUM('Sales'[Amount])";
var dax = measure.Expression;
```

> [!NOTE]
> El siguiente patrón `GetExpression`/`SetExpression` solo está disponible en Tabular Editor 3. En Tabular Editor 2, accede directamente a la propiedad `Expression` del objeto.

```csharp
// Tabular Editor 3 only: list all expression types on an object
var exprObj = (IExpressionObject)measure;
foreach (var prop in exprObj.GetExpressionProperties())
{
    var expr = exprObj.GetExpression(prop);
    if (!string.IsNullOrEmpty(expr))
        Info($"{prop}: {expr}");
}

// Set an expression by type
exprObj.SetExpression(ExpressionProperty.Expression, "SUM('Sales'[Amount])");
exprObj.SetExpression(ExpressionProperty.FormatStringExpression, "\"$#,##0.00\"");
```

La enumeración `ExpressionProperty` (solo en Tabular Editor 3) incluye:

| Valor                    | Se usa en                                           |
| ------------------------ | --------------------------------------------------- |
| `Expression`             | Medidas, columnas calculadas y elementos de cálculo |
| `DetailRowsExpression`   | Medidas                                             |
| `FormatStringExpression` | Medidas y elementos de cálculo                      |
| `TargetExpression`       | KPI                                                 |
| `StatusExpression`       | KPI                                                 |
| `TrendExpression`        | KPI                                                 |
| `MExpression`            | Particiones de M                                    |

## Dar formato a DAX

`FormatDax()` pone los objetos en cola para darles formato. El formato se aplica automáticamente al final del script. Llama a `CallDaxFormatter()` solo cuando necesites el resultado con formato a mitad del script.

```csharp
// Typical usage -- formatting happens automatically after the script ends
foreach (var m in Model.AllMeasures)
    FormatDax(m);

// Advanced: force formatting mid-script to read the result
var before = Selected.Measure.Expression;
FormatDax(Selected.Measure);
CallDaxFormatter();                      // format NOW, not at script end
var after = Selected.Measure.Expression; // now contains the formatted DAX
```

## Tokenización

`Tokenize()` devuelve los tokens de DAX de una expresión. Los tokens proporcionan una representación fiable, independiente de los espacios en blanco y del formato. Usa la tokenización cuando necesites analizar la estructura de una expresión DAX más allá de lo que ya ofrecen las funciones integradas de seguimiento de dependencias y cambio de nombre.

```csharp
foreach (var m in Model.AllMeasures.OrderByDescending(m => m.Tokenize().Count))
    Info($"{m.Name}: {m.Tokenize().Count} tokens");
```

## Buscar y reemplazar en expresiones

El reemplazo de cadenas con `Replace()` actúa sobre el texto sin procesar de la expresión, incluso dentro de literales de texto y comentarios. Para reemplazar de forma selectiva construcciones DAX específicas (referencias a tablas, referencias a columnas), analiza en su lugar la expresión tokenizada.

```csharp
// Replace a column reference across all measures
foreach (var m in Model.AllMeasures.Where(m => m.Expression.Contains("[Old Column]")))
{
    m.Expression = m.Expression.Replace("[Old Column]", "[New Column]");
}
```

## Equivalente de LINQ dinámico

En las expresiones de reglas de BPA, se accede directamente a las propiedades de la expresión en el objeto en contexto.

| C# Script                                 | LINQ dinámico (BPA)  |
| ----------------------------------------- | --------------------------------------- |
| `string.IsNullOrWhiteSpace(m.Expression)` | `String.IsNullOrWhitespace(Expression)` |
| `m.Expression.Contains("CALCULATE")`      | `Expression.Contains("CALCULATE")`      |
| `m.FormatString == ""`                    | `FormatString = ""`                     |
| `m.Expression.StartsWith("SUM")`          | `Expression.StartsWith("SUM")`          |

> [!TIP]
> Al comprobar el contenido de una expresión con `Contains()` o `StartsWith()`, usa una comparación que no distinga entre mayúsculas y minúsculas para evitar pasar por alto coincidencias debidas a diferencias de formato: `m.Expression.Contains("CALCULATE", StringComparison.OrdinalIgnoreCase)`.

## Errores habituales

> [!IMPORTANT]
>
> - `DataColumn` no tiene una propiedad `Expression`. Solo `CalculatedColumn`, `medida`, `CalculationItem` y `partición` tienen expresiones. Acceder a la propiedad `Expression` de una `DataColumn` provoca un error de compilación o una excepción en tiempo de ejecución, según el contexto.
> - `DaxObjectName` devuelve el nombre sin calificar (por ejemplo, `[Revenue]`), mientras que `DaxObjectFullName` incluye el prefijo de la tabla (por ejemplo, `'Sales'[Revenue]`). Use `DaxObjectFullName` para referirse a columnas en DAX y `DaxObjectName` para referirse a medidas cuando sea opcional calificar con la tabla.
> - `FormatDax()` en Tabular Editor 2 llama a la API externa de daxformatter.com y requiere una conexión a Internet. Tabular Editor 3 usa un formateador integrado de forma predeterminada. Para usar daxformatter.com en TE3, actívalo en las preferencias.

## Ver también

- @csharp-scripts
- @using-bpa-sample-rules-expressions
- @how-to-filter-query-objects-linq
- @script-find-replace
