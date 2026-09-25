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

The right-click context menu in the Explorer Tree lets you duplicate measures and columns. The duplicated objects will have their names suffixed by "copy". Furthermore, you can perform batch renames by selecting multiple objects and right-clicking in the Explorer Tree.

![Batch rename dialog](~/content/assets/images/getting-started-te-03.png)

你可以在重命名时使用正则表达式 RegEx，并可选择是否也要重命名翻译内容。

A duplicated object keeps whatever error and warning indicators the original carried, so a copy of an object with an invalid expression is marked as invalid straight away.