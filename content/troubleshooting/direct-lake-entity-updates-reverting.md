---
uid: direct-lake-entity-updates-reverting
title: Entity Name Changes Revert in Direct Lake Models
author: Morten Lønskov
updated: 2025-10-14
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
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
3. **Save the model in TE3.**
4. **Refresh the affected table (or the entire model) in Power BI.** 
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

// -------- Guard: need tables selected --------
var tables = Selected.Tables.ToList();
if (tables.Count == 0)
{
    Warning("Select one or more tables first.");
    return;
}

// -------- Build editable rows from selected tables --------
var candidates = tables
    .Select(table => new { Table = table, Partition = table.Partitions.OfType<TW.EntityPartition>().FirstOrDefault() })
    .ToList();

foreach (var skipped in candidates.Where(c => c.Partition == null))
{
    Warning($"Skipping '{skipped.Table.Name}': no Entity partition.");
}

var rows = new BindingList<EntityEditRow>(
    candidates
        .Where(c => c.Partition != null)
        .Select(c => new EntityEditRow(c.Table, c.Partition))
        .ToList());

if (rows.Count == 0)
{
    Warning("No selected tables have an Entity partition. Nothing to edit.");
    return;
}

// -------- Show batch dialog --------
using (var dialog = new BatchEntityEditor(rows))
{
    if (dialog.ShowDialog() != DialogResult.OK)
    {
        Info("Cancelled. No changes applied.");
        return;
    }
}

// -------- Apply changes --------
const string ExtendedPropertyName = "Changed Property Name";
var updated = 0;

foreach (var row in rows)
{
    try
    {
        if (!row.ApplyChanges(ExtendedPropertyName, Warning))
            continue;

        updated++;
        Output($"Updated '{row.TableName}': Entity='{row.CurrentEntity}', Partition='{row.Partition.Name}', SourceLineageTag='{row.CurrentEntity}'.");
    }
    catch (Exception ex)
    {
        Error($"Failed on '{row.TableName}': {ex.Message}");
    }
}

Info($"Done. {updated} table(s) updated.");


// ====================== Support types / UI ======================
public class EntityEditRow
{
    public EntityEditRow(TW.Table table, TW.EntityPartition partition)
    {
        Table = table ?? throw new ArgumentNullException(nameof(table));
        Partition = partition ?? throw new ArgumentNullException(nameof(partition));

        CurrentEntity = partition.EntityName ?? string.Empty;
        NewEntity = CurrentEntity;
    }

    [Browsable(false)]
    public TW.Table Table { get; }

    [Browsable(false)]
    public TW.EntityPartition Partition { get; }

    public string TableName => Table.Name;
    public string CurrentEntity { get; private set; }
    public string NewEntity { get; set; }

    public bool ApplyChanges(string extendedPropertyName, Action<string> warn)
    {
        var target = NewEntity ?? string.Empty;
        if (string.IsNullOrWhiteSpace(target) ||
            string.Equals(target, CurrentEntity, StringComparison.Ordinal))
        {
            return false;
        }

        Partition.EntityName = target;

        if (!string.Equals(Partition.Name, target, StringComparison.Ordinal))
        {
            var nameConflict = Table.Partitions
                .Where(p => !ReferenceEquals(p, Partition))
                .Any(p => string.Equals(p.Name, target, StringComparison.Ordinal));

            if (nameConflict)
            {
                warn?.Invoke($"Partition rename skipped for '{TableName}': another partition already named '{target}'.");
            }
            else
            {
                try
                {
                    Partition.Name = target;
                }
                catch (Exception ex)
                {
                    warn?.Invoke($"Partition rename failed for '{TableName}': {ex.Message}");
                }
            }
        }

        try
        {
            Table.SourceLineageTag = target;
        }
        catch (Exception ex)
        {
            warn?.Invoke($"SourceLineageTag not set on '{TableName}': {ex.Message}");
        }

        Table.SetExtendedProperty(extendedPropertyName, "true", TW.ExtendedPropertyType.String);
        CurrentEntity = target;
        return true;
    }
}

