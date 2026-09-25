# SQL Server 2017 支持

Starting from version 2.3, Tabular Editor now also supports SQL Server 2017 (Compatibility Level 1400). 这意味着 Tabular Editor 的界面现已支持[这里](https://blogs.msdn.microsoft.com/analysisservices/2017/04/19/whats-new-in-sql-server-2017-ctp-2-0-for-analysis-services/)中介绍的部分新功能。

Please note, however, that you need to download the [proper build of Tabular Editor](https://github.com/TabularEditor/TabularEditor/releases/tag/2.5-CL1400) to use these features. 原因是：Microsoft 为 SQL Server 2017 / SSDT 17.0 提供了一组新的客户端库，而这些库与面向 SQL Server 2016 构建的 Tabular Editor 不兼容。 The new libraries can be obtained through the new [version of SSDT](https://docs.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools-ssdt) (requires Visual Studio 2015).

如果你不需要兼容级别 1400 的功能，仍然可以使用面向 SQL Server 2016 构建的 [Tabular Editor](https://github.com/TabularEditor/TabularEditor/releases/tag/2.5)。

下面快速介绍一下如何在 Tabular Editor 中使用这些新功能：

## 日期关系

现在，所有关系都会在属性网格中显示“Join on Date Behavior”属性：

![image](~/content/assets/images/sql-server-2017-support-01.png)

## 变体（列/层级重用）

你可以通过在属性网格中展开“Variations”属性来设置列的变体：

![image](~/content/assets/images/sql-server-2017-support-02.png)

另外，你也可以在列级别指定 **对象级安全性**。

点击省略号按钮将打开“变体集合编辑器”，你可以在其中配置列和层级在 Power BI 中的呈现方式：

![image](~/content/assets/images/sql-server-2017-support-03.png)

别忘了在表级别将“Show As Variations Only”属性设置为“True”：

![image](~/content/assets/images/sql-server-2017-support-04.png)

**Detail Row Expressions** can be set directly on tables and measures. At this time, however, no syntax highlighting or IntelliSense is available.

层级对象新增了**隐藏成员**属性，对参差层级很有用。
