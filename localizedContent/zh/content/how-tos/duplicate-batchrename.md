---
uid: duplicate-and-batch
title: 复制对象和批量重命名
author: Morten Lønskov
updated: 2026-09-14
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

复制出来的对象会保留原对象携带的错误和警告标识，因此，若原对象包含无效表达式，其副本也会立即被标记为无效。