## Carga la Metric View de ejemplo para estas muestras de código

Antes de empezar, asegúrate de tener abierto Tabular Editor 3 y de haber abierto un modelo tabular, o crea uno nuevo.

Este tutorial paso a paso utiliza una Vista de Métricas de comercio electrónico de ejemplo que representa datos de ventas, con tres tablas de dimensiones (producto, cliente y fecha) unidas a una tabla de hechos (pedidos).
Usa cualquiera de los métodos siguientes para cargarla («Descargar y cargar» o «Copiar y deserializar»),
y luego sigue con el resto de esta guía paso a paso.
Puedes ejecutar cualquiera de los dos comandos en el mismo C# Script que el resto de este ejemplo,
o puedes ejecutarlo primero en su propio C# Script y el resto del ejemplo en otro C# Script.

<noscript>
<style>
  /* Alternativa sin JS: muestra todos los paneles de pestañas apilados para que todo el contenido siga siendo accesible cuando el
     script de pestañas no se ejecuta. Con los scripts habilitados, este bloque se ignora y las pestañas funcionan con normalidad. */
  .tabGroup section[role="tabpanel"][hidden] { display: block !important; }
</style>
</noscript>

# [Descargar y cargar](#tab/load)

[Descarga `sample-metricview.yaml`](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/how-tos/includes/sample-metricview.yaml)
y cárgalo indicando la ruta:

```csharp
SemanticBridge.MetricView.Load("C:/path/to/sample-metricview.yaml");
```

# [Copiar y deserializar](#tab/deserialize)

Copia la definición siguiente y pásala a `Deserialize` como una cadena:

```csharp
SemanticBridge.MetricView.Deserialize("""
    <PLACEHOLDER: copy and paste the YAML shown below, indented within the triple quotes here>
    """);
```

[!code-yaml[Metric View de ejemplo](sample-metricview.yaml)]

***
