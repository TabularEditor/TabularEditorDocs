---
uid: semantic-bridge
title: 语义桥
author: Greg Baldini
updated: 2026-04-17
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
> 在 3.25.0 版本中发布的 Semantic Bridge 目前处于公共预览阶段。 它存在下文所述的限制，且 API 和功能范围可能会发生变化。 它存在下文所述的限制，且 API 和功能范围可能会发生变化。

The Semantic Bridge is a semantic model compiler, with the capability to translate the structure and expressions of a semantic model from one platform to another.
这样你就能在多个数据平台上复用业务逻辑，支持终端用户，并在他们使用数据的场景中为其提供支持。
它还支持平台间迁移。

<a name="interface"></a>

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

1. The path to the Metric View YAML file.
   你可以粘贴该文件的路径，或使用 **浏览** 按钮来查找。
2. Databricks 主机名。
   用于在为 Databricks 源系统生成的 M 分区中提供正确的参数。
3. The HTTP path for Databricks.
   This is to provide the correct argument in the M partition generated for the Databricks source system.

如果你只是测试翻译功能，最后两项可以先用占位值填写，但在将数据刷新到你的 Tabular 模型之前，需要先修正 M 分区定义。

填写完详细信息后，点击 **确定**。
The Semantic Bridge will translate your Metric View to Tabular and create all the TOM objects for you.

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

If you click on **View Diagnostics**, you can see a list of messages describing the issues in translation.
这些诊断信息也可以在之后通过 C# Script 输出出来查看：

```csharp
// 显示上一次尝试导入 Metric View 时的所有诊断信息
SemanticBridge.MetricView.ImportDiagnostics.Output();
```

![导入诊断](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-diagnostics.png)

**失败**

![导入失败](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-failed.png)

查看失败的诊断信息与“成功但存在问题”时相同。

## 翻译过程

将 Metric View 翻译为 Tabular 模型分为几个步骤：

1. 从磁盘读取 YAML 文件
2. 对 YAML 进行反序列化
3. 验证反序列化后的 YAML 是否为有效的 Metric View
4. If it is a valid Metric View, store it as a the currently loaded Metric View, similar to how there is a loaded Tabular model that you interact with.
   如果它不是有效的 Metric View，流程将在此停止，并会提供信息。
5. 分析 Metric View，并尝试将其转换为一种中间表示
6. 尝试将中间表示转换为 Tabular 模型

The import GUI described above handles all of this for you, but you can also use C# scripts to customize different steps of the process and operate on the Metric View programatically, similarly to how you are used to doing with a Tabular model.
具体来说，你可以

- 使用 [`SemanticBridge.MetricView.Load`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Load_System_String_) 从磁盘加载 Metric View：加载后可在 C# Script 中通过 [`SemanticBridge.MetricView.Model`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Model) 访问，但不会将结构导入 Tabular 模型
- 使用 [`SemanticBridge.MetricView.Deserialize`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Deserialize_System_String_) 从字符串反序列化 Metric View：与加载类似，模型可通过 [`SemanticBridge.MetricView.Model`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Model) 访问，但不会导入到 Tabular 模型中
- 使用 [`SemanticBridge.MetricView.Save`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Save_System_String_) 将 Metric View 保存到磁盘
- 使用 [`SemanticBridge.MetricView.Serialize`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Serialize) 将 Metric View 序列化为字符串。
- 使用与 [Best Practice Analyzer](xref:best-practice-analyzer) 类似的系统，通过 [`SemanticBridge.MetricView.Validate`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Validate) 验证 Metric View
  - 你可以使用 [`SemanticBridge.MetricView.MakeValidationRule`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRule__1_System_String_System_String_System_Func___0_TabularEditor_SemanticBridge_Platforms_Databricks_Validation_IReadOnlyValidationContext_System_Collections_Generic_IEnumerable_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___) 及其更简化的版本创建自定义验证规则
- 使用 [`SemanticBridge.MetricView.ImportToTabularFromFile`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_ImportToTabularFromFile_System_String_TabularEditor_TOMWrapper_Model_System_String_System_String_System_Collections_Generic_List_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___System_Boolean_) 将 Metric View 导入到 Tabular，其作用与上方所示 GUI 完全相同；或使用 [`SemanticBridge.MetricView.ImportToTabular`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_ImportToTabular_TabularEditor_TOMWrapper_Model_System_String_System_String_System_Collections_Generic_List_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___System_Boolean_)，功能类似，但它操作的是当前已加载的 Metric View，而不是从磁盘读取。

