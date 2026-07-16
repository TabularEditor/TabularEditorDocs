---
uid: semantic-bridge-metric-view-validation
title: 语义桥指标视图验证
author: Greg Baldini
updated: 2026-07-01
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
此类诊断报告会在翻译管道的每个阶段提供：
从最初反序列化 Metric View，到将其翻译为 DAX 和 Tabular 过程中出现的错误。

> [!NOTE]
> Semantic Bridge 目前处于公开预览阶段，因此随着功能逐步成熟，相关接口可能会发生变化。
> 目前，验证只能通过 C# Script 来进行。

## 验证流程

验证分为多个阶段

1. 在反序列化 YAML 时，检查它是否表示一个有效的指标视图
2. 对已加载的指标视图执行验证
3. 在将指标视图翻译为 Tabular 时

第一项和第三项会自动执行，并在 Semantic Bridge 内部完成，
但第二项允许用户提供自己的验证规则。

验证是一个过程：针对 Metric View 中的所有对象，逐一评估一组验证规则。
每条验证规则都只针对一种指标视图对象类型，例如 `Join` 或 `Measure`。
验证完成后，所有由规则违规产生的诊断信息都会返回给你，方便你进行后续处理。

## 验证规则的构成

所有验证规则都是 [`IMetricViewValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.Interfaces.IMetricViewValidationRule) 的实例。
与其深入研究那个接口，不如通过这些辅助方法来理解和使用验证规则：

- [`MakeValidationRuleForField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForField%2A)
- [`MakeValidationRuleForJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForJoin%2A)
- [`MakeValidationRuleForMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForMeasure%2A)
- [`MakeValidationRuleForView`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForView%2A)
- [`MakeValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRule%2A)

前四个都是专用规则，用于为其名称所对应的对象类型创建规则。
它们提供了一个更简化的接口，你只需要提供：

- `name`：用于标识该规则的简短唯一名称
- `category`：用于把相似规则分组很有用，但完全是可选的
- `message`：当该规则被违反时，会在诊断信息中显示的文本
- `isInvalid`：一个函数，以 Metric View 对象作为参数；当该对象无效时返回 `true`

Name 和 Category 的设计初衷是让你更容易处理规则集合，例如在使用自定义规则的 C# Script 中。

这些辅助方法也都提供了一个重载版本，在最后额外接收一个 `minVersion` 参数。
该参数接受一个版本字符串，例如 "0.1" 或 "1.1"。
设置了 `minVersion` 的规则仅会对版本不低于该值的 Metric View 进行评估。

用一个例子更容易理解：

```csharp {compile}
// 创建一个规则，用于检查字段名称中是否包含下划线
var myRule = SemanticBridge.MetricView.MakeValidationRuleForField(
	"no_underscores",
	"naming",
	"Do not include underscores in field names. Use user-friendly names with spaces.",
	(field) => field.Name.Contains('_')
	);
```

这会创建一条适用于所有 [Metric View `Field`s](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field) 的规则。
这条规则（颇具反讽意味）被命名为“no_underscores”。
它的 `category` 是“naming”，用于表明该规则与命名方式有关。
违反该规则时，你会看到以下信息：“Do not include underscores in field names.”。 请使用带空格、便于阅读的名称。”
最后一个参数定义了一个函数，它会对模型中的每个 Metric View 字段调用一次；其函数体是一个布尔表达式，当某个 Metric View 字段的 `Name` 属性中包含下划线时，返回 `true`。

下面是一段完整脚本：以内联方式定义一个 Metric View，然后对其进行反序列化并验证，展示如何使用这条规则。

```csharp {run id=simple setup=none after=none output=true}
// 创建一个新的简单 Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: first_field
        expr: source.first_field
      - name: another field with no underscores
        expr: source.another_field_with_no_underscores
    """);

// 创建一条新的验证规则
var myRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Do not include underscores in field names. Use user-friendly names with spaces.",
    (field) => field.Name.Contains('_')
    );

// 使用上面定义的规则运行验证，并输出诊断信息
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.Validate([myRule]))
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

**输出**

```
[Error] no_underscores Model.Fields["first_field"]
     Do not include underscores in field names. Use user-friendly names with spaces。
```

可以看到，其中一个 Metric View 字段的名称中包含下划线。
运行脚本时，在按照我们定义的规则完成验证后，你会看到一条诊断信息。
你可以查看诊断信息中提供的详细内容：

- Code：你为规则指定的名称
- Context：这些帮助方法不会设置该值
- Message：你在规则中定义的信息
- Path：表示在 Metric View 中找到该对象的位置
- Severity：使用这些帮助程序时默认设置为 Error

![某个字段违反验证规则时的输出](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation.png)

如果你希望对诊断信息有更多控制，并且让验证函数更灵活，可以使用上面提到的 `MakeValidationRule` 来创建上下文验证规则。

```csharp {run id=contextual setup=none after=none output=true}
// 使用 Metric View 对象模型所需
// 使用别名以避免与同名 TOM 对象冲突
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// 创建一个新的简单 Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: customer
        expr: source.customer_id
      - name: repeat_customer
        expr: source.customer_id
    """);

