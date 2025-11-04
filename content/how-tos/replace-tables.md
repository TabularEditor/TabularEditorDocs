## Replace tables
As of version 2.7, you can now replace a table simply by copying (CTRL+C) one table - even from another instance of Tabular Editor - and then selecting the table you want to replace, before hitting paste (CTRL+V). A prompt will ask you to confirm whether you really want to replace the table ("Yes"), insert as a new table ("No") or cancel the operation entirely:

![image](https://user-images.githubusercontent.com/8976200/36545892-40983114-17ea-11e8-8825-e8de6fd4e284.png)

If you choose "Yes", the selected table will be replaced with the table in the clipboard. Furthermore, all relationships pointing to or from that table will be updated to use the new table. For this to work, columns participating in relationships must have the same name and data type in both the original table, and the inserted table.