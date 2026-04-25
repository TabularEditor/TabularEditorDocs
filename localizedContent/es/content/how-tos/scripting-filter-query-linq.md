---
uid: how-to-filter-query-objects-linq
title: Cómo filtrar y consultar objetos con LINQ
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo filtrar y consultar objetos con LINQ

Los C# Script utilizan métodos estándar de LINQ para filtrar, buscar y transformar colecciones de objetos TOM. Estos patrones son la base. Use métodos que devuelven colecciones en bucles `foreach`, métodos que devuelven `bool` en condiciones `if` y métodos que devuelven valores escalares en asignaciones de variables.

## Referencia rápida

```csharp
// Filter -- returns a collection for use in foreach or further chaining
Model.AllMeasures.Where(m => m.Name.EndsWith("Amount"));

// Find one -- returns a single object for assignment to a variable
var table = Model.Tables.First(t => t.Name == "Sales");
var tableOrNull = Model.Tables.FirstOrDefault(t => t.Name == "Sales");

// Existence checks -- returns bool for use in if conditions
if (table.Measures.Any(m => m.IsHidden)) { /* ... */ }
if (table.Columns.All(c => c.Description != "")) { /* ... */ }

// Count
var count = Model.AllColumns.Count(c => c.DataType == DataType.String);

// Project -- returns a List<string> of only the measure names
var names = Model.AllMeasures.Select(m => m.Name).ToList();

// Sort
var sorted = Model.AllMeasures.OrderBy(m => m.Name);

// Mutate
Model.AllMeasures.Where(m => m.FormatString == "").ForEach(m => m.FormatString = "0.00");

// Type filter
var calcCols = Model.AllColumns.OfType<CalculatedColumn>();

// Materialize before modifying the collection
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

## Filtrado con `Where`

`Where()` devuelve todos los objetos que coinciden con un predicado. Encadene varias condiciones con `&&` y `||`.

```csharp
// Columns with no description in a specific table
var undocumented = Model.Tables["Sales"].Columns
    .Where(c => string.IsNullOrEmpty(c.Description));
```

> [!WARNING]
> La búsqueda de cadenas con `Contains()` encuentra el texto en cualquier parte de la expresión, incluso dentro de literales de cadena y comentarios. Para detectar el uso real de funciones DAX, analice en su lugar la expresión tokenizada.

> [!TIP]
> Al comprobar el contenido de una expresión con `Contains()`, considere una comparación sin distinción entre mayúsculas y minúsculas: `m.Expression.Contains("calculate", StringComparison.OrdinalIgnoreCase)`.

## Búsqueda de un único objeto

`First()` devuelve la primera coincidencia o genera una excepción si no existe ninguna. `FirstOrDefault()` devuelve null en lugar de generar una excepción.

```csharp
// Throws if "Sales" does not exist
var sales = Model.Tables.First(t => t.Name == "Sales");

// Returns null if not found (safe)
var table = Model.Tables.FirstOrDefault(t => t.Name == "Sales");
if (table == null) { Error("Table not found."); return; } // return exits the script
```

## Comprobaciones de existencia y recuento

```csharp
// Are all columns documented?
var allDocs = table.Columns.All(c => !string.IsNullOrEmpty(c.Description));

// How many string columns?
var count = Model.AllColumns.Count(c => c.DataType == DataType.String);
```

## Proyección con `Select`

`Select()` transforma cada elemento. Úselo para extraer valores de propiedades o crear estructuras nuevas.

```csharp
// List of measure names only (returns List<string>)
var names = Model.AllMeasures.Select(m => m.Name).ToList();

// Table name + measure count pairs
var summary = Model.Tables.Select(t => new { t.Name, Count = t.Measures.Count() });
```

## Modificación con `ForEach`

El método de extensión `ForEach()` aplica una acción a cada elemento.

```csharp
// Set format string on all currency measures
Model.AllMeasures
    .Where(m => m.Name.EndsWith("Amount"))
    .ForEach(m => m.FormatString = "#,##0.00");

// Move all measures in a table to a display folder
Model.Tables["Sales"].Measures.ForEach(m => m.DisplayFolder = "Sales Metrics");
```

## Materializar antes de modificar una colección

Cuando modifica objetos dentro de un bucle (por ejemplo, al eliminarlos, agregarlos o moverlos), cambia la colección que se está iterando. Llama siempre a `.ToList()` o `.ToArray()` primero para crear una instantánea.

```csharp
// WRONG: modifying collection during iteration
table.Measures.Where(m => m.IsHidden).ForEach(m => m.Delete()); // throws

// CORRECT: materialize first, then modify
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

> [!WARNING]
> No materializar provoca: `"Collection was modified; enumeration operation may not complete."` Esto se aplica a cualquier modificación, no solo a la eliminación.

## Combinar colecciones

Usa `Concat()` para unir colecciones y `Distinct()` para eliminar duplicados.

```csharp
// All hidden objects (measures + columns) in a table
var hidden = table.Measures.Where(m => m.IsHidden).Cast<ITabularNamedObject>()
    .Concat(table.Columns.Where(c => c.IsHidden).Cast<ITabularNamedObject>());

// All unique tables referenced by selected measures
var tables = Selected.Measures
    .Select(m => m.Table)
    .Distinct();
```

## Equivalente en LINQ dinámico

En las expresiones de reglas de BPA, la sintaxis difiere de la de LINQ en C#. Dynamic LINQ no usa flechas lambda; utiliza operadores de palabras clave y compara las enumeraciones como cadenas.

| LINQ en C# (scripts)       | LINQ dinámico (BPA / filtro de Explorer) |
| --------------------------------------------- | ----------------------------------------------------------- |
| `m.IsHidden`                                  | `IsHidden`                                                  |
| `m.DataType == DataType.String`               | `DataType = "String"`                                       |
| `&&` / `\\|\\|` / `!`                       | `and` / `or` / `not`                                        |
| `==` / `!=`                                   | `=` / `!=` o `<>`                                           |
| `table.Columns.Count(c => c.IsHidden)`        | `Columns.Count(IsHidden)`                                   |
| `table.Medidas.Any(m => m.IsHidden)`          | `Medidas.Any(IsHidden)`                                     |
| `table.Columns.All(c => c.Description != "")` | `Columns.All(Description != "")`                            |
| `string.IsNullOrEmpty(m.Description)`         | `String.IsNullOrEmpty(Description)`                         |

> [!NOTE]
> Las expresiones de Dynamic LINQ se evalúan respecto a un único objeto del contexto. No existe ningún equivalente a `Model.AllMeasures` ni a las consultas entre tablas. Cada regla de BPA ejecuta su expresión una vez por cada objeto de su ámbito.

## Ver también

- @advanced-scripting
- @using-bpa-sample-rules-expressions
- @how-to-navigate-tom-hierarchy
- @how-to-dynamic-linq-vs-csharp-linq
