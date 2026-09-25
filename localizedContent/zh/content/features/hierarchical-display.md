---
uid: hierarchical-display
title: 层级显示
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

# 层级显示

已加载模型中的对象会显示在 TOM Explorer 树状视图中。 By default, all object types (visible tables, roles, relationships, etc.) are shown. If you only want to see tables, measures, columns and hierarchies, go to the "View" menu and toggle off "Show all object types".

![](~/content/assets/images/hierarchical-display-01.png)

Expanding a table in the "Tables" group, you will find the measures, columns and hierarchies contained in the table presented in their respective display folders by default. This way, objects are arranged similar to how end-users would see them in client tools:

![](~/content/assets/images/hierarchical-display-02.png)

Use the buttons immediately above the Explorer Tree, to toggle invisible objects, display folders, measures, columns and hierarchies, or to filter objects by name. You can rename an object by selecting it in then hitting F2. This also works for display folders. If you double-click a measure or calculated column, you may edit its [DAX expression](dax-editor.md). Right-clicking will show a context menu, providing a range of handy shortcuts for operations such as setting visibility, perspective inclusion, adding columns to a hierarchy, etc.
