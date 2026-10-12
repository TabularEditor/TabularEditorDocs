---
uid: semantic-bridge-validate-contextual-rules
title: 创建上下文验证规则
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

# 创建上下文验证规则

本操作指南演示如何使用验证上下文创建验证规则，以检查跨多个对象的条件。这些规则仅用于演示，并不一定反映 Metric Views 或 Semantic Bridge 的硬性技术要求。

> [!NOTE]
> 这些操作指南适用于 Tabular Editor 3.26.2 及更高版本。早期版本不支持此处所示的 v1.1 Metric View 功能。

## 何时使用上下文规则

在需要执行以下操作时，请使用上下文规则：

- 检查名称是否在不同对象类型之间重复使用
- 访问先前已验证对象的信息

> [!NOTE]
> 验证过程会按顺序验证每个 Metric View 对象（先验证连接，再验证字段，最后验证度量值），因此上下文仅包含在本次验证中已访问过的项。

## MakeValidationRule 方法

泛型方法 `MakeValidationRule<T>` 可用于访问验证上下文：

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(  // or Field, Join, View
    "rule_name",
    "category",

    // return an IEnumerable<DiagnosticMessage>;
    // an empty collection means the object passed
    (obj, context) => []
);
```

`context` 参数提供以下内容：

- `context.FieldNames` - 已验证的字段名称
- `context.MeasureNames` - 已验证的度量值名称列表
- `context.JoinNames` - 已验证的连接名称
- `context.MakeError(code, message, object)` - 为给定对象创建一条错误诊断信息
- `context.MakeWarning(code, message, object)` - 为给定对象创建一条警告诊断信息

由于诊断信息是在验证函数体内创建的，你可以在信息中加入当前正在验证对象的详细信息。

## Metric View 类型的 using 指令

添加以下 using 指令以引用 Metric View 类型：

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;
```

## 规则：Metric View 度量值名称不得与 Metric View 字段名称重复

字段会先于度量值进行验证，因此在检查度量值时，`context.FieldNames` 已包含所有字段名称。

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var measureNameRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_field_name",
    "naming",
    (measure, context) =>
        context.FieldNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_field_name_collision",
                $"Measure '{measure.Name}' has the same name as a field",
                measure)]
            : []
);
```

## 规则：Metric View 度量值名称不得与 Metric View 连接名称重复

连接会最先进行验证，因此在检查度量值时，`context.JoinNames` 已包含所有连接名称。

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var measureNotJoinRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_join_name",
    "naming",
    (measure, context) =>
        context.JoinNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_join_name_collision",
                $"Measure '{measure.Name}' has the same name as a join",
                measure)]
            : []
);
```

## 为什么拆分规则更好

注意，我们创建了两条独立的规则，而不是把它们合并成一条规则。推荐这样做，原因是：

1. **更清晰的错误信息**：每条规则都会生成明确、可操作的信息
2. **更易维护**：规则可以独立新增、移除或修改
3. **逻辑更简单**：每条规则只检查一个条件
4. **更便于分类**：规则可以按用途分组和筛选

## 完整示例

此 Metric View 存在命名冲突，将同时触发这两条上下文规则：

```csharp {run id=complete setup=mv-sample after=none output=true}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// Create a Metric View with names reused across object types
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: sales.fact.orders
    joins:
      - name: customer
        source: sales.dim.customer
        on: source.customer_id = customer.customer_id
        cardinality: many_to_one
    fields:
      # 'revenue' is also used as a measure name below
      - name: revenue
        expr: source.revenue
      - name: quantity
        expr: source.quantity
    measures:
      # measureNameRule violation - same name as the 'revenue' field
      - name: revenue
        expr: SUM(source.revenue)
      # measureNotJoinRule violation - same name as the 'customer' join
      - name: customer
        expr: COUNT(DISTINCT source.customer_id)
      # this measure is fine
      - name: order_count
        expr: COUNT(source.order_id)
    """);

var measureNameRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_field_name",
    "naming",
    (measure, context) =>
        context.FieldNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_field_name_collision",
                $"Measure '{measure.Name}' has the same name as a field",
                measure)]
            : []
);

var measureNotJoinRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_join_name",
    "naming",
    (measure, context) =>
        context.JoinNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_join_name_collision",
                $"Measure '{measure.Name}' has the same name as a join",
                measure)]
            : []
);

// Run validation with both rules
var diagnostics = SemanticBridge.MetricView.Validate([
    measureNameRule,
    measureNotJoinRule
]).ToList();

// Output results
var sb = new System.Text.StringBuilder();
sb.AppendLine("CONTEXTUAL VALIDATION RESULTS");
sb.AppendLine("-----------------------------");
sb.AppendLine("");
sb.AppendLine($"Found {diagnostics.Count} issue(s):");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Message}");
}

Output(sb.ToString());
```

**输出：**

```
CONTEXTUAL VALIDATION RESULTS
-----------------------------

Found 2 issue(s):

[Error] Measure 'revenue' has the same name as a field
[Error] Measure 'customer' has the same name as a join
```

## 与默认规则组合

你可以通过调用两次 `Validate`，将上下文规则与默认验证规则一起运行：

```csharp {run id=combined setup=mv-sample after=complete output=true}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var customRules = new[] {
    SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
        "measure_not_field_name",
        "naming",
        (measure, context) =>
            context.FieldNames.Contains(measure.Name)
                ? [context.MakeError(
                    "measure_field_name_collision",
                    $"Measure '{measure.Name}' has the same name as a field",
                    measure)]
                : []),
    SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
        "measure_not_join_name",
        "naming",
        (measure, context) =>
            context.JoinNames.Contains(measure.Name)
                ? [context.MakeError(
                    "measure_join_name_collision",
                    $"Measure '{measure.Name}' has the same name as a join",
                    measure)]
                : [])
};

// Run default rules first
var defaultDiagnostics = SemanticBridge.MetricView.Validate().ToList();

// Then run custom rules
var customDiagnostics = SemanticBridge.MetricView.Validate(customRules).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Default rule issues: {defaultDiagnostics.Count}");
sb.AppendLine($"Custom rule issues: {customDiagnostics.Count}");
Output(sb.ToString());
```

**输出**

```
Default rule issues: 0
Custom rule issues: 2
```

## 另请参阅

- [Semantic Bridge 验证](xref:semantic-bridge-metric-view-validation)
