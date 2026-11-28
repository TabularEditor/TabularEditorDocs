---
uid: metadata-translation-editor
title: 元数据翻译编辑器
author: Morten Lønskov
updated: 2026-10-11
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

**元数据翻译编辑器**可概览模型中可翻译对象的名称、说明和显示文件夹的翻译内容。你可以通过 **视图** 菜单启动元数据翻译编辑器。另外，如果你只需要编辑部分翻译，请在 **TOM Explorer** 中选中它们（按住 CTRL 或 SHIFT 可多选），然后右键单击并选择 **在元数据翻译编辑器中显示**。

![元数据翻译编辑器](~/content/assets/images/metadata-translation-editor.png)

使用元数据翻译编辑器中的输入字段，可以快速为相应语言添加、删除或编辑对象名称、说明和显示文件夹名称的翻译。编辑器中的前三列允许你更改对象的默认名称、说明和显示文件夹名称。你可以像平常一样使用撤销（Ctrl+Z）和重做（Ctrl+Y）。

要删除翻译，请清空其单元格，然后按**Enter**。清除默认的**描述**或**显示文件夹**单元格将清空该属性。无法清除默认**名称**。模型、表、层次结构级别和透视的**显示文件夹**单元格为只读。

## 元数据翻译编辑器工具栏

在元数据翻译编辑器处于活动状态时，工具栏提供以下选项：

- ![元数据翻译编辑器新建翻译](~/content/assets/images/metadata-translation-editor-add-translation.png) **新建翻译**：此按钮用于向模型添加新翻译。翻译将显示在元数据翻译编辑器中。 
- ![Metadata Translation Editor Hide Members](~/content/assets/images/perspective-editor-hide-members.png) **显示/隐藏已隐藏对象**：如果你想在元数据翻译编辑器中查看所有对象，包括隐藏对象，请启用此选项。
- ![Metadata Translation Editor Hide Names](~/content/assets/images/metadata-translation-editor-name.png) **显示/隐藏名称**：如果你不想在元数据翻译编辑器中看到名称翻译列，就关闭此选项。
- ![Metadata Translation Editor Hide Descriptions](~/content/assets/images/metadata-translation-editor-description.png) **显示/隐藏说明**：如果你不想在元数据翻译编辑器中看到说明翻译列，就关闭此选项
- ![Metadata Translation Editor Hide Display Folders](~/content/assets/images/perspective-editor-folder.png) **显示/隐藏显示文件夹**：如果你不想在元数据翻译编辑器中看到显示文件夹翻译列，就关闭此选项

## 处理大量翻译

如果你正在处理包含大量翻译的模型，一次性显示所有翻译可能并不现实。在元数据翻译编辑器中，你可以通过拖动列标题来调整翻译的显示顺序，更方便并排对照翻译内容。此外，你可以随时通过右键上下文菜单在编辑器中添加或删除翻译：

<!-- SCREENSHOT RESHOOT (3.27.1): metadata-translation-editor-columns-bands.png. The header context menu no longer has Show Auto Filter Row. -->
![元数据翻译编辑器列](~/content/assets/images/metadata-translation-editor-columns-bands.png)