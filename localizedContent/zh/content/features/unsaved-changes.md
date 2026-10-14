---
uid: unsaved-changes
title: 未保存更改指示符
author: Daniel Otykier
updated: 2026-09-23
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

# 未保存更改指示符

Tabular Editor 3 会标记与模型上次保存时相比发生变化的对象和属性。这包括来自 [C# Script](xref:csharp-scripts)、宏和 [AI Assistant](xref:ai-assistant) 的更改。保存、还原或撤销更改后，标记会被清除。

这些指示器会显示在两个位置：

- 在 [TOM Explorer](xref:tom-explorer-view) 中，已更改的对象所在行会以不同颜色显示，并带有图标徽章：橙色（已编辑）、绿色（已添加）和红色（已删除）。这些颜色与部署时显示的模型比较视图中的颜色一致。
- 在 [属性视图](xref:properties-view) 中，已更改的属性所在行会显示为淡橙色。

![TOM Explorer 中已编辑、新增和已删除的度量值已高亮显示，属性视图中已更改的“说明”行也已高亮显示](~/content/assets/images/unsaved-changes/overview.png)

这两个视图都提供 **显示更改** 工具栏按钮，以及右键菜单中的 **还原** 命令。

> [!NOTE]
> 这些指示器会跟踪相对于模型的加载来源或上次保存目标所发生的更改。将模型部署到其他数据库不会清除这些标记。

## TOM Explorer 中的更改指示器

树中的每个对象都会根据其自上次保存以来的变化进行标记：

- **已编辑** 对象所在行会显示为淡橙色，并在图标上带有橙色圆点徽章。这包括任何被修改的属性，也包括在树中没有对应节点的子对象上的更改，例如表的刷新策略或列的 `AlternateOf` 设置。
- **已添加** 对象所在行会显示淡绿色背景，并带有绿色 **+** 徽标。新表及其所有新列都会显示为绿色。编辑已添加的对象不会使其从绿色变为橙色。
- **已删除** 对象所在行会显示为淡红色，并带有红色 **−** 徽章，同时其名称会显示删除线。请参见 [已删除对象](#deleted-objects)。

如果其下方的内容发生了更改，表、显示文件夹、表格组以及 **Model** 节点会显示斜线填充图案。如果其下方的所有更改都是新增，其图标徽章就是绿色；否则为橙色。

在选中状态下，选中高亮会覆盖行颜色，但图标徽章仍会标记已更改的对象。错误和警告徽章的优先级高于更改徽章。

> [!TIP]
> 如果绿色行和红色行不易区分，请在 **工具 > 偏好 > Tabular Editor > 用户界面** 下的 **辅助功能** 组中选择 **色盲模式**。此后，新增对象会以蓝绿色而非绿色标记，这里和模型比较视图中都会这样显示。

### 显示更改

TOM Explorer 工具栏上的 **显示更改** 按钮会筛选树视图，仅显示有未保存更改的对象，以及包含这些对象的表、显示文件夹和表格组。启用此筛选器时，视图标题会显示为 **TOM Explorer (Changed)**。

![TOM Explorer 启用“显示更改”筛选器，仅列出已更改的对象及其所属容器](~/content/assets/images/unsaved-changes/tom-explorer-show-changes.png)

该筛选器可与工具栏上的其他切换按钮和搜索框配合使用。例如，使用 **Ctrl+2** 隐藏列时，已更改的列也会从筛选后的视图中隐藏。

## 属性视图中的更改指示器

选择已更改的对象时，已更改的属性也会以同样的浅橙色行背景高亮显示。对于包含子对象的折叠行，例如度量值的 **KPI** 行或表的 **刷新策略** 行，只要子对象中的任何内容发生更改，该行就会被标记。对于 **注释** 这类带索引的行，仅会标记发生更改的那条注释。选择多个对象时，只要所选对象中有任意一个更改了该属性，对应的属性行就会被标记。

属性视图工具栏上的 **显示更改** 按钮会隐藏未更改的行。启用该筛选器时，视图标题将显示为 **属性（已更改）**。

![已启用“显示更改”筛选器的属性视图，仅列出已更改的属性](~/content/assets/images/unsaved-changes/properties-show-changes.png)

## 还原更改

**文件 > 从磁盘重新加载** 会丢弃所有未保存的更改，并从其源重新加载模型。对于从服务器打开的模型，该命令为 **文件 > 从服务器重新加载**。**还原** 会撤销单个更改，其他所有未保存的更改则会保留。

执行还原时，就像手动输入旧值或手动重新创建已删除对象一样：Tabular Editor 会更新 DAX 引用和依赖对象，并将这次还原作为一个步骤加入撤销堆栈。要撤销还原，使用 **编辑 > 撤销**（**Ctrl+Z**）。

### 还原单个属性

在属性视图中右键单击带标记的行，然后选择 **还原**，即可将该属性恢复为上次保存时的值。该对象的其他未保存的更改会保留不变。

![属性视图，其中“描述”和“格式字符串”行已更改，并显示右键菜单中的“还原”命令](~/content/assets/images/unsaved-changes/revert-property.png)

**还原** 仅对包含未保存更改的行可用。选中多个对象时，在合并行上执行 **还原** 会将所有选中且更改了该属性的对象一并还原，并作为一个可撤销的步骤。在 **注释** 等容器行上执行 **还原**，会一次性还原其所有注释：已编辑的注释会恢复为保存时的值，新增的注释会被移除，而已删除的注释会被恢复。

### 还原对象或模型分支

在 TOM Explorer 中右键单击带标记的对象，然后选择 **还原**，即可将该对象及其下所有内容恢复为上次保存时的状态。只要其下有内容发生更改，就可以在表、显示文件夹、表格组以及 **模型** 节点上使用 **还原**。在 **模型** 节点上执行 **还原** 会丢弃模型中所有未保存的更改，并作为一个可撤销的步骤加入撤销堆栈。

![TOM Explorer 中已修改度量值的右键菜单，其中包含“还原”](~/content/assets/images/unsaved-changes/revert-object.png)

还原对象或模型分支时：

- 已编辑的属性会恢复为保存时的值。
- 自上次保存后新增的对象会被移除。
- 自上次保存后删除的对象会恢复为保存时的状态，包括已删除度量值的 KPI，或已删除列的层次结构级别和关系。
- 模型中其他位置的对象会保留其未保存的更改。

如果还原的某些部分失败，会显示 **还原未完成** 信息，列出失败项，Tabular Editor 会继续应用其余部分。例如，如果另一个对象已经占用了它的名称且无法移除，那么该已删除对象将无法还原。

## 已删除的对象

删除对象并不会将其从 TOM Explorer 中移除。在保存模型之前，该对象会保留在原处，其名称带删除线，所在行显示为浅红色，并带有红色 **−** 标记。显示信息列时，**对象类型**列中会显示例如 **度量值（已删除）** 这样的内容。

![TOM Explorer 中，已删除的度量值所在行显示为红色，名称带有删除线](~/content/assets/images/unsaved-changes/deleted-objects.png)

右键单击已删除的对象并选择 **还原**，即可将其恢复到删除前一刻的状态。如果对象在删除前有尚未保存的编辑，这些编辑也会一并恢复并继续保留标记，方便你单独撤销。要一步还原多个已删除对象，请将它们全部选中，然后选择 **还原**。

你不能编辑、重命名、拖动或展开已删除的对象，它也不能作为拖放或粘贴的目标。选择已删除的对象并不会选中模型对象，因此属性视图不会显示任何内容，右键菜单中也只有 **还原**。如果所选内容同时包含已删除对象和现有对象，则既不会提供 **还原**，也不会提供常规对象命令。

如 [脚本](#scripting) 中所述，C# Script 可通过 `Selected.Deleted` 访问所选的已删除对象。

### 将已删除对象集中到一个节点下

如果你在 **工具 > 偏好 > Tabular Editor > TOM Explorer** 下的 **未保存的更改** 部分选择 **将已删除对象收集到“已删除对象”节点下**，则表、层次结构、角色或表格组中的已删除对象会集中列在其容器末尾的同一个 **已删除对象** 节点下，而不管它们原先位于哪个显示文件夹中。该节点所在行会显示为红色，并带有删除标记；其下对象的名称会带有删除线。右键单击该节点并选择 **还原**，即可一步恢复其下的所有内容。

![TOM Explorer，其中已删除的度量值列在其表末尾的“已删除对象”节点下](~/content/assets/images/unsaved-changes/deleted-objects-group.png)

### 保存后仍保留已删除对象

默认情况下，已删除对象在保存前会一直保持可见。如需更改，请将 **保留已删除对象可见** 这一偏好设置为另外两个选项之一：

- **从不**：TOM Explorer 会立即隐藏已删除对象。要恢复它们，请在其容器上使用 **Revert**，或选择 **编辑 > 撤销**。
- **在模型关闭之前**：已删除对象在整个编辑会话期间都会保持可见并可还原，即使跨越多次保存也一样，只要其删除操作仍在撤销堆栈中。还原在上次保存前删除的对象时，会重新创建该对象，并将其标记为新增对象。在同一会话中创建又删除的对象，只有在其存在期间你编辑过它，或保存过模型时，才会显示出来。

## 指示标记何时会清除

标记反映的是当前状态与上次保存的状态之间的差异。将模型保存到文件、文件夹或数据库时，会一次性清除所有标记。标记也会在以下情况下清除：还原该更改、撤销到上次保存时的状态，或手动将属性设回其已保存的值。如果你撤销到了上次保存点之前，被撤销的对象会被标记为已更改；重新执行更改会恢复其标记。

## 偏好设置

相关指示器设置位于 **工具 > 偏好 > Tabular Editor > TOM Explorer** 下的 **未保存的更改** 部分：

![TOM Explorer 偏好设置页面中的“未保存的更改”部分](~/content/assets/images/unsaved-changes/preferences.png)

- **标记有未保存更改的对象**（已启用）：在 TOM Explorer 中为新增、已编辑和已删除对象的行着色，并为其图标添加角标，还会为其容器添加斜线填充。不影响已删除对象的可见性，也不影响 **显示更改**。
- **保持已删除对象可见**（直到模型保存）：控制已删除对象在 TOM Explorer 中保留可见的时长。请参阅[跨保存保留已删除对象](#keeping-deleted-objects-across-saves)。
- **将已删除对象集中到“已删除对象”节点下**（已禁用）：将容器中已删除的对象统一列在一个节点下。请参阅[将已删除对象集中到一个节点下](#gathering-deleted-objects-under-one-node)。
- **在“属性”窗格中标记有未保存更改的属性**（已启用）：在属性视图中对已更改属性的行着色。不影响属性视图中的 **显示更改**。

本页的其他设置请参见 @preferences。

## 脚本

[C# Script](xref:csharp-scripts) 和宏可以通过每个模型对象都具备的以下成员读取相同的更改信息，并执行相同的还原操作：

- 当该对象或其下任何内容与上次保存的状态不同时，`HasUnsavedChanges` 返回 `true`。在 `Model` 对象上，它会返回模型是否有任何未保存的更改。
- `Revert()` 会将该对象及其子对象作为一次撤销操作还原。该方法也存在于 `Selected.Measures` 等集合中，也存在于整个模型的 `Model` 上。如果部分还原失败，它会引发一个异常，其中列出无法还原的部分。
- `Revert("PropertyName")` 会将单个属性恢复为其已保存的值，例如 `Revert("Expression")` 或 `Revert("Annotations[MyAnnotation]")`。如果该属性未更改，它不会执行任何操作。

表、层次结构和角色等容器会提供一个 `DeletedObjects` 集合，其中列出当前会话中从该容器删除的对象。每个条目都有 `Name`、`ObjectType` 和 `Parent`，以及一个 `Restore()` 方法。在该集合上调用 `Restore()` 会还原其中的所有条目。

`Selected.Deleted` 返回在 TOM Explorer 中选中的已删除对象。已删除的对象不会出现在 `Selected.Measures`、`Selected.Columns` 或其他访问器中。

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
