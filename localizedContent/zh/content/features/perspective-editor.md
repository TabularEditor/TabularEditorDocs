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

**透视编辑器**可快速概览模型中各对象（表、列、层次结构和度量值）的透视分配情况。 你可以通过 **视图** 菜单启动透视编辑器。 或者，如果你只需要编辑某些透视，可在 **TOM Explorer** 中选中它们（按住 CTRL 或 SHIFT 进行多选），然后右键选择 **在透视编辑器中显示**。

![透视编辑器](~/content/assets/images/perspective-editor.png)

使用透视编辑器中的复选框，可快速将多个对象添加到透视中或从透视中移除。 你可以按常规方式使用撤销 (Ctrl+Z) 和重做 (Ctrl+Y)。 注意：通过透视编辑器所做的更改会立即应用到 TOM 中，但你仍需要保存 (Ctrl+S) 或部署模型，才能使更改在 Analysis Services / Power BI 中生效。

## 透视编辑器工具栏

打开透视编辑器时，随附的工具栏提供以下选项：

- ![Perspective Editor Add Perspective](~/content/assets/images/perspective-editor-add-perspective.png) **新建透视**：此按钮会向模型添加一个新的透视。 该透视将显示在透视编辑器中。
- ![Perspective Editor Hide Members](~/content/assets/images/perspective-editor-hide-members.png) **显示/隐藏隐藏选项**：如果你想在透视编辑器中查看包括隐藏对象在内的所有对象，请启用此选项。
- ![Perspective Editor Folder](~/content/assets/images/perspective-editor-folder.png) **显示/隐藏显示文件夹**：如果你希望透视编辑器按显示文件夹对表对象（度量值、层次结构、列）进行分组，请启用此切换按钮。

## 使用多个透视

如果你正在处理一个包含多个透视的模型，一次性显示所有透视可能并不太可行。 你可以在透视编辑器中通过拖动列标题来重新排列透视的显示顺序，从而更方便地将不同透视并排对比。 此外，你还可以随时通过右键快捷菜单在编辑器中添加或移除透视：

![透视编辑器列](~/content/assets/images/perspective-editor-columns.png)