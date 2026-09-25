---
uid: metadata-translation-editor
title: 元数据翻译编辑器
author: Šarūnas Jučius
updated: 2023-04-18
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

# 元数据翻译编辑器

**元数据翻译编辑器**可概览模型中可翻译对象的名称、说明和显示文件夹的翻译内容。 You can launch the Metadata Translation Editor through the **View** menu. Alternatively, if you only need to edit certain translations, select them in the **TOM Explorer** (hold down CTRL or SHIFT to multi-select), then right-click and choose **Show in metadata translation editor**.

![元数据翻译编辑器](~/content/assets/images/metadata-translation-editor.png)

使用元数据翻译编辑器中的输入字段，可以快速为相应语言添加、删除或编辑对象名称、说明和显示文件夹名称的翻译。 The first three columns in the editor allow you to change the default names, descriptions and display folder names of objects. You can use Undo (Ctrl+Z) and Redo (Ctrl+Y) the usual way.

## 元数据翻译编辑器工具栏

在元数据翻译编辑器处于活动状态时，工具栏提供以下选项：

- ![Metadata Translation Editor New Translation](~/content/assets/images/metadata-translation-editor-add-translation.png) **新建翻译**：点击此按钮可向模型中添加一条新翻译。 The translation will be displayed in the Metadata Translation Editor.
- ![Metadata Translation Editor Hide Members](~/content/assets/images/perspective-editor-hide-members.png) **显示/隐藏已隐藏对象**：如果你想在元数据翻译编辑器中查看所有对象，包括隐藏对象，请启用此选项。
- ![Metadata Translation Editor Hide Names](~/content/assets/images/metadata-translation-editor-name.png) **显示/隐藏名称**：如果你不想在元数据翻译编辑器中看到名称翻译列，就关闭此选项。
- ![Metadata Translation Editor Hide Descriptions](~/content/assets/images/metadata-translation-editor-description.png) **显示/隐藏说明**：如果你不想在元数据翻译编辑器中看到说明翻译列，就关闭此选项
- ![Metadata Translation Editor Hide Display Folders](~/content/assets/images/perspective-editor-folder.png) **显示/隐藏显示文件夹**：如果你不想在元数据翻译编辑器中看到显示文件夹翻译列，就关闭此选项

## 处理大量翻译

如果你正在处理包含大量翻译的模型，一次性显示所有翻译可能并不现实。 You can rearrange the display order of translations in the Metadata Translation Editor, by dragging the column headers around, making it easier to compare translations side-by-side. Moreover, you can add/remove translations from the editor at any time, through the right-click context menu:

![元数据翻译编辑器列](~/content/assets/images/metadata-translation-editor-columns-bands.png)