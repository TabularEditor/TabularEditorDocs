---
uid: semantic-bridge
title: 语义桥
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

# 语义桥

<!--
SUMMARY: Overview of the Semantic Bridge feature - a multi-platform semantic model compiler that enables translation between different semantic model platforms (e.g., Databricks Metric Views to Microsoft's Tabular model in Analysis Services and Power BI / Fabric).
-->

> [!NOTE]
> The Semantic Bridge is in public preview.
> It has limitations as documented below, and the API and feature surface area are subject to change.

Semantic Bridge 是一个语义模型编译器，能够将语义模型的结构和表达式从一个平台转换到另一个平台。
This allows you to reuse business logic on multiple data platforms, supporting end users and meeting them where they consume the data.
It also allows for migrations from one platform to another.

## 界面

### 导入 Metric View YAML

The Semantic Bridge is available through **File > Open > Import from Metric View YAML**.
This will launch a dialogue to guide you through importing a Metric View into the current Tabular model, adding tables, columns, measures, and relationships based on the structure of the Metric View.
You must have a Tabular model open in Tabular Editor.
This can be a new, empty model or an existing model you want to enhance with the objects from the Metric View.
The menu button will not be enabled until you open or create a new Tabular model.

![从文件菜单导入 Metric View：文件 > 打开 > 从 Metric View YAML 导入](~/content/assets/images/features/semantic-bridge/semantic-bridge-file-menu-import.png)

### 输入 Databricks 连接信息

你需要在此对话框中提供三项信息：

1. Metric View YAML 文件的路径。
   You can paste the path to the file or use the **Browse** button to find it.
2. The Databricks hostname.
   这是为了在为 Databricks 源系统生成的 M 分区中提供正确的参数。
3. Databricks 的 HTTP 路径。这是为了在为 Databricks 源系统生成的 M 分区中提供正确的参数。

如果你只是测试翻译功能，最后两项可以先用占位值填写，但在将数据刷新到你的 Tabular 模型之前，需要先修正 M 分区定义。

After filling out the details, click **OK**.
Semantic Bridge 会将您的 Metric View 转换为 Tabular，并为您创建所有 TOM 对象。

![导入对话框中的 Databricks 详细信息](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-details.png)

### 结果

可能有三种结果：

1. 成功：Metric View 中的所有内容都已翻译为 Tabular，你将获得一个可直接使用的 Tabular 模型。
2. 成功，但存在一些问题：Semantic Bridge 无法翻译 Metric View 中的每个对象；你可以查看诊断信息，了解哪些地方需要处理。
3. 失败：Semantic Bridge 无法翻译 Metric View

无论是哪种成功结果，你都可以像在 Tabular Editor 中一样使用撤销/重做功能，来撤销或立即重新执行导入。

**成功**

![导入成功通知](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-success.png)

**成功但存在问题**

![包含问题的导入成功通知](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-success-with-issues.png)

如果您点击 **查看诊断信息**，就会看到一份信息列表，用于描述翻译中存在的问题。
These diagnostics are available for review later by outputting them from a C# script:

```csharp {compile}
// Show all diagnostic messages from the last attempted import of a Metric View
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.ImportDiagnostics)
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

![导入诊断](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-diagnostics.png)

**失败**

![导入失败](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-failed.png)

查看失败的诊断信息与“成功但存在问题”时相同。

## 限制

### 支持的平台

在公共预览版中，我们支持将 Databricks Metric View 翻译为 Tabular 模型。

### 连接

The public preview does not connect to any platforms besides Fabric, Power BI, and Analysis Services.
Working with models from other platforms, e.g., Databricks Metric Views, is based on local source files, such as a Metric View YAML definition.

## 命名法附录

It can be confusing to discuss things when talking about the Semantic Bridge, as there are many words that have both generic and specific meanings, depending what level of abstraction we are talking about and which platform we are discussing.
For example, the term "semantic model" is both generic, referring to the concept of a collection of data and business logic in some form suitable for supporting business reporting and analytical needs, and also the name Microsoft has adopted for referring to their specific implementation of this generic concept in Power BI and Fabric.
Thus, a semantic model might generically refer to a Databricks Metric View, an OLAP / Multidimensional Cube, a Power BI semantic model, or a model hosted in another platform's semantic layer.
Because of this, we have adopted the following definitions and standards in our documentation to maintain clarity and sanity.

> [!NOTE]
> 这些约定只用于介绍 Semantic Bridge 功能的文档。

### 定义

- _Semantic model_: when used on its own always refers to the generic concept of a collection of data, metadata, and business logic to support reporting and analytics.
  If and only if it is immediately preceded by "Fabric" or "Power BI", then it is referring to that artifact type in that platform, specifically a Tabular model that is saved as TMDL or BIM and using M and DAX; we tend to prefer to use the term Tabular model to refer to the Power BI / Fabric semantic model to avoid this confusion where possible, because the Tabular model is shared across Power BI / Fabric as well as Analysis Services Tabular.
- _Platform_: a technology solution that has a semantic layer, on which a generic semantic model is hosted.
  Databricks Metric Views 是一种平台；Fabric / Power BI 是一种平台；Analysis Services Tabular 是一种平台；Analysis Services Multidimensional 也是一种平台，但 Semantic Bridge 目前不支持它。
- _Serialization format_: a way to represent a semantic model on disk in a textual format.
  TMDL 和 TMSL (.bim) 是 Power BI 语义模型的两种序列化格式；YAML 是 Databricks Metric View 的序列化格式。
- _对象模型_：语义模型在内存中的表示形式。我们通过 Semantic Bridge 在 Tabular Editor 中对它进行操作——既可以通过 GUI 操作，也可以通过 C# Script。
  The TOM or Tabular Object Model should be familiar to existing users of Tabular Editor.
  We have also created an object model for Databricks Metric Views, to allow manipulation of these in our tool.

### 通用维度建模术语

There are many terms that exist generally in discussion of a dimensional model or semantic model and also in a specific platform's object model and serialization formats.
例如，“度量值”一词从通用意义上指维度模型中被聚合的定量数值，用来表示关注的业务指标；但它在 Databricks Metric Views 和 Tabular 模型中也指一种特定对象：在 Metric View 中，度量值是一个已命名的 SQL 表达式，用于定义 Metric View 中的聚合；在 Tabular 模型中，度量值是一个已命名的 DAX 表达式，用于定义 Tabular 模型中的聚合。
It is impossible to discuss the work of the Semantic Bridge without talking about multiple meanings of such words at once.
For example, we talk about translating a Metric View measure to a Tabular measure.
As such, **we always refer to an object in a specific platform's model by saying the platform and the object, e.g., "Metric View measure" or "Tabular measure"; "Metric View field" or "TOM column".**
If the term is ever used without being accompanied by a platform's name, then we are discussing the idea generically.

## 其他资源

- [Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/)
- [Metric View YAML reference](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference)
- @semantic-bridge-metric-view-tabular-translation
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-how-tos
