---
uid: semantic-bridge-validate-simple-rules
title: 创建简单验证规则
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

# 创建简单验证规则

本操作指南演示如何创建基于谓词的简单验证规则，以强制遵循命名约定并满足结构要求。
这些规则仅用于演示，并不一定反映 Metric Views 或 Semantic Bridge 的硬性技术要求。

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

## 四个规则帮助方法

每种 Metric View 对象类型都有一个辅助方法：

- `MakeValidationRuleForView`：用于根 View 对象的规则
- `MakeValidationRuleForJoin`：用于 Join 对象的规则
- `MakeValidationRuleForField` - rules for Field objects
- `MakeValidationRuleForMeasure`：用于度量值对象的规则

每个辅助方法都接受四个参数：

1. **name**：规则的唯一标识符
2. **category**：相关规则的分组
3. **message**：违反规则时显示的错误信息
4. **isInvalid**：如果对象无效则返回 `true` 的函数

## View 的规则

确认 Metric View 版本是否为预期值：

```csharp {compile}
var versionRule = SemanticBridge.MetricView.MakeValidationRuleForView(
    "version_check",
    "structure",
    "Metric View 版本必须为 0.1 或 1.1",
    (view) => view.Version != "0.1" && view.Version != "1.1"
);
```

## Metric View 联接规则

检查 Metric View 联接源是否使用完全限定的表名（包含点“.”）：

```csharp {compile}
var joinSourceRule = SemanticBridge.MetricView.MakeValidationRuleForJoin(
    "qualified_source",
    "structure",
    "联接源必须是完全限定的表名（例如：`catalog.schema.table`）",
    (join) => !join.Source.Contains('.')
);
```

## Rule for Metric View Field

Check that Metric View field names do not contain underscores:

```csharp {compile}
var fieldNameRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Field names should use spaces, not underscores",
    (field) => field.Name.Contains('_')
);
```

## Metric View 度量值规则

检查 Metric View 度量值表达式中不应包含 SELECT（以避免意外的子查询）：

```csharp {compile}
var measureExprRule = SemanticBridge.MetricView.MakeValidationRuleForMeasure(
    "no_select_subquery",
    "structure",
    "度量值表达式不应包含 SELECT 子查询",
    (measure) => measure.Expr.ToUpper().Contains("SELECT")
);
```

## Rules for specific Metric View versions

Each helper has an overload that takes a final `minVersion` argument, a string such as "0.1" or "1.1".
Rules defined with a `minVersion` only run against Metric Views at or above that version.
This is useful for a rule that checks a property introduced in a later version,
such as `display_name` (added in v1.1):

```csharp {compile}
var displayNameRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "field_display_name_required",
    "naming",
    "Fields should have a display name set",
    (field) => string.IsNullOrEmpty(field.DisplayName),
    "1.1"
);
```

## 完整示例

这个 Metric View 违反了上面定义的每条规则：

```csharp {run id=complete setup=mv-sample after=none output=true}
// Create a Metric View with violations for each rule
SemanticBridge.MetricView.Deserialize("""
    version: 0.2
    source: sales.fact.orders
    joins:
      # joinSourceRule violation - not fully qualified
      - name: customer
        source: customer_table
        on: source.customer_id = customer.customer_id
    fields:
      # fieldNameRule violations - contains underscores
      - name: product_name
        expr: source.product_name
      - name: order_date
        expr: source.order_date
      # This one is fine
      - name: Category
        expr: source.category
    measures:
      # measureExprRule violation - contains SELECT subquery
      - name: complex_calc
        expr: (SELECT MAX(price) FROM products)
      # This one is fine
      - name: total_revenue
        expr: SUM(source.revenue)
    """);

var versionRule = SemanticBridge.MetricView.MakeValidationRuleForView(
    "version_check",
    "structure",
    "Metric View version must be 0.1 or 1.1",
    (view) => view.Version != "0.1" && view.Version != "1.1"
);

var joinSourceRule = SemanticBridge.MetricView.MakeValidationRuleForJoin(
    "qualified_source",
    "structure",
    "Join source must be a fully qualified table name (e.g., `catalog.schema.table`)",
    (join) => !join.Source.Contains('.')
);

var fieldNameRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Field names should use spaces, not underscores",
    (field) => field.Name.Contains('_')
);

var measureExprRule = SemanticBridge.MetricView.MakeValidationRuleForMeasure(
    "no_select_subquery",
    "structure",
    "Measure expressions should not contain SELECT subqueries",
    (measure) => measure.Expr.ToUpper().Contains("SELECT")
);

// Run validation with custom rules
var diagnostics = SemanticBridge.MetricView.Validate([
    versionRule,
    joinSourceRule,
    fieldNameRule,
    measureExprRule
]).ToList();

// Output results
var sb = new System.Text.StringBuilder();
sb.AppendLine("CUSTOM VALIDATION RESULTS");
sb.AppendLine("-------------------------");
sb.AppendLine("");
sb.AppendLine($"Found {diagnostics.Count} issue(s):");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Path}: {diag.Message}");
}

Output(sb.ToString());
```

**输出：**

```
CUSTOM VALIDATION RESULTS
-------------------------

Found 5 issue(s):

[Error] Model: Metric View version must be 0.1 or 1.1
[Error] Model.Joins["customer"]: Join source must be a fully qualified table name (e.g., `catalog.schema.table`)
[Error] Model.Fields["product_name"]: Field names should use spaces, not underscores
[Error] Model.Fields["order_date"]: Field names should use spaces, not underscores
[Error] Model.Measures["complex_calc"]: Measure expressions should not contain SELECT subqueries
```

## 后续步骤

- [Create contextual validation rules](xref:semantic-bridge-validate-contextual-rules)

## 另见

- [Semantic Bridge 验证](xref:semantic-bridge-metric-view-validation)
