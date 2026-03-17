---
uid: semantic-bridge-validate-simple-rules
title: 创建简单验证规则
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

# 创建简单验证规则

本操作指南演示如何创建基于谓词的简单验证规则，以强制遵循命名约定并满足结构要求。
这些规则仅用于演示，并不一定反映 Metric Views 或 Semantic Bridge 的硬性技术要求。

## 四个规则帮助方法

每种 Metric View 对象类型都有一个辅助方法：

- `MakeValidationRuleForView`：用于根 View 对象的规则
- `MakeValidationRuleForJoin`：用于 Join 对象的规则
- `MakeValidationRuleForDimension`：用于 Dimension 对象的规则
- `MakeValidationRuleForMeasure`：用于度量值对象的规则

每个辅助方法都接受四个参数：

1. **name**：规则的唯一标识符
2. **category**：相关规则的分组
3. **message**：违反规则时显示的错误信息
4. **isInvalid**：如果对象无效则返回 `true` 的函数

## View 的规则

确认 Metric View 版本是否为预期值：

```csharp
var versionRule = SemanticBridge.MetricView.MakeValidationRuleForView(
    "version_check",
    "structure",
    "Metric View 版本必须为 0.1 或 1.1",
    (view) => view.Version != "0.1" && view.Version != "1.1"
);
```

## Metric View 联接规则

检查 Metric View 联接源是否使用完全限定的表名（包含点“.”）：

```csharp
var joinSourceRule = SemanticBridge.MetricView.MakeValidationRuleForJoin(
    "qualified_source",
    "structure",
    "联接源必须是完全限定的表名（例如：`catalog.schema.table`）",
    (join) => !join.Source.Contains('.')
);
```

## Metric View 维度规则

检查 Metric View 维度名称中不应包含下划线：

```csharp
var dimensionNameRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "维度名称应使用空格，而不是下划线",
    (dim) => dim.Name.Contains('_')
);
```

## Metric View 度量值规则

检查 Metric View 度量值表达式中不应包含 SELECT（以避免意外的子查询）：

```csharp
var measureExprRule = SemanticBridge.MetricView.MakeValidationRuleForMeasure(
    "no_select_subquery",
    "structure",
    "度量值表达式不应包含 SELECT 子查询",
    (measure) => measure.Expr.ToUpper().Contains("SELECT")
);
```

## 完整示例

这个 Metric View 违反了上面定义的每条规则：

```csharp
// 创建一个在每条规则上都有违规项的 Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 0.2
    source: sales.fact.orders
    joins:
      # joinSourceRule 违规 - 未完全限定
      - name: customer
        source: customer_table
        on: source.customer_id = customer.customer_id
    dimensions:
      # dimensionNameRule 违规 - 包含下划线
      - name: product_name
        expr: source.product_name
      - name: order_date
        expr: source.order_date
      # 这一项没问题
      - name: Category
        expr: source.category
    measures:
      # measureExprRule 违规 - 包含 SELECT 子查询
      - name: complex_calc
        expr: (SELECT MAX(price) FROM products)
      # 这一项没问题
      - name: total_revenue
        expr: SUM(source.revenue)
    """);

var versionRule = SemanticBridge.MetricView.MakeValidationRuleForView(
    "version_check",
    "structure",
    "Metric View 版本必须为 0.1 或 1.1",
    (view) => view.Version != "0.1" && view.Version != "1.1"
);

var joinSourceRule = SemanticBridge.MetricView.MakeValidationRuleForJoin(
    "qualified_source",
    "structure",
    "联接源必须是完全限定的表名（例如：`catalog.schema.table`）",
    (join) => !join.Source.Contains('.')
);

var dimensionNameRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "维度名称应使用空格，而不是下划线",
    (dim) => dim.Name.Contains('_')
);

var measureExprRule = SemanticBridge.MetricView.MakeValidationRuleForMeasure(
    "no_select_subquery",
    "structure",
    "度量值表达式不应包含 SELECT 子查询",
    (measure) => measure.Expr.ToUpper().Contains("SELECT")
);

// 使用自定义规则运行验证
var diagnostics = SemanticBridge.MetricView.Validate([
    versionRule,
    joinSourceRule,
    dimensionNameRule,
    measureExprRule
]).ToList();

// 输出结果
var sb = new System.Text.StringBuilder();
sb.AppendLine("自定义验证结果");
sb.AppendLine("-------------------------");
sb.AppendLine("");
sb.AppendLine($"找到 {diagnostics.Count} 个问题（项）：");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Path}: {diag.Message}");
}

Output(sb.ToString());
```

**输出：**

```
自定义验证结果
-------------------------

找到 5 个问题（项）：

[Error] MetricView: Metric View 版本必须为 0.1 或 1.1
[Error] MetricView.Joins['customer']: 联接源必须是完全限定的表名（例如：`catalog.schema.table`）
[Error] MetricView.Dimensions['product_name']: 维度名称应使用空格，而不是下划线
[Error] MetricView.Dimensions['order_date']: 维度名称应使用空格，而不是下划线
[Error] MetricView.Measures['complex_calc']: 度量值表达式不应包含 SELECT 子查询
```

## 后续步骤

- [创建上下文验证规则](xref:semantic-bridge-validate-contextual-rules)，用于重复检测等跨对象检查

## 另见

- [Semantic Bridge 验证](xref:semantic-bridge-metric-view-validation)
- [使用默认规则验证](xref:semantic-bridge-validate-default)
