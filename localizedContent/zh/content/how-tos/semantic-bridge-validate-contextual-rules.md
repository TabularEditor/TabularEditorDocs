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

本操作指南演示如何使用验证上下文创建验证规则，以检查跨多个对象的条件。
这些规则仅用于演示，并不一定反映 Metric Views 或 Semantic Bridge 的严格技术要求。

> [!NOTE]
> 这些操作指南适用于 Tabular Editor 3.26.2 及更高版本。
> 早期版本不支持此处所示的 v1.1 Metric View 功能。

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

SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(  // 或 Field、Join、View
    "rule_name",
    "category",

    // 返回一个 IEnumerable<DiagnosticMessage>;
    // 空集合表示该对象通过了验证
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
                $"度量值 '{measure.Name}' 与字段同名",
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
                $"度量值 '{measure.Name}' 与连接同名",
                measure)]
            : []
);
```

## 为什么拆分规则更好

注意，我们创建了两条独立的规则，而不是把它们合并成一条规则。 推荐这样做，原因是：

1. **更清晰的错误信息**：每条规则都会生成明确、可操作的信息
2. **更易维护**：规则可以独立新增、移除或修改
3. **逻辑更简单**：每条规则只检查一个条件
4. **更便于分类**：规则可以按用途分组和筛选

## 完整示例

此 Metric View 存在命名冲突，将同时触发这两条上下文规则：

```csharp {run id=complete setup=mv-sample after=none output=true}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// 创建一个在不同对象类型间复用名称的 Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: sales.fact.orders
    joins:
      - name: customer
        source: sales.dim.customer
        on: source.customer_id = customer.customer_id
        cardinality: many_to_one
    fields:
      # 'revenue' 在下方也被用作度量值名称
      - name: revenue
        expr: source.revenue
      - name: quantity
        expr: source.quantity
    measures:
      # 违反 measureNameRule - 与 'revenue' 字段同名
      - name: revenue
        expr: SUM(source.revenue)
      # 违反 measureNotJoinRule - 与 'customer' 联接同名
      - name: customer
        expr: COUNT(DISTINCT source.customer_id)
      # 这个度量值没问题
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
                $"度量值 '{measure.Name}' 与字段同名",
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
                $"度量值 '{measure.Name}' 与联接同名",
                measure)]
            : []
);

// 使用这两个规则运行验证
var diagnostics = SemanticBridge.MetricView.Validate([
    measureNameRule,
    measureNotJoinRule
]).ToList();

// 输出结果
var sb = new System.Text.StringBuilder();
sb.AppendLine("上下文验证结果");
sb.AppendLine("-----------------------------");
sb.AppendLine("");
sb.AppendLine($"发现 {diagnostics.Count} 个问题(s):");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Message}");
}

Output(sb.ToString());
```

**输出：**

```
上下文验证结果
-----------------------------

发现 2 个问题(s):

[Error] 度量值 'revenue' 与字段同名
[Error] 度量值 'customer' 与连接同名
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
                    $"度量值 '{measure.Name}' 与字段同名",
                    measure)]
                : []),
    SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
        "measure_not_join_name",
        "naming",
        (measure, context) =>
            context.JoinNames.Contains(measure.Name)
                ? [context.MakeError(
                    "measure_join_name_collision",
                    $"度量值 '{measure.Name}' 与连接同名",
                    measure)]
                : [])
};

// 先运行默认规则
var defaultDiagnostics = SemanticBridge.MetricView.Validate().ToList();

// 然后运行自定义规则
var customDiagnostics = SemanticBridge.MetricView.Validate(customRules).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"默认规则问题数：{defaultDiagnostics.Count}");
sb.AppendLine($"自定义规则问题数：{customDiagnostics.Count}");
Output(sb.ToString());
```

**输出**

```
默认规则问题数：0
自定义规则问题数：2
```

## 另见

- [Semantic Bridge 验证](xref:semantic-bridge-metric-view-validation)
