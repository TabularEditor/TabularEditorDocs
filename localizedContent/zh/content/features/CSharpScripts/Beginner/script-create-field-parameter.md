---
uid: create-field-parameter
title: 创建字段参数
author: Daniel Otykier
updated: 2024-01-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 在中创建字段参数

## 脚本用途

如果你想使用 Tabular Editor 在 Power BI 模型中创建字段参数，或在 Direct Lake 模型中创建字段参数。

> [!TIP]
> 想看看脚本的实际效果？可以观看这个 [Guy in a Cube 视频](https://www.youtube.com/watch?v=Cg6zRhwF-Ro)，Patrick LeBlanc 会一步步讲解如何使用它。

## 脚本

### 选择列或度量值以创建字段参数表

```csharp
// 运行脚本前，请先选择要用作字段参数的度量值或列（按住 CTRL 可多选对象）。
// 此外，你也可以在下方修改字段参数表的名称。注意：如果用于 Power BI Desktop，
// 你必须在“文件 > 偏好”(TE2) 或“工具 > 偏好”(TE3) 下启用“不受支持的功能”。
var name = "Parameter";

if(Selected.Columns.Count == 0 && Selected.Measures.Count == 0) throw new Exception("未选择任何列或度量值！");

// 基于当前选择构建计算表格的 DAX：
var objects = Selected.Columns.Any() ? Selected.Columns.Cast<ITabularTableObject>() : Selected.Measures;
var dax = "{\n    " + string.Join(",\n    ", objects.Select((c,i) => string.Format("(\"{0}\", NAMEOF('{1}'[{0}]), {2})", c.Name, c.Table.Name, i))) + "\n}";

// 将计算表格添加到模型：
var table = Model.AddCalculatedTable(name, dax);

// 在 TE2 中，不会根据 DAX 表达式自动创建列，因此
// 需要手动添加：
var te2 = table.Columns.Count == 0;
var nameColumn = te2 ? table.AddCalculatedTableColumn(name, "[Value1]") : table.Columns["Value1"] as CalculatedTableColumn;
var fieldColumn = te2 ? table.AddCalculatedTableColumn(name + " Fields", "[Value2]") : table.Columns["Value2"] as CalculatedTableColumn;
var orderColumn = te2 ? table.AddCalculatedTableColumn(name + " Order", "[Value3]") : table.Columns["Value3"] as CalculatedTableColumn;

if(!te2) {
    // 重命名在 TE3 中自动添加的列：
    nameColumn.IsNameInferred = false;
    nameColumn.Name = name;
    fieldColumn.IsNameInferred = false;
    fieldColumn.Name = name + " Fields";
    orderColumn.IsNameInferred = false;
    orderColumn.Name = name + " Order";
}
// 设置其余属性，以便字段参数正常工作
// 参考：https://twitter.com/markbdi/status/1526558841172893696
nameColumn.SortByColumn = orderColumn;
nameColumn.GroupByColumns.Add(fieldColumn);
fieldColumn.SortByColumn = orderColumn;
fieldColumn.SetExtendedProperty("ParameterMetadata", "{\"version\":3,\"kind\":2}", ExtendedPropertyType.Json);
fieldColumn.IsHidden = true;
orderColumn.IsHidden = true;
```

### 说明

在运行脚本之前，用户需要在 TOM Explorer 中选择他们希望包含在字段参数表中的度量值或列。
随后，这些所选对象会被插入到一个计算表格中，并自动配置为字段参数表。

