---
uid: importing-tables-from-excel
title: 从 Excel 导入表格
author: Daniel Otykier
updated: 2021-11-10
---

# 从 Excel 导入表格

如果你需要将 Excel 工作表作为表添加到表格模型中，可以使用 Tabular Editor 2.x 和 Excel ODBC 驱动程序来实现。

# 先决条件

Tabular Editor 2.x 是一款 32 位应用程序，而大多数人通常安装的是 64 位版本的 Office（其中包含 64 位 Excel ODBC 驱动程序）。 遗憾的是，Tabular Editor 2.x 无法使用 64 位驱动程序；如果你已安装 64 位 Office，直接下载并尝试安装 32 位驱动程序会报错。 不过，你可以通过以下变通方法，在已安装 64 位 Office 的情况下并行安装 32 位 Excel ODBC 驱动程序：

1. 从这里下载 32 位版本的驱动程序：https://www.microsoft.com/en-us/download/details.aspx?id=54920
2. 解压 AccessDatabaseEngine.exe 文件
3. 在解压后的文件中，你会找到 aceredist.msi 文件。请在命令行中使用 /passive 参数运行：

  ```shell
  aceredist.msi /passive
  ```

4. 在“ODBC 数据源（32 位）”配置中确认安装是否成功（在 Windows 开始菜单中搜索“ODBC”，平台应显示“32/64 位”，如下图所示）：
   ![Excel Odbc 32 64](~/content/assets/images/excel-odbc-32-64.png)

# 设置 ODBC 数据源

按上述步骤确认已安装 32 位 ODBC Excel 驱动程序后，要在 Tabular Editor 2.x 中从 Excel 文件添加表，需要执行以下步骤：

1. 在 Tabular Editor 中，右键单击模型，选择“导入表…”，然后点击“下一步”
2. 在“连接属性”对话框中，点击“更改…”。 选择“Microsoft ODBC 数据源”选项，然后点击“确定”。
3. 选择“使用连接字符串”，然后点击“生成…”。 选择“Excel 文件”，然后点击“确定”。
   ![Odbc Connection Properties Excel](~/content/assets/images/odbc-connection-properties-excel.png)
4. 找到你要从中加载表的 Excel 文件，然后点击“确定”。 这会生成类似下面这样的连接字符串：

  ```connectionstring
  Dsn=Excel Files;dbq=C:\Users\DanielOtykier\Documents\A Beer Dataset Calculation.xlsx;defaultdir=C:\Users\DanielOtykier\Documents;driverid=1046;maxbuffersize=2048;pagetimeout=5
  ```

5. 点击“OK”后，Tabular Editor 应显示该 Excel 文件中的工作表和数据区域列表。 遗憾的是，导入表向导目前无法预览数据，因为它生成了一条无效的 SQL 语句：
   ![Import Tables Excel](~/content/assets/images/import-tables-excel.png)
6. 不过，你仍然可以勾选要导入的表。 完成后点击“Import”，并忽略错误提示。
7. 在新添加的表上，找到分区并修改 SQL，去掉空方括号，以及工作表名称前面的点。 应用更改（按 F5）。
   ![修复分区表达式 Excel](~/content/assets/images/fix-partition-expressions-excel.png)
8. 然后，在分区上右键单击，选择“Refresh Table Metadata…”。 Tabular Editor 现在会通过 ODBC 驱动程序从 Excel 文件读取列元数据：
   ![Refresh Metadata Excel](~/content/assets/images/refresh-metadata-excel.png)
9. （可选）如果你不想使用 ODBC 来刷新表中的数据，就需要替换该分区，改用基于 M 的表达式来加载同一工作表的数据。 为此，在该表中添加一个新的 Power Query 分区（右键单击“Partitions”，然后选择“New Partition (Power Query")”）。 删除旧版分区。 然后，将新分区的 M 表达式设置为如下内容：

  ```M
  let
      Source = Excel.Workbook(File.Contents("<excel file path>"), null, true),
      Customer_Sheet = Source{[Item="<sheet name>",Kind="Sheet"]}[Data],
      #"Promoted Headers" = Table.PromoteHeaders(Customer_Sheet, [PromoteAllScalars=true])
  in
      #"Promoted Headers"
  ```

将 `<excel file path>` 和 `<sheet name>` 占位符替换为实际值。

# 结论

在 Tabular Editor 2.x 中可以从 Excel 文件导入表，但需要像上面那样使用 ODBC Excel 驱动程序，这会让流程更复杂一些。