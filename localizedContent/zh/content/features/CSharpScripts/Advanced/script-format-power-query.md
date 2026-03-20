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
> 使用此脚本格式化 Power Query 代码时，请确保以负责任且合规的方式使用，并遵守相关要求。 <br></br>

## 脚本

### 格式化 Power Query

```csharp
// 此脚本会格式化任意所选 M 分区的 Power Query（M 代码）（不包含共享表达式或源表达式）。
// 它会将表达式通过 HTTPS POST 请求发送到 Power Query Formatter API，并用返回结果替换代码。
//
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

// powerqueryformatter.com API 的 URL
string powerqueryformatterAPI = "https://m-formatter.azurewebsites.net/api/v2";

// 使用 HttpClient 向该 URL 发起 API POST 调用
HttpClient client = new HttpClient();
HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, powerqueryformatterAPI);

// 获取所选分区的 M 表达式
string partitionExpression = Selected.Partition.Expression;

// 将请求正文序列化为 JSON 对象
var requestBody = JsonConvert.SerializeObject(
    new { 
        code = partitionExpression, 
        resultType = "text", 
        lineWidth = 40, 
        alignLineCommentsToPosition = true, 
        includeComments = true
    });

// 将请求头中的 "Content-Type" 设置为 "application/json"，编码设置为 UTF-8
var content = new StringContent(requestBody, Encoding.UTF8, "application/json");
content.Headers.ContentType = new MediaTypeHeaderValue("application/json");

// 获取响应
var response = client.PostAsync(powerqueryformatterAPI, content).Result;

// 如果响应成功
if (response.IsSuccessStatusCode)
{
    // 获取响应结果
    var result = response.Content.ReadAsStringAsync().Result;

    // 从字符串解析响应的 JSON 对象
    JObject data = JObject.Parse(result.ToString());

    // 获取格式化后的 Power Query 结果
    string formattedPowerQuery = (string)data["result"];

    ///////////////////////////////////////////////////////////////////////
    // 可选：手动格式化
    // 为每个步骤手动添加换行和注释
    var replace = new Dictionary<string, string> 
    { 
        { " //", "\n\n//" }, 
        { "\n  #", "\n\n  // 步骤\n  #" }, 
        { "\n  Source", "\n\n  // 数据源\n  Source" }, 
        { "\n  Dataflow", "\n\n  // Dataflow 连接信息\n  Dataflow" }, 
        {"\n  Data =", "\n\n  // 步骤\n  Data ="}, 
        {"\n  Navigation =", "\n\n  // 步骤\n  Navigation ="}, 
        {"in\n\n  // 步骤\n  #", "in\n  #"}, 
        {"\nin", "\n\n// 结果\nin"} 
    };

    // 用字典中的第二个字符串替换第一个字符串
    var manuallyformattedPowerQuery = replace.Aggregate(
        formattedPowerQuery, 
        (before, after) => before.Replace(after.Key, after.Value));

    // 用手动格式化版本替换自动格式化后的代码
    formattedPowerQuery = manuallyformattedPowerQuery;
    ////////////////////////////////////////////////////////////////////////

    // 用格式化后的表达式替换未格式化的 M 表达式
    Selected.Partition.Expression = formattedPowerQuery;

    // 弹窗提示完成
    Info("已格式化 " + Selected.Partition.Name);
}

// 否则返回错误信息
else
{
Info(
    "API 调用失败。" +
    "\n请确认您选择的是包含有效 M 表达式的分区。"
    );
}
```

### 说明

此代码片段会将 M 分区中的 Power Query 以 HTTP POST 请求发送到 [Power Query Formatter](https://www.powerqueryformatter.com/)。
同时还做了一些手动格式化，让代码更易读。

## 输出示例

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-format-power-query.png" alt="Format Power Query example" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 脚本对 Power Query 代码进行格式化的示意图。</figcaption>
</figure>