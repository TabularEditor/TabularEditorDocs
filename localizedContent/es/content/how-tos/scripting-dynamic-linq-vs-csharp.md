---
uid: how-to-dynamic-linq-vs-csharp-linq
title: En qué se diferencia Dynamic LINQ de LINQ de C#
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# En qué se diferencia Dynamic LINQ de LINQ de C\\#

Los C# Scripts usan LINQ estándar de C# con expresiones lambda. Las reglas de Best Practice Analyzer (BPA) y los filtros del árbol del Explorador usan [Dynamic LINQ](https://dynamic-linq.net/expression-language), un lenguaje de expresiones basado en cadenas con una sintaxis diferente. Este artículo es una guía de traducción entre ambos.

## Dónde se usa cada uno

| Contexto                                                                   | Sintaxis                                                                     |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| C# Scripts y macros                                                        | LINQ de C#                                                                   |
| Expresiones de reglas de BPA                                               | Dynamic LINQ                                                                 |
| Expresiones de corrección del BPA                                          | Dynamic LINQ (con el prefijo `it.` para las asignaciones) |
| Filtro del árbol del **Explorador TOM** (prefijo `:`)\* | Dynamic LINQ                                                                 |

\* Solo en Tabular Editor 2.

## Comparación de sintaxis

En Dynamic LINQ, el objeto es implícito: no hay ningún parámetro lambda como `m.` o `c.`. En BPA, el contexto viene dado por la configuración de ámbito **Se aplica a**, que determina sobre qué tipo de objeto se evalúa la expresión.

| Concepto                           | LINQ de C# (scripts)    | Dynamic LINQ (BPA / filtro) |
| ---------------------------------- | ------------------------------------------ | ---------------------------------------------- |
| AND lógico                         | `&&`                                       | `and`                                          |
| OR lógico                          | `\|\|`                                     | `or`                                           |
| Negación lógica                    | `!`                                        | `not`                                          |
| Igual a                            | `==`                                       | `=`                                            |
| Distinto de                        | `!=`                                       | `!=` o `<>`                                    |
| Mayor/menor que                    | `>`, `<`, `>=`, `<=`                       | `>`, `<`, `>=`, `<=`                           |
| La cadena contiene                 | `m.Name.Contains("Sales")`                 | `Name.Contains("Sales")`                       |
| La cadena empieza con              | `m.Name.StartsWith("Sum")`                 | `Name.StartsWith("Sum")`                       |
| La cadena termina con              | `m.Name.EndsWith("YTD")`                   | `Name.EndsWith("YTD")`                         |
| Comprobación de valor nulo o vacío | `string.IsNullOrEmpty(m.Description)`      | `String.IsNullOrEmpty(Description)`            |
| Comprobación de espacios en blanco | `string.IsNullOrWhiteSpace(m.Description)` | `String.IsNullOrWhitespace(Description)`       |
| Coincidencia de expresión regular  | `Regex.IsMatch(m.Name, "pattern")`         | `RegEx.IsMatch(Name, "pattern")`               |

## Comparación de enumeraciones

C# usa valores de enumeración con tipo. Dynamic LINQ usa representaciones como cadenas.

| C# LINQ                                                             | Dynamic LINQ                                |
| ------------------------------------------------------------------- | ------------------------------------------- |
| `c.DataType == DataType.String`                                     | `DataType = "String"`                       |
| `p.SourceType == PartitionSourceType.M`                             | `SourceType = "M"`                          |
| `p.Mode == ModeType.DirectLake`                                     | `Mode = "DirectLake"`                       |
| `r.CrossFilteringBehavior == CrossFilteringBehavior.BothDirections` | `CrossFilteringBehavior = "BothDirections"` |

## Expresiones lambda frente al contexto implícito

LINQ de C# usa parámetros lambda explícitos. LINQ dinámico evalúa propiedades en el objeto de contexto implícito `it`.

```csharp
// C# LINQ: explicit lambda parameter
Model.AllMeasures.Where(m => m.IsHidden && m.Description == "");
```

```
// Dynamic LINQ: implicit "it" -- properties are accessed directly
IsHidden and Description = ""
```

## Navegación hacia el objeto padre

