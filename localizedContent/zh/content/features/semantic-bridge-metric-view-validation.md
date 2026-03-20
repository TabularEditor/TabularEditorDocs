---
uid: semantic-bridge-metric-view-validation
title: 语义桥指标视图验证
author: Greg Baldini
updated: 2025-01-23
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

# 语义桥验证

<!--
SUMMARY: Describes the validation framework for Metric Views in the Semantic Bridge, including built-in validation rules, diagnostic messages (errors/warnings/info), and how validation integrates with the import workflow.
-->

语义桥内置了一个验证框架，让你在把指标视图导入 Tabular 之前先进行验证，并定义用于检查指标视图的规则。
该验证贯穿翻译流程的每个阶段：从首次反序列化指标视图开始，到将其翻译为 DAX 和 Tabular 过程中出现的错误。

> [!NOTE]
> 语义桥目前处于 MVP 阶段，因此随着功能逐步成熟，相关界面可能会发生变化。
> 目前，验证只能通过 C# Script 来进行。

## 验证流程

验证分为多个阶段

1. 在反序列化 YAML 时，检查它是否表示一个有效的指标视图
2. 对已加载的指标视图执行验证
3. 在将指标视图翻译为 Tabular 时

第一阶段和第三阶段是自动的，并且在语义桥内部完成；第二阶段则可以让你提供自己的验证规则。

验证的过程，是将一组验证规则逐一应用到指标视图中的所有对象上并进行评估。
每条验证规则都只针对一种指标视图对象类型，例如 `Join` 或 `Measure`。
验证完成后，所有由规则违规产生的诊断信息都会返回给你，方便你进行后续处理。

## 验证规则的构成

验证规则都是 [`IMetricViewValidationRule`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.Interfaces.IMetricViewValidationRule.html) 的实例。
与其深入研究那个接口，不如通过这些辅助方法来理解和使用验证规则：

- [`MakeValidationRuleForDimension`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForDimension_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Dimension_System_Boolean__)
- [`MakeValidationRuleForJoin`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForJoin_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Join_System_Boolean__)
- [`MakeValidationRuleForMeasure`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForMeasure_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Measure_System_Boolean__)
- [`MakeValidationRuleForView`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForView_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_View_System_Boolean__)
- [`MakeValidationRule`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRule__1_System_String_System_String_System_Func___0_TabularEditor_SemanticBridge_Platforms_Databricks_Validation_IReadOnlyValidationContext_System_Collections_Generic_IEnumerable_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___)

前四个都是专用方法，用于为其名称所对应的对象类型创建规则。
它们提供了一个更简化的接口，你只需要提供：

- `name`：用于标识该规则的简短唯一名称
- `category`：用于把相似规则分组很有用，但完全是可选的
- `message`：当该规则被违反时，会在诊断信息中显示的文本
- `isInvalid`：一个函数，以 Metric View 对象作为参数；当该对象无效时返回 `true`

Name 和 Category 的设计初衷是让你更容易处理规则集合，例如在使用自定义规则的 C# Script 中。

用一个例子更容易理解：

```csharp
// 创建一个规则，用于检查维度名称中是否包含下划线
var myRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
	"no_underscores",
	"naming",
	"Do not include underscores in dimension names. Use user-friendly names with spaces.",
	(dimension) => dimension.Name.Contains('_')
	);
```

这会创建一条规则，并将其应用于所有 [Metric View `Dimension`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension.html)。
这条规则（颇具反讽意味）被命名为“no_underscores”。
它的 `category` 是“naming”，用于表明该规则与命名方式有关。
当该规则被触发时，你会在诊断信息中看到的消息是：“请勿在维度名称中使用下划线。 请使用带空格、便于阅读的名称。”
最后一个参数定义了一个函数：它会针对模型中的每个 Metric View 维度被调用；函数体是一个布尔表达式，当某个 Metric View 维度的 `Name` 属性包含下划线时返回 `true`。

下面是一段完整脚本：以内联方式定义一个 Metric View，然后对其进行反序列化并验证，展示如何使用这条规则。

```csharp
// 创建一个新的简单 Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: database.schema.table
    dimensions:
      - name: first_field
        expr: source.first_field
      - name: another field with no underscores
        expr: source.another_field_with_no_underscores
    """);

// 创建一条新的验证规则
var myRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "Do not include underscores in dimension names. Use user-friendly names with spaces.",
    (dimension) => dimension.Name.Contains('_')
    );

// 使用上面定义的规则运行验证，并输出诊断信息
Output(SemanticBridge.MetricView.Validate([myRule]));
```

