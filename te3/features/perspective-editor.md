---
uid: perspective-editor
title: Perspective Editor
author: Šarūnas Jučius
updated: 2022-02-03
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Perspective Editor

> [!NOTE]
> The Perspective Editor was introduced in version 3.4.1. Information in this article is subject to change.

> [!NOTE]
> In order to add perspectives to models running on SSAS or Azure AS, you will need a Tabular Editor 3 Enterprise Edition license.

The **Perspective Editor** provides a quick overview of the perspective assignment of objects in the model (tables, columns, hierarchies and measures). You can launch the Perspective Editor through the **View** menu. Alternatively, if you only need to edit certain perspectives, select them in the **TOM Explorer** (hold down CTRL or SHIFT to multi-select), then right-click and choose **Show in Perspective Editor**.

![Perspective Editor](../../images/perspective-editor.png)

Use the checkboxes in the perspective editor to quickly add/remove multiple objects from a perspective. You can use Undo (Ctrl+Z) and Redo (Ctrl+Y) the usual way. Note that the changes made through the perspective editor are immediately applied to the TOM, although you will still have to save (Ctrl+S) or deploy your model for the changes to apply in Analysis Services / Power BI.