Ambos usan notación de punto, pero C# requiere el parámetro lambda.

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.Table.IsHidden);
```

```
// Dynamic LINQ
Table.IsHidden
```

## Métodos de colección

LINQ de C# usa lambdas dentro de los métodos de colección. LINQ dinámico usa un contexto implícito dentro de los métodos de colección, con `outerIt` para hacer referencia al objeto padre.

```csharp
// C# LINQ: count columns with no description
Model.Tables.Where(t => t.Columns.Count(c => c.Description == "") > 5);
```

```
// Dynamic LINQ: same logic
Columns.Count(Description = "") > 5
```

### La palabra clave `outerIt`

Dentro de un método de colección anidado en LINQ dinámico, `it` hace referencia al objeto interno (por ejemplo, una columna). Use `outerIt` para hacer referencia al objeto externo (por ejemplo, la tabla).

```
// BPA rule on Tables: find tables where any column name matches the table name
Columns.Any(Name = outerIt.Name)
```

En C#, el parámetro lambda externo `t` permanece en el ámbito durante todo el cuerpo de la lambda interna. La lambda interna `c => c.Name == t.Name` puede hacer referencia a `t` directamente porque queda capturado por la clausura.

```csharp
// C# equivalent -- t is accessible inside the inner lambda via closure
Model.Tables.Where(t => t.Columns.Any(c => c.Name == t.Name));
```

## Filtrado por tipo

C# usa `OfType<T>()` o `is`. En BPA, el ámbito **Se aplica a** de la regla se encarga del filtrado por tipo. No necesitas comprobaciones de tipo en la propia expresión.

| LINQ de C#                                     | Enfoque de LINQ dinámico                                               |
| ---------------------------------------------- | ---------------------------------------------------------------------- |
| `Model.AllColumns.OfType<CalculatedColumn>()`  | Establece el ámbito de la regla BPA en **Columnas calculadas**         |
| `Model.Tables.OfType<CalculationGroupTable>()` | Establece el ámbito de la regla BPA en **Tablas de grupos de cálculo** |

## Propiedades de dependencia

Funcionan igual en ambas sintaxis, pero LINQ dinámico omite el prefijo del objeto.

| LINQ de C#                    | LINQ dinámico               |
| ----------------------------- | --------------------------- |
| `m.ReferencedBy.Count == 0`   | `ReferencedBy.Count = 0`    |
| `m.DependsOn.Any()`           | `DependsOn.Any()`           |
| `c.UsedInRelationships.Any()` | `UsedInRelationships.Any()` |
| `c.ReferencedBy.AnyVisible`   | `ReferencedBy.AnyVisible`   |

## Métodos de anotación

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.HasAnnotation("AUTOGEN"));
```

```
// Dynamic LINQ
HasAnnotation("AUTOGEN")
```

| C# LINQ                             | LINQ dinámico                    |
| ----------------------------------- | -------------------------------- |
| `m.GetAnnotation("key") == "value"` | `GetAnnotation("key") = "value"` |
| `m.HasAnnotation("key")`            | `HasAnnotation("key")`           |

## Indexadores de perspectiva y traducción

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.InPerspective["Sales"]);
```

```
// Dynamic LINQ
InPerspective["Sales"]
```

| C# LINQ                                            | LINQ dinámico                                    |
| -------------------------------------------------- | ------------------------------------------------ |
| `m.InPerspective["Sales"]`                         | `InPerspective["Sales"]`                         |
| `!m.InPerspective["Sales"]`                        | `not InPerspective["Sales"]`                     |
| `string.IsNullOrEmpty(m.TranslatedNames["da-DK"])` | `String.IsNullOrEmpty(TranslatedNames["da-DK"])` |

## Expresiones de corrección de BPA

Las expresiones de corrección usan `it.` como destino de la asignación. `it` hace referencia al objeto concreto que incumplió la regla —el mismo objeto resaltado en la lista de resultados de BPA.

Por ejemplo, dada una regla de BPA con la expresión `IsHidden and String.IsNullOrWhitespace(Description)` aplicada a las **medidas**, cada medida que coincida aparece en los resultados de BPA. Cuando aplicas la corrección, `it` hace referencia a esa medida concreta:

```
// Set the description on the violating measure
it.Description = "TODO: Add description"

// Unhide the violating object
it.IsHidden = false
```

Aunque las expresiones de corrección no tienen un equivalente directo en LINQ de C#, puedes lograr el mismo resultado con un script:

```csharp
foreach (var m in Model.AllMeasures.Where(m => m.IsHidden && string.IsNullOrWhiteSpace(m.Description)))
{
    m.Description = "TODO: Add description";
}
```

## Ejemplo completo: la misma regla en ambas sintaxis

**Objetivo:** Buscar medidas que estén ocultas, no tengan referencias y no tengan descripción.

C# Script:

```csharp
var unused = Model.AllMeasures
    .Where(m => m.IsHidden
        && m.ReferencedBy.Count == 0
        && string.IsNullOrWhiteSpace(m.Description));

foreach (var m in unused)
    Info(m.DaxObjectFullName);
```

Expresión de la regla de BPA (se aplica a medidas):

```
IsHidden and ReferencedBy.Count = 0 and String.IsNullOrWhitespace(Description)
```

## Ver también

- @using-bpa-sample-rules-expressions
- @advanced-filtering-explorer-tree
- @bpa
- @how-to-filter-query-objects-linq
