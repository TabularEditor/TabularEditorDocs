---
uid: databricks-refresh-empty-catalog
title: Databricks 刷新失败：目录为空错误
author: Morten Lønskov
updated: 2026-04-16
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Databricks 刷新失败：目录为空错误

> [!NOTE]
> 从 Tabular Editor 3.26.1 开始，表导入向导默认在 Databricks 连接中使用 Implementation 2.0。 此问题只影响使用较早版本的 Tabular Editor 创建的 M 查询，或 `Databricks.Catalogs()` 的第三个参数为 `null` 的 M 查询。

刷新从 Databricks 导入数据的语义模型时，可能会遇到以下错误：

**"[Microsoft][ThriftExtension] (38) 尝试将空字符串设置为当前目录。 不允许进行此类操作。"**

当表导入向导生成的 M 查询在需要较新 Arrow Database Connectivity (ADBC) 驱动程序(也称为 Implementation 2.0)的 Databricks Workspace 中仍使用旧版连接器实现时，就会出现此错误。

---

## 了解问题

`Databricks.Catalogs()` Power Query 函数接受一个可选的第三个参数，用于控制使用哪种连接器实现。 当此参数为 `null` 时，连接器默认使用旧版实现 (1.0)。

### 为什么会这样

1. **较新的 Databricks Workspace 需要 Implementation 2.0。** 最近的 Databricks 实例对目录处理要求更严格，与旧版连接器不兼容。

2. **Tabular Editor 3.26.1 之前版本中的表导入向导会生成第三个参数为 `null` 的 M 查询。** 这意味着会使用旧版实现，而旧版实现在较新的 Databricks Workspace 中会失败。

3. **Power BI Desktop 已默认使用 Implementation 2.0。** Microsoft 已将 [Arrow Database Connectivity 驱动程序](https://learn.microsoft.com/en-us/power-query/connectors/databricks#arrow-database-connectivity-driver-connector-implementation-preview) 设为 Power BI Desktop 中新 Databricks 连接的默认选项。

---

## 解决方案

编辑每个受影响分区的 M 查询，在 `Databricks.Catalogs()` 调用中将 `[Implementation="2.0"]` 作为第三个参数。

### 修改前（旧版实现）

```powerquery
let
    Source = Databricks.Catalogs("adb-xxxx.1.azuredatabricks.net", "/sql/1.0/warehouses/xxxx", null),
    Database = Source{[Name="my_catalog",Kind="Database"]}[Data],
    Schema = Database{[Name="my_schema",Kind="Schema"]}[Data],
    Data = Schema{[Name="my_table",Kind="Table"]}[Data]
in
    Data
```

### 修改后（Implementation 2.0）

```powerquery
let
    Source = Databricks.Catalogs("adb-xxxx.1.azuredatabricks.net", "/sql/1.0/warehouses/xxxx", [Implementation="2.0"]),
    Database = Source{[Name="my_catalog",Kind="Database"]}[Data],
    Schema = Database{[Name="my_schema",Kind="Schema"]}[Data],
    Data = Schema{[Name="my_table",Kind="Table"]}[Data]
in
    Data
```

唯一的更改是将第三个参数中的 `null` 替换为 `[Implementation="2.0"]`。

### 步骤

1. 在 Tabular Editor 3 中打开模型。
2. 在 **TOM Explorer** 中，展开受影响的表并选择其分区。
3. 在 **表达式编辑器** 中，找到 `Databricks.Catalogs(...)` 调用。
4. 将 `null`（第三个参数）替换为 `[Implementation="2.0"]`。
5. 对模型中的每个 Databricks 分区重复此操作。
6. 保存模型后，再尝试刷新。

> [!TIP]
> 如果模型包含大量 Databricks 分区，可使用 **编辑 > 查找和替换** (**Ctrl+H**) 在所有表达式中批量替换 `Catalogs("adb-`。 或者，使用下面的 C# Script 一次性更新所有 Databricks 分区。

### 使用 C# Script 批量更新

下面的脚本会查找所有以 `null` 作为第三个参数调用 `Databricks.Catalogs` 的 M 分区，并将其替换为 `[Implementation="2.0"]`：

```csharp
var pattern = new System.Text.RegularExpressions.Regex(
    @"(Databricks\.Catalogs\([^,]+,\s*""[^""]*"",\s*)null(\s*\))");

var updated = 0;
foreach (var partition in Model.AllPartitions.OfType<MPartition>())
{
    if (partition.Expression == null) continue;
    var newExpr = pattern.Replace(partition.Expression, "$1[Implementation=\"2.0\"]$2");
    if (newExpr != partition.Expression)
    {
        partition.Expression = newExpr;
        updated++;
    }
}

Info($"Updated {updated} partition(s).");
```

---

## 预防措施

- **Tabular Editor 3.26.1 及更高版本：** 表导入向导默认生成使用 Implementation 2.0 的 M 查询。 升级到 3.26.1 或更高版本，以避免在新导入时出现此问题。
- **现有模型：** 升级后请检查 Databricks 分区表达式。 凡是第三个参数为 `null` 的表达式，都应更新。

---

## 其他资源

- [Arrow 数据库连接驱动程序（Microsoft 文档）](https://learn.microsoft.com/en-us/power-query/connectors/databricks#arrow-database-connectivity-driver-connector-implementation-preview)
- [连接到 Azure Databricks](xref:connecting-to-azure-databricks)
- [表导入向导](xref:importing-tables)
- [Databricks 列注释长度错误](xref:databricks-column-comments-length)
