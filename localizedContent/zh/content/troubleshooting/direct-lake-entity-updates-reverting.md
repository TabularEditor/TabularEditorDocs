---
uid: direct-lake-entity-updates-reverting
title: Direct Lake 模型中的实体名称更改会被还原
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

# Direct Lake 模型中的实体名称更改会被还原

在 Tabular Editor 3 中编辑 Direct Lake 表分区的 `EntityName` 后，模型在 Power BI 中重新加载时可能会恢复为原始名称。 这种现象常常看起来像是 TE3 没有保存更改，但根因是 Power BI 在刷新期间解析 Direct Lake 元数据的方式。

---

## 症状

- 表的元数据更改在 TE3 中可见，但在 Power BI 中刷新模型后会被还原。
- 被还原的是 Direct Lake 表，这些表的元数据是在 Power BI 之外修改的。
- 刷新操作不会报出明确错误，但已重命名的对象会恢复为原始名称。

---

## 根本原因

Power BI 通过 `SourceLineageTag` 属性将 Direct Lake 表与其来源绑定。 当该标记与当前分区的 `EntityName` 不匹配时，Power BI 会认为表应与原始源保持同步，并恢复之前的元数据。 Direct Lake 分区还要求通过 `ChangedProperties` 集合记录有意的更改；否则，Power BI 会忽略在 Power BI 服务之外进行的手动编辑。

---

## 解决步骤

1. **打开表分区。** 对于每个 Direct Lake 表，编辑关联的 `EntityName`。
2. **同步分区详细信息。**
   - 将表的 `SourceLineageTag` 设置为与新的 `EntityName` 完全一致。
   - 在表的 `ChangedProperties` 集合中将 `Name` 属性设置为 true，以便 Power BI 将重命名视为有意更改。
3. **在 TE3 中保存模型。**
4. **在 Power BI 中刷新受影响的表（或整个模型）。**
   这些名称现在应能保持不变。

---

## 重要说明

- 重命名表时，TE3 不会自动更新 `SourceLineageTag`。 务必手动对齐该标记。
- 只有 Direct Lake 表（以及其他复合表）才需要 `ChangedProperties` 标志；传统的导入模式模型不需要它。
- 这些行为源自 Power BI 的元数据同步规则，而不是 TE3 的存储机制。

## 使用 C# 自动化批量更新

需要调整多个 Direct Lake 表时，可以运行以下 TE3 脚本。 它会提示输入新的实体名称，更新每个选中的表，同步 `SourceLineageTag`，并标记已更改的元数据。

> **在 TE3 中使用：** 选择相关的 Direct Lake 表，打开 **C# Script** 窗口，粘贴脚本并运行。

```csharp
// -------- 命名空间 --------
using System;
using System.Linq;
using System.Collections.Generic;
using System.ComponentModel;
using System.Windows.Forms;
using TW = TabularEditor.TOMWrapper;

// -------- 检查：需要先选中表 --------
var tables = Selected.Tables.ToList();
if (tables.Count == 0)
{
    Warning("先选择一个或多个表。");
    return;
}

// -------- 从所选表构建可编辑的行 --------
var candidates = tables
    .Select(table => new { Table = table, Partition = table.Partitions.OfType<TW.EntityPartition>().FirstOrDefault() })
    .ToList();

foreach (var skipped in candidates.Where(c => c.Partition == null))
{
    Warning($"跳过 '{skipped.Table.Name}'：没有 Entity 分区。");
}

var rows = new BindingList<EntityEditRow>(
    candidates
        .Where(c => c.Partition != null)
        .Select(c => new EntityEditRow(c.Table, c.Partition))
        .ToList());

if (rows.Count == 0)
{
    Warning("所选表中没有任何表包含 Entity 分区。无可编辑内容。");
    return;
}

// -------- 显示批量对话框 --------
using (var dialog = new BatchEntityEditor(rows))
{
    if (dialog.ShowDialog() != DialogResult.OK)
    {
        Info("已取消。未应用任何更改。");
        return;
    }
}

// -------- 应用更改 --------
const string ExtendedPropertyName = "Changed Property Name";
var updated = 0;

foreach (var row in rows)
{
    try
    {
        if (!row.ApplyChanges(ExtendedPropertyName, Warning))
            continue;

        updated++;
        Output($"已更新 '{row.TableName}'：Entity='{row.CurrentEntity}'，分区='{row.Partition.Name}'，SourceLineageTag='{row.CurrentEntity}'。");
    }
    catch (Exception ex)
    {
        Error($"处理 '{row.TableName}' 失败：{ex.Message}");
    }
}

Info($"完成。{updated} 个表(s)已更新。");


// ====================== 支持类型 / UI ======================
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
                warn?.Invoke($"已跳过分区重命名：表 '{TableName}' 中另一个分区已命名为 '{target}'。");
            }
            else
            {
                try
                {
                    Partition.Name = target;
                }
                catch (Exception ex)
                {
                    warn?.Invoke($"表 '{TableName}' 的分区重命名失败：{ex.Message}");
                }
            }
        }

        try
        {
            Table.SourceLineageTag = target;
        }
        catch (Exception ex)
        {
            warn?.Invoke($"未在 '{TableName}' 上设置 SourceLineageTag：{ex.Message}");
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
        Text = "编辑所选表的 Entity 名称";
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
            Text = "为每个表编辑 Entity 名称。保持“New Entity”不变即可跳过。",
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
                HeaderText = "表",
                ReadOnly = true,
                FillWeight = 28
            },
            new DataGridViewTextBoxColumn
            {
                DataPropertyName = nameof(EntityEditRow.CurrentEntity),
                HeaderText = "当前 Entity",
                ReadOnly = true,
                FillWeight = 36
            },
            new DataGridViewTextBoxColumn
            {
                DataPropertyName = nameof(EntityEditRow.NewEntity),
                HeaderText = "新 Entity",
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

        var ok = new Button { Text = "确定", DialogResult = DialogResult.OK, AutoSize = true, Height = 32, Width = 110, Margin = new Padding(8, 8, 0, 8) };
        var cancel = new Button { Text = "取消", DialogResult = DialogResult.Cancel, AutoSize = true, Height = 32, Width = 110, Margin = new Padding(8, 8, 8, 8) };

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
> 该脚本使用 LLM 进行 Code Assist 生成，但已由 Tabular Editor 团队测试。

运行该脚本只会更新那些被设置了新实体名称的表。 脚本运行结束后，检查更改、保存模型，并在 Power BI 中刷新，以确认元数据能够持久保留。

最后，在从 Power BI 刷新之前，打开每个已更新的分区，并验证 `ChangedProperties` 集合中包含 `Name`。