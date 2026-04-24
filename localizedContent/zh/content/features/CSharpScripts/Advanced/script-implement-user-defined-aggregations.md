---
uid: script-implement-user-defined-aggregations
title: 实现用户定义聚合
author: Just Blindbæk
updated: 2026-02-22
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 实现用户定义聚合

## 脚本用途

该脚本会为所选事实表自动完成用户定义聚合的配置。

脚本将按照 [实现用户定义聚合](xref:user-defined-aggregations) 教程中介绍的步骤执行：

1. 克隆所选事实表，并将副本重命名为 `<FactTableName> details`
2. 将所有相关维度表分区设置为 **Dual** 存储模式
3. 将明细表缩减为单个分区，将其设置为 DirectQuery，隐藏所有列并隐藏该表，同时删除复制过来的度量值
4. 创建从明细表到各维度表的关系，并启用 **Rely On Referential Integrity**
5. 从聚合表中移除属性列，并隐藏该表
6. 更新度量值表达式，使其引用明细表
7. 为数值型基列配置 **Alternate Of** 属性

<br></br>

> [!NOTE]
> 脚本会根据数据类型识别并移除聚合表中的属性列。 未用作关系键的 `String`、`DateTime`、`Boolean` 或 `Unknown` 数据类型列会被移除。 运行脚本后检查结果，确认保留了正确的列。 未用作关系键的 `String`、`DateTime`、`Boolean` 或 `Unknown` 数据类型列会被移除。 运行脚本后检查结果，确认保留了正确的列。

<br></br>

## 脚本

### 为所选事实表实现用户定义聚合

