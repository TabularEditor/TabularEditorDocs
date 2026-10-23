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

**元数据翻译编辑器**提供了模型中可翻译对象的已翻译名称、描述和显示文件夹的概览。您可以通过**视图**菜单启动元数据翻译编辑器。或者，如果您只需要编辑某些翻译，请在**TOM 资源管理器**中选择它们（按住 CTRL 或 SHIFT 键可进行多选），然后右键单击并选择**在元数据翻译编辑器中显示**。

![元数据翻译编辑器](~/content/assets/images/metadata-translation-editor.png)

使用元数据翻译编辑器中的输入字段，快速添加/删除或编辑对象名称、描述和显示文件夹名称的相应语言翻译。编辑器中的前三列允许您更改对象的默认名称、描述和显示文件夹名称。您可以使用通常的方式撤消 (Ctrl+Z) 和重做 (Ctrl+Y)。

要删除翻译，请清空其单元格，然后按**Enter**。清除默认的**描述**或**显示文件夹**单元格将清空该属性。无法清除默认**名称**。模型、表、层次结构级别和透视的**显示文件夹**单元格为只读。

## 元数据翻译编辑器工具栏

当元数据翻译编辑器处于活动状态时，随附的工具栏提供以下选项：

- ![元数据翻译编辑器新翻译](~/content/assets/images/metadata-translation-editor-add-translation.png) **新翻译**：此按钮将新翻译添加到模型。翻译将显示在元数据翻译编辑器中。 
- ![元数据翻译编辑器隐藏成员](~/content/assets/images/perspective-editor-hide-members.png) **显示/隐藏隐藏对象**：如果您想在元数据翻译编辑器中查看所有对象（包括隐藏对象），请启用此选项。
- ![元数据翻译编辑器隐藏名称](~/content/assets/images/metadata-translation-editor-name.png) **显示/隐藏名称**：如果您不希望在元数据翻译编辑器中看到名称翻译列，请禁用此选项。
- ![元数据翻译编辑器隐藏描述](~/content/assets/images/metadata-translation-editor-description.png) **显示/隐藏描述**：如果您不想在元数据翻译编辑器中看到描述翻译列，请禁用此选项。
- ![元数据翻译编辑器隐藏显示文件夹](~/content/assets/images/perspective-editor-folder.png) **显示/隐藏显示文件夹**：如果您不希望在元数据翻译编辑器中看到显示文件夹翻译列，请禁用此选项。

## 处理多项翻译

如果您正在处理一个具有许多翻译的模型，一次性显示所有翻译可能不切实际。您可以通过拖动列标题来重新排列元数据翻译编辑器中翻译的显示顺序，从而更轻松地并排比较翻译。此外，您可以随时通过右键单击上下文菜单，在编辑器中添加/删除翻译：

<!-- 重新截取屏幕截图 (3.27.1)：metadata-translation-editor-columns-bands.png。标题上下文菜单不再有“显示自动筛选行”。-->
![元数据翻译编辑器列](~/content/assets/images/metadata-translation-editor-columns-bands.png)