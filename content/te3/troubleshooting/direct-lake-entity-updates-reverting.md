---
uid: direct-lake-entity-updates-reverting
title: Entity Name Changes Revert in Direct Lake Models
author: Morten Lønskov
updated: 2025-14-10
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
      none: x
    - edition: Enterprise
---
# Entity Name Changes Revert in Direct Lake Models

After editing `EntityName` in Tabular Editor 3 for a Direct Lake table partition, the model may reload in Power BI  with the original names. This behavior often looks like TE3 did not persist the change, but it is caused by how Power BI interprets Direct Lake metadata during refresh.

---

## Symptoms

- Table metadata changes appear in TE3 but revert after you refresh the model in Power BI.
- The reverted tables are Direct Lake tables whose metadata was altered outside Power BI.
- Refresh operations run without explicit errors, yet the renamed objects fall back to their original names.

---

## Root cause

Power BI binds Direct Lake tables to their origin through the `SourceLineageTag` property. When the tag does not match the current partition's `EntityName`, Power BI assumes the table should stay synchronized with the original source and restores the previous metadata. Direct Lake partitions also expect intentional changes to be registered through the `ChangedProperties` collection; without it, Power BI ignores manual edits made outside the service.

---

## Resolution steps

1. **Open the table partition.** For each Direct Lake table, edit the associated `EntityName`.
2. **Synchronize partition details.**
   - Set the table's `SourceLineageTag` to exactly match the new `EntityName`.
   - Set the `Name` property to true for table's `ChangedProperties` collection so Power BI treats the rename as intentional.
4. **Save the model in TE3.**
5. **Refresh the affected table (or the entire model) in Power BI.** 
The names should now persist.

---

## Important notes

- TE3 does not update `SourceLineageTag` automatically when you rename the table. Always align the tag manually.
- The `ChangedProperties` flag is required only for Direct Lake (and other composite) tables; legacy import models do not need it.
- These behaviors originate from Power BI’s metadata synchronization rules, not from TE3 storage.

## Automate bulk updates with C#

When you have many Direct Lake tables to adjust, you can run the following TE3 script. It prompts for new entity names, updates each selected table, syncs the `SourceLineageTag`, and flags the changed metadata.

> **Use it in TE3:** Select the relevant Direct Lake tables, open the **C# Script** window, paste the script, and run it.

