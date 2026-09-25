---
uid: script-format-power-query
title: 格式化 Power Query
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# 格式化 Power Query

## 脚本用途

如果您想对复杂的 Power Query 进行格式化，使其更易阅读、也更方便修改。 <br></br>

> [!NOTE]
> 此脚本会将您的 Power Query M 代码发送到 Power Query Formatter API。
> Please ensure responsible use and compliance when using this script to format your Power Query code. <br></br>

## 脚本

### 格式化 Power Query

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

### 说明

此代码片段会将 M 分区中的 Power Query 以 HTTP POST 请求发送到 [Power Query Formatter](https://www.powerqueryformatter.com/)。
Some manual formatting is done to make the code further readable.

## 输出示例

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-format-power-query.png" alt="Format Power Query example" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 脚本对 Power Query 代码进行格式化的示意图。</figcaption>
</figure>