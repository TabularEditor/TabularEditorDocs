---
uid: semantic-bridge-rename-objects
title: Renombrar objetos en una Metric View
author: Greg Baldini
updated: 2026-07-02
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

Esta guía práctica muestra cómo cambiar el nombre de un campo de una vista de métricas.
Los mismos patrones se aplican a todas las colecciones de una Metric View.

> [!NOTE]
> Estas guías prácticas están orientadas a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de la vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Cambiar el nombre de un campo

Cambie el nombre de un campo agregando uno nuevo con el nombre nuevo, copiando sus demás propiedades y, después, eliminando el original.
[`AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A) solo establece el nombre y la expresión, por lo que debe copiar manualmente las propiedades restantes (`Comment`, `DisplayName`, `Synonyms`, `Format`).

```csharp {run id=rename setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var old = view.Fields["order_month"];

// add the replacement, copy the remaining properties, then remove the original
var renamed = view.AddField("Order Month", old.Expr);
renamed.Comment = old.Comment;
renamed.DisplayName = old.DisplayName;
renamed.Synonyms = old.Synonyms;
renamed.Format = old.Format;
old.Delete();

var sb = new System.Text.StringBuilder();
sb.AppendLine("Fields:");
foreach (var field in view.Fields)
{
    sb.AppendLine($"  {field.Name}");
}
Output(sb.ToString());
```

**Salida:**

```
Fields:
  product_name
  product_category
  customer_segment
  order_date
  order_year
  Order Month
```

El campo que se vuelve a agregar pasa al final de la colección.

## Siguientes pasos

- [Agregar objetos a una vista de métricas](xref:semantic-bridge-add-object)
- [Eliminar objetos de una vista de métricas](xref:semantic-bridge-remove-object)
- [Serializar una vista de métricas en YAML](xref:semantic-bridge-serialize)

## Ver también

- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
