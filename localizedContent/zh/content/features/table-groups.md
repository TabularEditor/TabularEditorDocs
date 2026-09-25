---
uid: table-groups
title: 表格组
author: Daniel Otykier
updated: 2026-06-24
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

# 表格组

Table Groups is a new feature, available in Tabular Editor 3 starting from [version 3.5.0](xref:release-3-5-0). 此功能可让你快速将表格整理到文件夹中，使你在 Tabular Editor 3 的 [TOM Explorer](xref:tom-explorer-view) 中更轻松地管理和浏览大型复杂模型。

![表格组](~/content/assets/images/user-interface/table-groups.png)

你可以通过两种方式创建表格组：在表格上右键并选择 **创建 > 表格组** 菜单选项；或者在选中一个或多个表格时，在 **属性视图** 中为表格组指定名称。

You can also use the **Move to group** right-click submenu on one or more selected tables. The submenu lists existing Table Groups, a **(New...)** entry that creates a new group from the selected tables and opens its name editor, and a **(None)** entry that removes the Table Group assignment.

你可以在 TOM Explorer 中通过拖放，将表格在不同表格组之间移动。 Note that, unlike Display Folders for measures, columns and hierarchies, Table Groups cannot be nested.

在 TOM Explorer 中右键点击某个表格组，会显示与你选中该表格组内表格(s)时相同的上下文菜单选项。

> [!NOTE]
> Table Groups is a Tabular Editor-exclusive feature. Client tools (such as Excel, Power BI Desktop, etc.) 不会识别表格组，因为用于定义 Data model 概念架构的 [CSDL 格式](https://learn.microsoft.com/en-us/ef/ef6/modeling/designer/advanced/edmx/csdl-spec) 不支持表格组。

## 元数据和脚本

Tabular Editor 会在每个表格上使用一个注释，用于指定该表格属于哪个表格组。 The name of the annotation is `TabularEditor_TableGroup`. However, when scripting changes to the model using C# scripts, you can modify the Table Group directly through the new `Table.TableGroup` (string) property.

下面是一个 C# Script 示例：它会遍历模型中的所有表格，并根据表格的类型和用途将其整理到相应的表格组中：

```csharp
// Loop through all tables:
foreach(var table in Model.Tables)
{
    if (table is CalculationGroupTable)
    {
        table.TableGroup = "Calculation Groups";
    }
    else if (!table.UsedInRelationships.Any() && table.Measures.Any(m => m.IsVisible))
    {
        // Tables containing visible measures, but no relationships to other tables
        table.TableGroup = "Measure Groups";
    }
    else if (table.UsedInRelationships.All(r => r.FromTable == table) && table.UsedInRelationships.Any())
    {
        // Tables exclusively on the "many" side of relationships:
        table.TableGroup = "Facts";
    }
    else if (!table.UsedInRelationships.Any() && table is CalculatedTable && !table.Measures.Any())
    {
        // Tables without any relationships, that are Calculated Tables and do not have measures:
        table.TableGroup = "Parameter Tables";
    }
    else if (table.UsedInRelationships.Any(r => r.ToTable == table))
    {
        // Tables on the "one" side of relationships:
        table.TableGroup = "Dimensions";
    }
    else
    {
        // All other tables:
        table.TableGroup = "Misc";
    }
}
```

## 隐藏表格组

如果你希望在 TOM Explorer 中始终看到完整的未分组表列表，但又需要与他人协作处理包含表格组注释的模型，你仍然可以在自己的 Tabular Editor 3 安装中完全禁用表格组。 This is done through the **Tools > Preferences** dialog. Navigate to the **TOM Explorer** page, then uncheck **Use table groups** under **Display and filtering**:

![表格组禁用](~/content/assets/images/table-groups-disable.png)

> [!NOTE]
> 即使你按上述方法禁用了表格组，模型中的表仍可能已分配 `TabularEditor_TableGroup` 注释。 If you wish to clear all such annotations from the model, you can use the following C# script:
>
> ```csharp
> foreach(var table in Model.Tables) table.TableGroup = null;
> ```