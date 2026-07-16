## Load the sample Metric View for these code samples

Before starting, make sure you have Tabular Editor 3 open and have a Tabular model opened, or create a new model.

Este tutorial paso a paso utiliza una Vista de Métricas de comercio electrónico de ejemplo que representa datos de ventas, con tres tablas de dimensiones (producto, cliente y fecha) unidas a una tabla de hechos (pedidos).
Use either method below to load it (either "download and load" or "copy and deserialize"),
then follow along with the rest of this how-to.
You can run either command in the same C# script as the rest of this example,
or you can run it first, in its own C# script, and the rest of the example in its own C# script.

<noscript>
<style>
  /* JS-off fallback: reveal every tab panel stacked so all content stays reachable when the
     tab script does not run. With scripting on, this block is ignored and the tabs work normally. */
  .tabGroup section[role="tabpanel"][hidden] { display: block !important; }
</style>
</noscript>

# [Download and load](#tab/load)

[Download `sample-metricview.yaml`](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/how-tos/includes/sample-metricview.yaml)
and load it by path:

```csharp
SemanticBridge.MetricView.Load("C:/path/to/sample-metricview.yaml");
```

# [Copy and deserialize](#tab/deserialize)

Copy the definition below and pass it to `Deserialize` as a string:

```csharp
SemanticBridge.MetricView.Deserialize("""
    <PLACEHOLDER: copy and paste the YAML shown below, indented within the triple quotes here>
    """);
```

[!code-yaml[Sample Metric View](sample-metricview.yaml)]

***