```csharp
// -------- Namespaces --------
using System;
using System.Linq;
using System.Collections.Generic;
using System.ComponentModel;
using System.Windows.Forms;
using TW = TabularEditor.TOMWrapper;
using TOM = Microsoft.AnalysisServices.Tabular;

// -------- Guard: need tables selected --------
if (!Selected.Tables.Any())
{
    Warning("Select one or more tables first.");
    return;
}

// -------- Build editable rows from selected tables --------
var rows = new BindingList<EntityEditRow>();
foreach (var table in Selected.Tables.ToList())
{
    var epart = table.Partitions.OfType<TW.EntityPartition>().FirstOrDefault();
    if (epart == null)
    {
        Warning($"Skipping '{table.Name}': no Entity partition.");
        continue;
    }
    rows.Add(new EntityEditRow
    {
        Table = table,
        CurrentEntity = epart.EntityName ?? string.Empty,
        NewEntity = epart.EntityName ?? string.Empty
    });
}

if (rows.Count == 0)
{
    Warning("No selected tables have an Entity partition. Nothing to edit.");
    return;
}

// -------- Show batch dialog (improved layout/DPI handling) --------
var dlg = new BatchEntityEditor(rows);
var dr = dlg.ShowDialog();
if (dr != DialogResult.OK)
{
    Info("Cancelled. No changes applied.");
    return;
}

// -------- Apply changes --------
int updated = 0;
foreach (var r in rows)
{
    try
    {
        if (r.Table == null) continue;
        var epart = r.Table.Partitions.OfType<TW.EntityPartition>().FirstOrDefault();
        if (epart == null) continue;

        if (string.IsNullOrWhiteSpace(r.NewEntity) ||
            string.Equals(r.NewEntity, r.CurrentEntity, StringComparison.Ordinal))
            continue;

        epart.EntityName = r.NewEntity;

        try { r.Table.SourceLineageTag = r.NewEntity; }
        catch (Exception exTag)
        {
            Warning($"SourceLineageTag not set on '{r.Table.Name}': {exTag.Message}");
        }

        r.Table.SetExtendedProperty("Changed Property Name", "true", TW.ExtendedPropertyType.String);
        updated++;
        Output($"Updated '{r.Table.Name}': Entity='{r.NewEntity}', SourceLineageTag='{r.NewEntity}'.");
    }
    catch (Exception ex)
    {
        Error($"Failed on '{r.Table?.Name ?? "(unknown)"}': {ex.Message}");
    }
}

Info($"Done. {updated} table(s) updated.");


// ====================== Support types / UI ======================
public class EntityEditRow
{
    [Browsable(false)]
    public TW.Table Table { get; set; }
    public string TableName => Table?.Name ?? "";
    public string CurrentEntity { get; set; }
    public string NewEntity { get; set; }
}

public class BatchEntityEditor : Form
{
    private DataGridView _grid;
    private Button _ok;
    private Button _cancel;
    private BindingList<EntityEditRow> _rows;

    public BatchEntityEditor(BindingList<EntityEditRow> rows)
    {
        _rows = rows;
        BuildUI();
    }

    private void BuildUI()
    {
        // Form
        Text = "Edit Entity names for selected tables";
        TopMost = true;
        ShowInTaskbar = false;
        StartPosition = FormStartPosition.CenterScreen;
        AutoScaleMode = AutoScaleMode.Dpi;     // DPI-aware
        Font = new System.Drawing.Font("Segoe UI", 9F); // readable default
        Width = 900;
        Height = 600;
        MinimumSize = new System.Drawing.Size(820, 500);
        FormBorderStyle = FormBorderStyle.Sizable;

        // Root layout = table with 3 rows: label, grid, buttons
        var root = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 1,
            RowCount = 3,
            Padding = new Padding(10)
        };
        // Row heights: label (auto), grid (*), buttons (absolute)
        root.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        root.RowStyles.Add(new RowStyle(SizeType.Percent, 100f));
        root.RowStyles.Add(new RowStyle(SizeType.Absolute, 56f));
        Controls.Add(root);

        // Intro label
        var lbl = new Label
        {
            Text = "Edit the Entity name for each table. Leave 'New Entity' unchanged to skip.",
            AutoSize = true,
            Dock = DockStyle.Fill,
            Padding = new Padding(0, 0, 0, 6)
        };
        root.Controls.Add(lbl, 0, 0);

        // Grid
        _grid = new DataGridView
        {
            Dock = DockStyle.Fill,
            AutoGenerateColumns = false,
            AllowUserToAddRows = false,
            AllowUserToDeleteRows = false,
            ReadOnly = false,
            RowHeadersVisible = false,
            SelectionMode = DataGridViewSelectionMode.FullRowSelect,

            // Header/column sizing to avoid clipping
            ColumnHeadersVisible = true,
            ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
            AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.None,
            EnableHeadersVisualStyles = true
        };

        var colTable = new DataGridViewTextBoxColumn
        {
            DataPropertyName = "TableName",
            HeaderText = "Table",
            ReadOnly = true,
            AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill,
            FillWeight = 28
        };
        var colCurrent = new DataGridViewTextBoxColumn
        {
            DataPropertyName = "CurrentEntity",
            HeaderText = "Current Entity",
            ReadOnly = true,
            AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill,
            FillWeight = 36
        };
        var colNew = new DataGridViewTextBoxColumn
        {
            DataPropertyName = "NewEntity",
            HeaderText = "New Entity",
            ReadOnly = false,
            AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill,
            FillWeight = 36
        };

        _grid.Columns.AddRange(colTable, colCurrent, colNew);
        _grid.DataSource = _rows;

        // Ensure first cell visible and columns fitted
        _grid.DataBindingComplete += (s, e) =>
        {
            _grid.AutoResizeColumns(DataGridViewAutoSizeColumnsMode.DisplayedCells);
            if (_grid.Rows.Count > 0)
            {
                _grid.ClearSelection();
                _grid.CurrentCell = _grid.Rows[0].Cells[2]; // focus New Entity
                _grid.BeginEdit(true);
            }
        };

        root.Controls.Add(_grid, 0, 1);

        // Buttons panel
        var pnl = new FlowLayoutPanel
        {
            Dock = DockStyle.Fill,
            FlowDirection = FlowDirection.RightToLeft,
            Padding = new Padding(0),
            WrapContents = false
        };

        _ok = new Button { Text = "OK", DialogResult = DialogResult.OK, AutoSize = true, Height = 32, Width = 110, Margin = new Padding(8, 8, 0, 8) };
        _cancel = new Button { Text = "Cancel", DialogResult = DialogResult.Cancel, AutoSize = true, Height = 32, Width = 110, Margin = new Padding(8, 8, 8, 8) };

        pnl.Controls.Add(_ok);
        pnl.Controls.Add(_cancel);

        AcceptButton = _ok;
        CancelButton = _cancel;

        root.Controls.Add(pnl, 0, 2);

        // Bring to front when shown
        Load += (s, e) =>
        {
            Activate();
            BringToFront();
            _grid.Focus();
        };
    }
}
```
> [!NOTE] The script was generated using an LLM for code assistance, but have been tested by the Tabular Editor team. 

Running the script updates only the tables that receive a new entity name. After the script finishes, review the changes, save the model, and refresh in Power BI to confirm the metadata persists.

Finally, open each updated partition and verify that `Name` is present in the `ChangedProperties` collection before refreshing from Power BI.