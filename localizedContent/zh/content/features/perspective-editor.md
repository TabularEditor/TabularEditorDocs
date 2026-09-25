---
uid: perspective-editor
title: 透视编辑器
author: Šarūnas Jučius
updated: 2022-03-16
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 透视编辑器

> [!NOTE]
> 若要为在 SSAS 或 Azure AS 上运行的模型添加透视，需要 Tabular Editor 3 企业版许可证。

The **Perspective Editor** provides a quick overview of the perspective assignment of objects in the model (tables, columns, hierarchies and measures). You can launch the Perspective Editor through the **View** menu. Alternatively, if you only need to edit certain perspectives, select them in the **TOM Explorer** (hold down CTRL or SHIFT to multi-select), then right-click and choose **Show in Perspective Editor**.

![透视编辑器](~/content/assets/images/perspective-editor.png)

Use the checkboxes in the perspective editor to quickly add/remove multiple objects from a perspective. You can use Undo (Ctrl+Z) and Redo (Ctrl+Y) the usual way. Note that the changes made through the perspective editor are immediately applied to the TOM, although you will still have to save (Ctrl+S) or deploy your model for the changes to apply in Analysis Services / Power BI.

## 透视编辑器工具栏

打开透视编辑器时，随附的工具栏提供以下选项：

- ![Perspective Editor Add Perspective](~/content/assets/images/perspective-editor-add-perspective.png) **新建透视**：此按钮会向模型添加一个新的透视。 The perspective will be displayed in the Perspective Editor.
- ![Perspective Editor Hide Members](~/content/assets/images/perspective-editor-hide-members.png) **显示/隐藏隐藏选项**：如果你想在透视编辑器中查看包括隐藏对象在内的所有对象，请启用此选项。
- ![Perspective Editor Folder](~/content/assets/images/perspective-editor-folder.png) **显示/隐藏显示文件夹**：如果你希望透视编辑器按显示文件夹对表对象（度量值、层次结构、列）进行分组，请启用此切换按钮。

## 使用多个透视

If you're working on a model with many perspectives, it may be impractical to display all of them at once. You can rearrange the display order of perspectives in the Perspective Editor, by dragging the column headers around, making it easier to compare perspectives side-by-side. Moreover, you can add/remove perspectives from the editor at any time, through the right-click context menu:

![透视编辑器列](~/content/assets/images/perspective-editor-columns.png)