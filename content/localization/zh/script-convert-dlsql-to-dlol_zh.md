---
uid: script-convert-dlsql-to-dlol
title: 将 Direct Lake on SQL 转换为 OneLake
author: Daniel Otykier
updated: 2025-06-20
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---

# 将 Direct Lake on SQL 转换为 OneLake

## 脚本用途

此脚本将使用 Direct Lake on SQL (DL/SQL) 的模型转换为 Direct Lake on OneLake (DL/OL)。 如 [Direct Lake 指南文章](xref:direct-lake-guidance)中所述，这只需更新模型上 Direct Lake 分区使用的共享表达式上的 M 查询，以使用 [`AzureStorage.DataLake`](https://learn.microsoft.com/en-us/powerquery-m/azurestorage-datalake) 连接器替代 [`Sql.Database`](https://learn.microsoft.com/en-us/powerquery-m/sql-database) 连接器。

## 先决条件

您需要 **工作区 ID** 以及 Fabric 仓库或湖屋的**资源 ID**。 两者都是 GUID，是在 Fabric 门户中导航到仓库或湖屋时 URL 的一部分：

![Lakehouse Warehouse URL](~/content/assets/images/lakehouse-warehouse-url.png)

在上面的屏幕截图中，湖屋的**工作区 ID** 用蓝色突出显示，而**资源 ID** 用绿色突出显示。

## 脚本

### 将 Direct Lake on SQL 转换为 OneLake

```csharp
// ==================================================================
// 将 Direct Lake on SQL 转换为 OneLake
// -------------------------------------
// 
// 此脚本检测当前模型是否使用 Direct Lake on SQL
// 并建议将模型升级到 Direct Lake on OneLake。
//
// 您需要工作区 ID 和 Fabric 仓库
// 或湖屋的 ID（两者都是 GUID）。
// ==================================================================

// 查找模型上 EntityPartitions 使用的共享表达式：
using System.Windows.Forms;
using System.Drawing;

var partition = Model.AllPartitions.OfType<EntityPartition>()
    .FirstOrDefault(e => e.Mode == ModeType.DirectLake && e.ExpressionSource != null);
var expressionSource = partition == null ? null : partition.ExpressionSource;

if (expressionSource == null)
{
    Warning("您的模型似乎不包含任何 Direct Lake 模式的表。");
    return;
}

if (!expressionSource.Expression.Contains("Sql.Database"))
{
    Warning("此模型未配置为通过 SQL 的 Direct Lake。");
    return;
}

WaitFormVisible = false;
Application.UseWaitCursor = false;
var promptDialog = new UrlNameDialog();
if(promptDialog.ShowDialog() == DialogResult.Cancel) return;

const string mTemplate = @"let
    Source = AzureStorage.DataLake(""https://onelake.dfs.fabric.microsoft.com/%workspaceId%/%resourceId%"", [HierarchicalNavigation=true])
in
    Source";

expressionSource.Expression = mTemplate.Replace("%workspaceId%", promptDialog.WorkspaceId.Text).Replace("%resourceId%", promptDialog.ResourceId.Text);

if(!string.IsNullOrEmpty(Model.Collation))
{
    Model.Collation = null;
    Info("模型已成功转换为 Direct Lake on OneLake。由于修改了模型排序规则，您可能需要将其部署为新的语义模型。");
}
else
    Info("模型已成功转换为 Direct Lake on OneLake。");

// UI 代码在下面：
public class UrlNameDialog : Form
{
    public TextBox WorkspaceId { get; private set; }
    public TextBox ResourceId { get; private set; }
    private Button okButton;

    public UrlNameDialog()
    {
        Text = "将 Direct Lake on SQL 转换为 OneLake";
        AutoSize = true;
        AutoSizeMode = AutoSizeMode.GrowAndShrink;
        StartPosition = FormStartPosition.CenterParent;
        Padding = new Padding(20);

        var mainLayout = new TableLayoutPanel
        {
            ColumnCount = 1,
            RowCount = 3,
            Dock = DockStyle.Fill,
            AutoSize = true,
            AutoSizeMode = AutoSizeMode.GrowAndShrink
        };
        Controls.Add(mainLayout);

        // 工作区 ID
        mainLayout.Controls.Add(new Label { Text = "工作区 ID (GUID)：", AutoSize = true });
        WorkspaceId = new TextBox { Width = 1000 };
        mainLayout.Controls.Add(WorkspaceId);

        // 资源 ID
        mainLayout.Controls.Add(new Label { Text = "Fabric 仓库/湖屋 ID (GUID)：", AutoSize = true, Padding = new Padding(0, 20, 0, 0) });
        ResourceId = new TextBox { Width = 1000 };
        mainLayout.Controls.Add(ResourceId);

        // 按钮
        var buttonPanel = new FlowLayoutPanel
        {
            Padding = new Padding(0, 20, 0, 0),
            FlowDirection = FlowDirection.RightToLeft,
            Dock = DockStyle.Fill,
            AutoSize = true
        };

        okButton = new Button { Text = "确定", DialogResult = DialogResult.OK, AutoSize = true, Enabled = false };
        var cancelButton = new Button { Text = "取消", DialogResult = DialogResult.Cancel, AutoSize = true };
        buttonPanel.Controls.Add(okButton);
        buttonPanel.Controls.Add(cancelButton);

        AcceptButton = okButton;
        CancelButton = cancelButton;
        mainLayout.Controls.Add(buttonPanel);

        WorkspaceId.TextChanged += Validate;
        ResourceId.TextChanged += Validate;
    }
    
    private void Validate(object sender, EventArgs e)
    {
        Guid g;
        okButton.Enabled = Guid.TryParse(WorkspaceId.Text, out g) && Guid.TryParse(ResourceId.Text, out g);
    }
}
```

### 说明

脚本首先尝试查找配置为 Direct Lake 模式且具有表达式源（对共享表达式的引用）的 EntityPartition。 如果未找到这样的分区，它会显示警告消息并退出。 此外，引用的共享表达式必须指定 `Sql.Database` 连接器，这表明模型当前使用的是 Direct Lake on SQL。

脚本确认模型使用 Direct Lake on SQL 后，它会提示用户输入 Fabric 仓库或湖屋的**工作区 ID** 和**资源 ID**。 然后脚本用 `AzureStorage.DataLake` 连接器替换共享表达式中的 `Sql.Database` 连接器，并使用提供的 ID。

最后，如果模型设置了排序规则，脚本会清除它，因为此更改需要新的排序规则。 脚本然后通知用户模型已成功转换为 Direct Lake on OneLake。