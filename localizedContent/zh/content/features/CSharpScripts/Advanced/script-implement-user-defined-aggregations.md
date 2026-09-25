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
> 脚本会根据数据类型识别并移除聚合表中的属性列。 Columns with `String`, `DateTime`, `Boolean`, or `Unknown` data types that are not used as relationship keys are removed. Review the result after running the script to verify the correct columns were retained.

<br></br>

## 脚本

### 为所选事实表实现用户定义聚合

```csharp
// ============================================================
// Implement User-Defined Aggregations
//
// Select the fact table (the aggregation table) in the TOM
// Explorer, then run this script. All steps are automated:
//
//   1. Clones the fact table as "<FactTableName> details"
//   2. Sets related dimension partitions to Dual storage mode
//   3. Reduces the detail table to a single partition (AS only supports
//      one DQ partition with Full DataView), sets it to DirectQuery,
//      hides all columns and the table, deletes copied measures
//   4. Creates relationships from the detail table to dimension
//      tables with Rely On Referential Integrity = true
//   5. Removes attribute columns from the aggregation table,
//      hides the table
//   6. Updates measure expressions to reference the detail table
//   7. Configures Alternate Of on numeric base columns
// ============================================================

// ── Validate selection ────────────────────────────────────────────────────────

if (Selected.Table == null)
{
    Error("Select the original fact table (the aggregation table) in the TOM Explorer before running this script.");
    return;
}

var _aggTable   = Selected.Table;
var _detailName = _aggTable.Name + " details";

if (Model.Tables.Contains(_detailName))
{
    Error($"A table named '{_detailName}' already exists. Remove or rename it, then re-run the script.");
    return;
}

if (!Model.Relationships.Any(r => r.FromTable.Name == _aggTable.Name))
{
    Error($"No outbound relationships found on '{_aggTable.Name}'. The fact table must have relationships to dimension tables before running this script.");
    return;
}

// ── Step 1: Clone the fact table to create the detail table ──────────────────

var _detailTable = _aggTable.Clone(_detailName);

// ── Step 2: Set all related dimension partitions to Dual ─────────────────────

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

// ── Step 3: Configure the detail table ───────────────────────────────────────
// AS only supports one DirectQuery partition with Full DataView.
// Keep the first partition and delete the rest, then set it to DirectQuery.

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

// Delete any measures that were copied during cloning —
// measures belong on the aggregation table, not the detail table.
foreach (var _m in _detailTable.Measures.ToList())
    _m.Delete();

// ── Step 4: Create relationships from detail table to dimension tables ─────────

foreach (var _rel in _outboundRels)
{
    var _fromColName = _rel.FromColumn.Name;
    if (!_detailTable.Columns.Contains(_fromColName)) continue;

    var _newRel = Model.AddRelationship();
    _newRel.FromColumn = _detailTable.Columns[_fromColName];
    _newRel.ToColumn   = _rel.ToColumn;
    _newRel.RelyOnReferentialIntegrity = true;
}

// ── Step 5: Remove attribute columns from the aggregation table ───────────────
// Keep:   key columns (foreign keys used in relationships)
//         numeric columns (will be mapped as Alternate Of base columns)
// Remove: string, datetime, boolean, and other non-numeric attribute columns

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

// Hide key columns — structural columns, not for report consumers
foreach (var _col in _aggTable.Columns.Where(c => _keyCols.Contains(c.Name)).ToList())
{
    _col.IsHidden         = true;
    _col.IsAvailableInMDX = false;
}

// Hide the aggregation table itself
_aggTable.IsHidden = true;

// ── Step 6: Update measure expressions to reference the detail table ──────────

var _oldRef = "'" + _aggTable.Name + "'[";
var _newRef = "'" + _detailName    + "'[";

foreach (var _measure in _aggTable.Measures)
    _measure.Expression = _measure.Expression.Replace(_oldRef, _newRef);

// ── Step 7: Configure Alternate Of on numeric base columns ───────────────────

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
        _alternateOfWarnings.Add(_col.Name + " (no matching column found in detail table)");
        continue;
    }

    try
    {
        _col.AddAlternateOf(_detailTable.Columns[_col.Name], SummarizationType.Sum);
    }
    catch
    {
        _alternateOfWarnings.Add(_col.Name + " (configure Alternate Of manually in the Properties panel)");
    }
}

// ── Done ─────────────────────────────────────────────────────────────────────

var _summary =
    $"User-defined aggregations configured for '{_aggTable.Name}'.\n\n" +
    $"  Detail table:                {_detailName}\n" +
    $"  Partition retained:          {_keptPartition.Name}\n" +
    $"  Partitions removed:          {_removedPartitions.Count}\n" +
    $"  Dimensions set to Dual:      {string.Join(", ", _dimTables.Select(t => t.Name))}\n" +
    $"  Attribute columns removed:   {_colsToRemove.Count}\n" +
    $"  Numeric base columns:        {_numericCols.Count}";

if (_removedPartitions.Count > 0)
    _summary += $"\n\n⚠ IMPORTANT: Review the partition expression on '{_keptPartition.Name}'.\n" +
                "  The detail table must cover all data — remove any date/range filtering\n" +
                "  that was used for incremental refresh on the original table.";

if (_alternateOfWarnings.Any())
    _summary += "\n\nThe following columns could not have Alternate Of set automatically.\n" +
                "Configure them manually in the Properties panel:\n  - " +
                string.Join("\n  - ", _alternateOfWarnings);

_summary += "\n\nAfter saving, run Process Recalc on the model to recalculate\n" +
            "the new relationships. No data reimport is needed.\n\n" +
            "Review the model carefully before saving.";

Info(_summary);
```

