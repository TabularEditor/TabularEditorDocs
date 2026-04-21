---
uid: how-to-use-script-ui-helpers
title: Cómo usar los ayudantes de IU para scripts
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Cómo usar los ayudantes de IU para scripts

Tabular Editor proporciona métodos auxiliares para la interacción con el usuario en los scripts: mostrar salida, mostrar mensajes, solicitar la selección de objetos, evaluar DAX y crear cuadros de diálogo personalizados. En la interfaz de escritorio, estos métodos muestran cuadros de diálogo gráficos. En la CLI, estos métodos escriben en la consola.

## Referencia rápida

```csharp
// Messages
Info("Operation completed.");                          // informational popup
Warning("This might take a while.");                   // warning popup
Error("No valid selection."); return;                  // error popup + stop script

Output("Hello");                                       // simple dialog

// Object selection dialogs (capture returns for reuse below)
var table = SelectTable();                             // pick a table
var column = SelectColumn(table.Columns);              // pick from filtered columns
var measure = SelectMeasure();                         // pick a measure
var ds = SelectObject<DataSource>(Model.DataSources);  // generic selection
var items = SelectObjects(Model.AllMeasures);          // multi-select (TE3 only)

// Evaluate DAX
var result = EvaluateDax("COUNTROWS('Sales')");        // run DAX on connected model

// Output (uses the variables assigned above)
Output(measure);                                       // property grid for a TOM object
Output(items);                                         // list view with property grid
Output(result);                                        // sortable/filterable grid for a DataTable
```

## Mensajes: Información, Advertencia y Error

Úsalos para una comunicación sencilla. `Error()` no detiene la ejecución del script por sí solo; añade después `return` si quieres detenerla.

```csharp
if (Selected.Measures.Count() == 0)
{
    Error("Select at least one measure before running this script.");
    return;
}

// ... do work ...
Info("Updated " + Selected.Measures.Count() + " measures.");
```

## Salida

`Output()` se comporta de forma distinta según el tipo de argumento:

| Tipo de argumento                                      | Comportamiento                                       |
| ------------------------------------------------------ | ---------------------------------------------------- |
| Objeto TOM (por ejemplo, `Measure`) | Cuadrícula de propiedades para inspeccionar y editar |
| `IEnumerable<TabularNamedObject>`                      | Vista de lista con cuadrícula de propiedades         |
| `DataTable`                                            | Cuadrícula ordenable y filtrable                     |
| Cadena o tipo primitivo                                | Cuadro de diálogo sencillo de mensajes               |

> [!NOTE]
> La salida de cadenas utiliza finales de línea de Windows. Usa `\r\n` o `Environment.NewLine` para insertar saltos de línea. Un simple `\n` se renderiza en una sola línea. Esto suele confundir a los usuarios con las expresiones M, que usan `\n` y se muestran como una sola línea en `Output()`.

### DataTable para una salida estructurada

```csharp
using System.Data;

var result = new DataTable();
result.Columns.Add("Measure");
result.Columns.Add("Table");
result.Columns.Add("Token Count", typeof(int));

foreach (var m in Model.AllMeasures)
{
    result.Rows.Add(m.DaxObjectName, m.Table.Name, m.Tokenize().Count);
}

Output(result);
```

> [!TIP]
> Especifica `typeof(int)` o `typeof(double)` en las columnas numéricas para que se ordenen correctamente en la cuadrícula de salida.

## Cuadros de diálogo de selección de objetos

Los métodos auxiliares de selección muestran un cuadro de diálogo de lista y devuelven la elección del usuario. Lanzan una excepción si el usuario cancela. Envuélvelos en un bloque try/catch.

```csharp
try
{
    var table = SelectTable(Model.Tables, null, "Select a table:");
    var column = SelectColumn(
        table.Columns.Where(c => c.DataType == DataType.DateTime),
        null,
        "Select a date column:"
    );
    Info($"You selected {table.Name}.{column.Name}");
}
catch
{
    Error("Selection cancelled.");
}
```

### Selección múltiple (solo en Tabular Editor 3)

> [!NOTE]
> `SelectObjects()` solo está disponible en Tabular Editor 3. En Tabular Editor 2, usa un cuadro de diálogo de selección única en un bucle o filtra la selección antes de ejecutar el script.

`SelectObjects()` permite al usuario elegir varios objetos.

```csharp
try
{
    var measures = SelectObjects(
        Model.AllMeasures.Where(m => m.IsHidden),
        null,
        "Select measures to unhide:"
    );
    foreach (var m in measures)
        m.IsHidden = false;
}
catch
{
    Error("No selection made.");
}
```

## Evaluación de DAX

`EvaluateDax()` ejecuta una expresión DAX en modo conectado contra el modelo conectado y devuelve el resultado.

```csharp
var rowCount = Convert.ToInt64(EvaluateDax("COUNTROWS('Sales')"));
Info($"Sales table has {rowCount:N0} rows.");

// Return a table result
var result = EvaluateDax("ALL('Product'[Category])");
Output(result);
```

> [!NOTE]
> `EvaluateDax()` requiere una conexión activa a una instancia de Analysis Services o Power BI. No funciona al editar un modelo sin conexión.

## Patrones de cláusulas de guarda

Valida las condiciones previas antes de que se ejecute el script.

```csharp
// Require at least one column or measure
if (Selected.Columns.Count() == 0 && Selected.Measures.Count() == 0)
{
    Error("Select at least one column or measure.");
    return;
}

// Smart single-or-select pattern
DataSource ds;
if (Selected.DataSources.Count() == 1)
    ds = Selected.DataSource;
else
    ds = SelectObject<DataSource>(Model.DataSources, null, "Select a data source:");
```

## Cuadros de diálogo personalizados de WinForms

Para escenarios de entrada que vayan más allá de lo que ofrecen los métodos auxiliares integrados, crea cuadros de diálogo personalizados de WinForms directamente en el script. Consulta @how-to-build-custom-winforms-dialogs para ver patrones que abarcan mensajes sencillos, formularios de varios campos con validación y clases de cuadros de diálogo reutilizables.

## Ver también

- @script-helper-methods
- @script-output-things
- @how-to-build-custom-winforms-dialogs
- @csharp-scripts
- @script-implement-incremental-refresh
- @script-find-replace
- @script-convert-dlol-to-import