<a name="public-preview-limitations"></a>

## 公开预览限制

### 支持的平台

在公共预览版中，我们支持将 Databricks Metric View 翻译为 Tabular 模型。
具体来说，我们支持 Databricks Metric View 的以下内容：
具体来说，我们支持 Databricks Metric View 的以下内容：

- v0.1 Metric View 属性：
  - 支持：
    - `source`：事实表的来源
    - `joins`：左连接到事实表的表集合
    - `dimensions`：来自任意表的平铺字段集合，可来自单个事实表，也可来自多个连接表
    - `measures`: 表示业务逻辑的已命名聚合，即度量值的扁平集合
  - 不支持：
    - `filter`：用于 Metric View 的 SQL 筛选表达式

公开预览版不支持任何 v1.1 元数据。
Any v1.1 metadata is silently ignored upon deserialization of a Metric View, so it will not be visible in a C# script and it will not affect the translation to Tabular in any way.

> [!WARNING]
> Because the v1.1 metadata is silently ignored, a Metric View that you deserialize and then serialize will be missing this metadata.
> 注意不要在 C# Script 中覆盖 v1.1 源 YAML 文件，否则会移除所有 v1.1 元数据。

### 从 SQL 翻译的限制

Metric View 在 SQL 表达式之上提供了一个结构化层，因此翻译 Metric View 的一部分工作是在 Tabular 模型中将 SQL 转换为 DAX 和 M。

- Metric View `joins` with nested `joins` are not supported.
  换句话说，翻译仅支持严格的星型架构；不支持雪花模型
- 不支持使用 `using` 作为联接条件的 Metric View `joins`；仅支持通过 `on` 属性在单个键字段上进行等值联接。
- 包含 SQL 表达式的 Metric View `dimensions` 不会翻译为 M 或 DAX；它们会以 Tabular 模型计算列的形式呈现，并将其 SQL 表达式注释掉
- 包含非基础聚合的 Metric View `measures` 不会翻译为 DAX；它们会以 Tabular 模型度量值的形式呈现，并将其 SQL 表达式注释掉
  - 仅支持 sum、max、min、average、count 和 distinct count 这些聚合。
  - 基础聚合中的 SQL 注释不会在 DAX 中保留

> [!WARNING]
> 注意，SQL 和 DAX 是不同的语言，语义也不同。
> We can make no guarantee that a translated measure will behave identically between the Metric View SQL and the Tabular DAX we generate.
> 定义在事实表字段上的基础聚合通常表现一致；而定义在维度表字段上的聚合更可能产生非预期结果。

### 连接

公共预览版不会连接除 Tabular 之外的任何平台，而是完全基于本地文件运行。
你必须自行创建 Metric View YAML，然后将其放到 Tabular Editor 能够访问的位置。
你必须自行创建 Metric View YAML，然后将其放到 Tabular Editor 能够访问的位置。

### C# API

The C# interface has been built to optimize for the automatic translation workflow.
因此，与当前加载的 Metric View 交互的支持较为有限，某些类型的操作也比较繁琐。

## 命名法附录

在讨论 Semantic Bridge 时很容易产生困惑：许多词既有通用含义，也有特定含义，取决于我们所处的抽象层级以及正在讨论的平台。
例如，“语义模型”这个术语既可以是通用概念——指以某种形式组织的数据集合及业务逻辑，用于支撑业务报表与分析需求；也同时是 Microsoft 在 Power BI 和 Fabric 中用来指代其对该通用概念的具体实现的名称。
因此，从通用意义上说，语义模型可以泛指 Databricks Metric View、OLAP / 多维立方体 Multidimensional Cube、Power BI 语义模型，或托管在其他平台语义层中的模型。
同样，“维度”既是维度建模中的一个概念，也是在 Metric View 中一种特定对象类型的名称。
正因如此，我们在文档中采用了以下定义和规范，以保持表述清晰并避免混淆。

> [!NOTE]
> 这些约定只用于介绍 Semantic Bridge 功能的文档。

### 定义

- _语义模型_：单独使用时，始终指通用概念——用于支撑报表与分析的数据、元数据与业务逻辑的集合。
  If and only if it is immediately preceded by "Fabric" or "Power BI", then it is referring to that artifact type in that platform, specifically a Tabular model that is saved as TMDL or BIM and using M and DAX; we tend to prefer to use the term Tabular model to refer to the Power BI / Fabric semantic model to avoid this confusion where possible, because the Tabular model is shared across Power BI / Fabric as well as Analysis Serviced Tabular.
