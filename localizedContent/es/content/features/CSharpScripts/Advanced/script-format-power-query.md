---
uid: script-format-power-query
title: Dar formato a Power Query
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Dar formato a Power Query

## Propósito del script

Si quieres dar formato a consultas complejas de Power Query para que sean más legibles y fáciles de modificar. <br></br>

> [!NOTE]
> Este script enviará tu código M de Power Query a la API de Power Query Formatter.
> Asegúrate de usar este script de forma responsable y cumpliendo la normativa al dar formato a tu código de Power Query. <br></br>

## Script

### Dar formato a Power Query

```csharp
// Este script da formato a Power Query (código M) de cualquier partición M seleccionada (no Shared Expression ni Source Expression).
// Enviará una solicitud HTTPS POST de la expresión a la API de Power Query Formatter y reemplazará el código por el resultado.
//
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

// URL de la API de powerqueryformatter.com
string powerqueryformatterAPI = "https://m-formatter.azurewebsites.net/api/v2";

// Método HttpClient para iniciar la llamada a la API mediante el método POST para la URL
HttpClient client = new HttpClient();
HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, powerqueryformatterAPI);

// Obtener la expresión M de la partición seleccionada
string partitionExpression = Selected.Partition.Expression;

// Serializar el cuerpo de la solicitud como un objeto JSON
var requestBody = JsonConvert.SerializeObject(
    new { 
        code = partitionExpression, 
        resultType = "text", 
        lineWidth = 40, 
        alignLineCommentsToPosition = true, 
        includeComments = true
    });

// Establecer el encabezado "Content-Type" de la solicitud en "application/json" y la codificación en UTF-8
var content = new StringContent(requestBody, Encoding.UTF8, "application/json");
content.Headers.ContentType = new MediaTypeHeaderValue("application/json");

// Recuperar la respuesta
var response = client.PostAsync(powerqueryformatterAPI, content).Result;

// Si la respuesta es correcta
if (response.IsSuccessStatusCode)
{
    // Obtener el resultado de la respuesta
    var result = response.Content.ReadAsStringAsync().Result;

    // Analizar el objeto JSON de respuesta desde la cadena
    JObject data = JObject.Parse(result.ToString());

    // Obtener la respuesta de Power Query con formato
    string formattedPowerQuery = (string)data["result"];

    ///////////////////////////////////////////////////////////////////////
    // FORMATEO MANUAL OPCIONAL
    // Añadir manualmente una nueva línea y un comentario a cada paso
    var replace = new Dictionary<string, string> 
    { 
        { " //", "\n\n//" }, 
        { "\n  #", "\n\n  // Paso\n  #" }, 
        { "\n  Source", "\n\n  // Fuente de datos\n  Source" }, 
        { "\n  Dataflow", "\n\n  // Información de conexión de Dataflow\n  Dataflow" }, 
        {"\n  Data =", "\n\n  // Paso\n  Data ="}, 
        {"\n  Navigation =", "\n\n  // Paso\n  Navigation ="}, 
        {"in\n\n  // Paso\n  #", "in\n  #"}, 
        {"\nin", "\n\n// Resultado\nin"} 
    };

    // Reemplazar la primera cadena del diccionario por la segunda
    var manuallyformattedPowerQuery = replace.Aggregate(
        formattedPowerQuery, 
        (before, after) => before.Replace(after.Key, after.Value));

    // Reemplazar el código autoformateado por la versión con formato manual
    formattedPowerQuery = manuallyformattedPowerQuery;
    ////////////////////////////////////////////////////////////////////////

    // Reemplazar la expresión M sin formato por la expresión con formato
    Selected.Partition.Expression = formattedPowerQuery;

    // Ventana emergente para informar de la finalización
    Info("Formateado " + Selected.Partition.Name);
}

// En caso contrario, devolver un mensaje de error
else
{
Info(
    "Llamada a la API sin éxito." +
    "\nCompruebe que está seleccionando una partición con una expresión M válida."
    );
}
```

### Explicación

Este fragmento crea una solicitud HTTP POST del código de Power Query de la partición M y la envía a [Power Query Formatter](https://www.powerqueryformatter.com/).
Se aplica algo de formato manual para que el código sea aún más legible.

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-format-power-query.png" alt="Format Power Query example" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Una ilustración de cómo el script formatea el código de Power Query.</figcaption>
</figure>