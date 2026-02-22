---
uid: script-implement-user-defined-aggregations
title: Implement User-defined Aggregations
author: Just Blindbæk
updated: 2026-02-22
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# Implement User-defined Aggregations

## Script Purpose

This script fully automates the configuration of user-defined aggregations for a selected fact table.

The script performs the following steps, as described in the [Implementing User-defined Aggregations](xref:user-defined-aggregations) tutorial:

1. Clones the selected fact table and renames the copy to `<FactTableName> details`
2. Sets all related dimension table partitions to **Dual** storage mode
3. Reduces the detail table to a single partition, sets it to DirectQuery, hides all columns, hides the table, and deletes copied measures
4. Creates relationships from the detail table to the dimension tables with **Rely On Referential Integrity** enabled
5. Removes attribute columns from the aggregation table, hides the table
6. Updates measure expressions to reference the detail table
7. Configures the **Alternate Of** property on numeric base columns

<br></br>

> [!NOTE]
> The script identifies attribute columns to remove from the aggregation table by data type. Columns with `String`, `DateTime`, `Boolean`, or `Unknown` data types that are not used as relationship keys are removed. Review the result after running the script to verify the correct columns were retained.

<br></br>

## Script

### Implement User-defined Aggregations for Selected Fact Table

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

### Explanation

The script begins by validating the selection and checking that a table named `<FactTableName> details` does not already exist in the model.

**Step 1** clones the selected fact table using the built-in `.Clone()` method, creating an exact copy named `<FactTableName> details`. This copies all columns, partitions, and measures from the original.

**Step 2** identifies dimension tables by following outbound relationships from the aggregation table, then sets every partition on each dimension table to `Dual` storage mode.

**Step 3** configures the detail table. Analysis Services only supports one DirectQuery partition when using Full DataView, so all partitions except the first are deleted. The remaining partition is set to `DirectQuery`. All columns are hidden and marked as unavailable in MDX. Any measures copied during cloning are deleted. If partitions were removed, the summary dialog warns that the retained partition's expression must be reviewed — any date or range filtering inherited from an incremental refresh setup must be removed so that the detail table covers all data.

**Step 4** creates relationships from the detail table to each dimension table, mirroring the existing relationships on the aggregation table. `Rely On Referential Integrity` is set to `true` on each new relationship, which tells the engine to use INNER JOIN instead of OUTER JOIN in DirectQuery SQL.

**Step 5** removes attribute columns (string, datetime, boolean) from the aggregation table, retaining only key columns and numeric columns. Key columns are hidden. The aggregation table itself is also hidden.

**Step 6** updates measure expressions to reference the detail table instead of the aggregation table. This is necessary for the DirectQuery fallback to work correctly.

**Step 7** configures the `Alternate Of` property on each numeric base column using `AddAlternateOf()`, which initializes and sets the mapping in a single call. If a column cannot be mapped automatically (for example, if no matching column exists in the detail table), a warning is added to the summary dialog and the column must be configured manually in the **Properties** panel.

> [!NOTE]
> After saving the model, run **Process Recalc** on the model. The tables retain their processed state — only the new relationships are left in a `CalculationNeeded` state and need to be recalculated. No data reimport is required.
