---
uid: semantic-bridge-rename-objects
title: Renombrar objetos en una Metric View
author: Greg Baldini
updated: 2025-01-27
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Renombrar objetos en una Metric View

En este procedimiento se muestra cómo renombrar las dimensiones de una Metric View mediante un patrón de copia y modificación para realizar transformaciones en bloque.
Los mismos patrones se aplican a todas las colecciones de una Metric View.

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## El patrón de copia y modificación

Como los nombres de las dimensiones de una Metric View son propiedades de objetos dentro de una colección, el enfoque más limpio es:

1. Crear nuevos objetos `Dimension` de la Metric View con los nombres modificados
2. Vaciar la colección original
3. Agregar los nuevos objetos

Esto evita problemas al modificar objetos mientras se recorre la colección.

## Convertir snake_case a Title Case

Transforme los nombres de las dimensiones de una Metric View de `product_name` a `Product Name`:

```csharp
using System.Globalization;
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;
var textInfo = CultureInfo.CurrentCulture.TextInfo;

var sb = new System.Text.StringBuilder();
sb.AppendLine("BEFORE");
sb.AppendLine("------");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name}");
}

// Create renamed dimensions
var renamed = view.Dimensions.Select(dim => new MetricView.Dimension
{
    Name = textInfo.ToTitleCase(dim.Name.Replace('_', ' ')),
    Expr = dim.Expr
}).ToList();

// Replace the collection
view.Dimensions.Clear();
foreach (var dim in renamed)
{
    view.Dimensions.Add(dim);
}

sb.AppendLine();
sb.AppendLine("AFTER");
sb.AppendLine("-----");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name}");
}

Output(sb.ToString());
```

**Salida:**

```
ANTES
------
  product_name
  product_category
  customer_segment
  order_date
  order_year
  order_month

DESPUÉS
-----
  Nombre del producto
  Categoría del producto
  Segmento de cliente
  Fecha de pedido
  Año de pedido
  Mes de pedido
```

## Renombrar con un diccionario de mapeo

Aplica cambios de nombre específicos mediante una búsqueda:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// Definir asignaciones de cambio de nombre
var renames = new Dictionary<string, string>
{
    { "product_name", "Product" },
    { "product_category", "Category" },
    { "customer_segment", "Segmentos" },
    { "order_date", "Date" },
    { "order_year", "Year" },
    { "order_month", "Month" }
};

var sb = new System.Text.StringBuilder();

// Crear dimensiones renombradas
var renamed = view.Dimensions
    .Select(
        dim => new MetricView.Dimension
        {
            Name = renames.TryGetValue(dim.Name, out var newName) ? newName : dim.Name,
            Expr = dim.Expr
        })
    .ToList();

// Reemplazar la colección
view.Dimensions.Clear();
foreach (var dim in renamed)
{
    view.Dimensions.Add(dim);
}

sb.AppendLine("Dimensiones renombradas:");
sb.AppendLine("-------------------");
foreach (var dim in view.Dimensions)
{
    sb.AppendLine($"  {dim.Name,-20} <- {dim.Expr}");
}

Output(sb.ToString());
```

**Salida:**

```
Dimensiones renombradas:
-------------------
  Product              <- product.product_name
  Category             <- product.category
  Segmentos            <- customer.segment
  Date                 <- date.full_date
  Year                 <- date.year
  Month                <- date.month_name
```

## Ver también

- @semantic-bridge-add-object
- @semantic-bridge-remove-object
- @semantic-bridge-serialize
