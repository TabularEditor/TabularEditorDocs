---
uid: script-format-power-query
title: Format Power Query
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  versions:
    - version: 3.x
---
# Format Power Query

## Script Purpose
If you want to format complex Power Query to make it more readable and easy to change.
<br></br>
> [!NOTE] 
> This script will send your Power Query M Code to the Power Query Formatter API. 
> Please ensure responsible use and compliance when using this script to format your Power Query code.
<br></br>

## Script

### Format Power Query
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
### Explanation
This snippet creates an HTTP POST request of the Power Query in the M Partition and sends it to the [Power Query Formatter](https://www.powerqueryformatter.com/).
Some manual formatting is done to make the code further readable. 

## Example Output

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/assets/images/Cscripts/script-format-power-query.png" alt="Format Power Query example" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> An illustration of the script formatting Power Query code.</figcaption>
</figure>