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

## Objetivo del script

Si quieres dar formato a consultas complejas de Power Query para que sean más legibles y fáciles de modificar. <br></br>

> [!NOTE]
> Este script enviará tu código M de Power Query a la API de Power Query Formatter.
> Asegúrate de usar este script de forma responsable y cumpliendo la normativa al dar formato a tu código de Power Query. <br></br>

## Script

### Dar formato a Power Query

```csharp
// This script formats the Power Query (M Code) of any selected M Partition (not Shared Expression or Source Expression).
// It will send an HTTPS POST request of the expression to the Power Query Formatter API and replace the code with the result.
//
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

// URL of the powerqueryformatter.com API
string powerqueryformatterAPI = "https://m-formatter.azurewebsites.net/api/v2";

// HttpClient method to initiate the API call POST method for the URL
HttpClient client = new HttpClient();
HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, powerqueryformatterAPI);

// Get the M Expression of the selected partition
string partitionExpression = Selected.Partition.Expression;

// Serialize the request body as a JSON object
var requestBody = JsonConvert.SerializeObject(
    new { 
        code = partitionExpression, 
        resultType = "text", 
        lineWidth = 40, 
        alignLineCommentsToPosition = true, 
        includeComments = true
    });

// Set the "Content-Type" header of the request to "application/json" and the encoding to UTF-8
var content = new StringContent(requestBody, Encoding.UTF8, "application/json");
content.Headers.ContentType = new MediaTypeHeaderValue("application/json");

// Retrieve the response
var response = client.PostAsync(powerqueryformatterAPI, content).Result;

// If the response is successful
if (response.IsSuccessStatusCode)
{
    // Get the result of the response
    var result = response.Content.ReadAsStringAsync().Result;

    // Parse the response JSON object from the string
    JObject data = JObject.Parse(result.ToString());

    // Get the formatted Power Query response
    string formattedPowerQuery = (string)data["result"];

    ///////////////////////////////////////////////////////////////////////
    // OPTIONAL MANUAL FORMATTING
    // Manually add a new line and comment to each step
    var replace = new Dictionary<string, string> 
    { 
        { " //", "\n\n//" }, 
        { "\n  #", "\n\n  // Step\n  #" }, 
        { "\n  Source", "\n\n  // Data Source\n  Source" }, 
        { "\n  Dataflow", "\n\n  // Dataflow Connection Info\n  Dataflow" }, 
        {"\n  Data =", "\n\n  // Step\n  Data ="}, 
        {"\n  Navigation =", "\n\n  // Step\n  Navigation ="}, 
        {"in\n\n  // Step\n  #", "in\n  #"}, 
        {"\nin", "\n\n// Result\nin"} 
    };

    // Replace the first string in the dictionary with the second
    var manuallyformattedPowerQuery = replace.Aggregate(
        formattedPowerQuery, 
        (before, after) => before.Replace(after.Key, after.Value));

    // Replace the auto-formatted code with the manually formatted version
    formattedPowerQuery = manuallyformattedPowerQuery;
    ////////////////////////////////////////////////////////////////////////

    // Replace the unformatted M expression with the formatted expression
    Selected.Partition.Expression = formattedPowerQuery;

    // Pop-up to inform of completion
    Info("Formatted " + Selected.Partition.Name);
}

// Otherwise return an error message
else
{
Info(
    "API call unsuccessful." +
    "\nCheck that you are selecting a partition with a valid M Expression."
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