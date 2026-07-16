## 为这些代码示例加载示例 Metric View

开始前，请确保你已打开 Tabular Editor 3，并已打开一个表格模型；如果没有，也可以新建一个模型。

本操作指南使用一个示例电商 Metric View 来展示销售数据：三张维度表（产品、客户、日期）与一张事实表（订单）进行联接。
使用下面任一方法来加载它（“下载并加载”或“复制并反序列化”），然后继续阅读本操作指南的其余内容。
你可以在与本示例其余部分相同的 C# Script 中运行任一命令；也可以先在单独的 C# Script 中运行该命令，再在另一个 C# Script 中运行本示例的其余部分。

<noscript>
<style>
  /* JS 关闭时的回退方案：将所有选项卡面板依次堆叠显示，以便在
     选项卡脚本未运行时，仍可访问所有内容。 启用脚本时，将忽略此块，标签页会正常工作。 */
  .tabGroup section[role="tabpanel"][hidden] { display: block !important; }
</style>
</noscript>

# [下载并加载](#tab/load)

[下载 `sample-metricview.yaml`](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/how-tos/includes/sample-metricview.yaml)
然后按路径加载：

```csharp
SemanticBridge.MetricView.Load("C:/path/to/sample-metricview.yaml");
```

# [复制并反序列化](#tab/deserialize)

复制下面的定义，并将其作为字符串传递给 `Deserialize`：

```csharp
SemanticBridge.MetricView.Deserialize("""
    <PLACEHOLDER: copy and paste the YAML shown below, indented within the triple quotes here>
    """);
```

[!code-yaml[示例 Metric View](sample-metricview.yaml)]

***