### 说明

脚本会先验证所选内容，并确认模型中还没有名为 `<FactTableName> details` 的表。

**第 1 步** 使用内置的 `.Clone()` 方法克隆所选事实表，创建一个名为 `<FactTableName> details` 的完全副本。 This copies all columns, partitions, and measures from the original.

**第 2 步** 沿着聚合表的出站关系识别维度表，然后将每个维度表的所有分区存储模式设置为 `Dual`。

**Step 3** configures the detail table. 在使用 Full DataView 时，Analysis Services 只支持一个 DirectQuery 分区，因此会删除除第一个之外的所有分区。 The remaining partition is set to `DirectQuery`. All columns are hidden and marked as unavailable in MDX. Any measures copied during cloning are deleted. If partitions were removed, the summary dialog warns that the retained partition's expression must be reviewed — any date or range filtering inherited from an incremental refresh setup must be removed so that the detail table covers all data.

**Step 4** creates relationships from the detail table to each dimension table, mirroring the existing relationships on the aggregation table. 在每条新关系上将 `Rely On Referential Integrity` 设置为 `true`，这会指示引擎在 DirectQuery SQL 中使用 INNER JOIN 而不是 OUTER JOIN。

**第 5 步** 从聚合表中移除属性列（string、datetime、boolean），仅保留键列和数值列。 Key columns are hidden. The aggregation table itself is also hidden.

**Step 6** updates measure expressions to reference the detail table instead of the aggregation table. This is necessary for the DirectQuery fallback to work correctly.

**第 7 步** 使用 `AddAlternateOf()` 为每个数值型基列配置 `Alternate Of` 属性，该方法会在一次调用中完成初始化并设置映射。 If a column cannot be mapped automatically (for example, if no matching column exists in the detail table), a warning is added to the summary dialog and the column must be configured manually in the **Properties** panel.

> [!NOTE]
> 保存模型后，请对模型运行 **Process Recalc**。 The tables retain their processed state — only the new relationships are left in a `CalculationNeeded` state and need to be recalculated. No data reimport is required.
