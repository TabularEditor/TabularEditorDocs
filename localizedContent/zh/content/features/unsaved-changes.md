---
uid: unsaved-changes
title: 未保存的更改指示器
author: Daniel Otykier
updated: 2026-10-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# 未保存的更改指示器

Tabular Editor 3 会标记与模型上次保存的版本存在差异的对象和属性。这包括来自[C# 脚本](xref:csharp-scripts)、宏和[AI 助手](xref:ai-assistant)的更改。当您保存、还原或撤消更改时，标记将清除。

指示器出现在两个位置：

- 在[TOM 资源管理器](xref:tom-explorer-view)中，已更改的对象会显示为彩色行并带有图标徽章：橙色（已编辑）、绿色（已添加）和红色（已删除）。这些是部署时显示的模型比较视图的颜色。
- 在[属性视图](xref:properties-view)中，已更改的属性显示为浅橙色行。

![TOM Explorer 中突出显示了已编辑、已添加和已删除的度量值，并且“属性”视图中突出显示了已更改的“描述”行](~/content/assets/images/unsaved-changes/overview.png)

这两个视图均具有**显示更改**工具栏按钮和右键单击**还原**命令。

> [!NOTE]
> 这些指示器跟踪相对于模型从中加载或最后保存到的源的更改。将模型部署到其他数据库不会清除这些标记。

## TOM Explorer 中的更改指示器

树中的每个对象都根据其自上次保存以来的更改进行标记：

- **已编辑**的对象显示为浅橙色行，并带有橙色圆点徽章。这涵盖任何已修改的属性，包括对树中没有节点的子对象的更改，例如表的刷新策略或列的 `AlternateOf` 设置。
- **已添加**的对象显示为浅绿色行，并带有绿色 **+** 徽章。新表及其所有新列均为绿色。编辑已添加的对象不会将其从绿色变为橙色。
- **已删除**对象显示为浅红色行、红色 **−** 徽章和带删除线的名称。请参阅[已删除对象](#deleted-objects)。

当表格、显示文件夹、表格组和**模型**节点下方的某项内容发生变化时，它们将显示为阴影填充。当它们下方的所有更改都是添加时，它们的图标徽章为绿色，否则为橙色。

在选择范围内，选择高亮显示优先于行颜色，图标徽章仍会标记已更改的对象。错误和警告徽章的优先级高于更改徽章。

> [!TIP]
> 如果难以区分绿色和红色行，请在**工具 > 偏好 > Tabular Editor > 用户界面**下的**辅助功能**组中选择**色盲模式**。在此处和模型比较视图中，添加的对象将显示为蓝绿色，而不是绿色。

### 显示更改

TOM Explorer 工具栏上的**显示更改**按钮将树状视图筛选为具有未保存更改的对象，以及包含这些对象的表、文件夹和组。筛选器处于活动状态时，视图标题显示为**TOM Explorer（已更改）**。

![已启用“显示更改”筛选器的 TOM 资源管理器，仅列出已更改的对象及其容器](~/content/assets/images/unsaved-changes/tom-explorer-show-changes.png)

该筛选器与其他工具栏切换按钮和搜索框结合使用。例如，使用**Ctrl+2**隐藏列也会在筛选视图中隐藏已更改的列。

## 更改属性视图中的指示器

当您选择一个已更改的对象时，已更改的属性将显示在同一浅橙色行中。包含子对象的折叠行（例如度量的**KPI**行或表的**刷新策略**行）会在子对象内的任何内容发生更改时被标记。对于**注释**等索引行，仅标记已更改的注释。当选择多个对象时，如果任何所选对象更改了该属性，则会标记属性行。

“属性”视图工具栏上的**显示更改**按钮可隐藏未更改的行。筛选器处于活动状态时，视图标题显示为**属性（已更改）**。

![“属性”视图，其中“显示更改”筛选器处于活动状态，仅列出已更改的属性](~/content/assets/images/unsaved-changes/properties-show-changes.png)

## 还原更改

**文件 > 从磁盘重新加载**将放弃所有未保存的更改，并从源重新加载模型。对于从服务器打开的模型，命令为**文件 > 从服务器重新加载**。**还原**将撤消个别更改，并保留所有其他未保存的更改。

还原的运作方式类似于手动输入旧值或重新创建已删除的对象：Tabular Editor会更新DAX引用和依赖对象，并将还原作为一个步骤添加到撤消栈中。要撤消还原，请使用**编辑 > 撤消**（**Ctrl+Z**）。

### 还原单个属性

在“属性”视图中右键单击标记的行，然后选择**还原**以恢复其保存的值。对象的其他未保存的更改将保持不变。

![显示已更改的“描述”和“格式字符串”行的“属性”视图，以及右键单击“还原”命令](~/content/assets/images/unsaved-changes/revert-property.png)

**还原**仅在有未保存更改的行上启用。当选择了多个对象时，在合并行上执行**还原**操作将还原每个已更改属性的所选对象上的属性，作为一个撤消步骤。在**注释**等容器行上使用**还原**将还原其所有注释：已编辑的注释将恢复为已保存的值，已添加的注释将被移除，已删除的注释将被还原。

### 还原对象或模型分支

在 TOM Explorer 中右键单击已标记的对象，然后选择**还原**，将该对象及其下方的所有内容还原为其上次保存的状态。当表、显示文件夹、表组和**模型**节点下方的某些内容发生变化时，也可以使用**还原**。对**模型**节点执行**还原**操作将放弃模型中所有未保存的更改，作为一个撤消步骤。

![在已编辑的 Measure 上右键单击 TOM Explorer 菜单，选择“还原”](~/content/assets/images/unsaved-changes/revert-object.png)

当您还原对象或分支时：

- 已编辑的属性恢复为保存的值。
- 自上次保存以来添加的对象将被删除。
- 自上次保存以来删除的对象将按保存时的状态恢复，包括已删除度量的 KPI，或已删除列的层次结构级别和关系。
- 模型中其他位置的对象保留其未保存的更改。

如果还原操作的部分内容失败，则会显示“**还原不完整**”消息，列出失败的内容，而 Tabular Editor 会应用其余内容。例如，如果另一个对象现在使用已删除对象的名称且无法删除，则无法还原该已删除对象。

## 已删除对象

删除对象不会将其从 TOM Explorer 中移除。在您保存模型之前，该对象将保留在原位，其名称带有删除线，所在行显示为浅红色，并带有红色 **−** 徽章。显示信息列时，**对象类型**列显示的内容例如为**度量值（已删除）**。

![TOM Explorer 中红色行上带有删除线的已删除度量值](~/content/assets/images/unsaved-changes/deleted-objects.png)

右键单击已删除的对象，然后选择**还原**，将其还原为删除时的状态。如果在删除对象之前，对象有未保存的编辑内容，则这些编辑内容也会被还原并保持标记状态，您可以单独还原这些编辑内容。要一步还原多个已删除的对象，请全选这些对象，然后选择**还原**。

您无法编辑、重命名、拖动或展开已删除的对象，它也绝不会成为拖放或粘贴的目标。选择已删除对象不会选择模型对象，因此“属性”视图不显示任何内容，右键菜单中只有**还原**。同时选择了已删除对象和活动对象时，既没有**还原**命令，也没有常规对象命令。

C# 脚本通过 `Selected.Deleted` 访问选定的已删除对象，如[脚本](#scripting)中所述。

### 将已删除对象归集到一个节点下

如果你在**工具 > 偏好 > Tabular Editor > TOM Explorer**下的**未保存的更改**部分中选择**将已删除对象归集到“已删除对象”节点下**，则无论表、层次结构、角色或表组的已删除对象位于哪个显示文件夹中，它们都会在其容器的末尾列示在一个**已删除对象**节点下。该节点有一行红色和“已删除”徽章，其下的对象被删除线划掉。右键单击该节点并选择**还原**，即可一步还原其下的所有内容。

![TOM Explorer，其中一个已删除的度量值列在其表末尾的“已删除对象”节点下](~/content/assets/images/unsaved-changes/deleted-objects-group.png)

### 在多次保存中保留已删除对象

默认情况下，已删除的对象在您保存之前仍保持可见。要更改此设置，请将**保持已删除对象可见**首选项设置为其另外两个选项之一：

- **从不**：TOM Explorer 立即隐藏已删除对象。要恢复它们，请在其容器上使用**还原**，或使用**编辑 > 撤销**。
- **直到模型关闭**：在整个编辑会话（包括跨次保存）中，已删除的对象仍保持可见且可恢复，同时其删除操作仍位于撤消栈中。恢复上次保存之前已删除的对象会再次创建该对象，并将其标记为已添加。您在同一会话中创建并删除的对象仅在您编辑该对象或在其存在时保存模型的情况下才会显示。

## 指示器何时清除

标记反映了当前状态与上次保存状态的差异。将模型保存到文件、文件夹或数据库会一次性清除所有标记。当您撤销更改、撤消回上次保存的点，或手动将属性设置回其保存的值时，标记也会清除。如果您撤消到上次保存之后，被撤消的对象将被标记为已更改，而重做更改将恢复其标记。

## 偏好

指示器设置位于**工具 > 首选项 > Tabular Editor > TOM Explorer**下的**未保存的更改**部分：

![TOM Explorer首选项页面的“未保存的更改”部分](~/content/assets/images/unsaved-changes/preferences.png)

- **标记具有未保存更改的对象**（启用）：在 TOM Explorer 中为已添加、已编辑和已删除的对象的行着色，为其图标添加徽章，并为其容器添加阴影。不影响已删除对象的可见性或**显示更改**。
- **保持已删除对象可见**（直到模型保存）：已删除对象在 TOM Explorer 中保留的时间。请参阅[在多次保存之间保留已删除的对象](#keeping-deleted-objects-across-saves)。
- **将已删除对象归集到“已删除对象”节点下**（已禁用）：将容器的已删除对象列在同一个节点下。请参阅[将已删除对象归集到一个节点下](#gathering-deleted-objects-under-one-node)。
- **在属性窗格中标记具有未保存更改的属性**（已启用）：在属性视图中为已更改属性的行着色。不影响属性视图中的**显示更改**。

有关此页面上的其他设置，请参阅@preferences。

## 脚本

[C# 脚本](xref:csharp-scripts)和宏可以通过以下每个模型对象都具有的成员读取相同的更改信息并运行相同的还原操作：

- 当对象或其下任何内容与上次保存的状态不同时，`HasUnsavedChanges` 返回 `true`。在`Model`对象上，它返回模型是否有任何未保存的更改。
- `Revert()` 将对象及其子级作为一个撤消步骤进行还原。该方法也存在于 `Selected.Measures` 等集合中，以及整个模型的 `Model` 中。如果部分还原操作失败，它将抛出一个异常，列出无法还原的部分。
- `Revert("PropertyName")` 将一个属性还原为其保存的值，例如 `Revert("Expression")` 或 `Revert("Annotations[MyAnnotation]")`。当属性未变时，它不会执行任何操作。

表格、层次结构和角色等容器具有 `DeletedObjects` 集合，其中列出了当前会话中从它们中删除的对象。每个条目都有一个 `Name`、`ObjectType` 和 `Parent`，以及一个 `Restore()` 方法。集合上的 `Restore()` 会还原所有条目。

`Selected.Deleted` 返回在 TOM Explorer 中选定的已删除对象。已删除的对象不会出现在 `Selected.Measures`、`Selected.Columns` 或其他访问器中。

```csharp
// List the measures with unsaved changes in the selected tables:
Selected.Tables
    .SelectMany(t => t.Measures)
    .Where(m => m.HasUnsavedChanges)
    .Output();

// Revert only the format strings of the selected measures, keeping their other edits:
Selected.Measures.Revert("FormatString");

// Put an entire table back to its saved state:
Model.Tables["Sales"].Revert();

// Bring back everything that was deleted from the selected table:
Selected.Table.DeletedObjects.Restore();

// Restore the deleted objects currently selected in the TOM Explorer:
Selected.Deleted.Restore();
```
