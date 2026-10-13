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

Tabular Editor 3 marks objects and properties that differ from the last saved version of the model. This includes changes from [C# scripts](xref:csharp-scripts), macros and the [AI Assistant](xref:ai-assistant). A mark clears when you save, revert or undo the change.

这些指示器会显示在两个位置：

- In the [TOM Explorer](xref:tom-explorer-view), changed objects get a colored row and an icon badge: orange (edited), green (added) and red (deleted). These are the colors of the model comparison view shown when deploying.
- In the [Properties view](xref:properties-view), changed properties get a light orange row.

![TOM Explorer with edited, added and deleted measures highlighted, and the Properties view with the changed Description row highlighted](~/content/assets/images/unsaved-changes/overview.png)

Both views have a **Show changes** toolbar button and a right-click **Revert** command.

> [!NOTE]
> 这些指示器会跟踪相对于模型的加载来源或上次保存目标所发生的更改。 Deploying the model to a different database doesn't clear them.

## TOM Explorer 中的更改指示器

Each object in the tree is marked according to its change since the last save:

- **Edited** objects get a light orange row and an orange dot badge. This covers any modified property, including changes to a sub-object that has no node in the tree, such as a table's refresh policy or a column's `AlternateOf` settings.
- **已添加** 对象所在行会显示淡绿色背景，并带有绿色 **+** 徽标。 A new table and all its new columns are green. Editing an added object doesn't change it from green to orange.
- **Deleted** objects get a light red row, a red **−** badge and a struck-through name. See [Deleted objects](#deleted-objects).

Tables, display folders, table groups and the **Model** node get a hatched fill when something beneath them has changed. Their icon badge is green when everything changed beneath them is an addition, and orange otherwise.

Within a selection, the selection highlight takes precedence over the row color and the icon badge still marks changed objects. Error and warning badges take precedence over the change badge.

> [!TIP]
> If green and red rows are hard to tell apart, select **Color blindness mode** in the **Accessibility** group under **Tools > Preferences > Tabular Editor > User Interface**. Added objects are then teal instead of green, both here and in the model comparison view.

### 显示更改

The **Show changes** button on the TOM Explorer toolbar filters the tree to objects with unsaved changes, plus the tables, folders and groups that contain them. While the filter is active, the view title reads **TOM Explorer (Changed)**.

![TOM Explorer with the Show changes filter active, listing only changed objects and their containers](~/content/assets/images/unsaved-changes/tom-explorer-show-changes.png)

The filter combines with the other toolbar toggles and the search box. 例如，使用 **Ctrl+2** 隐藏列时，已更改的列也会从筛选后的视图中隐藏。

## 属性视图中的更改指示器

When you select a changed object, the changed properties get the same light orange row. 对于包含子对象的折叠行，例如度量值的 **KPI** 行或表的 **刷新策略** 行，只要子对象中的任何内容发生更改，该行就会被标记。 For indexed rows such as **Annotations**, only the changed annotation is marked. 选择多个对象时，只要所选对象中有任意一个更改了该属性，对应的属性行就会被标记。

The **Show changes** button on the Properties view toolbar hides unchanged rows. While the filter is active, the view title reads **Properties (Changed)**.

![Properties view with the Show changes filter active, listing only changed properties](~/content/assets/images/unsaved-changes/properties-show-changes.png)

## 还原更改

**File > Reload from disk** discards all unsaved changes and reloads the model from its source. For a model opened from a server, the command is **File > Reload from server**. **Revert** undoes individual changes and leaves all other unsaved changes in place.

A revert works like entering the old value or recreating the deleted object by hand: Tabular Editor updates DAX references and dependent objects, and adds the revert to the undo stack as one step. To undo a revert, use **Edit > Undo** (**Ctrl+Z**).

### 还原单个属性

Right-click a marked row in the Properties view and choose **Revert** to restore its saved value. The object's other unsaved changes stay in place.

![Properties view with changed Description and Format String rows and the right-click Revert command](~/content/assets/images/unsaved-changes/revert-property.png)

**Revert** is enabled only on rows with unsaved changes. With several objects selected, **Revert** on a merged row reverts the property on every selected object that changed it, as one undo step. **Revert** on a container row such as **Annotations** reverts all its annotations: edited annotations return to their saved values, added annotations are removed and deleted annotations are restored.

### 还原对象或模型分支

Right-click a marked object in the TOM Explorer and choose **Revert** to return the object and everything beneath it to its last saved state. **Revert** is also available on tables, display folders, table groups and the **Model** node when something beneath them has changed. **Revert** on the **Model** node discards all unsaved changes in the model, as one undo step.

![TOM Explorer right-click menu on an edited measure with Revert](~/content/assets/images/unsaved-changes/revert-object.png)

When you revert an object or a branch:

- 已编辑的属性会恢复为保存时的值。
- 自上次保存后新增的对象会被移除。
- Objects deleted since the last save are restored as saved, including a deleted measure's KPI, or a deleted column's hierarchy levels and relationships.
- 模型中其他位置的对象会保留其未保存的更改。

If part of a revert fails, a **Revert incomplete** message lists the failures and Tabular Editor applies the rest. For example, a deleted object can't be restored if another object now uses its name and can't be removed.

## 已删除的对象

Deleting an object doesn't remove it from the TOM Explorer. Until you save the model, the object stays in its place with a struck-through name, a light red row and a red **−** badge. When the info columns are shown, the **Object Type** column reads, for example, **Measure (Deleted)**.

![TOM Explorer with a deleted measure struck through on a red row](~/content/assets/images/unsaved-changes/deleted-objects.png)

Right-click a deleted object and choose **Restore** to restore it as it was when you deleted it. If the object had unsaved edits before you deleted it, the edits are restored too and stay marked, and you can revert them separately. To restore several deleted objects in one step, select them all and choose **Restore**.

You can't edit, rename, drag or expand a deleted object, and it's never a drop or paste target. Selecting a deleted object doesn't select a model object, so the Properties view shows nothing and the right-click menu has only **Restore**. A selection that mixes deleted and live objects has neither **Restore** nor the normal object commands.

C# scripts access the selected deleted objects through `Selected.Deleted`, as described in [Scripting](#scripting).

### 将已删除对象集中到一个节点下

If you select **Gather deleted objects under a "Deleted objects" node** in the **Unsaved changes** section under **Tools > Preferences > Tabular Editor > TOM Explorer**, the deleted objects of a table, hierarchy, role or table group are listed under one **Deleted objects** node at the end of their container, whichever display folders they were in. The node has a red row and a deleted badge, and the objects beneath it are struck through. Right-click the node and choose **Restore** to restore everything beneath it in one step.

![TOM Explorer with a deleted measure listed under a Deleted objects node at the end of its table](~/content/assets/images/unsaved-changes/deleted-objects-group.png)

### 保存后仍保留已删除对象

By default, deleted objects stay visible until you save. To change that, set the **Keep deleted objects visible** preference to one of its two other options:

- **Never**: The TOM Explorer hides deleted objects immediately. To restore them, use **Revert** on their container, or **Edit > Undo**.
- **Until the model is closed**: Deleted objects stay visible and restorable for the whole editing session, including across saves, while their deletion is still on the undo stack. Restoring an object deleted before the last save creates it again, and it's marked as added. An object you created and deleted in the same session appears only if you edited it or saved the model while it existed.

## 指示标记何时会清除

A mark reflects the current difference from the last saved state. Saving the model to a file, a folder or a database clears every mark at once. A mark also clears when you revert the change, when you undo back to the point of the last save, or when you set a property back to its saved value by hand. If you undo past the last save, the undone objects are marked as changed, and redoing a change restores its mark.

## 偏好设置

The indicator settings are in the **Unsaved changes** section under **Tools > Preferences > Tabular Editor > TOM Explorer**:

![Unsaved changes section of the TOM Explorer preferences page](~/content/assets/images/unsaved-changes/preferences.png)

- **Mark objects with unsaved changes** (enabled): Colors the rows and badges the icons of added, edited and deleted objects in the TOM Explorer, and hatches their containers. Doesn't affect deleted-object visibility or **Show changes**.
- **保持已删除对象可见**（直到模型保存）：控制已删除对象在 TOM Explorer 中保留可见的时长。请参阅[跨保存保留已删除对象](#keeping-deleted-objects-across-saves)。
- **Gather deleted objects under a "Deleted objects" node** (disabled): Lists a container's deleted objects under one node. 请参阅[将已删除对象集中到一个节点下](#gathering-deleted-objects-under-one-node)。
- **Mark properties with unsaved changes in the Properties pane** (enabled): Colors the rows of changed properties in the Properties view. Doesn't affect **Show changes** in the Properties view.

本页的其他设置请参见 @preferences。

## 脚本

[C# scripts](xref:csharp-scripts) and macros can read the same change information and run the same revert operations through these members, which every model object has:

- 当该对象或其下任何内容与上次保存的状态不同时，`HasUnsavedChanges` 返回 `true`。 On the `Model` object, it returns whether the model has any unsaved changes.
- `Revert()` reverts the object and its children as one undo step. The method also exists on collections such as `Selected.Measures`, and on `Model` for the whole model. If part of the revert fails, it throws an exception that lists the parts it couldn't revert.
- `Revert("PropertyName")` reverts one property to its saved value, for example `Revert("Expression")` or `Revert("Annotations[MyAnnotation]")`. 如果该属性未更改，它不会执行任何操作。

Containers such as tables, hierarchies and roles have a `DeletedObjects` collection that lists the objects deleted from them in the current session. 每个条目都有 `Name`、`ObjectType` 和 `Parent`，以及一个 `Restore()` 方法。 `Restore()` on the collection restores all entries.

`Selected.Deleted` returns the deleted objects selected in the TOM Explorer. Deleted objects don't appear in `Selected.Measures`, `Selected.Columns` or the other accessors.

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
