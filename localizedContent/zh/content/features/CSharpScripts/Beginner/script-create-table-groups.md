---
uid: script-create-table-groups
title: 创建表格组
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# 创建表格组

## 脚本用途

该脚本会在 Tabular Editor 3 中创建默认表格组。

## 脚本

### 脚本标题

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
        // 包含可见度量值但与其他表没有关系的表
        table.TableGroup = "度量值组";
    }
    else if (table.UsedInRelationships.All(r => r.FromTable == table) && table.UsedInRelationships.Any())
    {
        // 仅位于关系“多”端的表：
        table.TableGroup = "事实";
    }
    else if (!table.UsedInRelationships.Any() && table is CalculatedTable && !table.Measures.Any())
    {
        // 没有任何关系的表，属于计算表格且不包含度量值：
        table.TableGroup = "参数表";
    }
    else if (table.UsedInRelationships.Any(r => r.ToTable == table))
    {
        // 位于关系“一”端的表：
        table.TableGroup = "维度";
    }
    else
    {
        // 其他所有表：
        table.TableGroup = "杂项";
    }
}
```

### 说明

该脚本遍历模型中的所有表，并根据特定属性为其分配表格组。

