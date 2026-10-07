---
uid: duplicate-and-batch
title: Duplicating Objects and Batch Rename
author: Morten Lønskov
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Duplicate objects and batch renamings
The right-click context menu in the Explorer Tree lets you duplicate measures and columns. The duplicated objects will have their names suffixed by "copy". Furthermore, you can perform batch renames by selecting multiple objects and right-clicking in the Explorer Tree.

![Batch rename dialog](~/content/assets/images/getting-started-te-03.png)

You may use RegEx for your renamings, and optionally choose whether translations should be renamed as well.

A duplicated object keeps whatever error and warning indicators the original carried, so a copy of an object with an invalid expression is marked as invalid straight away.