- _平台_：具有语义层、并承载通用语义模型的技术解决方案。
  Databricks Metric Views represent a platform; Fabric / Power BI represent a platform; Analysis Services Tabular is a platform; Analysis Services Multidimensional is a platform which we have no support for in the Semantic Bridge today.
- _序列化格式_：一种将语义模型以文本形式表示并存储到磁盘上的方式。
  TMDL and TMSL (.bim) are two serialization formats for a Power BI semantic model; YAML is the serialization format for a Databricks Metric View.
- _对象模型_：语义模型在内存中的表示形式。我们通过 Semantic Bridge 在 Tabular Editor 中对它进行操作——既可以通过 GUI 操作，也可以通过 C# Script。
  TOM 或 Tabular Object Model 对现有 Tabular Editor 用户来说应该并不陌生。
  我们还为 Databricks Metric Views 创建了一个对象模型，以便在我们的工具中操作它们。

### 通用维度建模术语

在讨论维度模型或语义模型时，有许多术语既是通用概念，同时也出现在特定平台的对象模型与序列化格式中。
例如，“度量值”一词从通用意义上指维度模型中被聚合的定量数值，用来表示关注的业务指标；但它在 Databricks Metric Views 和 Tabular 模型中也指一种特定对象：在 Metric View 中，度量值是一个已命名的 SQL 表达式，用于定义 Metric View 中的聚合；在 Tabular 模型中，度量值是一个已命名的 DAX 表达式，用于定义 Tabular 模型中的聚合。
如果不同时谈这些词的多重含义，就无法讨论 Semantic Bridge 的工作。
例如，我们会谈到将 Metric View 度量值翻译为 Tabular 度量值。
因此，**我们在引用某个平台模型中的对象时，始终使用“平台 + 对象”的说法，例如 “Metric View 度量值” 或 “Tabular 度量值”**。
如果某个术语在使用时没有搭配平台名称，那么我们讨论的就是它的通用概念。

### Metric Views 与 Tabular 模型中的常见通用术语

对于可能不熟悉 Metric Views 或 Tabular 模型的用户，我们在下方提供了一份不完整的术语对照表。
We refer to the names of Metric View objects based on their representation in YAML, and Tabular based on the name of the type of object in TMDL/TMSL.

| 通用术语  | Tabular 中的名称 | Metric View 中的名称                                     | 描述                             | 备注                                                                                                                                                                 |
| ----- | ------------ | ---------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 事实表   | 表            | `source`                                             | 用于存放维度外键以及可聚合的数值字段的表           | a Metric View has a single fact which is unnamed and captured as the root-level `source` attribute in YAML. Tabular 模型不会区分表的类型：某个表是否为事实表只能通过推断才能确定 |
| 维度    | 表            | `join`                                               | 用于存放描述性属性以及一个主键的表，事实表通过该主键与其关联 | Tabular 模型同样不会区分，因此“维度”的角色也只能像事实表一样通过推断得出。                                                                                                                         |
| 分区    | 分区           | `source`（仅用于 `join`）                                 | 用于数据管理的对象，保存表中的一部分数据           | Tabular 模型中的表可以有多个分区，并且至少要有一个分区。 如上所述，Metric View 的事实表完全以 `source` 的形式定义；但 Metric View 的 `join` 也有一个 `source` 属性，其作用大致类似于分区                                        |
| 字段    | 列            | 维度                                                   | 表格中的一列                         |                                                                                                                                                                    |
| 度量值   | 度量值          | 度量值                                                  | 在模型中按业务逻辑进行汇总的定量值              | 表格模型中的度量值使用 DAX 编写，而在 Metric View 中使用 SQL 编写                                                                                                                       |
| 联接或关系 | 关系           | join.on 或 join.using | 一个表中的外键与另一个表中的主键之间的对应关系        | 在表格模型中，关系是显式对象；而在 Metric View YAML 中，它被隐式定义为 `join` 对象的一个属性                                                                                                        |

## 更多资源

- [Databricks Metric View 文档](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)
- [Databricks Metric View YAML 参考](https://learn.microsoft.com/en-us/azure/databricks/metric-views/data-modeling/syntax)
- @semantic-bridge-how-tos
