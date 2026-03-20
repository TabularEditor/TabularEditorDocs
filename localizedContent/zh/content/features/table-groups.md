---
uid: table-groups
title: 表格组
author: Daniel Otykier
updated: 2023-03-08
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# 表格组

表格组是一项新功能，从 [3.5.0 版本](xref:release-3-5-0) 起可在 Tabular Editor 3 中使用。 此功能可让你快速将表格整理到文件夹中，使你在 Tabular Editor 3 的 [TOM Explorer](xref:tom-explorer-view) 中更轻松地管理和浏览大型复杂模型。

![表格组](~/content/assets/images/user-interface/table-groups.png)

你可以通过两种方式创建表格组：在表格上右键并选择 **创建 > 表格组** 菜单选项；或者在选中一个或多个表格时，在 **属性视图** 中为表格组指定名称。

你可以在 TOM Explorer 中通过拖放，将表格在不同表格组之间移动。 注意：与度量值、列和层次结构的显示文件夹不同，表格组不能嵌套。

在 TOM Explorer 中右键点击某个表格组，会显示与你选中该表格组内表格(s)时相同的上下文菜单选项。

> [!NOTE]
> 表格组是 Tabular Editor 的专有功能。 客户端工具（如 Excel、Power BI Desktop 等） 不会识别表格组，因为用于定义 Data model 概念架构的 [CSDL 格式](https://learn.microsoft.com/en-us/ef/ef6/modeling/designer/advanced/edmx/csdl-spec) 不支持表格组。

## 元数据和脚本

Tabular Editor 会在每个表格上使用一个注释，用于指定该表格属于哪个表格组。 该注释的名称为 `TabularEditor_TableGroup`。 不过，当你使用 C# Script 对模型进行更改时，可以通过新的 `Table.TableGroup`（string）属性直接修改表格组。

下面是一个 C# Script 示例：它会遍历模型中的所有表格，并根据表格的类型和用途将其整理到相应的表格组中：

```csharp
// 遍历所有表：
foreach(var table in Model.Tables)
{
    if (table is CalculationGroupTable)
    {
        table.TableGroup = "计算组";
    }
    else if (!table.UsedInRelationships.Any() && table.Measures.Any(m => m.IsVisible))
    {
        // 包含可见度量值，但与其他表没有任何关系的表
        table.TableGroup = "Measure Groups";
    }
    else if (table.UsedInRelationships.All(r => r.FromTable == table) && table.UsedInRelationships.Any())
    {
        // 仅位于关系“多”端的表：
        table.TableGroup = "Facts";
    }
    else if (!table.UsedInRelationships.Any() && table is CalculatedTable && !table.Measures.Any())
    {
        // 没有任何关系、属于计算表格且不包含度量值的表：
        table.TableGroup = "Parameter Tables";
    }
    else if (table.UsedInRelationships.Any(r => r.ToTable == table))
    {
        // 位于关系“一”端的表：
        table.TableGroup = "Dimensions";
    }
    else
    {
        // 其他所有表：
        table.TableGroup = "Misc";
    }
}
```

## 隐藏表格组

如果你希望在 TOM Explorer 中始终看到完整的未分组表列表，但又需要与他人协作处理包含表格组注释的模型，你仍然可以在自己的 Tabular Editor 3 安装中完全禁用表格组。 可在 **工具 > 偏好设置** 对话框中进行设置。 转到 **TOM Explorer** 页面，然后在 **显示和筛选** 下取消选中 **使用表格组**：

![表格组禁用](~/content/assets/images/table-groups-disable.png)

> [!NOTE]
> 即使你按上述方法禁用了表格组，模型中的表仍可能已分配 `TabularEditor_TableGroup` 注释。 如果你想从模型中清除所有此类注释，可以使用以下 C# Script：
>
> ```csharp
> foreach(var table in Model.Tables) table.TableGroup = null;
> ```