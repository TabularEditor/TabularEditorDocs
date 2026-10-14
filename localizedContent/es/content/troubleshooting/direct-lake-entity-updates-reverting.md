---
uid: direct-lake-entity-updates-reverting
title: Se revierten los cambios de nombre de entidades en modelos Direct Lake
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

# Se revierten los cambios de nombre de entidades en modelos Direct Lake

Después de editar `EntityName` en Tabular Editor 3 para una partición de una tabla Direct Lake, es posible que el modelo se recargue en Power BI con los nombres originales. Este comportamiento suele dar la impresión de que TE3 no ha conservado el cambio, pero se debe a cómo Power BI interpreta los metadatos de Direct Lake durante la actualización.

---

## Síntomas

- Los cambios de metadatos de la tabla aparecen en TE3, pero se revierten después de actualizar el modelo en Power BI.
- Las tablas revertidas son tablas Direct Lake cuyos metadatos se modificaron fuera de Power BI.
- Las operaciones de actualización se ejecutan sin errores explícitos, pero los objetos renombrados vuelven a sus nombres originales.

---

## Causa raíz

Power BI vincula las tablas Direct Lake a su origen mediante la propiedad `SourceLineageTag`. Cuando la etiqueta no coincide con el `EntityName` de la partición actual, Power BI asume que la tabla debe seguir sincronizada con el origen original y restaura los metadatos anteriores. Las particiones Direct Lake también esperan que los cambios intencionados se registren mediante la colección `ChangedProperties`; sin ello, Power BI ignora las ediciones manuales realizadas fuera del servicio.

---

## Pasos para solucionarlo

1. **Abra la partición de la tabla.** Para cada tabla Direct Lake, edite el `EntityName` asociado.
2. **Sincronice los detalles de la partición.**
   - Configure el `SourceLineageTag` de la tabla para que coincida exactamente con el nuevo `EntityName`.
   - Establezca la propiedad `Name` en true en la colección `ChangedProperties` de la tabla para que Power BI trate el cambio de nombre como intencionado.
3. **Guarda el modelo en TE3.**
4. **Actualiza la tabla afectada (o el modelo completo) en Power BI.**
   Ahora los nombres deberían conservarse.

---

## Notas importantes

- TE3 no actualiza `SourceLineageTag` automáticamente cuando cambias el nombre de la tabla. Alinea siempre la etiqueta manualmente.
- El indicador `ChangedProperties` solo es necesario en tablas Direct Lake (y otras tablas compuestas); los modelos heredados en Import mode no lo requieren.
- Estos comportamientos se deben a las reglas de sincronización de metadatos de Power BI, no al almacenamiento de TE3.

## Automatiza actualizaciones masivas con C\#

Cuando tienes muchas tablas Direct Lake que ajustar, puedes ejecutar el siguiente script de TE3. Te pide nuevos nombres de entidad, actualiza cada tabla seleccionada, sincroniza el `SourceLineageTag` y marca los metadatos modificados.

> **Úsalo en TE3:** Selecciona las tablas Direct Lake relevantes, abre la ventana **C# Script**, pega el script y ejecútalo.

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
> El script se generó usando un LLM para Code Assist, pero el equipo de Tabular Editor lo ha probado.

Al ejecutar el script, solo se actualizan las tablas a las que se les asigna un nuevo nombre de entidad. Cuando termine el script, revisa los cambios, guarda el modelo y actualízalo en Power BI para confirmar que los metadatos se conservan.

Por último, abre cada partición actualizada y comprueba que `Name` aparece en la colección `ChangedProperties` antes de actualizar desde Power BI.