// 创建一条新的验证规则
var myRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Field>(
    "no_aliased_fields",
    "modeling",
    (field, context) =>
    {
        var original = context.FieldNames.FirstOrDefault(seen => field.View.Fields[seen].Expr == field.Expr);
        return original == null
            ? []
            : [context.MakeError(
                "field_alias",
                $"Field '{field.Name}' reuses source expression '{field.Expr}', already used by field '{original}'.",
                field)];
    });

// 使用上面定义的规则运行验证，并输出诊断信息
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.Validate([myRule]))
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

**输出**

```
[Error] field_alias Model.Fields["repeat_customer"]
     Field 'repeat_customer' reuses source expression 'source.customer_id', already used by field 'customer'。
```

这个帮助方法要求你将对象类型作为类型参数传入，而验证函数现在是一个双参数函数，签名为 `(metricViewObject, context)`。
第一个参数是要对其评估规则的 Metric View 对象。
第二个参数是一个 [`IReadOnlyValidationContext`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.Validation.IReadOnlyValidationContext)。
该上下文对象包含若干集合，用于保存已检查对象的名称；
这意味着我们可以用它只检查那些已通过验证的对象。
上下文对象还提供了一些辅助方法，用于创建新的诊断信息；
这样一来，信息不必写成硬编码字符串，
而是可以包含你正在检查的对象的属性。
这里我们使用 `MakeError`，上下文对象中也包含 `MakeWarning`。
你可以在这个示例中看到，我们在信息中同时包含了违规字段，以及它所别名指向的字段。

![某个字段违反更复杂验证规则时的输出](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation2.png)

## 验证规则最佳实践

建议创建更多简单规则，而不是更少但更复杂的规则。
验证过程非常轻量，即使规则很多，也无需担心性能问题。
例如，如果你想确保 Metric View 字段名称不是 `camelCased`、不是 `kebab-cased`，也不是 `snake_cased`，最好分别创建三条规则，而不是试图在一条规则中同时检查这些条件。
这样每条规则都能保持简单，信息也会更具体，因此更容易采取相应措施。

一般来说，一旦某条规则能够捕获某个特定问题，最好就保持不变，而不是继续编辑它。
如果你发现该规则遗漏了你想捕获的某个条件，只需新增一条小而简单的规则来覆盖这个新条件即可。

你可以在一个 C# Script 中保存许多不同的规则，以便在不同的 Metric View 之间复用。
由于[已加载的 Metric View 可在多个脚本中访问](xref:semantic-bridge-metric-view-object-model#loading-and-accessing-the-metric-view)，你可以保存仅用于定义规则的 C# Script，然后调用 `SemanticBridge.MetricView.Validate`，从而轻松复用这些验证脚本。
请看下图：左侧的脚本“deserialize-mv.csx”已经运行，用于将一个 Metric View 加载到 Tabular Editor 中。
然后，再运行右侧的第二个脚本“run-rules.csx”来执行验证。
第二个脚本可以长期保留，供你所有的指标视图复用。

![某个字段违反更复杂验证规则时的输出](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation3.png)

为方便起见，下面把这些脚本贴出来；它们只是对上文脚本的重新排列。

**"deserialize-mv.csx"**

```csharp {run id=deserialize setup=none after=none output=false}
// 创建一个新的简单 Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: customer
        expr: source.customer_id
      - name: repeat_customer
        expr: source.customer_id
    """);
```

**"run-rules.csx"**

```csharp {run id=run-rules setup=none after=deserialize output=true}
// 使用 Metric View 对象模型所必需
// 通过别名避免与同名 TOM 对象冲突
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// 创建一个简单的验证规则
var simpleRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Do not include underscores in field names. Use user-friendly names with spaces.",
    (field) => field.Name.Contains('_')
    );

// 创建一个上下文验证规则
var contextualRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Field>(
    "no_aliased_fields",
    "modeling",
    (field, context) =>
    {
        var original = context.FieldNames.FirstOrDefault(seen => field.View.Fields[seen].Expr == field.Expr);
        return original == null
            ? []
            : [context.MakeError(
                "field_alias",
                $"Field '{field.Name}' reuses source expression '{field.Expr}', already used by field '{original}'.",
                field)];
    });

// 使用上面定义的规则运行验证，并输出诊断信息
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.Validate([simpleRule, contextualRule]))
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

**输出**

```
[Error] no_underscores Model.Fields["repeat_customer"]
     不要在字段名称中包含下划线。请使用带空格的更易读名称。

[Error] field_alias Model.Fields["repeat_customer"]
     字段 'repeat_customer' 复用了源表达式 'source.customer_id'，该表达式已被字段 'customer' 使用。
```

## 参考资料

- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-how-tos