public class BatchEntityEditor : Form
{
    private readonly BindingList<EntityEditRow> rows;
    private DataGridView grid;

    public BatchEntityEditor(BindingList<EntityEditRow> rows)
    {
        this.rows = rows ?? throw new ArgumentNullException(nameof(rows));
        BuildUi();
    }

    private void BuildUi()
    {
        Text = "Edit Entity names for selected tables";
        TopMost = true;
        ShowInTaskbar = false;
        StartPosition = FormStartPosition.CenterScreen;
        AutoScaleMode = AutoScaleMode.Dpi;
        Font = new System.Drawing.Font("Segoe UI", 9F);
        Width = 900;
        Height = 600;
        MinimumSize = new System.Drawing.Size(820, 500);
        FormBorderStyle = FormBorderStyle.Sizable;

        var root = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 1,
            RowCount = 3,
            Padding = new Padding(10)
        };
        root.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        root.RowStyles.Add(new RowStyle(SizeType.Percent, 100f));
        root.RowStyles.Add(new RowStyle(SizeType.Absolute, 56f));
        Controls.Add(root);

        root.Controls.Add(new Label
        {
            Text = "Edit the Entity name for each table. Leave 'New Entity' unchanged to skip.",
            AutoSize = true,
            Dock = DockStyle.Fill,
            Padding = new Padding(0, 0, 0, 6)
        }, 0, 0);

        grid = new DataGridView
        {
            Dock = DockStyle.Fill,
            AutoGenerateColumns = false,
            AllowUserToAddRows = false,
            AllowUserToDeleteRows = false,
            ReadOnly = false,
            RowHeadersVisible = false,
            SelectionMode = DataGridViewSelectionMode.FullRowSelect,
            ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        };

        grid.Columns.AddRange(
            new DataGridViewTextBoxColumn
            {
                DataPropertyName = nameof(EntityEditRow.TableName),
                HeaderText = "Table",
                ReadOnly = true,
                FillWeight = 28
            },
            new DataGridViewTextBoxColumn
            {
                DataPropertyName = nameof(EntityEditRow.CurrentEntity),
                HeaderText = "Current Entity",
                ReadOnly = true,
                FillWeight = 36
            },
            new DataGridViewTextBoxColumn
            {
                DataPropertyName = nameof(EntityEditRow.NewEntity),
                HeaderText = "New Entity",
                FillWeight = 36
            });

        grid.DataSource = rows;
        root.Controls.Add(grid, 0, 1);

        var buttons = new FlowLayoutPanel
        {
            Dock = DockStyle.Fill,
            FlowDirection = FlowDirection.RightToLeft,
            WrapContents = false,
            Padding = new Padding(0)
        };

        var ok = new Button { Text = "OK", DialogResult = DialogResult.OK, AutoSize = true, Height = 32, Width = 110, Margin = new Padding(8, 8, 0, 8) };
        var cancel = new Button { Text = "Cancel", DialogResult = DialogResult.Cancel, AutoSize = true, Height = 32, Width = 110, Margin = new Padding(8, 8, 8, 8) };

        buttons.Controls.Add(ok);
        buttons.Controls.Add(cancel);

        AcceptButton = ok;
        CancelButton = cancel;
        root.Controls.Add(buttons, 0, 2);

        Shown += (_, _) =>
        {
            grid.ClearSelection();
            if (grid.Rows.Count > 0)
            {
                grid.CurrentCell = grid.Rows[0].Cells[2];
                grid.BeginEdit(true);
            }
        };
    }
}
```
> [!NOTE] 
> The script was generated using an LLM for code assistance, but has been tested by the Tabular Editor team. 

Running the script updates only the tables that receive a new entity name. After the script finishes, review the changes, save the model, and refresh in Power BI to confirm the metadata persists.

Finally, open each updated partition and verify that `Name` is present in the `ChangedProperties` collection before refreshing from Power BI.