```csharp
// ============================================================
// 实现用户定义聚合
//
// 在 TOM Explorer 中选择事实表（聚合表），然后运行此脚本。
// 以下步骤将全部自动完成：
//
//   1. 将事实表克隆为“<FactTableName> details”
//   2. 将相关维度的分区设置为 Dual 存储模式
//   3. 将明细表缩减为单个分区（AS 仅支持一个带 Full DataView 的 DQ 分区），
//      将明细表设置为 DirectQuery，隐藏其所有列及表本身，并删除复制的度量值
//   4. 创建从明细表到维度的关系，并设置 Rely On Referential Integrity = true
//   5. 从聚合表中移除属性列，并隐藏该表
//   6. 更新度量值表达式，使其引用明细表
//   7. 在数值基列上配置 Alternate Of
// ============================================================

// ── 验证选择 ────────────────────────────────────────────────────────

if (Selected.Table == null)
{
    Error("运行此脚本前，请先在 TOM Explorer 中选择原始事实表（聚合表）。");
    return;
}

var _aggTable   = Selected.Table;
var _detailName = _aggTable.Name + " details";

if (Model.Tables.Contains(_detailName))
{
    Error($"名为 '{_detailName}' 的表已存在。请删除或重命名它，然后重新运行脚本。");
    return;
}

if (!Model.Relationships.Any(r => r.FromTable.Name == _aggTable.Name))
{
    Error($"在 '{_aggTable.Name}' 上未找到出站关系。运行此脚本前，事实表必须先与维度建立关系。");
    return;
}

// ── 步骤 1：克隆事实表以创建明细表 ──────────────────

var _detailTable = _aggTable.Clone(_detailName);

// ── 步骤 2：将所有相关维度的分区设置为 Dual ─────────────────────

var _outboundRels = Model.Relationships
    .Where(r => r.FromTable.Name == _aggTable.Name)
    .ToList();

var _dimTables = _outboundRels
    .Select(r => r.ToTable)
    .Distinct()
    .ToList();

foreach (var _dim in _dimTables)
    foreach (var _p in _dim.Partitions)
        _p.Mode = ModeType.Dual;

// ── 步骤 3：配置明细表 ───────────────────────────────────────
// AS 仅支持一个带 Full DataView 的 DirectQuery 分区。
// 保留第一个分区并删除其余分区，然后将其设置为 DirectQuery。

var _allPartitions     = _detailTable.Partitions.ToList();
var _keptPartition     = _allPartitions[0];
var _removedPartitions = _allPartitions.Skip(1).ToList();

foreach (var _p in _removedPartitions)
    _p.Delete();

_keptPartition.Mode = ModeType.DirectQuery;

foreach (var _col in _detailTable.Columns)
{
    _col.IsHidden         = true;
    _col.IsAvailableInMDX = false;
}

_detailTable.IsHidden = true;

// 删除克隆过程中复制过来的所有度量值 —
// 度量值应保留在聚合表上，而不是明细表。
foreach (var _m in _detailTable.Measures.ToList())
    _m.Delete();

// ── 步骤 4：创建从明细表到维度的关系 ─────────

foreach (var _rel in _outboundRels)
{
    var _fromColName = _rel.FromColumn.Name;
    if (!_detailTable.Columns.Contains(_fromColName)) continue;

    var _newRel = Model.AddRelationship();
    _newRel.FromColumn = _detailTable.Columns[_fromColName];
    _newRel.ToColumn   = _rel.ToColumn;
    _newRel.RelyOnReferentialIntegrity = true;
}

// ── 步骤 5：从聚合表中移除属性列 ───────────────
// 保留：  键列（关系中使用的外键）
//         数值列（将被映射为基列的 Alternate Of）
// 移除：  String、DateTime、Boolean 以及其他非数值属性列

var _keyCols = new HashSet<string>(
    _outboundRels.Select(r => r.FromColumn.Name));

var _typesToRemove = new[] {
    DataType.String, DataType.DateTime, DataType.Boolean, DataType.Unknown };

var _colsToRemove = _aggTable.Columns
    .Where(c => !_keyCols.Contains(c.Name)
             && _typesToRemove.Contains(c.DataType))
    .ToList();

foreach (var _col in _colsToRemove)
    _col.Delete();

// 隐藏键列 — 结构性列，不面向报表用户
foreach (var _col in _aggTable.Columns.Where(c => _keyCols.Contains(c.Name)).ToList())
{
    _col.IsHidden         = true;
    _col.IsAvailableInMDX = false;
}

// 隐藏聚合表本身
_aggTable.IsHidden = true;

// ── 步骤 6：更新度量值表达式，使其引用明细表 ──────────

var _oldRef = "'" + _aggTable.Name + "'[";
var _newRef = "'" + _detailName    + "'[";

foreach (var _measure in _aggTable.Measures)
    _measure.Expression = _measure.Expression.Replace(_oldRef, _newRef);

// ── 步骤 7：在数值基列上配置 Alternate Of ───────────────────

var _numericTypes = new[] { DataType.Double, DataType.Int64, DataType.Decimal };

var _numericCols = _aggTable.Columns
    .Where(c => _numericTypes.Contains(c.DataType) && !_keyCols.Contains(c.Name))
    .ToList();

var _alternateOfWarnings = new List<string>();

foreach (var _col in _numericCols)
{
    _col.IsHidden         = true;
    _col.IsAvailableInMDX = false;

    if (!_detailTable.Columns.Contains(_col.Name))
    {
        _alternateOfWarnings.Add(_col.Name + "（在明细表中找不到匹配的列）");
        continue;
    }

    try
    {
        _col.AddAlternateOf(_detailTable.Columns[_col.Name], SummarizationType.Sum);
    }
    catch
    {
        _alternateOfWarnings.Add(_col.Name + "（请在“属性”面板中手动配置 Alternate Of）");
    }
}

// ── 完成 ─────────────────────────────────────────────────────────────────────

var _summary =
    $"已为 '{_aggTable.Name}' 配置用户定义聚合。\n\n" +
    $"  明细表：                    {_detailName}\n" +
    $"  保留的分区：                {_keptPartition.Name}\n" +
    $"  已删除的分区：              {_removedPartitions.Count}\n" +
    $"  已设置为 Dual 的维度：      {string.Join(", ", _dimTables.Select(t => t.Name))}\n" +
    $"  已移除的属性列：            {_colsToRemove.Count}\n" +
    $"  数值基列：                  {_numericCols.Count}";

if (_removedPartitions.Count > 0)
    _summary += $"\n\n⚠ 重要：请检查 '{_keptPartition.Name}' 上的分区表达式。\n" +
                "  明细表必须覆盖所有数据 — 请移除原表用于增量刷新的\n" +
                "  任何日期/范围筛选条件。";

if (_alternateOfWarnings.Any())
    _summary += "\n\n以下列无法自动设置 Alternate Of。\n" +
                "请在“属性”面板中手动配置：\n  - " +
                string.Join("\n  - ", _alternateOfWarnings);

_summary += "\n\n保存后，请在模型上运行 Process Recalc 以重新计算\n" +
            "新的关系。无需重新导入数据。\n\n" +
            "保存前请仔细检查模型。";

Info(_summary);
```

