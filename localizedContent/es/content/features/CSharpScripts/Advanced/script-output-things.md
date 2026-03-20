---
uid: script-output-things
title: Mostrar los detalles de los objetos en una cuadrícula
author: Daniel Otykier
updated: 2024-12-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Mostrar los detalles de los objetos en una cuadrícula

## Propósito del script

Otra forma de obtener una visión general de los objetos del modelo y de cómo están configurados es volcarlos en una cuadrícula mediante la clase C# [`DataTable`](https://learn.microsoft.com/en-us/dotnet/api/system.data.datatable?view=net-8.0). Es una técnica muy flexible, porque puedes añadir solo la información que te interese como columnas del `DataTable`. Además, al pasar un `DataTable` al método `Output()`, Tabular Editor lo mostrará automáticamente en una vista de cuadrícula, lo que resulta muy cómodo para inspeccionar los datos.

## Script

### Mostrar detalles de la complejidad de las medidas

```csharp
// Este script muestra una cuadrícula con detalles sobre cada medida en el modelo.
using System.Data;

var result = new DataTable();
result.Columns.Add("Name");
result.Columns.Add("Table");
result.Columns.Add("Expression token count", typeof(int));
result.Columns.Add("Expression line count", typeof(int));
result.Columns.Add("Description line count", typeof(int));
result.Columns.Add("Format String");

foreach(var m in Model.AllMeasures)
{
    var row = new object[]
    {
        m.DaxObjectName,    // Nombre
        m.Table.Name,       // Tabla
        m.Tokenize().Count, // Recuento de tokens
        m.Expression.Split(new []{'\n'}, StringSplitOptions.RemoveEmptyEntries).Length,
        m.Description.Split(new []{'\n'}, StringSplitOptions.RemoveEmptyEntries).Length,
        m.FormatStringExpression ?? m.FormatString
    };
    result.Rows.Add(row);
}

Output(result);
```

### Explicación

En primer lugar, este fragmento configura un objeto `DataTable` con las columnas que queremos mostrar en la cuadrícula. En algunas columnas especificamos explícitamente `typeof(int)` para asegurarnos de que la ordenación funcione correctamente. A continuación, iteramos por todas las medidas del modelo y, para cada medida, creamos una nueva fila en el `DataTable` con la información deseada. Por último, pasamos el `DataTable` al método `Output()`, que mostrará la cuadrícula.

Las columnas mostradas son:

- **Name**: El nombre de la medida.
- **Table**: El nombre de la tabla a la que pertenece la medida.
- **Expression token count**: El número de tokens en la expresión de la medida. Es una medida aproximada de la complejidad de DAX.
- **Expression line count**: El número de líneas de la expresión de la medida, sin contar las líneas vacías.
- **Número de líneas de la descripción**: El número de líneas de la descripción de la medida, sin contar las líneas en blanco.
- **Cadena de formato**: La expresión de la cadena de formato de la medida, o la propia cadena de formato, si existe.

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/script-output-things-example.png" alt="Example of the dialog pop-up that displays the grid." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Ejemplo del cuadro de diálogo emergente que muestra la cuadrícula. Tanto Tabular Editor 2 como Tabular Editor 3 permiten ordenar las columnas de la cuadrícula y copiar la salida al portapapeles. Sin embargo, Tabular Editor 3 también incluye funciones adicionales para agrupar, filtrar y buscar en la cuadrícula.</figcaption>
</figure>