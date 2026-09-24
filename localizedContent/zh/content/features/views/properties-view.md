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

## 工具栏

属性视图顶部的工具栏包含以下按钮：

- **分类**：将属性按 _基本_、_元数据_ 和 _选项_ 等类别分组。
- **按字母顺序**：在一个按字母顺序排序的列表中显示所有属性。
- **显示更改**：隐藏自上次保存模型以来未更改的所有属性，这样就只会保留有[未保存的更改](xref:unsaved-changes)的属性。启用该筛选器时，视图标题将显示为 **属性（已更改）**。
- **属性说明**：显示或隐藏视图底部的说明窗格，用于解释当前选中的属性。
- **搜索框**：按名称筛选属性列表。

## 未保存的更改

与模型上次保存版本不同的属性，其所在行会以浅橙色背景显示。选择多个对象时，如果所选对象中有任意一个更改了该属性，对应行就会被标记。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/unsaved-changes/revert-property.png" alt="Properties view with unsaved changes" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong> 一个度量值的“说明”和“格式字符串”存在未保存的更改。<strong>还原</strong> 选项可将单个属性恢复为其已保存的值。</figcaption>
</figure>

右键单击已标记的行并选择 **还原**，即可将该属性恢复为上次保存时的值，而不会影响任何其他未保存的更改。该还原操作在撤销堆栈中只占一步，因此按 **Ctrl+Z** 即可撤销还原并恢复更改。详见 @unsaved-changes，了解如何在 TOM Explorer 中还原整个对象，以及如何在 **工具 > 偏好** 中关闭这些指示标记。

## 停靠

默认情况下，属性视图位于右下角；你也可以按键盘上的 F4 打开它。你还可以将其停靠到主窗口的任意一侧，或将其取消停靠为独立窗口。