你可以看到，定义为 Metric View 维度的字段中，有一个名称包含下划线。
运行脚本时，在按照我们定义的规则完成验证后，你会看到一条诊断信息。
你可以查看诊断信息中提供的详细内容：

- Code、Context：当你使用这些帮助方法之一创建规则时，不会用到这两项
- Message：你在规则中定义的信息
- Path：表示在 Metric View 中找到该对象的位置
- Severity：使用这些帮助程序时默认设置为 Error

![某个字段违反验证规则时的输出](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation.png)

如果你希望对诊断信息有更多控制，并且让验证函数更灵活，可以使用上面提到的 `MakeValidationRule` 来创建上下文验证规则。

```csharp
// 使用 Metric View 对象模型所必需
// 使用别名以避免与同名 TOM 对象冲突
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// 创建一个新的简单 Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: database.schema.table
    dimensions:
      - name: same_field
        expr: source.same_field
      - name: same_field
        expr: source.same_field
    """);

// 创建一条新的验证规则
var myRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Dimension>(
    "no_duplicate_dimensions",
    "naming",
    (dimension, context) =>
        context.DimensionNames.Contains(dimension.Name)
            ? [context.MakeError($"{dimension.Name} 作为维度出现多次")]
            : []
    );

// 使用上面定义的规则运行验证并输出诊断信息
Output(SemanticBridge.MetricView.Validate([myRule]));
```

这个帮助程序方法要求你将对象类型作为类型参数传入；同时，验证函数现在变成了一个双参数函数，签名为 `(objectType, context)`。
第一个参数是要对其评估规则的 Metric View 对象。
第二个参数是一个 [`IReadOnlyValidationContext`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.Validation.IReadOnlyValidationContext.html)。
该上下文对象包含已检查对象名称的集合；因此它很适合用来检测重复名称。
上下文对象还提供一个帮助方法，用于生成新的诊断信息；这样一来，信息无需硬编码为固定字符串，而是可以包含你正在检查的对象属性。
在这个示例中，你可以看到我们在信息中包含了重复的 Metric View 维度名称。

![某个字段违反更复杂验证规则时的输出](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation2.png)

## 验证规则最佳实践

建议创建更多简单规则，而不是更少但更复杂的规则。
验证过程非常轻量，即使规则很多，也无需担心性能问题。
例如，如果你想确保 Metric View 的维度名称不使用 `camelCased`、不使用 `kebab-cased`，也不使用 `snake_cased`，最好分别创建三条规则，而不是试图在一条规则中检查所有条件。
这样每条规则都能保持简单，信息也会更具体，因此更容易采取相应措施。

通常来说，一旦某条规则已经能捕获某个特定问题，最好就保持不动，而不是去编辑它。
如果你发现该规则遗漏了你想捕获的某个条件，只需新增一条小而简单的规则来覆盖这个新条件即可。

你可以在一个 C# Script 中保存许多不同的规则，以便在不同的 Metric View 之间复用。
因为[已加载的 Metric View 可在多个脚本中访问](xref:semantic-bridge-metric-view-object-model#loading-and-accessing-the-metric-view)，你可以保存只负责定义规则的 C# Script，然后调用 `SemanticBridge.MetricView.Validate`，从而轻松复用这些验证脚本。
请看下图：左侧的脚本“load-mv.csx”已经运行过，用于将一个 Metric View 加载到 Tabular Editor。
然后，再运行右侧的第二个脚本“run-rules.csx”来执行验证。
第二个脚本可以长期保留，供你所有的指标视图复用。

![某个字段违反更复杂验证规则时的输出](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation3.png)

为方便起见，下面把这些脚本贴出来；它们只是对上文脚本的重新排列。

**"load-mv.csx"**

```csharp
// 创建一个新的简单 Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: database.schema.table
    dimensions:
      - name: same_field
        expr: source.same_field
      - name: same_field
        expr: source.same_field
    """);
```

**"run-rules.csx"**

```csharp
// 使用 Metric View 对象模型所必需
// 通过别名避免与同名 TOM 对象冲突
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// 创建一个简单的验证规则
var simpleRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "Do not include underscores in dimension names. Use user-friendly names with spaces.",
    (dimension) => dimension.Name.Contains('_')
    );

// 创建一个上下文验证规则
var contextualRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Dimension>(
    "no_duplicate_dimensions",
    "naming",
    (dimension, context) =>
        context.DimensionNames.Contains(dimension.Name)
            ? [context.MakeError($"{dimension.Name} appears more than once as a dimension")]
            : []
    );

// 使用上面定义的规则运行验证，并输出诊断信息
Output(SemanticBridge.MetricView.Validate([simpleRule, contextualRule]));
```

## 参考资料

- @semantic-bridge-how-tos
