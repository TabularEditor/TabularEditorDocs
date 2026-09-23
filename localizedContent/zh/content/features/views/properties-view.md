---
uid: properties-view
title: 属性视图
author: Daniel Otykier
updated: 2026-09-16
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 在 Tabular Editor 中使用属性网格

Tabular Editor 中的属性视图可让你检查并修改表格模型中任何对象的属性。在 TOM Explorer 中选择一个对象即可访问属性视图。随后你会看到与所选对象类型相关的属性列表，例如名称、说明、数据类型、格式字符串等。你还可以访问在 Visual Studio 或 Power BI Desktop 等其他工具中不可用的高级属性。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/properties-view.png" alt="Properties View" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong>表的属性示例。每个对象会因其类型不同而具有不同的属性 </figcaption>
</figure>

属性视图可帮助你：

- 查看并修改模型中任何对象的属性，例如表、列、度量值、层次结构、关系、分区、角色和透视。
- 使用搜索框以及视图顶部的按钮，按名称或类别筛选和排序属性。
- 使用 Ctrl+C 和 Ctrl+V 快捷键在不同对象之间复制和粘贴属性值。
- 使用 Ctrl+Z 和 Ctrl+Y 快捷键撤销和重做属性更改。
- 你可以使用键盘快捷键快速导航并编辑属性。例如，你可以按 Ctrl+Up 或 Ctrl+Down 在不同属性之间移动；按 Enter 或 F2 编辑属性值；按 Esc 取消编辑；按 Ctrl+S 保存更改；

> [!TIP]
> 你可以多选对象，以查看它们共有的属性，并进行批量编辑。例如，这对于设置格式字符串很有用。

## Toolbar

The toolbar at the top of the Properties view contains the following buttons:

- **Categorized**: Groups the properties into categories such as _Basic_, _Metadata_ and _Options_.
- **Alphabetical**: Lists all properties in a single, alphabetically sorted list.
- **Show changes**: Hides all properties that have not changed since the model was last saved, so that only the properties with [unsaved changes](xref:unsaved-changes) remain. While the filter is active, the title of the view reads **Properties (Changed)**.
- **Property descriptions**: Shows or hides the description pane at the bottom of the view, which explains the currently selected property.
- **Search box**: Filters the list of properties by name.

## Unsaved changes

Properties that differ from the last saved version of the model are drawn with a light orange row background. When several objects are selected, a row is marked if any of the selected objects changed that property.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/unsaved-changes/revert-property.png" alt="Properties view with unsaved changes" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 2:</strong> A measure with unsaved changes to its Description and Format String. The <strong>Revert</strong> option puts a single property back to its saved value.</figcaption>
</figure>

Right-click a marked row and choose **Revert** to put that property back to the value it had at the last save, without touching any other unsaved changes. The revert is a single step on the undo stack, so **Ctrl+Z** brings the change back. See @unsaved-changes for details, including how to revert whole objects from the TOM Explorer, and how to turn the indicators off under **Tools > Preferences**.

## Docking

默认情况下，属性视图位于右下角；你也可以按键盘上的 F4 打开它。你还可以将其停靠到主窗口的任意一侧，或将其取消停靠为独立窗口。
