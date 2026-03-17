---
uid: semantic-bridge-validate-contextual-rules
title: 创建上下文验证规则
author: Greg Baldini
updated: 2025-01-27
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: 桌面版
          none: true
        - edition: 商业版
          none: true
        - edition: 企业版
          full: true
---

# 创建上下文验证规则

本操作指南演示如何使用验证上下文创建验证规则，以检查跨多个对象的条件。
这些规则仅用于演示，并不一定反映 Metric Views 或 Semantic Bridge 的严格技术要求。

## 何时使用上下文规则

在需要执行以下操作时，请使用上下文规则：

- 检测跨对象的重复名称
- 检查不同对象类型之间是否存在名称冲突
- 访问先前已验证对象的信息

> [!NOTE]
> 验证过程会按顺序验证每个 Metric View 对象，因此上下文只包含在本次验证过程中已访问过的项。

## MakeValidationRule 方法

泛型方法 `MakeValidationRule<T>` 可用于访问验证上下文：

```csharp
SemanticBridge.MetricView.MakeValidationRule<IMetricViewObjectType>(
    "rule_name",
    "category",
    (obj, context) => {
        // Return IEnumerable<DiagnosticMessage>
        // Empty collection means validation passed
    }
);
```

`context` 参数提供以下内容：

- `context.DimensionNames` - 已验证的维度名称列表
- `context.MeasureNames` - 已验证的度量值名称列表
- `context.JoinNames` - 已验证的连接名称
- `context.MakeError(message)` - 创建一条错误诊断信息
- `context.MakeError(message, property)` - 创建一条错误诊断信息，并明确指出发生错误的具体属性

由于诊断信息是在验证函数体内创建的，你可以在信息中加入当前正在验证对象的详细信息。

## Metric View 类型的 using 指令

添加以下 using 指令以引用 Metric View 类型：

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;
```

## 规则：Metric View 度量值名称不得与 Metric View 维度名称重复

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var measureNotDimensionRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_dimension_name",
    "naming",
    (measure, context) =>
        context.DimensionNames.Contains(measure.Name)
            ? [context.MakeError($"度量值 '{measure.Name}' 与维度同名")]
            : []
);
```

## 规则：Metric View 度量值名称不得与另一个 Metric View 度量值重复

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var noDuplicateMeasureRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "no_duplicate_measures",
    "naming",
    (measure, context) =>
        context.MeasureNames.Contains(measure.Name)
            ? [context.MakeError($"度量值 '{measure.Name}' 被定义了多次")]
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

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// 创建一个存在命名冲突的 Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: sales.fact.orders
    dimensions:
      # 'revenue' 同时被用作维度名和度量值名
      - name: revenue
        expr: source.revenue
      - name: quantity
        expr: source.quantity
      - name: order_date
        expr: source.order_date
    measures:
      # 违反 measureNotDimensionRule - 与维度同名
      - name: revenue
        expr: SUM(source.revenue)
      # 违反 noDuplicateMeasureRule - 'total_quantity' 出现两次
      - name: total_quantity
        expr: SUM(source.quantity)
      - name: total_quantity
        expr: COUNT(source.order_id)
      # 这一项是正常的
      - name: order_count
        expr: COUNT(source.order_id)
    """);

// 定义上下文规则
var measureNotDimensionRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_dimension_name",
    "naming",
    (measure, context) =>
        context.DimensionNames.Contains(measure.Name)
            ? [context.MakeError($"度量值 '{measure.Name}' 与维度同名")]
            : []
);

var noDuplicateMeasureRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "no_duplicate_measures",
    "naming",
    (measure, context) =>
        context.MeasureNames.Contains(measure.Name)
            ? [context.MakeError($"度量值 '{measure.Name}' 被定义了多次")]
            : []
);

// 运行验证
var diagnostics = SemanticBridge.MetricView.Validate([
    measureNotDimensionRule,
    noDuplicateMeasureRule
]).ToList();

// 输出结果
var sb = new System.Text.StringBuilder();
sb.AppendLine("上下文验证结果");
sb.AppendLine("-----------------------------");
sb.AppendLine("");
sb.AppendLine($"发现 {diagnostics.Count} 个问题：");
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

[Error] 度量值 'revenue' 与维度同名
[Error] 度量值 'total_quantity' 被重复定义
```

## 与默认规则组合

你可以将上下文规则与默认验证规则一起运行：

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var customRules = new[] {
    SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
        "measure_not_dimension_name",
        "naming",
        (measure, context) =>
            context.DimensionNames.Contains(measure.Name)
                ? [context.MakeError($"度量值 '{measure.Name}' 与某个维度同名")]
                : []
    )
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

## 另见

- [Semantic Bridge 验证](xref:semantic-bridge-metric-view-validation)
- [创建简单验证规则](xref:semantic-bridge-validate-simple-rules)
- [使用默认规则进行验证](xref:semantic-bridge-validate-default)
