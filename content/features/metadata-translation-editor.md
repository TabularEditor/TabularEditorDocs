---
uid: metadata-translation-editor
title: Metadata Translation Editor
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
# Metadata Translation Editor

The **Metadata Translation Editor** provides an overview of the translated names, descriptions and display folders of translatable objects in the model. You can launch the Metadata Translation Editor through the **View** menu. Alternatively, if you only need to edit certain translations, select them in the **TOM Explorer** (hold down CTRL or SHIFT to multi-select), then right-click and choose **Show in metadata translation editor**.

![Metadata Translation Editor](~/content/assets/images/metadata-translation-editor.png)

Use the input fields in the metadata translation editor to quickly add/remove or edit translations of object names, descriptions and display folder names for the corresponding language. The first three columns in the editor allow you to change the default names, descriptions and display folder names of objects. You can use Undo (Ctrl+Z) and Redo (Ctrl+Y) the usual way.

To remove a translation, clear its cell and press **Enter**. Clearing the default **Description** or **Display folder** cell empties that property. The default **Name** can't be cleared. The **Display folder** cells of the model, tables, hierarchy levels and perspectives are read-only.

## Metadata Translation Editor toolbar

While the Metadata Translation Editor is active, the accompanying toolbar provides the following options:

- ![Metadata Translation Editor New Translation](~/content/assets/images/metadata-translation-editor-add-translation.png) **New translation**: This button adds a new translation to the model. The translation appears in the Metadata Translation Editor. 
- ![Metadata Translation Editor Hide Members](~/content/assets/images/perspective-editor-hide-members.png) **Show/Hide hidden objects**: Enable this option if you want to see all objects in the Metadata Translation Editor, including hidden objects.
- ![Metadata Translation Editor Hide Names](~/content/assets/images/metadata-translation-editor-name.png) **Show/Hide names**: Disable this option if you don't want to see the name translation columns in Metadata Translation Editor.
- ![Metadata Translation Editor Hide Descriptions](~/content/assets/images/metadata-translation-editor-description.png) **Show/Hide descriptions**: Disable this option if you don't want to see the description translation columns in Metadata Translation Editor
- ![Metadata Translation Editor Hide Display Folders](~/content/assets/images/perspective-editor-folder.png) **Show/Hide display folders**: Disable this option if you don't want to see the display folder translation columns in Metadata Translation Editor

## Working with many translations

If you're working on a model with many translations, it may be impractical to display all of them at once. You can rearrange the display order of translations in the Metadata Translation Editor, by dragging the column headers around, making it easier to compare translations side-by-side. Moreover, you can add/remove translations from the editor at any time, through the right-click context menu:

<!-- SCREENSHOT RESHOOT (3.27.1): metadata-translation-editor-columns-bands.png. The header context menu no longer has Show Auto Filter Row. -->
![Metadata Translation Editor Columns](~/content/assets/images/metadata-translation-editor-columns-bands.png)