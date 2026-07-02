---
uid: semantic-bridge-metric-view-import-from-file
title: Import a Metric View from a File
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
# Import a Metric View from a file

This how-to demonstrates importing a Metric View into a Tabular model directly from a YAML file.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

## Get the sample Metric View

Save the sample Metric View (below) to a local file.
You will need to replace the placeholder in the example below with this path.
For this how-to, specifically, you only need to save the file; you do not need to run `Load` or `Deserialize`.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Import from file

`ImportToTabularFromFile` loads the YAML from disk and imports it into the open model in one step.
Update the placeholder in the script below (`<PLACEHOLDER>`) with the path where you saved the YAML.
The Databricks hostname and HTTP path are used to build the M partition expressions; for a quick test you can pass placeholder values and fix them before refreshing data.

```csharp
var success = SemanticBridge.MetricView.ImportToTabularFromFile(
    "<PLACEHOLDER>",
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine(success ? "Import successful!" : "Import failed.");
sb.AppendLine($"Diagnostics: {diagnostics.Count}");
Output(sb.ToString());
```

## See also

- @semantic-bridge-import
- @semantic-bridge-load-inspect
- @semantic-bridge
