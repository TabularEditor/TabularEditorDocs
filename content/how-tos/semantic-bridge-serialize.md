---
uid: semantic-bridge-serialize
title: Serialize a Metric View to YAML
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
# Serialize a Metric View to YAML

This how-to demonstrates how to serialize a Metric View back to YAML format, either as a string or saved to a file.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Serialize to a string

Use `Serialize()` to get the YAML representation.
This simply re-serializes the YAML you loaded above.

```csharp
var yaml = SemanticBridge.MetricView.Serialize();

var sb = new System.Text.StringBuilder();
sb.AppendLine("YAML output:");
sb.AppendLine("------------");
sb.AppendLine(yaml);
Output(sb.ToString());
```

## Save to a file

Use `Save(path)` to write the YAML directly to disk.
This will write the metric view you loaded above to disk.

```csharp
var path = "C:/MetricViews/updated-sales-metrics.yaml";

SemanticBridge.MetricView.Save(path);

Output($"Metric View saved to: {path}");
```

## Round-trip workflow

A common workflow is to load, modify, and save a Metric View:

```csharp
var view = SemanticBridge.MetricView.Model;

// set a display name on a field, then serialize to confirm it round-trips
view.Fields["order_month"].DisplayName = "Order Month";

var yaml = SemanticBridge.MetricView.Serialize();

var sb = new System.Text.StringBuilder();
sb.AppendLine("Modified YAML:");
sb.AppendLine("--------------");
sb.AppendLine(yaml);
Output(sb.ToString());
```

**Output:**

```
<!-- TODO: capture serialized YAML from a run -->
```

## See also

- @semantic-bridge-load-inspect
- @semantic-bridge-import
- @semantic-bridge
