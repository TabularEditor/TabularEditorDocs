---
uid: semantic-bridge-metric-view-import-from-file
title: 从文件导入指标视图
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

# 从文件导入指标视图

本操作指南演示如何直接从 YAML 文件将指标视图导入到 Tabular 模型中。

> [!NOTE]
> 本系列操作指南适用于 Tabular Editor 3.26.2 及更高版本。
> 更早版本不支持此处展示的 v1.1 指标视图功能。

## 获取示例指标视图

将下面的示例指标视图(如下)保存到本地文件中。
你需要用此路径替换下面示例中的占位符。
就本操作而言，你只需保存文件；无需运行 `Load` 或 `Deserialize`。

[!INCLUDE [sample](includes/sample-metricview.md)]

## 从文件导入

`ImportToTabularFromFile` 会从磁盘加载 YAML，并在一步操作中将其导入到当前打开的模型中。
将下面脚本中的占位符 (`<PLACEHOLDER>`) 替换为你保存 YAML 的路径。
Databricks 主机名和 HTTP 路径用于构建 M 分区表达式；如果只是快速测试，可以先传入占位值，并在刷新数据前修正。

```csharp {compile}
var success = SemanticBridge.MetricView.ImportToTabularFromFile(
    "<PLACEHOLDER>",
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine(success ? "Import successful!" : "Import failed.");
sb.AppendLine($"Diagnostics: {diagnostics.Count}");
Output(sb.ToString());
```

## 后续步骤

- [加载并检查指标视图](xref:semantic-bridge-load-inspect)
- [导入指标视图并查看诊断信息](xref:semantic-bridge-import)

## 另见

- [Semantic Bridge 概述](xref:semantic-bridge)
