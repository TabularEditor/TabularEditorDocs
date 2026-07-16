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
> 它存在下文所述的限制，且 API 和功能范围可能会发生变化。

Semantic Bridge 是一个语义模型编译器，能够将语义模型的结构和表达式从一个平台转换到另一个平台。
这样你就能在多个数据平台上复用业务逻辑，支持终端用户，并在他们使用数据的场景中为其提供支持。
它还支持平台间迁移。

## 界面

### 导入 Metric View YAML

可通过 **文件 > 打开 > 从 Metric View YAML 导入** 使用语义桥。
这会打开一个对话框，引导你把 Metric View 导入当前 Tabular 模型，并根据 Metric View 的结构添加表、列、度量值和关系。
你必须先在 Tabular Editor 里打开一个 Tabular 模型。
这可以是一个新的空模型，也可以是你希望通过 Metric View 中的对象来增强的现有模型。
在你打开或新建 Tabular 模型之前，这个菜单按钮不会启用。

![从文件菜单导入 Metric View：文件 > 打开 > 从 Metric View YAML 导入](~/content/assets/images/features/semantic-bridge/semantic-bridge-file-menu-import.png)

### 输入 Databricks 连接信息

你需要在此对话框中提供三项信息：

1. Metric View YAML 文件的路径。
   你可以粘贴该文件的路径，或使用 **浏览** 按钮来查找。
2. Databricks 主机名。
   用于在为 Databricks 源系统生成的 M 分区中提供正确的参数。
3. Databricks 的 HTTP 路径。
   这是为了在为 Databricks 源系统生成的 M 分区中提供正确的参数。

如果你只是测试翻译功能，最后两项可以先用占位值填写，但在将数据刷新到你的 Tabular 模型之前，需要先修正 M 分区定义。

填写完详细信息后，点击 **确定**。
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
这些诊断信息也可以在之后通过 C# Script 输出出来查看：

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

在讨论 Semantic Bridge 时很容易产生困惑：许多词既有通用含义，也有特定含义，取决于我们所处的抽象层级以及正在讨论的平台。
例如，“语义模型”这个术语既可以是通用概念——指以某种形式组织的数据集合及业务逻辑，用于支撑业务报表与分析需求；也同时是 Microsoft 在 Power BI 和 Fabric 中用来指代其对该通用概念的具体实现的名称。
因此，从通用意义上说，语义模型可以泛指 Databricks Metric View、OLAP / 多维立方体 Multidimensional Cube、Power BI 语义模型，或托管在其他平台语义层中的模型。
正因如此，我们在文档中采用了以下定义和规范，以保持表述清晰并避免混淆。

> [!NOTE]
> 这些约定只用于介绍 Semantic Bridge 功能的文档。

### 定义

- _语义模型_：单独使用时，始终指通用概念——用于支撑报表与分析的数据、元数据与业务逻辑的集合。
  If and only if it is immediately preceded by "Fabric" or "Power BI", then it is referring to that artifact type in that platform, specifically a Tabular model that is saved as TMDL or BIM and using M and DAX; we tend to prefer to use the term Tabular model to refer to the Power BI / Fabric semantic model to avoid this confusion where possible, because the Tabular model is shared across Power BI / Fabric as well as Analysis Services Tabular.
- _平台_：具有语义层、并承载通用语义模型的技术解决方案。
  Databricks Metric Views 是一种平台；Fabric / Power BI 是一种平台；Analysis Services Tabular 是一种平台；Analysis Services Multidimensional 也是一种平台，但 Semantic Bridge 目前不支持它。
- _序列化格式_：一种将语义模型以文本形式表示并存储到磁盘上的方式。
  TMDL 和 TMSL (.bim) 是 Power BI 语义模型的两种序列化格式；YAML 是 Databricks Metric View 的序列化格式。
- _对象模型_：语义模型在内存中的表示形式。我们通过 Semantic Bridge 在 Tabular Editor 中对它进行操作——既可以通过 GUI 操作，也可以通过 C# Script。
  TOM 或 Tabular Object Model 对现有 Tabular Editor 用户来说应该并不陌生。
  我们还为 Databricks Metric Views 创建了一个对象模型，以便在我们的工具中操作它们。

### 通用维度建模术语

在讨论维度模型或语义模型时，有许多术语既是通用概念，同时也出现在特定平台的对象模型与序列化格式中。
例如，“度量值”一词从通用意义上指维度模型中被聚合的定量数值，用来表示关注的业务指标；但它在 Databricks Metric Views 和 Tabular 模型中也指一种特定对象：在 Metric View 中，度量值是一个已命名的 SQL 表达式，用于定义 Metric View 中的聚合；在 Tabular 模型中，度量值是一个已命名的 DAX 表达式，用于定义 Tabular 模型中的聚合。
如果不同时谈这些词的多重含义，就无法讨论 Semantic Bridge 的工作。
例如，我们会谈到将 Metric View 度量值翻译为 Tabular 度量值。
As such, **we always refer to an object in a specific platform's model by saying the platform and the object, e.g., "Metric View measure" or "Tabular measure"; "Metric View field" or "TOM column".**
If the term is ever used without being accompanied by a platform's name, then we are discussing the idea generically.

## 更多资源

- [Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/)
- [Metric View YAML reference](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference)
- @semantic-bridge-metric-view-tabular-translation
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-how-tos