### 说明

脚本会先验证所选内容，并确认模型中还没有名为 `<FactTableName> details` 的表。

**第 1 步** 使用内置的 `.Clone()` 方法克隆所选事实表，创建一个名为 `<FactTableName> details` 的完全副本。 这会从原表复制所有列、分区和度量值。 这会从原表复制所有列、分区和度量值。

**第 2 步** 沿着聚合表的出站关系识别维度表，然后将每个维度表的所有分区存储模式设置为 `Dual`。

**第 3 步** 配置明细表。 **第 3 步** 配置明细表。 在使用 Full DataView 时，Analysis Services 只支持一个 DirectQuery 分区，因此会删除除第一个之外的所有分区。 将保留的分区设置为 `DirectQuery`。 隐藏所有列，并将其标记为在 MDX 中不可用。 克隆时复制过来的所有度量值都会被删除。 如果删除了分区，摘要对话框会提示你检查保留分区的表达式——必须移除从增量刷新设置继承的任何日期或范围筛选，以确保明细表覆盖全部数据。 将保留的分区设置为 `DirectQuery`。 隐藏所有列，并将其标记为在 MDX 中不可用。 克隆时复制过来的所有度量值都会被删除。 如果删除了分区，摘要对话框会提示你检查保留分区的表达式——必须移除从增量刷新设置继承的任何日期或范围筛选，以确保明细表覆盖全部数据。

**第 4 步** 在明细表与各维度表之间创建关系，使之与聚合表上的现有关系保持一致。 **第 4 步** 在明细表与各维度表之间创建关系，使之与聚合表上的现有关系保持一致。 在每条新关系上将 `Rely On Referential Integrity` 设置为 `true`，这会指示引擎在 DirectQuery SQL 中使用 INNER JOIN 而不是 OUTER JOIN。

**第 5 步** 从聚合表中移除属性列（string、datetime、boolean），仅保留键列和数值列。 键列将被隐藏。 聚合表本身也会被隐藏。 键列将被隐藏。 聚合表本身也会被隐藏。

**第 6 步** 更新度量值表达式，使其引用明细表而不是聚合表。 这是确保 DirectQuery 回退机制正常工作的必要条件。

**第 7 步** 使用 `AddAlternateOf()` 为每个数值型基列配置 `Alternate Of` 属性，该方法会在一次调用中完成初始化并设置映射。 如果某列无法自动映射（例如，在明细表中找不到对应列），摘要对话框会添加一条警告，并且必须在 **Properties** 面板中手动配置该列。 如果某列无法自动映射（例如，在明细表中找不到对应列），摘要对话框会添加一条警告，并且必须在 **Properties** 面板中手动配置该列。

> [!NOTE]
> 保存模型后，请对模型运行 **Process Recalc**。 各表会保留其已处理状态——只有新建的关系会处于 `CalculationNeeded` 状态，需要重新计算。 无需重新导入数据。 各表会保留其已处理状态——只有新建的关系会处于 `CalculationNeeded` 状态，需要重新计算。 无需重新导入数据。
