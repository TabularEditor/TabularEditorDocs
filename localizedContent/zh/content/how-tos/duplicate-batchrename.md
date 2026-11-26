---
uid: duplicate-and-batch
title: 复制对象和批量重命名
author: Morten Lønskov
updated: 2026-10-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 复制对象和批量重命名

在资源管理器树中右键点击即可打开上下文菜单，用于复制度量值和列。复制后的对象名称会自动追加“copy”后缀。此外，你也可以选中多个对象，然后在资源管理器树中右键点击以进行批量重命名。

![批量重命名对话框](~/content/assets/images/getting-started-te-03.png)

你可以在重命名时使用正则表达式 RegEx，并可选择是否也要重命名翻译内容。

复制的对象会保留原始对象所携带的所有错误和警告指示符，因此，具有无效表达式的对象的副本会立即被标记为无效。

如果原始对象显示在多个显示文件夹中，则副本会出现在其中的每个文件夹中，并在创建后被选中。这同样适用于复制并粘贴对象的情况。
