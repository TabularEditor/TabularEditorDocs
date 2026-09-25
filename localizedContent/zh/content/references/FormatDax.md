---
uid: formatdax
title: FormatDax 弃用说明
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---

# FormatDax 弃用说明

随着 Tabular Editor 2.13.0 的发布，`FormatDax` 方法（Tabular Editor 中可用的[辅助方法](xref:advanced-scripting#helper-methods)之一）已被弃用。

The reason for the deprecation is that the web service at https://www.daxformatter.com/ was starting to experience a heavy load of multiple request in quick succession, which were causing issues at their end. 这是因为 `FormatDax` 方法在脚本中每次被调用时都会发起一次 Web 请求，而很多人一直在使用如下这类脚本：

**不要这样做！**

```csharp
foreach(var m in Model.AllMeasures)
{
    // DON'T DO THIS
    m.Expression = FormatDax(m.Expression);
}
```

对于只有几十个度量值的小模型来说这没问题，但 www.daxformatter.com 的流量表明，上述脚本正被用于包含数千个度量值的多个模型上，甚至每天执行好几次！

为解决该问题，当使用上述语法连续调用 `FormatDax` 超过三次时，Tabular Editor 2.13.0 会显示一条警告。 In addition, subsequent calls will be throttled with a 5 second delay between each call.

## 替代写法

Tabular Editor 2.13.0 引入了两种不同的方式来调用 `FormatDax`。 The above script can be rewritten into either of the following:

```csharp
foreach(var m in Model.AllMeasures)
{
    m.FormatDax();
}
```

……或者更简单地写成……：

```csharp
Model.AllMeasures.FormatDax();
```

这两种方式都会将对 www.daxformatter.com 的所有调用合并为一次请求。 You may also use the global method syntax if you prefer:

```csharp
foreach(var m in Model.AllMeasures)
{
    FormatDax(m);
}
```

……或者更简单地写成……：

```csharp
FormatDax(Model.AllMeasures);
```

## 更多详情

从技术角度来说，`FormatDax` 现已实现为两个重载的扩展方法：

1. `void FormatDax(this IDaxDependantObject obj)`
2. `void FormatDax(this IEnumerable<IDaxDependantObject> objects, bool shortFormat = false, bool? skipSpaceAfterFunctionName = null)`

上面的重载 #1 会在脚本执行完成后，或在调用新增的 `void CallDaxFormatter()` 方法时，将所提供的对象加入格式化队列。 Overload #2 will immediately call www.daxformatter.com with a single web request that will format all DAX expressions for all the objects provided in the enumerable. You may use either of these methods as you see fit.

Note that the new method does not take any string arguments. 它会对所提供对象上的所有 DAX 属性进行格式化（例如：对于度量值，包括 Expression 和 DetailRowsExpression 属性；对于 KPI，包括 StatusExpression、TargetExpression 和 TrendExpression 等）。
