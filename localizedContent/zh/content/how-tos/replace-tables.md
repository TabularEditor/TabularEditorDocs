---
uid: replace-tables
title: 替换表格
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 替换表格

你只需复制(CTRL+C)一张表——甚至可以从 Tabular Editor 的另一个实例中复制——然后选中要替换的表，再按下粘贴(CTRL+V)即可。 A prompt will ask you to confirm whether you really want to replace the table ("Yes"), insert as a new table ("No") or cancel the operation entirely:

![image](~/content/assets/images/replace-tables-01.png)

如果你选择“Yes”，所选表将被剪贴板中的表替换。 Furthermore, all relationships pointing to or from that table will be updated to use the new table. For this to work, columns participating in relationships must have the same name and data type in both the original table, and the inserted table.